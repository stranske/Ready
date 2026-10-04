# D3 unblock sweep — 2026-10-01T07

**Run 1 (cap 8):** Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data.

**Run 2 (resume):** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

**Deferred:** Orchestrator (fleet policy — not acted on). No other repos remain in `SUPPORTED_REPOS`.

| Repo | Frozen issues / result | Stalled PR reroute | Default-branch state | Agent-ready supply |
|---|---|---|---|---:|
| Workflows | Repaired #3662, #3661, #3657; left #3652–#3655 and #3660 frozen (merged consumer PRs, zero active review threads); #3123 durable LangSmith tracker | none | Gate Fork Status Publisher passed at `b7a1147` | 24 |
| Travel-Plan-Permission | none | none | latest successful automation stale vs tip; no failed Gate/CI in last 5 | 25 |
| Trend_Model_Project | none | none | automation health passed at tip; no failed Gate/CI in last 5 | 0 |
| Portable-Alpha-Extension-Model | none | none | automation health stale vs tip; no failed Gate/CI in last 5 | 0 |
| Counter_Risk | none | none | automation health stale vs tip; no failed Gate/CI in last 5 | 0 |
| Manager-Database | none; #1742 active with PR #1743 | none | Auto-Pilot queued at tip | 1 |
| Inv-Man-Intake | none | none | automation health passed at tip | 1 |
| Pension-Data | none | none | automation health passed at tip | 0 |
| Ready | none | none | CI workflow last run failed on older SHA (`f0b4607`); current `main` (`2e4e980`) check-runs green — no fix filed | 0 |
| trip-planner | left #1877 paused (format attempt-cap); #1/#1384 dashboards not touched | none; #1872 updated within 4h | CI passed at tip `9041478`; Gate workflow last success stale vs tip | 2 |
| learning-management-system | none | none | CI workflow last run stale vs tip; commit checks green on `f591895` | 0 |
| Fine-Art-Archive | none | none | CI passed at tip `9986488` | 0 |
| Doc-Lineage | left #1 Dependency Dashboard (bot tracker) | none | CI passed at tip `fa3406c` | 1 |
| Deliverable-Render | left #1 Dependency Dashboard (bot tracker) | none | CI passed at tip `3bf3a87` | 1 |
| Manager-Mosaic | none | none | CI passed at tip `c9018a2` | 11 |

## Genuinely needs the owner

- Workflows #3123 — durable LangSmith observability tracker; ask whether to restore stale dashboard evidence or accept the pause.

## Priority-label supply warning

Open / `priority:*`-labelled counts: Workflows 33/6; Travel-Plan-Permission 29/0; Trend_Model_Project 2/0; Portable-Alpha-Extension-Model 2/0; Counter_Risk 2/0; Manager-Database 3/0; Inv-Man-Intake 3/1; Pension-Data 2/0; Ready 3/0; trip-planner 4/1; learning-management-system 3/0; Fine-Art-Archive 4/0; Doc-Lineage 2/0; Deliverable-Render 2/0; Manager-Mosaic 12/8 (#64, #63, #1 lack `priority:*`).

REFUTED: https://github.com/stranske/Workflows/issues/3660 — Manager-Mosaic #78 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/Workflows/issues/3655 — Counter_Risk #1133 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/Workflows/issues/3654 — Template #1051 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/Workflows/issues/3653 — Fine-Art-Archive #763 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/Workflows/issues/3652 — Inv-Man-Intake #996 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/trip-planner/issues/1877 — at `main` `9041478`, `frontend/src/components/workspace/ApprovalPacket.tsx` and `frontend/src/styles.css` already implement the cited budget, cost/`price_source`, print, and journey fields covered by `ApprovalPacket.test.tsx`.

No silent claims (>12h, no open PR), stalled agent PRs (>4h without `agent:auto` already present), or mechanical red Gate/CI at tip required a PR in this offload workspace.
