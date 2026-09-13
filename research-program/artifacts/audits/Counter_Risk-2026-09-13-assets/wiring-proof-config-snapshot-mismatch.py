#!/usr/bin/env python3
"""Proof: manifest config_snapshot paths disagree with input_hashes after NISA generation."""
from __future__ import annotations

from datetime import date
from pathlib import Path
import tempfile

from counter_risk.config import WorkflowConfig
from counter_risk.pipeline.manifest import ManifestBuilder
import counter_risk.pipeline.run as run_module
from counter_risk.pipeline.run import _resolve_input_paths, _sha256_file

fixtures = Path("tests/fixtures")
run_dir = Path(tempfile.mkdtemp(prefix="wiring-snapshot-"))
external_mosers = fixtures / "MOSERS Counterparty Risk Summary 12-31-2025 - All Programs.xlsx"
config = WorkflowConfig(
    as_of_date=date(2025, 12, 31),
    raw_nisa_all_programs_xlsx=fixtures / "NISA Monthly All Programs - Raw.xlsx",
    mosers_all_programs_xlsx=external_mosers,
    mosers_ex_trend_xlsx=fixtures / "MOSERS Counterparty Risk Summary 12-31-2025 - Ex Trend.xlsx",
    mosers_trend_xlsx=fixtures / "MOSERS Counterparty Risk Summary 12-31-2025 - Trend.xlsx",
    hist_all_programs_3yr_xlsx=fixtures
    / "Historical Counterparty Risk Graphs - All Programs 3 Year.xlsx",
    hist_ex_llc_3yr_xlsx=fixtures / "Historical Counterparty Risk Graphs - ex LLC 3 Year.xlsx",
    hist_llc_3yr_xlsx=fixtures / "Historical Counterparty Risk Graphs - LLC 3 Year.xlsx",
    monthly_pptx=fixtures / "Monthly Counterparty Exposure Report.pptx",
)

warnings: list[str] = []
runtime_config = run_module._prepare_runtime_config(
    config=config,
    run_dir=run_dir,
    as_of_date=date(2025, 12, 31),
    warnings=warnings,
)
hashed_path = _resolve_input_paths(runtime_config)["mosers_all_programs_xlsx"]
snapshot_path = ManifestBuilder(
    config=config,
    as_of_date=date(2025, 12, 31),
    run_date=date(2026, 1, 1),
)._serialize_config_snapshot(config)["mosers_all_programs_xlsx"]

assert hashed_path.resolve() != Path(snapshot_path).resolve()
assert _sha256_file(hashed_path) != _sha256_file(external_mosers)
print("PASS: input_hashes file != config_snapshot mosers path (provenance mismatch)")
