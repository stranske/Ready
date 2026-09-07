# [P1] Policy UI must not show compliant and block export when evaluation_result is stripped

## Why

Default workspace sanitization nulls `proposal_state.evaluation.evaluation_result` while keeping `summary.approval_ready` true (`trip_planner/app/services/workspace.py:1815-1818`; `tests/app/test_workspace.py:3432-3434`). `frontend/src/routes/WorkspacePage.tsx:1287-1289` gates print/export on `evaluation.evaluation_result`, but `frontend/src/components/workspace/panels/PolicyPanel.tsx:107-114` shows `Policy compliant` from `approval_ready` alone. Users see a compliant headline with disabled print and export buttons on normal API loads.

## Scope

Alignment between public proposal summary fields and Policy tab presentation/export gating.

## Tasks

- [ ] Add `frontend/src/routes/WorkspacePage.test.tsx` coverage for sanitized proposal state where `approval_ready` is true and `evaluation_result` is null.
- [ ] Update `frontend/src/components/workspace/panels/PolicyPanel.tsx` `derivePolicyPanelView` to avoid `kind: "compliant"` when `evaluation.evaluation_result` is absent on non-debug payloads.
- [ ] Align print and export enablement in `frontend/src/routes/WorkspacePage.tsx` with the same submission-ready signal or expose a public `has_saved_verdict` flag from `trip_planner/app/services/workspace.py`.

## Acceptance Criteria

- `npm test -- WorkspacePage` passes including the sanitized proposal regression test.
- `pytest tests/app/test_workspace.py::test_workspace_response_filters_business_policy_proposal_diagnostics_by_default` passes.
- Deliberate-break → revert: restore compliant rendering from `approval_ready` alone and confirm the new frontend test fails; revert.

## Non-Goals

- Exposing full `evaluation_result` diagnostics on default workspace responses.
- Scaffold-only completion does NOT count: disabling the compliant headline without enabling a coherent export/submit path is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._
