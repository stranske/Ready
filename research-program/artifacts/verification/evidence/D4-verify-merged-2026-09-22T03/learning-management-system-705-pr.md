# PR #705

Closes #694

## Summary

- add stable primary-key tiebreakers to all five timestamp-ordered latest/page queries named by the issue
- add controlled tied-timestamp regressions for dashboard latest-attempt selection and Inspect evidence ordering
- preserve each query's existing primary timestamp direction and all untied behavior

## Validation

- `uv run pytest tests/ui/test_latest_record_ordering.py -q --no-cov` — 2 passed
- deliberate break: removing `Attempt.id.desc()` and running `uv run pytest tests/ui/test_latest_record_ordering.py -q` fails `test_latest_attempt_is_stable_under_tied_timestamps` with confidence `1/5` instead of the controlled `5/5` winner; restoring the key passes
- `uv run pytest tests/ui tests/api -q --no-cov` — 572 passed, 1 skipped
- `uv run pytest tests/ui tests/api -q` — all 572 tests passed with 1 skipped, but the partial suite exits nonzero because repository-wide coverage is 64.88%, below the global 80% threshold
- `uv run ruff check src/lms/ui/api.py src/lms/ui/attempts.py src/lms/api/inspect.py tests/ui/test_latest_record_ordering.py`
- `uv run black --check src/lms/ui/api.py src/lms/ui/attempts.py src/lms/api/inspect.py tests/ui/test_latest_record_ordering.py`
- `grep -n "order_by" src/lms/api/inspect.py` confirms secondary keys on both affected Inspect queries
