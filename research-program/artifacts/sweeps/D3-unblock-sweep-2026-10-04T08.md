# D3 unblock sweep — 2026-10-04T08

**Coverage (attempt 1, 8/14):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

Observed: 2026-10-04T08:31:32Z (live `gh` via `with-gh-auth.sh`). **Offload:** read-only on GitHub; no issue/PR edits, no repair PRs.

| Repository | Frozen issues | Stalled PR reroutes | Default-branch state | Agent-ready supply |
|---|---|---:|---|---:|
| Workflows | Left [#3123](https://github.com/stranske/Workflows/issues/3123) (`needs-human`, LangSmith observability tracker). | 0 | Tip `be2c9a1`: Gate Fork Status Publisher green on `main`. | 10 |
| Travel-Plan-Permission | None | 0 | Tip `2dfae15`: Gate Fork Status Publisher green. | 18 |
| Trend_Model_Project | None | 0 | Tip `c664b0b`: CI success on tip. | 0 |
| Portable-Alpha-Extension-Model | None | 0 | Tip `f40f635`: Gate Fork Status Publisher green. | 0 |
| Counter_Risk | None | 0 | Tip `262a811`: CI success on tip. | 0 |
| Manager-Database | None | 0 | Tip `e1a2460`: CI success on tip. | 0 |
| Inv-Man-Intake | None | 0 | Tip `a8f5dd6`: CI success on tip. | 1 |
| Pension-Data | None | 0 | Tip `9b7c0e7`: CI success on tip. | 0 |

**Silent claims (reviewed, not released):** Workflows [#3694](https://github.com/stranske/Workflows/issues/3694) (consumer-sync review debt; last comment names manifest paths; no open PR but not a bare stall). Workflows [#3123](https://github.com/stranske/Workflows/issues/3123) also matches stale heuristics but is `needs-human` / `tracker:durable` — leave frozen. Portable-Alpha [#2329](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2329) (post-merge verify sequencing; comment explicitly keeps issue open).

**Priority-label gap** (`priority:*` count / open issue count): Workflows 4/21; **Travel-Plan-Permission 0/22** (labels exist in repo but **no** open issue carries `priority:*` — opener cannot rank this backlog); Trend_Model_Project 0/2; Portable-Alpha-Extension-Model 0/3; Counter_Risk 0/2; Manager-Database 0/2; Inv-Man-Intake 1/3; Pension-Data 0/2.

## Genuinely needs the owner

- [#3123](https://github.com/stranske/Workflows/issues/3123) — LangSmith observability degraded vs healthy thresholds: needs a product/ops decision on acceptable publication state, not an agent body edit.

## Offload note

Travel-Plan-Permission losing all `priority:*` labels on open issues (was fully labelled at 2026-10-04T00 sweep) is the highest-risk finding in this batch: **18 agent-ready issues exist but none are opener-selectable** until priorities are reapplied (likely bulk automation or owner call on default priority for formatted backlog).

**Confidence:** High on live branch/supply/stalled-PR checks for these eight repos. High that Travel priority gap is real (verified label list + per-issue scan). Medium on whether Travel priorities were stripped by a workflow regression vs intentional — would change mind if an open Workflows issue documents an expected relabel job.

**REFUTED:** none.
