title:	[P2] Reject malformed nonblank maturity amounts
state:	CLOSED
author:	stranske
labels:	bug, priority:normal
comments:	0
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1063
--
# [P2] Reject malformed nonblank maturity amounts

## Why

`src/counter_risk/parsers/exposure_maturity_schedule.py:247` is current evidence at current main 7c01963cb4173128c806347e622ed43a08fdcf4a. Current break: a real synthetic workbook with a maturity date and Total=not-a-number parses as total=0.0. The parser catches every numeric-coercion error and replaces it with zero. Its documented zero-fill contract covers blank cells only (`src/counter_risk/parsers/exposure_maturity_schedule.py:226`); silently discarding a malformed leg can bias the downstream WAL.

## Scope

Keep blank cells as zero, but reject nonblank invalid amounts with source row/column context before WAL calculation.

## Non-Goals

No upstream workflow changes, model redesign, or unrelated refactors. Scaffold-only completion does NOT count: adding a helper or a test double that leaves reject malformed nonblank maturity amounts unimplemented is a failure of this issue.

## Tasks

- [ ] In `src/counter_risk/parsers/exposure_maturity_schedule.py`, raise the existing maturity schedule error for nonblank unparseable amounts instead of replacing numeric conversion failures with zero.
- [ ] In `tests/parsers/test_exposure_maturity_schedule.py`, add `test_invalid_nonblank_total_raises`. Add real workbook cases for blank, malformed text, boolean, NaN or Infinity text, and valid accounting amounts; assert malformed rows fail before `src/counter_risk/calculations/wal.py` returns a result.

## Acceptance Criteria

- [ ] `python -m pytest tests/parsers/test_exposure_maturity_schedule.py -q` passes and collects `test_invalid_nonblank_total_raises`. Blank totals still parse as zero; malformed nonblank totals raise with row and Total-column context; valid accounting values retain their amounts.
- [ ] Deliberate-break gate: temporarily restore the faulty behavior in `src/counter_risk/parsers/exposure_maturity_schedule.py`; `tests/parsers/test_exposure_maturity_schedule.py::test_invalid_nonblank_total_raises` must fail; revert the deliberate break and rerun the named test to pass. Capture both outcomes in the implementation PR.
- [ ] The test exercises the actual production boundary and retains a valid-input control.

## Implementation Notes

Verified audit work order filed 2026-09-14. Current-code proof: lead-numerical-seams.py creates and parses an actual XLSX. #963 validates signed WAL denominators and #1022 validates WAL output; neither preserves rejected parser inputs.
