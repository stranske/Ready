# [P1] Workspace policy reload must treat pass status with blocking issues as non-compliant

## Why

`trip_planner/app/services/policy.py:266-288` maps `blocking_issues` into `failure_reasons` only inside the `elif imported.organization_context.policy_status == "fail"` branch. When persisted `organization_context.policy_status` is the explicit string `"pass"` but `blocking_issues` is non-empty, evaluation falls through to compliant paths. #1778 fixed missing or empty `policy_status` (see `tests/app/test_policy.py:206-253`) but not an explicit `"pass"` paired with stored blockers. Live TPP HTTP import can populate both fields (`trip_planner/integrations/tpp/client.py:915-919`).

## Scope

Reload evaluation in `trip_planner/app/services/policy.py` for persisted `PersistedPolicyState.organization_context`.

## Tasks

- [ ] Add `test_workspace_policy_reload_pass_status_with_blocking_issues_is_non_compliant` in `tests/app/test_policy.py` seeding `policy_status: "pass"` plus a blocking issue and asserting `policy_evaluation.status == "non_compliant"`.
- [ ] Update `trip_planner/app/services/policy.py` `_policy_evaluation_from_import` to treat any non-empty `blocking_issues` as non-compliant regardless of `policy_status`.
- [ ] Keep `trip_planner/app/services/policy.py` `_normalize_organization_context_payload` consistent with the evaluation rule above.

## Acceptance Criteria

- `pytest tests/app/test_policy.py::test_workspace_policy_reload_pass_status_with_blocking_issues_is_non_compliant` passes.
- `pytest tests/app/test_policy.py` passes.
- Deliberate-break → revert: temporarily restrict `blocking_issues` handling to the `policy_status == "fail"` branch in `trip_planner/app/services/policy.py` and confirm the new test fails; revert.

## Non-Goals

- Changing TPP HTTP fetch logic in `trip_planner/integrations/tpp/client.py`.
- Scaffold-only completion does NOT count: adding a comment without changing evaluation when `policy_status == "pass"` and `blocking_issues` is non-empty is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._
