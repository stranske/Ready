# [P2] Collapse duplicate Repo rows when applying authoritative cash

## Why

`src/counter_risk/pipeline/run.py:1107` says Repo-cash upsert must prevent duplicate cash, but line 1120 retains only the first matching record in its index and line 1131 replaces only that row. All originals remain in the returned list. The live historical aggregator at `src/counter_risk/pipeline/run.py:4097` sums every normalized-name row. Lead-seat probes supplied two CIBC Repo records with cash 10 and 20 plus authoritative cash 100: the actual injection and historical aggregator reported 120. A single-row control reported 100. This is conditional on duplicated normalized Repo rows; no prevalence claim is made for current operator workbooks.

## Scope

The injection-to-historical-Cash seam when applying authoritative cash to existing duplicate Repo records.

## Non-Goals

No new financial model, source-format rewrite or upstream workflow change. Scaffold-only or partial completion does NOT count as done; the behavior and test gates must be delivered.

## Tasks

- [ ] In `src/counter_risk/pipeline/run.py`, make `_inject_repo_cash_into_cprs_ch` collapse or explicitly reject all normalized duplicate Repo records for each authoritative cash key, preserving unrelated rows and segments.
- [ ] Extend `tests/pipeline/test_run_pipeline.py` with duplicate literal names and normalized aliases, passing the injection output into `_aggregate_cprs_ch_series_totals`.
- [ ] Verify in `tests/pipeline/test_run_pipeline.py` that repeating authoritative cash application is idempotent and preserves unrelated counterparties.

## Acceptance Criteria

- [ ] `python -m pytest tests/pipeline/test_run_pipeline.py -q -m "not slow and not release"` passes with a named duplicate-Repo-cash regression: 10 and 20 replaced by authoritative 100 cannot aggregate to 120.
- [ ] The one-row control yields 100, unrelated non-Repo records retain their values, and reapplying the same authoritative mapping does not increase Cash.
- [ ] Deliberate-break gate: restore the first-record-only replacement in `_inject_repo_cash_into_cprs_ch` within `src/counter_risk/pipeline/run.py`; the new duplicate-Repo-cash regression must fail; restore the fix.

## Implementation Notes

Closed #1006 is about non-finite structured-source parsing, not duplicate CPRS-CH output rows. Keep the trigger and severity conditional.
