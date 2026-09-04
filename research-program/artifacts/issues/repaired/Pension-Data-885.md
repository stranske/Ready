## Why

Consultant vars should live beside actuarial facts — consume Doc-Lineage output, don't duplicate diff (R2 §6). Verified: `src/pension_data/extract/common/evidence.py:89-96` builds internal evidence refs but no `staging/` import module exists for external `tracked-variable/v1` files. **Depends on:** B2-002.

## Scope

Staging table/import for `tracked-variable/v1` JSON from Doc-Lineage runs.

## Non-Goals

- Do NOT implement diff engine inside Pension-Data.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/pension_data/staging/doc_lineage_vars.py`.
- [ ] Add `tests/staging/test_doc_lineage_import.py` with synthetic variable file.

## Acceptance Criteria

- [ ] Named test: `tests/staging/test_doc_lineage_import.py::test_variable_staged_with_entity_ref` passes.
- [ ] **Deliberate-break gate:** drop `ontology_key` → test **must FAIL** → revert.

_Surfaced by B2-044._
