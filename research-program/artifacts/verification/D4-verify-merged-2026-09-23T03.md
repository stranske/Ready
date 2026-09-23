# D4 implementation verification — 2026-09-23T03

**Window:** merged ≥ 2026-09-21T15:20:00Z (36h before run start)  
**Scope:** 20 oldest eligible issue-linked PRs not verified in `D4-verify-merged-2026-09-22T03` (52 remained in window). Template-sync, dependency/release chores, and `stranske/Orchestrator` excluded. Verdicts from squash diffs (`gh pr diff` / REST v3 diff where GraphQL throttled) and linked issue acceptance criteria; PR bodies checked for deliberate-break transcripts.

**Method note:** GraphQL (`gh pr view`) hit a short-lived user rate limit mid-run; resumed with REST (`gh api` + `Accept: application/vnd.github.v3.diff`). Reproduction blocks on #1708/#1715 were not re-executed locally (no shallow clones in `[LOCAL_WORKSPACE]/`); named gate tests in the squash diffs satisfy the behavioral AC.

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| Counter_Risk | #1102 | #1089 | VERIFIED | `src/counter_risk/pipeline/manifest.py` marks distribution PPT `failed` when master generation fails; `test_build_ppt_outputs_marks_distribution_failed_when_ppt_status_failed` + success control in diff. PR body includes pytest deliberate-break transcript. | — |
| Manager-Database | #1703 | #1696 | VERIFIED | Cascade delete via `services/manager_deletion.py`, schema/ETL hooks, and `test_delete_manager_cascades_related_records` (+ storage/retry/fence tests). PR documents fail→restore on single-row delete. | — |
| Counter_Risk | #1103 | #1090 | PARTIAL | `src/counter_risk/parsers/cprs_ch.py` prefers Trend variant; `test_parse_cprs_ch_trend_workbook_not_misclassified_when_filename_contains_all` in diff. **Unmet:** no pasted pytest output for deliberate-break restore of `"all" in title` precedence (checkbox/claim only). | [#1110](https://github.com/stranske/Counter_Risk/issues/1110) |
| Deliverable-Render | #34 | #28 | PARTIAL | Unknown memo tier rejected in `src/deliverable_render/store/__init__.py`; CLI/validation tests in `tests/docx/test_validation_and_cli.py`. **Unmet:** deliberate-break transcript for removing tier-membership check. | [#44](https://github.com/stranske/Deliverable-Render/issues/44) |
| Manager-Database | #1704 | #1698 | VERIFIED | `api/managers.py` applies search/name filters; `test_list_managers_search_and_name_filters` + Postgres predicate test. PR includes deliberate-break transcript. | — |
| Manager-Database | #1705 | #1699 | VERIFIED | `api/signals.py` rejects non-finite `min_conviction_pct`; named API tests. PR includes deliberate-break transcript. | — |
| Deliverable-Render | #35 | #32 | PARTIAL | Duplicate document identity scan in `src/deliverable_render/store/validate.py` with three discriminating tests. **Unmet:** deliberate-break transcript for removing duplicate scan. | [#45](https://github.com/stranske/Deliverable-Render/issues/45) |
| learning-management-system | #709 | #695 | PARTIAL | Runtime honors `LLM_DEFAULT_PROVIDER` via `src/lms/llm/config.py` / `client.py`; `test_explicit_provider_override_is_honored` and rejection test; `config/README.md` documents JSON ownership boundary. **Unmet:** executed deliberate-break transcript for reverting override wiring (issue AC). | [#717](https://github.com/stranske/learning-management-system/issues/717) |
| Counter_Risk | #1107 | #1104 | PARTIAL | `apply_repo_cash_to_totals` syncs `notional_change`/`NotionalChange` and asserts manifest `top_changes` ordering in `test_apply_repo_cash_syncs_notional_change_columns`. **Unmet:** deliberate-break transcript for removing `NotionalChange` assignment. | [#1111](https://github.com/stranske/Counter_Risk/issues/1111) |
| Manager-Database | #1710 | #1706 | VERIFIED | `alerts/engine.py` + `ui/alerts.py` align `new_filing` rule keys with EDGAR events; integration/UI tests including `test_new_filing_ui_condition_matches_edgar_event`. PR includes deliberate-break transcript. | — |
| Manager-Database | #1711 | #1707 | VERIFIED | `api/alerts.py` scopes acknowledge-all to inbox filters; API + UI tests. PR includes deliberate-break transcript. | — |
| Manager-Database | #1712 | #1708 | PARTIAL | SQLite bootstrap path enforces CIK uniqueness (`test_create_manager_rejects_duplicate_cik_on_sqlite_bootstrap` + normalization/race tests). **Unmet:** deliberate-break transcript for skipping uniqueness guard. | [#1721](https://github.com/stranske/Manager-Database/issues/1721) |
| Manager-Database | #1713 | #1709 | VERIFIED | Bulk import rolls back on mid-batch failure (`test_bulk_import_rolls_back_on_mid_batch_failure` + Postgres transaction tests). PR includes deliberate-break transcript. | — |
| Workflows | #3478 | #1836 | EXCLUDED | Deliberate-break pytest isolation in `scripts/check_deliberate_break.py` + consumer template sync. Campaign queue #1836 is not a fleet issue with product AC; infra maintenance (same class as prior D4 EXCLUDED Workflows rows). | — |
| trip-planner | #1828 | #1731 | VERIFIED | Policy sync + proposal submission wiring (`trip_planner/app/routes/policy.py`, `proposal.py`, `WorkspacePage.tsx`) with backend/frontend tests covering `/proposal` submission path. PR documents deliberate-break/gate evidence for submission flow. | — |
| trip-planner | #1834 | — | EXCLUDED | E2E canary selector updates only (`frontend/e2e/two-trip-canary.spec.ts`). No linked fleet issue with acceptance criteria (REST linked #1828 PR record, not a product issue). | — |
| Manager-Database | #1718 | #1715 | PARTIAL | Postgres `search_documents` joins managers on document owner in `embeddings.py`; `test_search_documents_postgres_manager_join_uses_document_owner`. **Unmet:** deliberate-break transcript restoring filter-literal join. Core function MDB-4 not re-scored (no local clone). | [#1722](https://github.com/stranske/Manager-Database/issues/1722) |
| Manager-Database | #1719 | #1716 | VERIFIED | `alerts/engine.py` fires `large_delta` net rules for buy/sell; `test_large_delta_net_rule_matches_buy_and_sell_events`. PR includes deliberate-break transcript. | — |
| Workflows | #3503 | #3502 | VERIFIED | `scripts/check_deliberate_break.py` adds reviewed assertion replacement allowlist for Deliverable-Render #36; regression tests in `tests/scripts/test_check_deliberate_break.py`. Fixes false `test-assertion-tamper` on mandated assertion flip. | — |
| Deliverable-Render | #39 | #36 | VERIFIED | Evidence page validation in `src/deliverable_render/store/validate.py`; `test_validator_rejects_invalid_evidence_page_values`; gate workflow installs project deps before deliberate-break proof; helper tests updated. | — |

**Result:** 11 VERIFIED, 7 PARTIAL, 0 NOT IMPLEMENTED, 2 EXCLUDED.  
**Follow-ups filed:** 7 (deliberate-break transcript hygiene).  
**Deferred:** ~32 additional eligible PRs remain in the 36h window for the next D4 pass.

Evidence: `artifacts/verification/evidence/D4-verify-merged-2026-09-23T03/`

**Confidence:** High on VERIFIED rows (diff-backed behavior + named tests; transcript-backed where required). High that PARTIAL rows delivered real fixes; medium that missing transcripts were never run (vs. omitted from PR body only). Would upgrade PARTIAL→VERIFIED if pytest fail→restore logs are added to the linked issues.
