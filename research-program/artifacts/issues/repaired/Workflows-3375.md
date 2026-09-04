## Why

Work PC has Excel preinstalled; tabular manifest export avoids WASM renderer deps (B2-gap-analysis §4). `output-substrate/v1` (issue 04) will define renderer profiles but no CSV export slice exists yet. Verified: `stranske/Pension-Data` at `apps/web/README.md:11` mentions "Filtered export to JSON or CSV" for the web app only — not a fleet manifest contract. **Depends on:** Workflows issue 04 (`output-substrate-v1`).

## Scope

Extend `output-substrate-v1.schema.json` with `manifest_csv_exports[]` (column spec, filename, encoding) and document Excel refresh workflow in spec.

## Non-Goals

- Do NOT build COM/Office add-in (Track C module 25 deferred).
- Do NOT change Pension-Data web export code in this issue.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `manifest_csv_exports` array property to `docs/contracts/schemas/output-substrate-v1.schema.json` with required `columns[]` (`name`, `type`, `source_path`).
- [ ] Document work-PC refresh steps in `docs/contracts/output-substrate-v1.md` §Excel lane.
- [ ] Add `tests/fixtures/backplane/valid_output_substrate_with_csv.json`.
- [ ] Add `test_output_substrate_csv_export_validates` in `tests/contracts/test_backplane_schemas.py`.

## Acceptance Criteria

- [ ] Named test: `tests/contracts/test_backplane_schemas.py::test_output_substrate_csv_export_validates` passes.
- [ ] **Deliberate-break gate:** set a column `type` to invalid enum value → test **must FAIL** → revert.

## Implementation Notes

Blocked on filing until Workflows `04-output-substrate-v1` merges.

_Surfaced by B2-032; depends on B2-028._
