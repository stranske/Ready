## Why
In `src/fine_art_archive/quality/source_quality.py:264-277`, `_record_blended_stats()` computes source age during warmup using `age_days = (datetime.now(UTC) - first).total_seconds() / 86400.0`. It parses `first_seen` with `first = datetime.fromisoformat(str(first_seen).replace("Z", "+00:00"))`. When `first_seen` is an offset-naive ISO timestamp string (e.g. `"2026-08-01T12:00:00"`), `first` has `tzinfo=None`. Subtracting `first` from timezone-aware `datetime.now(UTC)` raises `TypeError: can't subtract offset-naive and offset-aware datetimes`, which is not caught by `except ValueError:` and crashes `score_for()` and the entire acquisition assessment flow.

## Scope
- `src/fine_art_archive/quality/source_quality.py`
- `tests/test_source_quality_wiring.py`

## Non-Goals
- Scaffold-only completion does NOT count: silencing `TypeError` without ensuring parsed `first_seen` timestamps are coerced to timezone-aware UTC datetimes is a failure of this issue.
- Do not change the 30-day warmup blending formula or tier prior defaults.

## Tasks
- [ ] Coerce parsed `first` datetimes with `if first.tzinfo is None: first = first.replace(tzinfo=UTC)` and catch `(ValueError, TypeError)` in `src/fine_art_archive/quality/source_quality.py`.
- [ ] Add unit tests in `tests/test_source_quality_wiring.py` verifying `score_for()` computes blended scores correctly when `first_seen` contains offset-naive ISO strings.

## Acceptance Criteria
- `pytest tests/test_source_quality_wiring.py` passes.
- Calling `score_for("cleveland", "western-painting-19c", aggregates=...)` with `first_seen="2026-08-01T12:00:00"` returns a valid finite float score without raising TypeError.
- Deliberate break: remove timezone coercion in `src/fine_art_archive/quality/source_quality.py`, run `pytest tests/test_source_quality_wiring.py`, and verify the naive timestamp test fails with TypeError; revert to pass.

## Implementation Notes
- Ensure both `Z` replacements and naive ISO strings are normalized to timezone-aware UTC in `src/fine_art_archive/quality/source_quality.py`.
