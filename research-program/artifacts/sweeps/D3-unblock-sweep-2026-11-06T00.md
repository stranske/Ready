# Unblock sweep — 2026-11-06 00 UTC

**Done: 8 of 15 eligible repositories covered; 7 deferred.** Observed 2026-11-06T01:02:00Z. **Cursor/composer offload:** no GitHub mutations (read-only `gh`). **Frozen issues repaired: 0** (all pauses are opener-core parks or need live credentials; one format-guard candidate noted below). **Stalled agent PR reroutes: 0.** Consumer default-branch health checks **green** on all seven covered consumer repos; Workflows hub Health 68 **success** on latest completed run (Merge Sync PR failures are sync automation, not consumer Gate).

**Covered:** Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data.

**Deferred (8-repo budget):** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic. Orchestrator excluded.

| Repository | Frozen found / repaired | Owner holds | Silent → release rec | PR `agent:auto` adds | Default branch | Supply | Priority / open |
|---|---:|---:|---:|---:|---|---:|---:|
| Workflows | 9 / 0 | 9 | 14 / 14 | 0 | Hub; [Health 68 success](https://github.com/stranske/Workflows/actions/runs/42140150846) | 13 | 27/50 |
| Travel-Plan-Permission | 0 / 0 | 0 | 1 / 1 | 0 | [Agents PR Health green](https://github.com/stranske/Travel-Plan-Permission/actions/runs/42139006127) | 2 | 2/6 |
| Trend_Model_Project | 0 / 0 | 0 | 0 / 0 | 0 | [Agents PR Health green](https://github.com/stranske/Trend_Model_Project/actions/runs/42138574719) | 1 | 0/3 |
| Portable-Alpha-Extension-Model | 1 / 0 | 1 | 2 / 2 | 0 | [Agents PR Health green](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/42138635305) | 3 | 4/6 |
| Counter_Risk | 0 / 0 | 0 | 0 / 0 | 0 | [Agents PR Health green](https://github.com/stranske/Counter_Risk/actions/runs/42138570510) | 0 | 1/3 |
| Manager-Database | 1 / 0 | 1 | 1 / 1 | 0 | Gate followups green; Keepalive Loop Reporter failing (telemetry) | 4 | 2/6 |
| Inv-Man-Intake | 0 / 0 | 0 | 0 / 0 | 0 | [Agents PR Health green](https://github.com/stranske/Inv-Man-Intake/actions/runs/42138645443) | 0 | 0/2 |
| Pension-Data | 0 / 0 | 0 | 0 / 0 | 0 | [Agents PR Event Hub green](https://github.com/stranske/Pension-Data/actions/runs/42139240112) | 1 | 0/3 |

## REFUTED

REFUTED: https://github.com/stranske/Workflows/issues/4082 — `main` `pr-00-gate.yml` triggers on `opened`, `synchronize`, `reopened`, and `ready_for_review`; create-only premise is false.

REFUTED: https://github.com/stranske/Workflows/issues/4026 — `maint71_merge_sync_prs.js` on `main` defines stale-canary refresh paths (`STALE_CANARY_HOURS`, `canaryNeedsRefresh`).

REFUTED: https://github.com/stranske/Workflows/issues/3988 — consumer delegation templates ship `selectAgentFromRouteWeights` with capacity handling on `main`.

## Frozen issues

**Agent-repair candidate (not applied — offload):**

- [Workflows #4422](https://github.com/stranske/Workflows/issues/4422) — format-guard 3-attempt cap (2026-11-03), but the body now has complete Tasks / Acceptance Criteria sections. A non-offload pass should re-run format guard and remove `agents:auto-pilot-pause` if clean; opener-core park comment still cites live production verification (owner-heavy).

**Left for owner (opener-core `action=park` or equivalent):**

- Workflows #4432 — hosted keepalive auth, subscription usage-console access.
- Workflows #4422 — live multi-file verifier report + historical 2026-10-24 campaign reconstruction (after any format unblock).
- Workflows #4400 — original Doc-Lineage#81 verifier finding inputs.
- Workflows #4363 — post-merge verification for PR #4362 + closer execution record.
- Workflows #4284 — seven consecutive daily Gate p50 ≤10 min measurements in `docs/reports/ci-budget.json`.
- Workflows #4082 — PAEM#2390 merge + 48h consumer Gate observation (issue premise refuted; park reason remains operational).
- Workflows #3978 — keepalive cache-hit logs + 48h timing datasets.
- Workflows #3901 — live exact-plan qualification across FULL consumer regeneration.
- Workflows #4338 — integration alert on external Integration-Tests repo (not format-guard); mechanical fix may be possible but issue is an integration-failure tracker without a simple body repair.
- PAEM #2474 — live access to #2467 head + immutable green pytest run records.
- Manager-Database #1888 — open PR #1889 exists for Codex; pause is exhausted-repair follow-up, not a missing issue section.

## Silent claims (no open PR referencing issue, >12h stale)

**Recommend:** remove `status:in-progress` and `agents:auto-pilot` where present; clear stale `agent:*` after merged bootstrap PRs (#1728 → PR #1731 merged, #1750 → #1890 merged, #2480 → #2483 merged).

Workflows: #4458, #4455, #4454, #4437, #4433, #4429, #4413, #4402, #4389; #4026, #3988 (`status:in-progress`); #4432, #4400, #3978 carry `agent:codex` + pause (do not strip pause until step 1 resolves).

Travel-Plan-Permission: #1728 (`agent:claude`).

Portable-Alpha-Extension-Model: #2480, #2477 (no open PR cites `#2477`; #2475 cites #2336 only).

Manager-Database: #1750 (`agent:cursor`).

## Stalled PRs

None: no open `agent:*` PR stale >4h without `agent:auto` (Manager-Database #1889 updated within window; Workflows #4463 ~1.5h old).

## Priority gap

Trend_Model_Project, Inv-Man-Intake, Pension-Data: zero `priority:*` on open implementation issues (e.g. TMP #6188, Pension #1011). Workflows 23/50 open issues lack priority despite 27 labelled — opener still cannot select unprioritized work ([Workflows #3423](https://github.com/stranske/Workflows/issues/3423)).

## Genuinely needs the owner

All frozen rows above where park comments name credentials, production verification windows, or external account access; no new product decisions surfaced beyond those parks.

Checkpoints: `D3-unblock-sweep-2026-11-06T00.CHECKPOINT.md`.
