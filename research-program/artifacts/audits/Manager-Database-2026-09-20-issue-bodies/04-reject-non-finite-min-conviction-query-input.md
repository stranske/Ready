## Why

Current latent break on tip 54e4f406: `get_conviction_scores` in `api/signals.py:443-453` declares `min_conviction_pct: float = Query(0.0, ge=0.0)`, which accepts positive infinity, and the SQL filter at `api/signals.py:317` compares with `>=` without a finite guard. Verified: `GET /api/signals/conviction/1?min_conviction_pct=inf` returns HTTP 200 with an empty list instead of HTTP 422. Closed #1623 fixed non-finite JSON output serialization; this input boundary remains open.

## Scope

Query-parameter validation for conviction score list routes in `api/signals.py`.

## Non-Goals

Do not change conviction scoring formulas in `etl/conviction_flow.py` or alert rule parsing covered by closed #1299. Scaffold-only completion does NOT count: documenting infinity as unsupported without rejecting it at the API boundary is a failure of this issue.

## Tasks

- [ ] Add a finite upper bound and `math.isfinite` validation for `min_conviction_pct` on `get_conviction_scores` in `api/signals.py:443-453`, matching the finite guards used elsewhere in the signals module.
- [ ] Return HTTP 422 with a field error when `min_conviction_pct` is NaN, infinity, or above 100.
- [ ] Add `tests/test_signals_api.py::test_conviction_scores_rejects_non_finite_min_conviction_pct` covering `inf` and a valid finite control case.

## Acceptance Criteria

- Named test: `tests/test_signals_api.py::test_conviction_scores_rejects_non_finite_min_conviction_pct` must pass and assert HTTP 422 for `min_conviction_pct=inf`.
- Deliberate-break → revert: restore the bare `Query(0.0, ge=0.0)` declaration; the named test must fail because infinity returns HTTP 200; revert and rerun pytest tests/test_signals_api.py.

## Implementation Notes

NaN already returns HTTP 422 via Pydantic; infinity is the inconsistent case. The named test should also assert a finite value such as `0.5` still returns HTTP 200.
