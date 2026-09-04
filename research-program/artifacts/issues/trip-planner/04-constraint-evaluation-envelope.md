## Why

Epic #519 option contracts need constraint envelope on bundles (candidates.jsonl B2-048 prereq). Verified: `clones/trip-planner/docs/contracts/source-adapters.md:14` documents `NormalizationHandoff` but `grep -r constraint_evaluation clones/trip-planner` returns no matches in source or tests. **Missing behavior:** inventory bundles lack `constraint_evaluation` block.

## Scope

Add `constraint_evaluation` block to inventory bundle schema and emitter.

## Non-Goals

- Do NOT change TPP policy engine internals.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Extend bundle schema under `docs/contracts/`.
- [ ] Update `app/services/inventory.py` emitter.
- [ ] Add `tests/contracts/test_constraint_evaluation.py`.

## Acceptance Criteria

- [ ] Named test: `tests/contracts/test_constraint_evaluation.py::test_bundle_includes_evaluation` passes.
- [ ] **Deliberate-break gate:** omit block → test **must FAIL** → revert.

_Surfaced by B2-048._
