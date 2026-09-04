## Why

R6 requires deterministic mutations for CI ground truth without proprietary docs. Verified: `clones/Doc-Lineage/tests/test_main.py:1-33` is the only functional test module — no `tests/mutations/` directory. **Missing behavior:** no labeled mutation pairs for diff gates.

## Scope

`tests/mutations/` generator applying labeled edits to synthetic LPA fixtures.

## Non-Goals

- Do NOT use real manager documents.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `tools/generate_mutations.py` producing paired before/after JSON segment trees.
- [ ] Add `tests/mutations/test_mutation_pair_known_diff.py` asserting expected change classes.
- [ ] Wire mutation pairs into blackline tests (B2-005).

## Acceptance Criteria

- [ ] Named test: `tests/mutations/test_mutation_pair_known_diff.py::test_gate_provision_change_detected` passes.
- [ ] **Deliberate-break gate:** skip one mutation → test **must FAIL** → revert.

_Surfaced by B2-008._
