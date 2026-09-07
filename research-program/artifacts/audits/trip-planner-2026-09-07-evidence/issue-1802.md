# [P1] Proposal submission must read policy context from public workspace policy_state

## Why

`frontend/src/lib/proposalSubmission.ts:65-84` resolves `organizationId` and `constraintSetId` only from `workspace.view_model.debug_state.sections.policy_state.payload`. Default workspace responses omit debug sections and strip identifiers (`trip_planner/app/services/workspace.py:1815-1818`, `1847-1854`; `tests/app/test_workspace.py:3437-3438`). `buildProposalSubmissionPayload` then throws `Policy context is not available for this workspace` at `frontend/src/lib/proposalSubmission.ts:108-110` on normal loads even when policy preview renders.

## Scope

Frontend proposal submission context resolution and any minimal backend fields needed on the public workspace payload.

## Tasks

- [ ] Add a frontend unit test in `frontend/src/lib/proposalSubmission.test.ts` covering a non-debug workspace payload with public `policy_state` identifiers.
- [ ] Update `frontend/src/lib/proposalSubmission.ts` `readPolicyContext` to read `organization_id` and `constraint_set.policy_id` from `workspace.policy_state` before falling back to debug sections.
- [ ] If required identifiers are intentionally redacted, expose submission-safe `organization_id` and `policy_id` on the public workspace payload in `trip_planner/app/services/workspace.py` `_public_workspace_policy_state`.

## Acceptance Criteria

- `npm test -- proposalSubmission` passes including the new non-debug policy-context case.
- `pytest tests/app/test_workspace.py::test_workspace_response_filters_business_policy_proposal_diagnostics_by_default` still passes after any backend shape change.
- Deliberate-break → revert: restore debug-only lookup in `frontend/src/lib/proposalSubmission.ts` and confirm the new test fails; revert.

## Non-Goals

- Removing all policy redaction from public workspace responses.
- Scaffold-only completion does NOT count: documenting that users must append `?debug=true` instead of fixing submission on default loads is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._
