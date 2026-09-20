
## Why

`tests/test_pipeline_run_cache_fallbacks.py:238` and `tests/test_pipeline_helpers_additional.py:1113` both define `test_compute_signal_uses_cache` (and paired `without_cache` tests) against the same `pipeline_helpers.compute_signal` behaviour. Duplicate names mask which file actually guards cache keying in `src/trend_analysis/pipeline_helpers.py:614-650`.

## Scope

Retain one parametrized cache test module; delete the redundant copy. No production code changes unless a uncovered branch is found while merging.

## Implementation Notes

- Prefer keeping tests in `tests/test_pipeline_helpers_additional.py` (already covers error paths at line 911).
- If `tests/test_pipeline_run_cache_fallbacks.py` has unique assertions (dataset_hash tags), fold them into parametrized cases rather than duplicating entire functions.
- Preserve monkeypatch targets on `pipeline.get_cache` / `pipeline_helpers` as today.

## Tasks

- [ ] Merge cache assertions into a single parametrized test in `tests/test_pipeline_helpers_additional.py`
- [ ] Remove duplicate `test_compute_signal_uses_cache` from `tests/test_pipeline_run_cache_fallbacks.py`
- [ ] Remove duplicate `test_compute_signal_without_cache` from `tests/test_pipeline_run_cache_fallbacks.py`
- [ ] Verify remaining cache coverage in `tests/test_pipeline_run_cache_fallbacks.py` for other symbols is intact

## Acceptance Criteria

- [ ] `pytest tests/test_pipeline_helpers_additional.py -k compute_signal -q` passes
- [ ] `pytest tests/test_pipeline_run_cache_fallbacks.py -q` passes
- [ ] `rg 'def test_compute_signal_uses_cache' tests/` returns exactly one match
- [ ] temporarily force `pipeline_helpers.compute_signal` to skip cache and confirm the surviving `test_compute_signal_uses_cache` fails; revert

## Non-Goals

- Rewriting unrelated tests in `tests/test_pipeline_run_cache_fallbacks.py`
- Changing rolling-cache implementation in `src/trend_analysis/perf/rolling_cache.py`

Scaffold-only completion does NOT count: deleting both copies without a surviving cache regression test is a failure of this issue.
