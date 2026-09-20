title:	[P2] Validate finite and non-negative bounds for historical WAL row appends
state:	CLOSED
author:	stranske-automation-bot
labels:	bug, priority:normal
comments:	2
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1022
--
# [P2] Validate finite and non-negative bounds for historical WAL row appends

## Why

`src/counter_risk/writers/historical_update.py:798` casts `wal_value` directly to float without asserting that the value is finite and non-negative before writing to the historical WAL worksheet cell. While `src/counter_risk/calculations/wal.py:76` guards its calculation result, standalone calls to `append_wal_row` at line 732 or workflow wrappers at `src/counter_risk/workflows/historical_update.py:36` can inject NaN, infinity, or negative numbers into persistent Excel workbooks.

## Scope

Add finite and non-negative validation for `wal_value` in `append_wal_row` in `src/counter_risk/writers/historical_update.py`.

## Non-Goals

No changes to WAL calculation math or maturity schedule parsing. Scaffold-only or partial completion does NOT count as done; complete the observable behavior and test gates below.

## Tasks

- [ ] In `src/counter_risk/writers/historical_update.py`, add validation in `append_wal_row` to ensure `wal_value` is finite and greater than or equal to zero.
- [ ] Extend `tests/writers/test_historical_update.py` with test cases verifying that NaN, infinity, and negative WAL values raise `ValueError`.
- [ ] Verify in `tests/writers/test_historical_update.py` that valid 0.0 and positive WAL floats continue to append successfully.

## Acceptance Criteria

- [ ] `python -m pytest tests/writers/test_historical_update.py -q` passes with new test coverage asserting finite and non-negative WAL bounds.
- [ ] Deliberate-break gate: remove the finite and non-negative validation from `append_wal_row` in `src/counter_risk/writers/historical_update.py`; the non-finite WAL append tests must fail; restore the check and rerun.
- [ ] Valid WAL values (0.0 for wound-down TIPS and positive floats for active maturities) append to the worksheet without regression.

## Implementation Notes

Complements closed issue #963 (which hardened the WAL denominator against signed near-cancellation) by enforcing boundary safety at the workbook writer layer.

