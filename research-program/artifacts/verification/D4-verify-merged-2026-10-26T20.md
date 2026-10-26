# D4 verify merged — 2026-10-26T20

**Window:** merges since `2026-10-25T08:08:14Z` (36 h before run). **Fleet:** `SUPPORTED_REPOS` from `handoff.sh`, excluding Orchestrator. **Cap:** 20 PRs (oldest issue-linked first among non-chore merges). **Offload:** GitHub writes (issues, comments, reopen) not performed; follow-up column records intent only.

**Skipped without verification (dependency / template / release chores):** Python 3.13/3.14 matrix and aligned-coverage PRs (e.g. trip-planner #1936, Travel-Plan-Permission #1692, Ready #641, Deliverable-Render #107, Portable-Alpha-Extension-Model #2434, Doc-Lineage #148, Fine-Art-Archive #848, Manager-Database #1856, Inv-Man-Intake #1043, Pension-Data #992, Trend_Model_Project #6158, learning-management-system #796), plus all `chore: sync workflow templates` and `chore(main): release` merges in the window.

**Confidence:** High on diff-vs-AC for product fixes and named tests; medium on Workflows verifier/sync PRs (large diffs, not re-run locally); operational AC (Health 85 p50, Maint 68 promotion timelines, future dated pass numbers) judged against merge evidence only, not live re-read.

## Results

| Repo | PR | Issue | Verdict | Unmet / deferred criteria | Follow-up filed |
|------|-----|-------|---------|---------------------------|-----------------|
| Workflows | [#4240](https://github.com/stranske/Workflows/pull/4240) | [#4239](https://github.com/stranske/Workflows/issues/4239) | VERIFIED | — | — |
| Workflows | [#4242](https://github.com/stranske/Workflows/pull/4242) | [#4239](https://github.com/stranske/Workflows/issues/4239) | VERIFIED | — (bootstrap/provenance follow-up to #4240) | — |
| Trend_Model_Project | [#6130](https://github.com/stranske/Trend_Model_Project/pull/6130) | [#6128](https://github.com/stranske/Trend_Model_Project/issues/6128) | VERIFIED | — | — |
| Trend_Model_Project | [#6132](https://github.com/stranske/Trend_Model_Project/pull/6132) | [#6124](https://github.com/stranske/Trend_Model_Project/issues/6124) | PARTIAL | Health 85 trailing-seven-day Gate p50 ≤10 min for 7 consecutive days (post-merge metric; not re-read this run) | No (monitoring) |
| Workflows | [#4245](https://github.com/stranske/Workflows/pull/4245) | [#3987](https://github.com/stranske/Workflows/issues/3987) | PARTIAL | Maint 68 promotion run success within 24h; consumer default-branch muse pin; job summary `plans sealed awaiting promotion: 0` (operational, not re-run) | No (monitoring) |
| Inv-Man-Intake | [#1042](https://github.com/stranske/Inv-Man-Intake/pull/1042) | [#1012](https://github.com/stranske/Inv-Man-Intake/issues/1012) (refs only) | VERIFIED | PR states it does not certify #1012 product completion; gate AC in PR body met in diff (`.github/workflows/pr-00-gate.yml` only) | — |
| Counter_Risk | [#1191](https://github.com/stranske/Counter_Risk/pull/1191) | [#1189](https://github.com/stranske/Counter_Risk/issues/1189) | PARTIAL | Same Health 85 p50 pass number as #6124 | No (monitoring) |
| Workflows | [#4265](https://github.com/stranske/Workflows/pull/4265) | [#4254](https://github.com/stranske/Workflows/issues/4254) | VERIFIED | `test_recovery_window_counts_records_accumulated_across_*` and related guard tests added in squash diff | — |
| Fine-Art-Archive | [#851](https://github.com/stranske/Fine-Art-Archive/pull/851) | [#847](https://github.com/stranske/Fine-Art-Archive/issues/847) | VERIFIED | `dossier.py` uses `year not in (None, "")`; named tests including `test_sidecar_facts_includes_astronomical_year_zero` | — |
| Workflows | [#4267](https://github.com/stranske/Workflows/pull/4267) | [#4258](https://github.com/stranske/Workflows/issues/4258) | PARTIAL | Pass number due 2026-11-15 (python 3.14 job ≤10 min on last 5 runs) not yet evaluable; `test_gate_pytest_args_are_parallel` and `-n auto` present in diff | No (monitoring) |
| Counter_Risk | [#1194](https://github.com/stranske/Counter_Risk/pull/1194) | [#1193](https://github.com/stranske/Counter_Risk/issues/1193) | PARTIAL | Longest Gate python job ≤10 min pass number (2026-11-15 read) deferred; `test_gate_pytest_args_do_not_use_loadscope` and workflow change in diff | No (monitoring) |
| Trend_Model_Project | [#6159](https://github.com/stranske/Trend_Model_Project/pull/6159) | [#6127](https://github.com/stranske/Trend_Model_Project/issues/6127) | VERIFIED | AC allows reject-unknown: `store_paths` validation + `tests/monte_carlo/test_output_store_paths.py` | — |
| Trend_Model_Project | [#6161](https://github.com/stranske/Trend_Model_Project/pull/6161) | [#6149](https://github.com/stranske/Trend_Model_Project/issues/6149) | VERIFIED | Empty-frame guard + `test_manager_changes_with_only_decision_event` in diff | — |
| Trend_Model_Project | [#6162](https://github.com/stranske/Trend_Model_Project/pull/6162) | [#6150](https://github.com/stranske/Trend_Model_Project/issues/6150) | VERIFIED | `max_drawdown` lookup + `test_single_period_return_tab_shows_the_max_d` | — |
| learning-management-system | [#798](https://github.com/stranske/learning-management-system/pull/798) | [#789](https://github.com/stranske/learning-management-system/issues/789) | VERIFIED | `test_estimate_confidence_reflects_performance_history`; policy uses performance-weighted confidence (not count-only) | — |
| learning-management-system | [#800](https://github.com/stranske/learning-management-system/pull/800) | [#791](https://github.com/stranske/learning-management-system/issues/791) | VERIFIED | `test_learn_post_surfaces_self_grade_or_scored_correctness`; self-grade action in HTML | — |
| learning-management-system | [#801](https://github.com/stranske/learning-management-system/pull/801) | [#790](https://github.com/stranske/learning-management-system/issues/790) | VERIFIED | Calibration route/tests (`test_learner_calibration_page_shows_bucket_accuracy`) | — |
| Workflows | [#4250](https://github.com/stranske/Workflows/pull/4250) | — (TMP [#6134](https://github.com/stranske/Trend_Model_Project/pull/6134) review) | VERIFIED | PR-body AC: required comment retention through fitter; large test additions in diff | — |
| Workflows | [#4247](https://github.com/stranske/Workflows/pull/4247) | — (sync incident) | VERIFIED | Sealed Gate recovery resolver refresh in maint71 tests/scripts (no linked issue; verified against PR summary/tasks) | — |
| Ready | [#644](https://github.com/stranske/Ready/pull/644) | — (fleet gate delivery) | VERIFIED | `tests/test_publication_safety.py` extended for seal+publication summary matrix (16 combinations) | — |

**Summary:** 20 PRs verified. **VERIFIED:** 15. **PARTIAL:** 5 (all operational pass-number / Maint metrics, not missing implementation in squash diff). **NOT IMPLEMENTED:** 0. **Belt ledger-only merges:** none in this batch. **Reproduction blocks:** none on linked issues for this batch. **Follow-ups filed:** 0 (offload prohibits GitHub writes).

## Notes

- **#4239** landed across two merges (#4240 then #4242); together they add authenticated input-repair recovery, provenance bootstrap, and `test_verification_input_repair` / event tests in the squash diffs. Deliberate-break and live comment readback AC were not re-executed in this unit.
- **Consumer `fix(gate): restore exact-head sealed delivery checks`** PRs (many repos, same window) share Workflows #4245; only Inv-Man-Intake #1042 was in the oldest-20 issue-linked queue. Others remain for a subsequent run.
- **Remaining issue-linked merges in window** (not verified this run due to 20-PR cap): e.g. LMS #796, Pension #992, Fine-Art #848, Trend #6158, Workflows #4273/#4264/#4275/#4279, LMS #800/#801 already counted, etc.

## Ledger

Next run: resume after `Ready#644` (last checkpoint row); skip PRs listed in `D4-verify-merged-2026-10-26T20.CHECKPOINT.md`.
