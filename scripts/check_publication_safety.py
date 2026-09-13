"""Check published research files without echoing potentially sensitive content."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path, PurePosixPath

RULES = {
    "home-path": re.compile(rb"/Users/"),
    "credential": re.compile(rb"sk-ant-|sk-proj-|ghp_|github_pat_|lsv2_|crsr_|AIza"),
    "private-key": re.compile(rb"BEGIN (?:RSA|OPENSSH) PRIVATE KEY"),
    "scratch-path": re.compile(rb"clones/|/private/tmp/|scratchpad/"),
    "internal-host": re.compile(rb"\.local:|\blocalhost:[0-9]+"),
}
DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "research-program"


def load_allowlist(root: Path) -> tuple[set[tuple[str, str]], list[str]]:
    """Require exact paths, known rules, and a nonempty documented reason."""
    allowed: set[tuple[str, str]] = set()
    errors: list[str] = []
    path = root / ".publication-allow"
    if not path.exists():
        return allowed, errors
    if path.is_symlink():
        return allowed, [".publication-allow: symlinks are not allowed"]
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return allowed, [".publication-allow: cannot read UTF-8 allowlist"]
    for number, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        entry, separator, reason = line.partition(" #")
        name, colon, rule = entry.strip().rpartition(":")
        valid_path = (
            bool(name)
            and name != ".publication-allow"
            and not PurePosixPath(name).is_absolute()
            and ".." not in PurePosixPath(name).parts
            and not any(char in name for char in "*?[]\\")
            and PurePosixPath(name).as_posix() == name
        )
        if name == ".publication-allow":
            errors.append(f".publication-allow:{number}: cannot allowlist the allowlist file itself")
        elif not separator or not reason.strip() or not colon or not valid_path or rule not in RULES:
            errors.append(f".publication-allow:{number}: expected exact path:rule # reason")
        elif not (root / name).is_file():
            errors.append(f".publication-allow:{number}: target file does not exist")
        else:
            allowed.add((name, rule))
    return allowed, errors


def scan(root: Path) -> int:
    """Scan bytes in every file; fail closed for missing, unreadable, or linked files."""
    allowed, errors = load_allowlist(root)
    counts: Counter[str] = Counter()
    files_scanned = 0
    exceptions = 0
    if not root.is_dir() or root.is_symlink():
        errors.append("research root must be an existing directory, not a symlink")
    else:
        # Path.walk exposes traversal errors rather than silently skipping them.
        def walk_error(_error: OSError) -> None:
            errors.append("research tree contains an unreadable directory")

        for directory, _, filenames in root.walk(on_error=walk_error):
            for filename in sorted(filenames):
                path = directory / filename
                name = path.relative_to(root).as_posix()
                if path.is_symlink():
                    errors.append(f"{name}: symlinks are not allowed")
                    continue
                try:
                    content = path.read_bytes()
                except OSError:
                    errors.append(f"{name}: cannot read file")
                    continue
                files_scanned += 1
                for number, line in enumerate(content.splitlines(), 1):
                    for rule, pattern in RULES.items():
                        hits = len(pattern.findall(line))
                        if not hits:
                            continue
                        if (name, rule) in allowed:
                            exceptions += hits
                        else:
                            counts[rule] += hits
                            print(f"{name}:{number}: {rule} ({hits} hit(s))")
    if files_scanned == 0:
        errors.append("zero files scanned")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"files_scanned={files_scanned} "
        + " ".join(f"{rule}={counts[rule]}" for rule in RULES)
        + f" allowed_hits={exceptions} errors={len(errors)}"
    )
    return int(bool(errors or any(counts.values())))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    return scan(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
