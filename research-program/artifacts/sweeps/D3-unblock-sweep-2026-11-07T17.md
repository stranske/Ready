# D3-unblock-sweep-2026-11-07T17

**Run at:** 2026-11-07T17:36:10Z  
**Repos covered:** 8/8 from SUPPORTED_REPOS (Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Manager-Database, Counter_Risk, Inv-Man-Intake, Pension-Data)  
**Deferred:** none

## Summary Table

| Repo | Frozen (left for owner) | Silent claims to release | Stalled PRs | Branch | Supply | Priority gap |
|------|-------------------------|--------------------------|-------------|--------|--------|--------------|
| Workflows | #3901 (non-existent paths) | #4369 | none | GREEN | 16 | 10/34 |
| Travel-Plan-Permission | none | none | none | GREEN | 2 | 2/6 |
| Trend_Model_Project | none | #6190, #6191 | none | GREEN | 2 | 0/4 |
| Portable-Alpha-Extension-Model | #2474 (needs live GitHub access) | none | none | RED | 4 | 4/6 |
| Manager-Database | #1888 (non-existent path) | none | none | RED | 2 | 2/4 |
| Counter_Risk | none | none | none | GREEN | 1 | 1/3 |
| Inv-Man-Intake | none | none | none | GREEN | 0 | 0/2* |
| Pension-Data | none | none | none | RED | 0 | 0/2* |

*Both issues are tracker:durable, excluded from backlog counts

## Details

### Frozen issues (genuinely needs the owner)
- **Workflows#3901**: `agents:auto-pilot-pause` — Task cites non-existent paths (`report/reports/reported/reporting`, etc.), unclear acceptance criteria. Requires owner to fix body or clarify scope.
- **Portable-Alpha-Extension-Model#2474**: `agents:auto-pilot-pause` — Cites non-existent path `rank/distance`, requires live GitHub access for CI evidence. Cannot be resolved by agent.
- **Manager-Database#1888**: `agents:auto-pilot-pause` — Task cites non-existent path `rank/distance`. Requires owner to fix body.

### Silent claims to release (remove `agents:auto-pilot` + `status:in-progress`)
- **Workflows#4369**: Has `status:in-progress`, `agents:auto-pilot`, `agent:auto`, `agent:codex`. No PR referencing it. Last update 2026-11-05T05:01:44Z (>12h stale).
- **Trend_Model_Project#6190**: Has `agents:auto-pilot`. No PR. Last update 2026-11-06T01:12:45Z (>12h stale).
- **Trend_Model_Project#6191**: Has `agents:auto-pilot`. No PR. Last update 2026-11-06T01:12:49Z (>12h stale).

### Red default branches
- **Portable-Alpha-Extension-Model**: Keepalive Loop Reporter failed (mechanical - needs investigation)
- **Manager-Database**: Keepalive Loop Reporter failed (mechanical - needs investigation)
- **Pension-Data**: Keepalive Loop Reporter failed (mechanical - needs investigation)

### Priority label gaps (opener cannot select without priority:*)
- **Workflows**: 10/34 issues have priority labels — 24 issues lack priority and cannot be selected
- **Trend_Model_Project**: 0/4 issues have priority labels — all 4 issues lack priority
- **Counter_Risk**: 1/3 issues have priority labels — 2 issues lack priority

### Agent-ready supply
Total across 8 repos: 26 agent-ready issues

## Actions taken (this sweep)
None — offload workspace cannot edit labels, PRs, or post comments. The above are findings for the orchestrator to act on.

## REFUTATION LINE
None identified in this pass.
