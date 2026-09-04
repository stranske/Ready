## Why

DDQ extraction tests need synthetic fixtures (R6). Verified: `clones/Inv-Man-Intake/tests/fixtures/` has no `ddq_synthetic/` subtree (glob 2026-09-04) and `tests/intake/test_standard_element_library.py:1-20` only loads the bundled stub. **Missing behavior:** no ILPA DDQ golden packet for CI. **Depends on:** B2-010 ontology.

## Scope

`tests/fixtures/ddq_synthetic/` + loader for packet pipeline tests.

## Non-Goals

- Do NOT use real manager DDQ responses.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add synthetic DDQ JSON under `tests/fixtures/ddq_synthetic/`.
- [ ] Add `tests/intake/test_ddq_synthetic_fill.py` running packet pipeline.

## Acceptance Criteria

- [ ] Named test: `tests/intake/test_ddq_synthetic_fill.py::test_ddq_fields_extracted` passes.
- [ ] **Deliberate-break gate:** remove mandatory field from fixture → test **must FAIL** → revert.

_Surfaced by B2-040._
