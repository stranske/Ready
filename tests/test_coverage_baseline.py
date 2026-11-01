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
from xml.etree import ElementTree

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
    assert "--cov-report=xml" in args
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
        "scripts/check_publication_safety_copy.py",
        "scripts/prepare_publication_copy.py",
        "src_backup/my_project/unrelated.py",
        "tests/fixtures/src/my_project/unrelated.py",
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
    # These probes rewrite same-size tests within one filesystem timestamp tick.
    # Execute their current source bytes while retaining coverage and --lf data.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Exercise only pytest-cov and the copied repository hooks. Unrelated
    # runner plugins can add hooks or startup costs to every isolated probe.
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    env.pop("PYTEST_PLUGINS", None)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-p",
            "pytest_cov.plugin",
            "-q",
            "-m",
            "not slow",
            *pytest_args,
        ],
        cwd=project,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def _exercise_in_subprocess(project: Path, depth: int = 1) -> None:
    """Run the fixture's assertions through one or more real Python descendants."""
    exercise = project / "tests/test_exercise.py"
    for level in range(depth):
        runner = f"exercise_cli_{level}.py"
        (project / runner).write_text(exercise.read_text() + "\ntest_exercise()\n")
        exercise.write_text(
            "import subprocess\nimport sys\n\n"
            "def test_exercise():\n"
            f"    subprocess.run([sys.executable, {runner!r}], check=True)\n"
        )


def _assert_xml_matches_json(project: Path, report: dict) -> None:
    """The CI XML artifact must retain the JSON gate's exact files and hit counts."""
    root = ElementTree.parse(project / "coverage.xml").getroot()
    # Aggregate consumers read the XML root rather than its individual classes.
    # Keep both artifacts tied to the same denominator, including missed src
    # lines and publication branches, instead of accepting matching classes alone.
    for metric, covered, total in (
        ("lines", "covered_lines", "num_statements"),
        ("branches", "covered_branches", "num_branches"),
    ):
        hits = sum(file["summary"][covered] for file in report["files"].values())
        count = sum(file["summary"][total] for file in report["files"].values())
        assert report["totals"][covered] == int(root.attrib[f"{metric}-covered"]) == hits
        assert report["totals"][total] == int(root.attrib[f"{metric}-valid"]) == count
        rate = hits / count if count else 1.0
        # Cobertura rates have four significant digits; hit counts remain exact.
        rate_key = "line-rate" if metric == "lines" else "branch-rate"
        assert float(root.attrib[rate_key]) == pytest.approx(rate, abs=0.0001)
    classes = root.findall(".//class")
    assert len(classes) == len(report["files"])
    assert {entry.attrib["filename"] for entry in classes} == set(report["files"])
    for entry in classes:
        summary = report["files"][entry.attrib["filename"]]["summary"]
        lines = entry.findall("./lines/line")
        assert len(lines) == summary["num_statements"]
        assert sum(int(line.attrib["hits"]) > 0 for line in lines) == summary["covered_lines"]
        covered_branches = total_branches = 0
        for line in lines:
            if line.get("branch") == "true":
                counts = re.fullmatch(r"\d+% \((\d+)/(\d+)\)", line.attrib["condition-coverage"])
                assert counts is not None
                covered_branches += int(counts[1])
                total_branches += int(counts[2])
        assert covered_branches == summary["covered_branches"]
        assert total_branches == summary["num_branches"]


def test_coverage_probe_ignores_unrelated_runner_plugins(
    coverage_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Runner plugin requests must not change the isolated coverage experiment."""
    monkeypatch.setenv("PYTEST_PLUGINS", "runner_plugin_that_is_not_installed")
    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "0")

    result = _run_coverage_project(coverage_project)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout
    report = json.loads((coverage_project / "coverage.json").read_text())
    assert set(report["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    _assert_xml_matches_json(coverage_project, report)


@pytest.mark.parametrize("execution", ["in-process", "subprocess"])
@pytest.mark.parametrize("extension", [".py", ".pyw"])
@pytest.mark.parametrize(
    "source_directory",
    ["src", "src/another_product", "src/my_project", "src/my_project/nested/package"],
)
def test_measured_file_set_includes_unexecuted_source_and_excludes_tooling(
    coverage_project: Path, execution: str, extension: str, source_directory: str
) -> None:
    """Preserve product hits and misses while excluding tooling in parent and child runs."""
    original = coverage_project / "src/my_project/unexecuted.py"
    source = coverage_project / source_directory / f"unexecuted{extension}"
    source.parent.mkdir(parents=True, exist_ok=True)
    original.rename(source)
    partial = source.with_name(f"partially_exercised{extension}")
    partial.write_text("def choose(flag):\n    if flag:\n        return 1\n    return 0\n")
    partial_name = partial.relative_to(coverage_project).as_posix()
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        exercise.read_text() + f"    assert runpy.run_path({partial_name!r})['choose'](True) == 1\n"
    )
    if execution == "subprocess":
        _exercise_in_subprocess(coverage_project)

    result = _run_coverage_project(coverage_project)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((coverage_project / "coverage.json").read_text())
    _assert_xml_matches_json(coverage_project, report)
    source_name = source.relative_to(coverage_project).as_posix()
    assert set(report["files"]) == PUBLICATION_FILES | {source_name, partial_name}
    summary = report["files"][source_name]["summary"]
    assert summary["num_statements"] == 1
    assert summary["covered_lines"] == 0
    # Touching source files must preserve collected hits without inventing hits
    # for the unexecuted line or branch in that same product module.
    summary = report["files"][partial_name]["summary"]
    assert summary["num_statements"] == 4
    assert summary["covered_lines"] == 3
    assert summary["num_branches"] == 2
    assert summary["covered_branches"] == 1


@pytest.mark.parametrize("filename", [".editor.py", "module~.py"])
def test_source_discovery_ignores_unexecuted_editor_files(
    coverage_project: Path, filename: str
) -> None:
    """Editor side files must not enter the denominator or break coverage parsing."""
    (coverage_project / "src/my_project" / filename).write_text("unfinished editor buffer (\n")

    result = _run_coverage_project(coverage_project)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((coverage_project / "coverage.json").read_text())
    assert set(report["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    assert report["files"]["src/my_project/unexecuted.py"]["summary"]["covered_lines"] == 0
    _assert_xml_matches_json(coverage_project, report)


def test_measured_file_set_tracks_renamed_and_deleted_product_source(
    coverage_project: Path,
) -> None:
    """Current source discovery must replace stale product paths in both CI artifacts."""
    source = coverage_project / "src/my_project/unexecuted.py"
    renamed = source.with_name("renamed.py")
    original = source.read_bytes()
    report_path = coverage_project / "coverage.json"
    before = None

    for current in (source, renamed, None, source):
        if current == renamed:
            source.rename(renamed)
        elif current is None:
            renamed.unlink()
        elif not source.exists():
            source.write_bytes(original)

        # Retain the previous database and artifacts so stale paths cannot
        # silently change the next run's denominator or measured file set.
        result = _run_coverage_project(coverage_project)
        output = result.stdout + result.stderr
        assert result.returncode == 0, output
        assert "1 passed" in output
        assert "PUBLICATION COVERAGE:" not in output
        report = json.loads(report_path.read_text())
        _assert_xml_matches_json(coverage_project, report)
        expected = set() if current is None else {current.relative_to(coverage_project).as_posix()}
        assert set(report["files"]) == PUBLICATION_FILES | expected
        if current is not None:
            summary = report["files"][next(iter(expected))]["summary"]
            assert summary["covered_lines"] == 0
            assert summary["num_statements"] == 1
        if before is None:
            before = report
        else:
            for name in PUBLICATION_FILES:
                assert report["files"][name] == before["files"][name]
    assert report["files"] == before["files"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
def test_unparseable_publication_source_cannot_reuse_previous_coverage_report(
    coverage_project: Path, name: str
) -> None:
    """Omitting an unparseable publication script must fail despite prior passing hits."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    source = coverage_project / name
    original = source.read_bytes()
    exercise = coverage_project / "tests/test_exercise.py"
    original_test = exercise.read_bytes()
    # All assertions pass before the on-disk source becomes unreportable.
    exercise.write_text(
        exercise.read_text()
        + "    from pathlib import Path\n"
        + f"    Path({name!r}).write_text('def unfinished(\\n')\n"
    )

    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    assert "Couldn't parse" in output
    assert f"PUBLICATION COVERAGE: {name}: missing coverage measurement" in output
    assert "INTERNALERROR" not in output
    assert "Ready publication coverage floors PASS" not in output
    current = json.loads(report_path.read_text())
    assert name not in current["files"]
    assert set(current["files"]) == set(previous["files"]) - {name}
    _assert_xml_matches_json(coverage_project, current)

    source.write_bytes(original)
    exercise.write_bytes(original_test)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    report = json.loads(report_path.read_text())
    assert report["files"] == previous["files"]
    _assert_xml_matches_json(coverage_project, report)


@pytest.mark.parametrize("execution", ["in-process", "subprocess"])
@pytest.mark.parametrize(
    "source_directory",
    ["src", "src/another_product", "src/my_project", "src/my_project/nested/package"],
)
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


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
def test_aggregate_failure_survives_publication_regression_and_repair(
    coverage_project: Path, name: str
) -> None:
    """Repairing a publication floor must not clear an independent aggregate failure."""
    source = coverage_project / "src/my_project/unexecuted.py"
    original_source = source.read_bytes()
    source.write_text("def choose(flag):\n    if flag:\n        return 1\n    return 0\n")
    exercise = coverage_project / "tests/test_exercise.py"
    original_exercise = exercise.read_bytes()
    report_path = coverage_project / "coverage.json"
    before = None

    for phase in ("aggregate", "both", "publication-repaired", "all-repaired"):
        if phase == "both":
            exercise.write_text(
                exercise.read_text().replace(
                    "        assert choose(False) == 0",
                    f"        if path != {name!r}:\n            assert choose(False) == 0",
                )
            )
        elif phase == "publication-repaired":
            exercise.write_bytes(original_exercise)
        elif phase == "all-repaired":
            source.write_bytes(original_source)

        result = _run_coverage_project(coverage_project)
        output = result.stdout + result.stderr
        assert result.returncode == int(phase != "all-repaired"), output
        assert "1 passed" in output
        assert "INTERNALERROR" not in output
        assert ("FAIL Required test coverage of 80" in output) == (phase != "all-repaired")

        report = json.loads(report_path.read_text())
        _assert_xml_matches_json(coverage_project, report)
        assert set(report["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
        assert (report["totals"]["percent_covered"] >= _load_baseline()["line"]) == (
            phase == "all-repaired"
        )
        errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
        if phase == "both":
            assert len(errors) == 2, output
            for metric, error in zip(("line", "branch"), errors, strict=True):
                assert error.startswith(f"PUBLICATION COVERAGE: {name}: {metric} coverage ")
                assert "below floor" in error
            summary = report["files"][name]["summary"]
            for metric in ("covered_lines", "covered_branches"):
                assert summary[metric] == before["files"][name]["summary"][metric] - 1
        else:
            assert not errors, output
            if before is None:
                before = report
            else:
                for path in PUBLICATION_FILES:
                    assert report["files"][path] == before["files"][path]
        assert report["files"]["src/my_project/unexecuted.py"]["summary"]["covered_lines"] == 0


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
    """Both gate entry points must reject scope drift and recover from current reports."""
    config = coverage_project / "pyproject.toml"
    original = config.read_bytes()
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

    standalone = subprocess.run(
        [sys.executable, "scripts/publication_coverage_gate.py"],
        cwd=coverage_project,
        capture_output=True,
        text=True,
        check=False,
    )
    assert standalone.returncode == 1, standalone.stdout + standalone.stderr
    assert standalone.stderr == ""
    assert standalone.stdout == f"Synced or unrelated files measured: {[unrelated]!r}\n"

    # Repair only the selection, retaining the failing report and database.
    # A recovered Gate must replace both artifacts and discard unrelated hits.
    config.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    current = json.loads((coverage_project / "coverage.json").read_text())
    assert set(current["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    for name in current["files"]:
        assert current["files"][name] == report["files"][name]
    _assert_xml_matches_json(coverage_project, current)

    standalone = subprocess.run(
        [sys.executable, "scripts/publication_coverage_gate.py"],
        cwd=coverage_project,
        capture_output=True,
        text=True,
        check=False,
    )
    assert standalone.returncode == 0, standalone.stdout + standalone.stderr
    assert standalone.stderr == ""
    assert standalone.stdout == "Ready publication coverage floors PASS\n"


@pytest.mark.parametrize("execution", ["in-process", "subprocess"])
@pytest.mark.parametrize("failure_phase", ["test", "setup", "teardown"])
def test_pytest_gate_preserves_test_failure_with_passing_coverage(
    coverage_project: Path, execution: str, failure_phase: str
) -> None:
    """Meeting every coverage floor must preserve test and fixture failures."""
    from scripts.publication_coverage_gate import check_report

    if execution == "subprocess":
        _exercise_in_subprocess(coverage_project)
    exercise = coverage_project / "tests/test_exercise.py"
    original = exercise.read_text()
    failure = '    raise AssertionError("intentional functional failure")\n'
    if failure_phase == "test":
        failing_test = original + "\n" + failure
    else:
        # Exercise both publication scripts before failing setup or teardown,
        # so the coverage gate passes and pytest alone owns the error result.
        failing_test = (
            "import pytest\n"
            + original.replace("def test_exercise():", "def exercise():")
            + "\n@pytest.fixture\ndef publication():\n"
            "    exercise()\n"
            + (failure + "    yield\n" if failure_phase == "setup" else "    yield\n" + failure)
            + "\ndef test_exercise(publication):\n    pass\n"
        )
    exercise.write_text(failing_test)

    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert ("1 failed" if failure_phase == "test" else "1 error") in output
    if failure_phase != "test":
        assert f"ERROR at {failure_phase} of test_exercise" in output
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
def test_repairing_functional_failure_does_not_clear_publication_regression(
    coverage_project: Path, name: str
) -> None:
    """Gate must keep rejecting a coverage loss after a concurrent test failure is fixed."""
    source = coverage_project / "src/my_project/unexecuted.py"
    source.write_text("ANSWER = 42\n")
    exercise = coverage_project / "tests/test_exercise.py"
    complete = (
        exercise.read_text()
        + "    assert runpy.run_path('src/my_project/unexecuted.py')['ANSWER'] == 42\n"
    )
    exercise.write_text(complete)
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())

    regression = complete.replace(
        "        assert choose(False) == 0\n",
        f"        if path != {name!r}:\n            assert choose(False) == 0\n",
    )
    for functional_failure in (True, False):
        exercise.write_text(
            regression
            + (
                '    raise AssertionError("concurrent functional failure")\n'
                if functional_failure
                else ""
            )
        )
        result = _run_coverage_project(coverage_project)
        output = result.stdout + result.stderr
        assert result.returncode == 1, output
        assert ("1 failed" if functional_failure else "1 passed") in output
        assert "INTERNALERROR" not in output
        assert "FAIL Required test coverage" not in output
        errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
        assert len(errors) == 2, output
        for metric, error in zip(("line", "branch"), errors, strict=True):
            assert error.startswith(f"PUBLICATION COVERAGE: {name}: {metric} coverage ")
            assert "below floor" in error
        report = json.loads(report_path.read_text())
        _assert_xml_matches_json(coverage_project, report)
        assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
        assert set(report["files"]) == set(before["files"])
        for path in before["files"]:
            previous, current = (data["files"][path]["summary"] for data in (before, report))
            for covered in ("covered_lines", "covered_branches"):
                assert current[covered] == previous[covered] - int(path == name)

    exercise.write_text(complete)
    restored = _run_coverage_project(coverage_project)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    assert "PUBLICATION COVERAGE:" not in restored.stdout + restored.stderr
    assert json.loads(report_path.read_text())["files"] == before["files"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize("metric", ["line", "branch"])
@pytest.mark.parametrize("execution", ["in-process", "subprocess", "nested-subprocess"])
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

    if execution != "in-process":
        _exercise_in_subprocess(
            coverage_project, depth=2 if execution == "nested-subprocess" else 1
        )

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: {name}: {metric} coverage" in output
    assert "below floor" in output
    assert "INTERNALERROR" not in output

    report = json.loads((coverage_project / "coverage.json").read_text())
    assert set(report["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
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
@pytest.mark.parametrize("outcome", ["skip", "xfail"])
def test_suppressed_branch_test_still_fails_publication_floor(
    coverage_project: Path, name: str, outcome: str
) -> None:
    """Skipped and unexecuted xfails cannot hide a loss behind successful pytest outcomes."""
    script = coverage_project / name
    # An implicit false branch has no exclusive line: suppressing its test
    # leaves line coverage intact and the aggregate above its configured floor.
    script.write_text(script.read_text().replace("    return 0\n", ""))
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        "import pytest\n"
        + exercise.read_text().replace(
            "        assert choose(False) == 0\n",
            f"        if path != {name!r}:\n            assert choose(False) == 0\n",
        )
        + "\ndef test_publication_false_branch():\n"
        f"    assert runpy.run_path({name!r})['choose'](False) is None\n"
    )
    original = exercise.read_bytes()
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())

    marker = (
        "@pytest.mark.skip(reason='suppressed branch regression control')\n"
        if outcome == "skip"
        else "@pytest.mark.xfail(run=False, reason='suppressed branch regression control')\n"
    )
    exercise.write_text(
        exercise.read_text().replace(
            "def test_publication_false_branch():", marker + "def test_publication_false_branch():"
        )
    )
    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert f"1 passed, 1 {'skipped' if outcome == 'skip' else 'xfailed'}" in output
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert len(errors) == 1, output
    assert errors[0].startswith(f"PUBLICATION COVERAGE: {name}: branch coverage ")
    assert "below floor" in errors[0]
    assert "INTERNALERROR" not in output
    after = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, after)
    assert after["totals"]["percent_covered"] >= _load_baseline()["line"]
    for path in before["files"]:
        previous, current = (report["files"][path]["summary"] for report in (before, after))
        assert current["covered_lines"] == previous["covered_lines"]
        assert current["num_statements"] == previous["num_statements"]
        assert current["num_branches"] == previous["num_branches"]
        assert current["covered_branches"] == previous["covered_branches"] - int(path == name)

    exercise.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    assert json.loads(report_path.read_text())["files"] == before["files"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize("metric", ["line", "branch"])
@pytest.mark.parametrize(
    "floor_increase",
    [0.0001, 0.0000001, 0.0000000001],
    ids=["displayed", "sub-display", "sub-tolerance"],
)
def test_pytest_gate_uses_configured_publication_floor(
    coverage_project: Path, name: str, metric: str, floor_increase: float
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
    # this script's configured metric. Even a change hidden by the diagnostic's
    # six decimal places must fail; formatting must never round a loss away.
    baseline["publication_scripts"][name][metric] = measured + floor_increase
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
        f"below floor {measured + floor_increase:.6f}%"
    ]
    current = json.loads(report_path.read_text())
    assert current["files"] == previous["files"]
    assert current["totals"]["percent_covered"] >= baseline["line"]


@pytest.mark.parametrize("line_regression", [None, *sorted(PUBLICATION_FILES)])
@pytest.mark.parametrize("repair_first", sorted(PUBLICATION_FILES))
def test_pytest_gate_tracks_simultaneous_losses_until_both_are_restored(
    coverage_project: Path, line_regression: str | None, repair_first: str
) -> None:
    """Repairing one script must not hide the other script's remaining regression."""
    names = sorted(PUBLICATION_FILES)
    for name in names:
        script = coverage_project / name
        script.write_text(script.read_text().replace("    return 0\n", ""))
        if name == line_regression:
            script.write_text(script.read_text() + "\ndef extra():\n    return 2\n")
    (coverage_project / "src/my_project/unexecuted.py").write_text("ANSWER = 42\n")
    exercise = coverage_project / "tests/test_exercise.py"
    complete = exercise.read_text().replace(
        "        assert choose(False) == 0\n", "        choose(False)\n"
    )
    complete += "    assert runpy.run_path('src/my_project/unexecuted.py')['ANSWER'] == 42\n"

    for remaining in (names, [name for name in names if name != repair_first], []):
        exercise.write_text(
            complete.replace(
                "        choose(False)\n",
                f"        if path not in {remaining!r} or path == {line_regression!r}:\n"
                "            choose(False)\n"
                f"        if path == {line_regression!r} and path not in {remaining!r}:\n"
                "            assert runpy.run_path(path)['extra']() == 2\n",
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
            metric = "line" if name == line_regression else "branch"
            assert error.startswith(f"PUBLICATION COVERAGE: {name}: {metric} coverage ")
            assert "below floor" in error

        report = json.loads((coverage_project / "coverage.json").read_text())
        _assert_xml_matches_json(coverage_project, report)
        assert report["totals"]["percent_covered"] >= _load_baseline()["line"]
        for name in names:
            summary = report["files"][name]["summary"]
            assert summary["missing_lines"] == int(name == line_regression and name in remaining)
            assert summary["missing_branches"] == int(name != line_regression and name in remaining)


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize("collection_only", [False, True], ids=["absent", "collection-only"])
def test_pytest_gate_rejects_unexecuted_script_despite_previous_passing_report(
    coverage_project: Path, name: str, collection_only: bool
) -> None:
    """Collection-time imports cannot replace the removed execution tests for either script."""
    exercise = coverage_project / "tests/test_exercise.py"
    source_exercise = ""
    if collection_only:
        # Keep the aggregate above its floor even when importing the script
        # records only its function definition, with no exercised body or branches.
        (coverage_project / "src/my_project/unexecuted.py").write_text(
            "".join(f"value_{index} = {index}\n" for index in range(30))
        )
        source_exercise = "    runpy.run_path('src/my_project/unexecuted.py')\n"
        exercise.write_text(exercise.read_text() + source_exercise)
    original = exercise.read_bytes()
    previous = _run_coverage_project(coverage_project)
    assert previous.returncode == 0, previous.stdout + previous.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())
    assert set(before["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}

    remaining = next(path for path in PUBLICATION_FILES if path != name)
    collection = f"runpy.run_path({name!r})\n\n" if collection_only else ""
    exercise.write_text(
        "import runpy\n\n"
        + collection
        + "def test_exercise():\n"
        + source_exercise
        + f"    choose = runpy.run_path({remaining!r})['choose']\n"
        "    assert choose(True) == 1\n"
        "    assert choose(False) == 0\n"
    )

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]

    current = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, current)
    if collection_only:
        assert set(current["files"]) == set(before["files"])
        summary = current["files"][name]["summary"]
        assert summary["covered_lines"] == 1
        assert summary["num_statements"] == 4
        assert summary["covered_branches"] == 0
        assert summary["num_branches"] == 2
        assert len(errors) == 2
        for metric, error in zip(("line", "branch"), errors, strict=True):
            assert error.startswith(f"PUBLICATION COVERAGE: {name}: {metric} coverage ")
            assert "below floor" in error
    else:
        assert set(current["files"]) == {remaining, "src/my_project/unexecuted.py"}
        assert errors == [f"PUBLICATION COVERAGE: {name}: missing coverage measurement"]
    assert current["totals"]["percent_covered"] >= _load_baseline()["line"]
    summary = current["files"][remaining]["summary"]
    assert summary["covered_lines"] == summary["num_statements"]
    assert summary["covered_branches"] == summary["num_branches"]

    exercise.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    assert "PUBLICATION COVERAGE:" not in restored.stdout + restored.stderr
    report = json.loads(report_path.read_text())
    assert report["files"] == before["files"]
    _assert_xml_matches_json(coverage_project, report)


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
@pytest.mark.parametrize("phase", ["run", "report"])
@pytest.mark.parametrize("filter_kind", ["omit", "include"])
def test_pytest_gate_rejects_filter_hiding_publication_script(
    coverage_project: Path, name: str, phase: str, filter_kind: str
) -> None:
    """Collection and report filters cannot hide either script behind stale evidence."""
    from coverage import CoverageData

    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())

    config = coverage_project / "pyproject.toml"
    original = config.read_bytes()
    # Hide one script either before tracing or only when generating reports.
    # Dropping an include entry models accidental narrowing of the measured
    # source set; omit models an exclusion overriding that set.
    section = f"[tool.coverage.{phase}]\n"
    if filter_kind == "omit":
        config.write_text(config.read_text().replace(section, f'{section}omit = ["{name}"]\n'))
    else:
        before, settings = config.read_text().split(section, 1)
        settings = settings.replace(f', "{name}"', "", 1)
        config.write_text(before + section + settings)

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
    assert bool(data.lines(str(coverage_project / name))) == (phase == "report")
    report = json.loads(report_path.read_text())
    assert set(report["files"]) == (PUBLICATION_FILES - {name}) | {"src/my_project/unexecuted.py"}
    assert report["totals"]["percent_covered"] >= _load_baseline()["line"]

    config.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "PUBLICATION COVERAGE:" not in output
    current = json.loads(report_path.read_text())
    assert current["files"] == previous["files"]
    _assert_xml_matches_json(coverage_project, current)


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
    """Reject one lost hit at the recorded floors despite passing display percentages."""
    evidence = json.loads(
        (REPO_ROOT / "docs/evidence/issue-623-publication-coverage.json").read_text()
    )
    report = {"files": {name: {"summary": evidence["files"][name]} for name in PUBLICATION_FILES}}
    # Rounded or stale display fields cannot replace independent hit counts.
    for measurement in report["files"].values():
        measurement["summary"].update(percent_covered=100.0, percent_covered_display="100")
    report["totals"] = {"percent_covered": 100.0}
    if regression is not None:
        name, metric, covered = regression
        summary = report["files"][name]["summary"]
        summary[covered] -= 1
        total = "num_statements" if metric == "line" else "num_branches"
        measured = 100 * summary[covered] / summary[total]

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
            f"{name}: {metric} coverage {measured:.6f}% below floor "
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
@pytest.mark.parametrize(
    "invalid",
    ["missing", "directory", "malformed-json", "invalid-utf8", "non-object", "empty-object"],
)
def test_publication_gate_cli_rejects_invalid_evidence_and_recovers(
    tmp_path: Path, document, invalid
):
    """Invalid evidence must fail cleanly and pass only after the document is repaired."""
    paths = {name: tmp_path / f"{name}.json" for name in ("report", "baseline")}
    paths["report"].write_text(json.dumps(_measured_report()))
    paths["baseline"].write_text(json.dumps(_load_baseline()))
    path = paths[document]
    original = path.read_bytes()
    if invalid in ("missing", "directory"):
        path.unlink()
        if invalid == "directory":
            path.mkdir()
    elif invalid == "malformed-json":
        path.write_text('{"incomplete":')
    elif invalid == "invalid-utf8":
        path.write_bytes(b"\xff")
    else:
        path.write_text("null" if invalid == "non-object" else "{}")

    command = [
        sys.executable,
        str(REPO_ROOT / "scripts/publication_coverage_gate.py"),
        "--report",
        str(paths["report"]),
        "--baseline",
        str(paths["baseline"]),
    ]
    result = subprocess.run(
        command,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    if invalid == "non-object":
        assert result.stdout == "Coverage report and baseline must be JSON objects\n"
    elif invalid == "empty-object":
        if document == "report":
            assert result.stdout == "".join(
                f"{name}: missing coverage measurement\n" for name in sorted(PUBLICATION_FILES)
            )
        else:
            assert result.stdout == (
                "publication_scripts must name exactly the two Ready-owned scripts\n"
            )
    else:
        assert result.stdout.startswith(f"Cannot load publication coverage {document} {path}:")
    assert result.stderr == ""
    assert "PASS" not in result.stdout

    if path.is_dir():
        path.rmdir()
    path.write_bytes(original)
    restored = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, check=False)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    assert restored.stdout == "Ready publication coverage floors PASS\n"
    assert restored.stderr == ""


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize("regression", [None, "line", "branch"], ids=["complete", "line", "branch"])
@pytest.mark.parametrize("invocation", ["relative", "absolute"])
@pytest.mark.parametrize("exit_status", [0, 1], ids=["accepted", "rejected"])
def test_publication_coverage_tracks_subprocess_regressions(
    coverage_project: Path, name: str, regression: str | None, invocation: str, exit_status: int
) -> None:
    """Accepted and rejected CLI runs must enforce either script's independent floors."""
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
        f"        code += '; raise SystemExit({exit_status})'\n"
        "        result = subprocess.run(\n"
        "            [sys.executable, '-c', code], check=False, capture_output=True, text=True\n"
        "        )\n"
        f"        assert result.returncode == {exit_status}\n"
        "        assert result.stderr == '', result.stderr\n"
    )

    result = _run_coverage_project(coverage_project)
    output = result.stdout + result.stderr
    assert result.returncode == int(regression is not None), output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    report = json.loads((coverage_project / "coverage.json").read_text())
    _assert_xml_matches_json(coverage_project, report)
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


@pytest.mark.parametrize("execution", ["in-process", "subprocess"])
def test_publication_gate_includes_fixture_teardown_and_detects_its_removal(
    coverage_project: Path, execution: str
) -> None:
    """Report only after fixture cleanup, including CLI hits produced during teardown."""
    (coverage_project / "src/my_project/unexecuted.py").write_text("ANSWER = 42\n")
    for name in PUBLICATION_FILES:
        script = coverage_project / name
        script.write_text(script.read_text().replace("    return 0\n", ""))
    exercise = coverage_project / "tests/test_exercise.py"
    complete_test = (
        "import runpy\nimport subprocess\nimport sys\nimport pytest\n\n"
        "def exercise(flag):\n"
        f"    for path in {sorted(PUBLICATION_FILES)!r}:\n"
        + (
            "        subprocess.run([sys.executable, '-c',\n"
            "            f\"import runpy; runpy.run_path({path!r})['choose']({flag!r})\"],\n"
            "            check=True)\n"
            if execution == "subprocess"
            else "        runpy.run_path(path)['choose'](flag)\n"
        )
        + "\n@pytest.fixture\ndef publication():\n"
        "    assert runpy.run_path('src/my_project/unexecuted.py')['ANSWER'] == 42\n"
        "    exercise(True)\n"
        "    yield\n"
        "    exercise(False)\n\n"
        "def test_publication(publication):\n"
        "    pass\n"
    )
    exercise.write_text(complete_test)
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, before)

    # Leave successful artifacts in place. Only teardown exercises the false
    # branch, so dropping cleanup must fail despite passing test assertions.
    exercise.write_text(complete_test.replace("    exercise(False)\n", ""))
    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    after = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, after)
    assert set(after["files"]) == set(before["files"])
    assert after["totals"]["percent_covered"] >= _load_baseline()["line"]
    for name in PUBLICATION_FILES:
        original = before["files"][name]["summary"]
        reduced = after["files"][name]["summary"]
        assert original["covered_branches"] == original["num_branches"]
        assert reduced["covered_lines"] == original["covered_lines"]
        assert reduced["covered_branches"] == original["covered_branches"] - 1
        assert f"PUBLICATION COVERAGE: {name}: branch coverage" in output

    exercise.write_text(complete_test)
    restored = _run_coverage_project(coverage_project)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    current = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, current)
    assert current["files"] == before["files"]


def test_pytest_gate_rejects_unmeasured_child_working_directory_and_recovers(
    coverage_project: Path,
) -> None:
    """Child cwd changes must not let a prior report replace missing CLI measurements."""
    _exercise_in_subprocess(coverage_project)
    runner = coverage_project / "exercise_cli_0.py"
    runner.write_text(
        "import runpy\n\n"
        f"for path in {[str(coverage_project / name) for name in sorted(PUBLICATION_FILES)]!r}:\n"
        "    choose = runpy.run_path(path)['choose']\n"
        "    assert choose(True) == 1\n"
        "    assert choose(False) == 0\n"
    )
    (coverage_project / "src/my_project/unexecuted.py").write_text("ANSWER = 42\n")
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        "import runpy\n"
        + exercise.read_text()
        + "    assert runpy.run_path('src/my_project/unexecuted.py')['ANSWER'] == 42\n"
    )
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())

    # Coverage's relative run includes resolve against the child's cwd. A
    # child launched elsewhere still passes its assertions but is unmeasured.
    original = exercise.read_bytes()
    child_cwd = coverage_project / "export-stage"
    child_cwd.mkdir()
    exercise.write_text(
        "import runpy\nimport subprocess\nimport sys\n\n"
        "def test_exercise():\n"
        "    assert runpy.run_path('src/my_project/unexecuted.py')['ANSWER'] == 42\n"
        f"    subprocess.run([sys.executable, {str(runner)!r}], cwd={str(child_cwd)!r}, check=True)\n"
    )
    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    for name in PUBLICATION_FILES:
        assert f"PUBLICATION COVERAGE: {name}: missing coverage measurement" in output
    current = json.loads(report_path.read_text())
    assert set(current["files"]) == {"src/my_project/unexecuted.py"}
    assert current["totals"]["percent_covered"] == 100

    exercise.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "PUBLICATION COVERAGE:" not in output
    assert json.loads(report_path.read_text())["files"] == previous["files"]


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

    def assert_artifacts_and_standalone_gate(report: dict, errors: list[str]) -> None:
        _assert_xml_matches_json(coverage_project, report)
        standalone = subprocess.run(
            [sys.executable, "scripts/publication_coverage_gate.py"],
            cwd=coverage_project,
            capture_output=True,
            text=True,
            check=False,
        )
        assert standalone.returncode == int(bool(errors)), standalone.stdout + standalone.stderr
        assert standalone.stderr == ""
        expected = "\n".join(errors) if errors else "Ready publication coverage floors PASS"
        assert standalone.stdout == expected + "\n"

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
    assert_artifacts_and_standalone_gate(before, [])
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
    assert_artifacts_and_standalone_gate(
        report, [line.removeprefix("PUBLICATION COVERAGE: ") for line in errors]
    )
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
        restored_report = json.loads(report_path.read_text())
        assert restored_report["files"] == before["files"]
        assert_artifacts_and_standalone_gate(restored_report, [])


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
    """Only collecting branch evidence may recover a line-only run, including CLI overrides."""
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

    # The CLI override must take precedence over branch=false in the config.
    # Retain the line-only database and report to exercise the data-mode switch.
    restored = _run_coverage_project(coverage_project, "--cov-branch")
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    current = json.loads((coverage_project / "coverage.json").read_text())
    assert current["meta"]["branch_coverage"] is True
    assert set(current["files"]) == set(report["files"])
    _assert_xml_matches_json(coverage_project, current)
    for name in PUBLICATION_FILES:
        summary = current["files"][name]["summary"]
        assert summary["covered_lines"] == summary["num_statements"]
        assert summary["covered_branches"] == summary["num_branches"] > 0

    # Removing the override must fail again, despite the previous branch hits.
    line_only = _run_coverage_project(coverage_project)
    output = line_only.stdout + line_only.stderr
    assert line_only.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    assert "Traceback" not in output
    for name in PUBLICATION_FILES:
        assert f"PUBLICATION COVERAGE: {name}: invalid branch measurement or floor" in output
    assert json.loads((coverage_project / "coverage.json").read_text())["files"] == report["files"]


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
@pytest.mark.parametrize(
    "aggregate_floor", [80, 0], ids=["aggregate-enforced", "aggregate-disabled"]
)
@pytest.mark.parametrize("stale_shards", [False, True], ids=["combined-data", "parallel-shards"])
@pytest.mark.parametrize("metric", ["line", "branch"])
def test_previous_passing_run_cannot_mask_removed_coverage_test(
    coverage_project: Path, name: str, aggregate_floor: int, stale_shards: bool, metric: str
) -> None:
    """Fresh evidence controls each script's floors independently of the aggregate threshold."""
    script = coverage_project / name
    exercise = coverage_project / "tests/test_exercise.py"
    if metric == "line":
        # Removing this call loses a line while preserving every branch hit.
        script.write_text(script.read_text() + "\ndef extra():\n    return 2\n")
        removed_exercise = f"    assert runpy.run_path({name!r})['extra']() == 2\n"
        exercise.write_text(exercise.read_text() + removed_exercise)
        replacement = ""
    else:
        # The implicit false branch has no exclusive executable line.
        script.write_text(script.read_text().replace("    return 0\n", ""))
        exercise.write_text(
            exercise.read_text().replace(
                "        assert choose(False) == 0\n", "        choose(False)\n"
            )
        )
        removed_exercise = "        choose(False)\n"
        replacement = f"        if path != {name!r}:\n            choose(False)\n"
    complete_exercise = exercise.read_bytes()
    coverage_args = (f"--cov-fail-under={aggregate_floor}",)
    result = _run_coverage_project(coverage_project, *coverage_args)
    assert result.returncode == 0, result.stdout + result.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    assert (coverage_project / ".coverage").is_file()
    if stale_shards:
        # An interrupted subprocess run can leave uncombined parallel data.
        # Give those files passing hits so combining stale shards would hide
        # the removed exercise even after the combined database is erased.
        for suffix in ("interrupted-cli.12345.abc", "interrupted-cli.12346.def"):
            shutil.copyfile(
                coverage_project / ".coverage", coverage_project / f".coverage.{suffix}"
            )
        (coverage_project / ".coverage").unlink()

    # Remove one exercise without changing production code or clearing
    # the passing report and coverage data left by the previous invocation.
    exercise.write_text(exercise.read_text().replace(removed_exercise, replacement))

    result = _run_coverage_project(coverage_project, *coverage_args)
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "1 passed" in output
    assert f"PUBLICATION COVERAGE: {name}: {metric} coverage" in output
    assert "below floor" in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output

    current = json.loads(report_path.read_text())
    assert set(current["files"]) == set(previous["files"])
    assert current["totals"]["percent_covered"] >= _load_baseline()["line"]
    for path in PUBLICATION_FILES:
        before = previous["files"][path]["summary"]
        after = current["files"][path]["summary"]
        assert after["num_statements"] == before["num_statements"]
        assert after["covered_lines"] == before["covered_lines"] - int(
            path == name and metric == "line"
        )
        assert after["num_branches"] == before["num_branches"]
        assert after["covered_branches"] == before["covered_branches"] - int(
            path == name and metric == "branch"
        )
    _assert_xml_matches_json(coverage_project, current)

    # Restoring the exercise must replace the failing evidence and pass
    # without deleting the report or coverage database in between runs.
    exercise.write_bytes(complete_exercise)
    restored = _run_coverage_project(coverage_project, *coverage_args)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    assert "PUBLICATION COVERAGE:" not in restored.stdout + restored.stderr
    restored_report = json.loads(report_path.read_text())
    assert set(restored_report["files"]) == set(previous["files"])
    for path in PUBLICATION_FILES:
        assert restored_report["files"][path]["summary"] == previous["files"][path]["summary"]
    _assert_xml_matches_json(coverage_project, restored_report)


@pytest.mark.parametrize("name", sorted(PUBLICATION_FILES))
def test_last_failed_selection_cannot_reuse_unselected_branch_hits(
    coverage_project: Path, name: str
) -> None:
    """A repaired --lf rerun must fail coverage until the branch test runs again."""
    script = coverage_project / name
    # The implicit false branch has no exclusive line, keeping the aggregate
    # above 80% when only that branch's test is omitted by the failure cache.
    script.write_text(script.read_text().replace("    return 0\n", ""))
    exercise = coverage_project / "tests/test_exercise.py"
    complete_test = (
        "import runpy\n\n"
        "def test_exercise():\n"
        f"    for path in {sorted(PUBLICATION_FILES)!r}:\n"
        "        choose = runpy.run_path(path)['choose']\n"
        "        assert choose(True) == 1\n"
        f"        if path != {name!r}:\n"
        "            assert choose(False) == 0\n"
        "    assert 1 == 1\n\n"
        "def test_false_branch():\n"
        f"    assert runpy.run_path({name!r})['choose'](False) is None\n"
    )
    exercise.write_text(complete_test)
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())

    # Populate pytest's real lastfailed cache without losing any coverage.
    exercise.write_text(complete_test.replace("    assert 1 == 1\n", "    assert 1 == 2\n"))
    failed = _run_coverage_project(coverage_project)
    output = failed.stdout + failed.stderr
    assert failed.returncode == 1, output
    assert "1 failed, 1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output

    exercise.write_text(complete_test)
    selected = _run_coverage_project(coverage_project, "--lf")
    output = selected.stdout + selected.stderr
    assert selected.returncode == 1, output
    assert "1 passed" in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert len(errors) == 1, output
    assert errors[0].startswith(f"PUBLICATION COVERAGE: {name}: branch coverage ")
    assert "below floor" in errors[0]

    current = json.loads(report_path.read_text())
    assert set(current["files"]) == set(previous["files"])
    assert current["totals"]["percent_covered"] >= _load_baseline()["line"]
    for path in PUBLICATION_FILES:
        before = previous["files"][path]["summary"]
        after = current["files"][path]["summary"]
        assert after["num_statements"] == before["num_statements"]
        assert after["covered_lines"] == before["covered_lines"]
        assert after["num_branches"] == before["num_branches"]
        assert after["covered_branches"] == before["covered_branches"] - int(path == name)
    _assert_xml_matches_json(coverage_project, current)

    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "2 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    report = json.loads(report_path.read_text())
    assert report["files"] == previous["files"]
    _assert_xml_matches_json(coverage_project, report)


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
def test_publication_gate_combines_test_contexts_without_masking_removed_branch(
    coverage_project: Path, name: str
) -> None:
    """Hits split across test contexts must combine, but only for tests still selected."""
    names = sorted(PUBLICATION_FILES)
    for script in names:
        path = coverage_project / script
        # The false path has no separate line, so removing its test loses only a branch.
        path.write_text(path.read_text().replace("    return 0\n", ""))
    config = coverage_project / "pyproject.toml"
    config.write_text(config.read_text() + "\n[tool.coverage.json]\nshow_contexts = true\n")
    exercise = coverage_project / "tests/test_exercise.py"
    exercise.write_text(
        "import runpy\n\n"
        "def test_true():\n"
        f"    for path in {names!r}:\n"
        "        assert runpy.run_path(path)['choose'](True) == 1\n\n"
        + "\n".join(
            f"def test_false_{index}():\n"
            f"    assert runpy.run_path({script!r})['choose'](False) is None\n"
            for index, script in enumerate(names)
        )
    )
    args = ("--cov-context=test",)
    complete = _run_coverage_project(coverage_project, *args)
    assert complete.returncode == 0, complete.stdout + complete.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, before)
    for index, script in enumerate(names):
        contexts = {
            context for values in before["files"][script]["contexts"].values() for context in values
        }
        assert contexts == {
            "tests/test_exercise.py::test_true|run",
            f"tests/test_exercise.py::test_false_{index}|run",
        }

    removed = _run_coverage_project(
        coverage_project, *args, "-k", f"not test_false_{names.index(name)}"
    )
    output = removed.stdout + removed.stderr
    assert removed.returncode == 1, output
    assert "2 passed, 1 deselected" in output
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert len(errors) == 1, output
    assert errors[0].startswith(f"PUBLICATION COVERAGE: {name}: branch coverage ")
    after = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, after)
    assert (
        set(after["files"])
        == set(before["files"])
        == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    )
    assert after["totals"]["percent_covered"] >= _load_baseline()["line"]
    for script in names:
        original, reduced = (report["files"][script]["summary"] for report in (before, after))
        assert reduced["covered_lines"] == original["covered_lines"]
        assert reduced["num_branches"] == original["num_branches"]
        assert reduced["covered_branches"] == original["covered_branches"] - int(script == name)

    restored = _run_coverage_project(coverage_project, *args)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    restored_report = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, restored_report)
    assert set(restored_report["files"]) == set(before["files"])
    for script, original in before["files"].items():
        restored_file = restored_report["files"][script]
        assert restored_file["summary"] == original["summary"]
        # Coverage does not guarantee the ordering of context names in a report.
        assert {line: set(contexts) for line, contexts in restored_file["contexts"].items()} == {
            line: set(contexts) for line, contexts in original["contexts"].items()
        }


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


def _use_real_publication_tests(project: Path) -> None:
    """Replace the synthetic exercise with the repository's publication tests."""
    (project / "tests/test_exercise.py").unlink()
    for relative in (
        "scripts/check_publication_safety.py",
        "scripts/prepare_publication.py",
        "scripts/publication_patterns.py",
        "tests/test_publication_safety.py",
        "tests/test_prepare_publication.py",
    ):
        shutil.copyfile(REPO_ROOT / relative, project / relative)


@pytest.mark.parametrize(
    "changed_files",
    [(name,) for name in sorted(PUBLICATION_FILES)] + [tuple(sorted(PUBLICATION_FILES))],
    ids=["scanner", "preparer", "both"],
)
def test_real_publication_source_addition_fails_gate(
    coverage_project: Path, changed_files: tuple[str, ...]
) -> None:
    """New untested production paths must breach the floor without removing any tests."""
    _use_real_publication_tests(coverage_project)
    args = ("-k", "not workflow and not gate_summary")
    complete = _run_coverage_project(coverage_project, *args)
    assert complete.returncode == 0, complete.stdout + complete.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())

    originals = {name: (coverage_project / name).read_bytes() for name in changed_files}
    added = (
        b"\n\ndef untested_publication_path(flag):\n    if flag:\n        return 1\n    return 0\n"
    )
    for name, original in originals.items():
        (coverage_project / name).write_bytes(original + added)

    failing = _run_coverage_project(coverage_project, *args)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert re.search(r"\d+ passed", output), output
    assert "FAILED " not in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output
    after = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, after)
    assert set(after["files"]) == set(before["files"])
    assert after["totals"]["percent_covered"] >= _load_baseline()["line"]
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert len(errors) == 2 * len(changed_files), output
    for name in PUBLICATION_FILES - set(changed_files):
        assert after["files"][name] == before["files"][name]
    for index, name in enumerate(changed_files):
        original_summary = before["files"][name]["summary"]
        summary = after["files"][name]["summary"]
        assert summary["num_statements"] > original_summary["num_statements"]
        assert summary["num_branches"] == original_summary["num_branches"] + 2
        assert summary["covered_branches"] == original_summary["covered_branches"]
        for metric, error in zip(
            ("line", "branch"), errors[2 * index : 2 * index + 2], strict=True
        ):
            assert error.startswith(f"PUBLICATION COVERAGE: {name}: {metric} coverage ")
            assert "below floor" in error

    for name, original in originals.items():
        (coverage_project / name).write_bytes(original)
    restored = _run_coverage_project(coverage_project, *args)
    assert restored.returncode == 0, restored.stdout + restored.stderr
    restored_report = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, restored_report)
    for path in before["files"]:
        assert restored_report["files"][path]["summary"] == before["files"][path]["summary"]


@pytest.mark.parametrize(
    "regressions, lost_metrics",
    [
        (
            (
                (
                    "scripts/check_publication_safety.py",
                    "tests/test_publication_safety.py::test_unreadable_directory_fails_closed",
                ),
            ),
            ("line",),
        ),
        (
            (
                (
                    "scripts/prepare_publication.py",
                    "tests/test_prepare_publication.py::"
                    "test_unreadable_traversal_stops_export_before_writes",
                ),
            ),
            ("line",),
        ),
        (
            (
                (
                    "scripts/check_publication_safety.py",
                    "tests/test_publication_safety.py::test_empty_or_missing_tree_fails",
                ),
            ),
            ("line", "branch"),
        ),
        (
            (
                (
                    "scripts/check_publication_safety.py",
                    "tests/test_publication_safety.py::test_empty_or_missing_tree_fails[True]",
                ),
            ),
            ("line", "branch"),
        ),
        (
            (
                (
                    "scripts/prepare_publication.py",
                    "tests/test_prepare_publication.py::"
                    "test_named_legacy_process_capture_is_wrapped_without_losing_output",
                ),
            ),
            ("line", "branch"),
        ),
        (
            (
                (
                    "scripts/check_publication_safety.py",
                    "tests/test_publication_safety.py::test_empty_or_missing_tree_fails",
                ),
                (
                    "scripts/prepare_publication.py",
                    "tests/test_prepare_publication.py::"
                    "test_named_legacy_process_capture_is_wrapped_without_losing_output",
                ),
            ),
            ("line", "branch"),
        ),
    ],
    ids=[
        "guard-line-only",
        "preparer-line-only",
        "guard",
        "guard-single-case",
        "preparer",
        "both",
    ],
)
def test_real_test_removal_fails_publication_gate(
    coverage_project: Path, regressions: tuple[tuple[str, str], ...], lost_metrics: tuple[str, ...]
) -> None:
    """Reject real line-only and branch losses until the removed tests are restored."""
    _use_real_publication_tests(coverage_project)

    # Workflow-shell tests need the full repository; this isolated reproduction
    # exercises the real publication scripts without copying workflow files.
    args = ("-k", "not workflow and not gate_summary")
    complete = _run_coverage_project(coverage_project, *args)
    assert complete.returncode == 0, complete.stdout + complete.stderr
    report_path = coverage_project / "coverage.json"
    before = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, before)

    removed = _run_coverage_project(
        coverage_project,
        *args,
        *(arg for _, test in regressions for arg in ("--deselect", test)),
    )
    output = removed.stdout + removed.stderr
    assert removed.returncode == 1, output
    assert re.search(r"\d+ passed, \d+ deselected", output), output
    assert "FAILED " not in output
    assert "INTERNALERROR" not in output
    assert "FAIL Required test coverage" not in output

    after = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, after)
    assert (
        set(before["files"])
        == set(after["files"])
        == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    )
    assert after["totals"]["percent_covered"] >= _load_baseline()["line"]
    for name in PUBLICATION_FILES - {name for name, _ in regressions}:
        assert after["files"][name]["summary"] == before["files"][name]["summary"]
    errors = [line for line in output.splitlines() if line.startswith("PUBLICATION COVERAGE:")]
    assert len(errors) == len(lost_metrics) * len(regressions), output
    for index, (name, _) in enumerate(regressions):
        original, reduced = (report["files"][name]["summary"] for report in (before, after))
        for metric, covered, total in (
            ("line", "covered_lines", "num_statements"),
            ("branch", "covered_branches", "num_branches"),
        ):
            assert reduced[total] == original[total]
            if metric not in lost_metrics:
                assert reduced[covered] == original[covered]
            elif name == "scripts/check_publication_safety.py":
                assert reduced[covered] == original[covered] - 1
            else:
                assert reduced[covered] < original[covered]
        start = index * len(lost_metrics)
        for metric, error in zip(
            lost_metrics, errors[start : start + len(lost_metrics)], strict=True
        ):
            assert error.startswith(f"PUBLICATION COVERAGE: {name}: {metric} coverage ")
            assert "below floor" in error

    # Keep the failed report and coverage database in place: restoring test
    # collection must replace that evidence with the original measurements.
    restored = _run_coverage_project(coverage_project, *args)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "PUBLICATION COVERAGE:" not in output
    restored_report = json.loads(report_path.read_text())
    _assert_xml_matches_json(coverage_project, restored_report)
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


def test_pytest_gate_rejects_unrelated_publication_floor_and_recovers(
    coverage_project: Path,
) -> None:
    """Baseline scope drift must fail even when the measured files and coverage pass."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    baseline_path = coverage_project / "config/coverage-baseline.json"
    original = baseline_path.read_bytes()
    baseline = json.loads(original)
    baseline["publication_scripts"]["scripts/ci_coverage_delta.py"] = {
        "line": 0,
        "branch": 0,
    }
    baseline_path.write_text(json.dumps(baseline))

    failing = _run_coverage_project(coverage_project)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert "1 passed" in output
    assert (
        "PUBLICATION COVERAGE: publication_scripts must name exactly the two Ready-owned scripts"
        in output
    )
    assert "INTERNALERROR" not in output
    assert "Traceback" not in output
    current = json.loads(report_path.read_text())
    assert set(current["files"]) == PUBLICATION_FILES | {"src/my_project/unexecuted.py"}
    assert current["files"] == previous["files"]
    assert current["totals"]["percent_covered"] >= baseline["line"]

    baseline_path.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    report = json.loads(report_path.read_text())
    assert report["files"] == previous["files"]
    _assert_xml_matches_json(coverage_project, report)


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


@pytest.mark.parametrize(
    "selection_args, selection_message",
    [
        (("-k", "not test_exercise"), "1 deselected"),
        (("--ignore=tests/test_exercise.py",), "no tests ran"),
    ],
    ids=["deselected", "ignored-module"],
)
def test_pytest_gate_rejects_empty_selection_despite_previous_passing_report(
    coverage_project: Path, selection_args: tuple[str, ...], selection_message: str
) -> None:
    """Empty collection and deselection must both discard earlier publication hits."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())

    failing = _run_coverage_project(coverage_project, *selection_args)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert selection_message in output
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


@pytest.mark.parametrize("failure_phase", ["test", "setup", "teardown"])
def test_suppressed_failure_report_cannot_reuse_previous_publication_evidence(
    coverage_project: Path,
    failure_phase: str,
) -> None:
    """Suppressed reports must discard stale evidence for test and fixture failures."""
    args = ("--no-cov-on-fail",)
    passing = _run_coverage_project(coverage_project, *args)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    exercise = coverage_project / "tests/test_exercise.py"
    original = exercise.read_bytes()
    failure = '    raise AssertionError("suppressed-report regression control")\n'
    if failure_phase == "test":
        exercise.write_text(exercise.read_text() + "\n" + failure)
    else:
        # A fixture error follows a different pytest reporting path from a
        # failed call. In teardown, every publication assertion has already
        # passed, so earlier evidence would look especially plausible.
        exercise.write_text(
            "import pytest\n\n"
            "@pytest.fixture(autouse=True)\n"
            "def broken_fixture():\n"
            + (failure + "    yield\n" if failure_phase == "setup" else "    yield\n" + failure)
            + "\n"
            + exercise.read_text()
        )

    failing = _run_coverage_project(coverage_project, *args)
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert ("1 failed" if failure_phase == "test" else "1 error") in output
    if failure_phase != "test":
        assert f"ERROR at {failure_phase} of test_exercise" in output
    assert "suppressed-report regression control" in output
    assert "PUBLICATION COVERAGE: Current publication coverage evidence unavailable:" in output
    assert "INTERNALERROR" not in output
    assert not report_path.exists(), "A suppressed report must not leave earlier passing evidence"

    exercise.write_bytes(original)
    restored = _run_coverage_project(coverage_project, *args)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    report = json.loads(report_path.read_text())
    assert report["files"] == previous["files"]
    _assert_xml_matches_json(coverage_project, report)


@pytest.mark.parametrize("failure_phase", ["test", "setup", "teardown"])
def test_fail_fast_cannot_reuse_previous_publication_report(
    coverage_project: Path,
    failure_phase: str,
) -> None:
    """An interrupted loop cannot reuse passing evidence and must recover on the next run."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    exercise = coverage_project / "tests/test_exercise.py"
    original = exercise.read_bytes()
    measured, untouched = sorted(PUBLICATION_FILES)
    failure = '    raise AssertionError("fail-fast regression control")\n'
    partial_exercise = (
        f"    choose = runpy.run_path({measured!r})['choose']\n" "    assert choose(True) == 1\n"
    )
    if failure_phase == "test":
        failing_test = "def test_failure():\n" + partial_exercise + failure
    else:
        failing_test = (
            "@pytest.fixture\ndef publication():\n"
            + partial_exercise
            + (failure + "    yield\n" if failure_phase == "setup" else "    yield\n" + failure)
            + "\ndef test_failure(publication):\n    pass\n"
        )
    exercise.write_text(
        "import runpy\nimport pytest\n\n" + failing_test + "\n"
        "def test_never_reached():\n"
        f"    choose = runpy.run_path({untouched!r})['choose']\n"
        "    assert choose(True) == 1\n"
        "    assert choose(False) == 0\n"
    )

    failing = _run_coverage_project(coverage_project, "-x")
    output = failing.stdout + failing.stderr
    assert failing.returncode == 1, output
    assert ("1 failed" if failure_phase == "test" else "1 error") in output
    if failure_phase != "test":
        assert f"ERROR at {failure_phase} of test_failure" in output
    assert "stopping after 1 failures" in output
    assert "INTERNALERROR" not in output
    assert "PUBLICATION COVERAGE:" in output
    assert "Ready publication coverage floors PASS" not in output
    if report_path.exists():
        # If pytest-cov finalizes an interrupted loop, it must contain only
        # current hits and the per-script gate must diagnose the partial run.
        current = json.loads(report_path.read_text())
        assert untouched not in current["files"]
        assert f"PUBLICATION COVERAGE: {untouched}: missing coverage measurement" in output
        assert current["files"][measured]["summary"]["covered_branches"] < (
            previous["files"][measured]["summary"]["covered_branches"]
        )
    else:
        # pytest-cov 7.1.0 does not report when fail-fast raises out of the loop.
        assert "Current publication coverage evidence unavailable:" in output

    exercise.write_bytes(original)
    restored = _run_coverage_project(coverage_project, "-x")
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    assert json.loads(report_path.read_text())["files"] == previous["files"]


def test_interrupted_run_cannot_reuse_previous_publication_report(
    coverage_project: Path,
) -> None:
    """An interrupted run must fail and leave no earlier passing coverage evidence."""
    passing = _run_coverage_project(coverage_project)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())
    exercise = coverage_project / "tests/test_exercise.py"
    original = exercise.read_bytes()
    measured, untouched = sorted(PUBLICATION_FILES)
    exercise.write_text(
        "import runpy\n\n"
        "def test_interrupted():\n"
        f"    choose = runpy.run_path({measured!r})['choose']\n"
        "    assert choose(True) == 1\n"
        '    raise KeyboardInterrupt("interruption regression control")\n'
    )

    interrupted = _run_coverage_project(coverage_project)
    output = interrupted.stdout + interrupted.stderr
    assert interrupted.returncode != 0, output
    assert "KeyboardInterrupt: interruption regression control" in output
    assert "INTERNALERROR" not in output
    assert "PUBLICATION COVERAGE:" in output
    assert "Ready publication coverage floors PASS" not in output
    if report_path.exists():
        current = json.loads(report_path.read_text())
        assert untouched not in current["files"]
        assert f"PUBLICATION COVERAGE: {untouched}: missing coverage measurement" in output
        assert current["files"][measured]["summary"]["covered_branches"] < (
            previous["files"][measured]["summary"]["covered_branches"]
        )
    else:
        assert "Current publication coverage evidence unavailable:" in output

    exercise.write_bytes(original)
    restored = _run_coverage_project(coverage_project)
    output = restored.stdout + restored.stderr
    assert restored.returncode == 0, output
    assert "1 passed" in output
    assert "PUBLICATION COVERAGE:" not in output
    report = json.loads(report_path.read_text())
    assert report["files"] == previous["files"]
    _assert_xml_matches_json(coverage_project, report)


@pytest.mark.parametrize("continue_collection", [False, True], ids=["abort", "continue"])
def test_pytest_gate_rejects_collection_error_despite_previous_passing_report(
    coverage_project: Path, continue_collection: bool
) -> None:
    """Collection errors must fail even if continuing tests satisfies every coverage floor."""
    args = ("--continue-on-collection-errors",) if continue_collection else ()
    passing = _run_coverage_project(coverage_project, *args)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    report_path = coverage_project / "coverage.json"
    previous = json.loads(report_path.read_text())

    broken = coverage_project / "tests/test_broken_collection.py"
    broken.write_text('raise RuntimeError("collection regression control")\n')
    failing = _run_coverage_project(coverage_project, *args)
    output = failing.stdout + failing.stderr
    assert failing.returncode != 0, output
    assert "ERROR collecting tests/test_broken_collection.py" in output
    assert "collection regression control" in output
    assert "INTERNALERROR" not in output
    if continue_collection:
        assert "1 passed, 1 error" in output
        assert "PUBLICATION COVERAGE:" not in output
        current = json.loads(report_path.read_text())
        assert current["files"] == previous["files"]
        _assert_xml_matches_json(coverage_project, current)
    else:
        assert "PUBLICATION COVERAGE:" in output
        assert "1 passed" not in output
    if not continue_collection and report_path.exists():
        current = json.loads(report_path.read_text())
        assert current["totals"]["covered_lines"] == 0
        assert current["totals"]["covered_branches"] == 0

    broken.unlink()
    restored = _run_coverage_project(coverage_project, *args)
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


@pytest.mark.parametrize("workerinput", [{}, {"workerid": "gw0"}], ids=["empty", "identified"])
@pytest.mark.parametrize("exitstatus", [pytest.ExitCode.OK, pytest.ExitCode.TESTS_FAILED])
def test_pytest_workers_preserve_controller_evidence_and_exit_status(
    tmp_path: Path, monkeypatch, workerinput: dict, exitstatus: pytest.ExitCode
) -> None:
    """Workers must leave reporting and combined coverage decisions to the controller."""
    from types import SimpleNamespace

    from tests import conftest

    monkeypatch.setattr(conftest, "ROOT", tmp_path)
    report_path = tmp_path / "coverage.json"
    previous = json.dumps(_measured_report()).encode() + b"\n"
    report_path.write_bytes(previous)
    # Represent an active pytest-cov worker. Its partial data must never be
    # accessed by Ready's controller hooks, even before worker metadata arrives.
    plugin = SimpleNamespace(cov_controller=object())
    config = SimpleNamespace(
        workerinput=workerinput,
        option=SimpleNamespace(collectonly=False),
        getoption=lambda *args, **kwargs: False,
        pluginmanager=SimpleNamespace(getplugin=lambda name: plugin),
    )
    session = SimpleNamespace(config=config, exitstatus=exitstatus)

    conftest.pytest_sessionstart(session)
    assert report_path.read_bytes() == previous
    loop = conftest.pytest_runtestloop(session)
    next(loop)
    with pytest.raises(StopIteration):
        loop.send(None)
    conftest.pytest_sessionfinish(session, exitstatus)

    assert report_path.read_bytes() == previous
    assert session.exitstatus == exitstatus
