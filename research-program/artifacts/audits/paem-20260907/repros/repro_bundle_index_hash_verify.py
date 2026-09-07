#!/usr/bin/env python3
"""Prove RunArtifactBundle.verify() ignores index_hash tampering."""
import json
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4] / "clones" / "Portable-Alpha-Extension-Model"
sys.path.insert(0, str(REPO))

from pa_core.run_artifact_bundle import RunArtifact, RunArtifactBundle

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    out = td / "results.txt"
    out.write_text("ok")
    art = RunArtifact(
        config="x: 1\n",
        index_hash="realhash",
        seed=1,
        manifest=None,
        outputs={"r": str(out)},
    )
    RunArtifactBundle(art).save(td / "bundle")
    meta_path = td / "bundle" / "bundle.json"
    meta = json.loads(meta_path.read_text())
    meta["index_hash"] = "TAMPERED"
    meta_path.write_text(json.dumps(meta, indent=2))
    loaded = RunArtifactBundle.load(td / "bundle")
    assert loaded.verify() is True
    assert loaded.artifact.index_hash == "TAMPERED"
    print("PASS: verify() returns True after index_hash tamper")
