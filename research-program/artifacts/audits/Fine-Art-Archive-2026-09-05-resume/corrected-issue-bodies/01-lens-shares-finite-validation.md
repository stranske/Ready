## Why
In `src/fine_art_archive/selection/lenses.py:291-298` and `src/fine_art_archive/selection/lenses.py:351-358`, `allocate()` and `allocate_monthly()` normalize custom budget shares across available lenses using `weights = {n: float(shares.get(n, 0.0)) for n in available}` and `total = sum(weights.values())`. With a NaN share, `total` is NaN and bypasses the non-positive-total fallback; both allocation functions raise ValueError when converting allocations to integers. This was reproduced at the audited commit. Zero shares are already meaningful inputs under the documented lens-floor behavior and must retain that behavior; they do not independently establish this crash.

## Scope
- `src/fine_art_archive/selection/lenses.py`
- `tests/test_selection_lenses.py`

## Non-Goals
- Scaffold-only completion does NOT count: catching `ValueError` at call sites or returning empty dictionaries on invalid weights without validating each share against finite non-negative bounds is a failure of this issue.
- Do not redesign the round-robin candidate distribution loop or saturation caps.

## Tasks
- [ ] Add finite non-negative validation for shares in `src/fine_art_archive/selection/lenses.py` falling back to default shares or equal positive distribution when weights are non-finite or negative.
- [ ] Add unit tests in `tests/test_selection_lenses.py` asserting `allocate()` and `allocate_monthly()` safely handle NaN, infinity, and negative shares without raising ValueError.

## Acceptance Criteria
- `pytest tests/test_selection_lenses.py` passes with 100% success.
- Passing `shares={"canon": float("nan"), "atypicality": 1.0}` to `allocate(10, ["canon", "atypicality"], shares)` and `allocate_monthly(10, ["canon", "atypicality"], shares, monthly_cap=100, spent={})` produces valid non-negative integer allocations summing to the batch cap without crashing.
- Deliberate break: remove finite validation in `src/fine_art_archive/selection/lenses.py`, run `pytest tests/test_selection_lenses.py`, and verify that the NaN allocation tests fail; revert to pass.

## Implementation Notes
- Use `math.isfinite(w) and w >= 0.0` when sanitizing shares in `src/fine_art_archive/selection/lenses.py`.
