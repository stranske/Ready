## Why

The UI routes for viewing feedback records, revealing hints, revealing model answers, and submitting revision requests do not enforce learner ownership authorization (`src/lms/ui/feedback.py:80-184`). When deployed in multi-user environments with authentication enabled (`settings.auth_required = True`), `learner_feedback_detail_route`, `learner_hint_reveal_route`, `learner_model_answer_reveal_route`, and `learner_revision_submit_route` look up `FeedbackRecord` by ID from the database but never verify that `record.learner_id` matches the authenticated learner (`current_user`). Any authenticated user can view another learner's private diagnostic feedback, trigger hint and model answer reveals on their behalf, and submit forged revision requests. This is a verified **current break** and authorization bypass vulnerability across the feedback UI surface.

## Scope

Inject `CurrentUserDep` and `SettingsDep` into `learner_feedback_detail_route`, `learner_hint_reveal_route`, `learner_model_answer_reveal_route`, and `learner_revision_submit_route` in `src/lms/ui/feedback.py`. Call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=record.learner_id)` before rendering details or mutating records. Add regression tests in `tests/ui/test_feedback_surface.py`.

## Non-Goals

- Do NOT modify the core feedback scoring logic in `src/lms/feedback/scoring.py`.
- Do NOT modify the learner ownership authorization logic in `src/lms/auth/dependencies.py`.
- Scaffold-only completion does NOT count: adding dependency parameters to route signatures without invoking `require_learner_ownership` or without adding test assertions verifying HTTP 404 on cross-learner access is a failure of this issue.

## Tasks

- [ ] In `src/lms/ui/feedback.py`, import `CurrentUserDep`, `SettingsDep`, and `require_learner_ownership` from `src/lms/auth/dependencies.py`.
- [ ] In `src/lms/ui/feedback.py`, update `learner_feedback_detail_route` to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=record.learner_id)` after loading the feedback record.
- [ ] In `src/lms/ui/feedback.py`, update `learner_hint_reveal_route`, `learner_model_answer_reveal_route`, and `learner_revision_submit_route` to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=record.learner_id)` prior to executing reveals or submitting revisions.
- [ ] In `tests/ui/test_feedback_surface.py`, add test `test_feedback_surface_rejects_foreign_learner_access` asserting that accessing or mutating another learner's feedback record returns HTTP 404 when authentication is enabled.

## Acceptance Criteria

- [ ] The named test `pytest tests/ui/test_feedback_surface.py -k "test_feedback_surface_rejects_foreign_learner_access"` passes with 0 failures, asserting HTTP 404 responses for unauthorized learners across feedback detail, hint reveal, model answer reveal, and revision submit routes.
- [ ] **Deliberate-break gate:** In `src/lms/ui/feedback.py:85`, comment out the `require_learner_ownership` check in `learner_feedback_detail_route`. Running `pytest tests/ui/test_feedback_surface.py -k "test_feedback_surface_rejects_foreign_learner_access"` MUST fail with an assertion failure (receiving HTTP 200 instead of HTTP 404). Revert the edit after capturing the failure.
- [ ] Existing feedback surface tests pass via `pytest tests/ui/test_feedback_surface.py`.

## Implementation Notes

- Use `require_learner_ownership` from `src/lms/auth/dependencies.py:100`, which raises `HTTPException(status_code=404, detail="Feedback record not found")` on ownership mismatch to prevent learner ID enumeration.
- Confirmed-green test runner: `pytest tests/ui/test_feedback_surface.py`
