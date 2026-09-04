## Why

The communication synthesis tool in the work environment documents two silent data-corruption modes that pass syntactic validation: (1) a single mistyped internal ID makes an entire record vanish from the rendered view with no error; (2) a shell text-substitution on the structured data file corrupted a `$36B` figure to `B` while leaving the file syntactically valid ([INFORMATION-REQUEST-RESPONSE.md §D, communication synthesis tool](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). Deliverable-Render's README allocates `render/store` as the structured-store contract (`README.md:17`) and requires fleet evidence-object interoperability (`README.md:24-26`). Verified: `scripts/validate_run_contract.py:1-18` validates run-contract envelopes only — no structured-store semantic validator exists; `render/` is absent (`README.md:16-21` vs checkout). **Missing behavior:** no validator catches orphan IDs or shell-substitution dollar corruption; store fields are not aligned to `docs/contracts/schemas/evidence-object-v1.schema.json:8-15` required keys. **Latent fragility.**

## Scope

Implement `render/store` validation and align the structured-store contract with Workflows `evidence-object/v1` so stores produced by work tools render without a translation step ([response Appendix §1 item 1 and §3](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)).

## Non-Goals

- Do NOT implement HTML/PPTX/DOCX renderers in this issue.
- Do NOT add server-side validation endpoints.
- Scaffold-only completion does NOT count: a validator that only checks JSON Schema syntax but misses orphan-ID vanish or `$`-corruption cases is a failure. Both deliberate-break gates below must be demonstrated.

## Tasks

- [ ] Create `src/deliverable_render/store/schema.py` documenting required top-level keys (`fund`, `periods`, `entries`, `themes`, `documents`, `gaps`) mirroring [response §D, communication synthesis tool](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) field names.
- [ ] Create `src/deliverable_render/store/validate.py` with `validate_store(path: Path) -> ValidationReport` checking: (a) every `entries[].id` referenced from `mentions` resolves; (b) no `$`-only remnants in string fields that look like corrupted currency (`\$?\d` → lone letter); (c) each evidence pointer can project to `evidence-object/v1` required fields per `docs/contracts/schemas/evidence-object-v1.schema.json:8-15`.
- [ ] Add `scripts/validate_structured_store.py` CLI (wire in `pyproject.toml` `[project.scripts]` as `validate-structured-store`) exiting non-zero on semantic violations.
- [ ] Add `tests/store/test_orphan_id_detection.py` with fixture `tests/fixtures/stores/orphan_entry_id.json`.
- [ ] Add `tests/store/test_dollar_substitution_corruption.py` with fixture `tests/fixtures/stores/corrupted_dollar_amount.json` (contains `B` where `$36B` was expected).
- [ ] Add `tests/store/test_evidence_object_projection.py` asserting store evidence pointers validate against `evidence-object-v1.schema.json`.
- [ ] Perform deliberate-break verification (see Acceptance Criteria), capture FAIL output, then revert.

## Acceptance Criteria

- [ ] Named test: `tests/store/test_orphan_id_detection.py::test_mistyped_entry_id_fails_validation` passes — validator reports the orphan reference and exits non-zero via CLI.
- [ ] Named test: `tests/store/test_dollar_substitution_corruption.py::test_shell_substitution_corruption_fails_validation` passes — `$36B`→`B` corruption is flagged even though JSON parses.
- [ ] Named test: `tests/store/test_evidence_object_projection.py::test_store_evidence_projects_to_schema` passes against `docs/contracts/schemas/evidence-object-v1.schema.json`.
- [ ] **Deliberate-break gate:** temporarily comment out the orphan-ID cross-reference check in `src/deliverable_render/store/validate.py`. `tests/store/test_orphan_id_detection.py::test_mistyped_entry_id_fails_validation` **must FAIL**. Revert after capturing the failure.
- [ ] **Deliberate-break gate:** temporarily disable the dollar-corruption heuristic in `validate.py`. `tests/store/test_dollar_substitution_corruption.py::test_shell_substitution_corruption_fails_validation` **must FAIL**. Revert after capturing the failure.

## Implementation Notes

- Failure modes sourced from [response §D, communication synthesis tool](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).
- Reuse `jsonschema.Draft202012Validator` pattern from `scripts/validate_run_contract.py:30` for evidence-object projection.
- Confirmed-green local reproduction (scaffold baseline): `python -m pytest tests/test_main.py -q` → passes today.
