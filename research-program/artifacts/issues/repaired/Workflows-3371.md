## Why

R1/R2/R3 converge on one wire shape for clauses, consultant sections, and thesis claims (B3 interop architecture §3.1; grounding: [INFORMATION-REQUEST-RESPONSE.md](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) §D), but Workflows ships only the three backplane schemas today. Verified: `tests/contracts/test_backplane_schemas.py:17-21` parametrizes exactly `run-contract-v1`, `artifact-manifest-v1`, and `evidence-object-v1` — no `tracked-variable-v1.schema.json`. Verified: `docs/contracts/schemas/` contains seven JSON schemas and none named `tracked-variable-v1.schema.json`. **Latent fragility:** downstream Doc-Lineage and Inv-Man-Intake cannot validate extracted variables against a fleet-owned schema.

## Scope

Add `tracked-variable/v1` JSON Schema, normative spec markdown, golden fixtures under `tests/fixtures/backplane/`, validator hook in `scripts/validate_run_contract.py`, and sync-manifest entries per B3 §6.3. Include `clause-variable/v1` as a vocabulary-family alias documented in the spec (same wire shape, `ontology_family: "clause"`).

## Non-Goals

- Do NOT implement extractors in consumer repos (Doc-Lineage, Inv-Man-Intake) in this issue.
- Do NOT replace `evidence-object-v1.schema.json` — embed evidence per B3 §3.1.
- Scaffold-only completion does NOT count: landing schema files without `tests/contracts/test_backplane_schemas.py` coverage and a deliberate-break fixture is a failure of this issue.

## Tasks

- [ ] Create `docs/contracts/schemas/tracked-variable-v1.schema.json` with `schema_version` const `tracked-variable/v1`, required embedded `evidence` object conforming to `evidence-object/v1`, and dual `provenance.document` + `provenance.mirror` objects per B3 §3.1 sketch.
- [ ] Create `docs/contracts/tracked-variable-v1.md` normative spec cross-linking `docs/contracts/schemas/evidence-object-v1.schema.json:1-20`.
- [ ] Add `tests/fixtures/backplane/valid_tracked_variable.json` and `invalid_tracked_variable_missing_evidence.json` per B3 §6.2.
- [ ] Extend `tests/contracts/test_backplane_schemas.py:17-21` `SCHEMAS` dict to include `tracked-variable-v1.schema.json`.
- [ ] Add `test_tracked_variable_fixture_validates` in `tests/contracts/test_backplane_schemas.py` loading the golden fixture through `Draft202012Validator`.
- [ ] Append sync entries to `.github/sync-manifest.yml` for the new schema and spec (mirror existing `evidence-object-v1` entries around line 169 in `renovate-presets/consumer-managed-paths.json` pattern).
- [ ] Extend `scripts/validate_run_contract.py:48-52` schema map with `--tracked-variables` flag per B3 §6.2.

## Acceptance Criteria

- [ ] Named test: `tests/contracts/test_backplane_schemas.py::test_tracked_variable_fixture_validates` passes locally via `python -m pytest tests/contracts/test_backplane_schemas.py::test_tracked_variable_fixture_validates -q`.
- [ ] **Deliberate-break gate:** temporarily delete the `"evidence"` key from `tests/fixtures/backplane/valid_tracked_variable.json` → `test_tracked_variable_fixture_validates` **must FAIL** → restore the key.
- [ ] `python scripts/validate_run_contract.py --help` lists `--tracked-variables` and exits 0.

## Implementation Notes

Confirmed-green baseline: `python -m pytest tests/contracts/test_backplane_schemas.py -q` passes today with three schemas only.

_Surfaced by B2-003 / B3 §6.3; verified against Workflows checkout 2026-09-04._
