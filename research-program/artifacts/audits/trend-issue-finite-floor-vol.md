## Why

This is a current break. `src/trend_analysis/config/model.py:614-623` converts `vol_adjust.floor_vol` with `float()` but rejects only negative values, accepting `nan` and infinity. `src/trend_analysis/risk.py:130-135` applies a positive floor with `vol.clip(lower=float(floor_vol))`; with an infinite floor, every finite volatility becomes infinity and the subsequent factor cleanup returns `0.0` for every asset. A direct current-tip reproduction of `_scale_factors(Series({'A': .2, 'B': .1}), .1, floor_vol=inf)` returned `{'A': 0.0, 'B': 0.0}`. Existing tests at `tests/test_trend_analysis_config_model.py:419-445` reject negative floor values but not non-finite values, and `tests/test_vol_floor_and_warmup.py:32-45` exercises only a finite floor.

## Scope

Reject non-finite `vol_adjust.floor_vol` input before it can silently suppress every volatility-scaled allocation.

## Non-Goals

- Do not change the valid zero-floor behavior or the target-volatility exposure formula.
- Do not add new volatility-targeting modes or alter the default finite floor value.
- Scaffold-only completion does NOT count: a validator-only change without a regression test proving an infinite floor cannot zero scale factors is a failure of this issue.

## Tasks

- [ ] Update `src/trend_analysis/config/model.py` `RiskSettings._validate_floor` to reject `nan`, positive infinity, and negative infinity after numeric coercion.
- [ ] Extend `tests/test_trend_analysis_config_model.py` with non-finite `floor_vol` validation cases.
- [ ] Extend `tests/test_vol_floor_and_warmup.py` with a named regression test that confirms the configuration boundary rejects an infinite floor rather than passing it to `_scale_factors`.

## Acceptance Criteria

- [ ] `pytest tests/test_trend_analysis_config_model.py::test_risk_settings_reject_non_finite_floor_vol tests/test_vol_floor_and_warmup.py::test_infinite_floor_vol_is_rejected_before_scaling -q` passes and observes rejection for `nan`, `inf`, and `-inf`.
- [ ] Deliberate-break gate: temporarily remove the finite-value guard from `src/trend_analysis/config/model.py` `RiskSettings._validate_floor`; `tests/test_trend_analysis_config_model.py::test_risk_settings_reject_non_finite_floor_vol` must fail, then revert the mutation.
- [ ] `pytest tests/test_vol_floor_and_warmup.py::test_floor_vol_limits_scaling -q` passes with finite floor behavior unchanged.

## Implementation Notes

Use `math.isfinite`, matching `RiskSettings._validate_target` at `src/trend_analysis/config/model.py:601-612`. The existing `_scale_factors` cleanup is not validation: it transforms the invalid infinite-floor result into a plausible all-cash output.
