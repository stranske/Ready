"""Enforce Ready-owned per-script floors in every coverage-enabled pytest Gate."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.publication_coverage_gate import check_report

ROOT = Path(__file__).resolve().parents[1]


def _coverage_controller(config: pytest.Config) -> bool:
    return (
        not hasattr(config, "workerinput")
        and config.getoption("cov_source", default=None) is not None
        and not config.getoption("no_cov", default=False)
        and not config.option.collectonly
    )


def pytest_sessionstart(session: pytest.Session) -> None:
    if _coverage_controller(session.config):
        # A restored artifact must never stand in for this run's measurement.
        (ROOT / "coverage.json").unlink(missing_ok=True)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if not _coverage_controller(session.config):
        return
    try:
        report = json.loads((ROOT / "coverage.json").read_text())
        baseline = json.loads((ROOT / "config/coverage-baseline.json").read_text())
        errors = check_report(report, baseline)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors = [f"Current publication coverage evidence unavailable: {exc}"]
    if errors:
        reporter = session.config.pluginmanager.getplugin("terminalreporter")
        if reporter:
            for error in errors:
                reporter.write_line("PUBLICATION COVERAGE: " + error, red=True)
        session.exitstatus = pytest.ExitCode.TESTS_FAILED


@pytest.hookimpl(wrapper=True, trylast=True)
def pytest_runtestloop(session):
    result = yield
    if _coverage_controller(session.config):
        # Preserve source=src's discovery of unexecuted product files while
        # exact include paths keep synced scripts and fixture copies out.
        cov = session.config.pluginmanager.getplugin("_cov").cov_controller.cov
        data = cov.get_data()
        data.add_arcs({})
        data.touch_files([str(path) for path in (ROOT / "src").rglob("*.py")])
        cov.save()
    return result
