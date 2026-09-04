# Manager-Database — dossier (2026-09-04)

## 1. Purpose in one paragraph

Manager-Database is an investment surveillance platform for institutional allocators tracking external equity managers, quarterly portfolio shifts, activist campaigns, and diligence notes alongside regulatory filings. It ingests SEC EDGAR (13F-HR, 13D/G) and Companies House filings, reconciles amendments, computes conviction scores and position deltas, and links holdings with news. It runs containerized (FastAPI, PostgreSQL/pgvector, MinIO, Prefect) behind firewalls or compiles via WebAssembly into an offline browser demo.

## 2. Who uses it and how (surfaces)

| Surface | Entry point (file) | Who uses it | Status (working / partial / scaffold) with evidence |
| :--- | :--- | :--- | :--- |
| Web UI | `ui/app.py` (`mgrdb-app`) | Analysts | **Working**. Streamlit app (`ui/app.py:12`), console script `mgrdb-app` (`pyproject.toml:38`, `ui/launch.py:27-41`), verified in `tests/test_ui_navigation.py`. |
| Browser Demo | `web/index.html` | Allocators | **Working**. Pyodide app (`web/wasm_app.py:42`), verified in `tests/test_wasm_demo_build.py`. |
| REST API | `api/chat.py` | UI & services | **Working**. FastAPI routers (`api/chat.py:47`), verified in `tests/test_chat_api.py`. |
| Scheduled ETL | `etl/edgar_flow.py`, `etl/news_flow.py` | Operations | **Partial**. EDGAR flows work (`tests/test_edgar_flow.py`); foreign stubs return `unsupported` (`adapters/canada.py:44`, `adapters/asic.py:67`, `adapters/mas.py:53`). |
| CLI Tools | `diff_holdings.py`, `scripts/db_snapshot_restore.py` | Engineers | **Working**. Computes deltas (`diff_holdings.py:157`) and S3 backups (`tests/test_db_snapshot_restore.py`). |
| Observability | `llm/langsmith_fleet.py`, `tools/run_contract.py` | Orchestrators | **Partial**. Emits `langsmith-fleet/v1` (`llm/langsmith_fleet.py:27`); wire contract un-emitted (`.github/workflows/backplane-conformance.yml:54`). |

## 3. Structure map

Top functional directories (synced from `stranske/Workflows`):

- `adapters/`: Ingestion (EDGAR, Companies House, OpenFIGI, prices, news, foreign stubs).
- `alembic/`: Database migrations.
- `alerts/`: Engine and dispatchers (Email, Slack, Webhook).
- `api/`: FastAPI routers (managers, signals, activism, alerts, chat).
- `chains/`: LangChain intent, summary, and RAG pipelines.
- `config/`: Model catalogs and settings.
- `data/`: Filings and synthetic SQLite fixtures.
- `docs/`: Specs, audits, and fleet contracts.
- `etl/`: Prefect flows (EDGAR, point-in-time, diffs, conviction, backtests).
- `llm/`: Client wrappers, prompt defenses, LangSmith telemetry.
- `monitoring/`: Profiling logs and memory diagnostics.
- `scripts/`: Tools (WASM builder, S3 backup/restore).
- `tests/`: Test suite (unit, integration, golden, Playwright).
- `tools/`: Run envelopes (`RunResult`), coverage guards, model registry.
- `ui/`: Streamlit dashboard and research pages.
- `utils/`: CIK normalization, numeric parsing, PDF extraction.
- `web/`: Offline stlite/Pyodide WASM demo.

## 4. Major code features you must understand to extend it

- **Holdings Diff Engine** (`diff_holdings.py`: `diff_holdings`): Reconciles 13F filings against amendments (`/A`), outputting `RunResult` deltas (`ADD`, `EXIT`, `INCREASE`, `DECREASE`).
- **Bitemporal Point-In-Time Engine** (`etl/point_in_time.py`: `holdings_as_of`): Outputs historical portfolios without lookahead bias by isolating filing from knowledge time.
- **Rate-Governed EDGAR Ingest** (`adapters/edgar.py`: `list_new_filings`): Consumes SEC CIKs; uploads filings to MinIO and populates `holdings` under a 10 req/sec governor.
- **Identifier Resolution Cache** (`adapters/openfigi.py`: `OpenFigiClient.map_cusips`): Maps CUSIPs to Tickers, FIGIs, ISINs, and LEIs for market joins.
- **Signal-Alpha Strategy Backtesting** (`etl/backtest_flow.py`: `run_backtest`): Consumes rules and prices; logs returns in `backtest_results` to evaluate post-filing alpha.
- **Activism Campaign Engine** (`etl/activism_campaign_flow.py`: `materialize_activism_campaigns`): Consumes 13D/13G filings; outputs categorized `activism_events` grouped into campaigns.
- **Conviction & Crowding Detector** (`etl/conviction_flow.py`: `compute_conviction_scores`): Consumes active holdings; outputs conviction scores and crowded metrics.
- **Attributable RAG Router** (`chains/rag_search.py`, `chains/evidence.py`: `Evidence`): Consumes queries and filings; outputs answers with structured `Evidence` citations.

## 5. Data model, identifiers and contracts

- **Entities & Identifiers**: `managers` (`schema.sql:8`, integer `manager_id` PK) tracks `cik` (`utils/identifiers.py:normalize_cik`), `lei`, `aliases`, `registry_ids`. `holdings` (`schema.sql:185`, 9-char `cusip`) enriches via OpenFIGI (`identifier_resolution_cache`) to ticker, FIGI, LEI, ISIN. `filings` (`schema.sql:29`) tracks dates and MinIO `raw_key`. `documents` (`schema.sql:393`) stores text and `embedding vector(384)`.
- **Persistence Layer**: PostgreSQL 16 with `pgvector` and `pg_trgm`; SQLite 3 dialect abstraction for offline tests/WASM (`adapters/base.py:connect_db`); MinIO for raw blobs.
- **Versioning & Supersession**: `holdings` uses bitemporal `knowledge_time` and `superseded_at` for point-in-time queries (`etl/point_in_time.py`); `v_current_holdings` filters active rows. Amendments (`/A`) supersede base filings (`diff_holdings.py:_select_authoritative_filings`).
- **Contracts in `docs/contracts/`**:
  - `run-contract/v1` (`docs/contracts/run-contract-v1.md`): **Scaffolded**. Emits local `RunResult` (`tools/run_contract.py:85`); wire format un-emitted; skips in CI (`.github/workflows/backplane-conformance.yml:54`).
  - `evidence-object/v1` (`docs/contracts/schemas/evidence-object-v1.schema.json`): **Divergent**. Internal `Evidence` (`chains/evidence.py:11`) omits schema fields (`schema_version`, `fact_ref`, `evidence_id`).
  - `identity-map-conventions` (`docs/contracts/identity-map-conventions.md`): **Unconverted**. Uses integer `manager_id` instead of string `manager:<normalized_id>`.
  - `langsmith-fleet/v1` (`llm/langsmith_fleet.py`): **Emitted**. Emits conformant NDJSON telemetry for chat turns and feedback.

## 6. External inputs and dependencies

- **External Data Sources**: SEC EDGAR via `data.sec.gov` with rate pacing (`adapters/edgar.py:44`); UK Companies House REST API (`adapters/uk.py:24`); OpenFIGI API (`adapters/openfigi.py:18`); Stooq/yfinance scraped prices (`adapters/prices.py:30`); SEC RSS and GDELT 2.0 (`adapters/news.py:27`); Canada SEDAR+, Australia ASIC, Singapore MAS stubs; User files via `utils/extract.py`.
- **LLM and Frameworks**: LangChain ecosystem (`langchain`, `langchain-core`, `langchain-openai`, `langchain-anthropic`, `langsmith` in `pyproject.toml:29-33`). Embeddings use Sentence-Transformers `all-MiniLM-L6-v2` (384d) in `embeddings.py:25` (`USE_SIMPLE_EMBED=1` fallback).
- **Notable Libraries**: `stranske-pdf-extract` (`pyproject.toml:28`), `edgartools` (`>=5.44,<5.45`), `fastapi`, `uvicorn`, `streamlit`, `psycopg[binary]`, `boto3`, `prefect`.
- **Execution Modes**: Production runs via Docker Compose (PostgreSQL, MinIO, FastAPI, Streamlit, Prefect). Local dev uses `make app`. Browser demo (`scripts/build_wasm_demo.py`) compiles into static HTML/WASM (`web/index.html`) via stlite/Pyodide.

## 7. Current state

- **Test & CI Posture**: `ci.yml` runs Python CI (3.12/3.13, Ruff, Black, Mypy, 75% coverage gate). Suites: `postgres-integration`, `golden` (`pytest -m golden`), `schema-idempotence.yml`, `pr-00-gate.yml`, `database-snapshot.yml`.
- **Production-Usable vs Prototype**: Usable: EDGAR ingestion, holdings diffs, point-in-time queries, conviction scores, Streamlit UI, FastAPI routes, WASM demo. Prototype: foreign parsing, price scraping, run contract emission, entity deletion.
- **Consequential Known Gaps & Signals**:
  1. *Foreign adapter stubs*: Canada, ASIC, MAS return `unsupported` (`adapters/canada.py:44`, `adapters/asic.py:67`, `adapters/mas.py:53`).
  2. *Un-emitted contract*: Run contract skips in CI (`.github/workflows/backplane-conformance.yml:54`).
  3. *Evidence divergence*: `chains/evidence.py:Evidence` omits schema fields (`schema_version`, `fact_ref`, `evidence_id`).
  4. *Price scraping*: `adapters/prices.py:28` scrapes Stooq/yfinance for backtests.
  5. *Deletion cascade*: `api/managers.py:488` fails on foreign keys, orphaning blobs and vectors.
  6. *Missing regression corpus*: Lacks retained raw HTML filings (`docs/reports/design-doc-behavioral-claims-audit.md:32`, issue #1151).
  7. *Cost accounting*: `tools/run_contract.py:RunCost` defaults to `0.0` USD (`adapters/base.py:246-293`).
  8. *Identifier mismatch*: Integer `manager_id` vs string `manager:<normalized_id>` (`docs/contracts/identity-map-conventions.md:47`).

## 8. Claims vs reality

- **Parser Regression Suite**: *Claim*: Tests use retained HTML snapshots (`Manager-Intel-Platform.md:110`). *Reality*: No HTML corpus exists; tests use mocks (`docs/reports/design-doc-behavioral-claims-audit.md:32`, issue #1151; `tests/test_parser_snapshot_regression.py`).
- **Foreign Adapters**: *Documentation*: Early roadmap (Manager-Intel-Platform.md:201, 229) planned Canada and UK adapters, but the Revised Source Adapter Matrix (`Manager-Intel-Platform.md:119-123`) explicitly notes that Canada parsing returns `unsupported` until a parser exists, ASIC filing documents return `unsupported` (paywalled), and MAS returns `unsupported` (unconfigured endpoint). *Reality*: Confirms documentation; `adapters/canada.py:44`, `adapters/asic.py:67`, and `adapters/mas.py:53` return `{"status": "unsupported"}`.
- **Tika & XBRL**: *Claim*: Uses Tika and XBRL (`Manager-Intel-Platform.md:50, 59`). *Reality*: Neither exists in code; uses `stranske-pdf-extract` (`utils/extract.py:5`), `edgartools`, and XML parsing (`adapters/edgar.py:195`).
- **Commercial SEC API**: *Claim*: Ingests via `sec-api.io` (`Manager-Intel-Platform.md:44, 57`). *Reality*: Unused; queries `data.sec.gov` directly (`adapters/edgar.py:22`).
- **Universal Rate Limits**: *Claim*: Former guideline draft claimed all endpoints were rate limited (historical drift noted in `docs/reports/design-doc-behavioral-claims-audit.md:38`). *Reality*: Current code and docs (`docs/api_design_guidelines.md:11-14`, `docs/api_rate_limiting.md:43`, resolved by #1145) align: only chat write routes are throttled; read routes and health checks are unthrottled.
- **One-Click GDPR Takedown**: *Claim*: Provides one-click GDPR erasure (`Manager-Intel-Platform.md:104`). *Reality*: `DELETE /managers/{id}` (`api/managers.py:1580`, calling `_delete_manager` at `:488`) fails on foreign keys, orphaning blobs and vectors.
- **Backplane Conformance**: *Claim*: Run contract is often assumed to be actively wired. *Reality*: `docs/contracts/run-contract-v1.md:15-17` explicitly states "No participant emits an envelope yet (that is P1+); nothing here is wired into any repo's CI." The actual implementation gap is that `tools/run_contract.py:85` defines local `RunResult`, but `scripts/emit_reference_run.sh` does not exist, causing `.github/workflows/backplane-conformance.yml:54` to skip, while `chains/evidence.py:11` lacks schema-required fields.

## 9. Interoperability hooks (for the fleet program)

- **What this repo OFFERS**:
  - *Manager Directory*: Canonical records (`managers`) with CIK, LEI, and FCA FRN.
  - *Point-In-Time Holdings*: Portfolios (`holdings`, `etl/point_in_time.py:holdings_as_of`) isolating knowledge time.
  - *Quarterly Diffs*: Deltas (`daily_diffs`, `diff_holdings.py`) tracking position additions, exits, and adjustments.
  - *Activism Intelligence*: Schedules 13D/13G trajectories and campaign events (`activism_campaigns`, `activism_events`).
  - *Conviction & Crowding Analytics*: Conviction metrics and crowded positions (`conviction_scores`, `crowded_trades`).
  - *Observability Feed*: Standardized `langsmith-fleet/v1` telemetry.
- **What this repo CONSUMES**:
  - *Pricing & Benchmark Returns* (from `Trend_Model`): Replaces fragile scraping in `adapters/prices.py`.
  - *Mandate & Allocation Data* (from `Pension-Data`): Context to correlate with manager portfolios.
  - *Qualitative Diligence & DDQs* (from `Inv-Man-Intake`): Memos indexed into `documents` for RAG.
  - *Counterparty Exposure Data* (from `Counter_Risk`): Broker exposures mapping operational risk against concentration.
- **Naming and Identifier Collisions**:
  - *Entity IDs*: Siblings expect canonical strings (`manager:cik_...`); this repo uses integer `manager_id`.
  - *Security Identifiers*: Anchors on 9-digit `cusip`; downstream flows require CUSIP rather than FIGI/ISIN.
  - *Evidence Schema*: `chains/evidence.py` must adopt `docs/contracts/schemas/evidence-object-v1.schema.json`.

## 10. Reuse candidates

- `adapters/openfigi.py` (`OpenFigiClient`): CUSIP-to-FIGI/Ticker/LEI resolver with persistent caching.
- `diff_holdings.py`: Holdings reconciliation and diffing engine handling restatements.
- `etl/point_in_time.py` (`holdings_as_of`): Bitemporal portfolio query engine isolating knowledge time from filing event time.
- `etl/manager_similarity_flow.py`: Portfolio overlap engine computing Jaccard and cosine similarity.
- `utils/identifiers.py` (`normalize_cik`): Deterministic 10-digit SEC CIK normalizer.
- `scripts/build_wasm_demo.py` & `web/wasm_app.py`: Static builder bundling Streamlit pages and SQLite fixtures for browser execution.
- `adapters/edgar.py` (`_request_with_retry`): Paced HTTP client enforcing SEC EDGAR 10 req/sec rate limits.
- `alerts/engine.py` & `alerts/channels.py`: Rule evaluation engine and multi-channel notification dispatcher (Slack, Email, Webhook).

## 11. Proposed direction (evidence-based)

- **Finish What Is Scaffolded**:
  - *Backplane Run Contract*: Implement `scripts/emit_reference_run.sh` and emit `run-contract/v1` from `tools/run_contract.py`, activating `.github/workflows/backplane-conformance.yml`.
  - *Evidence Alignment*: Conform `chains/evidence.py:Evidence` to `docs/contracts/schemas/evidence-object-v1.schema.json` (`schema_version`, `fact_ref`, `evidence_id`).
  - *Foreign Adapters*: Build working scrapers for Canada, Australia, and Singapore or de-register them from `etl/ingest_flow.py`.
  - *Market Pricing*: Replace unsupported scraping in `adapters/prices.py` (Stooq/yfinance) with an internal feed.
  - *Cascade Deletion*: Refactor `_delete_manager` (`api/managers.py:488`) to cascade deletions and purge MinIO blobs and vector embeddings.
- **New Capabilities**:
  - *Dual Entity Routing*: Support canonical string identifiers (`manager:cik_0001067983`) across REST routes alongside integer `manager_id`.
  - *Point-in-Time REST Endpoints*: Expose `etl/point_in_time.py:holdings_as_of` via FastAPI (`/api/managers/{id}/holdings?as_of=YYYY-MM-DD`).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- **Core Purpose**: Tracks external asset managers, quarterly portfolio adjustments, and activist campaigns for institutional allocators.
- **Data Pipeline**: Ingests and cleans regulatory portfolio disclosures, activist filings, corporate news, and internal research notes.
- **Key Analytical Insights**: Highlights new positions, liquidations, conviction scores, crowded positions, and post-disclosure returns.
- **User Experience**: Analysts use a web dashboard, receive email digests, search research notes, or consult an AI assistant citing source documents.
- **Deployment & Data Security**: Runs disconnected in a browser using sample data, while production keeps proprietary data behind private firewalls.
*Evidence-checked against source repositories; verification metadata omitted from work bundle.*
