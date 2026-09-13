#!/usr/bin/env python3
"""Proof: export_pdf=True is silently ignored when enable_distribution_output=False."""
from __future__ import annotations

from datetime import date
from pathlib import Path
import tempfile

from counter_risk.config import WorkflowConfig
import counter_risk.pipeline.run as run_module

fixtures = Path("tests/fixtures")
run_dir = Path(tempfile.mkdtemp(prefix="wiring-export-pdf-"))
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
    export_pdf=True,
    enable_distribution_output=False,
)

run_module._refresh_ppt_links = lambda _path: run_module.PptProcessingResult(
    status=run_module.PptProcessingStatus.SUCCESS
)
warnings: list[str] = []
output_paths, _ = run_module._write_outputs(
    run_dir=run_dir,
    config=config,
    as_of_date=date(2025, 12, 31),
    warnings=warnings,
)

pdf_outputs = [path for path in output_paths if path.suffix.lower() == ".pdf"]
assert config.export_pdf is True
assert pdf_outputs == []
assert warnings == []
print("PASS: export_pdf=True produced no PDF and no operator warning")
