
## Why

`src/trend_analysis/config/model.py:658-665` rejects `signals.min_periods > signals.window` at config load, but `src/trend_analysis/signals.py:121-127` `TrendSpec.__post_init__` does not, and `tests/test_pipeline_helpers_additional.py:911-917` only guards `min_periods=0`. Runtime currently fails later with a pandas error message instead of the config-model contract.

## Scope

Add the same guard to `TrendSpec` and `pipeline_helpers.compute_signal`. Mirror tests from `tests/test_trend_config_model.py:140-148` for runtime entry points.

## Implementation Notes

- Reuse error text `signals.min_periods cannot exceed signals.window.` for consistency.
- `trend_spec_from_mapping` in `src/trend_analysis/signals.py:222-230` should inherit the guard via `TrendSpec`.
- Do not change preset clamping behaviour in `tests/test_presets_extended.py:47-49` unless presets rely on silent clamping (verify first).

## Tasks

- [ ] Add `min_periods <= window` validation to `TrendSpec.__post_init__` in `src/trend_analysis/signals.py`
- [ ] Add the same check to `compute_signal` in `src/trend_analysis/pipeline_helpers.py`
- [ ] Add `test_trend_spec_rejects_min_periods_above_window` in `tests/test_trend_signals_validation.py`
- [ ] Extend `test_compute_signal_error_paths` in `tests/test_pipeline_helpers_additional.py` for `min_periods > window`

## Acceptance Criteria

- [ ] `pytest tests/test_trend_config_model.py::test_signal_min_periods_cannot_exceed_window tests/test_trend_signals_validation.py tests/test_pipeline_helpers_additional.py::test_compute_signal_error_paths -q` passes
- [ ] `TrendSpec(window=5, min_periods=6)` raises `ValueError` before any pandas rolling call
- [ ] temporarily remove the new guard in `src/trend_analysis/signals.py` and confirm `test_trend_spec_rejects_min_periods_above_window` fails; revert

## Non-Goals

- Changing `SignalSettings` pydantic model fields
- Altering default window/min_periods in shipped YAML configs

Scaffold-only completion does NOT count: a test that expects pandas' error string instead of the config-model message is a failure of this issue.
