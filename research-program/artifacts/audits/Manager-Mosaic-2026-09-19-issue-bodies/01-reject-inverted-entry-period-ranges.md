## Why

`validate()` confirms that `Entry.first` and `Entry.last` each name an existing period (`src/manager_mosaic/model.py:349-364`), but it never checks their chronological order. `_period_in_range()` then tests `first.sort <= period.sort <= last.sort` (`src/manager_mosaic/model.py:443-452`), so a hand-edited entry with `first.sort > last.sort` has no active periods and `derive_gaps()` returns no coverage gaps. This is a current correctness break: an inverted range validates as clean and suppresses the silence-as-gap safeguard.

## Scope

Reject inverted entry ranges in the semantic validator and cover the resulting diagnostic with the model validation tests.

## Non-Goals

- Do not change the silence-is-not-a-status-change behavior of `derive_gaps()`.
- Do not redesign period labels, the JSON schema, or document/evidence validation.
- Scaffold-only completion does not count: adding a placeholder check without the named failing regression test and deliberate-break evidence is incomplete.

## Tasks

- [ ] In `src/manager_mosaic/model.py`, extend `validate()` after both entry period references resolve to report a `ValidationViolation` when the resolved `first.sort` is greater than `last.sort`.
- [ ] In `tests/test_model_validation.py`, add `test_inverted_entry_period_range_is_reported` using the checked-in `tests/fixtures/model/minimal_store.json` payload with its entry range inverted.
- [ ] In `tests/test_model_validation.py::test_inverted_entry_period_range_is_reported`, temporarily remove or invert the new ordering condition, confirm that this exact test fails, then revert the deliberate break before committing.

## Acceptance Criteria

- [ ] `python3 -m pytest -q --no-cov tests/test_model_validation.py::test_inverted_entry_period_range_is_reported` passes and asserts that an inverted range creates a violation rather than silently validating.
- [ ] The deliberate break that disables the new `src/manager_mosaic/model.py` ordering check makes `tests/test_model_validation.py::test_inverted_entry_period_range_is_reported` fail; the change is reverted and the named test passes again.
- [ ] `python3 -m pytest -q --no-cov tests/test_model_validation.py` passes.

## Implementation Notes

At the audited tip, an entry with `first="2024Q2"` and `last="2024Q1"` returns `validate(store) == []` and `derive_gaps(store) == ()`; the ordered control returns coverage gaps. Preserve the validator's existing all-violations-in-one-pass behavior.
