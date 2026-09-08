## Why

The float parsing helper in the capability repository lacks non-numeric string and `NaN` validation (`src/lms/capability/repository.py:221-240`). In `_as_float(value)`, the function performs `if isinstance(value, int | float | str): return float(value)`. Unlike `_as_int`, it lacks try-except protection against invalid strings such as empty strings. In addition, when `value` is `float("nan")` or `"nan"`, `_as_float` returns `nan`. When checking capability target thresholds (`_as_float(row["current_estimate"]) < target.confidence_threshold`), comparisons against `NaN` evaluate to `False`, silently masking weak nodes from learner gap analyses. This is a verified **latent fragility** and calculation robustness issue.

## Scope

Update `_as_float` in `src/lms/capability/repository.py` to safely catch conversion exceptions and validate `math.isfinite(parsed_val)`, returning a safe fallback default or raising a validation error. Add regression tests in `tests/capability/test_repository.py`.

## Non-Goals

- Do NOT modify Bayesian mastery formulas in `src/lms/mastery/policy.py`.
- Do NOT alter table schema definitions in `src/lms/capability/models.py`.
- Scaffold-only completion does NOT count: returning 0.0 for all string inputs without checking finite bounds or without adding unit test assertions for NaN and malformed string handling is a failure of this issue.

## Tasks

- [ ] In `src/lms/capability/repository.py`, import `math` and update `_as_float` to catch `(ValueError, TypeError)` and verify `math.isfinite(parsed_val)`, returning `default` when value is non-numeric, `NaN`, or infinite.
- [ ] In `src/lms/capability/repository.py`, ensure aggregate estimation queries handle null or non-finite mastery records safely without returning `NaN` scores.
- [ ] In `tests/capability/test_repository.py`, add test `test_as_float_handles_nan_and_invalid_strings_safely` asserting safe fallback behavior for `NaN`, `Inf`, and invalid string inputs.

## Acceptance Criteria

- [ ] The named test `pytest tests/capability/test_repository.py -k "test_as_float_handles_nan_and_invalid_strings_safely"` passes with 0 failures, asserting that `_as_float` returns the fallback value for `float("nan")`, `"nan"`, `float("inf")`, and non-numeric strings.
- [ ] **Deliberate-break gate:** In `src/lms/capability/repository.py:225`, remove the `math.isfinite` check in `_as_float`. Running `pytest tests/capability/test_repository.py -k "test_as_float_handles_nan_and_invalid_strings_safely"` MUST fail with an assertion failure (expecting fallback value but receiving `nan`). Revert the edit after capturing the failure.
- [ ] Existing capability repository tests pass via `pytest tests/capability/test_repository.py`.

## Implementation Notes

- Align `_as_float` error handling with `_as_int` in `src/lms/capability/repository.py:230-245`.
- Confirmed-green test runner: `pytest tests/capability/test_repository.py`
