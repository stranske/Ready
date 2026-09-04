## Why

Largest provenance gap in fleet: `evidence_refs` are page-pointer strings, not evidence IDs (`src/inv_man_intake/run.py:113-118` builds `document:{id}#page={n}` strings). Dossier confirms no conformant emitter (`dossier-out/DOSSIER.md:56`). **Depends on:** B2-015.

## Scope

Write standalone `evidence-object/v1` JSON files per extracted field; point `evidence_refs` at `evidence_id` values.

## Non-Goals

- Do NOT change scoring/threshold logic in run pipeline.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/inv_man_intake/emit/evidence_objects.py` validating against `docs/contracts/schemas/evidence-object-v1.schema.json`.
- [ ] Update `run.py:113-118` to emit sorted `evidence_id` list.
- [ ] Add `tests/emit/test_evidence_object_emitter.py`.
- [ ] Extend `scripts/validate_run_contract.py` to validate emitted evidence files.

## Acceptance Criteria

- [ ] Named test: `tests/emit/test_evidence_object_emitter.py::test_run_evidence_refs_are_evidence_ids` passes.
- [ ] **Deliberate-break gate:** revert `run.py` to page-pointer strings → test **must FAIL** → revert.

_Surfaced by B2-017; verified at run.py:113-118._
