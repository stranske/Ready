# D4 implementation verification — 2026-09-24T03

**Window:** merged ≥ 2026-09-22T15:25:13Z (36h before run start)  
**Scope:** 20 oldest eligible issue-linked PRs not verified in prior D4 checkpoints (`D4-verify-merged-2026-09-23T03` and earlier). Template-sync, dependency/release chores, and `stranske/Orchestrator` excluded. Verdicts from squash diffs (`gh pr diff`) and linked issue acceptance criteria; PR bodies checked for deliberate-break transcripts.

**Method note:** No `Reproduction:` blocks on linked issues in this batch. Local clones not required for diff review; reproduction re-run N/A.

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| Doc-Lineage | #61 | #60 | VERIFIED | `Span.text_lines` through `extract/pdf.py`, `cache.py`, `models.py`; `tests/test_extract_lines.py` + README contract. PR includes pytest fail→restore transcript for `test_pdf_preserves_metric_lines_and_normalized_text`. | — |
| learning-management-system | #711 | #580 | PARTIAL | `scripts/export_offline_review_packet.py`, `tests/test_local_first_delivery.py`, `docs/development/local-first-delivery.md`, README link in diff. **Unmet:** no pasted output for `export_offline_review_packet.py … && test -s` gate; no deliberate-break FAIL transcript for empty HTML shell. | [#718](https://github.com/stranske/learning-management-system/issues/718) |
| Pension-Data | #907 | #878 | PARTIAL | `doc_lineage_backend.py`, `pdf_pipeline.py`, fixtures and `tests/parser/test_doc_lineage_backend.py` in diff. **Unmet:** deliberate-break transcript for forcing `enable_ocr=False` (issue AC). | [#919](https://github.com/stranske/Pension-Data/issues/919) |
| Workflows | #3508 | #3370 | PARTIAL | `TARGET_WORK_ENVIRONMENT.md` template, sync manifest, `tests/workflows/test_target_work_environment_template.py` in diff. **Unmet:** deliberate-break transcript removing hosting block section. | [#3532](https://github.com/stranske/Workflows/issues/3532) |
| Workflows | #3509 | #3375 | VERIFIED | `valid_output_substrate_with_csv.json`, `output-substrate-v1.md` docs, `test_output_substrate_csv_export_validates` in diff; PR documents deliberate-break on invalid column `type`. | — |
| Counter_Risk | #1109 | #1105 | VERIFIED | `_parse_float` / `_format_deltas` in `chat/session.py`; `test_format_deltas_omits_non_finite_notional_change` with deliberate-break transcript in PR body. | — |
| Deliverable-Render | #42 | #41 | VERIFIED | `validate.py` rejects `pub.src` without detail/state; `test_validator_rejects_pub_without_detail_or_state`; deliberate-break noted in PR. | — |
| learning-management-system | #714 | #712 | VERIFIED | Remediation clear path in scheduling/UI layers; `test_remediation_queue_item_can_be_cleared_after_failure` + deliberate-break transcript in PR. | — |
| Deliverable-Render | #43 | #40 | VERIFIED | Cross-entry `mentions[].entry_id` check in `validate.py`; `test_validator_rejects_cross_entry_mention_id`; deliberate-break in PR. | — |
| learning-management-system | #716 | #713 | VERIFIED | Revision acceptance schedules review queue via `feedback/repository.py`; `test_revision_acceptance_enqueues_review_queue_item`; deliberate-break verifier note in PR. | — |
| Workflows | #3520 | #3392 | PARTIAL | Provider `HAS_*` flags on `evaluateKeepaliveLoop` steps in keepalive + agents-81 templates; `test_evaluate_steps_export_every_provider_flag_the_loop_reads` in diff. **Unmet:** deliberate-break FAIL transcript (delete `HAS_CURSOR_AUTH`). | [#3533](https://github.com/stranske/Workflows/issues/3533) |
| Travel-Plan-Permission | #1590 | #1588 | PARTIAL | `published_budget_rules()` + snapshot fields; `tests/test_policy_snapshot_caps.py` (5 tests) in diff. **Unmet:** pasted pytest output for deliberate breaks (hard-code 5000 / publish nothing) — narrative only in PR. | [#1627](https://github.com/stranske/Travel-Plan-Permission/issues/1627) |
| trip-planner | #1854 | #1851, #1853 | VERIFIED | `dates.ts` calendar vs instant formatting; `database_status.py` + degraded `/api/health`; frontend/backend tests including `test_degraded_health_clears_when_the_database_comes_back`; gate table with break results in PR. | — |
| trip-planner | #1855 | #1840 | VERIFIED | Workspace header/next-step wiring in `workspace_view_model.py` / services; backend + frontend tests; gate table documents break→fail in PR. | — |
| trip-planner | #1856 | #1843 | VERIFIED | Budget tab UX (`TripPricesPanel`, `WorkspaceBudgetPanel`); vitest gates with deliberate-break rows in PR body. | — |
| Workflows | #3521 | #3517 | VERIFIED | `agent_delegation_policy.js` initial runner selection + tests; PR includes `node --test` and pytest transcript plus deliberate-break note. | — |
| Pension-Data | #908 | #879 | PARTIAL | `harvest/calpers_ic.py` + `tests/harvest/test_calpers_ic_offline.py::test_ic_items_parsed` in diff. **Unmet:** deliberate-break transcript (return zero items). | [#920](https://github.com/stranske/Pension-Data/issues/920) |
| Pension-Data | #909 | #880 | PARTIAL | `harvest/ncsr_sample.py` + `test_ncsr_fixture_ingests` and filing-date guards in diff. **Unmet:** deliberate-break transcript (skip filing date). | [#921](https://github.com/stranske/Pension-Data/issues/921) |
| Inv-Man-Intake | #981 | #949 | PARTIAL | `emit/evidence_objects.py`, `run.py` evidence_id refs, `validate_run_contract.py` extensions, `test_run_evidence_refs_are_evidence_ids` in diff. **Unmet:** deliberate-break transcript reverting to page-pointer strings. | [#985](https://github.com/stranske/Inv-Man-Intake/issues/985) |
| Pension-Data | #910 | #882 | PARTIAL | `packages/renderer-shell/` factored from `apps/web/`; `tests/renderer/test_shell_import_smoke.py` in diff. **Unmet:** deliberate-break transcript (external CDN script). | [#922](https://github.com/stranske/Pension-Data/issues/922) |

**Result:** 11 VERIFIED, 9 PARTIAL, 0 NOT IMPLEMENTED, 0 EXCLUDED.  
**Follow-ups filed:** 9 (deliberate-break transcript hygiene).  
**Deferred:** ~45 additional eligible PRs remain in the 36h window for the next D4 pass (releases, template-sync, and issue-less trip-planner rows excluded from this batch).

Evidence: `artifacts/verification/evidence/D4-verify-merged-2026-09-24T03/`

**Confidence:** High on VERIFIED rows (diff-backed behavior + named tests; transcript or gate table where required). High that PARTIAL rows delivered real fixes; medium that deliberate breaks were never run (vs. omitted from PR body only). Would upgrade PARTIAL→VERIFIED if fail→restore logs are added to the linked issues or PR threads.
