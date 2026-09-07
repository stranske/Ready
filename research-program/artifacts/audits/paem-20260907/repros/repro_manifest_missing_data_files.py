#!/usr/bin/env python3
"""Prove ManifestWriter silently drops missing index paths from data_files."""
import json
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[4] / "clones" / "Portable-Alpha-Extension-Model"
sys.path.insert(0, str(REPO))

from pa_core.manifest import ManifestWriter

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    cfg = td / "cfg.yaml"
    cfg.write_text(yaml.safe_dump({"a": 1}))
    missing = td / "missing_index.csv"
    ManifestWriter(td / "manifest.json").write(
        config_path=cfg,
        data_files=[cfg, missing],
        seed=1,
        cli_args={"index": str(missing)},
    )
    manifest = json.loads((td / "manifest.json").read_text())
    assert str(missing) not in manifest["data_files"]
    print("PASS: missing index path omitted from manifest data_files without error")
