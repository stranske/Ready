# D4-verify-merged-2026-09-18T02

**Window:** merged ≥ 2026-09-16T14:52:30Z (36h before run start)  
**Repos:** 15 lane fleet (`SUPPORTED_REPOS`, excluding Orchestrator)  
**Cap:** 20 PRs (8 verified this run)  
**Method:** Squash diffs from `git fetch` + local clones (`[LOCAL_WORKSPACE]/*/origin/main`); issue bodies from cached D4 evidence. `gh` unavailable (`GH_TOKEN` invalid) — could not run `gh pr diff` / `gh issue view` or file follow-ups.

## Summary

| Metric | Count |
|--------|------:|
| PRs verified | 8 |
| VERIFIED | 2 |
| PARTIAL | 6 |
| NOT IMPLEMENTED | 0 |
| Follow-ups filed this run | 0 |
| Follow-ups dedup (prior D4 run) | 5 |
| Follow-ups blocked (gh auth) | 1 |
| Rate-limit stop | No |

## Results

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| Manager-Mosaic | [#34](https://github.com/stranske/Manager-Mosaic/pull/34) | [#14](https://github.com/stranske/Manager-Mosaic/issues/14) | VERIFIED | — | — |
| Doc-Lineage | [#32](https://github.com/stranske/Doc-Lineage/pull/32) | [#8](https://github.com/stranske/Doc-Lineage/issues/8) | PARTIAL | Deliberate-break gate requires mutating `src/doc_lineage/ingest.py` sha256 path; PR body checks the box but squash diff has no production-mutation RED/GREEN transcript | dedup [#36](https://github.com/stranske/Doc-Lineage/issues/36) |
| Doc-Lineage | [#28](https://github.com/stranske/Doc-Lineage/pull/28) | [#3](https://github.com/stranske/Doc-Lineage/issues/3) | PARTIAL | Per-page OCR and coverage counts land; deliberate-break is test-local arithmetic in `test_deliberate_break_per_document_detection_violates_mixed_pdf_contract`, not a production mutation of `src/doc_lineage/extract/pdf.py` | dedup [#37](https://github.com/stranske/Doc-Lineage/issues/37) |
| Ready | [#572](https://github.com/stranske/Ready/pull/572) | [#560](https://github.com/stranske/Ready/issues/560) | PARTIAL | `capability-bundle/v1` map + glob `_self_smoke` land; issue-mandated deliberate-break (remove mapping → named test FAILS → revert) absent from squash diff | dedup [#581](https://github.com/stranske/Ready/issues/581) |
| Doc-Lineage | [#30](https://github.com/stranske/Doc-Lineage/pull/30) | [#7](https://github.com/stranske/Doc-Lineage/issues/7) | VERIFIED | — | — |
| Ready | [#577](https://github.com/stranske/Ready/pull/577) | [#561](https://github.com/stranske/Ready/issues/561) | PARTIAL | `math.isfinite` guard in `scripts/langchain/issue_dedup.py` + parametrized tests land; deliberate-break RED/GREEN transcript absent from squash diff | dedup [#582](https://github.com/stranske/Ready/issues/582) |
| Doc-Lineage | [#35](https://github.com/stranske/Doc-Lineage/pull/35) | [#10](https://github.com/stranske/Doc-Lineage/issues/10) | PARTIAL | `align_sections` + `manual_review` fail-closed land; deliberate-break uses test helper `_misaligned_pairs_for_test`, not production semantic-only path mutation | dedup [#38](https://github.com/stranske/Doc-Lineage/issues/38) |
| Ready | [#562](https://github.com/stranske/Ready/pull/562) | [#562](https://github.com/stranske/Ready/issues/562) | PARTIAL | `_coerce_confidence` / `_normalize_confidence` `math.isfinite` guards + integration test land; deliberate-break demonstration absent from squash diff and merge commit message | **not filed** (gh auth) |

## Skipped (not verified)

| Reason | Count | Examples |
|--------|------:|----------|
| Already verified in D4-verify-merged-2026-09-17T02 | 5 | Manager-Mosaic #25–#30 (issues #3,#9,#11–#13); Workflows #3452/#3458/#3460; Fine-Art-Archive #723 |
| Template-sync / infra chore (no issue AC) | 9 | Workflows #3464, Trend_Model_Project template sync, Manager-Database/Inv-Man-Intake/Pension-Data/learning-management-system/Deliverable-Render/Manager-Mosaic template sync, Doc-Lineage #31 |

## Notable findings

1. **Doc-Lineage burst (#28–#35)** — four substantive PRs deliver real ingest, extract, fixtures, and blackline modules with non-vacuous tests (39 named-gate tests pass locally). The recurring gap remains **deliberate-break transcript hygiene**, not scaffold-only delivery.
2. **Manager-Mosaic #34** — cleanest delivery this window: 20-key registry, packaged loader, three non-vacuous tests; PR body documents `fund.net_irr` removal break.
3. **Ready #562** — new since D4-verify-merged-2026-09-13T01; same deliberate-break gap pattern as #577/#561. Follow-up filing blocked by invalid `gh` credentials in this executor.
4. **gh auth** — executor cannot mutate GitHub; dedup against follow-ups filed ~1h earlier by D4-verify-merged-2026-09-13T01 for the six overlapping PARTIAL verdicts.

## Evidence

Squash diffs and cached issue bodies: `artifacts/verification/evidence/D4-verify-merged-2026-09-18T02/`

Local gate runs (`--no-cov` where coverage gate interferes):
- Manager-Mosaic: `pytest tests/test_fact_key_registry.py -q` → **3 passed**
- Doc-Lineage: `pytest tests/fixtures/test_public_corpus_manifest.py tests/ingest/test_ingest_synthetic_pdf.py tests/test_extract_coverage.py tests/blackline/test_section_id_pairing.py -q` → **39 passed**
- Ready: `pytest tests/test_main.py -q -k "similarity or capability or self_smoke or verdict_policy" --no-cov` → **9 passed**
