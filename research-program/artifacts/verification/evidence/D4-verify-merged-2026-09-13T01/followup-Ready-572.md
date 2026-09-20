## Why (verified evidence)

`stranske/Ready#572` merged the consumer-side capability-bundle registration for `#560`, but the issue requires a deliberate-break demonstration that is absent from the squash diff and PR body.

- `scripts/validate_run_contract.py` maps `capability-bundle/v1` in `INGEST_SCHEMA_FILES` and `_self_smoke` glob-loads every bundled schema (merge SHA `66f0b33e24842c5e97659d51feb9a4cf995f7b67`).
- `tests/test_main.py::test_ingest_schema_files_includes_capability_bundle` and `test_self_smoke_validates_all_schema_files` assert the mapping and smoke coverage.
- Issue `#560` requires removing the capability-bundle mapping, confirming `pytest tests/test_main.py` FAILS, reverting, and recording both outcomes in the PR.
- PR #572 leaves the deliberate-break acceptance checkbox unchecked and provides no RED/GREEN transcript; `test_ingest_schema_files_requires_capability_bundle_mapping` only asserts the mapping exists on green code.

## Tasks

- [ ] In a follow-up PR linked to `#560`, temporarily remove `capability-bundle/v1` from `INGEST_SCHEMA_FILES` in `scripts/validate_run_contract.py`.
- [ ] Run `pytest tests/test_main.py::test_ingest_schema_files_includes_capability_bundle -q` and capture failing output.
- [ ] Revert and capture passing output; paste both blocks in the PR body.

## Acceptance Criteria

- Named test: `tests/test_main.py::test_ingest_schema_files_includes_capability_bundle` passes on `main`.
- Deliberate-break → revert: remove `capability-bundle/v1` from `INGEST_SCHEMA_FILES` → confirm the named test FAILS → revert and confirm it passes. Paste RED and GREEN blocks in the PR.

## Non-Goals

- Do not change schema definitions under `docs/contracts/schemas/`.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-13T01; verified by reading squash diff for PR #572 at merge SHA `66f0b33e`._
