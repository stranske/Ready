# [P1] Bind approval history to the authenticated decision maker

## Why

Current break: a token for authenticated-approver can write an approval-history entry for forged-manager-id. `src/travel_plan_permission/http_service.py:2033` authenticates a manager decision, but `src/travel_plan_permission/http_service.py:2041` accepts actor_id from the form and `src/travel_plan_permission/http_service.py:2074` forwards it as the decision actor. The exception decision repeats this at `src/travel_plan_permission/http_service.py:2123`. The goal is an audit trail whose approving identity reflects the authenticated caller. This does not claim an unauthenticated approval; the attacker already has generic approve permission.

## Scope

Authenticated identity propagation for manager and exception approval/rejection histories and success audit events.

## Non-Goals

Changing role grants, exception tier policy or silently treating an arbitrary actor_id as delegation. Scaffold-only completion does NOT count: correcting a page label while persisted approval events retain the forged body identity is a failure of this issue.

## Tasks

- [ ] In `src/travel_plan_permission/http_service.py`, use auth_context.subject for manager and exception decision actor_id; reject conflicting supplied actor_id or remove it from the form contract.
- [ ] Update `src/travel_plan_permission/templates/manager_review_detail.html` and `src/travel_plan_permission/templates/portal_admin.html` so operator text cannot override the authenticated actor identity.
- [ ] Add `test_approval_actor_comes_from_token` to `tests/python/test_http_service.py`, covering mismatched form actor values on both decision routes and inspecting persisted history and audit events.

## Acceptance Criteria

- [ ] Run pytest `tests/python/test_http_service.py::test_approval_actor_comes_from_token`; accepted decisions record the token subject, or conflicting form actors cause a rejection with unchanged state.
- [ ] Deliberate-break gate: restore parsed form actor_id as the manager decision argument in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_approval_actor_comes_from_token` must fail its recorded-identity assertion; revert the break.

## Implementation Notes

Audited remote main: 3ba14a8541b97338586ab6c253ea30e2aed7b86e.

Independent actor-spoof repro succeeded against the unchanged remote head. Closed issue 1506 explicitly excluded decision authorization; this is not another admin-console actor_role finding. Authorized delegation, if later added, must retain both actual caller and represented principal.
