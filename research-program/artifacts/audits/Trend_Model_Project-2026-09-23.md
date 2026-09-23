Scorecard: 1 work / 2 partial / 1 broken / 0 fabricated / 0 not exercised of 4; journey: passes with regime export gap; surfaces unscored 0; closed-still-broken 0.

Issues filed: 3 — https://github.com/stranske/Trend_Model_Project/issues/6053, https://github.com/stranske/Trend_Model_Project/issues/6054, https://github.com/stranske/Trend_Model_Project/issues/6055.

## Run report (Track D, 2026-09-23)

**Tip:** `adda9a41` on `main` (shallow clone; upstream no longer exposes `phase-3` — dossier default-branch note is stale).

**Phase 1.5 (product scorecard):** Exercised `trend run` / `trend report` on audit-isolated copies of `config/demo.yml` with absolute `data.csv_path` and per-run `export.directory` under `artifacts/audits/Trend_Model_Project-2026-09-23-assets/evidence/`. C1 works on full demo data (eight-manager portfolio). Truncating to 72 return rows yields an empty summary (no silent reuse of the full-demo holdings). C3 partial: enabling `vol_adjust` moves User Weight OS CAGR and weights; changing `regime.lookback` 24→6 leaves `analysis_summary.csv` identical. C4 broken: with `regime.enabled` and in-file `SPX`, unified HTML still shows **Regime analysis unavailable** because `src/trend_analysis/api.py` routes `multi_period` configs away from `build_regime_payload` (`src/trend_analysis/stages/portfolio.py:889-973`).

**Dimensions (scoped):** Wiring/deliverable contract (3/4) plus config validation gaps carried from 2026-09-19 staging. No Streamlit browser pass (CLI/report path exercised per owner 2026-09-20 direction). `.github` fleet sync excluded from filing targets.

**Findings filed:**
| Issue | Severity | Summary |
|---|---|---|
| #6053 | P1 | Wire Performance by Regime into multi_period `run_simulation` / exports |
| #6054 | P2 | Reject non-finite `portfolio.cost_model` bps on pydantic + runtime paths |
| #6055 | P2 | Reject non-finite `vol_adjust.floor_vol` before `_scale_factors` |

**Format guard:** `gh run list` shows Agents Issue Format Guard **success** for #6053 (run 35867204110), #6054 (35867230003), #6055 (35867231296). `agents:formatted` label had not appeared on issues within ~2 minutes of filing; re-check if dispatch depends on it.

**Dedup:** No open/closed duplicate for the multi_period regime export seam. Sept 2026 regime finite-value work tracked in #6025 (closed) and open test-evidence issues #6046–#6048 (distinct).

**Artifacts:** `Code/Audits/Trend_Model_Project/2026-09-23-SCORECARD.md`, `2026-09-23-issue-bodies/`, evidence tree under `research-program/artifacts/audits/Trend_Model_Project-2026-09-23-assets/`.

**Confidence:** High on filed wiring/validation defects (reproduced on tip). Medium on whether `regime.lookback` inertness warrants a separate issue — visible metrics unchanged because turnover cap is scalar `1.0`; subsumed under C3 partial, not separately filed.
