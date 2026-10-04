# D4 implementation verification — 2026-09-27T03

**Window:** merged ≥ 2026-09-25T15:59:54Z (36h before run start)  
**Scope:** 20 oldest eligible issue-linked PRs not yet in this unit’s checkpoint. Template-sync, dependency/release chores, and `stranske/Orchestrator` excluded. Verdicts from squash diffs (`gh pr diff` via `with-gh-auth.sh`) and linked issue acceptance criteria; local re-runs where noted.

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| Manager-Database | #1728 | #1682 | PARTIAL | `DOCUMENT_TEST_POSTGRES_URL` + `document_association` pytest in `ci.yml` (`ae68cd2`). **Unmet:** deliberate-break RED/GREEN transcript for disabling `document_managers` insert. | [#1731](https://github.com/stranske/Manager-Database/issues/1731) |
| Doc-Lineage | #68 | #36 | VERIFIED | `docs/evidence/issue-36-ingest-manifest-sha256-deliberate-break.md` with FAIL/PASS for `test_ingest_writes_valid_manifest`. | — |
| Workflows | #3584 | #3457 | PARTIAL | maint-77→maint-78 dispatch job, `refresh_model_eval_candidates` merge, `test_auto_dispatch_maint77_chains_to_maint78_on_catalog_drift` in diff (`b4c0862`); local `-k auto_dispatch` pass. **Unmet:** deliberate-break transcript removing dispatch step. | [#3594](https://github.com/stranske/Workflows/issues/3594) |
| Ready | #597 | #581 | VERIFIED | Evidence doc with RED/GREEN for `test_ingest_schema_files_includes_capability_bundle`. | — |
| Ready | #598 | #582 | VERIFIED | Evidence doc with RED/GREEN for `test_format_similarity_non_finite_scores_return_safe_fallback`. | — |
| Manager-Mosaic | #71 | #32 | VERIFIED | `docs/evidence/issue-32-evaluate-claim-deliberate-break.md` with RED/GREEN for thesis `min` gate test. | — |
| Doc-Lineage | #69 | #37 | VERIFIED | Evidence doc with RED/GREEN for `test_mixed_pdf_recognizes_only_missing_text_layer_page`. | — |
| Trend_Model_Project | #6062 | #6046 | VERIFIED | Evidence doc with RED/GREEN for `test_lambda_tc_rejects_non_finite`. | — |
| Trend_Model_Project | #6063 | #6047 | VERIFIED | Evidence doc with RED/GREEN for `test_run_from_config_rejects_invalid_regime_turnover_cap`. | — |
| Trend_Model_Project | #6064 | #6048 | VERIFIED | Evidence doc with RED/GREEN for `test_regime_control_values_reject_non_finite_and_string_boolean`. | — |
| Trend_Model_Project | #6065 | #6054 | VERIFIED | Non-finite guards on `CostModelSettings._validate_cost` + `test_cost_model_rejects_non_finite_values`; PR body records deliberate-break fail/pass counts. | — |
| Trend_Model_Project | #6066 | #6055 | VERIFIED | `RiskSettings._validate_floor` finite guard + `test_risk_settings_reject_non_finite_floor_vol` / `test_infinite_floor_vol_is_rejected_before_scaling`. | — |
| Counter_Risk | #1122 | #1106 | VERIFIED | `_format_deltas` iterates up to five movers; `test_format_deltas_lists_multiple_movers_per_variant` in diff; named test pass on `main`. | — |
| Counter_Risk | #1120 | #1110 | VERIFIED | Evidence doc + issue #1090 comment with RED/GREEN for CPRS-CH trend filename gate. | — |
| Counter_Risk | #1121 | #1111 | VERIFIED | Evidence doc + issue #1104 comment with RED/GREEN for `test_apply_repo_cash_syncs_notional_change_columns`. | — |
| Counter_Risk | #1123 | #1112 | VERIFIED | Historical banners in audit docs + `tests/docs/test_audit_log_historical.py::test_in_repo_audit_logs_marked_historical`. | — |
| Manager-Mosaic | #72 | #32 | VERIFIED | Second evidence file (`issue-32-thesis-eval-deliberate-break.md`) with RED/GREEN transcript (duplicate scope vs #71). | — |
| Counter_Risk | #1124 | #1073 | PARTIAL | Workbook regression moved into `tests/pipeline/test_reconciliation.py`; named coverage gate 24 passed locally (`d7701d6`). **Unmet:** literal deliberate-break FAIL output in PR/issue (narrative only). | [#1125](https://github.com/stranske/Counter_Risk/issues/1125) |
| Doc-Lineage | #70 | #38 | VERIFIED | Evidence doc with RED/GREEN for `test_pairs_by_section_id` semantic-only break. | — |
| Deliverable-Render | #57 | #37 | VERIFIED | `validate.py` `missing-entry-period` + named test in diff (`13c89b6`); issue `Reproduction:` no longer shows validate-pass/render-fail on tip; named pytest pass. | — |

**Result:** 17 VERIFIED, 3 PARTIAL, 0 NOT IMPLEMENTED, 0 belt-only ledger merges in batch.  
**Follow-ups filed:** 3 (Manager-Database #1731, Workflows #3594, Counter_Risk #1125).  
**Deferred:** 18 additional eligible PRs remain in the rolling 36h window for the next D4 pass.

Evidence: `artifacts/verification/evidence/D4-verify-merged-2026-09-27T03/`

**Confidence:** High on VERIFIED rows with production+test diffs or evidence files containing literal FAIL/PASS lines. High on PARTIAL rows (behavior landed; documentary AC gaps only). Medium on evidence-only PRs where transcripts were not independently re-executed this run (trusted diff content + spot local pytest on `Counter_Risk`, `Workflows`, `Deliverable-Render` clones).
