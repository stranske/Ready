"""Enforce Ready-owned per-script floors in every coverage-enabled pytest Gate."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.publication_coverage_gate import check_report

ROOT = Path(__file__).resolve().parents[1]


def _coverage_controller(config: pytest.Config) -> bool:
    """True only when pytest-cov actually registered an active controller.

    `--cov-reset` leaves `cov_source` as ``[]`` without registering ``_cov``, so
    checking ``cov_source is not None`` alone would crash the runtestloop hook.
    """
    if (
        hasattr(config, "workerinput")
        or config.getoption("no_cov", default=False)
        or config.option.collectonly
    ):
        return False
    plugin = config.pluginmanager.getplugin("_cov")
    return plugin is not None and getattr(plugin, "cov_controller", None) is not None


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
    if session.config.getoption("cov_append", default=False):
        # A fresh JSON report can still contain hits from an earlier test run.
        errors.append(
            "--cov-append cannot establish current publication coverage; rerun without it"
        )
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
        plugin = session.config.pluginmanager.getplugin("_cov")
        cov = plugin.cov_controller.cov
        data = cov.get_data()
        # Seed the configured data mode so missing branch collection reaches
        # the per-script gate instead of mixing line data with branch data.
        if cov.config.branch:
            data.add_arcs({})
        else:
            data.add_lines({})
        # Coverage's source discovery also includes Windows windowed scripts.
        # Seed both extensions so unexecuted .pyw files stay in the denominator.
        data.touch_files(
            [str(path) for pattern in ("*.py", "*.pyw") for path in (ROOT / "src").rglob(pattern)]
        )
        cov.save()
    return result
