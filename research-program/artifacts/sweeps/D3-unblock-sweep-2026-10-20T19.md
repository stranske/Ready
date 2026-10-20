# D3 unblock sweep — 2026-10-20T19

## Outcome

Covered (first eight `SUPPORTED_REPOS`, in order): Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data. Deferred by the eight-repository cap: Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic. `stranske/Orchestrator` was not inspected.

**Constraint:** this synchronous offload prohibits GitHub mutations (labels, bodies, comments, PRs, issues). No GitHub edit was made. The table records verified follow-ups for an interactive lane after rechecking live state.

| Repo | Frozen found / repair disposition | Genuinely needs owner | Stalled PR reroute (`agent:auto`) | Default branch (Gate/CI) | Agent-ready supply |
|---|---|---|---|---|---:|
| Workflows | 8 with `agents:auto-pilot-pause`: #4107, #4082, #4051, #3999, #3987, #3978, #3901, #3898 — format-guard attempt caps or optimizer failures; bodies are mechanically repairable (paths/tests cited). #4082 is optimizer churn, not a product decision. | None | None (#4139 `agent:cursor` updated <4h) | **RED:** latest completed **Maint 46 Post CI** run [#39487839261](https://github.com/stranske/Workflows/actions/runs/39487839261) — `snapshotFailureIssues` throws `context.repo` undefined; artifact upload then fails. Automation defect → file/repair issue, not a fixture guess. | 42 |
| Travel-Plan-Permission | 0 | None | None | No failed Gate/CI in recent main history | 4 |
| Trend_Model_Project | 2 paused: #6080, #6081 — premises **refuted** at current `main` (see below); labels unchanged here. | None | None | No failed Gate/CI among recent main runs | 5 |
| Portable-Alpha-Extension-Model | 0 | None | None | Recent issue-triggered Gate-family runs green/skipped; no default-branch Gate failure | 19 |
| Counter_Risk | 0 | None | None | No failed Gate/CI among recent main runs | 0 (only `tracker:durable` issues open) |
| Manager-Database | 1: #1773 — format guard: acceptance names no runnable test; mechanically repairable. | None | None | No failed Gate/CI among recent main runs | 14 |
| Inv-Man-Intake | 0 | None | None | No failed Gate/CI among recent main runs | 2 |
| Pension-Data | 0 | None | None | Keepalive Loop Reporter failed on dispatch; not Gate/CI evidence on `main` | 6 |

## Silent claims and priority coverage

**Release** stale `status:in-progress` / `agent:*` where no open PR references the issue (no label edits in this offload): Workflows #4036, #4026, #3988, #3713, #3691; Manager-Database #1786.

**Retain claims:** Workflows #3987, #3978 (frozen `agents:auto-pilot-pause` — handle via step 1 body repair, not silent release). Pension-Data #964 is stale by timestamp but open PR [#985](https://github.com/stranske/Pension-Data/pull/985) references it — do not release.

**Priority vs implementation issues** (open issues excluding `tracker:durable`, `dependencies`, `epic`): Workflows **42 / 48** (missing on #4107, #4087, #3579, #3558, #3557, #3549); Manager-Database **14 / 15** (missing on #1773). All other covered repos matched.

## Refutations

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6080 — at `fc43c3028d6e158d37798c0c4419889ffdeb75b5`, `hypothesis==6.155.7` sits only under `[project.optional-dependencies].dev`, not runtime dependencies.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6081 — at the same `main` head, zero `.agents/issue-*-ledger.yml` entries use `base: phase-3`; sampled ledgers (e.g. #4848–#5658) are `base: main`.

## Confidence

High on live `gh` label/run/timestamp data and clone-verified refutations. Moderate on Workflows freeze repairability (bodies not rewritten here). PR–issue linkage used `gh pr list --search "#N"` (index evidence, not exhaustive of every reference form).
