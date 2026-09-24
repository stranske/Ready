Scorecard: 3 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 4; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0 (`gh`/GitHub API HTTP 401 on this host). Staged body: `Code/Audits/Trend_Model_Project/2026-09-24-issue-bodies/product-contract-stale-status.md`. Open validation issues #6054/#6055 still reproduce on tip; not re-filed.

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6053 — multi_period `trend report` HTML includes Performance by Regime after PR #6056 on tip `eb7ecfb` (0× "Regime analysis unavailable").

## Run report (Track D, 2026-09-24, unit `D-audit-Trend_Model_Project--2026-09-23T22-11-14Z`)

**Tip:** `eb7ecfb0b10afa2c0c628986f61cd1856d79c633` on `main` (+1 commit since 2026-09-23 audit: merge PR #6056 for #6053).

**Refill trigger:** Prior canonical `Code/Audits/Trend_Model_Project/2026-09-23-SCORECARD.md` omitted the load-bearing `Scorecard:` headline line (backfilled 2026-09-24). Agent-ready supply ≤25% per `artifacts/audit-refill.md`.

**Phase 1 (orientation):** ~57.5k LOC `src/`; CLI subcommands unchanged; `pytest --collect-only` reports 5980 tests with 2 collection errors from host `anaconda` xarray vs NumPy 2.0 (not used as verdict).

**Phase 1.5 (scorecard):** Live exercises under `artifacts/audits/Trend_Model_Project-2026-09-24-assets/evidence/`:

| Check | Result |
|---|---|
| C1 `trend run` full demo + 72-row truncate | Weighted holdings on full run; truncate → 166 B empty `analysis_summary.csv` |
| C2/C4 `trend report` | `#regimes` shows Performance by Regime; regime table rows present |
| C3 `lookback6` vs baseline | `analysis_summary.csv` MD5 identical; CLI regime insight text differs for lookback6 |
| C3 `vol_on` | User Weight OS CAGR 1.49% → 2.61% |
| #6053 seam | `api.run_simulation` populates `performance_by_regime` (`src/trend_analysis/api.py:278-291`); `tests/test_multi_period_regime_exports.py` 3/3 pass |
| #6054/#6055 | `load_config` still accepts `inf`/`nan` cost bps and non-finite `floor_vol` (`src/trend_analysis/config/model.py:344-353`, `:614-623`) |

**Dimensions (scoped):** Product scorecard + config validation wiring (dim 3). No additional verified code defect beyond open #6054/#6055. `docs/PRODUCT_CONTRACT.md` status table stale (C3 `FABRICATED`, missing C4) — docs issue body staged, not filed.

**Dedup:** #6053 fixed on tip (REFUTED). #6054/#6055 assumed still open from prior round; could not `gh issue list` to confirm.

**Delivery:** Canonical scorecard `Code/Audits/Trend_Model_Project/2026-09-24-SCORECARD.md`; audit-run note `2026-09-24-audit-run.md`; ledger appended. Intake log not appended (`gh` unavailable).

**Confidence:** High on scorecard row and #6053 refutation (live HTML + tests). High that #6054/#6055 still reproduce (direct `load_config` repro). Medium-low on GitHub dedup and filing completeness without API access.
