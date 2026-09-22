# PR #704

## Summary
- Add shared `optional_int` / `optional_float` helpers in `src/lms/ui/forms.py` with `FormValueError` for unparsable or non-finite input.
- Delegate the five unguarded `_optional_*` copies in `api.py`, `graph_design.py`, `feedback.py`, and `attempts.py`, and align `capability_gap.py` to the shared helper while preserving blank/invalid → `None` behavior for threshold defaults.
- Catch `FormValueError` in the five posting routes so non-numeric form values render validation notices instead of HTTP 500.

Closes #693

## Test plan
- [x] `uv run pytest tests/ui/test_form_coercion.py -q` — 3 passed (non-numeric confidence no-500, blank field → None, helper rejects abc)
- [x] `uv run pytest tests/ui -q` — 189 passed, 1 skipped
- [x] Deliberate-break gate: reverting `optional_int` to bare `return int(value)` fails `test_non_numeric_confidence_does_not_500`; restored guard passes all three tests

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

* **New Features**
  * Added consistent handling for optional numeric form fields, including blank values and valid integer or decimal inputs.
  * Added clear validation messages for invalid or non-finite numeric entries.

* **Bug Fixes**
  * Invalid values now prevent submissions from being saved and preserve entered form data where applicable.
  * Failed submissions now roll back safely and return an appropriate validation response.

* **Tests**
  * Added coverage for numeric input validation across attempts, feedback, graph data, and knowledge-related forms.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->

<!-- pr-preamble:start -->
<!-- meta:issue:693 -->
> **Source:** Issue #693

Closes #693

<!-- pr-preamble:end -->

<!-- auto-status-summary:start -->
## Automated Status Summary
#### Scope
Five UI form-coercion helpers call `int()` / `float()` on raw request-body text without a guard, so non-numeric posted form values raise unhandled `ValueError` exceptions and return HTTP 500. A hardened copy already exists at `src/lms/ui/capability_gap.py:892-899`, making this divergence between copies.

The unguarded helpers are `_optional_float` in `src/lms/ui/api.py:1920-1923` and `src/lms/ui/graph_design.py:440-443`, plus `_optional_int` in `src/lms/ui/api.py:1418-1421`, `src/lms/ui/feedback.py:436-439`, and `src/lms/ui/attempts.py:589-592`. They receive untrusted text from `_read_form` (`src/lms/ui/api.py:1424-1426`) and no `ValueError` handler exists in `src/lms/main.py`.

Posting `confidence=abc` to the attempt-recording form at `src/lms/ui/api.py:717` currently returns HTTP 500 rather than re-rendering with a validation notice. This is a current learner-UI break.

#### Tasks
- [ ] Add shared `optional_int(value: str | None) -> int | None`, `optional_float(value: str | None) -> float | None`, and `FormValueError` in a UI-importable module such as `src/lms/ui/forms.py`; strip whitespace, return `None` for blank input, and raise `FormValueError` for unparsable input.
- [ ] Update `_optional_float` in `src/lms/ui/api.py:1920` and `src/lms/ui/graph_design.py:440` to delegate to the shared helper.
- [ ] Update `_optional_int` in `src/lms/ui/api.py:1418`, `src/lms/ui/feedback.py:436`, and `src/lms/ui/attempts.py:589` to delegate to the shared helper.
- [ ] Update `_optional_float` in `src/lms/ui/capability_gap.py:892` to use the shared helper while preserving return-`None` behavior for invalid input where required by callers.
- [ ] Add `FormValueError` handling to the posting routes at `src/lms/ui/api.py:204`, `src/lms/ui/api.py:717`, `src/lms/ui/graph_design.py:98`, `src/lms/ui/feedback.py:194`, and `src/lms/ui/attempts.py:94` using each module’s existing error-notice rendering.
- [ ] Add route-level non-numeric submission tests for the attempt and feedback surfaces in `tests/ui/test_form_coercion.py`.

#### Acceptance criteria
- [ ] `tests/ui/test_form_coercion.py::test_non_numeric_confidence_does_not_500` posts `confidence_rating=abc` to the attempt-recording route and asserts a non-5xx response containing validation-notice text.
- [ ] `tests/ui/test_form_coercion.py::test_blank_numeric_field_is_treated_as_absent` posts empty `confidence_rating` and asserts the request succeeds with the value stored as `None`.
- [ ] `tests/ui/test_form_coercion.py::test_optional_int_rejects_non_numeric` asserts the shared helper raises `FormValueError` for `"abc"` and returns `None` for `""` and `None`.
- [ ] Replacing guarded `optional_int` with `return int(value)` causes `uv run pytest tests/ui/test_form_coercion.py -q` to fail `test_non_numeric_confidence_does_not_500` with unhandled `ValueError`; after restoring the guard, all three tests pass.
- [ ] `uv run pytest tests/ui -q` passes with no new failures.
- [ ] `grep -rn "return int(value)\|return float(value)" src/lms/ui/` returns no matches.

<!-- auto-status-summary:end -->