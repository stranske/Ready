# [P2] Bind routed exception levels to authenticated approval authority

## Why

Verified enforcement gap: a credential containing only generic approve can approve a 20,000 exception and create a board-level record. `src/travel_plan_permission/models.py:194` defines director/board thresholds and `src/travel_plan_permission/models.py:263` records the routed level, while `src/travel_plan_permission/http_service.py:2114` checks only generic Permission.APPROVE. This is bounded design hardening, not a claimed violation of an existing tier-entitlement contract: `docs/exception-policy.md:53` explicitly describes the current generic approve-capable portal. The goal is to make routing levels enforceable authority requirements instead of labels inferred from the request.

## Scope

Explicit authenticated exception-tier entitlement and fail-closed checks on portal approval, with synthetic configuration fixtures and accurate audit records.

## Non-Goals

Assigning real employees to director or board roles, changing monetary thresholds, or treating actor_role query text as authority. Scaffold-only completion does NOT count: displaying a board label while the generic approve token still finalizes board requests is a failure of this issue.

## Tasks

- [ ] In `src/travel_plan_permission/security.py`, define an explicit trusted subject-to-exception-tier entitlement contract; missing higher-tier entitlement must not imply director or board authority.
- [ ] In `src/travel_plan_permission/http_service.py`, check the authenticated subject entitlement against the exception current routed level before calling decide_exception_request; reject insufficient authority without history mutation.
- [ ] Update `docs/exception-policy.md` to distinguish generic approval permission, exception-tier entitlement, and the deployment responsibility to configure actual principals.
- [ ] Add `test_exception_approval_enforces_tier` to `tests/python/test_http_service.py` covering manager, director and board, amount-derived levels, 48-hour escalation, missing entitlement, and spoofed actor fields.

## Acceptance Criteria

- [ ] Run pytest `tests/python/test_http_service.py::test_exception_approval_enforces_tier`; generic approve alone cannot finalize a board exception, an explicitly entitled synthetic board subject can, and rejected decisions preserve state.
- [ ] Deliberate-break gate: bypass the tier comparison in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_exception_approval_enforces_tier` must fail the generic-approver board case; revert the break.

## Implementation Notes

Audited remote main: 3ba14a8541b97338586ab6c253ea30e2aed7b86e.

Independent board-exception repro returned 303 and a board-level approval using only generic approve. Lead review downgraded the delegate BLOCKER classification because the current documented scope permits approve-capable roles; this is an explicit extension of the authorization model. Use synthetic entitlements in tests; leave actual organizational mapping unconfigured for the owner to supply at deployment.
