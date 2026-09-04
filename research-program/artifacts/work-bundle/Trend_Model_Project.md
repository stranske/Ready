# Trend_Model_Project — dossier (2026-09-04)

## 1. Purpose in one paragraph
Trend_Model_Project is an allocator-facing manager-of-managers trend-following/CTA portfolio construction and walk-forward backtesting platform. Operating as a local-first, file-executable Python system without database or server dependencies, it ingests historical manager return series, applies multi-metric ranking rules across rolling in-sample windows, constructs constrained out-of-sample portfolio allocations, and generates multi-tab executive workbooks, tearsheets, and risk analytics. It supports local execution and a zero-install client-side WebAssembly distribution (via stlite/Pyodide) for locked-down desktop environments (`demo/wasm/index.html:1`, `scripts/build_wasm_site.py:20`).

## 2. Who uses it and how (surfaces)
| Surface | Primary User | Invocation / Entrypoint | Status | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| CLI | Quant Allocator / Ops | `trend run -c <config.yml>` via `src/trend/cli.py` | Working | Dispatches full pipeline via `run_analysis_command` (`src/trend/cli_commands.py:105`). |
| Streamlit UI | Investment Committee / Analyst | `trend app` → `streamlit_app/app.py` | Working | Five-page dashboard under `streamlit_app/pages/` (`1_Data.py` … `5_Monte_Carlo.py`). |
| Browser WASM | Offline / Restricted Client | `open demo/wasm/index.html` via Pyodide/stlite | Working | Zero-install client bundle (`scripts/build_wasm_site.py:20`, `demo/wasm/index.html:1`). |
| Python API | Research Scripting | `trend_analysis.api.run_simulation()` | Working | Type-annotated simulation entrypoint (`src/trend_analysis/api.py:425`). |
| FastAPI Server | Headless Service | `trend_analysis.api_server:app` (`run()` at module bottom) | Partial | Exposes `/health` and `/config/patch` (+ preview); no pipeline run routes (`src/trend_analysis/api_server/__init__.py:140-189`). |
| Jupyter GUI | Research Analyst | `trend_analysis.gui.app.launch()` | Working | In-notebook interactive widgets (`src/trend_analysis/gui/app.py:875`). |
| Export Artifacts | Senior Leadership / Auditor | Output files via `src/trend/commands/report_export.py` | Working | Multi-tab Excel, CSV, HTML, PDF reports (`src/trend_analysis/export/__init__.py:560`). |

## 3. Structure map
The repository contains ~2,778 tracked files across these primary roots (counts from clone, 2026-09-04):
- `.github/` (~280 files): Automations, conformance tests, and PR gates (`.github/workflows/pr-00-gate.yml:1`). Orchestration workflows (`fleet-synced agent automation workflow`) sync from `a shared engineering-standards repository`; local edits are overwritten.
- `src/` (~219 files): Core packages: `trend/` (CLI) and `trend_analysis/` (domain models, pipeline, walk-forward engine, scoring, exporters).
- `tests/` (~716 files): Test suites enforcing coverage gates.
- `streamlit_app/` (~33 files): Multi-page Streamlit web dashboard.
- `demo/` (~163 files): Walkthrough configs, synthetic datasets, and standalone WASM distribution.
- `docs/` (~309 files): Operational guides, mathematical specs, and architecture records.
- `config/` (~34 files): Production and demo YAML pipelines.
- `scripts/` (~141 files): Bootstrap, dataset synthesis, and release verification utilities.

## 4. Major code features you must understand to extend it
- **Unified Pipeline Orchestration**: `run_full` / `run_full_from_config` coordinate config parsing, data ingestion, returns validation, simulation dispatch, and exports (`src/trend_analysis/pipeline.py:156-166`, `src/trend_analysis/pipeline_entrypoints.py:233`).
- **Walk-Forward Rolling Simulation Engine**: `trend_analysis.multi_period.engine.run` executes rolling in-sample evaluation and out-of-sample execution, delegating to `_run_phase1_multi_periods` or the large `_run_threshold_hold_multi_periods` routine (~2,468 lines) (`src/trend_analysis/multi_period/engine.py:1731`, `2054-4521`).
- **Multi-Metric Scoring Engine**: `trend_analysis.core.rank_selection` computes Sharpe, Sortino, Calmar, drawdown, and blended z-score rankings across rolling windows (`src/trend_analysis/core/rank_selection.py:866`, `1023`, `1034`).
- **Extensible Plugin Framework**: `Selector`, `Rebalancer`, and `WeightEngine` plugin registries define modular selection, rebalancing, and risk-based weighting (`src/trend_analysis/plugins/__init__.py:58-93`).
- **Cash Buffer Handling**: Weight policies can leave weights unnormalized so residual mass represents an implicit cash buffer; `CashPolicy` controls explicit cash rows in rebalancers (`src/trend_analysis/portfolio/weight_policy.py:55`, `src/trend_analysis/cash_policy.py:9-14`).
- **Performance Caching**: In-memory covariance cache plus optional disk-backed rolling cache via joblib shim (`src/trend_analysis/perf/cache.py:1-10`, `src/trend_analysis/perf/rolling_cache.py:17`).
- **Monte Carlo Resampling**: Stationary bootstrap and related return models under `monte_carlo/models/` (`src/trend_analysis/monte_carlo/models/bootstrap.py:1`, `126`).
- **Natural Language Config Interface**: LLM-driven translation of plain-language instructions into validated `ConfigPatch` operations (`src/trend_analysis/llm/chain.py:1`).
- **Comprehensive Reporting Engines**: Formatters producing institutional Excel workbooks with freeze panes, conditional formatting, and auto-filters (`src/trend_analysis/export/__init__.py:560`).
- **Config Validation Layer**: Strict runtime validation of nested YAML configurations via Pydantic models (`src/trend_analysis/config/model.py`, `src/trend_analysis/config/models.py:29`).

## 5. Data model, identifiers and contracts
- **Manager Identifiers**: The engine operates internally on raw CSV string column labels. An optional mapping layer (`trend_analysis.identity.IdentityMap`) resolves labels to configured `canonical_id` values (commonly `fund:<slug>` in universe files); unmapped labels default to `unknown:<label>` (`src/trend_analysis/identity.py:77-82`).
- **Returns Matrices**: Return data must satisfy the shared market-data contract (datetime index or `Date` column, numeric return columns) validated on ingest (`src/trend_analysis/data.py:502`, `src/trend_analysis/io/market_data.py:556`).
- **Run Envelopes**: The platform emits `trend.run_envelope/1` (`src/trend_analysis/export/run_envelope.py:31`) and `trend.run_artifacts/1` (`src/trend_analysis/reporting/run_artifacts.py:344`) containing execution parameters, runtime digests, input hashes, and metric summaries.
- **Contract Conformance**: Fleet documentation references `run-contract/v1`, while this repo currently emits `trend.run_envelope/1`. Backplane conformance validation (`.github/workflows/backplane-conformance.yml:51`) skips because `scripts/emit_reference_run.sh` is missing.

## 6. External inputs and dependencies
- **Input Data**: Ingests tabular CSV, Parquet, or Excel files containing historical manager return series, asset benchmarks, and risk-free cash series (`config/demo.yml:4-11`). Configurations load from YAML files validated against Pydantic schemas (`config/defaults.yml:1`).
- **Core Dependencies**: Built on Python 3.10+ using `numpy`, `pandas`, and `scipy` for computations; `pydantic` and `PyYAML` for config validation; `openpyxl` and `fpdf2` for reporting; optional `streamlit` and `plotly` for visualization (`pyproject.toml:38-56`, optional extras at `pyproject.toml:87`).
- **Runtime Environment**: Operates fully offline with local-first file I/O, requiring no network access or external database services.

## 7. Current state
The repository is production-ready for single-node CLI analysis, report generation, and interactive dashboard exploration. The CI pipeline (`.github/workflows/pr-00-gate.yml:73`) enforces strict code quality gates, requiring `black`, `ruff`, `mypy`, legacy surface absence verification, and an 80% minimum test coverage threshold (baseline notes ~90.8% measured as of 2026-08-26 in `config/coverage-baseline.json`). Technical debt and structural gaps persist:
1. ~19 inert configuration keys exist in schemas without engine wiring (`AUDIT_REPORT.md:88-102`).
2. The threshold-hold walk-forward path is concentrated in a ~2,468-line routine (`src/trend_analysis/multi_period/engine.py:2054-4521`).
3. A separate `backtesting/harness.py` walk-forward path coexists with the main multi-period engine, with overlapping but not identical cost/turnover semantics (`src/trend_analysis/backtesting/harness.py:1`, `145`).
4. Daily and weekly frequency configurations are resampled to monthly before simulation (`src/trend_analysis/stages/preprocessing.py:441-445`, `src/trend_analysis/util/frequency.py:111-113`).
5. Legacy `portfolio.transaction_cost_bps` / `portfolio.weighting_scheme` keys are rejected in favor of `portfolio.cost_model` and `portfolio.weighting.name` (`src/trend_analysis/config_contract.py:82-84`, `125-134`).
6. The FastAPI server lacks pipeline execution endpoints (`src/trend_analysis/api_server/__init__.py:140-189`).
7. Reference run scripts for backplane conformance testing are missing (`scripts/emit_reference_run.sh`).
8. Diversification guard UI and configuration persistence remain unimplemented scaffold docs (`docs/diversification_guard_scaffold.md:5-10`).

## 8. Claims vs reality
1. **Weighting configuration (outdated audit claim)**: Older docs/audits claimed `portfolio.weighting.name: risk_parity` silently fell back to equal weight and required a separate `portfolio.weighting_scheme` key. Current code routes `portfolio.weighting.name` (including `risk_parity`, `score_prop`, etc.) through `_resolve_portfolio_weighting`, and `portfolio.weighting_scheme` is removed (`src/trend_analysis/multi_period/engine.py:190-265`, `src/trend_analysis/config_contract.py:82-84`, `tests/test_weighting_resolution.py:18-27`).
2. **Frequency handling**: Docs may suggest daily/weekly end-to-end support; preprocessing resamples non-monthly series to month-end (`ME`) before simulation (`src/trend_analysis/stages/preprocessing.py:441-445`, `src/trend_analysis/util/frequency.py:111-113`).
3. **Transaction cost configuration (outdated audit claim)**: Older audits claimed the main engine ignored `portfolio.cost_model`. Current multi-period runs resolve costs from `portfolio.cost_model.{per_trade_bps,half_spread_bps}` via `resolve_portfolio_cost_bps` (`src/trend_analysis/multi_period/engine.py:2018`, `src/trend_analysis/config_contract.py:125-153`).
4. **Contract schema naming**: Fleet specs describe `run-contract/v1`; this repo's export envelope uses `trend.run_envelope/1` (`src/trend_analysis/export/run_envelope.py:31`, `docs/contracts/run-contract-v1.md:3`).
5. **Backplane conformance automation**: CI workflow checks for `scripts/emit_reference_run.sh` and skips conformance when absent (`.github/workflows/backplane-conformance.yml:51-54`).
6. **Score-proportional weighting (outdated audit claim)**: `ScorePropSimple` is reachable via `portfolio.weighting.name: score_prop` (aliases include `score_prop_simple`) (`src/trend_analysis/weighting.py:31`, `src/trend_analysis/multi_period/engine.py:214-215`, `tests/test_weighting_resolution.py:53-63`).
7. **Diversification guard**: Docs describe future UI/config persistence; code search shows only an unimplemented scaffold (`docs/diversification_guard_scaffold.md:5-10`).

## 9. Interoperability hooks (for the fleet program)
- **Offers**: Standardized execution outputs including `trend.run_envelope/1` JSON manifests, structured multi-tab Excel workbooks, time-series allocation weights, and normalized manager ranking tables (`src/trend_analysis/export/run_envelope.py:31`, `src/trend_analysis/export/__init__.py:560`).
- **Consumes**: Tabular monthly return matrices (CSV/Parquet) with standardized date indices, YAML execution configuration files, and benchmark index return series (`src/trend_analysis/io/market_data.py:556`, `config/demo.yml:4-11`).
- **Collision Risks**: Hardcoded monthly calendar assumptions (`ME`), unanchored string column identifiers bypassing canonical fleet entity registries, and conflicting contract schema namespaces (`trend.run_envelope/1` vs fleet `run-contract/v1`).

## 10. Reuse candidates
- **Institutional Excel Exporter**: Formatted financial workbook generator supporting freeze panes, auto-fit columns, and conditional accounting formats (`src/trend_analysis/export/__init__.py:560`).
- **Financial Metric Calculation Kernel**: Vectorized risk and performance analytics calculating Sharpe, Sortino, Calmar, and drawdowns with optional caching (`src/trend_analysis/core/rank_selection.py`, `src/trend_analysis/perf/cache.py:1-10`).
- **Synthetic Track Record Resampler**: Stationary bootstrap Monte Carlo engine for simulating synthetic manager return histories (`src/trend_analysis/monte_carlo/models/bootstrap.py:1`).
- **Flexible Scoring and Ranking Engine**: Multi-metric normalizer and weighted metric aggregator for multi-factor evaluation (`src/trend_analysis/core/rank_selection.py:866`, `1034`).
- **Zero-Install WASM Pipeline**: Portable Pyodide/stlite packaging pattern enabling browser-based client-side analytics without local Python setup (`scripts/build_wasm_site.py:20`).
- **Identity Normalization Map**: Configurable alias mapper translating external source strings into canonical entity identifiers (`src/trend_analysis/identity.py:77-82`).
- **Cash Buffer Weight Policy**: Allocation helper preserving implicit cash when weights are not fully invested (`src/trend_analysis/portfolio/weight_policy.py:55`).
- **Pydantic Configuration Validator**: Schema validation layer for complex nested quantitative finance configuration files (`src/trend_analysis/config/model.py`).

## 11. Proposed direction (evidence-based)
1. **Decompose Engine Monolith**: Refactor `_run_threshold_hold_multi_periods` into modular stages for window slicing, scoring, portfolio construction, and accounting (`src/trend_analysis/multi_period/engine.py:2054-4521`).
2. **Unify Execution Harnesses**: Consolidate `backtesting/harness.py` with the main multi-period engine to eliminate redundant logic and divergent execution paths (`src/trend_analysis/backtesting/harness.py:145`).
3. **Prune Inert Configuration Keys**: Audit and eliminate unused schema parameters to align configuration schemas with actual engine capabilities (`AUDIT_REPORT.md:88-102`).
4. **Harmonize Fleet Run Contracts**: Align emitted JSON schemas with the centralized fleet `run-contract/v1` standard and restore `scripts/emit_reference_run.sh` (`.github/workflows/backplane-conformance.yml:51`).
5. **Adopt Canonical Entity Identifiers**: Upgrade `IdentityMap` from an optional utility into an enforced boundary transform on all ingested manager labels (`src/trend_analysis/identity.py:77-82`).
6. **Complete or Retire Headless API**: Either wire pipeline execution endpoints into `api_server` or remove the dead service scaffold (`src/trend_analysis/api_server/__init__.py:140-189`).
7. **Native Multi-Frequency Support**: Refactor the preprocessing pipeline to support genuine daily and weekly frequency calculations without forced monthly downsampling (`src/trend_analysis/stages/preprocessing.py:441-445`).
8. **Implement or Retire Diversification Guard**: Complete the scaffold in `docs/diversification_guard_scaffold.md` or remove UI references until enforcement exists.

## 12. What a colleague needs to know (5 bullets, no code identifiers)
- The system evaluates external investment managers by analyzing historical monthly performance, ranking funds with combined performance metrics, and simulating how a portfolio of top managers would have performed over time.
- All calculations run entirely on your local computer or directly inside a web browser, requiring no database installation, network connection, or cloud services.
- The platform produces investor-grade deliverables including multi-tab Excel workbooks with financial formatting, interactive visual dashboards, and audit-ready execution records.
- Several advanced configuration options—such as daily analysis frequencies and certain legacy config key names—are currently simplified, rejected, or converted to standard monthly rules during simulation.
- Before connecting this tool to other investment office software, fund names and data file formats should be standardized through a shared naming registry to ensure smooth data exchange.
*Evidence-checked against source repositories; verification metadata omitted from work bundle.*
