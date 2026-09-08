## Why

The LLM trace-control API endpoint accepts arbitrary client-specified `actor_id` values and does not enforce authentication or learner ownership authorization (`src/lms/llm/api.py:657-686`). `control_llm_trace_route` (`POST /llm/sessions/{session_id}/trace-control`) accepts `payload: LLMTraceControlRequest` and checks only `if llm_session.learner_id != payload.actor_id: raise HTTPException(404)`. The route omits `CurrentUserDep` and `SettingsDep` and never validates that the authenticated caller matches `payload.actor_id` or owns the session. In deployed auth mode (`settings.auth_required = True`), an authenticated learner Alice can supply `actor_id = <bob_learner_id>` and trigger `action: "forget"` on Bob's private LLM session, wiping Bob's `response_summary` and modifying trace retention states. This is a verified **current break** and authorization bypass vulnerability.

## Scope

Inject `CurrentUserDep` and `SettingsDep` into `control_llm_trace_route` in `src/lms/llm/api.py`. Call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=llm_session.learner_id)` and verify that `payload.actor_id` matches the authenticated learner identity. Add regression tests in `tests/api/test_deployed_learner_ownership.py`.

## Non-Goals

- Do NOT modify the trace control transition state machine in `src/lms/llm/trace_controls.py`.
- Do NOT modify session creation or prompt execution routes in `src/lms/llm/api.py`.
- Scaffold-only completion does NOT count: modifying the route signature without calling `require_learner_ownership` or without adding test assertions verifying foreign session trace control rejection is a failure of this issue.

## Tasks

- [ ] In `src/lms/llm/api.py`, import `CurrentUserDep`, `SettingsDep`, and `require_learner_ownership` from `src/lms/auth/dependencies.py`.
- [ ] In `src/lms/llm/api.py`, update `control_llm_trace_route` signature to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=llm_session.learner_id)`.
- [ ] In `src/lms/llm/api.py`, verify that `payload.actor_id` matches the authenticated `current_user.learner_id` when authentication is enabled.
- [ ] In `tests/api/test_deployed_learner_ownership.py`, add test `test_control_llm_trace_foreign_learner_rejected` verifying that attempting trace control on another learner's session returns HTTP 404 when authentication is enabled.

## Acceptance Criteria

- [ ] The named test `pytest tests/api/test_deployed_learner_ownership.py -k "test_control_llm_trace_foreign_learner_rejected"` passes with 0 failures, asserting HTTP 404 when an authenticated user attempts trace control on a foreign LLM session.
- [ ] **Deliberate-break gate:** In `src/lms/llm/api.py:666`, remove the `require_learner_ownership` call in `control_llm_trace_route`. Running `pytest tests/api/test_deployed_learner_ownership.py -k "test_control_llm_trace_foreign_learner_rejected"` MUST fail (receiving HTTP 200 instead of HTTP 404). Revert the edit after capturing the failure.
- [ ] Existing deployed learner ownership tests pass via `pytest tests/api/test_deployed_learner_ownership.py`.

## Implementation Notes

- Follow the ownership enforcement pattern established across `tests/api/test_deployed_learner_ownership.py:50-120`.
- Confirmed-green test runner: `pytest tests/api/test_deployed_learner_ownership.py`
