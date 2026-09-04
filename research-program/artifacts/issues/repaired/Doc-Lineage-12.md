## Why

R6 requires deterministic mutations for CI ground truth without proprietary docs. Verified: `tests/test_main.py:1-33` is the only functional test module — no `tests/mutations/` directory. **Missing behavior:** no labeled mutation pairs for diff gates.

## Scope

`tests/mutations/` generator applying labeled edits to synthetic LPA fixtures.

## Non-Goals

- Do NOT use real manager documents.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `tools/generate_mutations.py` producing paired before/after JSON segment trees.
- [ ] Add `tests/mutations/test_mutation_pair_known_diff.py` asserting expected change classes.
- [ ] Add `tests/blackline/test_mutation_pairs.py` wiring mutation pairs to blackline diff (depends on B2-005).

## Acceptance Criteria

- [ ] Named test: `tests/mutations/test_mutation_pair_known_diff.py::test_gate_provision_change_detected` passes.
- [ ] **Deliberate-break gate:** skip one mutation → test **must FAIL** → revert.

## Implementation Notes

Mutation pairs feed the clause blackline engine in B2-005.

_Surfaced by B2-008._
