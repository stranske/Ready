# Repository Audit Report: Manager-Database

- **Date**: 2026-09-10
- **Base Commit**: `5681c1b8ed41911599a19014147300637a9c3b5f` (tip of `origin/main`)
- **Auditor**: Gemini via Antigravity (`repo-audit` skill)
- **Scope**: Full repository audit across 8 dimensions per `docs/AGENT_ISSUE_FORMAT.md`

## Executive Summary

A comprehensive, adversarial audit of `stranske/Manager-Database` was conducted at commit `5681c1b`. The open implementation issue backlog was at 0 (triggering Track D refill). 7 high-value, reproducible defects were identified, verified on the live codebase, and filed as machine-enforced `AGENT_ISSUE_FORMAT` work orders with 100% pass rates across local issue linters and remote GitHub Actions format guard.

## Dimension Assessment Summary

1. **Code Quality and Correctness**: Found SQL column error in dashboard `load_delta()` (F1) and redundant network fetches on non-trading dates in `PriceAdapter` (F6).
2. **Duplication and Consolidation**: Dialect column resolution helpers (`resolve_manager_id_column`) were omitted in `ui/upload.py` (F3) and `api/activism.py` (F5).
3. **Functionality and Wiring**: Alert UI manager selector completely disconnected due to response field key mismatch (`manager_id` vs `id`) in `ui/alerts.py` (F2); alert rule models accepted non-integer floats for manager counts (F4).
4. **Design and UX**: Dashboard trend expander crashes on open; Alerts UI displays empty dropdown for manager selection.
5. **Approach vs Public Field**: ETL similarity table ensure lacked PostgreSQL support standard in production pipelines (F7).
6. **Missed Opportunities**: Price caching lacked evaluation tracking for market holidays/weekends.
7. **Tools Worth Integrating**: Pre-submit dialect portability tests across all UI query handlers.
8. **Local Skills, Automations, and Human Touchpoints**: Format guards and auto-pilot intake verified operational and green.

## Filed Issues Backlog

| # | Priority | Title | Component / Path |
|---|---|---|---|
| [#1647](https://github.com/stranske/Manager-Database/issues/1647) | P1 | `fix(dashboard): resolve crash in load_delta on missing filed column` | `ui/dashboard.py:50-55, 1184` |
| [#1648](https://github.com/stranske/Manager-Database/issues/1648) | P2 | `fix(alerts-ui): fix manager selector empty list caused by manager_id key mismatch` | `ui/alerts.py:75-80` |
| [#1649](https://github.com/stranske/Manager-Database/issues/1649) | P2 | `fix(upload-ui): resolve manager_id column dialect error in upload manager loader` | `ui/upload.py:43-44` |
| [#1650](https://github.com/stranske/Manager-Database/issues/1650) | P2 | `fix(alerts): enforce integer validation for similar_manager_count_gte rule condition` | `alerts/models.py:33-35`, `alerts/engine.py:100-105` |
| [#1651](https://github.com/stranske/Manager-Database/issues/1651) | P2 | `fix(api-activism): resolve SQLite column error for managers table join in activism queries` | `api/activism.py:195, 255, 365, 432, 515` |
| [#1652](https://github.com/stranske/Manager-Database/issues/1652) | P2 | `fix(prices): eliminate redundant HTTP requests for weekend and holiday dates in PriceAdapter` | `adapters/prices.py:231-245` |
| [#1653](https://github.com/stranske/Manager-Database/issues/1653) | P2 | `fix(etl): implement Postgres schema check in ensure_manager_similarity_table` | `etl/manager_similarity_flow.py:27-47` |
