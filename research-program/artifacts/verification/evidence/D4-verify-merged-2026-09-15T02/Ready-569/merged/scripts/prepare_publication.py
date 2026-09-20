"""Redact a publication copy, preserving local evidence and structured file validity.

This is an export step, not a guard bypass. Run check_publication_safety.py on
its output before publishing. Diagnostics deliberately never contain matches.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

if __package__:
    from .publication_patterns import PRIVATE_KEY_BLOCK, PRIVATE_KEY_HEADER
else:
    from publication_patterns import PRIVATE_KEY_BLOCK, PRIVATE_KEY_HEADER

REPLACEMENTS = (
    (
        "private-key",
        PRIVATE_KEY_BLOCK,
        "[REDACTED_PRIVATE_KEY]",
    ),
    (
        "credential",
        re.compile(r"(?:[REDACTED_CREDENTIAL]|[REDACTED_CREDENTIAL]|[REDACTED_CREDENTIAL]|[REDACTED_CREDENTIAL]|[REDACTED_CREDENTIAL]|[REDACTED_CREDENTIAL]|[REDACTED_CREDENTIAL])[A-Za-z0-9_-]*"),
        "[REDACTED_CREDENTIAL]",
    ),
    ("home-path", re.compile(r"[LOCAL_HOME]/\s\"'`<>]+/?"), "[LOCAL_HOME]/"),
    ("home-path", re.compile(r"[LOCAL_HOME]/"), "[LOCAL_HOME]/"),
    ("scratch-path", re.compile(r"[LOCAL_WORKSPACE]/|[LOCAL_WORKSPACE]/|[LOCAL_WORKSPACE]/"), "[LOCAL_WORKSPACE]/"),
    (
        "internal-host",
        re.compile(r"\b[A-Za-z0-9_.-]+\[LOCAL_HOST](?:[0-9]+)?|\blocalhost:[0-9]+|\[LOCAL_HOST]"),
        "[LOCAL_HOST]",
    ),
)


# These archived dispatch captures contain raw process output, despite their suffix.
# Preserve that output as an explicit JSON string in the public copy only.
TEXT_CAPTURE_JSON = frozenset(
    {
        "artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/breadth-dispatch.json",
        "artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/correctness-dispatch.json",
    }
)


def redact_text(text: str, counts: Counter[str]) -> str:
    for rule, pattern, replacement in REPLACEMENTS:
        text, count = pattern.subn(replacement, text)
        counts[rule] += count
    if PRIVATE_KEY_HEADER.search(text):
        raise ValueError("incomplete private-key block cannot be safely redacted")
    return text


def unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject ambiguous input before JSON decoding can discard earlier values."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def redact_value(value: object, counts: Counter[str]) -> object:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, str):
        return redact_text(value, counts)
    if isinstance(value, list):
        return [redact_value(item, counts) for item in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            new_key = redact_text(key, counts)
            if new_key in result:
                raise ValueError("redaction would collapse distinct JSON keys")
            result[new_key] = redact_value(item, counts)
        return result
    return value


def needs_redaction(text: str, structured: bool) -> bool:
    """Inspect decoded JSON strings before the clean-file shortcut, including keys."""
    patterns = [PRIVATE_KEY_HEADER, *(pattern for _, pattern, _ in REPLACEMENTS)]
    if any(pattern.search(text) for pattern in patterns):
        return True
    if structured:
        for match in re.finditer(r'"(?:[^"\\]|\\.)*"', text):
            value = json.loads(match.group())
            if any(pattern.search(value) for pattern in patterns):
                return True
    return False


def prepare_copy(root: Path) -> Counter[str]:
    """Operate only on the caller's staging tree; fail before writing on errors."""
    if not root.is_dir() or root.is_symlink():
        raise ValueError("publication copy must be an existing non-symlink directory")
    counts: Counter[str] = Counter()
    pending: list[tuple[Path, bytes]] = []
    files = 0

    def walk_error(error: OSError) -> None:
        raise error

    for directory, dirnames, filenames in root.walk(on_error=walk_error, follow_symlinks=False):
        for name in [*dirnames, *filenames]:
            if (directory / name).is_symlink():
                raise ValueError("publication copy contains a symlink")
        for name in filenames:
            path = directory / name
            if not path.is_file():
                # read_bytes() on a FIFO BLOCKS FOREVER waiting for a writer, so an unsafe
                # staging tree would hang preparation instead of being rejected by it. The
                # guard already refuses non-regular files (check_publication_safety.py);
                # preparation has to fail closed the same way, or the two disagree about what
                # is publishable and the safer one is the one that never runs.
                raise ValueError(f"{path.relative_to(root).as_posix()}: not a regular file")
            original = path.read_bytes()
            files += 1
            try:
                text = original.decode("utf-8")
            except UnicodeError:
                # Binary artifacts are preserved; the byte scanner remains authoritative.
                continue
            file_counts: Counter[str] = Counter()
            try:
                # Historical process captures may not be complete JSON documents.
                # Preserve their clean bytes; affected structured files must parse.
                if not needs_redaction(text, path.suffix.lower() in {".json", ".jsonl"}):
                    continue
                value: object
                if path.suffix.lower() == ".json":
                    if path.relative_to(root).as_posix() in TEXT_CAPTURE_JSON:
                        value = {
                            "capture_format": "raw-process-output",
                            "text": redact_text(text, file_counts),
                        }
                    else:
                        value = redact_value(
                            json.loads(text, object_pairs_hook=unique_json_object), file_counts
                        )
                    replacement = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
                elif path.suffix.lower() == ".jsonl":
                    replacement = (
                        "\n".join(
                            (
                                json.dumps(
                                    redact_value(
                                        json.loads(line, object_pairs_hook=unique_json_object),
                                        file_counts,
                                    ),
                                    ensure_ascii=False,
                                )
                                if line.strip()
                                else ""
                            )
                            for line in text.splitlines()
                        )
                        + "\n"
                    )
                else:
                    replacement = redact_text(text, file_counts)
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    "publication copy has invalid or ambiguous structured data"
                ) from exc
            if any(file_counts.values()):
                counts.update(file_counts)
                pending.append((path, replacement.encode("utf-8")))
    if files == 0:
        raise ValueError("publication copy is empty")
    for path, content in pending:
        path.write_bytes(content)
    counts["files_scanned"] = files
    counts["files_redacted"] = len(pending)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staging-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        counts = prepare_copy(args.staging_root)
    except (OSError, ValueError):
        print("ERROR: publication preparation failed; do not publish this copy")
        return 1
    print(" ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
