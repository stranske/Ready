## Why

`FactRecord.period` accepts any string (`src/manager_mosaic/discrepancy.py:13-23`), while `_period_chronology_key()` recognizes only `YYYYQn` and `Qn YYYY` (`src/manager_mosaic/thesis.py:25-34`). Every other accepted label is ranked as `(0, 0, label)`, so `evaluate_claim()` selects `2024Q4` over a later accepted `2025-Q1` record (`src/manager_mosaic/thesis.py:72-75`). This is a current correctness break: a later contradictory fact can be silently ignored because its period label is not parsed.

## Scope

Make thesis chronology safe for non-current quarter spellings by parsing the supported hyphenated quarter form or rejecting unsupported labels before verdict selection.

## Non-Goals

- Do not add date libraries, fiscal-calendar configuration, or broad natural-language date parsing.
- Do not change same-period conflict policy; that is handled separately from this chronology boundary.
- Scaffold-only completion does not count: accepting an unparsed string or adding a TODO without the named regression and deliberate-break evidence is incomplete.

## Tasks

- [ ] In `src/manager_mosaic/thesis.py::_period_chronology_key`, support `YYYY-Qn` alongside the currently supported quarter labels, or make `evaluate_claim` reject labels the helper cannot order.
- [ ] In `tests/test_thesis_monitoring.py`, add `test_evaluate_claim_selects_hyphenated_later_quarter` with supported `2024Q4` evidence and later `2025-Q1` contradictory evidence.
- [ ] In `tests/test_thesis_monitoring.py::test_evaluate_claim_selects_hyphenated_later_quarter`, temporarily remove the new hyphenated-label parsing or validation, confirm the named test fails, then revert the deliberate break before committing.

## Acceptance Criteria

- [ ] `python3 -m pytest -q --no-cov tests/test_thesis_monitoring.py::test_evaluate_claim_selects_hyphenated_later_quarter` passes and uses the later `2025-Q1` evidence for the thesis verdict.
- [ ] The deliberate break that disables the new `src/manager_mosaic/thesis.py` hyphenated-label handling makes `tests/test_thesis_monitoring.py::test_evaluate_claim_selects_hyphenated_later_quarter` fail; it is reverted and the named test passes again.
- [ ] `python3 -m pytest -q --no-cov tests/test_thesis_monitoring.py` passes.

## Implementation Notes

Keep the existing `YYYYQn` and `Qn YYYY` behavior covered by `tests/test_thesis_monitoring.py`. A fail-closed rejection is acceptable for formats outside the explicitly supported set, but a raw lexical fallback must not supply a thesis verdict.
