# Scorecard — stranske/Trend_Model_Project — 2026-11-25 — tip bb216c4b5068a92192507f86de64db5741136d95
Scorecard: 4 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 4; journey: passes; surfaces unscored 0; closed-still-broken 0.

## Core functions

| id | core function | score | evidence |
|---|---|---|---|
| C1 | Run trend model; ranked holdings and portfolio metrics | WORKS | `uv run trend run -c config/demo.yml` — User Weight OS CAGR 1.49%, structured JSONL log emitted |
| C2 | Export deliverables (HTML/CSV/XLSX/JSON) | WORKS | `uv run trend report -c config/demo.yml -i demo/demo_returns.csv --out … --output report.html` — HTML contains Performance by Regime |
| C3 | Config/data changes move results consistently | WORKS | `per_trade_bps` 0→50 moves User Weight OS CAGR 1.49→-4.43 on demo; `tests/test_multi_period_regime_wiring.py::test_multi_period_lookback_reaches_labels_selection_and_regime_report` passed |
| C4 | Regime-enabled exports include Performance by Regime | WORKS | `tests/test_multi_period_regime_exports.py` 3 passed; report HTML grep count 1 |

## Primary journey
`config/demo.yml` + demo returns → `trend run` → stdout metrics → `trend report` HTML deliverable. Completed without blockers.

## Surface inventory (unchanged vs 2026-10-25)
CLI: check, run, report, stress, mc, app, quick-report, explain, nl. Streamlit pages 1–5. FastAPI: `/`, `/health`, `/config/patch`, `/config/patch/preview` (no pipeline run route — interior partial surface, not a scored core function). No new routes/commands since last scorecard.

## Environment notes
Tip `bb216c4` on `main` (+27 commits since 2026-10-25 scorecard). `pytest --collect-only`: 7107 tests. Live exercises via `uv run` in clone working tree.