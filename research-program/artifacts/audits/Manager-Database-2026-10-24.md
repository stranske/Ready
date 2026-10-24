Scorecard: 8 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

# stranske/Manager-Database audit — 2026-10-24

Tip audited: `bafe7d37ea774d8edcca21c2599222c3a2757994` (`main`). Scope: first-party application code and product surfaces; excluded Workflows-synced tool/script material except consumer boundaries.

## Delivery outcome

No new issue was filed in this pass. Same-day findings were already live:

- #1848 merged as [PR #1850](https://github.com/stranske/Manager-Database/pull/1850). Its current-tip schema regression, `tests/test_rag_search_chain.py::test_evidence_objects_validate_against_fleet_schema`, passed (two parametrized cases), proving the contract change in `chains/evidence.py` and `chains/rag_search.py`.
- #1849 already has an active clean PR #1851. Its hosted `emit-reference-run`, Backplane conformance, lint/format, mypy, and Python 3.12/3.13 checks are successful. A new issue would duplicate active delivery.

REFUTED: https://github.com/stranske/Manager-Database/issues/1790 — its reproduction no longer holds: `etl/data_quality_flow.py:74` calls `evaluate_daily_quality`, and the selected data-quality flow tests pass, including `test_data_quality_flow_delivers_etl_failure`.

## Product and surface evidence

The core contract in `docs/PRODUCT_CONTRACT.md` defines MDB-1 through MDB-8. The prior same-day scorecard reported 19 unscored REST paths. This pass drove those API groups through the FastAPI ASGI entry point, rather than preserving a static-only inventory result.

| Group | Verdict | Runtime evidence |
| --- | --- | --- |
| MDB-1/2: managers, filtering, tags, stats, bulk/universe import, similarity | WORKS | `tests/test_manager_api.py`, `tests/test_manager_bulk_api.py`, `tests/test_manager_universe_api.py`, `tests/test_manager_similarity_flow.py`, and `tests/test_manager_similarity_boundaries.py` passed. |
| MDB-3: holdings, signals, activism/campaign detail | WORKS | `tests/test_activism_api.py` and `tests/test_signals_api.py` passed, including varied filters/dates and all listed activism, attribution, crowded, contrarian, and conviction routes. |
| MDB-4/5: search and grounded research | WORKS | `tests/test_rag_search_chain.py` and the #1850 evidence-object contract regression passed. |
| MDB-6: data/dashboard API | WORKS | `tests/test_data_api.py` passed against `/api/data`; no dashboard product-code delta invalidated same-day evidence. |
| MDB-7: uploads | WORKS | No target-code delta since the same-day focused upload exercise; its evidence remains applicable. |
| MDB-8: alert rules/history/acknowledgements | WORKS | `tests/test_alerts_api.py`, `tests/test_ui_alerts.py`, and `tests/test_data_quality.py -k 'data_quality_flow or integration_wrapper'` passed. |

The API-level journey passes: create/query manager, ingest/query associated data, search/research, and review alert/dashboard surfaces. The ASGI tests vary manager filters, campaign dates/limits, signal dates/managers, and alert matching/acknowledgement; no constant-output result was observed.

## Surface reconciliation and risks

The formerly unscored groups—activism, alert history/count/acknowledgement, manager stats/similarity/tags/bulk/universe, signals, and `/api/data`—are covered by the passing route suites above. Inventory groups overlap methods, hence their apparent category total exceeds 19. Coverage debt is therefore reduced from 19 to zero.

No fresh first-party defect cleared adversarial verification and open/recently-closed issue dedup. In particular, the #1790 wiring premise is false on the current tip, and #1848/#1849 are respectively merged and actively delivered. Existing #1783/#1784/#1786/#1849 remain the appropriate trackers for their distinct work.

This is not a browser-UX verdict: no browser panel was run. The new coverage claim is for API/operator routes driven through ASGI. Environment warnings (FastAPI `on_event` deprecation, SciPy/NumPy compatibility, and pandas optional accelerators) were observed but not filed because no user-facing failure reproduced.

All commands used `/opt/anaconda3/bin/python3`. The canonical `Code/Audits` ledger was read for continuity but is outside this unit's write boundary; this OUT file and its checkpoint are the durable unit record. No intake measurement append is due because this pass filed no issue.
