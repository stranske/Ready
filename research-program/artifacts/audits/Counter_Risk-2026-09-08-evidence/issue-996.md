## Why

Fleet coverage initiative round 3 remains below the 90% objective. The next slice must prove a real behavioral branch, not pad the metric.

## Scope

Add a discriminating regression in `tests/workflows/test_historical_update_workflow.py` for an uncovered branch in `src/counter_risk/workflows/historical_update.py`.

## Non-Goals

- Do NOT change CI or workflow configuration.
- Do NOT add trivial getter or import-only tests.

## Tasks

- [ ] Run `python -m pytest tests/workflows/test_historical_update_workflow.py --cov=src/counter_risk/workflows/historical_update.py --cov-report=term-missing` and record baseline in the PR body.
- [ ] Add a regression in `tests/workflows/test_historical_update_workflow.py` for an uncovered non-trivial branch in `src/counter_risk/workflows/historical_update.py`.
- [ ] Document deliberate-break result and before/after coverage in the PR body.

## Acceptance Criteria

- [ ] `python -m pytest tests/workflows/test_historical_update_workflow.py --cov=src/counter_risk/workflows/historical_update.py --cov-report=term-missing` exits 0 with before/after coverage recorded in the PR body.
- [ ] The new regression fails when its selected branch is deliberately broken, then passes after revert; both recorded in the PR body.

## Implementation Notes

Coverage-autopilot round 3; low blast radius only.
