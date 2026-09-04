## Why

Workflows DESIGN positions `stranske_pdf_extract` as fleet PDF contract; Doc-Lineage must emit conformant `evidence-object/v1` at manifest boundary (B2-gap-analysis B2-004). Verified: `clones/Doc-Lineage/docs/contracts/schemas/evidence-object-v1.schema.json:18` requires `schema_version` const `evidence-object/v1`, but `clones/Doc-Lineage/src/my_project/__init__.py:1-5` exports only template stubs — no `emit/` module. **Latent fragility:** ingest cannot produce attributable facts. **Depends on:** B2-003 (Workflows), B2-002 M1.

## Scope

Adapter from segment spans to standalone `evidence-object/v1` JSON files referenced in run manifest.

## Non-Goals

- Do NOT fork `stranske_pdf_extract` — consume as dependency.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/doc_lineage/emit/evidence.py` with `emit_evidence_object(span, ...) -> dict` validating against `docs/contracts/schemas/evidence-object-v1.schema.json`.
- [ ] Integrate into ingest pipeline after segmentation (`ingest.py`).
- [ ] Add `tests/emit/test_evidence_object.py` using `tests/contracts/test_backplane_schemas.py` pattern from Workflows.
- [ ] Ensure `method` and `excerpt` required per schema lines 70-75 in synced evidence schema.

## Acceptance Criteria

- [ ] Named test: `tests/emit/test_evidence_object.py::test_emitted_evidence_validates_against_schema` passes.
- [ ] **Deliberate-break gate:** omit `excerpt` key in emitter → test **must FAIL** → revert.

_Surfaced by B2-004._
