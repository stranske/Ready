# D3 unblock sweep — 2026-10-22T12

**Run:** ATTEMPT 1 · **Offload:** read-only on GitHub (no label/issue/PR mutations; actions below are **recommended** for the owning session).

**Covered (8/15):** Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data.

**Deferred (next run):** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic. (`Orchestrator` is in `SUPPORTED_REPOS` but never acted on per policy.)

## Summary table

| Repo | Frozen found | Frozen repaired | Frozen → owner | Silent claims → release | Stalled agent PRs (`agent:auto` add) | Default branch Gate/CI | Agent-ready supply |
|------|-------------:|----------------:|-----------------|------------------------:|-------------------------------------:|------------------------|-------------------:|
| Workflows | 8 | 0 | 3 (+5 agent-fixable) | 7 | 0 | Gate last run **failure** (2026-10-16); no newer `Gate` on `main` | 46 |
| Travel-Plan-Permission | 0 | 0 | 0 | 0 | 0 | Gate success (2026-08-16) | 4 |
| Trend_Model_Project | 0 | 0 | 0 | 0 | 0 | No `Gate` workflow runs in history | 4 |
| Portable-Alpha-Extension-Model | 0 | 0 | 0 | 0 | 0 | Gate success (recent sample) | 20 |
| Counter_Risk | 0 | 0 | 0 | 0 | 0 | No `Gate` workflow | 0 |
| Manager-Database | 1 | 0 | 0 (+1 agent-fixable) | 1 (#1786) | 0 | No Gate/CI fail in recent `main` runs; **Nightly Regression** failed 2026-10-22 | 14 |
| Inv-Man-Intake | 0 | 0 | 0 | 0 | 0 | No `Gate` workflow | 2 |
| Pension-Data | 0 | 0 | 0 | 0 (#964 **not** released — open PR) | 0 | Agents Gate Followups success; Keepalive Loop Reporter failing (out of scope) | 6 |

## Priority labels (opener — Workflows#3423)

| Repo | Open (API) | With `priority:*` (sample ≤100) | Gap notes |
|------|----------:|--------------------------------:|-----------|
| Workflows | 71 | 46 | Gap is trackers/epics/sync dashboards outside opener backlog |
| Travel-Plan-Permission | 8 | 4 | 4× `tracker:durable` only |
| Trend_Model_Project | 6 | 4 | 2× trackers |
| Portable-Alpha-Extension-Model | 23 | 20 | 3× trackers |
| Counter_Risk | 2 | 0 | Both `tracker:durable` |
| Manager-Database | 17 | 14 | 3× trackers |
| Inv-Man-Intake | 5 | 2 | 3× trackers (API 5 vs sample 4 — one pagination edge) |
| Pension-Data | 9 | 6 | 3× trackers |

No implementation issue lacking `priority:*` beyond durable trackers.

## Genuinely needs the owner

| Issue | Ask |
|-------|-----|
| [Workflows#4082](https://github.com/stranske/Workflows/issues/4082) | Decide how `pr-00-gate.yml` `create_only` should propagate gate-trigger fixes to consumer repos. |
| [Workflows#3987](https://github.com/stranske/Workflows/issues/3987) | Open the human-authored PR from the `codex/issue-3987` compare link so Codex can engage. |
| [Workflows#3901](https://github.com/stranske/Workflows/issues/3901) | Resolve production verifier NON_PASS / evidence semantics after merged #3902 (not a format-only unblock). |

## Agent-fixable frozen (format guard / AC gate — not applied, offload)

| Issue | Remedy |
|-------|--------|
| Workflows#4107, #4051, #3999, #3978, #3898 | Edit body per format-guard comment; remove `agents:auto-pilot-pause`. |
| [Manager-Database#1773](https://github.com/stranske/Manager-Database/issues/1773) | Add explicit verification gate to AC; remove `agents:auto-pilot-pause`. |

## Step 1b — Silent stale claims (>12h, claim labels, no open PR in repo)

**Release** (remove `status:in-progress`, `agents:auto-pilot` if present, and stray `agent:*` claim labels):

| Repo | Issue | Notes |
|------|-------|-------|
| Workflows | [#4036](https://github.com/stranske/Workflows/issues/4036) | Stale `status:in-progress`; no open PR. |
| Workflows | [#4026](https://github.com/stranske/Workflows/issues/4026) | Stale in-progress; format guard on tasks — fix body or release after fix. |
| Workflows | [#3988](https://github.com/stranske/Workflows/issues/3988) | `agent:gemini`; invite flow waiting on human PR author. |
| Workflows | [#3987](https://github.com/stranske/Workflows/issues/3987) | Also frozen; clear in-progress per Workflows#3422 after pause. |
| Workflows | [#3978](https://github.com/stranske/Workflows/issues/3978) | Pause + in-progress; align with #3422. |
| Workflows | [#3713](https://github.com/stranske/Workflows/issues/3713) | Format guard on tasks — agent-fixable body. |
| Workflows | [#3691](https://github.com/stranske/Workflows/issues/3691) | Collab-Admin consumer sync — **do not implement** (fleet exclusion); still release stale `status:in-progress` / `agent:auto` so it does not read as active work. |
| Manager-Database | [#1786](https://github.com/stranske/Manager-Database/issues/1786) | Stale `status:in-progress`; audit comment only, no open PR. |

**Held:** [Pension-Data#964](https://github.com/stranske/Pension-Data/issues/964) has open PR [#985](https://github.com/stranske/Pension-Data/pull/985) — do **not** release claim.

## Step 2 — Stalled agent PRs (>4h, `agent:*`, missing `agent:auto`)

None in the eight repos (agent-labelled PRs on Workflows/Pension-Data updated within 4h or already carry `agent:auto`).

## Step 3 — Red default branch

- **Workflows:** Most recent `Gate` workflow on `main` concluded **failure** (2026-10-16). Failed-step logs are cleanup-heavy; job emitted `format_failure` / `cosmetic_failure` outputs — **investigate in a writable session** before assuming a mechanical pin/fix; do not guess from offload.
- **Manager-Database:** **Nightly Regression** failed 2026-10-22 — `manager-database-api-1` container exit during compose up (`dependency failed to start`). Treat as **product/infra defect** until logs show a mechanical pin; file or fix via PR in owning session, not offload.
- **Pension-Data / others:** No failing Gate/CI on `main` in recent history (Keepalive Loop Reporter failures excluded per fleet practice).

## Step 4 — Supply

Per-repo agent-ready counts in summary table (open issues excluding `needs-human`, `agents:pause`/`paused`, `status:in-progress`, `tracker:durable`, `dependencies`, `epic`).

## Confidence

High on inventory (gh API, 2026-10-22 ~12:40 UTC). Medium on Workflows Gate root cause (single stale failed run, log tail not diagnostic). Would change mind if a newer successful `Gate` run exists under a different workflow name or default branch alias.
