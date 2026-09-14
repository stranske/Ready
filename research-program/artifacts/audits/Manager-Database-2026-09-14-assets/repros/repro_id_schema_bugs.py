#!/usr/bin/env python3
"""Offline reproducers for Manager-Database id-column SQLite bugs (base 4523cf5)."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4] / "clones" / "Manager-Database"
sys.path.insert(0, str(REPO))

import os


def _seed_id_schema_db() -> str:
    path = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False).name
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE managers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, cik TEXT);
        INSERT INTO managers VALUES (1, 'Elliott', '0001791786');
        CREATE TABLE daily_diffs (
            manager_id INTEGER, report_date TEXT, cusip TEXT, name_of_issuer TEXT,
            delta_type TEXT, shares_prev REAL, shares_curr REAL, value_prev REAL, value_curr REAL
        );
        INSERT INTO daily_diffs VALUES (1, '2026-03-15', '037833100', 'Apple', 'ADD', 0, 100, 0, 1000);
        CREATE TABLE filings (filing_id INTEGER PRIMARY KEY, manager_id INTEGER, type TEXT, filed_date TEXT);
        INSERT INTO filings VALUES (1, 1, '13F-HR', '2026-01-01');
        """
    )
    conn.commit()
    conn.close()
    return path


def repro_dashboard_load_managers() -> None:
    from ui import dashboard

    path = _seed_id_schema_db()
    os.environ["DB_PATH"] = path
    os.environ.pop("DB_URL", None)
    dashboard.load_managers.clear()
    df = dashboard.load_managers()
    assert df.empty, "expected empty DataFrame masking schema error"
    print("PASS repro_dashboard_load_managers: load_managers() returns empty on id-schema SQLite")


def repro_daily_report_fallback() -> None:
    from ui import daily_report

    path = _seed_id_schema_db()
    os.environ["DB_PATH"] = path
    os.environ.pop("DB_URL", None)
    daily_report.load_diffs.clear()
    try:
        daily_report.load_diffs("2026-03-15")
        raise AssertionError("expected OperationalError from fallback join")
    except Exception as exc:
        assert "m.manager_id" in str(exc)
    print("PASS repro_daily_report_fallback: load_diffs fallback crashes on id-schema SQLite")


def repro_rag_entity_extraction() -> None:
    from chains.rag_search import RAGSearchChain

    path = _seed_id_schema_db()
    conn = sqlite3.connect(path)
    chain = RAGSearchChain(db_conn=conn)
    entities = chain._entity_extraction("What does Elliott hold?")
    assert entities["manager_ids"] == [], entities
    print("PASS repro_rag_entity_extraction: RAG misses manager on id-schema SQLite")


def repro_alerts_page_unreachable() -> None:
    import importlib

    app = importlib.import_module("ui.app")
    pages = app._build_pages()
    titles = [getattr(p, "title", str(p)) for p in pages]
    url_paths = [getattr(p, "url_path", None) for p in pages]
    assert "Alerts" not in titles and "alerts" not in url_paths
    assert importlib.util.find_spec("ui.alerts") is not None
    print("PASS repro_alerts_page_unreachable: ui/alerts.py exists but is not registered in ui/app.py")


if __name__ == "__main__":
    repro_dashboard_load_managers()
    repro_daily_report_fallback()
    repro_rag_entity_extraction()
    repro_alerts_page_unreachable()
