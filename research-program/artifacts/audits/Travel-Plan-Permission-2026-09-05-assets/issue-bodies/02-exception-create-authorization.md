# [P1] Authenticate exception creation and bind its audit actor

## Why

Current break: an anonymous POST creates an exception against an existing travel draft and attributes it to the traveler. `src/travel_plan_permission/http_service.py:1815` defines the mutation without authorization, `src/travel_plan_permission/http_service.py:1867` derives the requestor from stored traveler text, and `src/travel_plan_permission/http_service.py:1884` persists it. The existing handoff capability is explicitly view-only in `docs/security-model.md:148`. The goal is that exception submissions are attributable to an authorized creator, including when the draft identifier is known.

## Scope

Authorization and immutable caller attribution for exception creation on the saved travel-draft route.

## Non-Goals

Changing exception routing thresholds or allowing view-only handoff cookies to mutate drafts. Scaffold-only completion does NOT count: hiding the exception form while anonymous POST still persists a request is a failure of this issue.

## Tasks

- [ ] In `src/travel_plan_permission/http_service.py`, require Permission.CREATE before exception request parsing or persistence and retain the authenticated context.
- [ ] In `src/travel_plan_permission/http_service.py`, bind the exception requestor and audit actor to the authenticated subject; keep traveler display data separately if required.
- [ ] Add `test_exception_creation_requires_create_permission` to `tests/python/test_http_service.py` for anonymous, view-only token, view-only handoff cookie, expired token and create-enabled requests; verify rejected calls leave the exception store unchanged.

## Acceptance Criteria

- [ ] Run pytest `tests/python/test_http_service.py::test_exception_creation_requires_create_permission`; anonymous requests return 401, view-only credentials cannot create, and a valid creator gets a request attributed to its token subject.
- [ ] Deliberate-break gate: remove the creation permission check in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_exception_creation_requires_create_permission` must fail the anonymous mutation assertion; revert the break.

## Implementation Notes

Audited remote main: 3ba14a8541b97338586ab6c253ea30e2aed7b86e.

The independently executed anonymous exception repro returned 303 and persisted one traveler-attributed request. Closed issues 800 and 821 introduced UI and read permissions, respectively; neither covers this remaining mutation. Preserve the view-only handoff contract.
