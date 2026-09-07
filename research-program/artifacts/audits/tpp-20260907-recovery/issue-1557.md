## Why (verified evidence)

`ExceptionRequest.approve()` and `ExceptionRequest.reject()` in `src/travel_plan_permission/models.py:252-277` mutate status with no terminal-state guard. A second call can flip `APPROVED` to `REJECTED` and overwrite `approval.approver_id`. `PlannerProposalStore.decide_exception_request()` in `src/travel_plan_permission/http_service.py:885-905` invokes those methods without checking the current status, and the admin route at `src/travel_plan_permission/http_service.py:2205` exposes repeat decisions. Reproduced in-process: approve then reject leaves `status=rejected` while retaining the first approver record.

## Tasks

- [ ] In `src/travel_plan_permission/models.py:252-277`, raise a dedicated error (or return without mutation) when `approve()` / `reject()` is called on a request whose `status` is already `APPROVED` or `REJECTED`.
- [ ] In `src/travel_plan_permission/http_service.py:885-905`, reject repeat decisions with HTTP 409 before calling `approve()` / `reject()`, leaving status and approval history unchanged.
- [ ] Add `test_exception_decision_is_terminal` to `tests/python/test_http_service.py` covering approve-then-reject and reject-then-approve on `/portal/admin/exceptions/{draft_id}/{index}/decision`.

## Acceptance Criteria

- Named test: `tests/python/test_http_service.py::test_exception_decision_is_terminal` asserts the second POST returns HTTP 409 and the stored exception status and `approval.approver_id` are unchanged.
- Deliberate-break → revert: remove the terminal guard in `decide_exception_request()` → `test_exception_decision_is_terminal` fails its 409 assertion → revert.

## Non-Goals

- Do not change exception routing, tier entitlements, or audit event schema.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by repo-audit Track D refill 2026-09-07; verified on tip `37f7ed8` via in-process reproduction and line reads._
