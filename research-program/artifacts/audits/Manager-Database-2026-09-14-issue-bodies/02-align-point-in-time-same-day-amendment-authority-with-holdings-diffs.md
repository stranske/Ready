## Why

Current conditional data-integrity break: `etl/point_in_time.py:101` omits filing type and `etl/point_in_time.py:135` resolves same-day ties by largest ID. `diff_holdings.py:62` instead ranks amendment status before ID. A same-day amendment with ID 1 and original with ID 2 returns ORIGINAL from holdings_as_of while the diff selector chooses amendment 1. `etl/backtest_flow.py:247` consumes the affected history selector.

## Scope

Authority ranking for visible same-period original and restatement filings, preserving knowledge-time filtering.

## Non-Goals

Do not redesign additive-amendment semantics or pricing. Scaffold-only completion does NOT count: adding a rank helper that holdings_as_of does not call is a failure of this issue.

## Tasks

- [ ] Apply the same filed date, amendment status, and ID tie policy from `diff_holdings.py` to `etl/point_in_time.py`, retaining schemas without a type column and all existing knowledge-time visibility bounds.
- [ ] Add a same-day inverted-ID original and amendment fixture to `tests/test_bitemporal_holdings.py` with pre-amendment and post-amendment cutoffs.
- [ ] Add cross-selector agreement assertions in `tests/test_diff_holdings.py` for the same fixture.

## Acceptance Criteria

- [ ] pytest tests/test_bitemporal_holdings.py tests/test_diff_holdings.py must pass; the new same-day amendment test must return AMENDED after the amendment is known and preserve the original before that cutoff.
- [ ] Deliberate-break gate: Restore the ID-only tie comparison in `etl/point_in_time.py`; the new same-day amendment test in `tests/test_bitemporal_holdings.py` must fail; revert and rerun.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Offline matched-selector reproduction: same date 2024-05-15 and period 2024-03-31, amendment ID 1, original ID 2. Closed issues 1324 and 1463 established these separate paths; this is their currently untested tie boundary.
