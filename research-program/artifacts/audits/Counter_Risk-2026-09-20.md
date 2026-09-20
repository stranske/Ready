Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes through fixture-replay deliverables (Excel workbooks + PPT + manifest); surfaces unscored 2 (Runner.xlsm COM, frozen Windows bundle); closed-still-broken 0.

# Counter_Risk Track D audit — 2026-09-20

Unit: `D-audit-Counter_Risk--2026-09-20T20-25-21Z`  
Repo: [stranske/Counter_Risk](https://github.com/stranske/Counter_Risk) @ `56bee4faf6658b7031be5d9c7cc81b82735361ee`  
Trigger: agent-ready supply 2/4 (≤25% of last filed set)

**Issues filed: 10** (#1081–#1090: 3×P1, 7×P2). All bodies pre-validated with `.github/scripts/issue_format.py`; Agents Issue Format Guard runs observed success on filed issues.

## Scorecard detail

| ID | Core function | Score | How exercised |
|---|---|---|---|
| CF1 | Maintainer runs monthly pipeline via CLI | WORKS | `counter-risk run --fixture-replay --config config/fixture_replay.yml` → deliverables under `/tmp/cr-audit-20260920` |
| CF2 | Operator runs via Tk GUI | PARTIAL | Code review + headless GUI tests exist; Windows operator path not driven here |
| CF3 | Concentration/limit metrics respond to inputs | WORKS | Prior #1061/#1062 regression tests pass; new gap found for `group_name`-only totals rows (#1081) |
| CF4 | Manifest + data-quality summary | WORKS | Fixture replay writes manifest; fleet status under-reporting filed #1084 |
| CF5 | CPRS reconciliation | PARTIAL | NaN notionals misclassified as informational (#1082); clearing-house alias false gap (#1088) |
| CF6 | Runner.xlsm button workflow | NOT EXERCISED | Requires Windows Excel COM |
| CF7 | Frozen PyInstaller bundle | NOT EXERCISED | Requires Windows host |

Varying-input check (CF3): alias limit + split counterparty tests on tip both pass after #1061/#1062 merges; new `#1081` repro shows group_name-only rows still dropped.

## Findings filed

| Issue | Pri | Summary | Evidence |
|---|---|---|---|
| [#1081](https://github.com/stranske/Counter_Risk/issues/1081) | P1 | `group_name`-only counterparties omitted from concentration rows | `src/counter_risk/pipeline/run.py:2305-2307` |
| [#1082](https://github.com/stranske/Counter_Risk/issues/1082) | P1 | Non-finite CPRS totals → informational NaN gap | `src/counter_risk/pipeline/run.py:4839-4892` |
| [#1083](https://github.com/stranske/Counter_Risk/issues/1083) | P1 | GUI hides limit banner on failed runs | `src/counter_risk/gui/runner.py:273-533` |
| [#1084](https://github.com/stranske/Counter_Risk/issues/1084) | P2 | Fleet telemetry never emits fail data-quality status | `src/counter_risk/pipeline/run.py:725` |
| [#1085](https://github.com/stranske/Counter_Risk/issues/1085) | P2 | `top_changes` accepts NaN notional_change | `src/counter_risk/compute/rollups.py:411-437` |
| [#1086](https://github.com/stranske/Counter_Risk/issues/1086) | P2 | Repo-cash warnings miscategorized in manifest DQ rollup | `src/counter_risk/pipeline/data_quality.py:506-547` |
| [#1087](https://github.com/stranske/Counter_Risk/issues/1087) | P2 | GUI lacks Export PDF toggle wired to CLI | `src/counter_risk/gui/runner.py:468-478` |
| [#1088](https://github.com/stranske/Counter_Risk/issues/1088) | P2 | Clearing-house alias false reconciliation gap | `src/counter_risk/pipeline/reconciliation.py:177-178` |
| [#1089](https://github.com/stranske/Counter_Risk/issues/1089) | P2 | Distribution PPT marked success when master failed | `src/counter_risk/pipeline/manifest.py:246` |
| [#1090](https://github.com/stranske/Counter_Risk/issues/1090) | P2 | Trend CPRS misclassified when filename contains "all" | `src/counter_risk/parsers/cprs_ch.py:385-386` |

## Dedup / continuity

- Sept-13 staged bodies (#1061–#1068) were already closed on tip; re-verified #1062 concentration test passes (not re-filed).
- No `closed-as-fixed-still-broken` cases on core functions this round.
- Open pre-audit agent-ready issues: #1072 (coverage autopilot), #1073 (coverage gate test path).

## Coverage (8 dimensions)

| Dim | Outcome |
|---|---|
| 1 Correctness | #1081, #1082, #1085, #1090 |
| 2 Duplication | No new behavior-divergent dupes filed |
| 3 Wiring / output | #1082, #1084, #1086, #1088, #1089 |
| 4 UX / operator | #1083, #1087 |
| 5 Public field | Advisory only (traceability over silent coercion) |
| 6 Opportunities | Deferred (run.json emitter, provider ID export — documented in dossier) |
| 7 Tools | Deferred |
| 8 Local automation | Format guard verified on filing |

## Limits

- Windows frozen bundle, Runner.xlsm COM, and browser demo not exercised.
- Full pytest suite not awaited (2189 collected; targeted repros + alias/concentration regressions run).
- Canonical artifacts: `Code/Audits/Counter_Risk/2026-09-20-*`
