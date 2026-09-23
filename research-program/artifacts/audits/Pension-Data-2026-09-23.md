Scorecard: 2 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 3; journey: passes; surfaces unscored 0; closed-still-broken 0.

# Pension-Data Track D audit — 2026-09-23

Audited remote `main` at `33a29aa` after the merge of PR #912. The run used the product contract, current surface inventory, direct focused test execution, and current GitHub issue/Actions state. Two verified, non-duplicate issues were filed: #914 for F2's pilot-staging-to-served-API gap, and #915 for stale run-contract documentation.

## Product scorecard

| Core function | Result | Evidence |
| --- | --- | --- |
| F1 — run a PDF pilot and receive staged/published artifacts | WORKS | `tests/ops/test_one_pdf_pilot_cli.py` passed (8 tests). |
| F2 — run plan analytics keyed to the requested entity | PARTIAL | The library tests pass, but the served routes still feed `_fixture_funding_trend_inputs()` and `_fixture_metric_history_rows()` at `src/pension_data/api/app.py:65-101,164-212`, rather than pilot/staging persistence. The live pilot plus TestClient reproduction is filed as #914. |
| F3 — build a real-data workspace bundle with provenance | WORKS | The just-merged builder loads pilot manifest/staging rows and rejects fixture origin at `scripts/web/build_workspace_bundle.py:87-112`; `tests/export/test_workspace_bundle.py` and `tests/web/test_build_workspace_bundle.py` passed in the repository working directory. |

The primary journey now completes through generated workspace-bundle emission. The focused suite passed 37/37: one-PDF CLI, saved-view, metric-history, export, and workspace-build tests. A first invocation from the automation root made two path-relative web assertions fail; rerunning from the repository root passed, so that was an audit harness CWD error rather than a product defect.

## Surface inventory and verification

The contract's three core functions cover the one-PDF CLI, analytics library/API, and workspace build/serve flow. The additional FastAPI paths (`/health`, `/config`, LLM-disabled endpoints) are support or intentionally disabled surfaces, not new core functions. Recent PR #912 closes #883 and supplies F3's previously missing generated bundle path. The two audit issues are #914 (P1, hard-coded served analytics) and #915 (P2, stale emitter claim).

Closed issue #883's required generated-bundle test was re-executed through `tests/export/test_workspace_bundle.py` and the web builder tests and is refuted as still-open: current tip generates and validates `data_origin: generated`. The fixture-backed F2 service behavior remains documented explicitly in `docs/PRODUCT_CONTRACT.md` and prior issue history; it was therefore not misreported as a new regression.

## Audit disposition

Issues filed: [#914](https://github.com/stranske/Pension-Data/issues/914) and [#915](https://github.com/stranske/Pension-Data/issues/915). Current Actions show successful Gate and agent follow-up runs for the #884 delivery. The audit's first direct focused suite passed 37/37; the delegated pass independently reproduced F2 before filing #914.
