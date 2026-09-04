## Why

Doc-Lineage README (`clones/Doc-Lineage/README.md:5-6`) states the repo is scaffold-only; no vocabulary data exists. R1 requires ~25 stable `ontology_key` values for cross-manager clause joins. Verified: `clones/Doc-Lineage/tests/test_main.py:1-35` only tests template `my_project` stubs — no `vocab/` directory. **Missing behavior:** no `legal.withdrawal.notice_days`-class keys for extraction or diff.

## Scope

Add `vocab/legal-clauses.json` with ~25 keys, conformance test, and README wire-up.

## Non-Goals

- Do NOT implement full M1 pipeline (B2-002).
- Do NOT commit proprietary LPAs — public/synthetic only per README:14.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Create `vocab/legal-clauses.json` with `schema_version`, `version`, `non_authoritative: false`, and `clauses` map (~25 keys seeded from ILPA/CUAD per B2 owner default).
- [ ] Create `tests/vocab/test_legal_clauses.py` asserting unique keys, dotted `ontology_key` pattern, and minimum count ≥ 20.
- [ ] Update `README.md:18` interoperability bullet to point at `vocab/legal-clauses.json`.
- [ ] Add loader `src/doc_lineage/vocab.py` with `load_legal_clauses() -> dict` (replace `my_project` package name in `pyproject.toml` if still template).

## Acceptance Criteria

- [ ] Named test: `tests/vocab/test_legal_clauses.py::test_legal_clauses_minimum_keys_and_unique` passes.
- [ ] **Deliberate-break gate:** duplicate two `ontology_key` values in JSON → named test **must FAIL** → revert.

## Implementation Notes

Mirror Inv-Man-Intake stub pattern at `docs/contracts/standard_element_library.md:9-13` for data-file vocabulary shape.

_Surfaced by B2-001; verified scaffold-only Doc-Lineage checkout._
