# D4 implementation verification — 2026-09-21T03

**Window:** merged ≥ 2026-09-19T15:12:52Z (36h before run start)  
**Scope:** 20 oldest eligible issue-linked PRs not verified in prior D4 runs (`D4-2026-09-20T20` consumed the preceding 20). Template-sync, dependency/release chores, `PRODUCT_CONTRACT` doc churn, and `stranske/Orchestrator` excluded from discovery. Verdicts are based on squash diffs (`git show` on `[LOCAL_WORKSPACE]/*/origin/main`) and linked issue acceptance criteria; PR bodies used only for deliberate-break transcripts and gate claims.

**Method note:** `gh` is not authenticated in this executor (`gh auth login` required). Issue/PR metadata via GitHub web fetch; diffs from local shallow clones. Follow-up issues for PARTIAL verdicts could not be filed — blocked on `gh` auth (same constraint as `D4-verify-merged-2026-09-19T02`).

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| Workflows | #3462 | — | EXCLUDED | Evidence-driven `docx`→`python-docx` mapping fix (`scripts/sync_test_dependencies.py` + consumer template) with discriminating tests and deliberate-break transcript in PR body. No linked fleet issue with acceptance criteria (references stranske/Doc-Lineage#28 as reproduction only). Out of D4 issue-AC scope. | — |
| Deliverable-Render | #20 | #5 | VERIFIED | `src/deliverable_render/docx/memo.py`, CLI `render-docx-memo`, fixtures under `tests/fixtures/stores/`, and `tests/docx/test_change_memo_renderer.py` / `test_continuity_memo_renderer.py` assert T1 sections and continuity slices. PR records deliberate T1-skip fail→restore. | — |
| Manager-Mosaic | #39 | — | EXCLUDED | Gate dependency-bootstrap alignment with Workflows#3480 template (`tests/test_gate_project_dependencies.py`). No linked issue; workflow-source-only infra repair. | — |
| Workflows | #3482 | — | EXCLUDED | Role-based Codex model routing across registry, reusable workflows, and consumer template with 122+ focused tests. `workflow:source-local-request`; no linked issue AC. | — |
| learning-management-system | #686 | #672 | VERIFIED | `_weighted` in `src/lms/maintenance/budget.py` validates every supplied tier count before blending; expanded parametrized guards in `tests/maintenance/test_tiers_horizon_budget.py` (117 passed locally). PR documents mutation revert check. | — |
| Workflows | #3483 | — | EXCLUDED | Pins nested repo-review Codex child to Astra High (`scripts/repo_review_round2_runner.py` + tests). Local-request PR; verifier skipped (zero source AC). | — |
| Workflows | #3484 | — | EXCLUDED | Maint 82 delivery wake scoping to owned repos (`sync_dependency_campaign.js` + contract tests). No linked issue. | — |
| Deliverable-Render | #25 | #6 | VERIFIED | `src/deliverable_render/store/validate.py` with orphan-ID, dollar-corruption, and evidence-object projection checks; fixtures and `tests/store/test_*`; PR records deliberate-break fail→restore for orphan and dollar gates. | — |
| Counter_Risk | #1077 | #1066 | PARTIAL | `_validate_pdf_distribution_config` in `src/counter_risk/pipeline/run.py` plus `test_pdf_request_with_distribution_disabled_is_explicit` with enabled/disabled controls. Squash diff is substantive. No executed deliberate-break fail→restore transcript in PR body (AC requires captured outcomes). | not filed (gh auth) |
| trip-planner | #1822 | — | EXCLUDED | Guided setup + readiness fix in `workspace_view_model.py` / `NewTripPage.tsx` with backend and frontend test gates. User-report direct PR; no `Closes #` fleet issue. | — |
| Workflows | #3486 | — | EXCLUDED | Canary review fixes in `scripts/runner_lib/core.py`, `scripts/validate_run_contract.py`, and contract docs with regression tests. References stranske/trip-planner#1823 only; no fleet issue AC. | — |
| Manager-Database | #1673 | #1673 | PARTIAL | Registers `ui/alerts` in `ui/app.py`, links dashboard badge (`ui/dashboard.py`), adds `tests/test_ui_navigation.py` coverage including synthetic API AppTest on Alerts. **Unmet:** issue AC requires browser smoke navigating Dashboard→Alerts (tests hit Alerts directly / badge href only); no deliberate-break removal transcript for navigation registration. | not filed (gh auth) |
| Workflows | #3490 | — | EXCLUDED | Scoped App-token routing for verifier follow-ups (`agents-verify-to-new-pr.yml` + `tests/workflows/test_verify_to_new_pr_token.py`). Review-followup of #3446; no linked issue AC. | — |
| Counter_Risk | #1079 | #1068 | PARTIAL | Concentration slide finalization before PDF export in `src/counter_risk/pipeline/run.py`; `test_final_concentration_slide_precedes_pdf_export` and disabled controls in diff. Missing executed deliberate-break ordering transcript per #1068 AC. | not filed (gh auth) |
| Counter_Risk | #1078 | #1067 | PARTIAL | Provenance hashing extended for `exposure_summary_xlsx` and external `screenshot_inputs` in `src/counter_risk/pipeline/run.py`; `test_optional_input_provenance_hashes` asserts SHA-256 changes. Missing executed deliberate-break enumeration transcript per #1067 AC. | not filed (gh auth) |
| Workflows | #3489 | — | EXCLUDED | Large keepalive authority replay guard (`keepalive_authority_state.js` + extensive JS tests). No `Closes #` fleet issue; operational follow-on to #3491/#3492 chain. | — |
| Manager-Database | #1674 | #1674 | PARTIAL | `inserted_news_items` dedupes pending URL/date identities in `etl/news_flow.py`; integration test asserts one stored row and `news_count=1` for intra-batch duplicates. Missing deliberate-break restore transcript per #1674 AC. | not filed (gh auth) |
| Doc-Lineage | #52 | #47 | VERIFIED | `MANIFEST.in` includes `tests/fixtures/fact_key_map/tracked_variables.json`; `tests/test_package_identity.py` packaging regression. Checked deliberate-break gate in issue/PR checklist. | — |
| Workflows | #3493 | #3492 | VERIFIED | `reopenUnconfirmedChallenge` and PR head/label revalidation in `keepalive_authority_state.js`; tests force interleaved head/label changes before ledger writes. Meets #3492 AC on stale-head trust and interleaving coverage. | — |
| Doc-Lineage | #53 | #48 | VERIFIED | `_iter_documents` rejects out-of-root symlinks before `compute_identity` in `src/doc_lineage/manifest.py`; symlink regression tests in `tests/test_identity_manifest.py`. | — |

**Result:** 7 VERIFIED, 5 PARTIAL, 0 NOT IMPLEMENTED, 8 EXCLUDED (no linked issue AC / infra-only).  
**Follow-ups filed:** none (`gh` not authenticated).  
**Deferred:** ~16 additional eligible PRs remain in the 36h window for the next D4 pass (oldest unverified after this batch).

Evidence: `artifacts/verification/evidence/D4-verify-merged-2026-09-21T03/`
