## Why

The graph design UI routes for approving and rejecting AI-generated proposals do not catch invalid proposal state transitions (`src/lms/ui/graph_design.py:96-150`). In `approve_graph_proposal_route` and `reject_graph_proposal_route`, calls to `approve_proposal` and `reject_proposal` execute without handling `InvalidProposalStateError` or `ProposalNotFoundError`. When an author double-clicks the action button or processes an already-resolved proposal across multiple browser tabs, the server raises an unhandled exception resulting in HTTP 500 error pages. The UI should catch already-resolved proposal exceptions, flash a user notice, and redirect back to `/app/admin/graph-design` with HTTP 303. This is a verified **current break** in UI error handling.

## Scope

Wrap proposal approval and rejection service calls in `src/lms/ui/graph_design.py` in try-except blocks catching `(InvalidProposalStateError, ProposalNotFoundError)`, add feedback flash notices, and return HTTP 303 redirect responses. Add regression tests in `tests/ui/test_graph_design_surface.py`.

## Non-Goals

- Do NOT modify the authoring assist service in `src/lms/llm/authoring_assist.py`.
- Do NOT modify the proposal data model in `src/lms/llm/proposals.py`.
- Scaffold-only completion does NOT count: adding try-except blocks without redirecting to `/app/admin/graph-design` with flash error messages or without test coverage of already-resolved proposals is a failure of this issue.

## Tasks

- [ ] In `src/lms/ui/graph_design.py`, import `InvalidProposalStateError` and `ProposalNotFoundError` from `src/lms/llm/proposals.py`.
- [ ] In `src/lms/ui/graph_design.py`, update `approve_graph_proposal_route` and `reject_graph_proposal_route` to catch `(InvalidProposalStateError, ProposalNotFoundError)` and return a redirect response to `/app/admin/graph-design` with a flash warning message.
- [ ] In `tests/ui/test_graph_design_surface.py`, add test `test_graph_design_duplicate_proposal_approval_redirects_with_notice` asserting that approving an already-approved proposal returns HTTP 303 redirect with a notice.

## Acceptance Criteria

- [ ] The named test `pytest tests/ui/test_graph_design_surface.py -k "test_graph_design_duplicate_proposal_approval_redirects_with_notice"` passes with 0 failures, asserting HTTP 303 redirect when approving or rejecting an already-resolved proposal.
- [ ] **Deliberate-break gate:** In `src/lms/ui/graph_design.py:105`, comment out the exception handler for `InvalidProposalStateError`. Running `pytest tests/ui/test_graph_design_surface.py -k "test_graph_design_duplicate_proposal_approval_redirects_with_notice"` MUST fail (unhandled exception raised instead of HTTP 303 redirect). Revert the edit after capturing the failure.
- [ ] Existing graph design surface tests pass via `pytest tests/ui/test_graph_design_surface.py`.

## Implementation Notes

- Use `request.session.flash("Proposal has already been processed", "warning")` pattern consistent with support admin UI routes in `src/lms/ui/support_admin.py`.
- Confirmed-green test runner: `pytest tests/ui/test_graph_design_surface.py`
