# D3 unblock sweep — 2026-10-01T15

**Coverage (15/15, Orchestrator excluded):** Run 1 — Workflows → Pension-Data (8). Run 2 (attempt 2) — Ready → Manager-Mosaic (7). **Deferred:** none.

| Repo | Frozen issues / result | Stalled PR reroute | Default-branch state | Agent-ready supply |
|---|---|---|---|---:|
| Workflows | Repaired #3660, #3655, #3653, #3652, #3654, #3657 (format pause cleared); left #3123 (`needs-human` LangSmith tracker) | none | tip `dcec350` check-runs green; Agents Issue Format Guard last success stale vs tip | 20 |
| Travel-Plan-Permission | none | none | tip `4fc442f` checks green; Auto-merge workflow last success stale vs tip | 25 |
| Trend_Model_Project | none | none | tip `a383da6` checks green | 0 |
| Portable-Alpha-Extension-Model | none | none | tip `a97ba41` checks green; Keepalive reporter stale vs tip | 0 |
| Counter_Risk | none | none | tip `2afe707` checks green | 0 |
| Manager-Database | none | none | tip `de1ae7b` checks green | 0 |
| Inv-Man-Intake | none | none | tip `8287825` checks green | 1 |
| Pension-Data | none | none | tip `d4b7b80` checks green; keepalive sweep stale vs tip | 0 |
| Ready | none (open issues are `tracker:durable` only) | none | tip `2e4e980` check-runs green; Actions history stale vs tip | 0 |
| trip-planner | Repaired #1877 (added Tasks/AC with verified paths; removed `agents:auto-pilot-pause`); left #1384/#993 dashboards | none (#1872 active, already has `agent:auto`) | tip `040a1b5` green except Gate Followups rate-limit failure on merge job (not product) | 2 |
| learning-management-system | none | none | tip `f591895` checks green | 0 |
| Fine-Art-Archive | none | none | tip `9986488` checks green | 0 |
| Doc-Lineage | left #1 Dependency Dashboard (bot tracker) | none | tip `fa3406c` checks green | 1 |
| Deliverable-Render | left #1 Dependency Dashboard (bot tracker) | none | tip `3bf3a87` checks green | 1 |
| Manager-Mosaic | none | none | tip `c9018a2` checks green | 11 |

## Genuinely needs the owner

- Workflows #3123 — durable LangSmith observability tracker; ask whether to refresh stale dashboard evidence or accept the pause.

## Priority-label supply warning

Open / `priority:*`-labelled: Workflows 29/4; Travel-Plan-Permission 29/0; Trend_Model_Project 2/0; Portable-Alpha-Extension-Model 2/0; Counter_Risk 2/0; Manager-Database 2/0; Inv-Man-Intake 3/1; Pension-Data 2/0; Ready 3/0; trip-planner 4/1; learning-management-system 3/0; Fine-Art-Archive 4/0; Doc-Lineage 2/0; Deliverable-Render 2/0; Manager-Mosaic 12/8 (#64, #63, #1 lack `priority:*`).

REFUTED: https://github.com/stranske/Workflows/issues/3660 — Manager-Mosaic #78 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/Workflows/issues/3655 — Counter_Risk #1133 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/Workflows/issues/3653 — Fine-Art-Archive #763 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/Workflows/issues/3652 — Inv-Man-Intake #996 merged; active review-thread query empty.

REFUTED: https://github.com/stranske/trip-planner/issues/1877 — at `main` `040a1b5`, `frontend/src/components/workspace/ApprovalPacket.tsx` and `frontend/src/styles.css` match #1837 fields covered by `ApprovalPacket.test.tsx`.

No silent claims (>12h, no open PR), stalled agent PRs (>4h without `agent:auto`), or mechanical red Gate/CI at tip required a PR in this offload workspace.
