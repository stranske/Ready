# Trend_Model_Project — verification table (2026-09-04)

Adversarial cite-check of dossier sections **4**, **5**, **8**, and **9** against clone `./clones/Trend_Model_Project`.

| Section | Claim (summary) | Verdict | Notes / correct citation |
| :--- | :--- | :--- | :--- |
| **4** | `pipeline.run_pipeline` orchestrates the full run (`pipeline.py:48`) | **WRONG** | No `run_pipeline` symbol. Orchestration is `run_full` → `run_full_from_config` (`pipeline.py:156-166`, `pipeline_entrypoints.py:233`). |
| **4** | `run_multi_period_pipeline` is a 3,150-line monolith (`engine.py:736`) | **WRONG** | No `run_multi_period_pipeline`. Entry is `run` (`engine.py:1731`); threshold-hold path `_run_threshold_hold_multi_periods` spans `engine.py:2054-4521` (~2,468 lines). Line 736 is inside `_assemble_period_result`. |
| **4** | Multi-metric scoring in `scoring.py:53` | **WRONG** | `scoring.py` does not exist. Metrics/z-scores live in `core/rank_selection.py` (`_zscore` at `1023`, `blended_score` at `1034`). |
| **4** | `SelectorPlugin` / `WeightingSchemePlugin` (`plugins.py:38`) | **WRONG** | Classes are `Selector`, `Rebalancer`, `WeightEngine` in `plugins/__init__.py:58-93`. Line 38 is registry decorator internals. |
| **4** | Cash buffer via `multi_period/cash.py:22` | **WRONG** | `cash.py` missing. Implicit cash buffer in `portfolio/weight_policy.py:55`; explicit cash policy in `cash_policy.py:9-14`. |
| **4** | Scalar metric memoization via `metrics/cache.py:28` + joblib | **WRONG** | `metrics/cache.py` missing. Covariance cache: `perf/cache.py:1-10`; disk rolling cache uses joblib shim at `perf/rolling_cache.py:17`. |
| **4** | Monte Carlo in `monte_carlo/resampling.py:41` | **WRONG** | `resampling.py` missing. Stationary bootstrap: `monte_carlo/models/bootstrap.py:1`, `126`. |
| **4** | Rule-based NL query (`nlp/query.py:34`) | **WRONG** | `nlp/query.py` missing. NL config edits are LLM-driven (`llm/chain.py:1`). |
| **4** | Excel freeze panes (`export/excel.py:35`) | **WRONG** | `export/excel.py` missing. Freeze panes at `export/__init__.py:560`. |
| **4** | Pydantic YAML validation (`config/schema.py:44`) | **WRONG** | `config/schema.py` missing. Validators in `config/model.py` and `config/models.py` (e.g. `validate_trend_config` import at `models.py:29`). |
| **5** | Raw CSV labels; `IdentityMap` → `fund:<slug>`; unmapped → `unknown:<label>` (`identity.py:19`) | **WRONG** (citation) | Substance mostly right: `unknown:{raw}` fallback at `identity.py:77-82`. `fund:<slug>` is config convention, not enforced. Line 19 is `EntityId.resolved`. |
| **5** | Returns as float64 monthly `DatetimeIndex` matrix (`data.py:65`) | **WRONG** | Line 65 is `_coerce_limit_kwarg`. Contract enforced via `data.py:502` → `io/market_data.py:556` (`validate_market_data`). |
| **5** | Emits `trend.run_envelope/1` and `trend.run_artifacts/1` | **CONFIRMED** | `export/run_envelope.py:31`; `reporting/run_artifacts.py:344`. |
| **5** | Backplane conformance skips (missing `emit_reference_run.sh`) | **CONFIRMED** | `.github/workflows/backplane-conformance.yml:51-54`; script absent in clone. |
| **8.1** | `portfolio.weighting.name: risk_parity` ignored; need `weighting_scheme` | **WRONG** | Stale. `_resolve_portfolio_weighting` routes `risk_parity` via weight-engine registry (`engine.py:190-265`); `test_weighting_resolution.py:18-27`. `portfolio.weighting_scheme` is **removed** (`config_contract.py:82-84`). |
| **8.2** | Daily/weekly inputs resampled to monthly | **CONFIRMED** | `preprocessing.py:441-445` resamples to `MONTHLY_DATE_FREQ`; `util/frequency.py:111-113` targets monthly. (Dossier cited line 450 — wrong line.) |
| **8.3** | Engine ignores `cost_model`; only reads `transaction_cost_bps` | **WRONG** | Stale. Engine calls `_resolve_portfolio_cost_bps` (`engine.py:2018`) which reads `portfolio.cost_model.{per_trade_bps,half_spread_bps}` (`config_contract.py:125-153`) and rejects legacy `transaction_cost_bps`. |
| **8.4** | Docs say `run-contract/v1`; code emits `trend.run_envelope/1` | **CONFIRMED** | `run_envelope.py:31`; fleet docs in `docs/contracts/run-contract-v1.md:3`. |
| **8.5** | Backplane CI skips when emitter missing | **CONFIRMED** | `backplane-conformance.yml:51-54`. |
| **8.6** | `ScorePropSimple` unreachable from YAML | **WRONG** | `portfolio.weighting.name: score_prop` maps to `ScorePropSimple` (`engine.py:214-215`; `test_weighting_resolution.py:53-63`). |
| **8.7** | Diversification guard is scaffold only | **CONFIRMED** | `docs/diversification_guard_scaffold.md:5-10` ("No enforcement yet"). |
| **9** | Offers run envelope, Excel, weights, rankings | **CONFIRMED** | `run_envelope.py:31`; Excel `export/__init__.py`; rankings via `core/rank_selection.py`. |
| **9** | Consumes monthly return matrices + YAML (`data.py:65`) | **WRONG** (citation) | Substance confirmed; cite `io/market_data.py:556` / `data.py:502`. |
| **9** | Collision risks: monthly `ME`, string IDs, contract namespace | **CONFIRMED** | Monthly resample `preprocessing.py:442`; identity fallback `identity.py:77-82`; envelope vs fleet contract as in §8.4. |

**Totals:** 24 claims checked · **15 corrected** (wrong citation or wrong substance) · **0 unverifiable** (fleet-maturity `0/3` score retained as narrative context, not scored as a claim).
