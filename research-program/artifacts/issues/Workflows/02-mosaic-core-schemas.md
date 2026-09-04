## Why

Manager-Mosaic and thesis monitoring need a fleet wire format for cross-source facts and discrepancies (`artifacts/research/B2-gap-analysis.md` B2-015). Verified: no `mosaic` string appears in `clones/Workflows/docs/contracts/schemas/` (seven files, grep 2026-09-04). Verified: `config/backplane_participants.json` has no mosaic artifact kinds in `ingests` arrays (`clones/Workflows/config/backplane_participants.json:218-221` shows only `evidence-object/v1` and `identity-map-conventions` for LMS). **Missing behavior:** repos cannot emit conformant discrepancy objects.

## Scope

Add `docs/contracts/schemas/mosaic-core-v1.schema.json` with `Fact`, `Discrepancy`, `ThesisClaim`, `ThesisCheck` subtypes, spec markdown, fixtures, and extend `artifact-manifest-v1.schema.json` `kind` enum additively per B3 §5.3.

## Non-Goals

- Do NOT build Manager-Mosaic repo (separate issue B2-016).
- Do NOT add PROV/RDF or graph DB schemas (B2-R03 reject).
- Scaffold-only completion does NOT count: schema without fixture validation test is a failure.

## Tasks

- [ ] Create `docs/contracts/schemas/mosaic-core-v1.schema.json` with `schema_version` const `mosaic-core/v1` and discriminated subtypes per R3 brief.
- [ ] Create `docs/contracts/mosaic-core-v1.md` documenting `fact_key` join semantics to `tracked-variable/v1` `ontology_key`.
- [ ] Add `tests/fixtures/backplane/valid_mosaic_fact.json` and `valid_mosaic_discrepancy.json`.
- [ ] Extend `docs/contracts/schemas/artifact-manifest-v1.schema.json` `kind` enum with `tracked_variables`, `mosaic_bundle` (additive, non-breaking).
- [ ] Add `test_mosaic_core_fixture_validates` to `tests/contracts/test_backplane_schemas.py`.
- [ ] Append sync-manifest entries for schema + spec.

## Acceptance Criteria

- [ ] Named test: `tests/contracts/test_backplane_schemas.py::test_mosaic_core_fixture_validates` passes.
- [ ] **Deliberate-break gate:** set `fact_key` to empty string in `valid_mosaic_fact.json` → named test **must FAIL** → revert.
- [ ] Existing `tests/contracts/test_backplane_schemas.py::test_manifest_path_rejects_traversal` still passes (no regression on manifest schema).

## Implementation Notes

Run: `python -m pytest tests/contracts/test_backplane_schemas.py -q` before and after.

_Surfaced by B2-015; verified no mosaic schemas in Workflows checkout._
