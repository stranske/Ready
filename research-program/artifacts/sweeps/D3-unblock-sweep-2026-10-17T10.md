# D3 unblock sweep — 2026-10-17T10

Covered (first eight entries in `SUPPORTED_REPOS`): Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data. Deferred by the eight-repository cap: Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic. Orchestrator excluded by scope; Collab-Admin not inspected (owner exclusion).

**Constraint:** OFFLOAD WORKSPACE RULES prohibit GitHub mutations (labels, issue bodies, PR labels, comments). Findings are proposed actions, not completed repairs or reroutes.

| Repo | Frozen found / repair disposition | Left for owner | Stalled PR reroute | Default-branch state | Agent-ready supply |
|---|---|---|---|---|---:|
| Workflows | Seven `agents:auto-pilot-pause` issues. **#3999, #3986, #3898, #3978** — format-guard cap; bodies need concrete paths/tasks and runnable acceptance (mechanical edit + unpause). **#4027** — same guard, but **open PR #4028** implements and closes it; sync issue body from PR or unpause after merge; do not release claim while #4028 is open. **#3901** — pause stale vs merged #3902 and owner verifier disposition; needs human triage before unpause, not a blind format fix. | **#3987** — Invite flow requires a **human-authored PR** on `codex/issue-3987`; Codex will not open it. | None (`agent:*` PRs updated within 4h; #4030 already has `agent:auto`). | Latest Gate/CI sample green (e.g. Maint 46 Post CI success). | 33 |
| Travel-Plan-Permission | None (`needs-human` / pause). | None. | None. | Latest **CI** on `main` success; latest **Gate Fork Status Publisher** failed (`Expected one open PR at Gate head …; found 0`) — workflow/state mismatch, not a one-line product fix. | 5 |
| Trend_Model_Project | **#6081, #6080** — still carry `agents:auto-pilot-pause`; prerequisites refuted at tip (see REFUTED). Proposed: remove pause (and `status:in-progress` on #6080) after confirming no open PR. | None. | None. | Latest Gate/CI sample success. | 10 |
| Portable-Alpha-Extension-Model | None. | None. | None. | **Red:** latest **CI** on `main` failed — Black would reformat `tests/test_wizard_render_coverage.py` (mechanical format PR; not opened in offload). Gate Fork Status Publisher also failing with orphan Gate head (same class as TPP). | 14 |
| Counter_Risk | None. | None. | None. | Latest Gate Fork Status Publisher success. | 6 |
| Manager-Database | **#1773** — pause: missing task checkboxes and runnable acceptance; mechanically body-repairable, not applied. | None. | None. | Latest Gate/CI sample success. | 15 |
| Inv-Man-Intake | None. | None. | None. | Latest **CI** success. | 6 |
| Pension-Data | None. | None. | None. | Latest **CI** success; latest **Gate Fork Status Publisher** failed (orphan Gate head, same as TPP). | 7 |

**Silent claims (1b):** Proposed label release on **Workflows #3691** (`status:in-progress` + `agent:auto`, last update 2026-10-04, no open Workflows PR) — stale Collab-Admin sync-review claim. Do **not** release **#4027** (open **#4028**). **#3988** (`agent:gemini`, in-progress) updated ~7h ago — not silent.

**Priority labels (open impl candidates / `priority:*`):** Workflows 33/25 (gaps include #4011, #3999, #3908, #3723, #3579, #3558, #3557, #3549); Travel-Plan-Permission 5/5; Trend_Model_Project 12/9 (#6081); Portable-Alpha-Extension-Model 16/14; Counter_Risk 8/6; Manager-Database 18/14 (#1773); Inv-Man-Intake 8/6; Pension-Data 10/7. Inventory only — tracker/sync rows may lack `priority:*` by design.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6081 — prerequisite ledger repair #6082 merged; stale-base blocker no longer holds at live tip.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6080 — `hypothesis` is dev-only and cited focused tests exist at live tip.

**Judgment:** The highest-leverage unblock is still mechanical issue-body repair on Workflows #3999/#3986/#3898/#3978 and Manager-Database #1773, plus a formatting PR on Portable-Alpha-Extension-Model `main`. Gate Fork Status Publisher failures on TPP/Pension-Data/PAEM look like **missing open PR at recorded Gate SHAs** — fixing consumer product code will not green those runs; needs workflow or promotion-state repair (likely upstream Workflows/Maint), not guessed edits here.
