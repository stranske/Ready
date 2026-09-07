#!/usr/bin/env python3
"""Prove --bundle captures a pre-finalize manifest missing warnings/cost."""
import json
import sys
import tempfile
import types
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[4] / "clones" / "Portable-Alpha-Extension-Model"
sys.path.insert(0, str(REPO))

sys.modules.setdefault("streamlit", types.ModuleType("streamlit"))
pptx_mod = types.ModuleType("pptx")
pptx_util = types.ModuleType("pptx.util")
pptx_mod.Presentation = object
pptx_util.Inches = lambda x: x
pptx_mod.util = pptx_util
sys.modules.setdefault("pptx", pptx_mod)
sys.modules.setdefault("pptx.util", pptx_util)

import pa_core.reporting.sweep_excel
import pa_core.sweep

pa_core.sweep.run_parameter_sweep = lambda *a, **k: []
pa_core.reporting.sweep_excel.export_sweep_results = lambda *a, **k: None

from pa_core.cli import main

idx = REPO / "data" / "sp500tr_fred_divyield.csv"
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    cfg_path = td / "cfg.yaml"
    cfg_path.write_text(
        yaml.safe_dump({"N_SIMULATIONS": 1, "N_MONTHS": 1, "financing_mode": "broadcast"})
    )
    out_file = td / "out.xlsx"
    out_file.write_bytes(b"stub")
    bundle_dir = td / "bundle"
    main(
        [
            "--config",
            str(cfg_path),
            "--index",
            str(idx),
            "--output",
            str(out_file),
            "--seed",
            "123",
            "--bundle",
            str(bundle_dir),
            "--index-frequency",
            "daily",
            "--log-json",
        ]
    )
    final = json.loads((td / "manifest.json").read_text())
    bundle = json.loads((bundle_dir / "manifest.json").read_text())
    assert final.get("warnings"), "expected finalized warnings"
    assert bundle.get("warnings") is None, "bundle manifest should lack warnings"
    assert final.get("cost") is not None and bundle.get("cost") is None
    print("PASS: bundle manifest stale vs finalized manifest.json")
