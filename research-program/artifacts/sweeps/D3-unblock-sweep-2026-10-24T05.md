# D3 unblock sweep — 2026-10-24T05

**Covered (run cap 8):** Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data.

**Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic. Orchestrator excluded by scope.

**Offload constraint:** GitHub issue/label/PR/comment writes are prohibited in this invocation. Findings and intended repairs are recorded here; a non-offload writer must apply mutations.

| Repo | Frozen found / repairable | Left for owner | Stalled PR → `agent:auto` | Default branch (Gate/CI) | Agent-ready supply |
|---|---|---|---|---|---:|
| Workflows | 9× `agents:auto-pilot-pause` (#4223, #4107, #4082, #4051, #3999, #3987, #3978, #3901, #3898): mostly format-guard attempt caps or optimizer failure; bodies need verified repo-relative paths + runnable acceptance, then pause label removed. #3999 is refuted (do not unfreeze). | #3987/#3988: invite flows require a **human-authored PR** before Codex/Gemini engage. | None (agent PRs #4184/#4139 updated <4h). | **Red:** latest `Gate` on `main` failed 2026-10-16 (`test_agents_guard_registry_enabled` — registry includes `muse`; test expects without). Mechanical test update; no PR opened (offload). | 42 (of 57 open in query window) |
| Travel-Plan-Permission | None | None | None | CI success 2026-10-23; Gate success (stale 2026-08). | 4 |
| Trend_Model_Project | None | None | None | CI success 2026-10-23; no Gate workflow. | 4 |
| Portable-Alpha-Extension-Model | None | None | None | CI success 2026-10-23; Gate success (stale). | 20 |
| Counter_Risk | None (durable trackers excluded) | None | None | CI success 2026-10-22; no Gate workflow. | 2 |
| Manager-Database | #1773 paused — refuted blocker PR #1772 merged; reconcile/close, do not repair as frozen delivery. | #1786: owner acceptance audit in progress (merged #1795/#1812; disputes verifier disposition). | None | CI success 2026-10-23; Nightly Regression failing (docker API container exit 1) — **not** Gate/CI per workflow name. | 14 |
| Inv-Man-Intake | None | None | None | CI success 2026-10-22; no Gate workflow. | 2 |
| Pension-Data | None | None | None (open #985 has `agent:*`, updated <4h) | CI success 2026-10-22; Agents Gate Followups success 2026-10-24. | 6 |

## Silent claims (no open PR, >12h, not `needs-human`)

**Workflows — release `status:in-progress` / `agent:*` when no PR backs the claim (after frozen-body repair where applicable):** #4036, #4026, #3988 (after owner opens PR or lane reclaims), #3978, #3987; review #3691/#3713 (sync-review; merged delivery PRs exist but issues remain open). Do **not** release #964 in Pension-Data (open PR #985).

**Manager-Database:** #1786 — stale `status:in-progress`, no open PR; bootstrap PRs #1800/#1796 closed, delivery #1812 merged. Verify AC against owner audit before releasing label.

## Priority-label gap

| Repo | open (window) | with `priority:*` | gap notes |
|---|---:|---:|---|
| Workflows | 57 | 40 | **#4201** lacks priority (opener cannot select). #4223/#4107 paused without priority. |
| Manager-Database | 17 | 14 | **#1773** lacks priority (refuted; reconcile first). |
| Others in this pass | — | — | Implementation issues in TPP, TMP, PAEM, IMI, Pension-Data all carried priority in the returned set. Counter_Risk has no non-tracker implementation issues. |

## Apply when writes allowed

1. Workflows: repair frozen bodies (#4223, #4107, #4051, #3898, #3978, #3987, #3901, #4082); remove `agents:auto-pilot-pause` where guard passes. Open PR to fix `tests/workflows/test_agents_guard_registry_enabled.py` for `muse` in shipped registry (Gate red).
2. Workflows: release silent claims on #4036, #4026, #3978 (and #3987/#3988 per policy above).
3. Manager-Database: close or rewrite #1773; resolve #1786 claim after owner audit or release if #1812 satisfies AC.
4. Add `priority:normal` (or appropriate) to Workflows **#4201**.

## Genuinely needs the owner

- **Workflows #3987 / #3988:** Open the human-authored PR from the automation compare link so the assigned agent can run under invite policy.
- **Manager-Database #1786:** Confirm whether merged #1812 completes acceptance or a follow-up verification pass is still required.

REFUTED: https://github.com/stranske/Workflows/issues/3999 — named delivery PR #3993 merged 2026-10-17.

REFUTED: https://github.com/stranske/Manager-Database/issues/1773 — described blocker PR #1772 merged 2026-10-16.

**Confidence:** High on live labels, PR presence, merged-PR refutations, and sampled Gate/CI conclusions. Moderate on Workflows supply (60-issue cap). Gate failure on Workflows `main` may be stale if no Gate has run since 2026-10-16; re-run Gate after fix to confirm green.
