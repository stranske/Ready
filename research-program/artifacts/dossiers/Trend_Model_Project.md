# Trend_Model_Project — dossier (2026-09-04)

## 1. Purpose in one paragraph
Trend_Model_Project is an allocator-facing manager-of-managers trend-following/CTA portfolio construction and walk-forward backtesting platform. Operating as a local-first, file-executable Python system without database or server dependencies, it ingests historical manager return series, applies multi-metric ranking rules across rolling in-sample windows, constructs constrained out-of-sample portfolio allocations, and generates multi-tab executive workbooks, tearsheets, and risk analytics. It supports local execution and a zero-install client-side WebAssembly distribution (via stlite/Pyodide) for locked-down desktop environments (`src/trend_analysis/pipeline.py:20`, `demo/wasm/index.html:1`).

## 2. Who uses it and how (surfaces)
| Surface | Primary User | Invocation / Entrypoint | Status | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| CLI | Quant Allocator / Ops | `trend run -c <config.yml>` via `src/trend/cli.py` | Working | Dispatches full pipeline and exports (`src/trend/commands/run.py:21`). |
| Streamlit UI | Investment Committee / Analyst | `trend app` via `streamlit_app/app.py` | Working | Interactive 5-page allocation dashboard (`streamlit_app/app.py:12`). |
| Browser WASM | Offline / Restricted Client | `open demo/wasm/index.html` via Pyodide/stlite | Working | Zero-install client bundle (`scripts/build_wasm_site.py:20`). |
| Python API | Research Scripting | `trend_analysis.api.run_simulation()` | Working | Type-annotated simulation entrypoint (`src/trend_analysis/api.py:433`). |
| FastAPI Server | Headless Service | `trend_analysis.api_server:create_app()` | Partial | Exposes `/health` and `/config/patch`, lacks run routes (`src/trend_analysis/api_server/__init__.py:140`). |
| Jupyter GUI | Research Analyst | `trend_analysis.gui.app.display_app()` | Working | In-notebook interactive widgets (`src/trend_analysis/gui/app.py:380`). |
| Export Artifacts | Senior Leadership / Auditor | Output files via `src/trend/commands/report_export.py` | Working | Multi-tab Excel, CSV, HTML, PDF reports (`src/trend_analysis/export/excel.py:35`). |

## 3. Structure map
The repository contains 780 files across two primary root structures:
- `.github/` (66 files): Automations, conformance tests, and PR gates (`.github/workflows/pr-00-gate.yml:1`). Orchestration workflows (`agents-71-codex-belt-dispatcher.yml`) sync from `stranske/Workflows`; local edits are overwritten.
- `src/` (215 files): Core packages: `trend/` (CLI) and `trend_analysis/` (domain models, pipeline, walk-forward engine, scoring, exporters).
- `tests/` (194 files): Test suites enforcing coverage gates.
- `streamlit_app/` (11 files): Multi-page Streamlit web dashboard.
- `demo/` (23 files): Walkthrough configs, synthetic datasets, and standalone WASM distribution.
- `docs/` (143 files): Operational guides, mathematical specs, and architecture records.
- `config/` (18 files): Production and demo YAML pipelines.
- `scripts/` (88 files): Bootstrap, dataset synthesis, and release verification utilities.

## 4. Major code features you must understand to extend it
- **Unified Pipeline Orchestration**: `trend_analysis.pipeline.run_pipeline` coordinates config parsing, data ingestion, returns validation, simulation dispatch, and exports (`src/trend_analysis/pipeline.py:48`).
- **Walk-Forward Rolling Simulation Engine**: `trend_analysis.multi_period.engine.run_multi_period_pipeline` executes rolling in-sample evaluation and out-of-sample execution loops in a monolithic 3,150-line routine (`src/trend_analysis/multi_period/engine.py:736`).
- **Multi-Metric Scoring Engine**: Computes normalized z-scores across rolling metrics (Sharpe, Sortino, Calmar, drawdown) and applies weightings for manager ranking (`src/trend_analysis/scoring.py:53`).
- **Extensible Selection and Weighting Framework**: `SelectorPlugin` and `WeightingSchemePlugin` define modular selection and allocation interfaces (`src/trend_analysis/plugins.py:38`).
- **Cash Buffer Allocation**: Automatically assigns unallocated portfolio weight to synthetic risk-free cash yields (`src/trend_analysis/multi_period/cash.py:22`).
- **Performance Metric Memoization**: Opt-in disk and memory cache for scalar performance calculations via joblib (`src/trend_analysis/metrics/cache.py:28`).
- **Monte Carlo Resampling**: Generates stationary bootstrap and block-resampled synthetic performance distributions (`src/trend_analysis/monte_carlo/resampling.py:41`).
- **Natural Language Query Interface**: Rule-based translation of plain queries into configuration overrides (`src/trend_analysis/nlp/query.py:34`).
- **Comprehensive Reporting Engines**: Formatters producing institutional Excel workbooks with freeze panes, conditional formatting, and auto-filters (`src/trend_analysis/export/excel.py:35`).
- **Config Validation Layer**: Strict runtime validation of nested YAML configurations via Pydantic models (`src/trend_analysis/config/schema.py:44`).

## 5. Data model, identifiers and contracts
- **Manager Identifiers**: The engine operates internally on raw CSV string column labels (`0/3` fleet maturity). An optional mapping layer (`trend_analysis.identity.IdentityMap`) normalizes labels into canonical `fund:<slug>` slugs, but unmapped labels default to `unknown:<label>` (`src/trend_analysis/identity.py:19`).
- **Returns Matrices**: Return data must be represented as a dense, 2D float64 Pandas DataFrame indexed by monotonic monthly DatetimeIndex with clean column labels (`src/trend_analysis/data.py:65`).
- **Run Envelopes**: The platform emits `trend.run_envelope/1` (`src/trend_analysis/export/run_envelope.py:31`) and `trend.run_artifacts/1` (`src/trend_analysis/reporting/run_artifacts.py:344`) containing execution parameters, runtime digests, input hashes, and metric summaries.
- **Contract Conformance**: While documentation references `run-contract/v1`, the codebase actually emits `trend.run_envelope/1`. Backplane conformance validation (`.github/workflows/backplane-conformance.yml:51`) skips because `scripts/emit_reference_run.sh` is missing.

## 6. External inputs and dependencies
- **Input Data**: Ingests tabular CSV, Parquet, or Excel files containing historical manager return series, asset benchmarks, and risk-free cash series (`config/demo.yml:14`). Configurations load from YAML files validated against Pydantic schemas (`config/defaults.yml:1`).
- **Core Dependencies**: Built on Python 3.10+ using `numpy`, `pandas`, `scipy`, and `statsmodels` for computations; `pydantic` and `pyyaml` for config validation; `openpyxl` and `fpdf2` for reporting; and `streamlit` and `plotly` for visualization (`pyproject.toml:42`).
- **Runtime Environment**: Operates fully offline with local-first file I/O, requiring no network access or external database services.

## 7. Current state
The repository is production-ready for single-node CLI analysis, report generation, and interactive dashboard exploration. The CI pipeline (`.github/workflows/pr-00-gate.yml:1`) enforces strict code quality gates, requiring `black`, `ruff`, `mypy`, legacy surface absence verification, and an 80% minimum test coverage threshold (currently achieving ~90.8%). Technical debt and structural gaps persist:
1. ~19 inert configuration keys exist in schemas without engine wiring (`AUDIT_REPORT.md:88`).
2. The core walk-forward engine is concentrated in a 3,150-line monolithic function (`src/trend_analysis/multi_period/engine.py:736`).
3. Parallel backtesting harnesses exhibit divergent execution semantics (`src/trend_analysis/backtesting/harness.py:35`).
4. Daily and weekly frequency configurations are unconditionally coerced to monthly (`src/trend_analysis/stages/preprocessing.py:450`).
5. Transaction cost models in schemas are partially ignored in favor of basis-point calculations (`src/trend_analysis/multi_period/engine.py:1684`).
6. The FastAPI server lacks execution endpoints (`src/trend_analysis/api_server/__init__.py:140`).
7. Reference run scripts for backplane conformance testing are missing (`scripts/emit_reference_run.sh`).
8. Diversification guard UI and configuration persistence remain unimplemented scaffold docs (`docs/diversification_guard_scaffold.md`).

## 8. Claims vs reality
1. **Weighting Configuration Routing**: Docs claim `portfolio.weighting.name: risk_parity` activates risk parity; CLI silently falls back to `EqualWeight()` unless configured as `portfolio.weighting_scheme: risk_parity` (`src/trend_analysis/multi_period/engine.py:1622`).
2. **Frequency Handling**: Docs suggest daily and weekly return support; preprocessing unconditionally resamples to monthly (`ME`) with static annualized factors (`src/trend_analysis/stages/preprocessing.py:450`).
3. **Transaction Cost Configuration**: Schemas validate structured `portfolio.cost_model`, but engine ignores it and only reads `portfolio.transaction_cost_bps` (`src/trend_analysis/multi_period/engine.py:1684`).
4. **Contract Schema Naming**: Fleet specs describe `run-contract/v1`; codebase exclusively emits `trend.run_envelope/1` (`src/trend_analysis/export/run_envelope.py:31`).
5. **Backplane Conformance Automation**: CI claims automated contract conformance verification, but test step unconditionally passes with a warning because `scripts/emit_reference_run.sh` is missing (`.github/workflows/backplane-conformance.yml:51`).
6. **Score-Proportional Weighting**: Documented `ScorePropSimple` plugin exists in code but cannot be activated via YAML config (`src/trend_analysis/weighting.py:31`).
7. **Diversification Guard**: Docs describe active UI and config persistence, but code search reveals only an unimplemented scaffold design (`docs/diversification_guard_scaffold.md:1`).

## 9. Interoperability hooks (for the fleet program)
- **Offers**: Standardized execution outputs including `trend.run_envelope/1` JSON manifests, structured multi-tab Excel workbooks, time-series allocation weights, and normalized manager ranking tables (`src/trend_analysis/export/run_envelope.py:31`).
- **Consumes**: Tabular monthly return matrices (CSV/Parquet) with standardized date indices, YAML execution configuration files, and benchmark index return series (`src/trend_analysis/data.py:65`).
- **Collision Risks**: Hardcoded monthly calendar assumptions (`ME`), unanchored string column identifiers bypassing canonical fleet entity registries, and conflicting contract schema namespaces (`trend.run_envelope/1` vs fleet `run-contract/v1`).

## 10. Reuse candidates
- **Institutional Excel Exporter**: Formatted financial workbook generator supporting freeze panes, auto-fit columns, and conditional accounting formats (`src/trend_analysis/export/excel.py:35`).
- **Financial Metric Calculation Kernel**: Vectorized risk and performance analytics calculating Sharpe, Sortino, Calmar, and drawdowns with optional caching (`src/trend_analysis/metrics/`, `src/trend_analysis/metrics/cache.py:28`).
- **Synthetic Track Record Resampler**: Stationary and block bootstrap Monte Carlo engine for simulating synthetic manager return histories (`src/trend_analysis/monte_carlo/resampling.py:41`).
- **Flexible Scoring and Ranking Engine**: Multi-metric z-score normalizer and weighted metric aggregator for multi-factor evaluation (`src/trend_analysis/scoring.py:53`).
- **Zero-Install WASM Pipeline**: Portable Pyodide/stlite packaging pattern enabling browser-based client-side analytics without local Python setup (`scripts/build_wasm_site.py:20`).
- **Identity Normalization Map**: Configurable alias mapper translating external source strings into canonical entity identifiers (`src/trend_analysis/identity.py:19`).
- **Cash Buffer Rebalancer**: Constrained allocation algorithm ensuring portfolio weights smoothly account for frictional cash balances (`src/trend_analysis/multi_period/cash.py:22`).
- **Pydantic Configuration Validator**: Schema validation layer for complex nested quantitative finance configuration files (`src/trend_analysis/config/schema.py:44`).

## 11. Proposed direction (evidence-based)
1. **Decompose Engine Monolith**: Refactor `run_multi_period_pipeline` into modular stages for window slicing, scoring, portfolio construction, and accounting (`src/trend_analysis/multi_period/engine.py:736`).
2. **Unify Execution Harnesses**: Consolidate parallel backtesting modules to eliminate redundant logic and divergent execution paths (`src/trend_analysis/backtesting/harness.py:35`).
3. **Prune Inert Configuration Keys**: Audit and eliminate the ~19 unused schema parameters to align configuration schemas with actual engine capabilities (`AUDIT_REPORT.md:88`).
4. **Unify Weighting Configuration**: Fix weighting parameter routing so `portfolio.weighting.name` consistently activates desired allocation algorithms (`src/trend_analysis/multi_period/engine.py:1622`).
5. **Harmonize Fleet Run Contracts**: Align emitted JSON schemas with the centralized fleet `run-contract/v1` standard and restore `scripts/emit_reference_run.sh` (`.github/workflows/backplane-conformance.yml:51`).
6. **Adopt Canonical Entity Identifiers**: Upgrade `IdentityMap` from an optional utility into an enforced boundary transform on all ingested manager labels (`src/trend_analysis/identity.py:19`).
7. **Complete or Retire Headless API**: Either wire pipeline execution endpoints into `api_server` or remove the dead service scaffold (`src/trend_analysis/api_server/__init__.py:140`).
8. **Native Multi-Frequency Support**: Refactor the preprocessing pipeline to support genuine daily and weekly frequency calculations without forced monthly downsampling (`src/trend_analysis/stages/preprocessing.py:450`).

## 12. What a colleague needs to know (5 bullets, no code identifiers)
- The system evaluates external investment managers by analyzing historical monthly performance, ranking funds with combined performance metrics, and simulating how a portfolio of top managers would have performed over time.
- All calculations run entirely on your local computer or directly inside a web browser, requiring no database installation, network connection, or cloud services.
- The platform produces investor-grade deliverables including multi-tab Excel workbooks with financial formatting, interactive visual dashboards, and audit-ready execution records.
- Several advanced configuration options—such as daily analysis frequencies, specific custom weighting rules, and certain cost models—are currently simplified or converted to standard monthly rules during simulation.
- Before connecting this tool to other investment office software, fund names and data file formats should be standardized through a shared naming registry to ensure smooth data exchange.
