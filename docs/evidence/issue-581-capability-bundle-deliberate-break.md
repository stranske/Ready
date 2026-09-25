# Deliberate-break evidence: capability-bundle ingest map gate (#581 / #560)

Linked issue: `stranske/Ready#581` (parent verification gap `#560`, landed in merged PR #572).

## Mutation (temporary, reverted before merge)

In `scripts/validate_run_contract.py`, the `INGEST_SCHEMA_FILES` entry for `"capability-bundle/v1"` was temporarily removed so the named test could observe the missing mapping.

Production code on this branch still includes the mapping; this file records the RED/GREEN transcript only.

## RED — remove mapping, then `pytest tests/test_main.py::test_ingest_schema_files_includes_capability_bundle -q --no-cov`

```
tests/test_main.py F

=================================== FAILURES ===================================
_____________ test_ingest_schema_files_includes_capability_bundle ______________

    def test_ingest_schema_files_includes_capability_bundle() -> None:
        """Consumer ingest map must include capability-bundle/v1."""
>       assert "capability-bundle/v1" in INGEST_SCHEMA_FILES
E       AssertionError: assert 'capability-bundle/v1' in {'run-contract/v1': 'run-contract-v1.schema.json', ...}

tests/test_main.py:54: AssertionError
=========================== short test summary info ============================
FAILED tests/test_main.py::test_ingest_schema_files_includes_capability_bundle
============================== 1 failed in 11.87s ===============================
```

## GREEN — restore mapping, same command

```
tests/test_main.py .

============================== 1 passed in 4.57s ===============================
```

## Verification command (this PR)

`pytest tests/test_main.py::test_ingest_schema_files_includes_capability_bundle -q --no-cov`
