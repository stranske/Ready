## Why

Consultant report sections need fleet `ontology_key` values aligned to B2-003. Verified: `docs/contracts/standard_element_library.md:12` requires bundled `_stub.json` keep `non_authoritative: true`; `src/inv_man_intake/intake/standard_elements.py:1-30` loads stub only with no consultant section keys.

## Scope

Extend stub data with `report.consultant_review` element keys mapping to `consultant.*` ontology keys; conformance tests.

## Non-Goals

- Do NOT set `non_authoritative: false` on bundled stub without external library.
- Do NOT emit `tracked-variable/v1` yet (B2-017).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `data/consultant_sections.json` with ≥15 section keys per R2 brief.
- [ ] Extend `standard_elements.py` to load consultant sections when `doc_type` is `report.consultant_review`.
- [ ] Add `tests/intake/test_consultant_section_ontology.py`.
- [ ] Map keys in README cross-reference to Workflows `tracked-variable/v1` (after sync).

## Acceptance Criteria

- [ ] Named test: `tests/intake/test_consultant_section_ontology.py::test_sections_resolve_without_code_change` passes (data-only add).
- [ ] **Deliberate-break gate:** remove one key from JSON → test **must FAIL** → revert.

_Surfaced by B2-010; depends on Workflows B2-003._
