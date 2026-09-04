## Why

Manager-Mosaic discrepancy engine consumes `fact_key` joins (B2-gap-analysis B2-020). Verified: `README.md:5-6` confirms scaffold-only status; `stranske/Workflows` repo at `config/backplane_participants.json:236-238` has no Doc-Lineage participant entry emitting `tracked_variable_refs`. **Missing behavior:** no `fact_key_map` export artifact. **Depends on:** B2-002, B2-015.

## Scope

Emit a manifest artifact named `artifact:fact_key_map.json` (artifact name, not a repo path) mapping `variable_id` → `ontology_key` + `entity_ref`.

## Non-Goals

- Do NOT build Manager-Mosaic importer here.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/doc_lineage/export/fact_key_map.py`.
- [ ] Add `tests/export/test_fact_key_map.py`.

## Acceptance Criteria

- [ ] Named test: `tests/export/test_fact_key_map.py::test_map_joins_on_ontology_key` passes.
- [ ] **Deliberate-break gate:** drop `entity_ref` from one entry → test **must FAIL** → revert.

## Implementation Notes

Consumes `tracked-variable/v1` outputs from M1 ingest (B2-002) and mosaic schemas (B2-015).

_Surfaced by B2-020._
