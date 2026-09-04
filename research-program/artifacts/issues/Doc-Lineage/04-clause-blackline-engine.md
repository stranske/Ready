## Why

R1 §1.3 requires section-ID alignment before semantic fallback. Verified: `clones/Doc-Lineage/README.md:9-12` promises blackline output but `clones/Doc-Lineage/tests/test_main.py:23-27` only tests template `add()` — no `blackline` module. **Missing behavior:** no section pairing. **Depends on:** M1 parse (B2-002), adopt sentweave (B2-013) for fallback.

## Scope

`doc_lineage/blackline.py` pairing sections by ID, emitting `lineage-edges/v1` NDJSON.

## Non-Goals

- Do NOT ship HTML renderer profile (B2-009 Tier 4).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/doc_lineage/blackline.py` with `align_sections(doc_a, doc_b) -> list[SectionPair]`.
- [ ] Add `tests/blackline/test_section_id_pairing.py` with synthetic mutation fixture.
- [ ] Fail closed to `manual_review` when header confidence < threshold (R2 objection mitigation).

## Acceptance Criteria

- [ ] Named test: `tests/blackline/test_section_id_pairing.py::test_pairs_by_section_id` passes on golden pair.
- [ ] **Deliberate-break gate:** force semantic-only path to pair wrong sections → test **must FAIL** → revert.

_Surfaced by B2-005._
