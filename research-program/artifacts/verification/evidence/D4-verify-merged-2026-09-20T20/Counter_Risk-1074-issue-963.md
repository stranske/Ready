title:	Guard the WAL denominator against signed near-cancellation
state:	CLOSED
author:	stranske
labels:	bug, priority:high
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
number:	963
--

## Why

`calculate_wal` in `src/counter_risk/calculations/wal.py:44-48` divides by a **signed** sum of row
totals, guarded only against exact zero:

```python
total_exposure = sum(row.total for row in schedule.rows)
if not math.isfinite(total_exposure):
    raise ValueError("Total exposure is not finite")
if total_exposure == 0:
    return 0.0
weighted_days = sum((row.maturity_date - px).days * row.total for row in schedule.rows)
return weighted_days / total_exposure
```

The `math.isfinite` check added by the previous audit is present and passes — a near-cancelling
denominator is perfectly finite, just close to zero. Executed against `calculate_wal` with a long
1,000,000.00 leg maturing in one year and a short 999,999.99 leg maturing in ten years:

```
signed net exposure : 0.010000000009313226
WAL (days)          : -328,799,996,041
WAL (years)         : -900,205,328
```

WAL is defined by the module docstring as an exposure-weighted average time-to-maturity in days from
the Px Date, so any correct result must fall inside the span of the schedule's own maturity dates —
here `[365, 3653]` days. The returned value is nine orders of magnitude outside it and negative.

The exact-cancellation case is worse because it is silent. A fully-hedged TIPS book sums to exactly
zero and returns `0.0`, and the docstring at `src/counter_risk/calculations/wal.py:14-18` declares
`0.0` to mean "there is no TIPS exposure to measure … That is the expected value for June 2026
onward, not a data error". So a hedged book and a wound-down book are indistinguishable in the
output.

Both paths reach the historical workbook through `src/counter_risk/outputs/historical_workbook.py:89`.

No existing test can catch this: `tests/test_wal.py` is 66 lines and contains no negative total, no
mixed-sign schedule, and no near-zero denominator.

## Scope

- `src/counter_risk/calculations/wal.py`
- `tests/test_wal.py`

## Non-Goals

- Do not change the TIPS-only selection rule or the block the parser reads. Which rows enter the
  calculation is settled and out of scope.
- Do not change the sign convention of `ExposureMaturityRow.total` or touch the parser at
  `src/counter_risk/parsers/exposure_maturity_schedule.py`.
- Do not silently substitute a magnitude denominator (`sum(abs(...))`) without recording that the
  input was mixed-sign. A wrong-but-plausible WAL is worse than a refusal, because the report has no
  other signal that the book was hedged.
- Do not widen this into a general sign-convention refactor across `compute/`. Findings C-1 and C-2
  are filed separately.
- A scaffold-only change does NOT count as completing this issue and is a failure of this issue:
  adding tests without changing the guard, or adding the guard without a distinct signal for the
  exact-cancellation case, is scaffolding rather than a fix.

## Tasks

- [ ] In `src/counter_risk/calculations/wal.py`, compute the gross magnitude `sum(abs(row.total) for row in schedule.rows)` alongside the existing signed total.
- [ ] Raise `ValueError` naming both the signed and gross totals when the gross magnitude is non-zero but the signed total is negligible relative to it, using a documented relative threshold rather than an exact-zero comparison.
- [ ] In `src/counter_risk/calculations/wal.py`, keep returning `0.0` only when the gross magnitude is itself zero, which is the genuine no-TIPS-exposure case the docstring describes.
- [ ] Update the module docstring in `src/counter_risk/calculations/wal.py` to state that `0.0` means no gross exposure, and that a hedged-to-flat book raises rather than returning zero.
- [ ] Add `test_wal_raises_on_near_cancelling_signed_denominator` to `tests/test_wal.py` using a long leg at one year and an opposing short leg at ten years.
- [ ] Add `test_wal_result_lies_within_the_schedule_maturity_span` to `tests/test_wal.py`, asserting the result falls between the earliest and latest row offsets for any schedule that returns a value.
- [ ] Add `test_wal_returns_zero_only_for_empty_gross_exposure` to `tests/test_wal.py`, distinguishing an empty schedule from an exactly-hedged one.

## Acceptance Criteria

- [ ] `tests/test_wal.py::test_wal_raises_on_near_cancelling_signed_denominator` passes.
- [ ] `tests/test_wal.py::test_wal_result_lies_within_the_schedule_maturity_span` passes.
- [ ] `tests/test_wal.py::test_wal_returns_zero_only_for_empty_gross_exposure` passes.
- [ ] **Deliberate-break demonstration.** Restore the bare `if total_exposure == 0: return 0.0` guard in `src/counter_risk/calculations/wal.py`, run `pytest tests/test_wal.py::test_wal_result_lies_within_the_schedule_maturity_span` and paste the FAILING output, which must show the out-of-span value and the span. Revert, re-run the same node id, and paste the PASSING output. Both must appear in the PR body.
- [ ] All pre-existing tests in `tests/test_wal.py` still pass unchanged.
- [ ] `ruff check .` and `black --check .` pass at the pinned versions (`ruff==0.16.4`, `black==26.5.1`).

## Implementation Notes

The span assertion was written and run against the current tip during the 2026-08-24 audit and fails
there with:

```
AssertionError: WAL -328,799,996,041 days is outside the span [365, 3653]
```

That is the expected pre-fix output for the deliberate-break step.

A relative threshold is the right shape here rather than an absolute epsilon, because notional
magnitudes in this book span several orders of magnitude and any fixed epsilon is either
meaningless at the top of that range or trigger-happy at the bottom.

The correct non-finite guard pattern already exists in this package at
`src/counter_risk/compute/limits.py:92`, which raises rather than returning a sentinel — worth
matching for consistency.

Audit reference: `Code/Audits/Counter_Risk/2026-08-24-01-code-quality.md` and
`Code/Audits/Counter_Risk/2026-08-24-AUDIT_REPORT.md`, finding C-3.

