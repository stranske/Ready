# D4 implementation verification — 2026-09-26T03

**Window:** merged ≥ 2026-09-24T15:48:22Z (36h before run start)  
**Scope:** 20 oldest eligible issue-linked PRs not present in prior D4 unit checkpoints. Template-sync, dependency/release chores, and `stranske/Orchestrator` excluded. Verdicts from squash diffs (`gh pr diff` where available; local `git show` on `[LOCAL_WORKSPACE]/<Repo>` when GitHub secondary rate limit tripped) and linked issue acceptance criteria.

**Method note:** Secondary rate limit hit early during burst `gh pr diff` calls; run paused, then resumed with 12s+ pacing and clone-backed diffs. `gh` authenticated via `with-gh-auth.sh`.

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| learning-management-system | #721 | #666 | PARTIAL | Unique constraint, scope locks, `tests/graphs/test_edge_concurrency.py` in diff. **Unmet:** #666 deliberate-break fail/pass transcripts not in PR body. | [#727](https://github.com/stranske/learning-management-system/issues/727) |
| Workflows | #3562 | #3419 | PARTIAL | Merged PRs use authoritative `fetchPullRequestDiff`; sibling-exclusion tests in `agents-verifier-context.test.js`. **Unmet:** deliberate-break transcripts; live re-verification report per AC. | [#3586](https://github.com/stranske/Workflows/issues/3586) |
| Workflows | #3563 | #3422 | NOT IMPLEMENTED | Retry + integer banners + `test_autopilot_format_pause.py` in diff. **Unmet:** `needs-human` and no `status:in-progress` per AC; tests assert `needs-human` absent and branch preserved vs deleted. | [#3585](https://github.com/stranske/Workflows/issues/3585) |
| Workflows | #3564 | #3423 | VERIFIED | `maint-83-bootstrap-consumer.yml`, `bootstrap_consumer_settings.py`, `tests/scripts/test_bootstrap_consumer_labels.py` with priority label fixtures. | — |
| learning-management-system | #724 | #723 | VERIFIED | `sqlalchemy>=2.0.50,<2.1` in `pyproject.toml`; `test_sqlalchemy_install_stays_on_validated_major_minor` in `tests/test_dependency_version_alignment.py`. | — |
| Workflows | #3566 | #3428 | VERIFIED | Non-finite guards in CI metrics scripts; `test_parse_float_rejects_non_finite_values` / coverage XML nan rejection in diff. | — |
| Workflows | #3569 | #3568 | VERIFIED | Maint 71/82 handoff tests including behind-leased dev-tool routing; workflow/script changes in diff. | — |
| Workflows | #3570 | #3429 | VERIFIED | `ensure_destination` disposable-root guards; `test_ensure_destination_force_rejects_outside_disposable_root` and related tests. | — |
| Workflows | #3571 | #3567 | VERIFIED | Exact-head CodeRabbit reassessment path + idempotent replay tests in `maint71_merge_sync_prs.test.js`. | — |
| trip-planner | #1867 | #1786 | VERIFIED | `tests/eval/test_ranking_fixture.py::test_golden_scenario_scores` + fixture; deliberate-break steps documented in `docs/contracts/source-adapters.md`. | — |
| Portable-Alpha-Extension-Model | #2312 | #2281 | VERIFIED | Sweep RNG isolation in `pa_core/sweep.py` / facade; `tests/test_sweep_common_random_numbers.py` regressions. | — |
| Travel-Plan-Permission | #1636 | #1635 | VERIFIED | Gate workflow JS extraction + `tests/test_gate_commit_status_fork_tolerance.py` fork-403 tolerance cases. | — |
| Workflows | #3574 | #3448 | VERIFIED | `tools/discover_model_catalog.py` bool guard on `_parse_timestamp`; `test_parse_timestamp_rejects_bool_created_at`. | — |
| Workflows | #3577 | #3449 | VERIFIED | Keepalive authority/receipt fixes in `keepalive_loop.js` + `keepalive-loop.test.js` (campaign #1836 sub-issue). | — |
| Workflows | #3578 | #3455 | VERIFIED | `agents-pr-meta-update-body.test.js` exact-head/observer filtering (campaign #1836 sub-issue). | — |
| Portable-Alpha-Extension-Model | #2314 | #2300 | VERIFIED | `pa_core/presets.py` validation + `tests/test_preset_library.py` coverage regressions. | — |
| Counter_Risk | #1118 | #1073 | VERIFIED | `test_reconciliation_gate_rejects_boolean_workbook_total` exercises `_evaluate_cprs_ch_totals_reconciliation` failure on bool notional. | — |
| Ready | #594 | #575 | VERIFIED | Adds `test_black_force_exclude_required_for_explicit_paths` with inline force-exclude removal check. | — |
| Ready | #595 | #575 | VERIFIED | Refines same test (isolates force-exclude vs extend-exclude). | — |
| Ready | #596 | #575 | VERIFIED | Black-format hygiene on existing gate tests; #575 behavior delivered via #594/#595. | — |

**Result:** 17 VERIFIED, 2 PARTIAL, 1 NOT IMPLEMENTED, 0 belt-only bookkeeping merges in batch.  
**Follow-ups filed:** 3 (Workflows #3585, #3586; learning-management-system #727).  
**Deferred:** 13 additional eligible PRs remain in the rolling 36h window for the next D4 pass.

Evidence: `artifacts/verification/evidence/D4-verify-merged-2026-09-26T03/`

**Confidence:** High on NOT IMPLEMENTED (#3563 vs #3422 `needs-human` / claim-release AC). High on PARTIAL rows (implementation present; evidence gaps are documentary). High on VERIFIED rows where named tests and production changes appear in squash diffs. Medium on Counter_Risk #1118 (test-only diff; behavior assumed pre-existing on main and exercised by new regression).
