# Unblock sweep — 2026-10-29T14 UTC

**Done: 8 of 15 eligible repositories covered; 7 deferred.** Observed 2026-10-29T16:35:00Z. **Offload run:** no GitHub mutations applied here; table lists live state and **recommended** repairs/reroutes for the applying session.

**Covered:** Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data.

**Deferred (next run):** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic. **Excluded:** Orchestrator.

| Repository | Frozen found / repaired | Owner holds | Silent claims → release | PR reroutes | Default branch | Supply | Priority / open |
|---|---:|---:|---:|---:|---|---:|---:|
| Workflows | 8 / 0 | 2 | 6 | 0 | Hub; no consumer Gate on `main` | 42 | 40/57 |
| Travel-Plan-Permission | 0 / 0 | 0 | 0 | 0 | Agents PR Health green (2026-10-29) | 4 | 4/8 |
| Trend_Model_Project | 0 / 0 | 0 | 0 | 0 | Agents PR Health green | 6 | 6/8 |
| Portable-Alpha-Extension-Model | 0 / 0 | 0 | 0 | 0 | Agents PR Health green | 20 | 20/22 |
| Counter_Risk | 0 / 0 | 0 | 0 | 0 | Gate Followups success; Keepalive Loop Reporter failed (not Gate) | 6 | 6/8 |
| Manager-Database | 0 / 0 | 0 | 1 (#1786) | 0 | Agents PR Health green | 13 | 14/16 |
| Inv-Man-Intake | 0 / 0 | 0 | 0 | 0 | Agents PR Health green | 1 | 1/3 |
| Pension-Data | 0 / 0 | 0 | 0 | 0 | Gate Followups success; Keepalive Loop Reporter failed (not Gate) | 6 | 6/8 |

## Frozen issues (Workflows)

**Leave alone (tracker):** [#4284](https://github.com/stranske/Workflows/issues/4284) — `ci-budget` + pause; bot-maintained CI budget row, not implementation work.

**Recommended repair (format-guard / body ready; remove `agents:auto-pilot-pause` after any minor guard fixes):**

- [#4223](https://github.com/stranske/Workflows/issues/4223) — evaluate receipt / PASS publication split; body has Tasks, AC, paths.
- [#4107](https://github.com/stranske/Workflows/issues/4107) — contributor-tier prompt binding; full AGENT_ISSUE_FORMAT sections present.
- [#4082](https://github.com/stranske/Workflows/issues/4082) — Gate `labeled` trigger campaign; body complete; optimizer workflow error on last bot pass, not missing sections.
- [#4051](https://github.com/stranske/Workflows/issues/4051) — repo-review uploader → Orchestrator prompt role; Tasks/AC name files and pytest gate.
- [#3978](https://github.com/stranske/Workflows/issues/3978) — runner `actions/cache`; also carries stale `status:in-progress` (see silent claims).

**Genuinely needs the owner:**

- [#3901](https://github.com/stranske/Workflows/issues/3901) — body states **local source owner only; no hosted agent opt-in** under workflows-1836 campaign rules.
- [#3898](https://github.com/stranske/Workflows/issues/3898) — same **local source owner only** constraint for Maint68/71 guard campaign work.

## Silent claims (>12h, no open PR referencing issue)

Release `status:in-progress` and any `agents:auto-pilot` per [Workflows #3422](https://github.com/stranske/Workflows/issues/3422) (do **not** release if an open PR references the issue — none do):

| Issue | Note |
|---|---|
| [#4036](https://github.com/stranske/Workflows/issues/4036), [#4026](https://github.com/stranske/Workflows/issues/4026), [#3988](https://github.com/stranske/Workflows/issues/3988), [#3713](https://github.com/stranske/Workflows/issues/3713), [#3691](https://github.com/stranske/Workflows/issues/3691) | Stale `status:in-progress` / `agent:*`; no referencing open PR |
| [#3978](https://github.com/stranske/Workflows/issues/3978) | Overlaps frozen pause; release claim labels after body repair |
| [Manager-Database #1786](https://github.com/stranske/Manager-Database/issues/1786) | Stale `status:in-progress`; no open PR |

[#4026](https://github.com/stranske/Workflows/issues/4026) still advertises missing paths in an advisory block — releasing the claim lets the opener either fix citations or re-pause via guard; do not treat as refuted without clone verification this run.

## Stalled agent PRs

None. Open agent-labelled PRs on Workflows (#4184, #4139) were updated within the last 4h and already carry `agent:auto` where applicable.

## Default branch

All seven consumer repos show recent **Agents PR Health** (or **Agents Gate Followups**) **success** on `main`. Workflows has no consumer Gate on `main`. Recent **Keepalive Loop Reporter** failures on Counter_Risk and Pension-Data are reporter workflows, not the Gate/CI check named in the sweep brief.

## Priority gap

Opener cannot select issues without `priority:*` where counts differ: Workflows **40/57**, Travel-Plan-Permission **4/8**, Portable-Alpha-Extension-Model **20/22**, Counter_Risk **6/8**, Manager-Database **14/16** (#1164, #927), Inv-Man-Intake **1/3**, Pension-Data **6/8**. Track fleet labeling under [Workflows #3423](https://github.com/stranske/Workflows/issues/3423).

## REFUTATION

None newly verified this batch.

Evidence: `gh` queries 2026-10-29T16:15–16:35Z. Checkpoint: `D3-unblock-sweep-2026-10-29T14.CHECKPOINT.md`.
