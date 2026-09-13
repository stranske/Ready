#!/usr/bin/env python3
"""Proof: screenshot_inputs and exposure_summary_xlsx are omitted from input_hashes."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from counter_risk.config import WorkflowConfig
from counter_risk.pipeline.run import _resolve_input_paths

fixtures = Path("tests/fixtures")
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
    exposure_summary_xlsx=fixtures
    / "MOSERS Counterparty Risk Summary 12-31-2025 - All Programs.xlsx",
    screenshot_inputs={"section_a": fixtures / "Monthly Counterparty Exposure Report.pptx"},
)

resolved = _resolve_input_paths(config)
assert "exposure_summary_xlsx" not in resolved
assert not any("screenshot" in key for key in resolved)
print("PASS: optional runtime inputs absent from _resolve_input_paths / input_hashes")
