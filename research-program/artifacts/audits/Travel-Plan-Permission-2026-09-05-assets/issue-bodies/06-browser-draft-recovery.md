# [P2] Give direct portal drafts a usable scoped review session

## Why

Current browser break: completing the public form and clicking Save draft and review ends at raw JSON saying Missing bearer token. With an injected synthetic bearer token, the same saved draft renders. `src/travel_plan_permission/http_service.py:1703` saves the public direct draft, then redirects at line 1721 without a browser session. Review authorization at `src/travel_plan_permission/http_service.py:1762` rejects it. The sibling handoff flow already issues a short-lived draft-specific view cookie at `src/travel_plan_permission/http_service.py:1696`. The goal is a complete direct browser drafting/review flow while retaining protected mutation and download permissions.

## Scope

Direct draft creation and review-session recovery using the existing view-only handoff capability contract.

## Non-Goals

Granting anonymous create/approve/export permissions, removing bearer checks globally or exposing tokens in URLs. Scaffold-only completion does NOT count: replacing the raw error with static prose while a newly saved direct draft remains inaccessible to its creator is a failure of this issue.

## Tasks

- [ ] In `src/travel_plan_permission/http_service.py`, reuse the existing `_set_handoff_cookie` and `issue_handoff_token` flow for a successfully created direct draft, limited to viewing that draft with the existing expiry and cookie attributes.
- [ ] In `src/travel_plan_permission/http_service.py`, verify signing configuration before saving a direct draft and return a browser-readable recoverable error when the capability cannot be issued.
- [ ] Add `test_direct_draft_scoped_review_session` to `tests/python/test_http_service.py`, covering direct form POST followed by browser-cookie review, wrong draft, expiry and denied submission using only the view cookie.

## Acceptance Criteria

- [ ] Run pytest `tests/python/test_http_service.py::test_direct_draft_scoped_review_session`; a new browser session completes direct draft creation and review without manually supplied headers, but cannot view a different draft or submit with the cookie alone.
- [ ] Deliberate-break gate: remove cookie issuance from direct draft creation in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_direct_draft_scoped_review_session` must fail the follow-redirect review assertion; revert the break.
- [ ] Capture browser verification of the completed synthetic form leading to its review page and a separate denied mutation with the view-only cookie.

## Implementation Notes

Audited remote main: 3ba14a8541b97338586ab6c253ea30e2aed7b86e.

Browser screenshots anonymous-draft-result and authenticated-draft-result establish the matched control. Closed issue 821 intentionally protects review access; this issue preserves it by reusing the existing narrowly scoped capability. The four-evaluator UX panel corroborated the recovery failure.
