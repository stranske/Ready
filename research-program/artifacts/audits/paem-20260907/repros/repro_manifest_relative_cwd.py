#!/usr/bin/env python3
"""Prove manifest_path_from_run_end returns a cwd-relative path that breaks off-run-dir."""
import json
import os
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4] / "clones" / "Portable-Alpha-Extension-Model"
sys.path.insert(0, str(REPO))

from pa_core.contracts import RUN_END_MANIFEST_PATH_KEY, manifest_path_from_run_end

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    run_dir = td / "runs" / "run-A"
    run_dir.mkdir(parents=True)
    manifest = run_dir / "manifest.json"
    manifest.write_text('{"run":"A"}', encoding="utf-8")
    run_end = run_dir / "run_end.json"
    run_end.write_text(json.dumps({RUN_END_MANIFEST_PATH_KEY: "manifest.json"}), encoding="utf-8")
    os.chdir(run_dir)
    assert manifest_path_from_run_end(run_end).exists()
    os.chdir(td)
    p = manifest_path_from_run_end(run_end)
    assert p is not None
    assert not p.exists()
    print("PASS: relative manifest_path missing when cwd != run output directory")
