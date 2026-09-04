## Why

The work-environment response pins Doc-Lineage's build order as identity → extraction → ledger schemas → **lineage and comparison engine** ([INFORMATION-REQUEST-RESPONSE.md §D, consultant-report comparison tool; §Scope fixed 2026-09-04](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). Verified: `README.md:30` states that sequence explicitly, but `tests/test_main.py:23-27` is the only functional test module and exercises template `add()` — no `src/doc_lineage/compare.py`, no segment classifier, no supersession resolver, no synthetic evaluation corpus. The consultant tracker already names the segment vocabulary (`VERBATIM / NEAR_VERBATIM / REVISED / NEW / DROPPED`) and materiality tiers (`T1` decision-relevant, `T2` factual refresh, `T3` cosmetic) as **data fields**, not ad hoc branches ([response §D, consultant-report comparison tool](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). The communication synthesis tool documents a costly failure mode: inferring an exit from document silence produced a wrong finding — **silence is weak evidence, never proof of removal** ([response §D, communication synthesis tool](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). **Latent fragility, not a current break:** issues #2–#4 define prerequisites; this issue delivers the engine they feed.

## Scope

Implement the comparison/lineage engine in Doc-Lineage after #2 (identity), #3 (extraction), and #4 (ledger schemas):

1. Segment classification into `VERBATIM`, `NEAR_VERBATIM`, `REVISED`, `NEW`, `DROPPED` with `T1`/`T2`/`T3` tiers loaded from versioned data files (not `if tier == "T1"` code branches).
2. Document-family detection and supersession chains (filename-prefix supersession from Q9, content-hash identity from #2).
3. A **silence-is-weak-evidence** invariant: absence of a mention must never auto-emit `DROPPED` or an exit inference without an explicit positive signal.
4. A synthetic corpus generator with labeled ground truth so the engine can be evaluated in CI without proprietary documents.

## Non-Goals

- Do NOT implement HTML/Word/PPTX rendering (Deliverable-Render owns outputs).
- Do NOT re-implement PDF extraction or OCR (depends on #3).
- Do NOT invent new ledger field names (depends on #4 schemas).
- Scaffold-only completion does NOT count: a green `pytest` run that collected **0** of the named comparison/lineage tests is a failure. The deliberate-break acceptance criteria below must be demonstrated.

## Tasks

- [ ] Add `data/segment_tiers.json` defining `T1`/`T2`/`T3` tier metadata and `data/segment_classes.json` defining the five segment classes; load both from `src/doc_lineage/compare/classify.py` (create module) — no hardcoded tier branch tables in Python.
- [ ] Add `src/doc_lineage/compare/classify.py` with `classify_segment(pair: SegmentPair, *, tiers: TierCatalog, classes: ClassCatalog) -> ClassifiedSegment` reading tier/class definitions from the data files above.
- [ ] Add `src/doc_lineage/lineage/families.py` with `detect_family(doc: DocumentRef) -> FamilyId` and `build_supersession_chain(docs: Sequence[DocumentRef]) -> list[SupersessionEdge]` using content-hash identity from #2 and numeric-prefix supersession heuristics described in [response §C Q9](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).
- [ ] Add `src/doc_lineage/compare/silence.py` with `apply_silence_invariant(classified: ClassifiedSegment, *, prior_mentions: int) -> ClassifiedSegment` that refuses to map bare absence to `DROPPED` (returns `UNKNOWN_ABSENCE` or leaves unclassified per schema).
- [ ] Add `tools/generate_synthetic_corpus.py` writing paired before/after segment trees under `tests/fixtures/synthetic_corpus/` with a `ground_truth.json` manifest labeling expected segment classes and tiers.
- [ ] Add `tests/compare/test_segment_classification.py`, `tests/lineage/test_supersession_chain.py`, `tests/compare/test_silence_invariant.py`, and `tests/synthetic_corpus/test_ground_truth_replay.py` wired to the generator output.
- [ ] Perform the deliberate-break verification in Acceptance Criteria, capture FAIL output, then revert before requesting review.

## Acceptance Criteria

- [ ] Named test: `tests/compare/test_segment_classification.py::test_tier_labels_loaded_from_data_not_branches` passes — asserts `T2` label text comes from `data/segment_tiers.json`, not a Python literal.
- [ ] Named test: `tests/compare/test_silence_invariant.py::test_absence_does_not_emit_dropped` passes — a segment present in the prior doc but missing in the current doc without an explicit removal signal must not classify as `DROPPED`.
- [ ] Named test: `tests/synthetic_corpus/test_ground_truth_replay.py::test_replay_matches_ground_truth_manifest` passes on the generator-produced corpus with non-zero cases.
- [ ] **Deliberate-break gate:** temporarily edit `src/doc_lineage/compare/silence.py` so `apply_silence_invariant` returns `change_type="DROPPED"` when `prior_mentions > 0` and the current mention count is zero. With this change, `tests/compare/test_silence_invariant.py::test_absence_does_not_emit_dropped` **must FAIL**. Revert the edit after capturing the failure.
- [ ] **Deliberate-break gate:** temporarily delete the `T3` entry from `data/segment_tiers.json`. `tests/compare/test_segment_classification.py::test_tier_labels_loaded_from_data_not_branches` **must FAIL**. Restore the entry after capturing the failure.

## Implementation Notes

- Ground segment/tier vocabulary in the consultant tracker field list from [response §D](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) (`change_type`, `tier` columns).
- Confirmed-green local reproduction from repo root (scaffold baseline): `python -m pytest tests/test_main.py -q` → passes today; new modules must add non-zero collection counts for the named test files above.
- Depends on Doc-Lineage #2, #3, #4.
