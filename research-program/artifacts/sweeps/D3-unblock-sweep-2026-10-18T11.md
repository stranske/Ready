# D3 unblock sweep — 2026-10-18T11

**Run budget:** Covered the first eight `SUPPORTED_REPOS` entries (Orchestrator skipped by scope): Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data. **Deferred** (cap): Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

**Offload constraint:** GitHub mutations (issue bodies, labels, PR labels, comments, PRs) were not applied; table rows are **proposed** repairs/reroutes.

| Repo | Frozen found / repair disposition | Left for owner | Stalled PR reroute | Default-branch state | Agent-ready supply |
|---|---|---|---|---|---:|
| Workflows | Eight `agents:auto-pilot-pause` (no `needs-human`). **#4051, #3999, #3986, #3978, #3898** — format-guard attempt cap; bodies need concrete tasks + runnable acceptance, then remove pause. **#4082** — new; detailed body but `agents-issue-optimizer` workflow **failed** (not format cap); verify optimizer log before unpause. | **#3987** — Invite/Codex lane: branch `codex/issue-3987` exists; **owner must author the PR** (Codex will not open it). **#3901** — pause after merged work with durable verifier **NON_PASS**; needs human disposition, not blind unpause. | None (`agent:*` open PRs all updated <4h or lack `agent:*`). | Recent `main` automation sample green (e.g. Agents 70 Orchestrator 2026-10-18T11:11Z); no completed `CI`/`Gate` failure in latest five `main` runs. | 36 |
| Travel-Plan-Permission | None. | None. | None. | Latest **Auto-merge documentation PRs** on `main` success (2026-10-18T11:10Z). | 5 |
| Trend_Model_Project | **#6081, #6080** — `agents:auto-pilot-pause`; underlying claims **refuted** at tip (see REFUTED). Proposed: remove pause; on **#6080** also drop `status:in-progress` for opener selection. | None. | None. | Latest **Agents PR Health** on `main` success (2026-10-18T11:10Z). | 9 |
| Portable-Alpha-Extension-Model | None. | None. | None. | **Red:** latest **CI** failed (2026-10-18T11:01Z) — Black would reformat `tests/test_wizard_render_coverage.py` (mechanical format-only fix). | 17 |
| Counter_Risk | None. | None. | None. | Latest **Agents PR Health** success (2026-10-18T11:11Z). | 1 |
| Manager-Database | **#1773** — optimizer pause (missing runnable acceptance + path citations); body repairable mechanically, not applied in offload. | None. | None. | **Red:** latest **CI** failed (2026-10-18T07:56Z) — `tests/test_chain_postgres_integration.py`: sqlglot `Unknown dialect 'postgresql'` (suggest `postgres`; product/test fix, not a one-line sweep guess without PR). **Agents Gate Followups** latest success (2026-10-18T10:31Z). | 10 |
| Inv-Man-Intake | None. | None. | None. | Latest **Gate Fork Status Publisher** / **Agents PR Health** on `main` success (2026-10-18T06:00Z / 11:10Z). Prior promotion mismatch appears cleared. | 2 |
| Pension-Data | None. | None. | None. | Latest **Gate Fork Status Publisher** green (2026-10-18T11:12Z). | 6 |

### Genuinely needs the owner

- **Workflows #3987** — Open the human-authored PR from `codex/issue-3987` so the Invite lane can proceed; automation will not create it.
- **Workflows #3901** — Decide how to handle durable post-merge verifier **NON_PASS** after #3902; do not unpause for blind re-dispatch.

### Silent claims (1b)

Proposed label release (`status:in-progress` / `agent:*` where stale **>12h**, no open repo PR referencing the issue):

- **Workflows #3691** — last update 2026-10-04; `status:in-progress` + `agent:auto`; no open PR reference (consumer-sync scope; still a stale claim on Workflows).
- **Workflows #3978** — `status:in-progress` + format cap only.
- **Workflows #3988** — `agent:gemini`, ~31h; branch only, no PR.
- **Workflows #3713** — `agent:retry`, ~28h; audit comment only.
- **Workflows #4026** — `status:in-progress` + `agents:formatted`, ~27h; format guard cites missing `.github/scripts/` path prefixes — fix body **or** release claim so opener is not blocked.
- **Manager-Database #1791** — `agent:muse`, ~20h; no open PR (distinct from active **#1792** / PR #1813).
- **Manager-Database #1786** — `status:in-progress`, ~13h stale; no open PR reference.
- **Pension-Data #964** — `agent:muse`, ~20h; no open PR.

**Do not release:** **#3987** (owner PR author). **#3977** (active post-merge Gate measurement window). **#4036** (<12h, updated 2026-10-18T02:46Z). **Manager-Database #1792** (open **PR #1813**).

### Priority labels (`priority:*` / open issues, limit 100)

Workflows 43/59; Travel-Plan-Permission 5/9; Trend_Model_Project 11/13; Portable-Alpha-Extension-Model 17/19; Counter_Risk 1/3; Manager-Database 11/14; Inv-Man-Intake 2/4; Pension-Data 6/8.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6081 — no `base: phase-3` ledger entries remain on `main` (code search 2026-10-18); sample `.agents/issue-4848-ledger.yml` has `base: main`.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6080 — `hypothesis` is under `[project.optional-dependencies] dev` at live `main`, not runtime.

**Judgment (confidence ~0.88):** Highest leverage unchanged — mechanical issue-body repair on Workflows format-cap rows and Manager-Database #1773, unpause Trend #6080/#6081 after REFUTED, Black-only fix on Portable-Alpha `main`. Manager-Database CI needs a deliberate `postgresql`→`postgres` (or dialect wiring) fix, not a blind sweep patch. Inv-Man-Intake Gate publisher is green again on latest sample. Would revise if a newer `main` CI run succeeds on Manager-Database or Workflows #4082 optimizer failure is traced to a transient workflow bug.
