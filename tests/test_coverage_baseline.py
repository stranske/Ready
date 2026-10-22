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

import pytest

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
    assert config["tool"]["coverage"]["run"]["branch"] is True
    assert config["tool"]["coverage"]["run"]["patch"] == ["subprocess"]
    baseline = _load_baseline()
    assert set(baseline["publication_scripts"]) == PUBLICATION_FILES
    assert "Ready-owned publication scripts" in baseline["notes"]
    assert "synced fleet tooling remains excluded" in baseline["notes"]


@pytest.fixture
def coverage_project(tmp_path: Path) -> Path:
    """Isolate the real coverage config and hooks with small, fully exercised scripts."""
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
    return tmp_path


def _run_coverage_project(project: Path, *pytest_args: str) -> subprocess.CompletedProcess[str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("COVERAGE_", "COV_CORE_")) and key != "PYTEST_ADDOPTS"
    }
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-m", "not slow", *pytest_args],
        cwd=project,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def _exercise_in_subprocess(project: Path) -> None:
    """Run the fixture's current assertions through a real Python child process."""
    exercise = project / "tests/test_exercise.py"
    (project / "exercise_cli.py").write_text(exercise.read_text() + "\ntest_exercise()\n")
    exercise.write_text(
        "import subprocess\nimport sys\n\n"
        "def test_exercise():\n"
        "    subprocess.run([sys.executable, 'exercise_cli.py'], check=True)\n"
    )


@pytest.mark.parametrize("execution", ["in-process", "subprocess"])
@pytest.mark.parametrize("source_directory", ["src/my_project", "src/my_project/nested/package"])
def test_measured_file_set_includes_unexecuted_source_and_excludes_tooling(
    coverage_project: Path, execution: str, source_directory: str
) -> None:
    """Keep tooling and fixture copies excluded in both parent and child processes."""
    original = coverage_project / "src/my_project/unexecuted.py"
    source = coverage_project / source_directory / "unexecuted.py"
    source.parent.mkdir(parents=True, exist_ok=True)
    original.rename(source)
    if execution == "subprocess":
        _exercise_in_subprocess(coverage_project)

    result = _run_coverage_project(coverage_project)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((coverage_project / "coverage.json").read_text())
    source_name = source.relative_to(coverage_project).as_posix()
    assert set(report["files"]) == PUBLICATION_FILES | {source_name}
    summary = report["files"][source_name]["summary"]
    assert summary["num_statements"] == 1
    assert summary["covered_lines"] == 0


@pytest.mark.parametrize("execution", ["in-process", "subprocess"])
@pytest.mark.parametrize("source_directory", ["src/my_project", "src/my_project/nested/package"])
def test_unexecuted_product_branches_still_fail_aggregate_gate(
    coverage_project: Path, execution: str, source_directory: str
) -> None:
    """Exact script selection must preserve the aggregate gate for unexecuted product code."""
    original = coverage_project / "src/my_project/unexecuted.py"
    source = coverage_project / source_directory / "unexecuted.py"
    source.parent.mkdir(parents=True, exist_ok=True)
    original.rename(source)
    source.write_text("def choose(flag):\n    if flag:\n        return 1\n    return 0\n")
    if execution == "subprocess":
        _exercise_in_subprocess(coverage_project)

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert "FAIL Required test coverage of 80" in output
    assert "PUBLICATION COVERAGE:" not in output
    assert "INTERNALERROR" not in output

    report = json.loads((coverage_project / "coverage.json").read_text())
    source_name = source.relative_to(coverage_project).as_posix()
    assert set(report["files"]) == PUBLICATION_FILES | {source_name}
    summary = report["files"][source_name]["summary"]
    assert summary["num_statements"] == 4
    assert summary["num_branches"] == 2
    assert summary["covered_lines"] == summary["covered_branches"] == 0
    assert report["totals"]["percent_covered"] < _load_baseline()["line"]
    for name in PUBLICATION_FILES:
        summary = report["files"][name]["summary"]
        assert summary["covered_lines"] == summary["num_statements"]
        assert summary["covered_branches"] == summary["num_branches"]


@pytest.mark.parametrize(
    "unrelated",
    [
        "scripts/ci_coverage_delta.py",
        "tests/fixtures/scripts/check_publication_safety.py",
        "tests/fixtures/scripts/prepare_publication.py",
    ],
)
def test_pytest_gate_rejects_unrelated_files_even_with_passing_coverage(
    coverage_project: Path, unrelated: str
) -> None:
    """Widening coverage to tooling or fixture copies must fail the measured-file gate."""
    config = coverage_project / "pyproject.toml"
    # Widen both run and report selection so real coverage data reaches the gate.
    config.write_text(
        config.read_text().replace(
            '"scripts/prepare_publication.py"]',
            f'"scripts/prepare_publication.py", "{unrelated}"]',
        )
    )

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: Synced or unrelated files measured: {[unrelated]!r}" in output
    assert "INTERNALERROR" not in output

    report = json.loads((coverage_project / "coverage.json").read_text())
    assert set(report["files"]) == PUBLICATION_FILES | {
        "src/my_project/unexecuted.py",
        unrelated,
    }
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
    for name in PUBLICATION_FILES | {unrelated}:
        summary = report["files"][name]["summary"]
        assert summary["covered_lines"] == summary["num_statements"]
        assert summary["covered_branches"] == summary["num_branches"]


@pytest.mark.parametrize("execution", ["in-process", "subprocess"])
def test_pytest_gate_preserves_test_failure_with_passing_coverage(
    coverage_project: Path, execution: str
) -> None:
    """Meeting every coverage floor must never turn a functional failure green."""
    from scripts.publication_coverage_gate import check_report

    if execution == "subprocess":
        _exercise_in_subprocess(coverage_project)
    exercise = coverage_project / "tests/test_exercise.py"
    original = exercise.read_text()
    exercise.write_text(original + '\n    raise AssertionError("intentional functional failure")\n')

    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 failed" in output
    assert "intentional functional failure" in output
    assert "PUBLICATION COVERAGE:" not in output
    assert "INTERNALERROR" not in output
    report_path = coverage_project / "coverage.json"
    report = json.loads(report_path.read_text())
    assert check_report(report, _load_baseline()) == []
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]

    exercise.write_text(original)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert json.loads(report_path.read_text())["files"] == report["files"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize("metric", ["line", "branch"])
@pytest.mark.parametrize("execution", ["in-process", "subprocess"])
def test_pytest_gate_rejects_independent_publication_regressions(
    coverage_project: Path, name: str, metric: str, execution: str
) -> None:
    """Passing tests and aggregate coverage cannot mask either script's regression."""
    script = coverage_project / name
    if metric == "line":
        # Leave every existing branch exercised, but add an unexecuted function body.
        script.write_text(script.read_text() + "\ndef untested():\n    return 0\n")
    else:
        # Exercise every line while leaving the implicit false branch uncovered.
        script.write_text(script.read_text().replace("    return 0\n", ""))
        exercise = coverage_project / "tests/test_exercise.py"
        exercise.write_text(
            exercise.read_text().replace(
                "        assert choose(False) == 0\n",
                f"        if path != {name!r}:\n            assert choose(False) == 0\n",
            )
        )

    if execution == "subprocess":
        _exercise_in_subprocess(coverage_project)

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: {name}: {metric} coverage" in output
    assert "below floor" in output
    assert "INTERNALERROR" not in output

    report = json.loads((coverage_project / "coverage.json").read_text())
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
    for measured_name in PUBLICATION_FILES:
        summary = report["files"][measured_name]["summary"]
        for measured_metric, covered, total in (
            ("line", "covered_lines", "num_statements"),
            ("branch", "covered_branches", "num_branches"),
        ):
            percent = 100 * summary[covered] / summary[total]
            if (measured_name, measured_metric) == (name, metric):
                assert percent < _load_baseline()["publication_scripts"][name][metric]
            else:
                assert percent == 100


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize("metric", ["line", "branch"])
def test_pytest_gate_uses_configured_publication_floor(
    coverage_project: Path, name: str, metric: str
) -> None:
    """Changing only a configured floor must change the Gate decision at that boundary."""
    script = coverage_project / name
    if metric == "line":
        script.write_text(script.read_text() + "\ndef untested():\n    return 0\n")
        measured = 100 * 5 / 6
    else:
        script.write_text(script.read_text().replace("    return 0\n", ""))
        exercise = coverage_project / "tests/test_exercise.py"
        exercise.write_text(
            exercise.read_text().replace(
                "        assert choose(False) == 0\n",
                f"        if path != {name!r}:\n            assert choose(False) == 0\n",
            )
        )
        measured = 50.0

    baseline_path = coverage_project / "config/coverage-baseline.json"
    baseline = _load_baseline()
    baseline["publication_scripts"][name][metric] = measured
    baseline_path.write_text(json.dumps(baseline))
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())

    # Leave code, tests and previous coverage artifacts intact; tighten only
    # this script's configured metric by less than the terminal display precision.
    baseline["publication_scripts"][name][metric] = measured + 0.0001
    baseline_path.write_text(json.dumps(baseline))
    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert errors == [
        f"PUBLICATION COVERAGE: {name}: {metric} coverage {measured:.6f}% "
        f"below floor {measured + 0.0001:.6f}%"
    ]
    current = json.loads(report_path.read_text())
    assert current["files"] == previous["files"]
    assert current["totals"]["percent_covered"] >= baseline["line"]


def test_pytest_gate_tracks_simultaneous_branch_losses_until_both_are_restored(
    coverage_project: Path,
) -> None:
    """Repairing one script must not hide the other script's remaining regression."""
    names = sorted(PUBLICATION_FILES)
    for name in names:
        script = coverage_project / name
        script.write_text(script.read_text().replace("    return 0\n", ""))
    (coverage_project / "src/my_project/unexecuted.py").write_text("ANSWER = 42\n")
    exercise = coverage_project / "tests/test_exercise.py"
    complete = exercise.read_text().replace(
        "        assert choose(False) == 0\n", "        choose(False)\n"
    )
    complete += "    assert runpy.run_path('src/my_project/unexecuted.py')['ANSWER'] == 42\n"

    for remaining in (names, names[1:], []):
        exercise.write_text(
            complete.replace(
                "        choose(False)\n",
                f"        if path not in {remaining!r}:\n            choose(False)\n",
            )
        )
        # Keep previous reports and databases to verify each run's current loss.
        result = _run_coverage_project(coverage_project)
        output = result.stdout + result.stderr
        assert result.returncode == int(bool(remaining)), output
        assert "1 passed" in output
        assert "INTERNALERROR" not in output
        assert "FAIL Required test coverage" not in output
        errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
        assert len(errors) == len(remaining), output
        for name, error in zip(remaining, errors, strict=True):
            assert error.startswith(f"PUBLICATION COVERAGE: {name}: branch coverage ")
            assert "below floor" in error

        report = json.loads((coverage_project / "coverage.json").read_text())
        assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
        for name in names:
            summary = report["files"][name]["summary"]
            assert summary["covered_lines"] == summary["num_statements"]
            assert summary["missing_branches"] == int(name in remaining)


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
def test_pytest_gate_rejects_unexecuted_script_despite_previous_passing_report(
    coverage_project: Path, name: str
) -> None:
    """Removing all execution of either script must invalidate its prior measurement."""
    previous = _run_coverage_project(coverage_project)
    assert previous.returncode == 0, previous.stdout + previous.stderr
    report_path = coverage_project / "coverage.json"
    assert set(json.loads(report_path.read_text())["files"]) == PUBLICATION_FILES | {
        "src/my_project/unexecuted.py"
    }

    remaining = next(path for path in PUBLICATION_FILES if path != name)
    (coverage_project / "tests/test_exercise.py").write_text(
        "import runpy\n\n"
        "def test_exercise():\n"
        f"    choose = runpy.run_path({remaining!r})['choose']\n"
        "    assert choose(True) == 1\n"
        "    assert choose(False) == 0\n"
    )

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: {name}: missing coverage measurement" in output
    assert "INTERNALERROR" not in output

    current = json.loads(report_path.read_text())
    assert set(current["files"]) == {remaining, "src/my_project/unexecuted.py"}
    assert current["totals"]["percent_covered"] >= _load_baseline()["line"]
    summary = current["files"][remaining]["summary"]
    assert summary["covered_lines"] == summary["num_statements"]
    assert summary["covered_branches"] == summary["num_branches"]


def test_pytest_gate_rejects_src_only_coverage_override(coverage_project: Path) -> None:
    """A CLI source override cannot silently restore the original src-only blind spot."""
    source = coverage_project / "src/my_project/unexecuted.py"
    source.write_text("ANSWER = 42\n")
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        exercise.read_text()
        + "    assert runpy.run_path('src/my_project/unexecuted.py')['ANSWER'] == 42\n"
    )

    result = _run_coverage_project(coverage_project, "--cov-reset", "--cov=src")
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output

    report = json.loads((coverage_project / "coverage.json").read_text())
    assert set(report["files"]) == {"src/my_project/unexecuted.py"}
    assert report["totals"]["percent_covered"] == 100
    for name in PUBLICATION_FILES:
        assert f"PUBLICATION COVERAGE: {name}: missing coverage measurement" in output


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
def test_pytest_gate_rejects_report_filter_hiding_publication_script(
    coverage_project: Path, name: str
) -> None:
    """Collected hits cannot replace a script's missing entry in the final report."""
    from coverage import CoverageData

    config = coverage_project / "pyproject.toml"
    original = config.read_bytes()
    # Retain collection of both scripts; omit one only when generating reports.
    config.write_text(
        config.read_text().replace(
            "[tool.coverage.report]\n", f'[tool.coverage.report]\nomit = ["{name}"]\n'
        )
    )

    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert errors == [f"PUBLICATION COVERAGE: {name}: missing coverage measurement"]

    data = CoverageData(basename=str(coverage_project / ".coverage"))
    data.read()
    assert data.lines(str(coverage_project / name))
    report_path = coverage_project / "coverage.json"
    report = json.loads(report_path.read_text())
    assert set(report["files"]) == (PUBLICATION_FILES - {name}) | {"src/my_project/unexecuted.py"}
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]

    config.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    assert set(json.loads(report_path.read_text())["files"]) == PUBLICATION_FILES | {
        "src/my_project/unexecuted.py"
    }


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


@pytest.mark.parametrize(
    "regression",
    [None]
    + [
        (name, metric, covered)
        for name in sorted(PUBLICATION_FILES)
        for metric, covered in (("line", "covered_lines"), ("branch", "covered_branches"))
    ],
)
def test_publication_gate_cli_enforces_each_floor(tmp_path: Path, regression) -> None:
    """The standalone gate must return failure even when aggregate coverage passes."""
    report = _measured_report()
    # The command must inspect each script rather than trust the aggregate summary.
    report["totals"] = {"percent_covered": 100.0}
    if regression is not None:
        name, metric, covered = regression
        report["files"][name]["summary"][covered] = 0

    report_path = tmp_path / "publication coverage.json"
    baseline_path = tmp_path / "publication baseline.json"
    report_path.write_text(json.dumps(report))
    baseline_path.write_text(json.dumps(_load_baseline()))

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts/publication_coverage_gate.py"),
            "--report",
            str(report_path),
            "--baseline",
            str(baseline_path),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == int(regression is not None), result.stdout + result.stderr
    assert result.stderr == ""
    if regression is None:
        assert result.stdout == "Ready publication coverage floors PASS\n"
    else:
        assert result.stdout == (
            f"{name}: {metric} coverage 0.000000% below floor "
            f"{_load_baseline()['publication_scripts'][name][metric]:.6f}%\n"
        )


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
def test_publication_gate_cli_defaults_use_current_pytest_report(
    coverage_project: Path, name: str
) -> None:
    """The documented standalone command must agree with pytest after a branch loss."""
    script = coverage_project / name
    script.write_text(script.read_text().replace("    return 0\n", ""))
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        exercise.read_text().replace(
            "        assert choose(False) == 0\n", "        choose(False)\n"
        )
    )
    for missing_branch in (False, True):
        if missing_branch:
            exercise.write_text(
                exercise.read_text().replace(
                    "        choose(False)\n",
                    f"        if path != {name!r}:\n            choose(False)\n",
                )
            )
        measured = _run_coverage_project(coverage_project)
        assert measured.returncode == int(missing_branch), measured.stdout + measured.stderr

        result = subprocess.run(
            [sys.executable, "scripts/publication_coverage_gate.py"],
            cwd=coverage_project,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == int(missing_branch), result.stdout + result.stderr
        assert result.stderr == ""
        if missing_branch:
            report = json.loads((coverage_project / "coverage.json").read_text())
            assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
            assert f"{name}: branch coverage" in result.stdout
            assert "below floor" in result.stdout
            assert "PASS" not in result.stdout
        else:
            assert result.stdout == "Ready publication coverage floors PASS\n"


@pytest.mark.parametrize("document", ["report", "baseline"])
@pytest.mark.parametrize("invalid", ["missing", "directory", "malformed-json", "invalid-utf8"])
def test_publication_gate_cli_rejects_unreadable_evidence(tmp_path: Path, document, invalid):
    """Unavailable evidence must fail with an actionable diagnostic, without a traceback."""
    paths = {name: tmp_path / f"{name}.json" for name in ("report", "baseline")}
    paths["report"].write_text(json.dumps(_measured_report()))
    paths["baseline"].write_text(json.dumps(_load_baseline()))
    path = paths[document]
    if invalid in ("missing", "directory"):
        path.unlink()
        if invalid == "directory":
            path.mkdir()
    elif invalid == "malformed-json":
        path.write_text('{"incomplete":')
    else:
        path.write_bytes(b"\xff")

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts/publication_coverage_gate.py"),
            "--report",
            str(paths["report"]),
            "--baseline",
            str(paths["baseline"]),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert result.stdout.startswith(f"Cannot load publication coverage {document} {path}:")
    assert result.stderr == ""
    assert "PASS" not in result.stdout


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize("regression", [None, "line", "branch"], ids=["complete", "line", "branch"])
@pytest.mark.parametrize("invocation", ["relative", "absolute"])
def test_publication_coverage_tracks_subprocess_regressions(
    coverage_project: Path, name: str, regression: str | None, invocation: str
) -> None:
    """Relative and absolute CLI paths must enforce either script's independent floors."""
    script = coverage_project / name
    if regression == "line":
        # Keep both branches exercised while adding one unexecuted line.
        script.write_text(script.read_text() + "\ndef untested():\n    return 0\n")
    else:
        # Both paths execute every line; omitting choose(False) loses only a branch.
        script.write_text(script.read_text().replace("    return 0\n", ""))
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        "import subprocess\nimport sys\nfrom pathlib import Path\n\n"
        "def test_exercise():\n"
        f"    for path in {sorted(PUBLICATION_FILES)!r}:\n"
        f"        script_path = str(Path(path).resolve()) if {invocation == 'absolute'!r} else path\n"
        "        code = f\"import runpy; choose = runpy.run_path({script_path!r})['choose']; "
        'assert choose(True) == 1"\n'
        f"        if not ({regression == 'branch'!r} and path == {name!r}):\n"
        "            code += '; choose(False)'\n"
        "        subprocess.run([sys.executable, '-c', code], check=True)\n"
    )

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == int(regression is not None), output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    report = json.loads((coverage_project / "coverage.json").read_text())
    assert set(report["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
    for path in PUBLICATION_FILES:
        summary = report["files"][path]["summary"]
        assert summary["covered_lines"] == summary["num_statements"] - int(
            regression == "line" and path == name
        )
        assert summary["covered_branches"] == summary["num_branches"] - int(
            regression == "branch" and path == name
        )
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    if regression is None:
        assert not errors
    else:
        assert len(errors) == 1
        assert f"{name}: {regression} coverage" in errors[0]
        assert "below floor" in errors[0]


def test_pytest_gate_rejects_disabled_subprocess_measurement_and_recovers(
    coverage_project: Path,
) -> None:
    """Parent coverage cannot stand in for missing CLI measurements or stale hits."""
    _exercise_in_subprocess(coverage_project)
    source = coverage_project / "src/my_project/unexecuted.py"
    source.unlink()
    source.with_name("exercised.py").write_text("value = 1\n")
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        exercise.read_text()
        + "    import runpy\n"
        + "    assert runpy.run_path('src/my_project/exercised.py')['value'] == 1\n"
    )

    complete = _run_coverage_project(coverage_project)
    assert complete.returncode == 0, complete.stdout + complete.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())
    assert set(before["files"]) == PUBLICATION_FILES | {"src/my_project/exercised.py"}

    config = coverage_project / "pyproject.toml"
    original_config = config.read_bytes()
    config.write_text(config.read_text().replace('patch = ["subprocess"]', "patch = []"))
    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output
    current = json.loads(report_path.read_text())
    assert set(current["files"]) == {"src/my_project/exercised.py"}
    assert current["totals"]["percent_covered"] == 100
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert errors == [
        f"PUBLICATION COVERAGE: {name}: missing coverage measurement"
        for name in sorted(PUBLICATION_FILES)
    ]

    config.write_bytes(original_config)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "PUBLICATION COVERAGE:" not in output
    assert json.loads(report_path.read_text())["files"] == before["files"]


@pytest.mark.parametrize("missing_branch", [None, *sorted(PUBLICATION_FILES)])
def test_publication_coverage_merges_parallel_cli_measurements(
    coverage_project: Path, missing_branch: str | None
) -> None:
    """Concurrent CLI hits must reflect branch removal and restoration on each run."""
    for name in PUBLICATION_FILES:
        (coverage_project / name).write_text(
            "import sys\n\n"
            "def choose(flag):\n"
            "    if flag:\n"
            "        return 1\n\n"
            "choose(sys.argv[1] == 'true')\n"
        )
    exercise = coverage_project / "tests/test_exercise.py"
    complete_test = (
        "import subprocess\nimport sys\n\n"
        "OMIT_BRANCH = None\n\n"
        "def test_exercise():\n"
        "    children = []\n"
        f"    for path in {sorted(PUBLICATION_FILES)!r}:\n"
        "        for flag in ('true', 'false'):\n"
        "            if path == OMIT_BRANCH and flag == 'false':\n"
        "                continue\n"
        "            children.append(subprocess.Popen([sys.executable, path, flag]))\n"
        "    results = [child.wait(timeout=30) for child in children]\n"
        "    assert all(code == 0 for code in results)\n"
    )
    exercise.write_text(complete_test)
    complete = _run_coverage_project(coverage_project)
    assert complete.returncode == 0, complete.stdout + complete.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())
    if missing_branch is not None:
        exercise.write_text(
            complete_test.replace("OMIT_BRANCH = None", f"OMIT_BRANCH = {missing_branch!r}")
        )

    result = _run_coverage_project(coverage_project) if missing_branch is not None else complete
    output = result.stdout + result.stderr
    assert result.returncode == int(missing_branch is not None), output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    report = json.loads(report_path.read_text())
    assert set(report["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    assert set(report["files"]) == set(before["files"])
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
    for name in PUBLICATION_FILES:
        summary = report["files"][name]["summary"]
        original = before["files"][name]["summary"]
        assert original["covered_branches"] == original["num_branches"]
        assert summary["num_branches"] == original["num_branches"]
        assert summary["covered_lines"] == summary["num_statements"]
        assert summary["missing_branches"] == int(name == missing_branch)
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    if missing_branch is None:
        assert not errors
    else:
        assert len(errors) == 1
        assert f"{missing_branch}: branch coverage" in errors[0]
        assert "below floor" in errors[0]

        # Leave the failed database and report intact so recovery proves that
        # each concurrent run replaces, rather than accumulates, prior hits.
        exercise.write_text(complete_test)
        restored = _run_coverage_project(coverage_project)
        output = restored.stdout + restored.stderr
        assert restored.returncode == 0, output
        assert "PUBLICATION COVERAGE:" not in output
        assert json.loads(report_path.read_text())["files"] == before["files"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
def test_pytest_gate_rejects_missing_publication_measurement(
    coverage_project: Path, name: str
) -> None:
    """An unexecuted publication script must fail even when aggregate coverage passes."""
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        exercise.read_text().replace(
            "        choose = runpy.run_path(path)['choose']\n",
            f"        if path == {name!r}:\n            continue\n"
            "        choose = runpy.run_path(path)['choose']\n",
        )
    )

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: {name}: missing coverage measurement" in output
    assert "INTERNALERROR" not in output
    report = json.loads((coverage_project / "coverage.json").read_text())
    assert name not in report["files"]
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]


def test_pytest_gate_rejects_disabled_branch_collection(coverage_project: Path) -> None:
    """Missing branch evidence must fail cleanly even when every line is covered."""
    config = coverage_project / "pyproject.toml"
    config.write_text(config.read_text().replace("branch = true", "branch = false"))

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    assert "Traceback" not in output
    for name in PUBLICATION_FILES:
        assert f"PUBLICATION COVERAGE: {name}: invalid branch measurement or floor" in output

    report = json.loads((coverage_project / "coverage.json").read_text())
    assert set(report["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    assert report["meta"]["branch_coverage"] is False
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
    for name in PUBLICATION_FILES:
        summary = report["files"][name]["summary"]
        assert summary["covered_lines"] == summary["num_statements"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize(
    "aggregate_floor", [80, 0], ids=["aggregate-enforced", "aggregate-disabled"]
)
def test_previous_passing_run_cannot_mask_removed_branch_test(
    coverage_project: Path, name: str, aggregate_floor: int
) -> None:
    """Fresh branch evidence controls the gate independently of the aggregate threshold."""
    script = coverage_project / name
    script.write_text(script.read_text().replace("    return 0\n", ""))
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        exercise.read_text().replace(
            "        assert choose(False) == 0\n", "        choose(False)\n"
        )
    )
    complete_exercise = exercise.read_bytes()
    coverage_args = (f"--cov-fail-under={aggregate_floor}",)
    result = _run_coverage_project(coverage_project, *coverage_args)
    assert result.returncode == 0, result.stdout + result.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    assert (coverage_project / ".coverage").is_file()

    # Remove one branch exercise without changing production code or deleting
    # the passing report and coverage database left by the previous invocation.
    exercise.write_text(
        exercise.read_text().replace(
            "        choose(False)\n",
            f"        if path != {name!r}:\n            choose(False)\n",
        )
    )

    result = _run_coverage_project(coverage_project, *coverage_args)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: {name}: branch coverage" in output
    assert "below floor" in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output

    current = json.loads(report_path.read_text())
    assert set(current["files"]) == set(previous["files"])
    assert current["totals"]["percent_covered"] >= _load_baseline()["line"]
    for path in PUBLICATION_FILES:
        before = previous["files"][path]["summary"]
        after = current["files"][path]["summary"]
        assert after["covered_lines"] == before["covered_lines"]
        assert after["num_branches"] == before["num_branches"]
        assert after["covered_branches"] == before["covered_branches"] - int(path == name)

    # Restoring the branch exercise must replace the failing evidence and pass
    # without deleting the report or coverage database in between runs.
    exercise.write_bytes(complete_exercise)
    restored = _run_coverage_project(coverage_project, *coverage_args)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    assert "PUBLICATION COVERAGE:" not in restored.stdout + restored.stderr
    restored_report = json.loads(report_path.read_text())
    assert set(restored_report["files"]) == set(previous["files"])
    for path in PUBLICATION_FILES:
        assert restored_report["files"][path]["summary"] == previous["files"][path]["summary"]


@pytest.mark.parametrize("stale_report", [False, True], ids=["absent", "stale"])
def test_pytest_gate_requires_current_json_report(
    coverage_project: Path, stale_report: bool
) -> None:
    """A passing terminal report cannot substitute for fresh per-file evidence."""
    config = coverage_project / "pyproject.toml"
    config.write_text(config.read_text().replace(" --cov-report=json", ""))
    report_path = coverage_project / "coverage.json"
    if stale_report:
        report_path.write_text(json.dumps(_measured_report()))

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE: Current publication coverage evidence unavailable:" in output
    assert "INTERNALERROR" not in output
    assert not report_path.exists()


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
def test_pytest_gate_rejects_appended_coverage_that_masks_removed_branch_test(
    coverage_project: Path, name: str
) -> None:
    """A newly written report can still contain branch hits from a previous run."""
    previous = _run_coverage_project(coverage_project)
    assert previous.returncode == 0, previous.stdout + previous.stderr

    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        exercise.read_text().replace(
            "        assert choose(False) == 0\n",
            f"        if path != {name!r}:\n            assert choose(False) == 0\n",
        )
    )

    result = _run_coverage_project(coverage_project, "--cov-append")
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert (
        "PUBLICATION COVERAGE: --cov-append cannot establish current publication coverage" in output
    )
    assert "INTERNALERROR" not in output

    # Accumulated hits conceal the removed assertion, even in the fresh JSON.
    report = json.loads((coverage_project / "coverage.json").read_text())
    for path in PUBLICATION_FILES:
        summary = report["files"][path]["summary"]
        assert summary["covered_lines"] == summary["num_statements"]
        assert summary["covered_branches"] == summary["num_branches"]

    current = _run_coverage_project(coverage_project)
    output = current.stdout + current.stderr
    assert current.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: {name}: branch coverage" in output
    assert "below floor" in output
    assert "--cov-append cannot" not in output
    report = json.loads((coverage_project / "coverage.json").read_text())
    for path in PUBLICATION_FILES:
        summary = report["files"][path]["summary"]
        assert summary["covered_branches"] == summary["num_branches"] - int(path == name)


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


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize(
    "metric,covered,total",
    [
        ("line", "covered_lines", "num_statements"),
        ("branch", "covered_branches", "num_branches"),
    ],
)
def test_recorded_publication_baseline_rejects_one_lost_hit(name, metric, covered, total):
    """Recorded floors must accept the evidence and detect the smallest coverage loss."""
    from scripts.publication_coverage_gate import check_report

    evidence = json.loads(
        (REPO_ROOT / "docs/evidence/issue-623-publication-coverage.json").read_text()
    )
    report = {"files": {path: {"summary": evidence["files"][path]} for path in PUBLICATION_FILES}}
    baseline = _load_baseline()
    assert check_report(report, baseline) == []

    summary = report["files"][name]["summary"]
    measured = 100 * summary[covered] / summary[total]
    floor = baseline["publication_scripts"][name][metric]
    assert 0 <= measured - floor < 0.0001, "Floor must round down the recorded measurement"

    baseline["publication_scripts"][name][metric] = measured
    assert check_report(report, baseline) == [], "An exact floor match must pass"
    baseline["publication_scripts"][name][metric] = floor
    summary[covered] -= 1
    errors = check_report(report, baseline)
    assert len(errors) == 1
    assert errors[0].startswith(f"{name}: {metric} coverage ")
    assert "below floor" in errors[0]


def test_recorded_branch_removal_breaches_guard_floors_above_aggregate_floor():
    """Keep the deliberate-break evidence tied to the gate's actual decisions."""
    from scripts.publication_coverage_gate import check_report

    evidence = json.loads(
        (REPO_ROOT / "docs/evidence/issue-623-publication-coverage.json").read_text()
    )
    control = evidence["branch_removal_control"]
    name = "scripts/check_publication_safety.py"
    report = {"files": {path: {"summary": summary} for path, summary in evidence["files"].items()}}
    baseline = _load_baseline()
    assert control["before"] == report["files"][name]["summary"]
    assert check_report(report, baseline) == []

    before, after = control["before"], control["after"]
    for covered, total in (
        ("covered_lines", "num_statements"),
        ("covered_branches", "num_branches"),
    ):
        assert after[total] == before[total]
        assert after[covered] == before[covered] - 1
    assert control["branch_decreased"] is True
    assert control["exit"] == 1

    report["files"][name]["summary"] = after
    summaries = [file["summary"] for file in report["files"].values()]
    hits = sum(summary["covered_lines"] + summary["covered_branches"] for summary in summaries)
    total = sum(summary["num_statements"] + summary["num_branches"] for summary in summaries)
    assert 100 * hits / total >= baseline["line"]
    errors = check_report(report, baseline)
    assert len(errors) == 2
    for metric, error in zip(("line", "branch"), errors, strict=True):
        assert error.startswith(f"{name}: {metric} coverage ")
        assert "below floor" in error


@pytest.mark.parametrize(
    "name,removed_test",
    [
        (
            "scripts/check_publication_safety.py",
            "tests/test_publication_safety.py::test_empty_or_missing_tree_fails",
        ),
        (
            "scripts/prepare_publication.py",
            "tests/test_prepare_publication.py::"
            "test_named_legacy_process_capture_is_wrapped_without_losing_output",
        ),
    ],
    ids=["guard", "preparer"],
)
def test_real_branch_test_removal_fails_publication_gate(
    coverage_project: Path, name: str, removed_test: str
) -> None:
    """Either real script's lost branch must fail until its test is restored."""
    (coverage_project / "tests/test_exercise.py").unlink()
    for relative in (
        "scripts/check_publication_safety.py",
        "scripts/prepare_publication.py",
        "scripts/publication_patterns.py",
        "tests/test_publication_safety.py",
        "tests/test_prepare_publication.py",
    ):
        shutil.copyfile(REPO_ROOT / relative, coverage_project / relative)

    # Workflow-shell tests need the full repository; this isolated reproduction
    # exercises the real publication scripts without copying workflow files.
    args = ("-k", "not workflow and not gate_summary")
    complete = _run_coverage_project(coverage_project, *args)
    assert complete.returncode == 0, complete.stdout + complete.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())

    removed = _run_coverage_project(
        coverage_project,
        *args,
        "--deselect",
        removed_test,
    )
    output = removed.stdout + removed.stderr
    assert removed.returncode == 1, output
    assert re.search(r"\d+ passed, \d+ deselected", output), output
    assert "FAILED " not in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output

    after = json.loads(report_path.read_text())
    assert (
        set(before["files"])
        == set(after["files"])
        == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    )
    assert after["totals"]["percent_covered"] >= _load_baseline()["line"]
    original, reduced = (report["files"][name]["summary"] for report in (before, after))
    for covered, total in (
        ("covered_lines", "num_statements"),
        ("covered_branches", "num_branches"),
    ):
        assert reduced[total] == original[total]
        assert reduced[covered] < original[covered]
        if name == "scripts/check_publication_safety.py":
            assert reduced[covered] == original[covered] - 1
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert len(errors) == 2, output
    for metric, error in zip(("line", "branch"), errors, strict=True):
        assert error.startswith(f"PUBLICATION COVERAGE: {name}: {metric} coverage ")
        assert "below floor" in error

    # Keep the failed report and coverage database in place: restoring test
    # collection must replace that evidence with the original measurements.
    restored = _run_coverage_project(coverage_project, *args)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "PUBLICATION COVERAGE:" not in output
    restored_report = json.loads(report_path.read_text())
    assert set(restored_report["files"]) == set(before["files"])
    for path in before["files"]:
        assert restored_report["files"][path]["summary"] == before["files"][path]["summary"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize(
    "metric,covered,total",
    [
        ("line", "covered_lines", "num_statements"),
        ("branch", "covered_branches", "num_branches"),
    ],
)
@pytest.mark.parametrize("field", ["floor", "covered", "total"])
@pytest.mark.parametrize(
    "invalid",
    [None, True, False, "100", float("nan"), float("inf"), float("-inf"), -1],
    ids=["null", "true", "false", "string", "nan", "inf", "negative-inf", "negative"],
)
def test_publication_measurements_fail_closed(name, metric, covered, total, field, invalid):
    """Neither Python's numeric booleans nor JSON decoder extensions are valid evidence."""
    from scripts.publication_coverage_gate import check_report

    baseline = _load_baseline()
    report = _measured_report()
    if field == "floor":
        baseline["publication_scripts"][name][metric] = invalid
    else:
        report["files"][name]["summary"][covered if field == "covered" else total] = invalid

    errors = check_report(json.loads(json.dumps(report)), json.loads(json.dumps(baseline)))
    assert errors == [f"{name}: invalid {metric} measurement or floor"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize(
    "metric,covered,total",
    [
        ("line", "covered_lines", "num_statements"),
        ("branch", "covered_branches", "num_branches"),
    ],
)
@pytest.mark.parametrize("field,invalid", [("floor", 101), ("covered", 101), ("total", 0)])
def test_publication_gate_rejects_impossible_measurements(
    name, metric, covered, total, field, invalid
):
    """Invalid bounds must not appear as above-floor or empty passing measurements."""
    from scripts.publication_coverage_gate import check_report

    baseline = _load_baseline()
    report = _measured_report()
    if field == "floor":
        baseline["publication_scripts"][name][metric] = invalid
    else:
        report["files"][name]["summary"][covered if field == "covered" else total] = invalid

    errors = check_report(report, baseline)
    assert errors == [f"{name}: invalid {metric} measurement or floor"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize(
    "metric,covered,total",
    [
        ("line", "covered_lines", "num_statements"),
        ("branch", "covered_branches", "num_branches"),
    ],
)
@pytest.mark.parametrize("field", ["covered", "total"])
def test_publication_gate_rejects_fractional_counts(name, field, metric, covered, total):
    """Above-floor percentages cannot make fractional line or branch counts valid."""
    from scripts.publication_coverage_gate import check_report

    report = _measured_report()
    summary = report["files"][name]["summary"]
    summary[covered if field == "covered" else total] = 99.5 if field == "covered" else 100.5

    errors = check_report(json.loads(json.dumps(report)), _load_baseline())
    assert errors == [f"{name}: invalid {metric} measurement or floor"]


@pytest.mark.parametrize("field", ["floor", "covered", "total"])
@pytest.mark.parametrize(
    "metric,covered,total",
    [
        ("line", "covered_lines", "num_statements"),
        ("branch", "covered_branches", "num_branches"),
    ],
)
def test_publication_gate_rejects_oversized_json_integers(field, metric, covered, total):
    """Unbounded JSON numbers must produce a diagnostic instead of overflowing."""
    from scripts.publication_coverage_gate import check_report

    baseline = _load_baseline()
    report = _measured_report()
    name = "scripts/check_publication_safety.py"
    if field == "floor":
        baseline["publication_scripts"][name][metric] = 10**400
    else:
        report["files"][name]["summary"][covered if field == "covered" else total] = 10**400

    # Exercise the same JSON decoding boundary as the command-line gate.
    errors = check_report(json.loads(json.dumps(report)), json.loads(json.dumps(baseline)))
    assert errors == [f"{name}: invalid {metric} measurement or floor"]


@pytest.mark.parametrize("invalid", [None, [], "invalid"])
@pytest.mark.parametrize(
    "document,path",
    [
        ("report", ()),
        ("report", ("files",)),
        ("report", ("files", "scripts/check_publication_safety.py")),
        ("report", ("files", "scripts/check_publication_safety.py", "summary")),
        ("baseline", ()),
        ("baseline", ("publication_scripts",)),
        ("baseline", ("publication_scripts", "scripts/check_publication_safety.py")),
    ],
)
def test_publication_gate_rejects_malformed_json_objects(document, path, invalid):
    """Valid JSON with the wrong structure must yield diagnostics, not exceptions."""
    from scripts.publication_coverage_gate import check_report

    documents = {"report": _measured_report(), "baseline": _load_baseline()}
    parent = documents
    for key in (document, *path)[:-1]:
        parent = parent[key]
    parent[(document, *path)[-1]] = invalid

    errors = check_report(documents["report"], documents["baseline"])
    assert errors
    assert all(isinstance(error, str) and error for error in errors)


@pytest.mark.parametrize(
    "invalid,diagnostic",
    [
        (None, "coverage summary and floors"),
        ({"line": 10**400, "branch": 90}, "invalid line measurement or floor"),
    ],
    ids=["wrong-type", "oversized-integer"],
)
def test_pytest_gate_rejects_malformed_baseline_without_internal_error(
    coverage_project: Path, invalid, diagnostic: str
) -> None:
    """Malformed per-script floors must fail the Gate cleanly after passing tests."""
    baseline = _load_baseline()
    name = "scripts/check_publication_safety.py"
    baseline["publication_scripts"][name] = invalid
    (coverage_project / "config/coverage-baseline.json").write_text(json.dumps(baseline))

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: {name}: {diagnostic}" in output
    assert "INTERNALERROR" not in output
    assert "Traceback" not in output


@pytest.mark.parametrize(
    "path",
    [("publication_scripts",)]
    + [("publication_scripts", name) for name in sorted(PUBLICATION_FILES)]
    + [
        ("publication_scripts", name, metric)
        for name in sorted(PUBLICATION_FILES)
        for metric in ("line", "branch")
    ],
)
def test_pytest_gate_rejects_missing_publication_floors_and_recovers(
    coverage_project: Path, path: tuple[str, ...]
) -> None:
    """Deleting any required floor must fail despite a previous passing report."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    baseline_path = coverage_project / "config/coverage-baseline.json"
    original = baseline_path.read_bytes()
    baseline = json.loads(original)
    parent = baseline
    for key in path[:-1]:
        parent = parent[key]
    del parent[path[-1]]
    baseline_path.write_text(json.dumps(baseline))

    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    diagnostic = (
        f"{path[1]}: invalid {path[2]} measurement or floor"
        if len(path) == 3
        else "publication_scripts must name exactly the two Ready-owned scripts"
    )
    assert f"PUBLICATION COVERAGE: {diagnostic}" in output
    assert "INTERNALERROR" not in output
    assert "Traceback" not in output
    current = json.loads(report_path.read_text())
    assert current["files"] == previous["files"]
    assert current["totals"]["percent_covered"] >= _load_baseline()["line"]

    baseline_path.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "PUBLICATION COVERAGE:" not in output
    assert json.loads(report_path.read_text())["files"] == previous["files"]


@pytest.mark.parametrize("invalid", ["missing", "directory", "malformed-json", "invalid-utf8"])
def test_pytest_gate_rejects_unreadable_baseline_and_recovers(
    coverage_project: Path, invalid: str
) -> None:
    """Passing coverage cannot replace unreadable floors, even after a successful run."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    baseline_path = coverage_project / "config/coverage-baseline.json"
    original = baseline_path.read_bytes()
    if invalid in ("missing", "directory"):
        baseline_path.unlink()
        if invalid == "directory":
            baseline_path.mkdir()
    elif invalid == "malformed-json":
        baseline_path.write_text('{"publication_scripts":')
    else:
        baseline_path.write_bytes(b"\xff")

    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE: Current publication coverage evidence unavailable:" in output
    assert "INTERNALERROR" not in output
    assert "Traceback" not in output
    current = json.loads(report_path.read_text())
    assert current["files"] == previous["files"]
    assert current["totals"]["percent_covered"] >= _load_baseline()["line"]

    if baseline_path.is_dir():
        baseline_path.rmdir()
    baseline_path.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "PUBLICATION COVERAGE:" not in output
    assert json.loads(report_path.read_text())["files"] == previous["files"]


def test_pytest_gate_rejects_empty_selection_despite_previous_passing_report(
    coverage_project: Path,
) -> None:
    """An active run that executes no tests cannot reuse earlier publication hits."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())

    failing = _run_coverage_project(coverage_project, "-k", "not test_exercise")
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 deselected" in output
    assert "INTERNALERROR" not in output
    assert "Traceback" not in output
    for name in PUBLICATION_FILES:
        assert f"PUBLICATION COVERAGE: {name}: missing coverage measurement" in output
    current = json.loads(report_path.read_text())
    assert set(current["files"]) == {"src/my_project/unexecuted.py"}
    assert current["totals"]["covered_lines"] == 0
    assert current["totals"]["percent_covered"] == 0

    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    assert json.loads(report_path.read_text())["files"] == previous["files"]


def test_pytest_gate_rejects_collection_error_despite_previous_passing_report(
    coverage_project: Path,
) -> None:
    """Aborted collection must not reuse earlier hits, and repairing it must recover."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())

    broken = coverage_project / "tests/test_broken_collection.py"
    broken.write_text('raise RuntimeError("collection regression control")\n')
    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode != 0, output
    assert "ERROR collecting tests/test_broken_collection.py" in output
    assert "collection regression control" in output
    assert "PUBLICATION COVERAGE:" in output
    assert "INTERNALERROR" not in output
    assert "1 passed" not in output
    if report_path.exists():
        current = json.loads(report_path.read_text())
        assert current["totals"]["covered_lines"] == 0
        assert current["totals"]["covered_branches"] == 0

    broken.unlink()
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    assert json.loads(report_path.read_text())["files"] == previous["files"]


@pytest.mark.parametrize("mode", ["--cov-reset", "--no-cov", "--collect-only"])
def test_inactive_coverage_skips_publication_hooks_without_changing_evidence(
    coverage_project: Path, mode: str
) -> None:
    """Focused and collection-only runs must neither gate nor replace prior evidence."""
    # An invalid baseline would fail an active gate, so a successful run also
    # demonstrates that the per-script gate was skipped, not merely satisfied.
    (coverage_project / "config/coverage-baseline.json").write_text("{}\n")
    report_path = coverage_project / "coverage.json"
    previous_report = json.dumps(_measured_report(), indent=2).encode() + b"\n"
    report_path.write_bytes(previous_report)

    result = _run_coverage_project(coverage_project, mode)
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    expected = "1 test collected" if mode == "--collect-only" else "1 passed"
    assert expected in combined
    assert "INTERNALERROR" not in combined
    assert "AttributeError" not in combined
    assert "PUBLICATION COVERAGE:" not in combined
    assert report_path.read_bytes() == previous_report
