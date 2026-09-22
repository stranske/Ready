# PR #1092

Closes #1081

## Summary
- Reuse the totals-row counterparty resolver for concentration exposure rows, including `group_name` when `group_type` is `counterparty`.
- Cover group-name-only Alpha, ordinary Beta, and a non-counterparty group in the named regression test.

## Validation
- `python3 -m pytest tests/pipeline/test_run_pipeline.py::test_concentration_includes_group_name_only_counterparty_rows -q` — passed.
- Before the fix, the named test failed because Alpha was absent; after the fix, it passed.
- `python3 -m ruff check src/counter_risk/pipeline/run.py tests/pipeline/test_run_pipeline.py` — passed.
- `python3 -m black --check src/counter_risk/pipeline/run.py tests/pipeline/test_run_pipeline.py` — passed.
- `git diff --check` — passed.
