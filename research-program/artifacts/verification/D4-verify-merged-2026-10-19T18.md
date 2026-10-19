# D4 — verify merged PRs against issue acceptance criteria

Run: 2026-10-19 (36-hour window from ~2026-10-18T06:33:00Z; **20 PRs** verified, oldest merged first among in-window non-chore merges with issue references, not in this unit’s ledger)

## Result

**91** non-chore merges with issue references fell in the window (excluding Orchestrator). This pass audited the **first twenty** by `mergedAt`. No ledger-only belt bookkeeping PRs appeared in the batch. **No `Reproduction:` blocks** on linked issues in this batch; re-run/reopen not required.

| Repo | PR | Issue | Verdict | Unmet criteria / diff evidence | Follow-up filed |
|---|---:|---|---|---|---|
| Workflows | [#4069](https://github.com/stranske/Workflows/pull/4069) | [#4068](https://github.com/stranske/Workflows/issues/4068) | VERIFIED | Substantive `maint71_merge_sync_prs.js` debounce (`canaryRefreshDecision`, `CANARY_REFRESH_DEBOUNCE_MS`, `refresh: skipped …`), promotion drain (`dispatchCanaryPromotion`, `promote: blocked …; drainable …`); workflow/test updates; **78** JS tests documented. Deliberate-break (disabled successful-SHA debounce) in PR body. **Pending (not due):** issue pass-number (≤3 canary / ≥1 promote in 24h after merge+re-enable). | N/A (offload: no GitHub writes) |
| Manager-Mosaic | [#115](https://github.com/stranske/Manager-Mosaic/pull/115) | [#101](https://github.com/stranske/Manager-Mosaic/issues/101) | VERIFIED | Production: `model.py` `FactRecord`/`FactBasis`, provenance through `discrepancy.py`/`thesis.py`; `tests/test_model_validation.py` + evidence under `docs/evidence/issue-101/` including deliberate-break on `model.py`. | N/A |
| Counter_Risk | [#1178](https://github.com/stranske/Counter_Risk/pull/1178) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Squash diff: exactly one line in `.github/workflows/pr-00-gate.yml` removing `labeled` from `pull_request.types` (2 diff lines). Campaign item for WF#4082. | N/A |
| Deliverable-Render | [#101](https://github.com/stranske/Deliverable-Render/pull/101) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix as above. | N/A |
| Doc-Lineage | [#138](https://github.com/stranske/Doc-Lineage/pull/138) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| Fine-Art-Archive | [#832](https://github.com/stranske/Fine-Art-Archive/pull/832) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| Inv-Man-Intake | [#1037](https://github.com/stranske/Inv-Man-Intake/pull/1037) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| Manager-Mosaic | [#116](https://github.com/stranske/Manager-Mosaic/pull/116) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| Pension-Data | [#979](https://github.com/stranske/Pension-Data/pull/979) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| Travel-Plan-Permission | [#1682](https://github.com/stranske/Travel-Plan-Permission/pull/1682) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| Trend_Model_Project | [#6112](https://github.com/stranske/Trend_Model_Project/pull/6112) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| learning-management-system | [#775](https://github.com/stranske/learning-management-system/pull/775) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| trip-planner | [#1921](https://github.com/stranske/trip-planner/pull/1921) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| Manager-Database | [#1824](https://github.com/stranske/Manager-Database/pull/1824) | [#4082](https://github.com/stranske/Workflows/issues/4082) (refs) | VERIFIED | Same one-line Gate trigger fix. | N/A |
| Manager-Mosaic | [#117](https://github.com/stranske/Manager-Mosaic/pull/117) | [#101](https://github.com/stranske/Manager-Mosaic/issues/101) | VERIFIED | Adds ordered `bases` / `evidence_bases` on `DiscrepancyRecord` and `ThesisCheck`, top-level exports in `__init__.py`; `test_result_provenance_accessors_expose_inferred_only_and_mixed_bases`; deliberate-break evidence `docs/evidence/issue-101/model-provenance-accessors-break.txt`. Builds on #115. | N/A |
| Workflows | [#4078](https://github.com/stranske/Workflows/pull/4078) | [#4077](https://github.com/stranske/Workflows/issues/4077) | VERIFIED | Test-only: four new/expanded test modules for `llm_registry`, heartbeat, orchestrator skill, AGENTS freshness; PR documents four break-and-revert RED runs (85 focused pytest). No production edits. | N/A |
| Portable-Alpha-Extension-Model | [#2391](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2391) | [#2363](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2363) | VERIFIED | `compare_runs.py` uses `_sanitize_error_message` without `exc_info=True`; caplog/chained-cause and dashboard regressions; `docs/evidence/issue-2363/redaction-break.txt`. | N/A |
| Pension-Data | [#980](https://github.com/stranske/Pension-Data/pull/980) | [#957](https://github.com/stranske/Pension-Data/issues/957) | VERIFIED | `artifact_data.py` conflict/unresolved-period policy; `app.py` funding-trend exposes `unresolved_periods`; loader + HTTP tests; `INITIAL_VIEWS.md` policy doc. | N/A |
| Portable-Alpha-Extension-Model | [#2392](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2392) | [#2361](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2361) | VERIFIED | `_payload_fingerprint` wired into `explain_results.py` cache key and download payload; tests + `docs/evidence/issue-2361/cache-fingerprint-proof.txt`. | N/A |
| Pension-Data | [#981](https://github.com/stranske/Pension-Data/pull/981) | [#958](https://github.com/stranske/Pension-Data/issues/958) | VERIFIED | `document_orchestration.py` skips rate/% rows for dollar cash-flow fields; orchestration regressions (`cash_flow_uses_monetary_rows`, order variation, rate-only); `docs/evidence/issue-958/money-row-proof.txt` with deliberate-break transcript. | N/A |

## Test-gate, belt-ledger, reproduction, and campaign disposition

- **Belt ledger:** None of the twenty PRs were ledger-only; rule 3b not triggered.
- **Reproduction:** No linked issue in this batch contained a runnable `Reproduction:` block.
- **WF#4082 campaign (parent issue):** Per-consumer one-line PRs in this batch satisfy the consumer checklist item. Issue-level AC for Health-68 `gate triggers: all match` ([Workflows#4084](https://github.com/stranske/Workflows/pull/4084)) and the 48h cancellation pass number were **not re-checked** this run (structural PR not in batch; metric window not due).
- **WF#4068 pass number:** 24h canary/promote budget **not re-checked** (observation window / ops).
- **GitHub writes:** Unit instructions authorize follow-ups, comments, and reopens; **OFFLOAD WORKSPACE RULES** forbid them this run. No issues filed or reopened.

## Resume pointer

~**71** in-window issue-linked non-chore merges remain after `Pension-Data#981` (merged 2026-10-18T12:12:36Z). Next run should continue from this unit’s checkpoint ledger (oldest unverified next: e.g. `Trend_Model_Project#6113`, `Travel-Plan-Permission#1683`, `trip-planner#1922`, …).

**Confidence:** High for homogeneous Gate-trigger PRs and evidence-backed feature fixes (diffs include falsifiable tests and deliberate-break artifacts). Moderate on parent-level WF#4082/WF#4068 time-bounded campaign criteria—not contradicted by diffs, but not operationally re-driven here.
