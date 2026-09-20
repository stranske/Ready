# D4-verify-merged-2026-09-13T01

**Window:** merged ≥ 2026-09-16T12:56:26Z (36h before run start)  
**Repos:** 15 lane fleet (`SUPPORTED_REPOS`, excluding Orchestrator)  
**Cap:** 20 PRs (7 verified this run; 7 already adjudicated in prior D4 units; 9 chores/no-issue skips)

## Summary

| Metric | Count |
|--------|------:|
| PRs verified | 7 |
| VERIFIED | 2 |
| PARTIAL | 5 |
| NOT IMPLEMENTED | 0 |
| Follow-ups filed | 5 |
| Rate-limit stop | No |

## Results

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| Doc-Lineage | [#32](https://github.com/stranske/Doc-Lineage/pull/32) | [#8](https://github.com/stranske/Doc-Lineage/issues/8) | PARTIAL | Deliberate-break gate for manifest `sha256` in `src/doc_lineage/ingest.py` claimed in PR body but no production mutation RED/GREEN transcript | [#36](https://github.com/stranske/Doc-Lineage/issues/36) |
| Doc-Lineage | [#28](https://github.com/stranske/Doc-Lineage/pull/28) | [#3](https://github.com/stranske/Doc-Lineage/issues/3) | PARTIAL | Per-page OCR fallback implemented; deliberate-break documented via test-local comparison only, not by mutating `src/doc_lineage/extract/pdf.py` as issue requires | [#37](https://github.com/stranske/Doc-Lineage/issues/37) |
| Ready | [#572](https://github.com/stranske/Ready/pull/572) | [#560](https://github.com/stranske/Ready/issues/560) | PARTIAL | `capability-bundle/v1` mapping and glob `_self_smoke` land in diff; deliberate-break demonstration absent from PR body | [#581](https://github.com/stranske/Ready/issues/581) |
| Manager-Mosaic | [#34](https://github.com/stranske/Manager-Mosaic/pull/34) | [#14](https://github.com/stranske/Manager-Mosaic/issues/14) | VERIFIED | — | — |
| Doc-Lineage | [#30](https://github.com/stranske/Doc-Lineage/pull/30) | [#7](https://github.com/stranske/Doc-Lineage/issues/7) | VERIFIED | — | — |
| Ready | [#577](https://github.com/stranske/Ready/pull/577) | [#561](https://github.com/stranske/Ready/issues/561) | PARTIAL | `math.isfinite` guard and parametrized tests present; deliberate-break RED/GREEN transcript absent | [#582](https://github.com/stranske/Ready/issues/582) |
| Doc-Lineage | [#35](https://github.com/stranske/Doc-Lineage/pull/35) | [#10](https://github.com/stranske/Doc-Lineage/issues/10) | PARTIAL | Section-ID pairing and `manual_review` fail-closed behavior land; deliberate-break uses test helper `_misaligned_pairs_for_test` without production mutation evidence | [#38](https://github.com/stranske/Doc-Lineage/issues/38) |

## Skipped (not verified)

| Reason | Count | Examples |
|--------|------:|----------|
| Already verified in prior D4 units | 7 | Workflows #3452/#3458/#3460, Fine-Art-Archive #723, Manager-Mosaic #28/#29/#30 |
| Template-sync / dependency chore | 9 | Workflows #3464, Trend_Model_Project #6036, Manager-Database #1683, Inv-Man-Intake #972, Pension-Data #901, learning-management-system #677, Doc-Lineage #31, Deliverable-Render #21, Manager-Mosaic #26 |

## Notable findings

1. **Doc-Lineage burst (#28–#35)** — four substantive PRs in one window deliver real ingest, extract, fixtures, and blackline modules with non-vacuous tests. The recurring gap is deliberate-break transcript hygiene (same pattern as Manager-Mosaic #25/#30 in D4-verify-merged-2026-09-17T02).
2. **Manager-Mosaic #34** — clean delivery: 20-key registry, packaged copy, loader, synthetic-fixture coverage scan, and PR body documents the `fund.net_irr` break→revert cycle.
3. **Ready #572 + #577** — implementation is present and named gates pass locally; both lack the issue-mandated deliberate-break RED/GREEN blocks in the PR body.
4. **No belt-ledger-only merges** in the selected set; no Workflows#3391 ledger defects observed.

## Evidence

Squash diffs, issue JSON, and follow-up bodies: `artifacts/verification/evidence/D4-verify-merged-2026-09-13T01/`

Local gate runs (current `[LOCAL_WORKSPACE]/*/main` after `git pull`):
- Doc-Lineage: `pytest tests/ingest/test_ingest_synthetic_pdf.py::test_ingest_writes_valid_manifest tests/fixtures/test_public_corpus_manifest.py::test_manifest_has_calpers_entry tests/blackline/test_section_id_pairing.py::test_pairs_by_section_id tests/test_extract_coverage.py -q -o addopts=` → **15 passed**
- Ready: `pytest tests/test_main.py::test_ingest_schema_files_includes_capability_bundle tests/test_main.py::test_self_smoke_validates_all_schema_files tests/test_main.py::test_format_similarity_non_finite_scores_return_safe_fallback -q -o addopts=` → **5 passed**
- Manager-Mosaic: `pytest tests/test_fact_key_registry.py::test_fact_key_registry_contains_core_performance_and_liquidity_keys -q -o addopts=` → **1 passed**
