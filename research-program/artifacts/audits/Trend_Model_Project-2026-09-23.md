Scorecard: 1 work / 2 partial / 1 broken / 0 fabricated / 0 not exercised of 4; journey: passes with regime export gap; surfaces unscored 0; closed-still-broken 0.

Issues filed: 3 — https://github.com/stranske/Trend_Model_Project/issues/6053, https://github.com/stranske/Trend_Model_Project/issues/6054, https://github.com/stranske/Trend_Model_Project/issues/6055.

## Run report (Track D, 2026-09-23, attempt 2)

**Tip:** `adda9a41` on `main` (`git pull` already up to date). Attempt 2 resumed from unit checkpoint after attempt 1 filed #6053–#6055 and updated ledger/intake; this pass re-verified findings on the live tree without re-filing duplicates.

**Phase 1 (orientation):** ~57k LOC under `src/`; `uv run pytest --collect-only` reports 5977 tests collected (2 collection errors in streamlit/viz numpy-unicode helpers — environment skew, not re-run as CI substitute).

**Phase 1.5 (scorecard):** Prior live evidence under `artifacts/audits/Trend_Model_Project-2026-09-23-assets/evidence/` retained. Re-checked: `lookback6` vs baseline `analysis_summary.csv` byte-identical (2624 bytes); `report-baseline.html` still contains **Regime analysis unavailable** at `#regimes`. `_run_multi_period_simulation` (`src/trend_analysis/api.py:132-284`) still never calls `build_regime_payload` (contrast `src/trend_analysis/stages/portfolio.py:889-973`). `CostModelSettings` still accepts `inf`/`nan` (`src/trend_analysis/config/model.py:344-353`; reproduced in-session via pydantic).

**Dimensions (scoped, unchanged from attempt 1):** Wiring/deliverable contract (3/4). Dimensions 2, 5–8 not expanded this refill; no additional verified, dedup-clean findings beyond the three filed issues.

**Findings filed (attempt 1; ledger + `intake-2026-09-04.log` already recorded):**
| Issue | Severity | Summary |
|---|---|---|
| #6053 | P1 | Wire Performance by Regime into multi_period `run_simulation` / exports |
| #6054 | P2 | Reject non-finite `portfolio.cost_model` bps on pydantic + runtime paths |
| #6055 | P2 | Reject non-finite `vol_adjust.floor_vol` before `_scale_factors` |

**Format guard:** Attempt 1 logged Agents Issue Format Guard success for #6053–#6055. Attempt 2 could not re-query `gh run list` (`gh` not authenticated in this runtime).

**Dedup / refutation:** No new candidates filed. Closed #6025 (regime finite controls) not re-opened — distinct from multi_period export seam (#6053). No `REFUTED:` lines (no open/closed issue claim disproved on tip).

**Artifacts:** `Code/Audits/Trend_Model_Project/2026-09-23-SCORECARD.md`, `2026-09-23-issue-bodies/`, evidence tree under `research-program/artifacts/audits/Trend_Model_Project-2026-09-23-assets/`.

**Confidence:** High on scorecard row scores and the three filed defects (code + prior CLI evidence + attempt 2 pydantic repro). Medium on whether a separate issue for `regime.lookback` inertness on scalar `max_turnover` configs is worth filing — still subsumed under C3 partial, not filed.
