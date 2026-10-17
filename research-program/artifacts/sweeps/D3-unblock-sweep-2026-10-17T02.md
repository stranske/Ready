# D3 unblock sweep — 2026-10-17T02

Covered (first eight eligible entries in `SUPPORTED_REPOS`): Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data. Deferred by the mandatory eight-repository cap: Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic. Orchestrator was excluded by scope; Collab-Admin was not inspected or reported.

**Constraint:** the normal sweep asks for GitHub issue-body/label and PR-label mutations, but this invocation's later OFFLOAD WORKSPACE RULES expressly prohibit all GitHub edits. Findings below are therefore proposed actions, not completed repairs or reroutes.

| Repo | Frozen issues found / repair disposition | Left for owner | Stalled PR reroute | Default-branch state | Agent-ready supply |
|---|---|---|---|---|---:|
| Workflows | #3999, #3986, #3901, #3898 have format-guard defects (missing concrete task/path or runnable acceptance) that are mechanically body-repairable; no repair applied. #3989 has an open linked PR #3997, so its claim must not be released. #3713 is an 10-day stale `agent:retry` claim with no open Workflows PR referencing it; proposed release only. | #3987 explicitly requires a human-authored PR before Codex may engage. | None qualifying (all `agent:*` PRs updated within 4h). | Latest listed run success; no latest Gate/CI failure observed. | 28 |
| Travel-Plan-Permission | None. | None. | None. | Latest listed run skipped; no failed Gate/CI observed in the five-run sample. | 5 |
| Trend_Model_Project | #6081 and #6080 retain pause labels, but their own current comments say their underlying prerequisites are already merged/fixed; left unchanged under refutation rule. | None. | None. | Latest listed run success. | 10 |
| Portable-Alpha-Extension-Model | None. | None. | None. | **Red:** CI 38994319764 failed because Black would reformat `tests/test_wizard_render_coverage.py`; mechanical formatting fix, but no PR opened. | 12 |
| Counter_Risk | None. | None. | None. | Latest listed run success. | 6 |
| Manager-Database | #1773 is paused because its tasks lack checkboxes and its acceptance lacks a runnable command; mechanically body-repairable, but not applied. | None. | None. | Latest listed run success. | 14 |
| Inv-Man-Intake | None. | None. | None. | Latest listed run success. | 6 |
| Pension-Data | None. | None. | None. | Latest listed run success. | 7 |

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6081 — its prerequisite ledger-base repair #6082 merged and the current comment records a passing post-merge preflight.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6080 — its current comment records that `hypothesis==6.155.7` is already dev-only and the cited focused tests exist.

Priority-label coverage (open non-durable/non-dependency implementation candidates / priority-labelled): Workflows 33/26 (missing #3999, #3908, #3723, #3579, #3558, #3557, #3549); Travel-Plan-Permission 5/5; Trend_Model_Project 12/10 (missing #6081, #6080); Portable-Alpha-Extension-Model 12/12; Counter_Risk 6/6; Manager-Database 15/14 (missing #1773); Inv-Man-Intake 6/6; Pension-Data 8/8. This is a label inventory, not a judgment that tracker-like sync items are runnable.

The strongest operational risk is not a missing owner decision: it is the contradictory authorization. The mechanically safe changes are identifiable, but the offload restriction prevents doing them. A normal (non-offload) sweep should first repair the three malformed bodies, then release Workflows #3713 only after rechecking PR references, and create a bounded formatting PR for Portable-Alpha-Extension-Model's red main.
