"""Redact a publication copy, preserving local evidence and structured file validity.

This is an export step, not a guard bypass. Run check_publication_safety.py on
its output before publishing. Diagnostics deliberately never contain matches.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

REPLACEMENTS = (
    (
        "private-key",
        re.compile(
            r"-----BEGIN (RSA|OPENSSH) PRIVATE KEY-----.*?-----END \1 PRIVATE KEY-----", re.S
        ),
        "[REDACTED_PRIVATE_KEY]",
    ),
    ("private-key", re.compile(r"BEGIN (?:RSA|OPENSSH) PRIVATE KEY"), "[PRIVATE_KEY_HEADER]"),
    (
        "credential",
        re.compile(r"(?:sk-ant-|sk-proj-|ghp_|github_pat_|lsv2_|crsr_|AIza)[A-Za-z0-9_-]*"),
        "[REDACTED_CREDENTIAL]",
    ),
    ("home-path", re.compile(r"/Users/[^/\s\"'`<>]+/?"), "[LOCAL_HOME]/"),
    ("home-path", re.compile(r"/Users/"), "[LOCAL_HOME]/"),
    ("scratch-path", re.compile(r"clones/|/private/tmp/|scratchpad/"), "[LOCAL_WORKSPACE]/"),
    (
        "internal-host",
        re.compile(r"\b[A-Za-z0-9_.-]+\.local:(?:[0-9]+)?|\blocalhost:[0-9]+|\.local:"),
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
    return text


def redact_value(value: object, counts: Counter[str]) -> object:
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
    if any(pattern.search(text) for _, pattern, _ in REPLACEMENTS):
        return True
    if structured:
        for match in re.finditer(r'"(?:[^"\\]|\\.)*"', text):
            value = json.loads(match.group())
            if any(pattern.search(value) for _, pattern, _ in REPLACEMENTS):
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
                        value = redact_value(json.loads(text), file_counts)
                    replacement = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
                elif path.suffix.lower() == ".jsonl":
                    replacement = (
                        "\n".join(
                            (
                                json.dumps(
                                    redact_value(json.loads(line), file_counts), ensure_ascii=False
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
