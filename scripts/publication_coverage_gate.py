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
    if not isinstance(report, dict) or not isinstance(baseline, dict):
        return ["Coverage report and baseline must be JSON objects"]
    errors = []
    floors = baseline.get("publication_scripts", {})
    if not isinstance(floors, dict) or set(floors) != set(PUBLICATION_FILES):
        return ["publication_scripts must name exactly the two Ready-owned scripts"]
    files = report.get("files", {})
    if not isinstance(files, dict):
        return ["Coverage report files must be a JSON object"]
    unexpected = set(files) - set(PUBLICATION_FILES)
    unexpected = {name for name in unexpected if not name.startswith("src/")}
    if unexpected:
        errors.append(f"Synced or unrelated files measured: {sorted(unexpected)}")
    for name in PUBLICATION_FILES:
        if name not in files:
            errors.append(f"{name}: missing coverage measurement")
            continue
        measurement = files[name]
        if not isinstance(measurement, dict):
            errors.append(f"{name}: coverage measurement must be a JSON object")
            continue
        summary = measurement.get("summary", {})
        if not isinstance(summary, dict) or not isinstance(floors[name], dict):
            errors.append(f"{name}: coverage summary and floors must be JSON objects")
            continue
        for metric, covered, total in (
            ("line", "covered_lines", "num_statements"),
            ("branch", "covered_branches", "num_branches"),
        ):
            floor = floors[name].get(metric)
            hit, count = summary.get(covered), summary.get(total)
            if (
                not isinstance(floor, (int, float))
                or type(hit) is not int
                or type(count) is not int
            ):
                errors.append(f"{name}: invalid {metric} measurement or floor")
                continue
            try:
                finite_numbers = all(
                    not isinstance(v, bool) and math.isfinite(v) for v in (floor, hit, count)
                )
            except OverflowError:
                # JSON integers are unbounded; math.isfinite converts them to float.
                finite_numbers = False
            if not finite_numbers or not 0 <= floor <= 100 or count <= 0 or not 0 <= hit <= count:
                errors.append(f"{name}: invalid {metric} measurement or floor")
            elif 100 * hit / count < floor:
                errors.append(
                    f"{name}: {metric} coverage {100 * hit / count:.6f}% below floor {floor:.6f}%"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path("coverage.json"))
    parser.add_argument("--baseline", type=Path, default=Path("config/coverage-baseline.json"))
    args = parser.parse_args()
    documents = {}
    for name, path in (("report", args.report), ("baseline", args.baseline)):
        try:
            documents[name] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"Cannot load publication coverage {name} {path}: {exc}")
            return 1
    errors = check_report(documents["report"], documents["baseline"])
    print("\n".join(errors) if errors else "Ready publication coverage floors PASS")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
