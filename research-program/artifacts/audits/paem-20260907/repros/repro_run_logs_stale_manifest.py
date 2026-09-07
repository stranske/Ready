#!/usr/bin/env python3
"""Prove Run Logs falls back to cwd manifest.json and can show the wrong run."""
import json
import os
import runpy
import sys
import tempfile
from pathlib import Path
from types import ModuleType


class _Col:
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FakeST(ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.calls = []

    def set_page_config(self, **k):
        pass

    def title(self, m):
        pass

    def info(self, m):
        pass

    def warning(self, m):
        pass

    def error(self, m):
        pass

    def subheader(self, m):
        pass

    def code(self, p, language=None):
        self.calls.append(p)

    def text(self, p):
        pass

    def write(self, *a, **k):
        pass

    def stop(self):
        raise SystemExit

    def selectbox(self, label, options):
        return "run-1"

    def columns(self, n):
        return [_Col() for _ in range(n)]


REPO = Path(__file__).resolve().parents[4] / "clones" / "Portable-Alpha-Extension-Model"
page = REPO / "dashboard/pages/7_Run_Logs.py"

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    (td / "runs" / "run-1").mkdir(parents=True)
    (td / "runs" / "run-1" / "run.log").write_text("line\n", encoding="utf-8")
    (td / "manifest.json").write_text(json.dumps({"provenance": "STALE_ROOT_MANIFEST"}))
    fake = FakeST()
    sys.modules["streamlit"] = fake
    os.chdir(td)
    runpy.run_path(str(page))
    shown = fake.calls[0] if fake.calls else ""
    assert "STALE_ROOT_MANIFEST" in shown
    print("PASS: Run Logs displayed cwd manifest.json without run_end.json link")
