# D4 verify merged — 2026-10-27T20

**Window:** merges since `2026-10-26T08:21:55Z` (36 h before run). **Fleet:** `SUPPORTED_REPOS` from `handoff.sh`, excluding Orchestrator. **Cap:** 20 PRs (oldest issue-linked first among non-chore merges). **Offload:** GitHub writes (issues, comments, reopen, follow-up filing) not performed; follow-up column records intent only.

**Skipped without verification (dependency / template / release chores):** Python 3.13/3.14 matrix and single-runtime coverage alignment PRs (`Trend_Model_Project` [#6158](https://github.com/stranske/Trend_Model_Project/pull/6158), `learning-management-system` [#796](https://github.com/stranske/learning-management-system/pull/796), `Workflows` [#4272](https://github.com/stranske/Workflows/pull/4272)), plus all `chore: sync workflow templates` and `chore(main): release` merges in the window (55 chore-class merges in discovery).

**Confidence:** High on squash-diff vs acceptance criteria for product fixes and named tests (especially `Trend_Model_Project` #6163–#6166 read this run). Medium on operational timing pass numbers (`Workflows` #4267, `Counter_Risk` #1194) and on re-carried verdicts for merges also covered in `D4-verify-merged-2026-10-26T20` (same squash evidence, not re-fetched this run).

## Results

| Repo | PR | Issue | Verdict | Unmet / deferred criteria | Follow-up filed |
|------|-----|-------|---------|---------------------------|-----------------|
| Fine-Art-Archive | [#851](https://github.com/stranske/Fine-Art-Archive/pull/851) | [#847](https://github.com/stranske/Fine-Art-Archive/issues/847) | VERIFIED | — (carried; `dossier.py` year-zero guard + named tests in prior diff read) | — |
| Workflows | [#4267](https://github.com/stranske/Workflows/pull/4267) | [#4258](https://github.com/stranske/Workflows/issues/4258) | PARTIAL | Pass number due 2026-11-15 (python 3.14 job ≤10 min on last 5 runs) not evaluable this run; `test_gate_pytest_args_are_parallel` / `-n auto` present in prior squash read | No (monitoring; offload) |
| Counter_Risk | [#1194](https://github.com/stranske/Counter_Risk/pull/1194) | [#1193](https://github.com/stranske/Counter_Risk/issues/1193) | PARTIAL | Longest Gate python job ≤10 min pass number (2026-11-15) deferred; loadscope removal + named test in prior squash read | No (monitoring; offload) |
| Trend_Model_Project | [#6159](https://github.com/stranske/Trend_Model_Project/pull/6159) | [#6127](https://github.com/stranske/Trend_Model_Project/issues/6127) | VERIFIED | — (`store_paths` validation + `tests/monte_carlo/test_output_store_paths.py`; carried) | — |
| Trend_Model_Project | [#6161](https://github.com/stranske/Trend_Model_Project/pull/6161) | [#6149](https://github.com/stranske/Trend_Model_Project/issues/6149) | VERIFIED | — (decision-only manager guard + `test_manager_changes_with_only_decision_event`; carried) | — |
| Trend_Model_Project | [#6162](https://github.com/stranske/Trend_Model_Project/pull/6162) | [#6150](https://github.com/stranske/Trend_Model_Project/issues/6150) | VERIFIED | — (`max_drawdown` display + named test; carried) | — |
| learning-management-system | [#798](https://github.com/stranske/learning-management-system/pull/798) | [#789](https://github.com/stranske/learning-management-system/issues/789) | VERIFIED | — (performance-weighted confidence + `test_estimate_confidence_reflects_performance_history`; carried) | — |
| learning-management-system | [#800](https://github.com/stranske/learning-management-system/pull/800) | [#791](https://github.com/stranske/learning-management-system/issues/791) | VERIFIED | — (self-grade/scoring UI + `test_learn_post_surfaces_self_grade_or_scored_correctness`; carried) | — |
| learning-management-system | [#801](https://github.com/stranske/learning-management-system/pull/801) | [#790](https://github.com/stranske/learning-management-system/issues/790) | VERIFIED | — (calibration surface + `test_learner_calibration_page_shows_bucket_accuracy`; carried) | — |
| Trend_Model_Project | [#6163](https://github.com/stranske/Trend_Model_Project/pull/6163) | [#6129](https://github.com/stranske/Trend_Model_Project/issues/6129) | VERIFIED | Squash diff adds C4 row + C3 probe text in `docs/PRODUCT_CONTRACT.md`; new `tests/test_product_contract.py::test_product_contract_lists_core_function_c4` asserts regime export row | — |
| Trend_Model_Project | [#6164](https://github.com/stranske/Trend_Model_Project/pull/6164) | [#6148](https://github.com/stranske/Trend_Model_Project/issues/6148) | VERIFIED | `_chain_cache_signature` returns SHA-256 hex; strict xfail removed from `test_config_chat_contents_signature_label_distinguishes_cache_keys` | — |
| Trend_Model_Project | [#6166](https://github.com/stranske/Trend_Model_Project/pull/6166) | [#6147](https://github.com/stranske/Trend_Model_Project/issues/6147) | VERIFIED | `round` + clamp at widget sync/render sites; xfail removed; parametrized `test_sync_model_widgets_round_trips_whole_percentages` and save-path coverage in `test_coverage_wp_t8.py` | — |

**Summary:** 12 issue-linked PRs verified (under 20 cap). **VERIFIED:** 10. **PARTIAL:** 2 (operational CI timing pass numbers only). **NOT IMPLEMENTED:** 0. **Belt ledger-only merges:** none in verified set. **Reproduction blocks:** none on linked issues for this batch. **Follow-ups filed:** 0 (offload prohibits GitHub writes).

## Notes

- **Issue-linked queue exhausted** for this window after skipping dependency-matrix chores; 11 merged `Workflows` PRs in-window have no linked issue reference in body/`closingIssuesReferences` and were out of scope for this track.
- **#6166** evidence doc documents deliberate-break transcript; not re-run locally this unit (no `Reproduction:` block on issue).
- **Workflows#3391 belt defect:** no ledger-only merge with falsely `done` tasks observed in this batch.

## Ledger

Next run: resume after `Trend_Model_Project#6166` (last checkpoint row). Re-check any new merges after `2026-10-27T06:06:24Z` and any `Workflows` merges that later gain issue links.
