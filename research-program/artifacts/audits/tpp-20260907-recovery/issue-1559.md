## Why (verified evidence)

`ReviewWorkflowStore.create_or_get()` in `src/travel_plan_permission/review_workflow.py:196-200` returns the first persisted review for a `draft_id` and ignores newer `trip_plan`, `policy_snapshot`, and `policy_result` arguments. `PlannerProposalStore.create_manager_review()` in `src/travel_plan_permission/http_service.py:746` calls `create_or_get` on every portal submit, including after a manager `request_changes` decision. Reproduced on tip `37f7ed8`: second `create_or_get` with `traveler_name='CHANGED-TRAVELER'` still returns the original traveler from the first submission.

## Tasks

- [ ] In `src/travel_plan_permission/review_workflow.py:188-209`, refresh stored `trip_plan`, `policy_snapshot`, and `policy_result` when an existing review is in `CHANGES_REQUESTED` (or create a new review id when a finalized review already exists).
- [ ] In `src/travel_plan_permission/http_service.py:2025`, ensure resubmit after `request_changes` surfaces the updated portal answers to the manager queue/detail views.
- [ ] Add `test_manager_review_resubmit_refreshes_trip_plan` to `tests/python/test_http_service.py` covering submit → `request_changes` → edit draft answers → resubmit.

## Acceptance Criteria

- Named test: `tests/python/test_http_service.py::test_manager_review_resubmit_refreshes_trip_plan` asserts `lookup_manager_review_for_draft` returns the edited traveler name and current policy snapshot after resubmit.
- Deliberate-break → revert: restore the early return in `create_or_get()` without refresh → `test_manager_review_resubmit_refreshes_trip_plan` fails → revert.

## Non-Goals

- Do not reopen finalized `APPROVED` / `REJECTED` reviews for mutation (#1544 behavior must remain).
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by repo-audit Track D refill 2026-09-07; verified on tip `37f7ed8` with fixture-based reproduction of stale `create_or_get` output._
