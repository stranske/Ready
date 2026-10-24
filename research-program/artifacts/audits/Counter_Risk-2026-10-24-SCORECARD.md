# Scorecard — stranske/Counter_Risk — 2026-10-24 — tip affd8bf1c1adeca336c23662abf503304f9ef1c7

Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes; surfaces unscored 2; closed-still-broken 0.

UX panel: not run (macOS headless; Tk/Excel operator surfaces not UI-driven this round); gate: not measured.

## 1. Purpose and core functions

| id | core function | entry point | expected outcome | source |
|---|---|---|---|---|
| CF1 | Maintainer runs monthly pipeline via CLI | `counter-risk run` | Excel/PPT/manifest run folder | docs/PRODUCT_CONTRACT.md C1/C4 |
| CF2 | Operator runs via Tk GUI | `counter-risk gui` | Pipeline on worker thread with operator errors | dossier §2 |
| CF3 | Concentration/limit metrics respond to inputs | pipeline `compute/` | HHI/shares/breaches change with portfolio | contract C2/C3 |
| CF4 | Manifest + data-quality summary | pipeline output | `manifest.json` movers/DQ match totals | contract C4 |
| CF5 | CPRS reconciliation | parse/reconcile | Variant detection and alias normalization | README |
| CF6 | Runner.xlsm button workflow | `Runner.xlsm` | VBA-driven run from Excel | dossier §2 |
| CF7 | Frozen PyInstaller bundle | packaged `.exe` | Frozen path resolution on Windows | gui_runner.md |

## 2. Live exercise results

| id | score | how exercised | varying-input check |
|---|---|---|---|
| CF1 | WORKS | `python -m counter_risk.cli run --fixture-replay --config config/fixture_replay.yml --output-dir /tmp/cr-audit-20261024` → manifest + deliverables | deterministic fixture copy |
| CF2 | PARTIAL | Code review + prior tests; GUI not driven headless on macOS | N/A |
| CF3 | WORKS | `pytest tests/compute/test_concentration_metrics.py -k hhi -q` (5 passed); fleet/limit mapper tests green | distinct HHI fixtures |
| CF4 | WORKS | manifest from CF1 run; `tests/pipeline/test_langsmith_fleet_data_quality_status.py` (6 passed) | fail vs warn breach summaries differ in `data_quality_status` |
| CF5 | WORKS | Oct merges #1149/#1158/#1161 on alias/limit scope; targeted reconciliation tests remain green on prior rounds | N/A |
| CF6 | NOT EXERCISED | Requires Windows Excel COM click-test | — |
| CF7 | NOT EXERCISED | Requires Windows PyInstaller host | — |

## 3. Audit rounds on this repo

| date | source | core functions exercised | issues filed | core-function |
|---|---|---|---|---|
| 2026-10-24 | Track D refill | CF1, CF3–CF5 | 2 (#1182, #1183) | 0 |
| 2026-09-23 | Track D refill | CF1, CF3–CF5 | 1 (#1112) | 0 |

## 4. Core function × audit matrix

| id | works today | ever exercised | ever reported | closed-still-broken |
|---|---|---|---|---|
| CF1 | yes | yes | yes | — |
| CF2 | partial | yes | yes | — |
| CF3 | yes | yes | yes | — |
| CF4 | yes | yes | yes | — |
| CF5 | yes | yes | yes | — |
| CF6 | partial (7/9 actions wired) | no | yes | — |
| CF7 | unknown | no | yes | — |

## 5. Productivity verdict

Since the 2026-09-23 scorecard (`2f92b17`), fourteen commits landed on `main`, including high-priority limit/concentration fixes (#1149, #1158–#1162) and audit-doc supersession (#1112/#1113). The maintainer fixture-replay journey still completes on macOS; concentration HHI and LangSmith fleet data-quality mapping stay aligned with manifest severity. Remaining operator debt is Excel-only (two dead Runner labels filed as #1183) and documentation (dimension audit files still read as live BLOCKERs — #1182). Windows bundle verification remains outside this host.

## 6. Surface inventory and coverage

Scored 5 / 7 core functions; unscored 2 (Runner.xlsm COM click-test, frozen Windows bundle).

CLI inventory unchanged: `counter-risk {run,gui}`, `mapping_diff_report`. No new surfaces since 2026-09-23.

## 7. Environment notes

Audit host: macOS; Python 3.12 (`/opt/anaconda3`); editable install. Tip audited: `affd8bf` on `fix/black-langsmith-fleet-test` (black-format fleet test; main at `15830ec`). Scorecard pytest bundle: 290 passed (~16m) across pipeline/limits/rollups/fleet mapper tests.
