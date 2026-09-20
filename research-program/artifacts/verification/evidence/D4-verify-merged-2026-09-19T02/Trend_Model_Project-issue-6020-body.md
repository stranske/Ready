
## Why

`src/trend_analysis/util/weights.py:35-40` only converts inputs when `sum(abs)` ≈ 100 or ≈ 1; otherwise weights pass through unchanged (e.g. `{A:30, B:20}` stays 30/20). Callers in `src/trend_analysis/api.py:340` and `src/trend_analysis/multi_period/engine.py:159` rely on this helper with no test for the ambiguous band in `tests/test_weights_utils.py`.

## Scope

Document and enforce the intended behaviour for totals that are neither percent-like nor fraction-like. Add boundary tests; adjust implementation only if product owner wants rejection or sum-normalisation (default: divide by `total_abs` when `total_abs > 0` and not close to 1 or 100).

## Implementation Notes

- Existing tests at `tests/test_weights_utils.py:9-33` cover percent and fraction paths.
- Preserve long-short percent case at `tests/test_weights_utils.py:43-47` (`120, -20` sums to 100).
- Add explicit tests for `sum=0`, ambiguous mid-range, and negative totals not summing to 100.
- Update docstring on `normalize_weights` to state the chosen rule.

## Tasks

- [ ] Decide and implement ambiguous-total handling in `src/trend_analysis/util/weights.py`
- [ ] Add boundary tests in `tests/test_weights_utils.py` for ambiguous and zero-sum inputs
- [ ] Verify `src/trend_analysis/api.py` callers still receive expected fractions in a smoke test if needed

## Acceptance Criteria

- [ ] `pytest tests/test_weights_utils.py -q` passes
- [ ] new test `test_normalize_weights_ambiguous_total` documents the chosen rule with exact expected values
- [ ] temporarily remove ambiguous-total handling in `src/trend_analysis/util/weights.py` and confirm `test_normalize_weights_ambiguous_total` fails; revert

## Non-Goals

- Changing portfolio optimisation weight constraints in `src/trend_analysis/stages/portfolio.py`
- UI copy changes in Streamlit pages

Scaffold-only completion does NOT count: a docstring-only change without a failing-before/passing-after test is a failure of this issue.
