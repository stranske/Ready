## Why

Trace control compares the session learner only with client-supplied actor_id. A synthetic authenticated foreign caller supplied the victim learner ID and cleared the victim response summary with HTTP 200. This is a current break in ownership authorization. Login is already enforced globally in `src/lms/main.py`:93 and `src/lms/main.py`:121; anonymous access is not established. Evidence: `src/lms/llm/api.py:657`.

## Scope

Repair the demonstrated boundary in `src/lms/llm/api.py` and cover it in `tests/api/test_deployed_learner_ownership.py`.

## Non-Goals

- Do not redesign unrelated subsystems or modify synced workflows.
- Scaffold-only completion does NOT count: editing signatures or adding a test that skips the demonstrated boundary is a failure of this issue.

## Tasks

- [ ] In `src/lms/llm/api.py`, Resolve the authenticated user with CurrentUserDep and require_learner_ownership from `src/lms/learners/identity.py` and SettingsDep from `src/lms/auth/login.py`. Check session ownership and derive the audit actor from the authenticated learner in deployed mode. Preserve documented local-mode behavior.
- [ ] In `tests/api/test_deployed_learner_ownership.py`, add `test_foreign_trace_control_is_rejected` with the demonstrated failing case and a valid-input control.

## Acceptance Criteria

- [ ] `pytest tests/api/test_deployed_learner_ownership.py -k test_foreign_trace_control_is_rejected` passes and verifies the specified boundary and valid control.
- [ ] Deliberate-break gate in `src/lms/llm/api.py`: Temporarily remove all new authenticated identity checks from trace control while retaining the old payload equality check; the named test must fail with foreign HTTP 200; restore the checks. Run `pytest tests/api/test_deployed_learner_ownership.py -k test_foreign_trace_control_is_rejected` for this proof.
- [ ] Existing tests in `tests/api/test_deployed_learner_ownership.py` pass.

## Implementation Notes

- Existing CI is green at the audited commit; the new regression is prospective and has not been implemented.
- Test runner: `pytest tests/api/test_deployed_learner_ownership.py`.
