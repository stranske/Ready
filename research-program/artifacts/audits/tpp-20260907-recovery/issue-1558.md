## Why (verified evidence)

`docs/exception-policy.md:66-68` documents that pending exception requests escalate to the next approval level after 48 hours. `ExceptionRequest.escalate_if_overdue()` in `src/travel_plan_permission/models.py:279-293` implements that SLA, but repository search shows it is only called from tests (`tests/python/test_exceptions.py:83`, `tests/python/test_http_service.py:2107`) and never from production `src/`. As a result, `authorize_exception_tier()` in `src/travel_plan_permission/exception_authority.py:78` and `decide_exception_request()` in `src/travel_plan_permission/http_service.py:885` evaluate the pre-escalation `approval_level`, so overdue manager-tier requests remain manager-routable indefinitely.

## Tasks

- [ ] Add a store-level helper in `src/travel_plan_permission/http_service.py` (near `decide_exception_request`) that escalates all pending/escalated exceptions for a draft before tier authorization or decision.
- [ ] Call that helper from the exception decision route at `src/travel_plan_permission/http_service.py:2187` and from exception listing surfaces that drive admin review (at minimum before `authorize_exception_tier()` at `src/travel_plan_permission/http_service.py:2196`).
- [ ] Add `test_exception_escalation_before_authorization` to `tests/python/test_http_service.py` seeding a manager-tier request with `requested_at` older than 48 hours and asserting stored `approval_level` becomes `director` without manually calling `escalate_if_overdue()` in the test.

## Acceptance Criteria

- Named test: `tests/python/test_http_service.py::test_exception_escalation_before_authorization` asserts overdue pending requests escalate before authorization and a generic approver receives HTTP 403 while a director-entitled subject can decide.
- Deliberate-break → revert: skip the new escalation call on the decision route → `test_exception_escalation_before_authorization` fails → revert.

## Non-Goals

- Do not change the 48-hour window constant or entitlement configuration format.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by repo-audit Track D refill 2026-09-07; verified on tip `37f7ed8` via docs/implementation parity check and `rg escalate_if_overdue` showing zero `src/` callers._
