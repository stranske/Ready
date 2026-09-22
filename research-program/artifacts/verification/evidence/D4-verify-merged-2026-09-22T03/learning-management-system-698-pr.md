# PR #698

<!-- pr-preamble:start -->
<!-- meta:issue:690 -->
> **Source:** Issue #690

Closes #690

<!-- pr-preamble:end -->

<!-- auto-status-summary:start -->
## Automated Status Summary
#### Scope
`list_misconception_patterns` applies SQL `LIMIT` before its Python-side signature filter, so matching patterns outside the newest `limit` rows cannot be found. Its signature branch also lacks the `MisconceptionPattern.id` tiebreaker used by the sibling branch, causing nondeterministic results for equal `created_at` values.

#### Tasks
- [x] Update `src/lms/feedback/repository.py:501-507` to remove SQL-side `.limit(limit)` from the `signature_text` branch and apply `islice` after the Python signature filter.
- [x] Add `MisconceptionPattern.id` as the secondary sort key in the `signature_text` branch to match `src/lms/feedback/repository.py:515-517`.
- [x] Import `islice` from `itertools` in `src/lms/feedback/repository.py` if not already imported.
- [x] Add `test_oldest_matching_pattern_survives_limit` to `tests/feedback/test_misconception_patterns.py` with more patterns than `limit` and an oldest matching pattern.
- [x] Add `test_signature_branch_ordering_is_deterministic` to `tests/feedback/test_misconception_patterns.py` for patterns sharing `created_at`.

#### Acceptance criteria
- [x] `tests/feedback/test_misconception_patterns.py::test_oldest_matching_pattern_survives_limit` seeds 5 non-matching patterns plus 1 matching pattern created first, calls `list_misconception_patterns(..., signature_text=..., limit=3)`, and returns the matching pattern ID.
- [x] `tests/feedback/test_misconception_patterns.py::test_signature_branch_ordering_is_deterministic` seeds patterns sharing one `created_at` and verifies two calls return the same ID order.
- [x] Restoring SQL-side `.limit(limit)` in the `signature_text` branch causes `test_oldest_matching_pattern_survives_limit` to fail; reverting it makes `uv run pytest tests/feedback/test_misconception_patterns.py -q` pass.
- [x] `uv run pytest tests/feedback -q` passes with no new failures.
- [x] `tests/feedback/test_misconception_patterns.py::test_pattern_matches_wrong_answer_signature` passes unmodified.

<!-- auto-status-summary:end -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

- **Bug Fixes**
  - Corrected misconception-pattern filtering so result limits are applied after matching entries are selected.
  - Matching results are now ordered consistently by creation time and ID, ensuring older matching patterns are retained and ties produce deterministic results.

- **Tests**
  - Added coverage for filtering, limit behavior, and deterministic ordering of matching patterns.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->