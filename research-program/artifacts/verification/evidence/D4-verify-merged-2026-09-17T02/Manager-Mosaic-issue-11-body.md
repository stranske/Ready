## Why (verified evidence)

Fleet contracts require every evidence link to carry `method` and a present `excerpt`, but this repo only copies the JSON Schema — there is no Python validator in the product package agents import.

- `docs/contracts/schemas/evidence-object-v1.schema.json:8-15` requires `schema_version`, `evidence_id`, `fact_ref`, `source_id`, `method`, and `excerpt`.
- `docs/contracts/schemas/evidence-object-v1.schema.json:50-53` states `excerpt` must be present (string or explicit null) — positional anchors alone are insufficient.
- `src/manager_mosaic/__init__.py:8-33` exports only scaffold helpers; no validation module exists under `src/manager_mosaic/`.
- README invariant 4 (`README.md:20-21`) requires one-click navigation from a fact to quotable evidence — validation is the gate before facts enter the mosaic index.

## Scope

Add a small, dependency-light validator module wrapping the checked-in schema. Complements #3 (store model) without implementing rendering or extraction.

## Tasks

- [ ] Add `src/manager_mosaic/evidence.py` with `validate_evidence_object(payload: dict) -> list[str]` returning all schema violations (empty list when valid) using `docs/contracts/schemas/evidence-object-v1.schema.json`.
- [ ] Reject objects whose `excerpt` key is absent entirely, mirroring the schema description at `evidence-object-v1.schema.json:50-53`.
- [ ] Export `validate_evidence_object` from `src/manager_mosaic/__init__.py`.
- [ ] Add `tests/test_evidence_validation.py::test_validate_evidence_object_reports_missing_excerpt_key` using the invalid fixture from #5 or an inline dict missing `excerpt`.

## Acceptance Criteria

- Named test: `tests/test_evidence_validation.py::test_validate_evidence_object_reports_missing_excerpt_key` passes under `pytest tests/test_evidence_validation.py`.
- Deliberate-break → revert: make `validate_evidence_object` return `[]` for a payload missing `excerpt` → confirm the named test FAILS → revert and confirm it passes.

## Non-Goals

- Do not implement PDF extraction or document identity (owned by Doc-Lineage).
- Do not emit run-contract envelopes (consumer role only).
- No scaffolding / TODO-only module stubs without the failing test above.

_Surfaced by repo-audit Track D 2026-09-05; verified by reading `evidence-object-v1.schema.json:8-15` and confirming no `src/manager_mosaic/evidence.py` on tip `02ffccf`._

