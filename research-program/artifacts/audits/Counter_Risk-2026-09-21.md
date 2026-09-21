Scorecard: 4 work / 2 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes fixture-replay deliverables (repo-cash top_changes gap filed #1104); surfaces unscored 2; closed-still-broken 0.

# Counter_Risk Track D audit — 2026-09-21

Unit: `D-audit-Counter_Risk--2026-09-21T20-41-04Z`  
Repo: [stranske/Counter_Risk](https://github.com/stranske/Counter_Risk) @ `1f723517f73d546d718e5a66a636f75783c239c4`  
Trigger: agent-ready supply 2/10 (≤25% of last filed set)

**Issues filed: 3** (#1104–#1106: 1×P1, 2×P2). Agents Issue Format Guard **success** on all three (runs 35653541002, 35653543364, 35653544431).

## Continuity since 2026-09-20

All ten issues from the prior refill (#1081–#1090) merged between `56bee4fa` and `1f72351`. Re-verified on tip:

- `test_concentration_includes_group_name_only_counterparty_rows` PASS (#1092)
- Repo-cash DQ codes, fleet fail status, GUI limit banner, CPRS NaN guard, clearing-house normalize, PDF toggle — all on tip
- No `closed-as-fixed-still-broken` cases on core functions

Open pre-audit agent-ready issues remain #1072 (coverage autopilot) and #1073 (coverage gate path); not duplicated.

## Scorecard detail

| ID | Core function | Score | Notes |
|---|---|---|---|
| CF1 | CLI pipeline | WORKS | Fixture replay → manifest + deliverables under `/tmp/cr-audit-20260921` |
| CF2 | Tk GUI | PARTIAL | Not driven here; Sept fixes merged (#1083, #1087, #1100) |
| CF3 | Concentration/limits | WORKS | Group-name rows included; targeted regressions PASS |
| CF4 | Manifest / movers | PARTIAL | Repo-cash overlay desyncs `NotionalChange` vs `notional_change` (#1104) |
| CF5 | CPRS reconciliation | WORKS | #1082/#1088/#1103 on tip |
| CF6 | Runner.xlsm | NOT EXERCISED | Windows COM |
| CF7 | Frozen bundle | NOT EXERCISED | Windows PyInstaller |

## Findings filed

| Issue | Pri | Summary | Evidence |
|---|---|---|---|
| [#1104](https://github.com/stranske/Counter_Risk/issues/1104) | P1 | Repo-cash overlay leaves `NotionalChange` stale — manifest `top_changes` under-report deltas | `src/counter_risk/compute/rollups.py:302-315`, `src/counter_risk/pipeline/run.py:1836-1854` |
| [#1105](https://github.com/stranske/Counter_Risk/issues/1105) | P2 | Chat delta formatter emits non-finite `notional_change` | `src/counter_risk/chat/session.py:766-768` |
| [#1106](https://github.com/stranske/Counter_Risk/issues/1106) | P2 | Chat `_format_deltas` surfaces only first manifest mover per variant | `src/counter_risk/chat/session.py:746-752` |

## Coverage (8 dimensions)

| Dim | Outcome |
|---|---|
| 1 Correctness | #1104 (delta columns), #1105 (finite chat deltas) |
| 2 Duplication | No new dupes |
| 3 Wiring / output | #1104 (manifest movers vs repo cash) |
| 4 UX / operator | #1106 (chat delta completeness) |
| 5–8 | No new filable items; run.json emitter and provider ID export remain documented gaps |

## Limits

- Windows frozen bundle and Runner.xlsm COM not exercised.
- Full 2228-test suite not awaited; targeted regressions + live repros used.
- Canonical artifacts: `Code/Audits/Counter_Risk/2026-09-21-*`
