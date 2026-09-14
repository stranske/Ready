## Why

Current missing workflow: `ui/app.py:9` and `ui/app.py:14` import/register five pages without alerts. `ui/alerts.py:462` already implements rule creation, alert history and statistics. `ui/dashboard.py:1208` renders an Alerts badge as static text. Browser navigation confirmed no Alerts link in the full app, so operators cannot reach the implemented rule and inbox workflow through the supported launcher.

## Scope

Full analyst application navigation and dashboard Alerts affordance; offline demo remains intentionally restricted.

## Non-Goals

Do not add Alerts to the offline WASM build or rebuild the existing alert API. Scaffold-only completion does NOT count: adding badge styling without a working registered destination is a failure of this issue.

## Tasks

- [ ] Import and register `ui/alerts.py` in the full navigation in `ui/app.py` with a stable alerts URL.
- [ ] Connect the Alerts affordance in `ui/dashboard.py` to the registered destination while retaining its count.
- [ ] Extend `tests/test_ui_navigation.py` to assert Alerts registration and a runtime navigation path; retain existing offline page expectations in `tests/test_wasm_demo_build.py`.

## Acceptance Criteria

- [ ] pytest tests/test_ui_navigation.py tests/test_ui_alerts.py tests/test_wasm_demo_build.py must pass; a browser smoke must navigate from Dashboard to Alerts and display the existing rule and inbox controls with a synthetic API backend.
- [ ] Deliberate-break gate: Remove Alerts registration from `ui/app.py`; the new Alerts navigation test in `tests/test_ui_navigation.py` must fail; restore registration and rerun.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Closed issue 710 implemented the page, not its current multipage-shell registration. Do not remove the badge as a substitute for restoring access to the implemented workflow.
