## Why

When selected run-end metadata is absent, `dashboard/pages/7_Run_Logs.py:59` falls back to the working-directory manifest at line 61. A real Streamlit AppTest selects run-selected but displays a manifest identifying WRONG_UNRELATED_RUN. There is no identity check at the display point, line 68. Closed #1901 addressed session handoff; this is a separate incorrect-provenance fallback.

## Scope

Keep Run Logs provenance bound to the selected run. First-party ui behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] In `dashboard/pages/7_Run_Logs.py`, only show a manifest explicitly attributable to the selected run; show the existing missing-manifest guidance when attribution cannot be established.
- [ ] Extend `tests/test_dashboard_run_logs_page.py` using real AppTest or equivalent runtime observation: selected run without run_end, unrelated root manifest, valid linked manifest, missing linked file, and a malformed run_end.

## Acceptance Criteria

- [ ] Selecting a run without a valid linked manifest never displays an unrelated root manifest; a valid explicit link still displays its own provenance.
- [ ] Run `pytest tests/test_dashboard_run_logs_page.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Restore the cwd glob fallback; the wrong-run marker test must fail; revert.

## Implementation Notes

Severity P2. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
