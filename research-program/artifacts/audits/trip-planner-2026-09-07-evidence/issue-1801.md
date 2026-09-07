# [P1] Lodging policy preview must not mark compliant when nightly rate is unavailable

## Why

`trip_planner/app/services/scenario_policy_preview.py:91-92` returns an empty violation list when `nightly_typical_amount` is missing or non-numeric, even when `lodging_rules.max_nightly_rate_usd` is configured. Trip-total preview correctly returns an incomplete violation at `:57-66` after #1780. A business scenario with a trip total but no nightly breakdown can still show `In policy (preview)` while the lodging cap was never checked.

## Scope

Lodging branch of `trip_planner/app/services/scenario_policy_preview.py`.

## Tasks

- [ ] Add `test_missing_nightly_amount_marks_lodging_preview_incomplete_not_compliant` in `tests/app/test_scenario_policy_preview.py` with a lodging cap and `estimated_total` lacking `nightly_typical_amount`.
- [ ] Change `trip_planner/app/services/scenario_policy_preview.py` `_lodging_violations` to return an `incomplete: True` violation when a cap exists and nightly actual is absent, mirroring `_budget_violations`.
- [ ] Ensure `build_scenario_policy_preview` in `trip_planner/app/services/scenario_policy_preview.py` treats lodging-only incomplete violations like budget incomplete violations at lines 207-215.

## Acceptance Criteria

- `pytest tests/app/test_scenario_policy_preview.py::test_missing_nightly_amount_marks_lodging_preview_incomplete_not_compliant` passes.
- `pytest tests/app/test_scenario_policy_preview.py` passes.
- Deliberate-break → revert: restore the early `return []` at `trip_planner/app/services/scenario_policy_preview.py:91-92` and confirm the new test fails; revert.

## Non-Goals

- Authoritative TPP verdict logic in `trip_planner/app/services/policy.py`.
- Scaffold-only completion does NOT count: returning a generic note without setting `compliant: None` for missing nightly data is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._
