# D3 unblock sweep — 2026-10-18T03

**Run budget:** Covered the first eight `SUPPORTED_REPOS` entries (Orchestrator skipped by scope): Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data. **Deferred** (cap): Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

**Offload constraint:** GitHub mutations (issue bodies, labels, PR labels, comments, PRs) were not applied; table rows are **proposed** repairs/reroutes.

| Repo | Frozen found / repair disposition | Left for owner | Stalled PR reroute | Default-branch state | Agent-ready supply |
|---|---|---|---|---|---:|
| Workflows | Eight `agents:auto-pilot-pause` (no `needs-human`). **#4068, #4051, #3999, #3986, #3978, #3898** — format-guard attempt cap; bodies need concrete tasks + runnable acceptance (mechanical edit, then remove pause). **#4068** also has open **PR #4069** (implementation in flight; unpause issue body still worthwhile). **#3901** — pause after merged work with durable verifier **NON_PASS**; needs human disposition, not blind unpause. | **#3987** — Invite/Codex lane: branch `codex/issue-3987` exists; **owner must author the PR** (Codex will not open it). | None (`agent:*` open PRs all updated <4h or already carry `agent:auto`). | No workflow literally named `CI`/`Gate` on `main` in recent history; adjacent automation (e.g. Gate Fork Status Publisher) green on latest sample. | 42 |
| Travel-Plan-Permission | None. | None. | None. | Latest **Agents Gate Followups** on `main` success (2026-10-18T02:53Z). | 5 |
| Trend_Model_Project | **#6081, #6080** — `agents:auto-pilot-pause` + format stall; underlying claims **refuted** at tip (see REFUTED). Proposed: remove pause; on **#6080** also drop `status:in-progress` for opener selection. | None. | None. | Latest **CI** on `main` success (2026-10-17T19:51Z). | 10 |
| Portable-Alpha-Extension-Model | None. | None. | None. | **Red:** latest **CI** failed — Black would reformat `tests/test_wizard_render_coverage.py` (mechanical format-only fix). | 17 |
| Counter_Risk | None. | None. | None. | Latest **Agents Gate Followups** success (2026-10-17T19:45Z); latest **CI** success. | 1 |
| Manager-Database | **#1773** — optimizer pause (missing checkbox tasks + runnable acceptance); body repairable mechanically, not applied in offload. | None. | None. | **Red:** latest **CI** failed — `tests/test_chain_postgres_integration.py` (`sqlglot`: unknown dialect `postgresql`; schema/column errors). Product/integration defect → file/fix via issue, not a sweep guess. | 11 |
| Inv-Man-Intake | None. | None. | None. | **Red:** latest **Gate Fork Status Publisher** failed (`Expected one open PR at Gate head …; found 0`). Promotion/state mismatch, not consumer product code. Latest **CI** on `main` still success. | 2 |
| Pension-Data | None. | None. | None. | Latest **Agents Keepalive Sweep** / **CI** sample green. | 6 |

### Genuinely needs the owner

- **Workflows #3987** — Open the human-authored PR from `codex/issue-3987` so the Invite lane can proceed; automation will not create it.

### Silent claims (1b)

Proposed label release (`status:in-progress` / `agent:*` where stale **>12h**, no open repo PR referencing the issue):

- **Workflows #3691** — last update 2026-10-04; `status:in-progress` + `agent:auto`; no open PR reference (consumer-sync to excluded Collab-Admin scope — still a stale claim on Workflows).
- **Workflows #3978** — `status:in-progress` + format cap only.
- **Workflows #3988** — `agent:gemini`, ~23h; branch only, no PR.
- **Workflows #3713** — `agent:retry`, ~20h; audit comment only.
- **Workflows #4026** — `status:in-progress` + `agents:formatted`, ~14h; format optimizer still failing (path citations missing `.github/scripts/` prefix); fix body **or** release claim so opener is not blocked.

**Do not release:** **#3987** (owner PR author). **#3977** (active closer 48h post-merge measurement). **#4036** (<12h). **Manager-Database #1792** (open **PR #1813**). **#1786**, **Pension-Data #964** (<12h).

### Priority labels (`priority:*` / open issues, limit 100)

Workflows 40/58; Travel-Plan-Permission 5/9; Trend_Model_Project 11/13; Portable-Alpha-Extension-Model 17/19; Counter_Risk 1/3; Manager-Database 11/14; Inv-Man-Intake 2/4; Pension-Data 6/8.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6081 — ledger repair #6082 merged; sample ledger `.agents/issue-4848-ledger.yml` at `main` has `base: main`.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6080 — `hypothesis` is under `[project.optional-dependencies] dev` at live `main`, not runtime.

**Judgment (confidence ~0.85):** Highest leverage unchanged from prior pass — mechanical issue-body repair on Workflows format-cap rows and Manager-Database #1773, unpause Trend #6080/#6081 after REFUTED, Black-only fix on Portable-Alpha `main`. Manager-Database CI and Inv-Man-Intake Gate publisher failures are not one-line mechanical greens without targeted code or Workflows promotion repair. Would revise if a newer `main` CI run succeeds or Gate head gains a matching open PR.
