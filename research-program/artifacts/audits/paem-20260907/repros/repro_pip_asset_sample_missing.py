#!/usr/bin/env python3
"""Prove bundled asset sample path resolves outside shipped package data on pip layout."""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4] / "clones" / "Portable-Alpha-Extension-Model"
sys.path.insert(0, str(REPO))

from dashboard.utils import SAMPLE_ASSET_TIMESERIES_FILENAME

fake_site = Path("/tmp/paem-fake-site-packages")
fake_utils = fake_site / "dashboard" / "utils.py"
resolved = fake_utils.resolve().parents[1] / "templates" / SAMPLE_ASSET_TIMESERIES_FILENAME
assert not resolved.exists()
print("PASS: pip-style layout has no templates/asset_timeseries_wide_returns.csv at", resolved)
