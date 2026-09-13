#!/usr/bin/env python3
"""Proof: ppt_status=skipped while distribution PPT succeeds -> misleading DQ."""
from __future__ import annotations

from datetime import date
from pathlib import Path
import tempfile

from counter_risk.config import WorkflowConfig
from counter_risk.pipeline.manifest import ManifestBuilder
import counter_risk.pipeline.run as run_module

fixtures = Path("tests/fixtures")
run_dir = Path(tempfile.mkdtemp(prefix="wiring-ppt-status-"))
config = WorkflowConfig(
    as_of_date=date(2025, 12, 31),
    mosers_all_programs_xlsx=fixtures
    / "MOSERS Counterparty Risk Summary 12-31-2025 - All Programs.xlsx",
    mosers_ex_trend_xlsx=fixtures / "MOSERS Counterparty Risk Summary 12-31-2025 - Ex Trend.xlsx",
    mosers_trend_xlsx=fixtures / "MOSERS Counterparty Risk Summary 12-31-2025 - Trend.xlsx",
    hist_all_programs_3yr_xlsx=fixtures
    / "Historical Counterparty Risk Graphs - All Programs 3 Year.xlsx",
    hist_ex_llc_3yr_xlsx=fixtures / "Historical Counterparty Risk Graphs - ex LLC 3 Year.xlsx",
    hist_llc_3yr_xlsx=fixtures / "Historical Counterparty Risk Graphs - LLC 3 Year.xlsx",
    monthly_pptx=fixtures / "Monthly Counterparty Exposure Report.pptx",
)

orig_refresh = run_module._refresh_ppt_links
run_module._refresh_ppt_links = lambda _path: run_module.PptProcessingResult(
    status=run_module.PptProcessingStatus.SKIPPED,
    error_detail="unsupported platform",
)
try:
    output_paths, ppt_result = run_module._write_outputs(
        run_dir=run_dir,
        config=config,
        as_of_date=date(2025, 12, 31),
        warnings=["PPT links not refreshed; COM refresh skipped"],
    )
finally:
    run_module._refresh_ppt_links = orig_refresh

dist_name = run_module.resolve_ppt_output_names(date(2025, 12, 31)).distribution_filename
manifest = ManifestBuilder(
    config=config,
    as_of_date=date(2025, 12, 31),
    run_date=date(2026, 1, 1),
).build(
    run_dir=run_dir,
    input_hashes={},
    output_paths=[p.relative_to(run_dir) for p in output_paths],
    top_exposures={},
    top_changes_per_variant={},
    warnings=["PPT links not refreshed; COM refresh skipped"],
    ppt_status=ppt_result.status.value,
    ppt_outputs=ppt_result.ppt_outputs,
)

assert (run_dir / dist_name).exists(), "distribution deck missing"
assert manifest["ppt_status"] == "skipped"
assert manifest["ppt_outputs"]["distribution"]["status"] == "success"
assert "PPT_GENERATION_SKIPPED" in {f["code"] for f in manifest["data_quality"]["findings"]}
assert manifest["data_quality"]["overall_status"] == "warn"
print("PASS: distribution exists but manifest reports PPT_GENERATION_SKIPPED (warn)")
