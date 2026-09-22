# PR #697

<!-- pr-preamble:start -->
<!-- meta:issue:689 -->
> **Source:** Issue #689

Closes #689

<!-- pr-preamble:end -->

<!-- auto-status-summary:start -->
## Automated Status Summary
#### Scope
`get_or_seed_card_state` performs a check-then-insert against the unique `ux_review_card_states_learner_subject` index at `src/lms/scheduling/models.py:396-403` without recovering the losing writer. Concurrent first attempts for the same learner and knowledge node can raise `IntegrityError`, return HTTP 500, and fail to record the attempt. The sibling `get_or_create_review_policy` helper already implements the required savepoint-and-requery pattern.

<!-- Updated WORKFLOW_OUTPUTS.md context:start -->
## Context for Agent

### Related Issues/PRs
- [#666](https://github.com/stranske/learning-management-system/issues/666)
<!-- Updated WORKFLOW_OUTPUTS.md context:end -->

#### Tasks
- [x] Update `src/lms/scheduling/card_state.py` to wrap `session.add(state)` and `session.flush()` at lines 74-75 in `session.begin_nested()`, mirroring `get_or_create_review_policy`.
- [x] Add `sqlalchemy.exc.IntegrityError` handling that re-runs `get_card_state` with the same learner and subject arguments and returns the winning row.
- [x] Apply the existing `retention_tier` reconciliation from `src/lms/scheduling/card_state.py:53-55` to the re-queried winning row.
- [x] Re-raise the original `IntegrityError` if the re-query returns `None`.
- [x] Add `tests/scheduling/test_card_state.py` with a deterministic concurrent-insert regression test using a second `Session` between the initial lookup and flush.

#### Acceptance criteria
- [x] `tests/scheduling/test_card_state.py::test_concurrent_first_seed_returns_winning_row` commits a competing `ReviewCardState` with the same `(learner_id, subject_type, subject_id)` after the initial lookup and before flush, and asserts `get_or_seed_card_state` returns the winning row ID without raising.
- [x] `tests/scheduling/test_card_state.py::test_seed_still_raises_on_unrelated_integrity_error` verifies a non-learner/subject uniqueness `IntegrityError` propagates.
- [x] Removing `begin_nested()` and the `IntegrityError` handler causes `uv run pytest tests/scheduling/test_card_state.py -q` to fail `test_concurrent_first_seed_returns_winning_row` with `IntegrityError`; restoring them makes both tests pass.
- [x] `uv run pytest tests/scheduling -q` passes with no new failures.
- [x] The existing `tests/scheduling/test_review_policies.py` concurrency test passes unmodified.

<!-- auto-status-summary:end -->
