# Repository Audit Report: Manager-Database

- **Date**: 2026-09-10
- **Base Commit**: `5681c1b8ed41911599a19014147300637a9c3b5f` (tip of `origin/main`)
- **Auditor**: Gemini via Antigravity (`repo-audit` skill)
- **Scope**: Full repository audit across 8 dimensions per `docs/AGENT_ISSUE_FORMAT.md`
- **Initial Open Issue Supply**: 0 open implementation issues (triggered Track D refill)
- **Filed Issues**: 7 verified work orders (#1647–#1653)

---

## Executive Summary

A comprehensive, adversarial repository audit was conducted on `stranske/Manager-Database` at commit `5681c1b8ed41911599a19014147300637a9c3b5f`. Prior supply of implementation-ready issues was at 0, triggering Track D refill. Across all 8 audit dimensions, 7 reproducible defects were verified on the live codebase, staged as strictly conforming `AGENT_ISSUE_FORMAT` work orders with 0 linter errors/advisories, filed to GitHub, and indexed in the persistent audit ledger and measurement intake logs.

---

## Dimension Assessment Summary

| Dimension | Assessment & Findings |
|---|---|
| **1. Code Quality and Correctness** | **Defects Identified**: `ui/dashboard.py:50-55` SQL column error (`load_delta` references non-existent column `holdings.filed`); `adapters/prices.py:231-245` cache bypass for weekend/holiday dates causing redundant HTTP requests. |
| **2. Duplication and Consolidation** | **Defects Identified**: Missing centralized column dialect resolution (`resolve_manager_id_column`) in `ui/upload.py:43` and `api/activism.py:195, 255, 365, 432, 515`. |
| **3. Functionality and Wiring** | **Defects Identified**: `ui/alerts.py:75-80` manager dropdown broken due to response key mismatch (`item.get("id")` vs API `manager_id`); `alerts/models.py:33-35` / `alerts/engine.py:100-105` count threshold `similar_manager_count_gte` treated as float rather than validated integer. |
| **4. Design and UX** | **Defects Identified**: Dashboard historical filing trend crashes on load (`OperationalError`); Alerts UI displays an empty manager dropdown selector. |
| **5. Approach vs Public Field** | **Defects Identified**: `etl/manager_similarity_flow.py:27-47` `ensure_manager_similarity_table()` omits PostgreSQL DDL branch, deviating from production pipeline schema idempotency standards. |
| **6. Missed Opportunities** | **Identified**: Price caching missing date-level negative caching for market holidays and weekend dates when historical data is requested. |
| **7. Tools Worth Integrating** | **Identified**: Automated dialect-matrix unit tests verifying all UI and API query handlers against both SQLite and PostgreSQL schemas. |
| **8. Local Skills, Automations, and Human Touchpoints** | **Verified**: GitHub Actions `agents-issue-format-guard.yml` and keepalive intake flows operational. |

---

## Adversarially Verified Defect Backlog

### Finding 1 (P1): `ui/dashboard.py` — `load_delta()` crashes on non-existent `filed` column
- **Issue**: [#1647](https://github.com/stranske/Manager-Database/issues/1647)
- **Path & Lines**: `ui/dashboard.py:50-55`, called at `ui/dashboard.py:1184`
- **Root Cause**: `load_delta()` executes `SELECT filed as date, COUNT(*) AS filings FROM holdings GROUP BY filed ORDER BY filed`. In the `holdings` schema, the filing date column is `filed_date` (or bitemporal `knowledge_time`), not `filed`.
- **Runtime Impact**: Expanding or rendering the historical filing trend in Streamlit triggers an unhandled `sqlite3.OperationalError: no such column: filed` (or PostgreSQL equivalent), crashing the UI section.
- **Resolution**: Query `filings` table using `filed_date` (`SELECT filed_date AS date, COUNT(*) AS filings FROM filings GROUP BY filed_date ORDER BY filed_date`), or query `holdings` with `filed_date`.

### Finding 2 (P2): `ui/alerts.py` — Manager selector empty list caused by `manager_id` key mismatch
- **Issue**: [#1648](https://github.com/stranske/Manager-Database/issues/1648)
- **Path & Lines**: `ui/alerts.py:75-80`
- **Root Cause**: `_load_managers()` filters on `if item.get("id") is not None and item.get("name")`. However, the `/api/managers` endpoint returns `ManagerResponse` instances serialized with field `manager_id`, not `id`.
- **Runtime Impact**: `item.get("id")` is always `None`, resulting in `_load_managers()` returning an empty list `[]`, stranding the manager selection widget in the Alerts UI.
- **Resolution**: Access `item.get("manager_id")` with fallback to `item.get("id")`.

### Finding 3 (P2): `ui/upload.py` — Manager loader `manager_id` column dialect error on SQLite
- **Issue**: [#1649](https://github.com/stranske/Manager-Database/issues/1649)
- **Path & Lines**: `ui/upload.py:43-44`
- **Root Cause**: `_load_managers()` runs raw SQL `SELECT manager_id, name FROM managers ORDER BY name ASC` without using `resolve_manager_id_column(conn)`.
- **Runtime Impact**: On SQLite database configurations (where `managers` primary key is `id`), the query fails with `OperationalError: no such column: manager_id` and logs an exception, returning an empty list.
- **Resolution**: Use `resolve_manager_id_column(conn)` to resolve the primary key column dynamically.

### Finding 4 (P2): `alerts/models.py` & `alerts/engine.py` — `similar_manager_count_gte` integer validation
- **Issue**: [#1650](https://github.com/stranske/Manager-Database/issues/1650)
- **Path & Lines**: `alerts/models.py:33-35`, `alerts/engine.py:100-105`
- **Root Cause**: While commit `#1642` enforced positive integer validation for `news_count_gt` and `manager_count_gte`, `similar_manager_count_gte` was left in `_NUMERIC_CONDITION_BOUNDS` as float `(1.0, None)` and evaluated in `alerts/engine.py` using `_as_float()`.
- **Runtime Impact**: Float threshold values like `1.5` pass rule validation for discrete manager count conditions, leading to invalid rule configurations.
- **Resolution**: Move `similar_manager_count_gte` to `_INTEGER_CONDITION_KEYS` and parse using `parse_count_threshold()`.

### Finding 5 (P2): `api/activism.py` — SQLite column error in activism queries for `managers` table join
- **Issue**: [#1651](https://github.com/stranske/Manager-Database/issues/1651)
- **Path & Lines**: `api/activism.py:195, 255, 365, 432, 515`
- **Root Cause**: Query functions `query_activism_filings`, `query_activism_events`, `query_activism_ranking`, `query_activism_campaigns`, and `query_manager_activism_profile` hardcode `LEFT JOIN managers m ON m.manager_id = ...`.
- **Runtime Impact**: Crashes on SQLite databases with `OperationalError: no such column: m.manager_id`.
- **Resolution**: Resolve manager ID column dynamically via `resolve_manager_id_column(conn)`.

### Finding 6 (P2): `adapters/prices.py` — Weekend/holiday cache bypass causes redundant HTTP requests
- **Issue**: [#1652](https://github.com/stranske/Manager-Database/issues/1652)
- **Path & Lines**: `adapters/prices.py:231-245`
- **Root Cause**: In `close_on_or_before(symbol, on)`, `needs_refresh = not window or max(window) < on`. For non-trading dates (weekends, holidays), `max(window) < on` is True, triggering `self._fetch()`. Because `window` is non-empty, `(symbol, on)` is not added to `self._missing`.
- **Runtime Impact**: Every subsequent query for a weekend/holiday date triggers repeated network requests to external price fetchers instead of using the cached Friday close.
- **Resolution**: Mark `(symbol, on)` as evaluated or record maximum probed date in cache metadata.

### Finding 7 (P2): `etl/manager_similarity_flow.py` — Schema check in `ensure_manager_similarity_table` omits PostgreSQL
- **Issue**: [#1653](https://github.com/stranske/Manager-Database/issues/1653)
- **Path & Lines**: `etl/manager_similarity_flow.py:27-47`
- **Root Cause**: `ensure_manager_similarity_table(conn)` only contains an `if isinstance(conn, sqlite3.Connection):` branch and does nothing for PostgreSQL connections.
- **Runtime Impact**: In production PostgreSQL environments, `compute_manager_similarity` fails with table/column missing errors if migrations have not been applied.
- **Resolution**: Add PostgreSQL DDL / `CREATE TABLE IF NOT EXISTS` branch with `manager_id_a BIGINT REFERENCES managers(manager_id)` foreign keys.

---

## Filed Issues Summary Table

| # | Priority | Title | Component / Path |
|---|---|---|---|
| [#1647](https://github.com/stranske/Manager-Database/issues/1647) | P1 | `fix(dashboard): resolve crash in load_delta on missing filed column` | `ui/dashboard.py:50-55, 1184` |
| [#1648](https://github.com/stranske/Manager-Database/issues/1648) | P2 | `fix(alerts-ui): fix manager selector empty list caused by manager_id key mismatch` | `ui/alerts.py:75-80` |
| [#1649](https://github.com/stranske/Manager-Database/issues/1649) | P2 | `fix(upload-ui): resolve manager_id column dialect error in upload manager loader` | `ui/upload.py:43-44` |
| [#1650](https://github.com/stranske/Manager-Database/issues/1650) | P2 | `fix(alerts): enforce integer validation for similar_manager_count_gte rule condition` | `alerts/models.py:33-35`, `alerts/engine.py:100-105` |
| [#1651](https://github.com/stranske/Manager-Database/issues/1651) | P2 | `fix(api-activism): resolve SQLite column error for managers table join in activism queries` | `api/activism.py:195, 255, 365, 432, 515` |
| [#1652](https://github.com/stranske/Manager-Database/issues/1652) | P2 | `fix(prices): eliminate redundant HTTP requests for weekend and holiday dates in PriceAdapter` | `adapters/prices.py:231-245` |
| [#1653](https://github.com/stranske/Manager-Database/issues/1653) | P2 | `fix(etl): implement Postgres schema check in ensure_manager_similarity_table` | `etl/manager_similarity_flow.py:27-47` |

---

## Verification & Compliance Checklist

- [x] **Path Citations**: All paths cited relative to target repo root (`ui/dashboard.py`, `ui/alerts.py`, etc.). No `clones/...` references.
- [x] **Adversarial Verification**: Each finding verified by opening exact lines and tracing execution in `clones/Manager-Database` @ `5681c1b`.
- [x] **Format Guard Conformance**: Staged issue bodies validated with `issue_format.py` (7/7 PASS, 0 errors, 0 advisories).
- [x] **Intake Logging**: Appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- [x] **Durable Audit Storage**: Staged under `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Manager-Database/` and indexed in `AUDIT_LEDGER.md`.

