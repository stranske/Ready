# D3 unblock sweep — 2026-10-31T14 (attempt 1)

**Observed:** ~2026-10-31T14:48Z · **Mode:** Cursor offload (read-only on GitHub; repairs, label changes, and PRs below are **recommended** for a writable lane, not applied here).

**Coverage (8/15):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen (found / repaired) | Stalled PR reroutes | Default branch (Gate/CI + head) | Agent-ready supply |
|---|---:|---:|---|---:|
| Workflows | 9 / 0 | 0 | `main` tip `8feb0cc`; latest **Gate** on `main` still **failure** at `12cea89` ([run](https://github.com/stranske/Workflows/actions/runs/38938420079), 2026-10-16); no Gate run on tip in `gh` | 40 |
| Travel-Plan-Permission | 0 / 0 | 0 | [green — CI on `b44b114`](https://github.com/stranske/Travel-Plan-Permission/actions/runs/41179584979) | 4 |
| Trend_Model_Project | 0 / 0 | 0 | Latest **CI** on tip `12e324f` **cancelled** ([run](https://github.com/stranske/Trend_Model_Project/actions/runs/41179626535)); last **success** on `35f186c` | 6 |
| Portable-Alpha-Extension-Model | 0 / 0 | 0 | [green — CI on `872f791`](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/41179027927) | 20 |
| Counter_Risk | 0 / 0 | 0 | [green — CI on `d907f74`](https://github.com/stranske/Counter_Risk/actions/runs/41179591503) (Keepalive Loop Reporter failures are not Gate/CI) | 6 |
| Manager-Database | 0 / 0 | 0 | [green — CI on `987164d`](https://github.com/stranske/Manager-Database/actions/runs/41179613120) | 12 |
| Inv-Man-Intake | 0 / 0 | 0 | [green — CI on `2960e93`](https://github.com/stranske/Inv-Man-Intake/actions/runs/41179599679) | 1 |
| Pension-Data | 0 / 0 | 0 | [green — CI on `aba8f68`](https://github.com/stranske/Pension-Data/actions/runs/41179595234) | 6 |

**Priority gaps (`priority:*` vs open issues):** Workflows **37 / 54**; Travel-Plan-Permission **4 / 8**; Inv-Man-Intake **1 / 3**. Among **agent-ready** issues missing `priority:*`: Workflows **8** (32/40 labelled); all other covered repos: every agent-ready issue has `priority:*`.

**Silent claims (1b) — recommended release (no open PR referencing issue):** [Workflows #4036](https://github.com/stranske/Workflows/issues/4036), [#4026](https://github.com/stranske/Workflows/issues/4026), [#3988](https://github.com/stranske/Workflows/issues/3988), [#3978](https://github.com/stranske/Workflows/issues/3978) (also format-pause frozen), [#3713](https://github.com/stranske/Workflows/issues/3713), [#3691](https://github.com/stranske/Workflows/issues/3691); [Manager-Database #1786](https://github.com/stranske/Manager-Database/issues/1786). **Held:** [Pension-Data #964](https://github.com/stranske/Pension-Data/issues/964) — open [PR #985](https://github.com/stranske/Pension-Data/pull/985) (`agent:muse`, active today).

**Stalled agent PRs:** none (>4h idle with `agent:*` and without `agent:auto` in covered repos).

**Red-main fixes:** none opened (offload). Workflows Gate failure predates current `main`; Trend tip CI cancelled (not failed) — re-run or diagnose cancel before treating as red-main product defect.

## Genuinely needs the owner

- [Workflows #4338](https://github.com/stranske/Workflows/issues/4338) — Integration-Tests still red on `chore/python-floor-313` (`python-version` pin mismatch); cross-repo coordination, not a body-format edit.
- [Workflows #4284](https://github.com/stranske/Workflows/issues/4284) — `ci-budget` pause (p50 11.75 min vs 10 min target); confirm unpause vs continued drain.
- [Workflows #3901](https://github.com/stranske/Workflows/issues/3901) — Post-merge verifier compare NON_PASS / evidence conflict; needs verifier-lane judgment, not format-guard cleanup.
- [Workflows #4363](https://github.com/stranske/Workflows/issues/4363) — Format attempt cap while [PR #4362](https://github.com/stranske/Workflows/pull/4362) is open; owner may prefer merging PR path vs manual body edit (not a credential block).

## Agent-repairable frozen (writable lane: fix bodies, drop `agents:auto-pilot-pause`)

- [#4223](https://github.com/stranske/Workflows/issues/4223), [#4051](https://github.com/stranske/Workflows/issues/4051), [#3978](https://github.com/stranske/Workflows/issues/3978), [#3898](https://github.com/stranske/Workflows/issues/3898) — format-guard attempt cap.
- [#4082](https://github.com/stranske/Workflows/issues/4082) — issue-optimizer error; body cites concrete gate/sync paths; agent-repairable once guard passes.

## Refutations

(none new this pass — #4026’s “missing path” block was already refuted in-issue 2026-10-30)

**Confidence:** High on live issue/PR/run reads and silent-claim PR cross-check (#964 held). **Uncertainty:** Whether Trend’s cancelled CI on tip blocks consumers vs transient cancel. **Objection:** Offload cannot apply six Workflows + one Manager-Database silent releases or five format-pause body fixes; that remains the dominant opener drag. Stale Workflows Gate on `12cea89` may overstate tip health if Gate is no longer push-triggered on `main`.
