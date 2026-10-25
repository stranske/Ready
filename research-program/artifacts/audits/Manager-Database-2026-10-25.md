Scorecard: 8 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0.

# stranske/Manager-Database audit — 2026-10-25 (Track D refill)

Tip audited: `5605c75711c03cdb2a0cacd15ec9a193d7cbb45c` (`main`, includes #1853 activism lifecycle wiring). Scope: first-party application code; excluded Workflows-synced infra except consumer boundaries.

## Run summary

This round’s trigger was coverage debt: **surfaces unscored 19** unchanged on the canonical 2026-10-24 scorecard. Those paths were exercised live via FastAPI ASGI tests (not static OpenAPI inventory), with varied inputs on filters, dates, managers, and alert matching. All eight `docs/PRODUCT_CONTRACT.md` core functions remain **WORKS**; **K is now 0**.

Focused route and product suites passed on tip, including: `tests/test_manager_api.py`, `tests/test_manager_bulk_api.py`, `tests/test_manager_universe_api.py`, `tests/test_activism_api.py` (compat/materialized active-campaign tests), `tests/test_signals_api.py`, `tests/test_alerts_api.py`, `tests/test_data_api.py`, `tests/test_rag_search_chain.py` (fleet evidence schema + campaign snapshot), `tests/test_diff_holdings.py`, `tests/test_chat_api.py`, `tests/test_search_api.py`, `tests/test_ui_dashboard.py`, `tests/test_ui_alerts.py`, and `tests/test_data_quality.py` (`test_data_quality_flow_delivers_etl_failure`).

No new finding survived adversarial verification and open/recently-closed dedup. Tracked open work remains appropriate on existing issues (#1783, #1786, #1791, coverage epics, etc.).

## Refutations (open issues whose claims no longer hold on tip)

REFUTED: https://github.com/stranske/Manager-Database/issues/1790 — `etl/data_quality_flow.py` calls `evaluate_daily_quality` and `test_data_quality_flow_delivers_etl_failure` passes on `5605c75`.

REFUTED: https://github.com/stranske/Manager-Database/issues/1784 — `query_active_campaigns` reads materialized `activism_campaigns` via `query_activism_campaigns` (`api/activism.py:342-367`); `test_compat_reads_passive_materialized_status_and_preserves_identity` and `test_campaign_snapshot_reaches_prompt_and_citations_with_scope` pass on `5605c75` (delivered with #1853).

## Delivery consequence

**0 issues filed.** #1848 and #1849 are closed (evidence-object alignment and run-contract emitter). No intake log append.

## Continuity

Canonical scorecard: `Code/Audits/Manager-Database/2026-10-25-SCORECARD.md`. Surface inventory: `Code/Audits/Manager-Database/2026-10-25-surface-inventory.txt`.

## Limits

No browser UX panel this round; headline API/operator coverage only. Full-suite CI not re-run locally; `main` scheduled keepalive workflows were green at audit time.
