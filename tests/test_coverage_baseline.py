"""Guard config/coverage-baseline.json against silently regressing the choices this repo made.

Ready's whole purpose is to exercise the fleet coverage pipeline end-to-end, so the baseline
file's fields aren't cosmetic: `line` (not `coverage`) exercises the precedence path both
tools/coverage_trend.py and tools/coverage_guard.py implement, and its value must agree with
coverage-min in pr-00-gate.yml and fail_under in pyproject.toml or the three drift apart.
"""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = REPO_ROOT / "config" / "coverage-baseline.json"
CI_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"
PR_GATE_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "pr-00-gate.yml"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"


def _load_baseline() -> dict:
    return json.loads(BASELINE_PATH.read_text())


def test_baseline_file_exists() -> None:
    assert BASELINE_PATH.is_file(), (
        "config/coverage-baseline.json must exist so Maint Coverage Guard has something to "
        "compare against instead of reporting baseline_status=absent."
    )


def test_baseline_keys_line_not_coverage() -> None:
    baseline = _load_baseline()
    assert "line" in baseline, (
        "Baseline must key coverage as `line`: coverage_trend.py and coverage_guard.py both "
        "accept `line` or `coverage`, with `line` taking precedence, and exercising that "
        "precedence path is the point of a conformance repo."
    )
    assert "coverage" not in baseline, (
        "Do not also set `coverage` -- that reintroduces the ambiguity `line` precedence is "
        "meant to resolve."
    )


def _coverage_min(path: Path) -> float:
    match = re.search(
        r"(?m)^[ \t]*coverage-min[ \t]*:[ \t]*([\"']?)(\d+(?:\.\d+)?)\1[ \t]*(?:#.*)?$",
        path.read_text(),
    )
    assert match, f"{path.name} must set a numeric coverage-min."
    return float(match.group(2))


def test_baseline_matches_ci_gate_and_pyproject() -> None:
    baseline = _load_baseline()
    ci_min = _coverage_min(CI_WORKFLOW_PATH)
    gate_min = _coverage_min(PR_GATE_WORKFLOW_PATH)

    pyproject_text = PYPROJECT_PATH.read_text()
    coverage_report = re.search(
        r"(?ms)^\[tool\.coverage\.report\][ \t]*\n(.*?)(?=^\[|\Z)", pyproject_text
    )
    assert coverage_report, "pyproject.toml must define [tool.coverage.report]."
    fail_under_match = re.search(
        r"(?m)^[ \t]*fail_under[ \t]*=[ \t]*(\d+(?:\.\d+)?)[ \t]*(?:#.*)?$",
        coverage_report.group(1),
    )
    assert fail_under_match, "pyproject.toml [tool.coverage.report] must set fail_under."
    fail_under = float(fail_under_match.group(1))

    assert baseline["line"] == ci_min == gate_min == fail_under == 80.0, (
        "config/coverage-baseline.json `line`, ci.yml and pr-00-gate.yml `coverage-min`, "
        "and pyproject.toml `fail_under` must all agree (80) so the four don't drift apart: "
        f"line={baseline['line']!r}, ci={ci_min!r}, gate={gate_min!r}, "
        f"fail_under={fail_under!r}"
    )


def test_baseline_has_warn_drop_and_recovery_days() -> None:
    """Coverage recovery controls must reject ambiguous or non-finite JSON numbers."""
    baseline = _load_baseline()
    warn_drop = baseline.get("warn_drop")
    assert (
        isinstance(warn_drop, (int, float))
        and not isinstance(warn_drop, bool)
        and math.isfinite(warn_drop)
    ), (
        "warn_drop must be a finite numeric value excluding booleans -- it's the coverage-point "
        "drop that triggers a warning before a breach issue is opened."
    )
    assert type(baseline.get("recovery_days")) is int, (
        "recovery_days must be an exact int excluding booleans -- consecutive passing days required before a breach "
        "issue auto-closes."
    )
    assert baseline["recovery_days"] > 0


PUBLICATION_FILES = {
    "scripts/check_publication_safety.py",
    "scripts/prepare_publication.py",
}


def test_publication_source_and_baseline_notes_agree():
    import shlex
    import tomllib

    config = tomllib.loads(PYPROJECT_PATH.read_text())
    assert set(config["tool"]["coverage"]["run"]["include"]) == {
        "src/**",
        "scripts/check_publication_safety.py",
        "scripts/prepare_publication.py",
    }
    args = shlex.split(config["tool"]["pytest"]["ini_options"]["addopts"])
    assert "--cov" in args and not any(a.startswith("--cov=") for a in args)
    assert "source" not in config["tool"]["coverage"]["run"]
    assert (
        config["tool"]["coverage"]["report"]["include"]
        == config["tool"]["coverage"]["run"]["include"]
    )
    assert "--cov-report=json" in args
    assert config["tool"]["coverage"]["run"]["patch"] == ["subprocess"]
    baseline = _load_baseline()
    assert set(baseline["publication_scripts"]) == PUBLICATION_FILES
    assert "Ready-owned publication scripts" in baseline["notes"]
    assert "synced fleet tooling remains excluded" in baseline["notes"]


def test_measured_file_set_includes_unexecuted_source_and_excludes_tooling(tmp_path: Path) -> None:
    """Exercise the real pytest hooks and config, including source discovery."""
    for relative in (
        "pyproject.toml",
        "config/coverage-baseline.json",
        "scripts/publication_coverage_gate.py",
        "tests/conftest.py",
    ):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / relative, destination)

    unexecuted = tmp_path / "src/my_project/unexecuted.py"
    unexecuted.parent.mkdir(parents=True)
    unexecuted.write_text('raise RuntimeError("source discovery must not execute this file")\n')

    exercised_files = sorted(PUBLICATION_FILES) + [
        "scripts/ci_coverage_delta.py",
        "tests/fixtures/scripts/check_publication_safety.py",
        "tests/fixtures/scripts/prepare_publication.py",
    ]
    for relative in exercised_files:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("def choose(flag):\n    if flag:\n        return 1\n    return 0\n")
    (tmp_path / "tests/test_exercise.py").write_text(
        "import runpy\n\n"
        "def test_exercise():\n"
        f"    for path in {exercised_files!r}:\n"
        "        choose = runpy.run_path(path)['choose']\n"
        "        assert choose(True) == 1\n"
        "        assert choose(False) == 0\n"
    )
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("COVERAGE_", "COV_CORE_")) and key != "PYTEST_ADDOPTS"
    }
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-m", "not slow"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((tmp_path / "coverage.json").read_text())
    assert set(report["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    summary = report["files"]["src/my_project/unexecuted.py"]["summary"]
    assert summary["num_statements"] == 1
    assert summary["covered_lines"] == 0


def _measured_report():
    return {
        "files": {
            name: {
                "summary": {
                    "covered_lines": 100,
                    "num_statements": 100,
                    "covered_branches": 100,
                    "num_branches": 100,
                }
            }
            for name in PUBLICATION_FILES
        }
    }


def test_each_publication_file_and_metric_is_enforced():
    import copy

    from scripts.publication_coverage_gate import check_report

    baseline = _load_baseline()
    report = _measured_report()
    assert check_report(report, baseline) == []
    for name in PUBLICATION_FILES:
        for metric in ("covered_lines", "covered_branches"):
            changed = copy.deepcopy(report)
            changed["files"][name]["summary"][metric] = 0
            assert any(name in e and "below floor" in e for e in check_report(changed, baseline))
        changed = copy.deepcopy(report)
        del changed["files"][name]
        assert any(name in e and "missing" in e for e in check_report(changed, baseline))
    report["files"]["scripts/ci_coverage_delta.py"] = {}
    assert any("unrelated" in e for e in check_report(report, baseline))


def test_publication_measurements_fail_closed():
    import copy

    from scripts.publication_coverage_gate import check_report

    baseline = _load_baseline()
    for invalid in (None, True, float("nan"), -1):
        changed = copy.deepcopy(baseline)
        changed["publication_scripts"]["scripts/prepare_publication.py"]["line"] = invalid
        assert check_report(_measured_report(), changed)
    report = _measured_report()
    report["files"]["scripts/prepare_publication.py"]["summary"]["num_branches"] = 0
    assert check_report(report, baseline)


def test_cov_reset_skips_publication_hooks_without_crash() -> None:
    """`--cov-reset` clears sources without registering `_cov`; hooks must no-op."""
    env = os.environ.copy()
    env.pop("PYTEST_ADDOPTS", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_coverage_baseline.py::test_baseline_file_exists",
            "-q",
            "--cov-reset",
            "-p",
            "no:cacheprovider",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert "INTERNALERROR" not in combined
    assert "AttributeError" not in combined
    assert "PUBLICATION COVERAGE:" not in combined
