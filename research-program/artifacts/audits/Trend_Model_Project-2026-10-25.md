Scorecard: 3 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 4; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: #6127, #6128, #6129 (Agents Issue Format Guard success on runs 40183195041, 40183196989, 40183197483).

## Run report (Track D refill 2026-10-25)

**Tip:** `96922c1681c3d2f0db740ad1508e811000a9bc2e` (`main`).

**Phase 0–1.5:** Dossier + prior scorecard (2026-09-24) read; bash orientation (CLI inventory, OpenAPI paths, CI green on scheduled workflows). Live probes in isolated temp dirs with `uv run trend` on `config/demo.yml` / `demo/demo_returns.csv`. Regime export regression via `uv run python -m pytest tests/test_multi_period_regime_exports.py` (3 passed after `uv sync --extra dev`).

**Scorecard delta vs 2026-09-24:** C4 remains WORKS; C3 remains PARTIAL on the shipped demo config (lookback moves regime narrative, not aggregate portfolio summary). Product contract on tip already documents bounded lookback WORKS (#6101 closed); still missing a C4 table row → #6129.

**Dimensions (abbreviated):** D3 Monte Carlo wiring/doc gaps verified adversarially (`store_paths` doc-only; scenario `multi_period` override ignored in `_apply_scenario_overrides`; manifest omits merged `data`/`metrics`). D1/D2/D4–D8: no additional verified defects beyond open repo-review backlog (#6093–#6100, #6124–#6125). Streamlit/WASM not browser-driven; core journey exercised via CLI/API-equivalent paths per owner 2026-09-20 rule.

**Dedup:** No filing against closed #6053/#6054/#6055/#6101 (fixes present on tip). #5529 addressed broader bundle layout, not the `store_paths` knob.

**Artifacts:** `Code/Audits/Trend_Model_Project/2026-10-25-SCORECARD.md`, issue bodies under `2026-10-25-issue-bodies/`, unit checkpoint `D-audit-Trend_Model_Project--2026-10-25T08-11-09Z.CHECKPOINT.md`.
