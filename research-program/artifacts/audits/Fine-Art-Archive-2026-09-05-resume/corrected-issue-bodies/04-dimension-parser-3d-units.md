## Why
In `src/fine_art_archive/parsers/dimension_utils.py:25-78`, `parse_dimension_pair()` matches dimension pairs using regular expression `DIMENSION_PAIR_TOKEN` and selects unit via `unit = (second_unit or first_unit or "cm").lower()`. When given 3D physical dimension strings with a trailing unit such as `"535 x 463 x 52 mm"`, the regex captures the first two numbers (`535` and `463`) with empty unit groups because `"mm"` is attached to the third number (`52 mm`). The function defaults to `"cm"`, parsing the dimension as `(463.0, 535.0)` cm instead of `(46.3, 53.5)` cm. This 10x error causes `dim_compat("53.5 x 46.3 cm", "535 x 463 x 52 mm")` to report `"mismatch"` (relative difference 0.90), failing duplicate detection for 3D or framed museum objects.

## Scope
- `src/fine_art_archive/parsers/dimension_utils.py`
- `tests/test_dimension_utils.py`

## Non-Goals
- Scaffold-only completion does NOT count: returning hardcoded conversions for mm without handling 3D depth dimensions (`H x W x D`) in regex matching is a failure of this issue.
- Do not change the 5% relative tolerance threshold in `dim_compat()`.

## Tasks
- [ ] Update `DIMENSION_PAIR_TOKEN` and parsing in `src/fine_art_archive/parsers/dimension_utils.py` to recognize optional depth dimensions (`x <depth> <unit>`) and capture trailing units.
- [ ] Add unit tests in `tests/test_dimension_utils.py` verifying 3D dimension strings with trailing mm, cm, and in units convert to cm correctly and match 2D equivalent dimensions.

## Acceptance Criteria
- `pytest tests/test_dimension_utils.py` passes.
- `parse_dimension_pair("535 x 463 x 52 mm")` returns `(46.3, 53.5)` in cm.
- `dim_compat("53.5 x 46.3 cm", "535 x 463 x 52 mm")[0]` returns `"match"`.
- Deliberate break: revert regex in `src/fine_art_archive/parsers/dimension_utils.py`, run `pytest tests/test_dimension_utils.py`, and verify the 3D unit test fails; revert to pass.

## Implementation Notes
- Allow optional `(?:\s*[×x]\s*\d+(?:[.,]\d+)?\s*(cm|mm|m|in|inch|inches)?)?` in `src/fine_art_archive/parsers/dimension_utils.py` and inspect all matched unit groups.
