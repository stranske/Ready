"""Pytest reproducers run from clone: pytest ../artifacts/.../test_audit_repros.py"""

from __future__ import annotations

import sqlite3
import tempfile
import os

import pytest


@pytest.fixture
def id_schema_db(monkeypatch):
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
        CREATE TABLE holdings (filing_id INTEGER);
        CREATE TABLE news_items (manager_id INTEGER, published_at TEXT);
        """
    )
    conn.commit()
    conn.close()
    monkeypatch.setenv("DB_PATH", path)
    monkeypatch.delenv("DB_URL", raising=False)
    return path


def test_dashboard_load_managers_empty_on_id_schema(id_schema_db):
    from ui import dashboard

    dashboard.load_managers.clear()
    df = dashboard.load_managers()
    assert df.empty


def test_daily_report_fallback_join_fails_on_id_schema(id_schema_db):
    from ui import daily_report

    daily_report.load_diffs.clear()
    with pytest.raises(Exception, match="m.manager_id"):
        daily_report.load_diffs("2026-03-15")


def test_rag_entity_extraction_misses_manager_on_id_schema():
    from chains.rag_search import RAGSearchChain

    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE managers (id INTEGER PRIMARY KEY, name TEXT, cik TEXT)")
    conn.execute("INSERT INTO managers VALUES (1, 'Elliott', '0001791786')")
    conn.commit()
    chain = RAGSearchChain(db_conn=conn)
    entities = chain._entity_extraction("What does Elliott hold?")
    assert entities["manager_ids"] == []


def test_all_managers_summary_qc_warnings_missing_on_id_schema(id_schema_db):
    from ui import dashboard

    summary = dashboard.load_all_managers_summary()
    assert summary["total_managers"] == 1
    assert summary["stale_managers"].empty


def test_alerts_page_not_in_navigation():
    import importlib

    app = importlib.import_module("ui.app")
    pages = app._build_pages()
    titles = [page.title for page in pages]
    url_paths = [page.url_path for page in pages]
    assert "Alerts" not in titles
    assert "alerts" not in url_paths
