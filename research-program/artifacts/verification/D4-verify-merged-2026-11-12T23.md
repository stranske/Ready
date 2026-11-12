# D4 merged-PR verification — 2026-11-12

**Outcome number:** 18 eligible PRs reviewed (within the 20-PR per-run cap), 9 VERIFIED, 9 PARTIAL, 0 NOT IMPLEMENTED.

**Check date:** 2026-11-12. Scope was pull requests merged in the preceding 36 hours across `SUPPORTED_REPOS` (excluding `stranske/Orchestrator`), that close or reference an issue. Template-sync chores (21 PRs), dependency updates, and release chores were excluded. Three PRs merged early in the window were already verified in yesterday's checkpoint (`Workflows#4647`, `Manager-Database#1912`, `Ready#679`) and were skipped to avoid duplicate review. The remaining 18 eligible PRs were reviewed oldest-merged first. No GitHub secondary-rate-limit response was encountered.

**Method:** Inspect each squash diff (`gh pr diff <n> -R <repo>`) against the linked issue's Acceptance Criteria (`gh issue view <n> -R <repo>`); verify test existence, CI check conclusions (`Gate / gate` or repo-equivalent required checks), non-vacuous assertions, deliberate-break/mutation evidence, and reproduction blocks where specified. PR descriptions were treated as claims; diffs were treated as evidence.

| Repo | PR | Issue | Verdict | Unmet criteria / evidence | Follow-up filed |
| --- | --- | --- | --- | --- | --- |
| Workflows | [#4644](https://github.com/stranske/Workflows/pull/4644) | [#4636](https://github.com/stranske/Workflows/issues/4636) | VERIFIED | Diff updates `sync_dependency_campaign.js` and tests to classify `unstable` and `has_hooks` as recovered when required checks pass. Named test asserts non-vacuously; required check `Gate / gate` succeeded. | — |
| Workflows | [#4657](https://github.com/stranske/Workflows/pull/4657) | [#4500](https://github.com/stranske/Workflows/issues/4500) | PARTIAL | Diff contains only `scripts/reconcile_issue_4426_coverage.py`, `agents/codex-4500.md`, and evidence files under `docs/evidence/issue-4426/`. It omits `tests/scripts/test_pr_verifier_ranked_remainder.py`, client selection tests in `tests/tools/test_langchain_client.py`, and the ~180 attributable unit reduction. | No — GitHub writes prohibited in this offload |
| Workflows | [#4658](https://github.com/stranske/Workflows/pull/4658) | [#4502](https://github.com/stranske/Workflows/issues/4502) | PARTIAL | Non-vacuous behavioral tests and 9 mutation receipts landed in `test_aggregate_agent_metrics.py`, `test_check_consumer_sync_drift.py`, and `test_validate_run_contract.py` (`Gate / gate` passed). However, Task 1 (`docs/AGENT_ISSUE_FORMAT.md` inspection) remains unperformed/unchecked because the path was absent. | No — GitHub writes prohibited in this offload |
| Pension-Data | [#1027](https://github.com/stranske/Pension-Data/pull/1027) | [#1019](https://github.com/stranske/Pension-Data/issues/1019) | VERIFIED | Diff implements canonical replacement key calculation in `staging_persistence.py`, adds wildcard escaping (`ESCAPE '\'`) for `_` and `%`, removes strict `xfail`s in `test_staging_persistence_postgres_integration.py`, updates `docs/reports/semantic-equality-audit.md`, and adds non-vacuous regressions for `a_b`/`axb` and decimal precision; `Gate / gate` and `postgres-integration` passed. | — |
| Workflows | [#4650](https://github.com/stranske/Workflows/pull/4650) | [#4635](https://github.com/stranske/Workflows/issues/4635) | VERIFIED | Diff implements `--revalidate-retained` provider-free admission in `tools/verifier_event_recovery.py`, adds named tests in `test_retained_verification_recovery.py` matching `-k exact_4509`, and documents unrecoverable historical capture in `docs/analysis/verifier-4509-capture-recovery.md` retaining `NON_PASS`; required `Gate / gate` passed. | — |
| Workflows | [#4656](https://github.com/stranske/Workflows/pull/4656) | [#4632](https://github.com/stranske/Workflows/issues/4632) | VERIFIED | Diff updates `docs/ops/issue-4427-wasm-pytest-handoff.md` with qualifying native-schedule run 42966520283, confirming `#6189 merged` and `#6186 closed unmerged` for Trend_Model_Project, recording source head, and reconciling complete A1–A4 criteria; `Gate / gate` passed. | — |
| Workflows | [#4665](https://github.com/stranske/Workflows/pull/4665) | [#4663](https://github.com/stranske/Workflows/issues/4663) | PARTIAL | Diff implements `scripts/compare_gate_coverage.py` and test reconciliation, but whole-Gate comparison remained blocked (`blocked_before_baseline_replay`), attributable reduction is recorded as null, and `test_pr_verifier_ranked_remainder.py` was not added. | No — GitHub writes prohibited in this offload |
| Workflows | [#4659](https://github.com/stranske/Workflows/pull/4659) | [#4651](https://github.com/stranske/Workflows/issues/4651) | PARTIAL | Diff adds simulated reopening unit tests to `tests/scripts/test_ci_time_budget.py`, but does not provide the live operational acceptance (seven consecutive daily measurements on the `ci-time-budget` branch) required by Issue #4651. | No — GitHub writes prohibited in this offload |
| Workflows | [#4667](https://github.com/stranske/Workflows/pull/4667) | [#4666](https://github.com/stranske/Workflows/issues/4666) | VERIFIED | Diff updates `canaryRefreshFailureClass` in `.github/scripts/maint71_merge_sync_prs.js` to return `'infrastructure'` when only `Create sync PR` failed and earlier steps succeeded; adds tests in `maint71_merge_sync_prs.test.js` and fixture `canary-pr-creation-failure-43114630584.json`; required `Gate / gate` passed. | — |
| Portable-Alpha-Extension-Model | [#2498](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2498) | [#2476](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2476) | PARTIAL | Diff contains only evidence and calibration files under `docs/evidence/issue-2476/` and `agents/codex-2476.md`. No test files (e.g. `tests/test_coverage_round_2381.py`) or production files were modified, and the required ~180-unit coverage reduction was not delivered. | No — GitHub writes prohibited in this offload |
| Trend_Model_Project | [#6220](https://github.com/stranske/Trend_Model_Project/pull/6220) | [#6194](https://github.com/stranske/Trend_Model_Project/issues/6194) | PARTIAL | Diff adds `docs/evidence/issue-6188-closer-acceptance.md` and a structural markdown test in `test_issue_6188_acceptance.py`. However, acceptance criteria checkboxes remain unchecked and exact-head Evidence receipt for Python 3.13 sync acceptance was not established. | No — GitHub writes prohibited in this offload |
| Portable-Alpha-Extension-Model | [#2503](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2503) | [#2496](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2496) | PARTIAL | Diff delivers bundle integrity tests in `tests/test_coverage_round_2375.py` and mutation receipts, but README task status explicitly notes that hosted Gate baseline/final comparison and ~120-unit reduction criteria remain unmet. | No — GitHub writes prohibited in this offload |
| Travel-Plan-Permission | [#1744](https://github.com/stranske/Travel-Plan-Permission/pull/1744) | [#1740](https://github.com/stranske/Travel-Plan-Permission/issues/1740) | VERIFIED | Diff updates `Issues.txt` lines 112-114 to `[x]`, removes `(needs-human)`, points to `.github/workflows/ci.yml:62-88`, and adds non-vacuous regression test `test_issues_txt_orchestration_ci_tasks_match_workflow` in `tests/python/test_http_service.py`; required `Gate / gate` passed. | — |
| Trend_Model_Project | [#6221](https://github.com/stranske/Trend_Model_Project/pull/6221) | [#6208](https://github.com/stranske/Trend_Model_Project/issues/6208) | VERIFIED | Diff records exact-head Python 3.14 CI confirmation for run 42518199588, deliberate-break probe and local suite execution under Python >=3.13 in `docs/acceptance/issue-6205.md`, and adds non-vacuous tests in `tests/scripts/test_issue_6205_acceptance.py`; required `Gate / gate` passed. | — |
| Workflows | [#4672](https://github.com/stranske/Workflows/pull/4672) | [#4669](https://github.com/stranske/Workflows/issues/4669) | VERIFIED | Diff adds provisioned baseline artifacts, `tests/scripts/test_pr_verifier_ranked_remainder.py`, `tests/scripts/test_reconcile_issue_4426_coverage.py`, and records non-null counts (`attributable_round_reduction: 394`, `acceptance_complete: true`) in `docs/evidence/issue-4426/coverage-measurement.json`; required `Gate / gate` passed. | — |
| Workflows | [#4674](https://github.com/stranske/Workflows/pull/4674) | [#4523](https://github.com/stranske/Workflows/issues/4523) | PARTIAL | Diff changes only documentation/evidence files under `docs/evidence/issue-4019/r3/`. It does not merge PR #4516 or cherry-pick the required test files (`test_aggregate_agent_metrics.py`, `test_llm_provider.py`), and commit ancestry verification is not established in git. | No — GitHub writes prohibited in this offload |
| Portable-Alpha-Extension-Model | [#2500](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2500) | [#2495](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2495) | PARTIAL | Diff is confined to `docs/evidence/issue-2336-png-failures/`. Full coverage run was blocked by parameter dictionary schema failure on Python 3.13, and the issue was explicitly left open for structural schema resolution. | No — GitHub writes prohibited in this offload |
| Portable-Alpha-Extension-Model | [#2505](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2505) | [#2504](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2504) | VERIFIED | Diff implements stable type stringification across Python 3.13 and 3.14 in `pa_core/schema.py` (`_union_member_repr`, `_public_module_name`), and adds regression test in `tests/test_schema_export.py`; required `Gate / gate` passed. | — |

## Detailed Findings per PR

### 1. Workflows #4644 (Issue #4636) — VERIFIED
- **Merge commit:** `10e0568019be45e05a8d9a263aa15db4c6328a6f`
- **Criteria analysis:** Issue #4636 demanded that Maint 82 re-plan a recovered `checks_failed` handoff on the same head. PR #4644 is a direct follow-up extending recovery to `unstable` and `has_hooks` states (where non-required checks fail/cancel but required checks succeed).
- **Evidence:** `.github/scripts/sync_dependency_campaign.js` updated; `.github/scripts/__tests__/sync_dependency_campaign.test.js` updated with non-vacuous assertions for `unstable` and `has_hooks` yielding `checks_recovered`.
- **CI Conclusion:** Required check `Gate / gate` succeeded.

### 2. Workflows #4657 (Issue #4500) — PARTIAL
- **Merge commit:** `cfef819777f955beee78bb81ce26b553e4b78619`
- **Criteria analysis:** Issue #4500 required adding `tests/scripts/test_pr_verifier_ranked_remainder.py`, client selection tests in `tests/tools/test_langchain_client.py`, and achieving an attributable ~180-unit coverage reduction across the ranked remainder.
- **Evidence:** Diff of PR #4657 contains 100 files, of which 98 are under `docs/evidence/issue-4426/`, 1 is `agents/codex-4500.md`, and 1 is `scripts/reconcile_issue_4426_coverage.py`. No tests were added to `tests/scripts/` or `tests/tools/`. Attributable reduction was not delivered.
- **Follow-up:** Follow-up issue #4663 was subsequently filed in the repository by closer automation.

### 3. Workflows #4658 (Issue #4502) — PARTIAL
- **Merge commit:** `1cf22634e9e0a2936a28795c6f37ce49942a73a6`
- **Criteria analysis:** Issue #4502 requested three-module coverage across `validate_run_contract.py`, `check_consumer_sync_drift.py`, and `aggregate_agent_metrics.py`.
- **Evidence:** Real behavioral tests and 9 mutation receipts landed in `tests/scripts/test_aggregate_agent_metrics.py`, `tests/scripts/test_check_consumer_sync_drift.py`, and `tests/scripts/test_validate_run_contract.py`. Full `Gate / gate` succeeded. However, Task 1 (`docs/AGENT_ISSUE_FORMAT.md` inspection) remains unperformed/unchecked because the path was absent.

### 4. Pension-Data #1027 (Issue #1019) — VERIFIED
- **Merge commit:** `bc4fa155b9e07504a7428f6d539eeb38ee7fc26f`
- **Criteria analysis:** Issue #1019 required canonical content hashing in replacement key construction, escaping `_` and `%` in `LIKE` queries with `ESCAPE '\'`, removing strict `xfail`s, and updating the audit report.
- **Evidence:** `src/pension_data/db/staging_persistence.py` implements canonical replacement key calculation and wildcard escaping. `tests/db/test_staging_persistence_postgres_integration.py` removes `xfail` marks and adds non-vacuous regressions for representation variants, wildcard isolation (`a_b` vs `axb`), and decimal precision. `docs/reports/semantic-equality-audit.md` updated.
- **CI Conclusion:** Required check `Gate / gate` and `postgres-integration` succeeded.

### 5. Workflows #4650 (Issue #4635) — VERIFIED
- **Merge commit:** `3e309995c7324b8ea16238b16bbd791ee5999cfc`
- **Criteria analysis:** Issue #4635 required provider-free admission for event 872cfa6b5cc9d664566f1aa1ecb5dbeaf303b27bd5a96288414318455a343e9c and `--revalidate-retained` verification retaining `NON_PASS`.
- **Evidence:** `tools/verifier_event_recovery.py` implements `--revalidate-retained`. `tests/tools/test_retained_verification_recovery.py` adds tests matching `-k exact_4509`. `docs/analysis/verifier-4509-capture-recovery.md` documents unrecoverable historical capture and retains `NON_PASS`.
- **CI Conclusion:** Required check `Gate / gate` succeeded.

### 6. Workflows #4656 (Issue #4632) — VERIFIED
- **Merge commit:** `6f0302b1f8cbb81ef236dc99b0c2049e0c7a1cbe`
- **Criteria analysis:** Issue #4632 was a documentation and ops verification contract to capture a qualifying production Maint 71 run log/summary showing `#6189 merged` and `#6186 closed unmerged` for Trend_Model_Project.
- **Evidence:** `docs/ops/issue-4427-wasm-pytest-handoff.md` updated with native run 42966520283, recording the required run ID, event, Workflows head, and both Trend_Model_Project dispositions.
- **CI Conclusion:** Required check `Gate / gate` succeeded.

### 7. Workflows #4665 (Issue #4663) — PARTIAL
- **Merge commit:** `6f4fd58e99633aaaa480815966d678926fcef7c9`
- **Criteria analysis:** Issue #4663 requested a controlled whole-Gate coverage comparison for #3998 and addition of `tests/scripts/test_pr_verifier_ranked_remainder.py`.
- **Evidence:** PR #4665 implemented `scripts/compare_gate_coverage.py` and reconciliation tests, but recorded whole-Gate comparison as `blocked_before_baseline_replay` with null attributable reduction. `tests/scripts/test_pr_verifier_ranked_remainder.py` was not added.
- **Follow-up:** Successor issue #4669 was subsequently filed in the repository.

### 8. Workflows #4659 (Issue #4651) — PARTIAL
- **Merge commit:** `d857fc7c13e54b6d45fc2303c734493393582490`
- **Criteria analysis:** Issue #4651 required verifying the seven-day Gate p50 target on the `ci-time-budget` branch and restoring Health 85 tracking.
- **Evidence:** Diff adds unit tests in `tests/scripts/test_ci_time_budget.py` verifying reopening handling in mock data. The real operational acceptance (seven consecutive daily observations meeting the threshold) was not evidenced by the squash diff.

### 9. Workflows #4667 (Issue #4666) — VERIFIED
- **Merge commit:** `9e0d164d14c2b9a7c6f059c905ea5880496da5e2`
- **Criteria analysis:** Issue #4666 required classifying a Maint 68 Sync job failure as `'infrastructure'` when only `Create sync PR` failed due to GraphQL rate limit.
- **Evidence:** `.github/scripts/maint71_merge_sync_prs.js` updated in `canaryRefreshFailureClass`. `.github/scripts/__tests__/maint71_merge_sync_prs.test.js` updated with non-vacuous regression tests and fixture `canary-pr-creation-failure-43114630584.json`.
- **CI Conclusion:** Required check `Gate / gate` succeeded.

### 10. Portable-Alpha-Extension-Model #2498 (Issue #2476) — PARTIAL
- **Merge commit:** `31d604b9015bcda639ba3932cfd52a220268a6ca`
- **Criteria analysis:** Issue #2476 required delivering remaining ranked-module coverage and approximately 180 fewer uncovered units across seven targets.
- **Evidence:** Diff of PR #2498 consists solely of evidence and calibration artifacts under `docs/evidence/issue-2476/` and `agents/codex-2476.md`. No test or production code was modified; the 180-unit reduction was not delivered.

### 11. Trend_Model_Project #6220 (Issue #6194) — PARTIAL
- **Merge commit:** `4038b50a5013663b9547d0602b99839929e179d1`
- **Criteria analysis:** Issue #6194 required completing exact-target Python 3.13 sync acceptance and recording exact-head Evidence run receipts.
- **Evidence:** Diff adds `docs/evidence/issue-6188-closer-acceptance.md` and a test asserting markdown headings. The acceptance document explicitly notes that no exact-head Evidence receipt was verified, and its criteria checkboxes remain unchecked.

### 12. Portable-Alpha-Extension-Model #2503 (Issue #2496) — PARTIAL
- **Merge commit:** `56c3da985a9df61a7a4023253b27218659d81d2a`
- **Criteria analysis:** Issue #2496 requested bundle integrity assertions, GIF export verification, and a ~120-unit coverage reduction on hosted Gate.
- **Evidence:** Diff updates `tests/test_coverage_round_2375.py` with non-vacuous integrity tests and records mutation receipts in `docs/evidence/issue-2496/`. However, the README task status candidly records that hosted Gate baseline/final comparison and ~120-unit reduction criteria remain open.

### 13. Travel-Plan-Permission #1744 (Issue #1740) — VERIFIED
- **Merge commit:** `904ce20412854378f8cb0a84e27f6c6d09e5196e`
- **Criteria analysis:** Issue #1740 required updating `Issues.txt` orchestration CI tasks to `[x]`, removing `(needs-human)`, adding a pointer to `.github/workflows/ci.yml:62-88`, and adding a regression test.
- **Evidence:** `Issues.txt` updated exactly as requested. `tests/python/test_http_service.py` adds `test_issues_txt_orchestration_ci_tasks_match_workflow` validating YAML workflow jobs, checkbox status, and absence of `(needs-human)`.
- **CI Conclusion:** Required check `Gate / gate` succeeded.

### 14. Trend_Model_Project #6221 (Issue #6208) — VERIFIED
- **Merge commit:** `45c588523c91df348e3a2b8e390c53d4eb95cb4a`
- **Criteria analysis:** Issue #6208 required exact-head Python 3.14 CI verification, deliberate break probe under Python >=3.13, local suite execution record, and non-vacuous regression tests.
- **Evidence:** `docs/acceptance/issue-6205.md` records verified run 42518199588 (attempt 2), probe output under Python 3.14.10, and suite execution. `tests/scripts/test_issue_6205_acceptance.py` adds non-vacuous regression tests.
- **CI Conclusion:** Required check `Gate / gate` succeeded.

### 15. Workflows #4672 (Issue #4669) — VERIFIED
- **Merge commit:** `2d9212ad12a7a514d872b22f46e5595992925eb5`
- **Criteria analysis:** Issue #4669 required provisioned baseline artifacts, executing whole-Gate comparison, adding `tests/scripts/test_pr_verifier_ranked_remainder.py`, and recording non-null attributable reduction counts with `acceptance_complete: true`.
- **Evidence:** Packfile and baseline coverage artifacts provisioned in `docs/evidence/issue-4426/`. `tests/scripts/test_pr_verifier_ranked_remainder.py` and `tests/scripts/test_reconcile_issue_4426_coverage.py` landed. `docs/evidence/issue-4426/coverage-measurement.json` records `attributable_round_reduction: 394` and `acceptance_complete: true`.
- **CI Conclusion:** Required check `Gate / gate` succeeded.

### 16. Workflows #4674 (Issue #4523) — PARTIAL
- **Merge commit:** `f3b6c2a8f895cba2718e873ad92569528d22dfb4`
- **Criteria analysis:** Issue #4523 required integrating PR #4516's test additions (`test_aggregate_agent_metrics.py`, `test_llm_provider.py`, mutation suite) onto `main` and proving ancestry via `git merge-base --is-ancestor`.
- **Evidence:** Diff of PR #4674 is confined entirely to `docs/evidence/issue-4019/r3/`. No test files were modified or merged onto `main`, and commit ancestry was not proven.

### 17. Portable-Alpha-Extension-Model #2500 (Issue #2495) — PARTIAL
- **Merge commit:** `1efd918306041300ce4da255a80d4fbb1b9136ca`
- **Criteria analysis:** Issue #2495 required current-main coverage, 8 RED/GREEN mutation pairs, and supported dispositions for every full-run failure before issue closure.
- **Evidence:** Diff is confined to `docs/evidence/issue-2336-png-failures/`. Full coverage run encountered a parameter dictionary schema failure on Python 3.13; the PR body and README explicitly leave #2495 open for structural schema resolution.

### 18. Portable-Alpha-Extension-Model #2505 (Issue #2504) — VERIFIED
- **Merge commit:** `642b934b281f6211be8dae39818816f1a4e52543`
- **Criteria analysis:** Issue #2504 required updating `pa_core/schema.py::_stringify_type` to render Optional/Union annotations stably across Python 3.13 and 3.14, and adding regression tests in `tests/test_schema_export.py`.
- **Evidence:** `pa_core/schema.py` implements `_union_member_repr` and `_public_module_name` to normalize type reprs across Python 3.13 and 3.14. `tests/test_schema_export.py` adds parameterized regression tests for union/optional stringification.
- **CI Conclusion:** Required check `Gate / gate` succeeded.

## Risks and Limits

- **Reproduction re-run status:** None of the 18 linked issues contained a top-level `Reproduction:` block, so the verbatim reproduction re-run and immediate reopen path did not trigger.
- **Write prohibition:** Per offload rules ("On GitHub, do not open, merge or close pull requests, close issues, edit labels, or post comments or reviews"), follow-up issues and reopens were **not** filed on GitHub. The 9 PARTIAL findings and specific unmet criteria are documented here and in the append-only checkpoint ledger for follow-up by write-authorized lane sessions.
- **Confidence:** High for all 9 VERIFIED rows and for the 9 PARTIAL rows. All evaluations are grounded in the actual squash diffs and CI receipts rather than PR descriptions.
