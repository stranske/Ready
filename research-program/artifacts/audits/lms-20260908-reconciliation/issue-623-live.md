## Why

Criterion points validation in rubric scoring accepts `NaN` (not-a-number) floating-point values without rejection (`src/lms/feedback/scoring.py:233-237`). In `_normalize_criterion_scores`, points are parsed via `points = float(item.get("points", 0))` and validated with `if points < 0 or points > criterion.max_points:`. In Python, comparisons against `float("nan")` always evaluate to `False`, allowing `NaN` values to bypass boundary checks. This causes `raw_score = nan` and `normalized_score = nan` to propagate into `EvidenceRecord` and downstream database models. When persisted, SQLite rejects `NaN` in `NOT NULL` columns or stores corrupt non-numeric values, triggering unhandled `sqlite3.IntegrityError` (HTTP 500) rather than raising `InvalidRubricScoringError` (HTTP 422). This is a verified **current break** in rubric scoring boundary validation.

## Scope

Add explicit `math.isfinite(points)` checks in `_normalize_criterion_scores` in `src/lms/feedback/scoring.py`. Raise `InvalidRubricScoringError` when criterion points contain `NaN`, `Inf`, or `-Inf`. Add unit test coverage in `tests/feedback/test_rubric_scoring.py`.

## Non-Goals

- Do NOT alter valid integer and floating-point scoring computations in `score_rubric`.
- Do NOT alter template models in `src/lms/feedback/templates.py`.
- Scaffold-only completion does NOT count: adding `math.isnan` without checking `math.isinf` or without raising `InvalidRubricScoringError` on invalid scores is a failure of this issue.

## Tasks

- [ ] In `src/lms/feedback/scoring.py`, import `math` and add a finite numeric check `if not math.isfinite(points): raise InvalidRubricScoringError(f"Points for criterion {criterion.id} must be a finite number")` inside `_normalize_criterion_scores`.
- [ ] In `src/lms/feedback/scoring.py`, ensure parsing errors from non-numeric string values raise `InvalidRubricScoringError` cleanly.
- [ ] In `tests/feedback/test_rubric_scoring.py`, add test `test_score_rubric_rejects_nan_and_inf_points` asserting that `score_rubric` raises `InvalidRubricScoringError` when criterion points contain `float("nan")` or `float("inf")`.

## Acceptance Criteria

- [ ] The named test `pytest tests/feedback/test_rubric_scoring.py -k "test_score_rubric_rejects_nan_and_inf_points"` passes with 0 failures, asserting `InvalidRubricScoringError` is raised when scoring input contains `float("nan")` or `float("inf")`.
- [ ] **Deliberate-break gate:** In `src/lms/feedback/scoring.py`, comment out the `math.isfinite(points)` check in `_normalize_criterion_scores`. Running `pytest tests/feedback/test_rubric_scoring.py -k "test_score_rubric_rejects_nan_and_inf_points"` MUST fail with `Failed: DID NOT RAISE <class 'lms.feedback.scoring.InvalidRubricScoringError'>`. Revert the edit after capturing the failure.
- [ ] Existing rubric scoring tests pass via `pytest tests/feedback/test_rubric_scoring.py`.

## Implementation Notes

- Validate finite status before comparing against minimum and maximum points: `try: points = float(item.get("points", 0)) except (ValueError, TypeError) as exc: raise InvalidRubricScoringError(...) from exc`.
- Confirmed-green test runner: `pytest tests/feedback/test_rubric_scoring.py`
