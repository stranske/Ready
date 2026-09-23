## Why (verified evidence)

`docs/audit/AUDIT_REPORT.md` and `docs/audit/REMAINING_WORK.md` still describe four BLOCKER-class defects and operator gaps that are fixed on `main` at `2f92b17`. Fleet audits and humans cite these files as live state (see dossier §11), which re-opens already-merged work and wastes dedup cycles.

- `docs/audit/AUDIT_REPORT.md:7-9` still claims `percent_of_total` limits use a mixed denominator (`compute/limits.py:195`) and HHI is wrong for mixed-sign notionals (`compute/rollups.py:576-586`). On tip, `check_limits` scopes denominators per `entity_type` at `src/counter_risk/compute/limits.py:257-286` (regression: `tests/compute/test_limits.py::test_percent_of_total_scopes_denominator_to_matching_granularity`).
- Same paragraph claims `severity:fail` breaches never escalate to RED (`pipeline/data_quality.py:20`). On tip, fail breaches set explicit `severity="fail"` at `src/counter_risk/pipeline/data_quality.py:271-287` and `_derive_overall_status` returns `"fail"` at `:431-434` (`tests/pipeline/test_manifest_data_quality.py` asserts RED mapping).
- `docs/audit/AUDIT_REPORT.md:9` still says `Runner.xlsm` buttons are inert text and the GUI freezes on the Tk main thread. Shipped workbook has Form-Control macros (`xl/drawings/vmlDrawing1.vml`); GUI runs the pipeline on a worker thread at `src/counter_risk/gui/runner.py:616`.
- `docs/audit/REMAINING_WORK.md:16-29` lists #6 (XLSM buttons) and #7 (GUI `input()` discover) under **NOT yet done** although both are resolved on tip.

User-facing consequence: operators and agents treat the monthly reporting pipeline as broken when the cited BLOCKERs are already fixed; open issues get duplicated or dropped incorrectly.

## Tasks

- [ ] Add a prominent historical banner at the top of `docs/audit/AUDIT_REPORT.md` (after the title) stating the report is superseded as of 2026-09-23, naming the merged fix arcs (#1081–#1090, #1103–#1107), and pointing readers to `docs/PRODUCT_CONTRACT.md` plus GitHub issues for current gaps.
- [ ] Add the same banner pattern to `docs/audit/REMAINING_WORK.md` and replace the "NOT yet done" BLOCKER rows (#6, #7, #9, #10, #17) with a short "resolved on main" note or remove them from the active section.
- [ ] Add `tests/docs/test_audit_log_historical.py::test_in_repo_audit_logs_marked_historical` that reads both files and asserts each contains the superseded banner text (so the banner cannot be removed silently).

## Acceptance Criteria

- Named test: `pytest tests/docs/test_audit_log_historical.py::test_in_repo_audit_logs_marked_historical -q` passes.
- Deliberate-break → revert: remove the banner line from `docs/audit/AUDIT_REPORT.md` → confirm `test_in_repo_audit_logs_marked_historical` FAILS → revert → passes.

## Non-Goals

- Do NOT rewrite the full 2026 audit narrative body in this issue; only stamp supersession and excise active BLOCKER lists that contradict `main`.
- Do NOT change pipeline/runtime code or `.github/` synced workflows.
- No scaffolding / TODO-only changes; every task is a concrete doc or test edit verified by the gate above.

_Surfaced by Track D audit 2026-09-23; verified by reading cited paths on tip `2f92b17`._
