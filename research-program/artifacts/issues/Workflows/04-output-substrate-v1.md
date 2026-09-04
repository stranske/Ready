## Why

Hand-built HTML drifts across repos (B2-gap-analysis §1.1). Pension-Data's `apps/web/` is the embryonic standard (`clones/Pension-Data/apps/web/README.md:7-17` documents workspace bundle, drilldowns, PWA) but Workflows has no `output-substrate/v1` schema to generalize it. Verified: no `output-substrate` file under `clones/Workflows/docs/contracts/`. **Latent fragility:** each product reinvents renderer wiring.

## Scope

Define `output-substrate/v1` schema describing `renderer_profile`, `workspace_bundle_ref`, `manifest_csv_exports[]`, and link to `artifact-manifest/v1`.

## Non-Goals

- Do NOT extract Pension-Data `apps/web/` (B2-029 separate issue).
- Do NOT add Node/Evidence.dev renderer deps (B2-R15 reject).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Create `docs/contracts/schemas/output-substrate-v1.schema.json` with profiles `investment_review`, `blackline_bundle`, `mosaic_book` per R5 brief.
- [ ] Create `docs/contracts/output-substrate-v1.md` referencing Pension-Data `apps/contracts/runtime-contract.json` as exemplar.
- [ ] Add `tests/fixtures/backplane/valid_output_substrate.json`.
- [ ] Extend `artifact-manifest-v1.schema.json` `kind` enum with `output_substrate` (additive).
- [ ] Add `test_output_substrate_fixture_validates` in `tests/contracts/test_backplane_schemas.py`.
- [ ] Sync-manifest entries.

## Acceptance Criteria

- [ ] Named test: `tests/contracts/test_backplane_schemas.py::test_output_substrate_fixture_validates` passes.
- [ ] **Deliberate-break gate:** remove required `renderer_profile` from fixture → test **must FAIL** → revert.
- [ ] All existing `tests/contracts/test_backplane_schemas.py` parametrized schema-load tests still pass.

## Implementation Notes

Read `clones/Pension-Data/tests/web/test_workspace_contract.py:135` for workspace bundle shape constraints.

_Surfaced by B2-028; verified absent from Workflows contracts._
