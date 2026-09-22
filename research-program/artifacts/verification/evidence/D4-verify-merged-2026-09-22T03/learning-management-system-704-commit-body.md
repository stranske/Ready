Consolidate UI numeric form coercion onto one guarded helper (#704)

* fix(ui): consolidate numeric form coercion onto guarded helpers

Shared optional_int/optional_float raise FormValueError for bad input so
learner and author posting routes render validation notices instead of 500s.

Co-authored-by: Cursor <cursoragent@cursor.com>

* test(ui): cover float and feedback form coercion

* fix(ui): preserve response text and catch schema validation on learn route

Catch Pydantic ValidationError when confidence parses but fails range checks,
render submitted response_text on numeric validation errors for both learn and
attempt surfaces, and extend form-coercion tests for /learn/attempts coverage.

Co-authored-by: Cursor <cursoragent@cursor.com>

---------

Co-authored-by: Cursor <cursoragent@cursor.com>
