# Counter_Risk UX evidence and handoff

Coverage is partial. [Bundle]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/bundle.json), [panel]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/report.json), [improvement hints]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/improvements.json), [gate]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/gate.json). Four evaluator rubric files and the critic are nonempty under [LOCAL_HOME]/.codex/orchestrator-mirror/ux_reviews/stranske_Counter_Risk_uxreview_2026-09-13-function-surfaces.

| Surface | Driven | Evidence or blocker |
| --- | --- | --- |
| Maintainer CLI help | yes | cli-help.txt; console entry succeeds. python -m counter_risk is not the documented entry and was discarded as a bad probe. |
| Fixture download generation | yes | demo-output and demo-proof.txt;145 operator/demo/chat tests pass. |
| GUI function control | yes, controlled runner | operator-observations.json; missing-input guidance, month-end normalization and status-label reading. No Tk visual inference. |
| Chat delta provider transport | yes, intercepted final transport | lead-chat-delta-proof.json; omitted facts. Actual LLM answer not observed. |
| Browser fixture page | no | Browser connection timed out twice; no DOM/screenshot, no browser usability conclusion. |
| Windows frozen GUI | no | No Windows host. |
| Runner.xlsm and COM | no | No Excel/PowerPoint Windows runtime. |

Raw medians: wiring4, usability6, help6, productivity6; overall3.0. Gate not done. These are function-evidence scores, not a full app rating. Aggregate chat findings are duplicates; retain one P2 draft. Reject trusted-block suggestion for untrusted delta text; preserve guarded data delimiters. Retain link-refresh-specific message wording without requiring green status. Defer date-help wording to clarify month-end behavior, rather than changing domain semantics without a contract.

The initial controlled RED summary fixture omitted the expected parenthesized color and produced empty status. That was an invalid probe, not a product defect. The corrected fixture returns RED - Do not send; operator-observations.json contains that corrected observation. The original panel bundle is preserved as its input record; no finding depends on the invalid status probe.

## Platform acceptance handoff

At source SHA 6e2a87b27be9a23d388155e37ed01675b1e27dc7, use the repo's documented portable build and launch commands from docs/gui_runner.md and run_counter_risk_gui.cmd. On Windows launch from a folder outside the repository; exercise all, ex_trend and trend modes, manual and discover inputs, ambiguous discovery selection, missing roots, a second same-date run, and Open Output/Manifest/Summary/PPT. Open Runner.xlsm and exercise all seven macros. Verify selected/effective date is explicit, newly written files open from the completed run, and RED blocks distribution operationally. Save screenshots, executed command, exit code and manifest into a dated platform-verification artifact folder.

For draft08, enable export_pdf and include_concentration_table_in_ppt together on a synthetic fixture: final PPTX and rendered PDF must contain the same concentration slide and counts; repeat with each toggle disabled. Capture real PDF pages and PowerPoint output. Browser handoff: serve web locally with python -m http.server, open index, capture DOM and screenshot and verify the fixture-only boundary; do not score real-file upload/processing that the static page does not claim to implement.
