## Why

Tabular drilldown pattern proven in `apps/web/data/workspace.json` (`tests/web/test_workspace_contract.py:135`) but not emitted from ingest runs. **Depends on:** B2-029.

## Scope

Emit `workspace-bundle.json` from extraction runs with `data_origin: generated`.

## Non-Goals

- Do NOT change fixture demo bundle semantics for local dev.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/pension_data/export/workspace_bundle.py` matching `apps/contracts/runtime-contract.json`.
- [ ] Add `tests/export/test_workspace_bundle.py`.

## Acceptance Criteria

- [ ] Named test: `tests/export/test_workspace_bundle.py::test_bundle_matches_runtime_contract` passes.
- [ ] **Deliberate-break gate:** set invalid `data_origin` → test **must FAIL** → revert.

_Surfaced by B2-030._
