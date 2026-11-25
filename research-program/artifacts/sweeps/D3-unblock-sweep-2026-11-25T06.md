# D3 unblock sweep — 2026-11-25T06

**Run:** ATTEMPT 1 · **checked at** 2026-11-25T06:55:26Z · **mode:** offload (read-only; no GitHub mutations)

## Coverage

| Covered (8) | Deferred (6) |
|---|---|
| Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data | Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic |
| | *Skipped by policy:* Orchestrator |

## Summary table

| Repo | Frozen found / repaired | Left for owner | Stalled PRs (+`agent:auto`) | Default branch (latest Gate) | Agent-ready supply |
|---|---:|---|---:|---|---:|
| Workflows | 0 / 0 | 0 | 0 (5135 already has `agent:auto`) | success | 2 |
| Travel-Plan-Permission | 0 / 0 | 0 | 0 | success | 0 |
| Trend_Model_Project | 0 / 0 | 0 | 0 | success | 0 |
| Portable-Alpha-Extension-Model | 0 / 0 | 0 | 0 | success | 0 |
| Counter_Risk | 0 / 0 | 0 | 0 | success | 1 |
| Manager-Database | 0 / 0 | 0 | 0 | success | 0 |
| Inv-Man-Intake | 0 / 0 | 0 | 0 | success | 0 |
| Pension-Data | 0 / 0 | 0 | 0 | success | 0 |

## Step notes

### 1 — Frozen issues (`needs-human`, `agents:auto-pilot-pause`)

None open in this batch (repo search + issue list, limit 100).

### 1b — Silent claims & priority labels

- **Silent-claim scan:** One candidate, **no release recommended**
  - [Workflows#3123](https://github.com/stranske/Workflows/issues/3123) — `agent:needs-attention` + `tracker:durable`; last comment (2026-11-24) records observability **degraded** with run link; no open implementation PR (expected for a health tracker). Not an opener `status:in-progress` stall.
- **`status:in-progress`:** none in batch.
- **Priority label gap (opener cannot select without `priority:*`):**
  - **Workflows:** 1 open implementation issue, **0** with `priority:*` → [#5136](https://github.com/stranske/Workflows/issues/5136) needs a priority label (e.g. `priority:normal`) if the opener should take it.

### 2 — Stalled agent PRs (>4h, `agent:*` without fresh update)

None requiring `agent:auto`; Workflows [#5135](https://github.com/stranske/Workflows/pull/5135) already carries `agent:auto` (keepalive handoff 2026-11-25).

### 3 — Red default branch (`main`)

Latest completed **Gate** (or equivalent) run: **success** on all eight repos (Workflows gate in flight at sweep time; last completed gate success 2026-11-25T06:55:24Z).

### 4 — Supply (agent-ready open issues)

Counts exclude `needs-human`, `agents:pause`, `agents:paused`, `status:in-progress`, `tracker:durable`, `dependencies`, `epic`.

## Genuinely needs the owner

*(none in this batch)*

## Recommended actions (not applied — offload)

1. Add `priority:*` to [Workflows#5136](https://github.com/stranske/Workflows/issues/5136) if opener selection is intended.

## REFUTATION lines

*(none)*

---
*Next run: continue from checkpoint; process deferred six repos.*