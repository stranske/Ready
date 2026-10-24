Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes; surfaces unscored 2; closed-still-broken 0.

**Issues filed:** #1182, #1183 (2 verified, agent-ready).

## Run report — Track D refill — 2026-10-24

| Field | Value |
|---|---|
| Unit | `D-audit-Counter_Risk--2026-10-24T04-03-28Z` |
| Repo tip | `affd8bf` (`fix/black-langsmith-fleet-test`; `main` at `15830ec`) |
| Prior scorecard | 2026-09-23 @ `2f92b17` (31d stale trigger) |
| Canonical scorecard | `artifacts/audits/Counter_Risk-2026-10-24-SCORECARD.md` |

### Phase 1.5 (product)

- **CF1** fixture-replay CLI completed; `manifest.json` written under `/tmp/cr-audit-20261024`.
- **CF3/CF4** concentration HHI tests (5) and LangSmith fleet `data_quality_status` mapper tests (6) passed; varying-input checks on HHI fixtures and fail vs warn breach summaries.
- **CF5** reconciliation/limit alias fixes from Oct merges (#1149, #1158–#1162) assumed green via prior CI; no regression signal on targeted probes.
- **CF2** partial (GUI not UI-driven on macOS). **CF6/CF7** not exercised (Windows Excel / frozen bundle).

UX panel: not run; gate not measured (headless macOS).

### Dimensions (summary)

| # | Area | Result |
|---|---|---|
| 1 | Code quality | No new P0/P1 defect on tip; Oct PRs tightened limits/concentration scope. |
| 2 | Duplication | No new consolidation finding filed (unchanged from prior rounds). |
| 3 | Wiring / output | Core limit/HHI paths match contract; stale narrative only in `docs/audit/20-*` and `10-calc-core.md` → #1182. |
| 4 | Design / UX | Runner row-5 dead labels D5/I5 verified → #1183; Tk GUI not driven. |
| 5–7 | Field / opportunities / tools | No filable delta on tip. |
| 8 | Automations | Fleet intake succeeded on filed issues; format guard run skipped on first poll (re-check below). |

### Filed issues

1. [#1182](https://github.com/stranske/Counter_Risk/issues/1182) — [P2] Dimension audit markdown still lists superseded BLOCKERs without historical banner.
2. [#1183](https://github.com/stranske/Counter_Risk/issues/1183) — [P2] Runner.xlsm Dry-Run and Ask-about labels have no Form Control or VBA handler.

### Dedup / refutation

- No candidate dropped against a closed issue requiring `REFUTED:` this round.
- #1112 scope intentionally excluded dimension files; #1182 extends banners without contradicting that PR’s non-goals.

### CI / format guard

- Scheduled `main` workflows green at audit start.
- **Agents Issue Format Guard** succeeded for both issues (runs `40061678810`, `40061679230`).

### Surface inventory

Unchanged CLI: `counter-risk {run,gui}`, `mapping_diff_report`. Unscored: Runner.xlsm COM journey, Windows frozen bundle.

### Notes

- Open agent-ready supply was 0/1 per `audit-refill.md`; this round restores backlog with two docs/operator issues.
- Deferred bundle `test_langsmith_fleet_data_quality_status` + `test_run_pipeline` + `test_limits` + `test_rollups`: **290 passed** in ~16m (completed after initial OUT draft).
