# D3 unblock sweep — 2026-11-04T08 (attempt 1)

**Observed:** ~2026-11-04T08:12Z · **Mode:** synchronous offload (read-only on GitHub; repairs/reroutes/PRs listed as recommended actions, not applied).

**Coverage (8/15 lane repos):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (`Orchestrator` never acted on). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen (found / repaired) | Stalled PR reroutes | Default branch (Gate / CI) | Agent-ready supply |
|---|---:|---:|---|---:|
| Workflows | 19 / **0** (19× `agents:auto-pilot-pause` after format-guard cap; body edits needed) | 0 | Gate workflow last run **failure** on `12cea89` (2026-10-16); no `CI` workflow; head `ff86eb8` — stale Gate, not re-run on tip | 38 |
| Travel-Plan-Permission | 0 / 0 | 0 | [Gate success 2026-10-26](https://github.com/stranske/Travel-Plan-Permission/actions); [CI success 2026-11-04](https://github.com/stranske/Travel-Plan-Permission/actions) | 0 |
| Trend_Model_Project | 0 / 0 | 0 | [Gate + CI success 2026-11-03–04](https://github.com/stranske/Trend_Model_Project/actions) | 1 |
| Portable-Alpha-Extension-Model | 3 / **0** (format-guard cap on #2474, #2476, #2480) | 0 | [Gate success 2026-10-26; CI success 2026-11-04](https://github.com/stranske/Portable-Alpha-Extension-Model/actions) | 4 |
| Counter_Risk | 0 / 0 | 0 | Gate green; [**CI failure** on `main` 2026-11-04](https://github.com/stranske/Counter_Risk/actions/runs/41780013057) — `black --check` on `tests/test_python_floor.py` | 4 |
| Manager-Database | 1 / **0** (#1888 format-guard cap after verifier/coverage disagreement on open PR) | 0 | [Gate + CI success 2026-11-03–04](https://github.com/stranske/Manager-Database/actions) | 4 |
| Inv-Man-Intake | 0 / 0 | 0 | [Gate + CI success 2026-11-04](https://github.com/stranske/Inv-Man-Intake/actions) | 0 |
| Pension-Data | 0 / 0 | 0 | [Gate + CI success 2026-11-04](https://github.com/stranske/Pension-Data/actions) | 0 |

### Priority labelling (`priority:*` vs open implementation issues)

| Repository | With `priority:*` | Open impl issues | Gap |
|---|---:|---:|---|
| Workflows | 28 | 42 | **14** without priority |
| Trend_Model_Project | 0 | 1 | **1** |
| Portable-Alpha-Extension-Model | 4 | 4 | 0 |
| Counter_Risk | 5 | 5 | 0 |
| Manager-Database | 3 | 4 | **1** |
| Travel-Plan-Permission, Inv-Man-Intake, Pension-Data | — | 0 (trackers only) | n/a |

### Silent claims (1b) — recommended label release (no open PR references issue)

**Workflows:** [#4413](https://github.com/stranske/Workflows/issues/4413), [#4402](https://github.com/stranske/Workflows/issues/4402), [#4400](https://github.com/stranske/Workflows/issues/4400), [#3988](https://github.com/stranske/Workflows/issues/3988), [#3978](https://github.com/stranske/Workflows/issues/3978) — stale `agent:*` / `status:in-progress` (>12h, no linked open PR). #4402/#4400/#3978 last comment is format-guard attempt cap (same family as Workflows#3422): drop `agents:auto-pilot`, `status:in-progress`, and stale `agent:*` so opener can retry after body/format work; keep `agents:auto-pilot-pause` until body fixed.

**Others:** none.

### Red-main remediation (recommended)

- **Counter_Risk:** run `black` on `tests/test_python_floor.py` (only file failing lint-format) and open a mechanical PR (offload blocked).
- **Workflows:** trigger or fix **Gate** on current `main`; last Gate failure predates head by ~19 days — treat as operational debt until a fresh Gate run passes on `ff86eb8`.

### Frozen backlog detail (not repaired this pass)

All paused issues share format-guard attempt cap: Tasks/acceptance sections need concrete repo-relative paths (see guard on e.g. [#4402](https://github.com/stranske/Workflows/issues/4402)), then remove `agents:auto-pilot-pause`. **Workflows:** #4417–#4437 band (19 issues). **Portable-Alpha:** #2474, #2476, #2480. **Manager-Database:** #1888 (coverage/verifier evidence dispute on linked PR — body fix may not suffice without PR work).

## Genuinely needs the owner

(none newly identified — frozen items are agent-repairable issue bodies or code/format, not credentials or product calls)

## Refutations

(none this pass)

---

**Confidence:** High on live `gh` reads, silent-claim PR cross-check, and Counter_Risk CI root cause. **Uncertainty:** Whether step 3 should treat a **19-day-old Gate failure** as “red `main`” when head moved without a new Gate run — would change if Gate is required on every push and fails on `ff86eb8`. **Objection:** Nineteen format-guard-paused Workflows issues are fleet throughput drag; this sweep correctly classifies them as agent-fixable, but offload mode leaves them frozen until a non-offload pass edits bodies on GitHub.
