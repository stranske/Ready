# D3 unblock sweep — 2026-10-21T20 (attempt 1)

**Run budget:** Covered the first eight `SUPPORTED_REPOS` entries (Orchestrator skipped by scope): Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data. **Deferred** (cap): Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

**Offload constraint:** No GitHub mutations (issue bodies, labels, PR labels, comments, PRs). Findings are live `gh` API + shallow clones; **proposed** repairs/reroutes for a mutating driver pass.

| Repo | Frozen found / repair disposition | Left for owner | Stalled PR reroute | Default-branch state | Agent-ready supply |
|---|---|---|---|---:|---:|
| Workflows | **8** `agents:auto-pilot-pause` (no `needs-human`). **Format cap** (optimizer stopped after 3 attempts): [#4107](https://github.com/stranske/Workflows/issues/4107), [#4051](https://github.com/stranske/Workflows/issues/4051), [#3999](https://github.com/stranske/Workflows/issues/3999), [#3978](https://github.com/stranske/Workflows/issues/3978), [#3898](https://github.com/stranske/Workflows/issues/3898) — bodies largely DoR-complete; repair/tweak per guard, remove pause; **#4107** lacks `priority:*` (opener cannot select); **PR #4108** open. **#4082** — optimizer workflow error (run 39102778120), not format-cap-only; unpause only after optimizer healthy. **#3901** — pause after merge + durable verifier **NON_PASS**; not blind unpause. **#3987** — pause + `agent:codex` / in-progress (owner PR lane). | **#3987** — author PR from `codex/issue-3987`. **#3988** — author PR from `gemini/issue-3988` (in-progress, no pause). **#3901** — disposition on verifier **NON_PASS** / consumer regeneration. | **0** (**#4183**, **#4139** updated &lt;4h; both have `agent:auto`). | Latest **Gate** workflow on `main`: **failure** 2026-10-16 (`python ci` 3.12/3.13); recent `main` runs (Agents/Orchestrator, format guard) **success**. Stale Gate on old SHA — re-run Gate on tip before treating as product red. | 47 |
| Travel-Plan-Permission | **0** frozen. | — | **0** | **Agents PR Health** success (2026-10-21T20:12Z). Gate last run success (2026-08-16). | 4 |
| Trend_Model_Project | **#6080**, **#6081** — `agents:auto-pilot-pause`; underlying claims **refuted** on live `main` (see REFUTED). Proposed: remove pause; on **#6080** drop stale `status:in-progress` / suggestion labels for opener. | — | **0** | **Agents Issue Format Guard** success (2026-10-21T20:15Z). | 5 |
| Portable-Alpha-Extension-Model | **0** frozen. | — | **0** | **Agents PR Health** success (2026-10-21T20:06Z). | 20 |
| Counter_Risk | **0** frozen. | — | **0** | **Agents PR Health** success (2026-10-21T20:14Z). | 0 |
| Manager-Database | **#1773** — optimizer pause; format guard: acceptance names no runnable test gate (body otherwise substantive). **Mechanically repairable** (cite `tests/test_dashboard_read_failure_evidence.py::...`). | — | **0** | **Agents PR Health** success (2026-10-21T20:07Z). | 14 |
| Inv-Man-Intake | **0** frozen. | — | **0** | **Agents PR Health** success (2026-10-21T20:12Z). | 2 |
| Pension-Data | **0** frozen. | — | **0** (**#985** `agent:muse`, updated 2026-10-21T19:28Z). | **Keepalive Loop Reporter** **failure** on `main` (404 `keepalive-authority-state` ref); **Agents PR Health** success. Reporter infra, not product Gate/CI. | 6 |

### Genuinely needs the owner

- **Workflows #3987** — Author the PR from `codex/issue-3987` (Invite lane will not self-open).
- **Workflows #3988** — Author the PR from `gemini/issue-3988`.
- **Workflows #3901** — Decide verifier **NON_PASS** / consumer follow-up before clearing pause.

### Silent claims (1b)

Proposed release (`status:in-progress` / `agent:*` stale **>12h**, no open repo PR referencing the issue):

- **Workflows [#4036](https://github.com/stranske/Workflows/issues/4036)** — ~51h; measurement thread (input-capacity); no open PR reference.
- **Workflows [#4026](https://github.com/stranske/Workflows/issues/4026)** — ~103h; stale in-progress.
- **Workflows [#3713](https://github.com/stranske/Workflows/issues/3713)** — `agent:retry`, ~110h.
- **Workflows [#3691](https://github.com/stranske/Workflows/issues/3691)** — ~419h; `agent:auto`; Collab-Admin consumer target (repo excluded — release claim only).
- **Manager-Database [#1786](https://github.com/stranske/Manager-Database/issues/1786)** — ~94h; no open PR.

**Do not release:** **#3987**, **#3988** (owner PR author). **#3978** (format cap + in-progress). **#4107** (**PR #4108**). **Pension-Data #964** (**PR #985**).

### Priority labels (`priority:*` / open issues)

Workflows **47/60**; Travel-Plan-Permission **4/8** (four `tracker:durable` without priority); Trend_Model_Project **6/8**; Portable-Alpha-Extension-Model **20/22**; Counter_Risk **0/2** (both `tracker:durable`); Manager-Database **14/17**; Inv-Man-Intake **2/4**; Pension-Data **6/8**.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6081 — shallow clone on `main`: sampled `.agents/issue-*-ledger.yml` all use `base: main` (no `base: phase-3`).

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6080 — `hypothesis==6.155.7` is under `[project.optional-dependencies]` `dev` on live `main`, not runtime dependencies.

**Judgment (confidence ~0.9):** Highest agent leverage unchanged: format-cap Workflows bodies + **#4107** `priority:*`; Trend **#6080/#6081** should lose pause after REFUTED (re-verified this run). **Objection:** Treating Workflows **Gate** failure (2026-10-16) as current `main` red overstates risk — tip automation is green; driver should re-run Gate on HEAD before opening a CI-fix PR. **Uncertainty:** **#4082** optimizer failures may be transient vs. body content — inspect run 39102778120 before unpause.

**Offload:** `gh` read-only; mutations deferred to non-offload driver.
