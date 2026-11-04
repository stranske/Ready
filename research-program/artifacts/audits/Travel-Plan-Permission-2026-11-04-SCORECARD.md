# Scorecard — stranske/Travel-Plan-Permission — 2026-11-04 — tip 24693f79196fd741040b9428e26de43c94025f5a

Scorecard: 8 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 9; journey: passes; surfaces unscored 0; closed-still-broken 0.
UX gate: unmeasured — TestClient and pytest probes only; no browser panel this run.

## 1. Purpose and core functions

| id | core function | entry point | source |
|---|---|---|---|
| PP1 | policy evaluation with reasons | `/api/planner/proposals` → evaluation-result | `docs/PRODUCT_CONTRACT.md` |
| PP2 | traveller draft → submit | portal draft/review/submit | contract |
| PP3 | exception + admin terminal decision | portal exception routes | contract |
| PP4 | overdue exception escalation | `/portal/admin` | contract |
| PP5 | manager review decision | manager-review routes | contract |
| PP6 | corrected answers via new draft | portal draft after changes_requested | contract (known gap) |
| PP7 | policy-gated artifact download | review artifact routes | contract |
| PP8 | policy snapshot caps | `/api/planner/policy-snapshot` | contract |
| PP9 | expense review + CSV/XLSX export | `/portal/expenses/*` | contract (#1724) |

## 2. Live exercise results

| id | score | how exercised | varying-input check |
|---|---|---|---|
| PP1 | WORKS | `test_submission_status_and_evaluation_routes_round_trip` | compliant vs blocking proposal paths diverge |
| PP2 | WORKS | `test_portal_generates_review_artifacts_and_submission`, blocking submit test | blocking vs compliant submit |
| PP3 | WORKS | `test_exception_decision_is_terminal` | terminal vs conflicting decision |
| PP4 | WORKS | `test_exception_listing_escalates_and_persists` | overdue vs ordinary exception |
| PP5 | WORKS | `test_manager_review_decision_updates_status_and_history` | approve vs request_changes |
| PP6 | PARTIAL | `test_manager_review_resubmit_refreshes_trip_plan` | resubmit refreshes plan; no in-place draft edit (contract gap) |
| PP7 | WORKS | portal artifact download tests | blocked vs permitted downloads |
| PP8 | WORKS | `test_snapshot_route_returns_planner_contract` | snapshot carries configured requirements |
| PP9 | WORKS | `test_expense_portal_generates_exports_and_policy_warning`, linkage block tests | approved vs unapproved linkage |

## 3. Interior surfaces scored (clears K=12 debt)

| surface | score | evidence |
|---|---|---|
| `fill-spreadsheet` CLI | WORKS | live runs on `sample_trip_plan_minimal.json` + `washington_dc_business_trip.json`; `tests/python/test_cli.py` |
| `tpp-audit-export` / `tpp-audit-prune` | WORKS | `tests/python/test_audit.py` (76 passed) |
| `orchestration-demo` / LangGraph path | WORKS | orchestration pytest selection (31 passed) |
| `tpp-planner-smoke` | WORKS | `tests/python/test_planner_smoke.py` |
| `tpp-cross-repo-smoke` harness | WORKS | `tests/python/test_cross_repo_smoke.py` (37 passed) |
| portal handoff routes | WORKS | `tests/python/test_portal_handoff.py` |
| `/portal/demo` | WORKS (demo mode) | `http_service.py:1659-1663` returns 404 off demo; 200 with `TPP_DEMO_MODE=1` (Render path) |
| `/healthz` | WORKS | TestClient 200 `{"status":"ok"}` |
| `/readyz` | PARTIAL | TestClient 503 without full planner auth/readiness env (expected pre-config) |
| ERP GL write-back | PARTIAL | `docs/accounting-integration.md` export-only; no ledger post |
| `run-contract/v1` emitter | NOT EXERCISED | documented only; no `run.json` in `src/` |
| security-model REST table | BROKEN (doc) | `docs/security-model.md:17-27` lists routes that 404 on tip → filed #1727 |

## 4. Closed-issue re-probes

- #1669 foreign overwrite: `test_foreign_overwrite_cannot_replace_bound_execution` passes — fix holds.
- #1720/#1721/#1724 doc contract fixes closed; operator doc guard tests pass.

## 5. Environment

Tip `24693f7`; scorecard keyword gate 34 passed; CI main green (`41779988988` deps sync). Local Python 3.12 env runs tests; package requires `>=3.13` per `pyproject.toml:7` (CI authoritative).
