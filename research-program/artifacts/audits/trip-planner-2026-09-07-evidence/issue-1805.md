# [P2] Exception-nearest scenario preview must key off exception_nearest label not hyphenated note

## Why

`trip_planner/app/services/scenario_policy_preview.py:143-144` only adds the `POL-EXC` preview when scenario notes contain the literal `"exception-nearest"`. Canonical scenario labels use underscore form `exception_nearest` (`trip_planner/state/scenarios.py:21`, saved fixture `trip_planner/resources/state/scenarios/business_compliant_vs_exception.json:52`). Runtime search notes are prose (`trip_planner/itinerary/search.py:272-290`), so exception-nearest scenarios usually skip the preview unless a seeded hyphenated note is present (`trip_planner/app/services/workspace.py:346`).

## Scope

Exception-path preview detection in `trip_planner/app/services/scenario_policy_preview.py` and compare-row inputs from `trip_planner/app/services/workspace.py`.

## Tasks

- [ ] Add `test_exception_nearest_saved_scenario_surfaces_pol_exc_preview_violation` in `tests/app/test_scenario_policy_preview.py` using label `exception_nearest` without the hyphenated note token.
- [ ] Pass scenario label or metadata into `build_scenario_policy_preview` from `trip_planner/app/services/workspace.py` `attach_policy_preview_to_row` instead of relying on `"exception-nearest" in notes` at `trip_planner/app/services/scenario_policy_preview.py:143`.
- [ ] Update `trip_planner/app/services/scenario_policy_preview.py` `_exception_note_violation` to detect `exception_nearest` label metadata.

## Acceptance Criteria

- `pytest tests/app/test_scenario_policy_preview.py::test_exception_nearest_saved_scenario_surfaces_pol_exc_preview_violation` passes.
- `pytest tests/app/test_scenario_policy_preview.py` passes.
- Deliberate-break → revert: restore the `"exception-nearest" in notes` check and confirm the new test fails; revert.

## Non-Goals

- Changing authoritative TPP exception approval workflow in `trip_planner/business/approval_ready.py`.
- Scaffold-only completion does NOT count: adding another magic string to notes without using scenario label metadata is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._
