# D3 unblock sweep — 2026-11-01T06 (attempt 1)

**Observed:** ~2026-11-01T06:50Z · **Mode:** Cursor offload (read-only on GitHub; label/body/PR actions below are **recommended** for a writable lane, not applied here).

**Coverage (8/15):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen (found / repaired) | Stalled PR reroutes | Default branch (Gate/CI + head) | Agent-ready supply |
|---|---:|---:|---|---:|
| Workflows | 9 / 0 | 0 | `main` tip `c4633a9`; latest **Gate** on `main` still **failure** at `12cea89` ([run](https://github.com/stranske/Workflows/actions/runs/38938420079), 2026-10-16); no Gate run on current tip in `gh` | 40 |
| Travel-Plan-Permission | 0 / 0 | 0 | [green — CI on tip `503eae9`](https://github.com/stranske/Travel-Plan-Permission/actions/runs/41277412044) | 4 |
| Trend_Model_Project | 0 / 0 | 0 | Tip `12e324f`; latest **CI** **cancelled** ([run](https://github.com/stranske/Trend_Model_Project/actions/runs/41179626535)); prior **success** on `35f186c` — not a failed head run | 6 |
| Portable-Alpha-Extension-Model | 0 / 0 | 0 | [green — CI on tip `5b96b76`](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/41277464327) | 20 |
| Counter_Risk | 0 / 0 | 0 | [green — CI on tip `eaebeaa`](https://github.com/stranske/Counter_Risk/actions/runs/41277418841) | 6 |
| Manager-Database | 0 / 0 | 0 | [green — CI on tip `e5830db`](https://github.com/stranske/Manager-Database/actions/runs/41255604323) | 10 |
| Inv-Man-Intake | 0 / 0 | 0 | [green — CI on tip `2960e93`](https://github.com/stranske/Inv-Man-Intake/actions/runs/41179599679) | 1 |
| Pension-Data | 0 / 0 | 0 | [green — CI on tip `aba8f68`](https://github.com/stranske/Pension-Data/actions/runs/41179595234) | 6 |

**Priority gaps (`priority:*` vs open issues):** Workflows **37 / 54**; Travel-Plan-Permission **4 / 8** (four open issues are `tracker:durable` dashboards/audits only); Manager-Database **11 / 13** (two durable trackers); Portable-Alpha-Extension-Model **20 / 22** (two trackers); Inv-Man-Intake **1 / 3** (two durable trackers). Among **agent-ready** issues missing `priority:*`: Workflows **8** ([#4363](https://github.com/stranske/Workflows/issues/4363), [#4358](https://github.com/stranske/Workflows/issues/4358), [#4338](https://github.com/stranske/Workflows/issues/4338), [#4223](https://github.com/stranske/Workflows/issues/4223), [#3579](https://github.com/stranske/Workflows/issues/3579), [#3558](https://github.com/stranske/Workflows/issues/3558), [#3557](https://github.com/stranske/Workflows/issues/3557), [#3549](https://github.com/stranske/Workflows/issues/3549)); all other covered repos: every agent-ready issue has `priority:*`.

**Silent claims (1b) — recommended release (no open PR referencing issue):** [Workflows #4036](https://github.com/stranske/Workflows/issues/4036), [#4026](https://github.com/stranske/Workflows/issues/4026), [#3988](https://github.com/stranske/Workflows/issues/3988), [#3978](https://github.com/stranske/Workflows/issues/3978) (also format-pause frozen), [#3713](https://github.com/stranske/Workflows/issues/3713), [#3691](https://github.com/stranske/Workflows/issues/3691); [Manager-Database #1786](https://github.com/stranske/Manager-Database/issues/1786). **Held:** [Pension-Data #964](https://github.com/stranske/Pension-Data/issues/964) — open [PR #985](https://github.com/stranske/Pension-Data/pull/985) (`agent:muse`, body cites issue 964).

**Stalled agent PRs:** none (>4h idle with `agent:*` and without `agent:auto` in covered repos).

**Red-main fixes:** none opened (offload). Workflows Gate failure predates current `main`; Trend tip CI **cancelled** (not failed) — re-run before treating as red-main product defect.

## Genuinely needs the owner

- [Workflows #4338](https://github.com/stranske/Workflows/issues/4338) — Integration-Tests failure on pinned branch; cross-repo / integration coordination, not a format-guard body edit.
- [Workflows #4284](https://github.com/stranske/Workflows/issues/4284) — `ci-budget` pause (Gate p50 above target); confirm unpause vs continued drain.
- [Workflows #3901](https://github.com/stranske/Workflows/issues/3901) — Post-merge verifier compare / evidence judgment; not opener format cleanup.
- [Workflows #4363](https://github.com/stranske/Workflows/issues/4363) — Format attempt cap (2026-10-31) plus fleet-wide GitHub Models fallback policy; confirm scope before agent rewrite.

## Agent-repairable frozen (writable lane: fix bodies, drop `agents:auto-pilot-pause`)

- [#4223](https://github.com/stranske/Workflows/issues/4223), [#4051](https://github.com/stranske/Workflows/issues/4051), [#3978](https://github.com/stranske/Workflows/issues/3978), [#3898](https://github.com/stranske/Workflows/issues/3898) — format-guard attempt cap.
- [#4082](https://github.com/stranske/Workflows/issues/4082) — optimizer error on concrete gate/sync paths; agent-repairable once guard passes.

## Refutations

(none new this pass — [#4026](https://github.com/stranske/Workflows/issues/4026) path-citation block already refuted in-issue 2026-10-30)

**Confidence:** High on live issue/PR/run reads and silent-claim PR cross-check (#964 held). **Uncertainty:** Whether Trend’s cancelled CI on tip blocks consumers vs transient cancel; whether Workflows Gate still push-triggers on `main` (stale 2026-10-16 failure may overstate tip risk). **Objection:** Offload cannot apply seven silent releases or five format-pause body fixes — that remains the dominant opener drag unless a writable lane runs immediately after this artifact.
