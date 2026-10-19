"""Ready-only non-regression gate for its publication scanner and preparer.

The fleet aggregate coverage threshold remains separate. Coverage measures exercised
lines and branches; it does not certify publication safety.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

PUBLICATION_FILES = (
    "scripts/check_publication_safety.py",
    "scripts/prepare_publication.py",
)


def check_report(report: dict[str, Any], baseline: dict[str, Any]) -> list[str]:
    """Reject absent measurements and independent line or branch regressions."""
    errors = []
    floors = baseline.get("publication_scripts", {})
    if set(floors) != set(PUBLICATION_FILES):
        return ["publication_scripts must name exactly the two Ready-owned scripts"]
    files = report.get("files", {})
    unexpected = set(files) - set(PUBLICATION_FILES)
    unexpected = {name for name in unexpected if not name.startswith("src/")}
    if unexpected:
        errors.append(f"Synced or unrelated files measured: {sorted(unexpected)}")
    for name in PUBLICATION_FILES:
        if name not in files:
            errors.append(f"{name}: missing coverage measurement")
            continue
        summary = files[name].get("summary", {})
        for metric, covered, total in (
            ("line", "covered_lines", "num_statements"),
            ("branch", "covered_branches", "num_branches"),
        ):
            floor = floors[name].get(metric)
            hit, count = summary.get(covered), summary.get(total)
            values = (floor, hit, count)
            if (
                any(
                    isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
                    for v in values
                )
                or not 0 <= floor <= 100
                or count <= 0
                or not 0 <= hit <= count
            ):
                errors.append(f"{name}: invalid {metric} measurement or floor")
            elif 100 * hit / count + 1e-9 < floor:
                errors.append(
                    f"{name}: {metric} coverage {100 * hit / count:.6f}% below floor {floor:.6f}%"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path("coverage.json"))
    parser.add_argument("--baseline", type=Path, default=Path("config/coverage-baseline.json"))
    args = parser.parse_args()
    errors = check_report(
        json.loads(args.report.read_text()), json.loads(args.baseline.read_text())
    )
    print("\n".join(errors) if errors else "Ready publication coverage floors PASS")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
