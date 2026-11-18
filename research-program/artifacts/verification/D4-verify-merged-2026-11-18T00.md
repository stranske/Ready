# D4 verify merged — 2026-11-18T00 (attempt 1)

**Window:** merges on/after `2026-11-16T12:00:00Z` (~36h before run). **Repos:** `SUPPORTED_REPOS` minus Orchestrator. **Cap:** 20 PRs (oldest first among eligible; chore template-sync and `*bootstrap for #*` excluded from queue). **GitHub writes:** none (offload read-only); follow-ups not filed.

**Rate limit:** none (stopping after 20).

**Ledger:** 20 verified; **~55** additional eligible merges remain in-window for the next run (same filters).

## Summary

| Verdict | Count |
|---------|------:|
| VERIFIED | 16 |
| PARTIAL | 3 |
| NOT IMPLEMENTED | 0 |
| DOC / no issue AC (accepted) | 1 |

One **belt ledger** in window (`Ready#690`) was not in the oldest-20 slice.

## Results

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| Workflows | [4712](https://github.com/stranske/Workflows/pull/4712) | [#4454](https://github.com/stranske/Workflows/issues/4454) (body ref) | VERIFIED | — | no (offload) |
| Manager-Mosaic | [156](https://github.com/stranske/Manager-Mosaic/pull/156) | [#155](https://github.com/stranske/Manager-Mosaic/issues/155) | VERIFIED | — | no (offload) |
| Workflows | [4717](https://github.com/stranske/Workflows/pull/4717) | — (docs; cites Orchestrator#1407 as example only) | DOC | — | no |
| Pension-Data | [1033](https://github.com/stranske/Pension-Data/pull/1033) | [#1031](https://github.com/stranske/Pension-Data/issues/1031) | VERIFIED | — | no (offload) |
| Ready | [685](https://github.com/stranske/Ready/pull/685) | [#683](https://github.com/stranske/Ready/issues/683) | VERIFIED | — | no (offload) |
| trip-planner | [2040](https://github.com/stranske/trip-planner/pull/2040) | [#2038](https://github.com/stranske/trip-planner/issues/2038) | PARTIAL | Issue AC: regenerated `#2037` Python 3.14 check green; next sync-core round clears `pin-conflict` (explicitly deferred/human). Diff satisfies local pin alignment + `test_cross_repo_dev_pins`. | no (offload) |
| Workflows | [4723](https://github.com/stranske/Workflows/pull/4723) | [#4696](https://github.com/stranske/Workflows/issues/4696) (context) | VERIFIED | Docs-only: `templates/consumer-repo/AGENTS.md` gains “Lanes On This Repository”. | no (offload) |
| Workflows | [4722](https://github.com/stranske/Workflows/pull/4722) | — (PR-owned fix) | VERIFIED | `requested-model` fallback in `reusable-codex-run.yml`; `test_codex_requested_model_falls_back_to_the_configured_model` in diff. | no (offload) |
| Doc-Lineage | [187](https://github.com/stranske/Doc-Lineage/pull/187) | [#185](https://github.com/stranske/Doc-Lineage/issues/185) | VERIFIED | `section-id/v2`, inline heading split, unassigned preamble; named + preamble tests in diff. | no (offload) |
| Workflows | [4724](https://github.com/stranske/Workflows/pull/4724) | [#4688](https://github.com/stranske/Workflows/issues/4688) | VERIFIED | Blocking `acceptance-criteria-label` in `summary` needs; removes `continue-on-error` on label apply (root + consumer template); gate drift tests updated. | no (offload) |
| Manager-Database | [1929](https://github.com/stranske/Manager-Database/pull/1929) | [#1923](https://github.com/stranske/Manager-Database/issues/1923) | VERIFIED | `emit_news_spike_alerts` stable identity + `test_news_producer_retry_preserves_delivery_identity`. | no (offload) |
| Workflows | [4725](https://github.com/stranske/Workflows/pull/4725) | — (maint-46; PR-owned) | VERIFIED | `trackedGateContext` preserves prototype getters; `maint-post-ci.test.js` regression. | no (offload) |
| Counter_Risk | [1258](https://github.com/stranske/Counter_Risk/pull/1258) | [#1252](https://github.com/stranske/Counter_Risk/issues/1252) | VERIFIED | `input_hashes` includes auto-discovered `cash_overrides_*`; `test_optional_input_provenance_hashes_implicit_cash_override`. | no (offload) |
| Counter_Risk | [1257](https://github.com/stranske/Counter_Risk/pull/1257) | [#1251](https://github.com/stranske/Counter_Risk/issues/1251) | VERIFIED | `test_unreadable_distribution_ppt_fails_output_generation` + pipeline fail-closed path. | no (offload) |
| Manager-Database | [1932](https://github.com/stranske/Manager-Database/pull/1932) | [#1926](https://github.com/stranske/Manager-Database/issues/1926) | VERIFIED | Default `conviction_flow` runs dispatch; `test_default_entry_point_runs_detection_and_dispatch`. | no (offload) |
| Doc-Lineage | [188](https://github.com/stranske/Doc-Lineage/pull/188) | [#186](https://github.com/stranske/Doc-Lineage/issues/186) | VERIFIED | `test_ocr_tesseract_smoke.py::test_default_backend_recovers_image_only_pdf` + CI `real_tesseract` job wiring. | no (offload) |
| Counter_Risk | [1259](https://github.com/stranske/Counter_Risk/pull/1259) | [#1254](https://github.com/stranske/Counter_Risk/issues/1254) | PARTIAL | Squash diff is CI repair only (monkeypatch signature for `class_breakdown_sources`). Issue AC landed in [#1255](https://github.com/stranske/Counter_Risk/pull/1255) (merged earlier same window, not in this ledger batch). | no (offload) |
| Counter_Risk | [1256](https://github.com/stranske/Counter_Risk/pull/1256) | [#1253](https://github.com/stranske/Counter_Risk/issues/1253) | VERIFIED | `dates.py` / conflict detection; `test_inferred_as_of_mismatch_with_identified_sources_is_conflict` + deliberate-break evidence files. | no (offload) |
| Workflows | [4726](https://github.com/stranske/Workflows/pull/4726) | [#4718](https://github.com/stranske/Workflows/issues/4718) | VERIFIED | Concurrency group scoped to `inputs.pr_number`; `test_reusable_concurrency_group_is_scoped_to_target_pr`. | no (offload) |
| Manager-Database | [1934](https://github.com/stranske/Manager-Database/pull/1934) | [#1925](https://github.com/stranske/Manager-Database/issues/1925) | VERIFIED | Alembic provenance columns + `test_persisted_positions_record_source_provenance`. | no (offload) |

## Notes

- **Ready#685:** diff includes unrelated binary touch under `research-program/artifacts/audits/...` (demo XLSX). Acceptance work is in `check_publication_safety.py`, `prepare_publication.py`, and named parametrized guard test; not treated as scaffold.
- **Reproduction blocks:** no linked issue in this batch carried a `Reproduction:` block requiring re-run on merged tip.
- **Belt (#Workflows#3391):** no ledger-only merges among these 20.
- **Confidence:** high on diff-vs-named-test alignment; medium on trip-planner post-merge sync criteria (not observable in this offload).

**Stopped:** ledger full (20/20). **Next run:** resume from checkpoint; oldest unverified in-window merges continue (e.g. `learning-management-system#842`, `Ready#690`, remaining Workflows merges after 4730).