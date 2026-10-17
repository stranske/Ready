# D3 unblock sweep — 2026-10-17T18

Covered (first eight entries in `SUPPORTED_REPOS`): Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data. Deferred by the eight-repository cap: Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic. Orchestrator excluded by scope; Collab-Admin not inspected (owner exclusion).

**Constraint:** OFFLOAD WORKSPACE RULES prohibit GitHub mutations (labels, issue bodies, PR labels, comments, PRs). Findings are proposed actions, not completed repairs or reroutes.

| Repo | Frozen found / repair disposition | Left for owner | Stalled PR reroute | Default-branch state | Agent-ready supply |
|---|---|---|---|---|---:|
| Workflows | Eight `agents:auto-pilot-pause` issues. **#4051, #3999, #3986, #3898, #3978** — format-guard attempt cap; bodies need runnable acceptance / concrete tasks (mechanical edit + remove pause). **#4045** — same guard, but **open PR #4048** implements; do not release in-progress claim while #4048 is open. **#3901** — pause after merged #3902 with durable verifier NON_PASS; needs human disposition, not blind unpause. | **#3987** — Invite flow: branch exists; **Codex will not open the PR**; owner must author the PR on `codex/issue-3987`. | None (no `agent:*` open PR stale >4h without `agent:auto`). | Recent Gate/CI sample green (e.g. PR 11 Minimal invariant CI success; Maint 52 Validate Workflows success). | 38 |
| Travel-Plan-Permission | None (`needs-human` / pause). | None. | None. | Latest **Agents Gate Followups** on `main` success (2026-10-17T17:11Z). | 5 |
| Trend_Model_Project | **#6081, #6080** — still `agents:auto-pilot-pause` (format/auto-pilot stall); underlying blockers refuted at tip (see REFUTED). Proposed: remove pause; on **#6080** also drop `status:in-progress` so opener can select. | None. | None. | Latest **CI** on `main` success. | 10 |
| Portable-Alpha-Extension-Model | None. | None. | None. | **Red:** latest **CI** on `main` failed — Black would reformat `tests/test_wizard_render_coverage.py` (mechanical format PR; not opened in offload). | 14 |
| Counter_Risk | None. | None. | None. | **Red:** latest **Agents Gate Followups** on `main` failed (`TypeError: classifyCompletion is not a function` in keepalive round finish) — shared workflow/script defect, not a one-line product fix here. | 1 |
| Manager-Database | **#1773** — optimizer pause: missing runnable acceptance in criteria; body repairable mechanically, not applied in offload. | None. | None. | Latest **Agents Gate Followups** success. | 11 |
| Inv-Man-Intake | None. | None. | None. | **Red:** latest **Gate Fork Status Publisher** failed (`Expected one open PR at Gate head …; found 0`) — promotion/state mismatch, not consumer product code. | 4 |
| Pension-Data | None. | None. | None. | Latest **Gate Fork Status Publisher** success. | 7 |

**Silent claims (1b):** Proposed release of stale progress labels (no open repo PR referencing the issue): **Workflows #3691** (`status:in-progress` + `agent:auto`, last update 2026-10-04). **#3978** (`status:in-progress` + pause, format cap only). **#3988** (`status:in-progress` + `agent:gemini`, >12h, branch only — invite/human-PR lane). **#3713** (`agent:retry`, >12h, audit comment only). Do **not** release **#4045** (open **#4048**). Leave **#3987** frozen (owner PR author). **#4027** not open; no action.

**Priority labels (`priority:*` / open issues):** Workflows 37/55; Travel-Plan-Permission 5/9; Trend_Model_Project 9/13; Portable-Alpha-Extension-Model 14/16; Counter_Risk 1/3; Manager-Database 11/14; Inv-Man-Intake 4/6; Pension-Data 7/9. Gaps are mostly trackers/sync rows (#4047, #4011, TPP #1494, etc.).

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6081 — ledger repair #6082 merged; sample ledger `.agents/issue-4848-ledger.yml` at `main` has `base: main`.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6080 — `hypothesis` is under `[project.optional-dependencies] dev` at live `main`, not runtime.

**Judgment:** Highest leverage remains mechanical issue-body repair on Workflows format-cap issues and Manager-Database #1773, unpause on Trend #6080/#6081 after REFUTED confirmation, and a Black-only PR on Portable-Alpha-Extension-Model `main`. Counter_Risk Gate followup failure and Inv-Man-Intake Gate publisher failure are upstream workflow/state problems (`classifyCompletion`, orphan Gate head); fixing consumer product code will not green those runs without Workflows/Maint promotion repair.
