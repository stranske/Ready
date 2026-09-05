# [P1] Enforce permissions on expense intake, review, and export

## Why

Current break at the audited head: an anonymous HTTP client can create an expense draft (303), read its saved details (200), and download its accounting CSV (200). A valid approved-request linkage is checked, but it does not establish the caller identity. `src/travel_plan_permission/http_service.py:1726` accepts the expense POST, `src/travel_plan_permission/http_service.py:1799` renders saved details, and `src/travel_plan_permission/http_service.py:2253` serves exports without authentication. The role model distinguishes view, create, and export at `src/travel_plan_permission/security.py:14` and grants export to finance administrators at `src/travel_plan_permission/security.py:55`. The goal is an authenticated accounting handoff. A caller must know or obtain an existing identifier; no enumeration exploit is claimed.

## Scope

Expense portal route authorization, with existing linkage validation retained. Use create for intake, view for saved details, and export for downloadable accounting artifacts.

## Non-Goals

Changing reimbursement policy, OCR, or pre-trip permission requirements. Scaffold-only completion does NOT count: protecting only the navigation while direct expense requests still succeed without permission is a failure of this issue.

## Tasks

- [ ] In `src/travel_plan_permission/http_service.py`, authorize expense POST, saved-detail GET, and artifact GET before reading or mutating draft state using the matching Permission member from `src/travel_plan_permission/security.py`.
- [ ] In `src/travel_plan_permission/http_service.py`, record the authenticated subject for expense export audit events instead of the constant expense-portal actor.
- [ ] Add `test_expense_routes_enforce_permissions` to `tests/python/test_http_service.py`, with missing-token, view-only, create-only, export-enabled and invalid-linkage controls; assert denied operations do not mutate state or emit success events.

## Acceptance Criteria

- [ ] Run pytest `tests/python/test_http_service.py::test_expense_routes_enforce_permissions`; unauthenticated requests return 401, insufficient permissions return 403, and allowed requests retain the existing linkage checks.
- [ ] Deliberate-break gate: temporarily remove the expense export authorization call in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_expense_routes_enforce_permissions` must fail its missing-token export assertion; revert the break.

## Implementation Notes

Audited remote main: 3ba14a8541b97338586ab6c253ea30e2aed7b86e.

Independent proof: expense-proof.json records 303/200/200 without credentials and 400 for an unknown approved request. Closed issue 821 covered pre-trip review reads; this is the separate expense route. Tests should preserve the deliberate accounting-review handoff behavior for flagged reports.
