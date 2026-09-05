## Why
In `src/fine_art_archive/preference/bradley_terry.py:209-218`, `next_pair()` calculates the score gap between candidates using `gap = abs(strengths.get(a, 1.0) - strengths.get(b, 1.0)) if strengths else 0.0`. A direct call with an explicit None strength raises TypeError; a NaN strength can keep the first encountered pair selected even when a later pair has a valid zero gap. These are defensive library-boundary cases: the declared input type is dict[str, float], so None is out of contract, and this audit has not established that the production fitter emits None or NaN. Treat as lower-priority hardening, not an observed production outage.

## Scope
- `src/fine_art_archive/preference/bradley_terry.py`
- `tests/test_bradley_terry.py`

## Non-Goals
- Scaffold-only completion does NOT count: catching `TypeError` inside the outer loop and skipping pair comparisons without sanitizing node strengths is a failure of this issue.
- Do not alter the component graph connection logic in Rule 1 of `next_pair()`.

## Tasks
- [ ] Add numeric sanitization in `next_pair()` in `src/fine_art_archive/preference/bradley_terry.py` to default `None` and non-finite strengths to `1.0`.
- [ ] Add unit tests in `tests/test_bradley_terry.py` verifying `next_pair()` handles `None` and `NaN` values in `strengths` without raising TypeError or pinning pair selection to a NaN gap.

## Acceptance Criteria
- `pytest tests/test_bradley_terry.py` passes.
- Calling `next_pair(["work-a", "work-b"], [], strengths={"work-a": None, "work-b": 1.0})` returns `("work-a", "work-b")` without raising TypeError.
- Deliberate break: remove `None` check in `src/fine_art_archive/preference/bradley_terry.py`, run `pytest tests/test_bradley_terry.py`, and verify the None-strength test fails; revert to pass.

## Implementation Notes
- Define a small helper `_get_finite_strength(strengths, key, default=1.0)` in `src/fine_art_archive/preference/bradley_terry.py`.
