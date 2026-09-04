## Why

Manager-Mosaic discrepancy engine consumes `fact_key` joins (B2-gap-analysis B2-020). Verified: `clones/Workflows/config/backplane_participants.json:236-238` excludes trip-planner from backplane; no Doc-Lineage participant entry emits `tracked_variable_refs`. **Missing behavior:** no `fact_key_map` export artifact. **Depends on:** B2-002, B2-015.

## Scope

Emit `artifact:fact_key_map.json` mapping `variable_id` → `ontology_key` + `entity_ref`.

## Non-Goals

- Do NOT build Manager-Mosaic importer here.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/doc_lineage/export/fact_key_map.py`.
- [ ] Add `tests/export/test_fact_key_map.py`.

## Acceptance Criteria

- [ ] Named test: `tests/export/test_fact_key_map.py::test_map_joins_on_ontology_key` passes.
- [ ] **Deliberate-break gate:** drop `entity_ref` from one entry → test **must FAIL** → revert.

_Surfaced by B2-020._
