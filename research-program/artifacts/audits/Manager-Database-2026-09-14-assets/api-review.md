# Manager-Database API/UI Audit — Track D (read-only)

**Repo:** stranske/Manager-Database  
**Base SHA:** `4523cf50dac3f3fe2ba338b8243e630940c54fd0`  
**Audit date:** 2026-09-14  
**Scope:** `api/`, `alerts/`, `chains/`, `ui/`, `web/`, `pyproject.toml` and related tests  
**Mode:** Read-only; no issues filed; no clone edits  

## Executive summary

Reviewed production-reachable API/UI seams at base `4523cf5` (1651 tests collected; CI green). The FastAPI surface (`api/chat.py`, `api/alerts.py`, `api/signals.py`, `api/activism.py`, `api/search.py`) is wired and exercised by tests. The Streamlit shell (`ui/app.py`) exposes five pages; a sixth alerts-management page (`ui/alerts.py`) is implemented but not registered in navigation.

The dominant defect cluster is **inconsistent SQLite manager PK handling**: several UI and chain paths still hardcode `managers.manager_id` while `scripts/seed_managers.py` creates SQLite databases with `managers.id` as the primary key. Upload (`ui/upload.py`), dashboard news (`ui/dashboard.py:load_news_stream`), activism API, and universal search already use `resolve_manager_id_column()` or equivalent — but dashboard manager loading, daily report joins, all-managers QC summary, and RAG entity extraction do not. Production Postgres and the WASM demo bundle (`scripts/build_wasm_demo.py`, which uses `manager_id`) are unaffected; **local SQLite dev after `seed_managers` is the primary blast radius**.

**Verified novel findings:** 6  
**Duplicates / already tracked:** partial overlap with closed #1648/#1649 (upload/alerts-ui selector) and open #1664 (dashboard `load_news_stream` test slice only) — findings below are distinct call sites.  
**Confidence:** High on navigation and SQLite dialect gaps (reproduced offline). Medium on RAG impact severity (catalog fails silently; existing tests only cover `manager_id` schema).

## Production reachability

| Surface | Entry | Reachability |
|--------|-------|--------------|
| REST API | `api/chat.py` (`FastAPI` app) | Docker Compose / `uvicorn`; routers for managers, alerts, signals, activism, search included at `api/chat.py:48-54` |
| Alerts API | `api/alerts.py` | Mounted on main app; UI and ETL call `/api/alerts/*` |
| Streamlit UI | `ui/app.py` via `mgrdb-app` | `pyproject.toml:38`, `ui/launch.py` |
| Alerts UI page | `ui/alerts.py` | **Not reachable** from `ui/app.py` navigation (see F1) |
| WASM demo | `web/wasm_app.py` | Offline; excludes Research/Alerts by design (`tests/test_wasm_demo_build.py:68-78`) |
| RAG / chat chains | `api/chat.py` → `chains/*` | `/api/chat` and Research page; RAG catalog loaded per request |

## Packaging / dependencies (`pyproject.toml`)

- Python `>=3.12`; core stack: FastAPI, Streamlit, LangChain 1.2.x, psycopg, Prefect, edgartools pin `>=5.44,<5.45`.
- Console entry `mgrdb-app` correctly points at `ui.launch:main`.
- No scope issues found in dependency pins for audited surfaces.

## Wiring observations (non-bugs)

- **Alerts engine ↔ API:** `alerts/engine.py` condition keys align with `ui/alerts.py` rule builder (empty `{}` for unfiltered event types is intentional; comment at `ui/alerts.py:198-206`).
- **Offline signals:** `api/signals.py` sets `UI_OFFLINE=1` when FastAPI missing — enables Streamlit imports in WASM build (`tests/test_wasm_demo_build.py:120-135`).
- **Evidence schema drift:** `chains/evidence.py` still omits contract fields (`schema_version`, `fact_ref`, `evidence_id`) — known dossier gap, not re-filed here.
- **Duplication:** `api/search.py:_sqlite_manager_name_map` (lines 101-109) implements the correct id/`manager_id` fallback that several UI modules lack.

---

## Findings

### F1 — Alerts management UI is implemented but not in app navigation

| Field | Value |
|-------|-------|
| **Severity** | P1 / MAJOR |
| **Evidence** | `ui/app.py:9-19` imports and registers Dashboard, Daily Report, Search, Upload, Research only — no `ui.alerts`. `ui/alerts.py:462-476` defines a complete `main()` (rule builder, inbox, stats) behind `require_login()`. |
| **Impact** | Analysts see an “Alerts” badge on the dashboard sidebar (`ui/dashboard.py:1206-1218`) but cannot open rule management or the alert inbox without manually running `ui/alerts.py` or knowing a non-existent route. REST API (`api/alerts.py`) works; operator UI is dead on arrival. |
| **Reachability** | All `mgrdb-app` deployments. |
| **Dedup** | #710 (closed) shipped alerts UI; no open issue for missing nav registration. |
| **Repro** | `python -c "import ui.app; assert 'alerts' not in [p.url_path for p in ui.app._build_pages()]"` from clone (or inspect `ui/app.py`). |
| **Fix direction** | Add `st.Page(alerts.main, title="Alerts", url_path="alerts", ...)` to `_build_pages()` and import `ui.alerts`. |

**Adversarial check:** WASM demo intentionally omits Alerts (`web/wasm_app.py`, `tests/test_wasm_demo_build.py`) — that is by design, not a counterexample for production UI.

---

### F2 — `dashboard.load_managers()` returns empty list on `managers.id` SQLite schemas

| Field | Value |
|-------|-------|
| **Severity** | P2 / MINOR |
| **Evidence** | `ui/dashboard.py:363-368` hardcodes `SELECT manager_id, name FROM managers`; on failure returns empty DataFrame (`:367-368`). Contrast `ui/upload.py:43-44` which uses `resolve_manager_id_column(conn)`. `scripts/seed_managers.py:47-49` creates `managers.id INTEGER PRIMARY KEY`. |
| **Impact** | Manager selector on Dashboard shows only “All Managers”; per-manager portfolio/activism/signals tabs unusable on seed_managers-style SQLite DBs. |
| **Reachability** | Local SQLite dev (`seed_managers`, default seed path). Postgres + WASM demo (`manager_id` schema) OK. |
| **Dedup** | Closed #1649 fixed upload; closed #1648 fixed alerts-ui API loader; open #1664 covers `load_news_stream` only — not this function. |
| **Repro** | `artifacts/.../repros/test_audit_repros.py::test_dashboard_load_managers_empty_on_id_schema` (passes). |
| **Fix direction** | Mirror `resolve_manager_id_column` + alias selected column as `manager_id` in the DataFrame. |

---

### F3 — `daily_report.load_diffs()` fallback JOIN crashes on `managers.id` SQLite

| Field | Value |
|-------|-------|
| **Severity** | P2 / MINOR |
| **Evidence** | `ui/daily_report.py:29-34` fallback query `JOIN managers m ON m.manager_id = d.manager_id` when materialized view `mv_daily_report` is absent (typical in dev SQLite). |
| **Impact** | Daily Report page raises `OperationalError: no such column: m.manager_id` instead of showing diffs. |
| **Reachability** | SQLite without `mv_daily_report` (dev / test fixtures). |
| **Dedup** | `tests/test_daily_report_views.py` exercises `manager_id` schema only. |
| **Repro** | `test_audit_repros.py::test_daily_report_fallback_join_fails_on_id_schema` (passes). |
| **Fix direction** | Use `resolve_manager_id_column(conn)` in the JOIN, same pattern as `ui/dashboard.py:136-147`. |

---

### F4 — `daily_report.load_news()` silently returns no rows on `managers.id` SQLite

| Field | Value |
|-------|-------|
| **Severity** | P2 / MINOR |
| **Evidence** | `ui/daily_report.py:54-58` (SQLite) and `:67-68` (Postgres) `LEFT JOIN managers m ON m.manager_id = n.manager_id`; broad `except Exception` at `:74-85` swallows the schema error. |
| **Impact** | Daily Report news section shows empty state despite `news_items` rows present. |
| **Reachability** | SQLite dev DBs with `managers.id`. |
| **Repro** | Seed id-schema DB with news row; `load_news('2026-03-15')` returns 0 rows (verified in audit session). |
| **Fix direction** | Dialect-aware manager join; avoid swallowing schema errors that indicate misconfiguration. |

---

### F5 — `load_all_managers_summary()` QC warnings never populate on `managers.id` SQLite

| Field | Value |
|-------|-------|
| **Severity** | P2 / MINOR |
| **Evidence** | `ui/dashboard.py:1023-1036` loads managers via hardcoded `SELECT manager_id, name`; loop at `:1034-1087` never runs when `managers_df` is empty. Outer `except Exception: pass` at `:1088-1089` hides failures. Totals at `:979-994` still work (COUNT queries). |
| **Impact** | “All Managers Summary” shows counts but “Managers with QC Warnings” is always empty/stale on id-schema SQLite even when filings exist. |
| **Reachability** | Dashboard → “All Managers” view (`selected_manager_id is None`). |
| **Repro** | `test_audit_repros.py::test_all_managers_summary_qc_warnings_missing_on_id_schema` (passes). |
| **Fix direction** | Resolve manager PK column once; normalize to `manager_id` in the DataFrame before QC loop. |

---

### F6 — `RAGSearchChain._manager_catalog()` hardcodes `manager_id`; entity extraction fails silently

| Field | Value |
|-------|-------|
| **Severity** | P2 / MINOR |
| **Evidence** | `chains/rag_search.py:87-98` runs `SELECT manager_id, name, cik FROM managers` and returns `[]` on any exception. `_entity_extraction` (`:114-119`) depends on catalog; `_structured_search` (`:197`) repeats hardcoded `manager_id IN (...)`. |
| **Impact** | Research chat / RAG cannot match manager names from the catalog on id-schema SQLite; questions like “What does Elliott hold?” miss structured holdings/filings context. Chat API `_manager_ids_for_name` (`api/chat.py:586-602`) **does** use `_manager_id_column` — inconsistency across chains. |
| **Reachability** | `/api/chat` with `chain=rag_search` or auto-routed RAG on SQLite dev. |
| **Dedup** | `tests/test_rag_search_chain.py` builds `manager_id` schema only (`:31`). |
| **Repro** | Code path + silent empty catalog; run `tests/test_rag_search_chain.py::test_entity_extraction_matches_manager_ids` (passes on `manager_id` schema — invert schema to fail). |
| **Fix direction** | Use `resolve_manager_id_column` / `manager_id_column` from `adapters.base`; add id-schema regression beside `test_dashboard_news_schema.py`. |

---

## Intentional / out of scope (verified not filed)

| Item | Rationale |
|------|-----------|
| WASM demo lacks Research/Alerts pages | Tested intentional (`tests/test_wasm_demo_build.py:68-78`) |
| Foreign adapter `unsupported` stubs | Documented design per dossier §8 |
| Evidence object schema divergence | Known contract gap; not API wiring bug |
| `DELETE /managers/{id}` FK cascade failure | Documented (# dossier §7); `api/managers.py` out of focused UI/API seam review depth |
| Rate limiting only on chat writes | Resolved #1145; current behavior matches docs |

## Test gate notes

Offline reproducers:  
`artifacts/audits/Manager-Database-2026-09-14-assets/repros/test_audit_repros.py`  
(3/5 auto-tests pass; RAG test blocked by import order when run outside `tests/` package — use clone test suite for RAG: `pytest tests/test_rag_search_chain.py`)

Suggested regression gate for fixes:  
`pytest tests/test_dashboard.py tests/test_daily_report.py tests/test_rag_search_chain.py tests/test_ui_navigation.py tests/test_ui_alerts.py -q`

## Prioritized table

| ID | Severity | Area | Summary |
|----|----------|------|---------|
| F1 | P1 | `ui/app.py` | Alerts page not in navigation |
| F2 | P2 | `ui/dashboard.py` | `load_managers` empty on id-schema SQLite |
| F3 | P2 | `ui/daily_report.py` | `load_diffs` fallback JOIN crash |
| F4 | P2 | `ui/daily_report.py` | `load_news` silent empty |
| F5 | P2 | `ui/dashboard.py` | QC warnings never computed on id-schema |
| F6 | P2 | `chains/rag_search.py` | RAG catalog ignores `managers.id` |
