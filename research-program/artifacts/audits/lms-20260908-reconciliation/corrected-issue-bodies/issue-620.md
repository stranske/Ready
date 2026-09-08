## Why

The feedback detail and reveal/revision routes omit learner ownership checks. A synthetic authenticated foreign user received HTTP 200 and the private feedback goal from the detail route. This is a current break. The application already gates login in `src/lms/main.py`; the missing boundary is resource ownership. Evidence: `src/lms/ui/feedback.py:80`.

## Scope

Repair the demonstrated boundary in `src/lms/ui/feedback.py` and cover it in `tests/ui/test_feedback_surface.py`.

## Non-Goals

- Do not redesign unrelated subsystems or modify synced workflows.
- Scaffold-only completion does NOT count: editing signatures or adding a test that skips the demonstrated boundary is a failure of this issue.

## Tasks

- [ ] In `src/lms/ui/feedback.py`, Check the feedback learner before rendering or mutating any feedback detail, hint reveal, answer reveal, or revision. Use CurrentUserDep and require_learner_ownership from `src/lms/learners/identity.py` and SettingsDep from `src/lms/auth/login.py`.
- [ ] In `tests/ui/test_feedback_surface.py`, add `test_foreign_feedback_ui_is_rejected` with the demonstrated failing case and a valid-input control.

## Acceptance Criteria

- [ ] `pytest tests/ui/test_feedback_surface.py -k test_foreign_feedback_ui_is_rejected` passes and verifies the specified boundary and valid control.
- [ ] Deliberate-break gate in `src/lms/ui/feedback.py`: Temporarily remove the ownership check from the feedback detail route; the named test must fail because foreign access returns HTTP 200; restore the check. Run `pytest tests/ui/test_feedback_surface.py -k test_foreign_feedback_ui_is_rejected` for this proof.
- [ ] Existing tests in `tests/ui/test_feedback_surface.py` pass.

## Implementation Notes

- Existing CI is green at the audited commit; the new regression is prospective and has not been implemented.
- Test runner: `pytest tests/ui/test_feedback_surface.py`.
