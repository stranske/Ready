Reject non-finite notional_change in top_changes (#1085)

* fix(compute): reject non-finite notional_change in top_changes

Guard top_changes against NaN/Infinity notional_change inputs so
absolute_change sort order cannot be corrupted by non-finite values.

Closes #1085

Co-authored-by: Cursor <cursoragent@cursor.com>

* fix(compute): reject derived notional overflow

---------

Co-authored-by: Cursor <cursoragent@cursor.com>
