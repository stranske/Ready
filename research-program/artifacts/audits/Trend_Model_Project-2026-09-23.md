Scorecard: 1 work / 2 partial / 1 broken / 0 fabricated / 0 not exercised of 4; journey: passes with regime export gap; surfaces unscored 0; closed-still-broken 0.

Issues filed: 3 — https://github.com/stranske/Trend_Model_Project/issues/6053, https://github.com/stranske/Trend_Model_Project/issues/6054, https://github.com/stranske/Trend_Model_Project/issues/6055.

## Run report (Track D, 2026-09-23, attempt 3)

**Tip:** `adda9a41e8a5de37a3c73ea5f19832d75baf571c` on `main` (`git pull` up to date). Resumed from unit checkpoint after attempts 1–2; no duplicate filing.

**Phase 1 (orientation):** Unchanged from attempt 2 (~57k LOC `src/`, CLI subcommands `check run report stress mc app quick-report explain nl`).

**Phase 1.5 (scorecard):** Prior live evidence retained under `artifacts/audits/Trend_Model_Project-2026-09-23-assets/evidence/`. Re-checked on tip:

| Check | Result |
|---|---|
| C1 `trend run` on full demo | Prior exports valid; 72-row truncate still yields empty holdings (not baseline reuse) |
| C2/C4 `report-baseline.html` | `#regimes` still **Regime analysis unavailable** (`artifacts/.../report-baseline.html:141`) |
| C3 `lookback6` vs baseline `analysis_summary.csv` | Still byte-identical (2624 bytes each) |
| C3 `vol_adjust` variant | Prior CAGR/weight delta retained |
| Code seam #6053 | `src/trend_analysis/api.py:132-284` `_run_multi_period_simulation` has no `build_regime_payload`; single-period path still calls it at `src/trend_analysis/stages/portfolio.py:889-897` |
| #6054 | `CostModelSettings` at `src/trend_analysis/config/model.py:344-353` still accepts `inf`/`nan` (repro in `.venv` session) |
| #6055 | `RiskSettings._validate_floor` at `src/trend_analysis/config/model.py:614-623` checks negativity only, not `math.isfinite` (contrast `target_vol` at `:608-609`); `inf`/`nan` still accepted in session repro |

**Dimensions (scoped):** Wiring/deliverable contract (dim 3) only; no additional verified, dedup-clean findings beyond the three filed issues. `regime.lookback` inertness on visible multi_period metrics remains C3 partial; no dedicated issue (no existing open/closed duplicate; subordinate to analyst-visible config sensitivity, not a separate broken core function).

**Findings filed (attempt 1):**

| Issue | Severity | Summary |
|---|---|---|
| #6053 | P1 | Wire Performance by Regime into multi_period `run_simulation` / exports |
| #6054 | P2 | Reject non-finite `portfolio.cost_model` bps on pydantic path |
| #6055 | P2 | Reject non-finite `vol_adjust.floor_vol` before `_scale_factors` (`src/trend_analysis/risk.py:115-134`) |

**Format guard (attempt 3 re-query):** `gh run list` — success on #6053 (run `35867204110`), #6054 (`35867230003`), #6055 (`35867231296`). All three lacked `agents:formatted` despite success; applied label via `gh issue edit` so opener routing matches guard verdict.

**Dedup / refutation:** No new candidates. Closed regime finite-control issues remain distinct from #6053 export seam. No `REFUTED:` lines.

**Delivery:** Ledger + `intake-2026-09-04.log` unchanged (attempt 1). Canonical scorecard: `Code/Audits/Trend_Model_Project/2026-09-23-SCORECARD.md`.

**Confidence:** High on scorecard row and the three defects (CLI/HTML evidence + live pydantic repro + line-level code read). Medium-low that a fourth issue for lookback-only inertness would pass dedup/value bar without overlapping #6053/C3 narrative.
