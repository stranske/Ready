Scorecard: 6 work / 0 partial / 1 broken / 0 fabricated / 0 not exercised of 8; journey: passes (register manager → search → chat → dashboard empty-state); surfaces unscored 0; closed-still-broken 0.

Issues filed: 4 (#1706–#1709). Agents Issue Format Guard success (runs 35656495558, 35656496900, 35656498652, 35656500081).

## Run report — Manager-Database Track D refill — 2026-09-21

**Tip:** `d3d340522c434ebbca5b14e021d6497f7fb20479` (`d3d3405`)

### Context

Supply trigger: 1 agent-ready open issue vs last set of 4 (≤25%). Prior round (2026-09-20) filed #1696–#1699; all four merged on tip before this audit.

### Phase 1.5 scorecard

Re-probed all eight PRODUCT_CONTRACT core functions (MDB-8 added in #1700). Prior fixes verified: delete cascade (#1696), dashboard `load_delta` empty state (#1697), list filters (#1704), conviction `inf` rejection (#1705).

**New broken core function:** MDB-8 alerts — UI stores `filing_type`/`source:sec` conditions but EDGAR events carry `type`/`source:edgar`; rules never fire.

### Verified findings filed

| Issue | Severity | Area |
|---|---|---|
| [#1706](https://github.com/stranske/Manager-Database/issues/1706) | P1 | `new_filing` alert UI condition keys vs EDGAR payload (MDB-8) |
| [#1707](https://github.com/stranske/Manager-Database/issues/1707) | P1 | Acknowledge All ignores inbox filters (MDB-8) |
| [#1708](https://github.com/stranske/Manager-Database/issues/1708) | P1 | Duplicate CIK allowed on SQLite bootstrap (MDB-1 integrity) |
| [#1709](https://github.com/stranske/Manager-Database/issues/1709) | P1 | Bulk import partial commit on mid-batch failure |

### Evidence and verification

All four issue bodies cite paths relative to `stranske/Manager-Database` and were re-opened after filing. The alert mismatch is a live core-function break: `ui/alerts.py` emits `filing_type` and `source=sec`, while `alerts/integration.py` and `etl/edgar_flow.py` provide `type` and `source=edgar`; `alerts/engine.py` compares keys exactly. The second alert finding was exercised with two filtered event types: the visible history contained one record but the bulk acknowledgement endpoint cleared both. The manager findings were also reproduced on a clean SQLite path: duplicate CIK creates returned two `201` responses, and an injected failure on row two of bulk import left row one committed. These were not inferred from static code alone.

The audit independently rechecked the prior refill before filing anything new. Its four closed issues are fixed on the audited tip, and the open backlog contained only the durable dashboards plus a Postgres acceptance-leg issue, so none of #1706–#1709 duplicated an open or recently closed item. GitHub's Agents Issue Format Guard completed successfully for every new issue: runs `35656495558`, `35656496900`, `35656498652`, and `35656500081`.

No owner decision was required. The report does not claim a complete production deployment test: credentialed external EDGAR ingestion and full browser navigation remain outside this local exercise. The product scorecard nevertheless drove every stated core function through an ASGI, CLI, or focused runtime equivalent and explicitly recorded the one broken alert journey.

### Dedup / declined

- #1696–#1699: closed and re-verified fixed; not re-filed.
- Evidence-object schema divergence: known gap; deferred (contract alignment epic, not a live user regression).
- `test_ui_navigation.py` AppTest path failure: test harness resolves `ui/app.py` relative to `tests/`; product navigation smoke passes via `test_full_shell_import_resolves_domain_alerts_package_from_script_directory`.

### Artifacts

- Canonical scorecard: `Code/Audits/Manager-Database/2026-09-21-SCORECARD.md`
- Issue bodies: `Code/Audits/Manager-Database/2026-09-21-issue-bodies/`
- Surface inventory: `Code/Audits/Manager-Database/2026-09-21-surface-inventory.txt`
