## Why

Pension-Data has richest internal evidence (`build_evidence_reference` at `src/pension_data/extract/common/evidence.py:89-96`) but dossier notes no standalone `evidence-object/v1` files at manifest boundary. **Depends on:** B2-015.

## Scope

Project internal `EvidenceReference` to `evidence-object/v1` files; publish `identity-map/v1` for pension/fund/manager tokens per B3 §6.1.

## Non-Goals

- Do NOT change internal DB schema.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/pension_data/emit/evidence_object.py` mapping from `build_evidence_reference`.
- [ ] Add `src/pension_data/emit/identity_map.py` per B3 §1.5 sketch.
- [ ] Wire into `backplane_emitter.py` manifest output.
- [ ] Add `tests/emit/test_evidence_object_files.py` and `tests/emit/test_identity_map_export.py`.

## Acceptance Criteria

- [ ] Named test: `tests/emit/test_evidence_object_files.py::test_emitted_file_validates` passes.
- [ ] **Deliberate-break gate:** omit `excerpt` in emitter → test **must FAIL** → revert.

_Surfaced by B2-018; verified evidence.py:89._
