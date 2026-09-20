
## Why

Current break: `src/trend_analysis/config/model.py:517-528` converts `portfolio.lambda_tc` with `float()` and checks only the numeric interval, so NaN passes both comparisons. `src/trend_analysis/risk.py:156-168` then uses that NaN in the turnover blend and returns NaN weights when previous weights are supplied. The fallback validator repeats the interval-only check at `src/trend_analysis/config/models.py:482-492`.

## Scope

Reject NaN and both infinities for `portfolio.lambda_tc` in every supported configuration validation path while preserving finite values in the inclusive `[0, 1]` interval.

## Implementation Notes

Perform the finite check after numeric coercion and before the existing bounds check. Keep the present null and blank-value behaviour unless a compatibility review identifies a required change.

## Tasks

- [ ] Update `src/trend_analysis/config/model.py` to reject non-finite `portfolio.lambda_tc` after coercion.
- [ ] Update `src/trend_analysis/config/models.py` to enforce the same rejection in runtime and fallback portfolio validation.
- [ ] Extend `tests/test_config_turnover_validation.py` with NaN and infinity coverage for `portfolio.lambda_tc`.

## Acceptance Criteria

- `pytest tests/test_config_turnover_validation.py::test_lambda_tc_rejects_non_finite` passes while finite values from 0 through 1 remain accepted.
- temporarily remove the finite check and confirm tests/test_config_turnover_validation.py::test_lambda_tc_rejects_non_finite fails; revert.

## Non-Goals

- Do not alter the turnover-penalty formula in `src/trend_analysis/risk.py`.
- Scaffold-only completion does NOT count: adding coverage without rejecting non-finite values in both validation paths is a failure of this issue.
