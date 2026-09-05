## Why
In `scripts/build_manifest.py:111-124`, `_row()` extracts `"year": _text(meta.get("year"))` for CSV generation. In the archive schema (`schemas/meta.schema.json`) and sidecars, approximate or range-dated artworks frequently leave `year` as `null` while recording `year_min: 1565` and `year_max: 1568`. When `scripts/build_manifest.py` processes these sidecars, it writes an empty string to the `year` column in `manifest.csv`. In the Companion App UI and `/works` endpoint, these artworks appear with a blank year.

## Scope
- `scripts/build_manifest.py`
- `tests/test_build_manifest.py`

## Non-Goals
- Scaffold-only completion does NOT count: modifying the sidecar files on disk instead of implementing the `year_min` fallback during manifest row serialization is a failure of this issue.
- Do not change column ordering in `COLUMNS`.

## Tasks
- [ ] Update `_row()` in `scripts/build_manifest.py` to fall back to `meta.get("year_min")` when `meta.get("year")` is absent.
- [ ] Add unit tests in `tests/test_build_manifest.py` verifying `_row()` outputs `year_min` when `year` is None.

## Acceptance Criteria
- `pytest tests/test_build_manifest.py` passes with all tests green.
- Calling `_row("test-wid", {"title": "Tower of Babel", "year": None, "year_min": 1563})` produces a row dictionary with `"year": "1563"`.
- Deliberate break: remove `year_min` fallback in `scripts/build_manifest.py`, run `pytest tests/test_build_manifest.py`, and verify test failure; revert to pass.

## Implementation Notes
- Align `_row()` in `scripts/build_manifest.py` with `_clean(meta.get("year")) or _clean(meta.get("year_min"))` from `src/fine_art_archive/crosswalk.py`.
