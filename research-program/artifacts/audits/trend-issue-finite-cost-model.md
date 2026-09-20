## Why

This is a current break. `src/trend_analysis/config/model.py:344-353` converts `portfolio.cost_model.per_trade_bps` and `half_spread_bps` with `float()` but only rejects negative values, so both `nan` and `inf` validate. `src/trend_analysis/config/models.py:510-517` repeats that incomplete check on the runtime configuration path. A direct current-tip reproduction accepted `{per_trade_bps: inf, half_spread_bps: nan}` through `load_config`; `src/trend_analysis/metrics/turnover.py:39-50` then propagates those values as infinite or NaN transaction costs. This is not covered by `tests/test_trend_analysis_config_model.py:381-405`, which covers negative and over-range turnover but not non-finite cost inputs.

## Scope

Reject non-finite cost-model values at every supported configuration boundary before a portfolio run can calculate transaction-cost deductions.

## Non-Goals

- Do not change the supported non-negative basis-point semantics or add an arbitrary upper limit.
- Do not change turnover calculation formulas in `src/trend_analysis/metrics/turnover.py`.
- Scaffold-only completion does NOT count: adding a guard to only one configuration model while another supported `load_config` path still accepts non-finite cost values is a failure of this issue.

## Tasks

- [ ] Update `src/trend_analysis/config/model.py` `CostModelSettings._validate_cost` to reject `nan`, positive infinity, and negative infinity after numeric coercion.
- [ ] Update `src/trend_analysis/config/models.py` cost-model validation in both runtime implementations so `load_config` rejects non-finite `per_trade_bps` and `half_spread_bps`.
- [ ] Extend `tests/test_trend_analysis_config_model.py` with direct strict-model and mapping-based `load_config` cases for non-finite cost inputs.

## Acceptance Criteria

- [ ] `pytest tests/test_trend_analysis_config_model.py::test_cost_model_rejects_non_finite_values -q` passes and proves that `nan`, `inf`, and `-inf` are rejected for both cost fields through the strict and runtime configuration paths.
- [ ] Deliberate-break gate: temporarily remove the finite-value guard from `src/trend_analysis/config/model.py` `CostModelSettings._validate_cost`; `tests/test_trend_analysis_config_model.py::test_cost_model_rejects_non_finite_values` must fail, then revert the mutation.
- [ ] `pytest tests/test_turnover_vectorization.py -q` passes, confirming finite transaction-cost calculations retain their existing contract.

## Implementation Notes

The current-tip reproduction used `config/demo.yml` with valid paths and replaced only `portfolio.cost_model.per_trade_bps` with `float('inf')` and `half_spread_bps` with `float('nan')`; `load_config` accepted the mapping. Keep the error text field-specific.
