## Why

Fleet coverage initiative round 5 remains below the 90% objective. The next slice must prove real validation branches in distribution PPT standalone checks, not pad the metric.

## Scope

Add a discriminating regression in `tests/pipeline/test_ppt_validation.py` for uncovered error and external-link branches in `src/counter_risk/pipeline/ppt_validation.py`.

## Non-Goals

- Do NOT change CI or workflow configuration.
- Do NOT add trivial getter or import-only tests.

## Tasks

- [ ] Run `pytest tests/pipeline/test_ppt_validation.py --cov=src/counter_risk/pipeline/ppt_validation.py --cov-report=term-missing` and record baseline in the PR body.
- [ ] In `tests/pipeline/test_ppt_validation.py`, add regressions for missing-file, corrupt-archive, and external-relationship rejection paths in `validate_distribution_ppt_standalone` in `src/counter_risk/pipeline/ppt_validation.py`, and record deliberate-break plus measured coverage delta in the PR body.

## Acceptance Criteria

- [ ] `pytest tests/pipeline/test_ppt_validation.py --cov=src/counter_risk/pipeline/ppt_validation.py --cov-report=term-missing` exits 0 with measured coverage delta recorded in the PR body.
- [ ] The new regressions fail when their selected validation branch is deliberately broken, then pass after revert; both recorded in the PR body.

## Implementation Notes

Coverage-autopilot round 5; low blast radius only. If measured coverage is already at or above 90%, comment and close without opening a PR.
