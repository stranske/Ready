## Why

Fleet coverage initiative round 8 remains below the 90% objective. The next slice must prove real validation branches in preset import helpers, not pad the metric.

## Scope

Add a discriminating regression in `tests/test_preset_library.py` for uncovered duplicate-ID and key-mismatch validation in `pa_core/presets.py`.

## Non-Goals

- Do NOT change CI or workflow configuration.
- Do NOT add trivial getter or import-only tests.

## Tasks

- [ ] Run `pytest tests/test_preset_library.py --cov=pa_core/presets.py --cov-report=term-missing` and record baseline in the PR body.
- [ ] In `tests/test_preset_library.py`, add regressions for duplicate preset IDs and key/id mismatch rejection in `PresetLibrary.load_yaml_str` and `PresetLibrary.load_json_str` in `pa_core/presets.py`, and record deliberate-break plus measured coverage delta in the PR body.

## Acceptance Criteria

- [ ] `pytest tests/test_preset_library.py --cov=pa_core/presets.py --cov-report=term-missing` exits 0 with measured coverage delta recorded in the PR body.
- [ ] The new regressions fail when their selected validation branch is deliberately broken, then pass after revert; both recorded in the PR body.

## Implementation Notes

Coverage-autopilot round 8; low blast radius only. If measured coverage is already at or above 90%, comment and close without opening a PR.
