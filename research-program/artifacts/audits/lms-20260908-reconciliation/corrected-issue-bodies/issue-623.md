## Why

The criterion normalizer accepts NaN points because both relational bounds comparisons are false. A direct execution returned a normalized criterion containing NaN. This is a current validation break. End-to-end HTTP and PostgreSQL outcomes have not been established by this reconciliation. Evidence: `src/lms/feedback/scoring.py:233`.

## Scope

Repair the demonstrated boundary in `src/lms/feedback/scoring.py` and cover it in `tests/feedback/test_rubric_scoring.py`.

## Non-Goals

- Do not redesign unrelated subsystems or modify synced workflows.
- Scaffold-only completion does NOT count: editing signatures or adding a test that skips the demonstrated boundary is a failure of this issue.

## Tasks

- [ ] In `src/lms/feedback/scoring.py`, Reject non-finite and malformed criterion points with InvalidRubricScoringError in _normalize_criterion_scores, before comparison or persistence. The actual scoring entry point is score_attempt_with_rubric.
- [ ] In `tests/feedback/test_rubric_scoring.py`, add `test_rubric_nonfinite_points_are_rejected` with the demonstrated failing case and a valid-input control.

## Acceptance Criteria

- [ ] `pytest tests/feedback/test_rubric_scoring.py -k test_rubric_nonfinite_points_are_rejected` passes and verifies the specified boundary and valid control.
- [ ] Deliberate-break gate in `src/lms/feedback/scoring.py`: Temporarily remove the finite-number check; the named test must fail on NaN acceptance; restore the check. Run `pytest tests/feedback/test_rubric_scoring.py -k test_rubric_nonfinite_points_are_rejected` for this proof.
- [ ] Existing tests in `tests/feedback/test_rubric_scoring.py` pass.

## Implementation Notes

- Existing CI is green at the audited commit; the new regression is prospective and has not been implemented.
- Test runner: `pytest tests/feedback/test_rubric_scoring.py`.
