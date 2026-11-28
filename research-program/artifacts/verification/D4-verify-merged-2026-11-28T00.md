# Verification Report — D4-verify-merged-2026-11-28T00

- **Window:** Last 36 hours (`mergedAt >= 2026-11-26T12:58:40Z`, anchored to `2026-11-28T00:58:40Z`) across the 15 `SUPPORTED_REPOS` in `[LOCAL_HOME]/.codex/bin/handoff.sh` (excluding `stranske/Orchestrator`).
- **Inventory & pacing:** Scanned 203 merged PRs (zero secondary rate limits); identified 89 non-chore PRs not covered in `D4-verify-merged-2026-11-27T00`; excluded PRs lacking an issue reference (citing only PRs or external PRs); verified the oldest **20** eligible PRs. Remaining eligible PRs starting with `Workflows#5338` (`2026-11-27T12:59:14Z`) through `Trend_Model_Project#6262` (`2026-11-28T00:44:35Z`) are deferred to the next run under the 20-PR pacing cap.
- **Reproduction & offload constraint:** None of the 21 linked issues carried a `Reproduction:` block. One issue (`Manager-Mosaic#172`) named core function `CF-5` and was re-driven locally (`WORKS`). Notice of rule conflict: the D4 brief instructs filing a follow-up issue for every `PARTIAL`/`NOT IMPLEMENTED` finding, whereas `OFFLOAD WORKSPACE RULES` strictly prohibits GitHub writes (creating issues, commenting, reopening, editing labels). Consistent with prior offload runs, **0 GitHub writes were performed**; for the single `PARTIAL` verdict (`Workflows#5332`), the live defect on tip `af8b2c9990` was already repaired later on `2026-11-27` by merged `Workflows#5338` (`dea846b8d8`, deferred to the next run).

## Summary Table

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|---|---|---|---|---|---|
| `stranske/Workflows` | [#5275](https://github.com/stranske/Workflows/pull/5275) | [#5271](https://github.com/stranske/Workflows/issues/5271) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5289](https://github.com/stranske/Workflows/pull/5289) | [#4484](https://github.com/stranske/Workflows/issues/4484) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5298](https://github.com/stranske/Workflows/pull/5298) | [#5296](https://github.com/stranske/Workflows/issues/5296) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5299](https://github.com/stranske/Workflows/pull/5299) | [#5296](https://github.com/stranske/Workflows/issues/5296), [#2819](https://github.com/stranske/Workflows/issues/2819) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5302](https://github.com/stranske/Workflows/pull/5302) | [#5300](https://github.com/stranske/Workflows/issues/5300) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5297](https://github.com/stranske/Workflows/pull/5297) | [#5296](https://github.com/stranske/Workflows/issues/5296) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5301](https://github.com/stranske/Workflows/pull/5301) | [#5300](https://github.com/stranske/Workflows/issues/5300) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5307](https://github.com/stranske/Workflows/pull/5307) | [#4082](https://github.com/stranske/Workflows/issues/4082), [#4522](https://github.com/stranske/Workflows/issues/4522) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5291](https://github.com/stranske/Workflows/pull/5291) | [#1836](https://github.com/stranske/Workflows/issues/1836) | **VERIFIED** | None | — |
| `stranske/Manager-Mosaic` | [#173](https://github.com/stranske/Manager-Mosaic/pull/173) | [#172](https://github.com/stranske/Manager-Mosaic/issues/172) (`CF-5`) | **VERIFIED** | None (`CF-5`: **WORKS**) | — |
| `stranske/Workflows` | [#5313](https://github.com/stranske/Workflows/pull/5313) | [#3383](https://github.com/stranske/Workflows/issues/3383), [#1299](https://github.com/stranske/Workflows/issues/1299), [#1366](https://github.com/stranske/Workflows/issues/1366) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5317](https://github.com/stranske/Workflows/pull/5317) | [#5315](https://github.com/stranske/Workflows/issues/5315) | **VERIFIED** | None | — |
| `stranske/trip-planner` | [#2068](https://github.com/stranske/trip-planner/pull/2068) | [#2066](https://github.com/stranske/trip-planner/issues/2066), [#2044](https://github.com/stranske/trip-planner/issues/2044) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5318](https://github.com/stranske/Workflows/pull/5318) | [#5315](https://github.com/stranske/Workflows/issues/5315) | **VERIFIED** | None | — |
| `stranske/trip-planner` | [#2073](https://github.com/stranske/trip-planner/pull/2073) | [#2071](https://github.com/stranske/trip-planner/issues/2071), [#697](https://github.com/stranske/trip-planner/issues/697) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5323](https://github.com/stranske/Workflows/pull/5323) | [#5324](https://github.com/stranske/Workflows/issues/5324) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5326](https://github.com/stranske/Workflows/pull/5326) | [#5325](https://github.com/stranske/Workflows/issues/5325) | **VERIFIED** | None | — |
| `stranske/Deliverable-Render` | [#163](https://github.com/stranske/Deliverable-Render/pull/163) | [#162](https://github.com/stranske/Deliverable-Render/issues/162) | **VERIFIED** | None | — |
| `stranske/Workflows` | [#5332](https://github.com/stranske/Workflows/pull/5332) | [#5324](https://github.com/stranske/Workflows/issues/5324) | **PARTIAL** | **AC 5:** At `#5332` tip (`af8b2c9990`), post-merge `workflow_dispatch` runs `45995663642` & `45995742376` matched `<!-- backplane-freshness-tracker:v1 -->` in `#5324`'s body and overwrote/closed `#5324` (`2026-11-27T12:08:33Z`) instead of opening a dedicated marker issue; `gh issue list --search "backplane-freshness-tracker in:body"` still matches 3 issues (`#5339`, `#5324`, `#4770`). | No (offload rule forbids GitHub writes; identity bug subsequently repaired by merged `Workflows#5338`) |
| `stranske/trip-planner` | [#2074](https://github.com/stranske/trip-planner/pull/2074) | [#2072](https://github.com/stranske/trip-planner/issues/2072) | **VERIFIED** | None | — |

## Skipped (Not Verified This Run)

- **Previously verified in `D4-verify-merged-2026-11-27T00` (9 PRs):** `Workflows#5260..5277`, `Trend_Model_Project#6251`.
- **Chores excluded by scope:** `chore: sync workflow templates`, dependency/Renovate PRs, `chore(main): release *`, and `chore: clean up tracked PR body` PRs across the fleet.
- **No-issue / PR-only-reference PRs (26 PRs):** `Workflows#5264`, `5266`, `5267`, `5272`, `5276`, `5278`, `5279`, `5281`, `5282`, `5283`, `5284`, `5285`, `5286`, `5287`, `trip-planner#2065`, `Workflows#5292`, `5294`, `5290`, `5295`, `5305`, `5306`, `5308`, `5309`, `5311`, `5310` (cites only `Workflows-Integration-Tests/pull/69`), and `5312`.
- **Deferred past 20-PR pacing cap:** Eligible PRs merged from `Workflows#5338` (`2026-11-27T12:59:14Z`) through `Trend_Model_Project#6262` (`2026-11-28T00:44:35Z`).

## Per-PR Verification Notes

1. **`Workflows#5275` (`ab57c177d9`, `2026-11-26T17:32:40Z`) -> `#5271` — VERIFIED**
   - Diff modifies `.github/workflows/reusable-10-ci-python.yml` and `tests/workflows/test_reusable_ci_workflow.py` (4 bash subprocess tests for `Finalize check results` covering JUnit failures/errors and coverage shortfall).
   - CI: 126 `SUCCESS`, 0 failed. Local `python3 -m pytest -c pyproject.toml -p no:asyncio --import-mode=importlib -q tests/workflows/test_reusable_ci_workflow.py -k finalize_check_results`: `4 passed, 53 deselected in 2.36s`.

2. **`Workflows#5289` (`2c70670643`, `2026-11-27T00:40:25Z`) -> `#4484` — VERIFIED**
   - Diff deletes `scripts/reconcile_issue_4484_ledger.py` and `tests/scripts/test_reconcile_issue_4484_ledger.py`, relocates `issue-4484-validation.md` and `issue-4534-acceptance.json` into `docs/evidence/issue-4484/`, updates receipt paths in `.agents/issue-4484-ledger.yml`, adds `test_validate_ledger_accepts_retained_task_evidence` in `tests/scripts/test_ledger_validate.py`, and updates `docs/reports/workflows-cleanup-tracker.md`.
   - Belt-ledger check: not a ledger-only PR; `task-09` remains `blocked` and `task-11` cites `a0547eff1150b59ca8009a226c1dfca3d4f6118b`. CI: 49 `SUCCESS`, 0 failed.

3. **`Workflows#5298` (`f5a448dd21`, `2026-11-27T01:34:42Z`) -> `#5296` — VERIFIED**
   - Diff updates `.github/sync-manifest.yml` (`requires: scripts/langchain/response_content.py`), updates `scripts/langchain/task_validator.py` and `templates/consumer-repo/scripts/langchain/task_validator.py` to use `text_from_response_content`, and expands `tests/scripts/test_task_validator.py` (including `blocks` parameter and `test_refinement_without_text_preserves_original_task`).
   - CI: 50 `SUCCESS`, 0 failed. Local `tests/scripts/test_task_validator.py` passed inside the 371-test local Workflows pytest run (`371 passed in 2.91s`).

4. **`Workflows#5299` (`ce64a90124`, `2026-11-27T01:41:47Z`) -> `#5296`, `#2819` — VERIFIED**
   - Diff updates `.github/workflows/maint-45-cosmetic-repair.yml`, `maint-84-prune-agent-stubs.yml`, and `maint-86-model-promotion-prepare.yml` to emit `<!-- workflow-source:automation_run -->`, `<!-- workflow-source-ref:... -->`, and `Workflow run:` URLs, and adds `resolvePrSourceContext recognizes the actual retained maintenance publisher bodies as automation runs` to `.github/scripts/__tests__/source-context.test.js`.
   - CI: 56 `SUCCESS`, 0 failed. Local `node --test` on the 5 JS test suites passed (`tests 105, pass 105, fail 0, skipped 0`).

5. **`Workflows#5302` (`27665552cf`, `2026-11-27T01:42:32Z`) -> `#5300` — VERIFIED**
   - Diff updates `docs/reports/workflow-decisions.md` and `docs/reports/workflows-cleanup-tracker.md` documenting hosted optimizer acceptance on `#5300` and `#5295`. CI: 19 `SUCCESS`, 0 failed.

6. **`Workflows#5297` (`600c3fb993`, `2026-11-27T01:46:38Z`) -> `#5296` — VERIFIED**
   - Diff adds `SOURCE_MARKER`, `SOURCE_LABEL`, `cleanupPullBody`, and `repairProvenance` in `.github/scripts/maint72-pr-body-cleanup.js`, 4 unit tests in `.github/scripts/__tests__/maint72-pr-body-cleanup.test.js`, and coverage in `tests/workflows/test_no_silent_api_failures.py`.
   - Local `node --test` passed (within the 105 passing JS tests). In CI, 50 checks succeeded while 2 auxiliary checks (`guard`, `Apply verified source issue closure rule`) failed on a GitHub App 403 API rate limit (`run 45924532983`), unrelated to code correctness.

7. **`Workflows#5301` (`e8ce269b4a`, `2026-11-27T02:15:25Z`) -> `#5300` — VERIFIED**
   - Diff updates `.github/scripts/issue_format.py` and `templates/consumer-repo/.github/scripts/issue_format.py` (`_is_source_repository`, `_guide_path`, `Report.guide_path`, `REWRITE_INSTRUCTIONS`) and adds 4 parametrized test functions (including the `#5296` body) in `tests/scripts/test_issue_format.py`.
   - CI: 54 `SUCCESS`, 0 failed. Local `tests/scripts/test_issue_format.py` passed within the 371-test Workflows pytest run.

8. **`Workflows#5307` (`b95fcb6b37`, `2026-11-27T03:58:58Z`) -> `#4082`, `#4522` — VERIFIED**
   - Diff deletes `scripts/measure_gate_cancellations.py` and `tests/scripts/test_measure_gate_cancellations.py`, records offline `jq` recount (`complete 0/401 (0%)`) and `git archive` recovery in `docs/evidence/issue-4082/VERIFICATION_SUMMARY_4522.md`, and updates `docs/ops/CONSUMER_REPO_MAINTENANCE.md`. CI: 47 `SUCCESS`, 0 failed.

9. **`Workflows#5291` (`4b014ef31a`, `2026-11-27T05:02:25Z`) -> `#1836` — VERIFIED**
   - Diff implements `.github/workflows/maint-90-sync-finding-assessment.yml`, `.github/scripts/maint71_finding_assessment.js`, `maint90_finding_assessment_run.js`, `maint90_run_regression.py`, `maint71_finding_verification.js` (`summary_variants`), `config/consumer_sync_review_policy.json`, supporting docs under `docs/`, `tests/workflows/test_maint90_run_regression.py`, and `.github/scripts/__tests__/maint71_finding_assessment.test.js`.
   - CI: 55 `SUCCESS`, 0 failed. Local `node --test` on `maint71_finding_assessment.test.js` passed within the 105-test run.

10. **`Manager-Mosaic#173` (`30f15b6956`, `2026-11-27T06:02:39Z`) -> `#172` (`CF-5`) — VERIFIED (`CF-5`: WORKS)**
    - Diff updates `agents/claude-172.md`, `docs/PRODUCT_CONTRACT.md` (`CF-5` row), `src/manager_mosaic/evidence.py` (`validate_evidence_object(payload: Any)` checking `is_object = isinstance(payload, dict)`), and `tests/test_evidence_validation.py` (`test_validate_evidence_object_reports_non_object_root`).
    - Local `python3 -m pytest -q --no-cov tests/test_evidence_validation.py tests/test_backplane_fixtures.py`: `34 passed in 1.45s`. Live CF-5 probe on `manager_mosaic.validate_evidence_object`: non-object inputs (`None`, `[]`, `3`, `True`, `"text"`) each returned `["... is not of type 'object'"]`, `tests/fixtures/backplane/valid_evidence_object.json` returned `[]`, and an incomplete dict returned 6 violations. CI: 68 `SUCCESS`, 4 `CANCELLED` (`Resolve Context`, `Record autofix dispatch completion`).

11. **`Workflows#5313` (`55d923ffb9`, `2026-11-27T07:03:09Z`) -> `#3383`, `#1299`, `#1366` — VERIFIED**
    - Diff removes `apply-correction` from `.github/workflows/agents-verify-to-new-pr.yml` and its template mirror, removes `verifier_correction_artifact_sdk/{package.json,package-lock.json}` (both trees) and `runtimeArtifactClient`, updates `.github/sync-manifest.yml`, `consumer-managed-paths.json`, `docs/ops/VERIFIER_CORRECTION_*.md`, `tests/scripts/test_sync_manifest_compiler.py` (`280` entries, `19` removals), and JS tests (`verifier-correction-inert-deployment.test.js`, `verifier-correction-wiring.test.js`).
    - CI: 55 `SUCCESS`, 0 failed. Local `node --test` passed within the 105-test run.

12. **`Workflows#5317` (`58b8cc887b`, `2026-11-27T07:31:31Z`) -> `#5315` — VERIFIED**
    - Diff updates `README.md` (`### First-party Consumers`), `docs/INTEGRATION_GUIDE.md` (`### Method 2: Template Workflows`), and `tests/docs/test_integration_guide_current_defaults.py` (`test_delivery_entry_points_match_generated_delivery_review_policy`).
    - CI: 40 `SUCCESS`, 0 failed. Local `tests/docs/test_integration_guide_current_defaults.py` passed within the 371-test Workflows pytest run.

13. **`trip-planner#2068` (`7cdce0bfd2`, `2026-11-27T07:46:35Z`) -> `#2066`, `#2044` — VERIFIED**
    - Diff updates `.github/workflows/cross-repo-smoke.yml`, `Makefile`, `docs/CROSS_REPO_SMOKE.md`, `scripts/build_section15_receipt.py`, `scripts/check_full_product_verification.py`, `tests/app/test_full_product_verification.py`, `tests/preferences/test_legacy_request_adapter.py`, and `tests/scripts/test_cross_repo_smoke_workflow.py`.
    - CI: 40 `SUCCESS`, 0 failed; post-merge Cross-Repo Smoke run `45960798737` on head `7cdce0bfd2f969dc3bfc951c990d633676e9da55` finished `success` (`cross-repo-full-product: success`).

14. **`Workflows#5318` (`c538df7c32`, `2026-11-27T08:05:01Z`) -> `#5315` — VERIFIED**
    - Diff updates `docs/reports/workflow-decisions.md` and `docs/reports/workflows-cleanup-tracker.md` separating hosted `#5315` filing from `#5317`. CI: 20 `SUCCESS`, 0 failed.

15. **`trip-planner#2073` (`efc6bfa8aa`, `2026-11-27T09:50:04Z`) -> `#2071`, `#697` — VERIFIED**
    - Diff updates `frontend/src/api/workspace.ts`, `frontend/src/api/workspace.test.ts`, `frontend/src/routes/WorkspacePage.tsx`, `frontend/src/routes/WorkspacePage.test.tsx`, `scripts/check_full_product_verification.py`, `tests/app/test_full_product_verification.py`, `tests/app/test_policy_sync_route.py`, and `docs/design-coverage-map.md`.
    - CI: 54 `SUCCESS`, 0 failed; post-merge Cross-Repo Smoke run `45977004300` on head `efc6bfa8aad2bdabcf3c7952b1db5e730486a558` finished `success` (`cross-repo-full-product: success`).

16. **`Workflows#5323` (`cc47ee037a`, `2026-11-27T10:13:21Z`) -> `#5324` — VERIFIED**
    - Diff updates `docs/reports/workflow-decisions.md` and `docs/reports/workflows-cleanup-tracker.md` recording the structure review and citing `#5324` as context without claiming implementation of `#5324`. CI: 20 `SUCCESS`, 0 failed.

17. **`Workflows#5326` (`f35a4e4c00`, `2026-11-27T10:49:28Z`) -> `#5325` — VERIFIED**
    - Diff updates `scripts/check_issue_consistency.py` (`is_comment_line` restricting markdown scanning to `<!--`) and adds 3 unit tests in `tests/scripts/test_issue_consistency_check.py`.
    - CI: 47 `SUCCESS`, 0 failed. Local `tests/scripts/test_issue_consistency_check.py` passed within the 371-test Workflows pytest run.

18. **`Deliverable-Render#163` (`172f888f21`, `2026-11-27T11:15:55Z`) -> `#162` — VERIFIED**
    - Diff updates `README.md`, `src/deliverable_render/html.py` (`_url_path(..., file_authority=...)`, case-insensitive `file://`), and `tests/test_render_html_offline.py` (12 parametrized UNC cases). CI: 34 `SUCCESS`, 0 failed (not run locally because host Python is 3.12 vs project `>=3.13`).

19. **`Workflows#5332` (`af8b2c9990`, `2026-11-27T12:04:02Z`) -> `#5324` — PARTIAL**
    - Diff updates `.github/workflows/health-78-backplane-contract.yml`, `docs/LABELS.md`, `docs/contracts/research-backplane-contract.md`, `scripts/validate_backplane_registry.py`, and `tests/test_backplane_registry.py`.
    - Offline checks passed: CI had 74 `SUCCESS` and 2 `CANCELLED`; local `python3 -m pytest -c pyproject.toml -p no:asyncio --import-mode=importlib -q tests/test_backplane_registry.py` passed (within the 371-test run) and `python3 scripts/validate_backplane_registry.py --check-status docs/reports/backplane_registry_status.md` exited 0.
    - **Why PARTIAL:** `#5324` AC 5 requires that after merge, running `workflow_dispatch` on `main` twice produces one open marker issue citing both run URLs and that `gh issue list --repo stranske/Workflows --search "backplane-freshness-tracker in:body"` returns exactly one issue. At `#5332` merge commit `af8b2c9990`, `publish-freshness-tracker` searched via `(item.body || '').includes('<!-- backplane-freshness-tracker:v1 -->')`, so post-merge `workflow_dispatch` runs `45995663642` and `45995742376` (`2026-11-27T12:04–12:05Z`) matched design issue `#5324` itself, overwrote `#5324`'s body, and closed `#5324` (`2026-11-27T12:08:33Z`) instead of opening a dedicated tracker issue. Later PR `Workflows#5338` (`dea846b8d8`, merged `2026-11-27T12:59:14Z`, deferred to next run) repaired first-line marker matching and opened `#5339` (`12:59:43Z`), though `gh issue list --repo stranske/Workflows --search "backplane-freshness-tracker in:body" --state all` still returns 3 issues (`#5339`, `#5324`, `#4770`) because `#5324` and `#4770` quote the marker string in body text.

20. **`trip-planner#2074` (`71a292c391`, `2026-11-27T12:45:11Z`) -> `#2072` — VERIFIED**
    - Diff updates `trip_planner/app/services/workspace.py`, `scripts/check_full_product_verification.py`, `tests/app/test_workspace.py`, `tests/app/test_scenario_policy_preview.py`, and `tests/scripts/test_check_full_product_verification.py` (with deliberate-break evidence recorded on the PR). CI: 52 `SUCCESS`, 0 failed.

## Belt Ledger Rule (`Workflows#3391`)

- Zero merged PRs in this 20-PR batch were `.agents/issue-<n>-ledger.yml`-only bookkeeping commits; `Workflows#5289` edited `.agents/issue-4484-ledger.yml` alongside evidence relocation and test changes, with `task-09` still `blocked` and `task-11` referencing a real commit (`a0547eff1150b59ca8009a226c1dfca3d4f6118b`). No `Workflows#3391` defects triggered.

## Confidence

- **High confidence** on the 13 `Workflows` code/script/test PRs and `Manager-Mosaic#173` (locally executed `371 passed` pytest, `4 passed` targeted CI-workflow pytest, `--check-status` exit 0, `105` passing Node tests, `34 passed` Manager-Mosaic pytest + live CF-5 varying-input probe), `Workflows#5332` `PARTIAL` (directly verified against live `gh run` and `gh issue` records), and `trip-planner#2068`/`#2073` (verified by diff + post-merge `Cross-Repo Smoke` runs `45960798737` and `45977004300`).
- **Medium confidence** on `Deliverable-Render#163` (diff + 34 CI passes; host Python 3.12 prevented running its `>=3.13` pytest suite locally) and `trip-planner#2074` (diff + 52 CI passes + deliberate-break record; no local pytest run). Running those suites in matching environments, or checking `Workflows#5338` in the next run, would confirm or refine those verdicts.
