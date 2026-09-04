# Manager-Database dossier — verification table

Verified against clone `clones/Manager-Database` at HEAD `68baf3f5f1678427cb36f0e1b2c9a97f38175b67` (2026-09-04 17:30 UTC).
Method: every cited file:line/symbol opened and verified against current code and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 40 |
| WRONG (corrected in dossier) | 6 |
| UNVERIFIABLE | 4 |
| **Total checked** | **50** |

### Key Findings & Corrections

1. **§4 Activism Campaign Engine function name:** The dossier cited `etl/activism_campaign_flow.py` as having a function `rebuild_activism_campaigns`. Inspection of `etl/activism_campaign_flow.py:333` shows that the function is named `materialize_activism_campaigns`. The symbol `rebuild_activism_campaigns` does not exist in the codebase (it appeared only in pre-commit generated drafts under `dossier-out/`). Corrected in dossier §4.
2. **§8 Foreign Adapters refutation (adversarial check):** The dossier asserted that `Manager-Intel-Platform.md:119-123` claimed working adapters for Canada, Australia, and Singapore, and refuted it because stubs return `unsupported`. Opening `Manager-Intel-Platform.md:119-123` reveals that this section is the "Revised Source Adapter Matrix", which explicitly documented that Canada parsing returns a structured `unsupported` status until a parser exists, ASIC filing documents return `unsupported` because documents are paywalled, and MAS filing documents return `unsupported` until an endpoint is configured. Refuting lines 119-123 as claiming working adapters was a false refutation against a strawman. Corrected in dossier §8.
3. **§8 Universal Rate Limits claim attribution:** The dossier cited `docs/api_design_guidelines.md:11` as claiming all endpoints enforce rate limits. Opening `docs/api_design_guidelines.md:11-14` at HEAD reveals the exact opposite: "Rate limiting applies to the chat write paths documented in API Rate Limiting. Other endpoints are currently unlimited unless they explicitly delegate to the chat rate limiter in api/chat.py." The in-repo audit (`docs/reports/design-doc-behavioral-claims-audit.md:38`) confirms this was historical documentation drift resolved in PR #1145. Citing line 11 as an active claim was false attribution. Corrected in dossier §8.
4. **§8 Backplane Conformance claim attribution:** The dossier cited `docs/contracts/run-contract-v1.md` as claiming conformance. Opening `docs/contracts/run-contract-v1.md:15-17` reveals that the specification explicitly warns: *"No participant emits an envelope yet (that is P1+); nothing here is wired into any repo's CI."* The actual implementation defect is that `tools/run_contract.py:85` defines `RunResult` but `scripts/emit_reference_run.sh` does not exist, causing `.github/workflows/backplane-conformance.yml:54` to skip, while `chains/evidence.py:11` omits required schema fields (`schema_version`, `evidence_id`, `fact_ref`). Corrected in dossier §8.
5. **§2 CLI Tools backup test citation:** The dossier cited `tests/test_diff_holdings.py` as verifying S3 backups. Opening `tests/test_diff_holdings.py` shows it tests only `diff_holdings.py`. S3 backup plans, credential masking, and KMS encryption are tested in `tests/test_db_snapshot_restore.py:11-38`. Corrected in dossier §2.
6. **§7 Cost accounting citation:** The dossier cited `adapters/base.py:175` for `tools/run_contract.py:RunCost` defaulting to `0.0` USD. Line 175 of `adapters/base.py` is `return manager_id_column(conn) or "id"`. The actual cost tracking logic in `adapters/base.py` is in `tracked_call` at lines 246-293 (where `computed_cost` defaults to `0.0`), alongside `tools/run_contract.py:78-83` (`RunCost(usd=0.0, tokens=0)`). Corrected in dossier §7.
7. **§9 Fleet program inter-repo consumption:** Claims regarding consumption of data from external repos (`Trend_Model`, `Pension-Data`, `Inv-Man-Intake`, `Counter_Risk`) are architectural touchpoints that are UNVERIFIABLE from within the isolated clone.

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | Holdings Diff Engine: Reconciles 13F filings against amendments (`/A`), outputting `RunResult` deltas (`ADD`, `EXIT`, `INCREASE`, `DECREASE`) | `diff_holdings.py:157`, `diff_holdings.py:28-82` | CONFIRMED | `diff_holdings` (:157) calls `_select_authoritative_filings` (:28-82) prioritizing `/A` amendments, emitting `RunResult` with delta types `ADD`, `EXIT`, `INCREASE`, `DECREASE` (:202, 216, 238). |
| 2 | Bitemporal Point-In-Time Engine: Outputs historical portfolios without lookahead bias by isolating filing from knowledge time | `etl/point_in_time.py:67-120` | CONFIRMED | `holdings_as_of` filters `knowledge_time <= as_of` and `superseded_at > as_of`, matching `filed_date <= as_of`. |
| 3 | Rate-Governed EDGAR Ingest: Consumes SEC CIKs; uploads filings to MinIO and populates `holdings` under a 10 req/sec governor | `adapters/edgar.py:44, 343`, `etl/edgar_flow.py:372-422` | CONFIRMED | `EDGAR_MIN_REQUEST_INTERVAL: 0.11` (:44) enforces ≤9.09 req/sec; `etl/edgar_flow.py:392, 413` uploads to S3/MinIO and populates `holdings`. |
| 4 | Identifier Resolution Cache: Maps CUSIPs to Tickers, FIGIs, ISINs, and LEIs for market joins | `adapters/openfigi.py:67-78` | CONFIRMED | `OpenFigiClient.map_cusips` batches CUSIPs to OpenFIGI API, resolving ticker, figi, isin, lei. |
| 5 | Signal-Alpha Strategy Backtesting: Consumes rules and prices; logs returns in `backtest_results` to evaluate post-filing alpha | `etl/backtest_flow.py:349-380` | CONFIRMED | `run_backtest` replays strategy against `holdings_as_of`, evaluates returns, and records in `backtest_runs` and `backtest_results`. |
| 6 | Activism Campaign Engine: Consumes 13D/13G filings; outputs categorized `activism_events` grouped into campaigns | `etl/activism_campaign_flow.py:333` | **WRONG** | Function is named `materialize_activism_campaigns` (:333), not `rebuild_activism_campaigns`. Rebuild symbol does not exist in code. |
| 7 | Conviction & Crowding Detector: Consumes active holdings; outputs conviction scores and crowded metrics | `etl/conviction_flow.py:99, 481` | CONFIRMED | `compute_conviction_scores` (:99) and `detect_crowded_trades` (:481) output to `conviction_scores` and `crowded_trades`. |
| 8 | Attributable RAG Router: Consumes queries and filings; outputs answers with structured `Evidence` citations | `chains/rag_search.py:40`, `chains/evidence.py:11` | CONFIRMED | `RAGSearchResult` in `rag_search.py` attaches structured `Evidence` instances defined in `chains/evidence.py:11-29`. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 9 | `managers` tracks `cik`, `lei`, `aliases`, `registry_ids` with integer `manager_id` PK | `schema.sql:8-20`, `utils/identifiers.py:8-23` | CONFIRMED | `schema.sql:9` defines `manager_id bigserial PRIMARY KEY`; `utils/identifiers.py:normalize_cik` normalizes to 10 digits. |
| 10 | `holdings` (9-char CUSIP) enriches via OpenFIGI (`identifier_resolution_cache`) to ticker, FIGI, LEI, ISIN | `schema.sql:184-202`, `schema.sql:351` | CONFIRMED | `holdings` columns include `resolved_ticker`, `resolved_figi`, `resolved_lei`, and `identifier_resolution_cache` table matches. |
| 11 | `filings` tracks dates and MinIO `raw_key` | `schema.sql:29-41` | CONFIRMED | `filings` carries `period_end`, `filed_date`, `raw_key` with unique index on `raw_key`. |
| 12 | `documents` stores text and `embedding vector(384)` | `schema.sql:393-402` | CONFIRMED | `documents` defines `embedding vector(384)` and SHA-256 unique index. |
| 13 | Persistence: Postgres 16 with `pgvector`/`pg_trgm`; SQLite 3 dialect abstraction for offline tests/WASM | `adapters/base.py:47-60`, `schema.sql:5-6` | CONFIRMED | `connect_db` dynamically handles PostgreSQL or SQLite connection depending on `DB_URL` / `DB_PATH`. |
| 14 | Versioning: Bitemporal `knowledge_time` and `superseded_at`; `v_current_holdings` view; `/A` supersedes base filings | `etl/point_in_time.py:72-78`, `schema.sql:217`, `diff_holdings.py:28-82` | CONFIRMED | `v_current_holdings` filters `superseded_at IS NULL`; `_select_authoritative_filings` selects `/A` amendments. |
| 15 | `run-contract/v1`: Scaffolded local `RunResult`; wire format un-emitted; skips in CI | `tools/run_contract.py:85`, `.github/workflows/backplane-conformance.yml:51-55` | CONFIRMED | `RunResult` class exists; `scripts/emit_reference_run.sh` does not exist; CI outputs skip notice. |
| 16 | `evidence-object/v1`: Divergent; internal `Evidence` omits `schema_version`, `fact_ref`, `evidence_id` | `docs/contracts/schemas/evidence-object-v1.schema.json:8-15`, `chains/evidence.py:11-29` | CONFIRMED | Schema requires all 3 fields; `chains/evidence.py:Evidence` does not define them. |
| 17 | `identity-map-conventions`: Unconverted; uses integer `manager_id` instead of `manager:<normalized_id>` | `docs/contracts/identity-map-conventions.md:44-60`, `schema.sql:9` | CONFIRMED | Canonical format requires lowercase entity-prefixed string; repository uses bigserial/integer PK. |
| 18 | `langsmith-fleet/v1`: Emits conformant NDJSON telemetry for chat turns and feedback | `llm/langsmith_fleet.py:27, 98-150` | CONFIRMED | `SCHEMA_VERSION = "langsmith-fleet/v1"`; records chat-turn and chat-feedback NDJSON events. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement |
|---|---|---|---|---|
| 19 | **Parser Regression Suite**: Tests use retained HTML snapshots | `Manager-Intel-Platform.md:110`, `docs/reports/design-doc-behavioral-claims-audit.md:32`, issue #1151 | CONFIRMED | Design doc claimed prior HTML snapshots for regression; audit confirms unimplemented (#1151); `tests/test_parser_snapshot_regression.py` uses a synthetic XML mock (`edgar_13f_prior_snapshot.xml`). |
| 20 | **Foreign Adapters**: Working adapters for Canada, Australia, Singapore | `Manager-Intel-Platform.md:119-123`, `adapters/canada.py:44`, `adapters/asic.py:67`, `adapters/mas.py:53` | **WRONG (false refutation)** | `Manager-Intel-Platform.md:119-123` (the Revised Source Adapter Matrix) explicitly documented that Canada parsing returns `unsupported` until a parser exists, ASIC returns `unsupported` (paywalled documents), and MAS returns `unsupported` (unconfigured endpoint). Refuting lines 119-123 as claiming working adapters was a false refutation against a strawman. |
| 21 | **Tika & XBRL**: Uses Tika and XBRL | `Manager-Intel-Platform.md:50, 59`, `utils/extract.py:5`, `adapters/edgar.py:195` | CONFIRMED | Early design spec suggested Apache Tika and XBRL libraries; neither is in code or dependencies; extraction uses `stranske-pdf-extract` and `edgartools`. |
| 22 | **Commercial SEC API**: Ingests via `sec-api.io` | `Manager-Intel-Platform.md:44, 57`, `adapters/edgar.py:22` | CONFIRMED | Early design spec recommended `sec-api.io`; actual implementation queries public `data.sec.gov` directly with rate limiting. |
| 23 | **Universal Rate Limits**: All endpoints enforce rate limits | `docs/api_design_guidelines.md:11`, `docs/api_rate_limiting.md:43` | **WRONG (claim attribution)** | In current code at HEAD, `docs/api_design_guidelines.md:11-14` explicitly states that rate limiting applies only to chat write paths and other endpoints are unthrottled. Citing it as claiming universal rate limits reflects historical pre-PR #1145 documentation drift (cataloged in `docs/reports/design-doc-behavioral-claims-audit.md:38`). |
| 24 | **One-Click GDPR Takedown**: Provides one-click GDPR erasure | `Manager-Intel-Platform.md:104`, `api/managers.py:488, 1580` | CONFIRMED | `Manager-Intel-Platform.md:104` called for a one-click takedown; `DELETE /managers/{id}` executes `_delete_manager` (`DELETE FROM managers`), failing on foreign keys and leaving MinIO blobs/embeddings orphaned. |
| 25 | **Backplane Conformance**: `run-contract/v1` and `evidence-object/v1` are conformant | `docs/contracts/run-contract-v1.md:15-17`, `.github/workflows/backplane-conformance.yml:54`, `chains/evidence.py:11` | **WRONG (claim attribution)** | `docs/contracts/run-contract-v1.md:15-17` explicitly notes that no participant emits an envelope yet and nothing is wired into CI. The actual defect is that `tools/run_contract.py:85` defines `RunResult` but `scripts/emit_reference_run.sh` is missing, causing CI to skip, while `chains/evidence.py` omits required schema fields. |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 26 | Offers Manager Directory: Canonical records (`managers`) with CIK, LEI, and FCA FRN | `schema.sql:8-20`, `api/managers.py:71` | CONFIRMED | `managers` table tracks `cik`, `lei`, `registry_ids` (including `fca_frn`). |
| 27 | Offers Point-In-Time Holdings: Portfolios (`holdings`, `etl/point_in_time.py:holdings_as_of`) isolating knowledge time | `etl/point_in_time.py:67-120` | CONFIRMED | Point-in-time holdings query isolates knowledge time from filing event time. |
| 28 | Offers Quarterly Diffs: Deltas (`daily_diffs`, `diff_holdings.py`) tracking position additions, exits, adjustments | `diff_holdings.py:157-254`, `schema.sql:408` | CONFIRMED | Daily diffs and holdings diff engine produce structured position delta records. |
| 29 | Offers Activism Intelligence: Schedules 13D/13G trajectories and campaign events | `schema.sql:53-108`, `etl/activism_campaign_flow.py` | CONFIRMED | Tables `activism_filings`, `activism_campaigns`, and `activism_events` store campaign data. |
| 30 | Offers Conviction & Crowding Analytics: Conviction scores and crowded positions | `schema.sql:429, 444`, `etl/conviction_flow.py:99, 481` | CONFIRMED | Materializes `conviction_scores` and `crowded_trades`. |
| 31 | Offers Observability Feed: Standardized `langsmith-fleet/v1` telemetry | `llm/langsmith_fleet.py:27` | CONFIRMED | Telemetry writer emits compliant NDJSON events for chat and feedback. |
| 32 | Consumes Pricing & Benchmark Returns (from `Trend_Model`) | `adapters/prices.py` | **UNVERIFIABLE (off-clone)** | Inter-repo fleet integration hook; cannot be verified from Manager-Database alone. |
| 33 | Consumes Mandate & Allocation Data (from `Pension-Data`) | `docs/contracts/` | **UNVERIFIABLE (off-clone)** | Inter-repo fleet integration hook; cannot be verified from Manager-Database alone. |
| 34 | Consumes Qualitative Diligence & DDQs (from `Inv-Man-Intake`) | `documents`, `utils/extract.py` | **UNVERIFIABLE (off-clone)** | Inter-repo fleet integration hook; cannot be verified from Manager-Database alone. |
| 35 | Consumes Counterparty Exposure Data (from `Counter_Risk`) | `docs/contracts/` | **UNVERIFIABLE (off-clone)** | Inter-repo fleet integration hook; cannot be verified from Manager-Database alone. |
| 36 | Collision: Siblings expect canonical strings (`manager:cik_...`); this repo uses integer `manager_id` | `docs/contracts/identity-map-conventions.md:44-60`, `schema.sql:9` | CONFIRMED | Schema uses bigint PK; convention dictates `manager:<normalized_id>`. |
| 37 | Collision: Anchors on 9-digit `cusip`; downstream flows require CUSIP rather than FIGI/ISIN | `diff_holdings.py:173`, `schema.sql:187` | CONFIRMED | Internal diffs and views key primarily on 9-character CUSIP. |
| 38 | Collision: `chains/evidence.py` must adopt `docs/contracts/schemas/evidence-object-v1.schema.json` | `chains/evidence.py:11`, `docs/contracts/schemas/evidence-object-v1.schema.json` | CONFIRMED | Current dataclass diverges from schema by omitting required envelope keys. |

---

## §1, §2, §6, §7, §10, §11 — Supporting Claims

| # | Section | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|---|
| 39 | §1 | Purpose: Investment surveillance platform ingesting EDGAR, Companies House, computing deltas and conviction | `README.md:1-10`, `schema.sql:8-60` | CONFIRMED | Matches purpose, schema, and operational capabilities of the repo. |
| 40 | §2 | Web UI: Streamlit app (`ui/app.py:12`), console script `mgrdb-app` | `pyproject.toml:38`, `ui/launch.py:27-41`, `tests/test_ui_navigation.py` | CONFIRMED | `mgrdb-app = "ui.launch:main"` launches Streamlit app; tests pass. |
| 41 | §2 | Browser Demo: Offline stlite/Pyodide app (`web/index.html`, `web/wasm_app.py:42`) | `scripts/build_wasm_demo.py`, `tests/test_wasm_demo_build.py` | CONFIRMED | Static builder bundles synthetic SQLite and UI pages into WASM container. |
| 42 | §2 | REST API: FastAPI application entry point in `api/chat.py:47` | `api/chat.py:47-53`, `tests/test_chat_api.py` | CONFIRMED | Mounts managers, data, alerts, activism, and signals routers. |
| 43 | §2 | Scheduled ETL: EDGAR flows work; foreign stubs return `unsupported` | `etl/edgar_flow.py`, `adapters/canada.py:44`, `adapters/asic.py:67`, `adapters/mas.py:53` | CONFIRMED | EDGAR flow functions; Canada, ASIC, and MAS parse methods return explicit `unsupported` status. |
| 44 | §2 | CLI Tools: `diff_holdings.py:157` computes deltas; S3 backups tested in `tests/test_db_snapshot_restore.py` | `diff_holdings.py:157`, `scripts/db_snapshot_restore.py` | **WRONG (citation)** | Dossier cited `tests/test_diff_holdings.py` for S3 backups; S3 backups are tested in `tests/test_db_snapshot_restore.py`. |
| 45 | §2 | Observability: Emits `langsmith-fleet/v1`; wire contract un-emitted | `llm/langsmith_fleet.py:27`, `.github/workflows/backplane-conformance.yml:54` | CONFIRMED | Confirmed lines and values in code and workflow files. |
| 46 | §6 | External Data Sources: EDGAR, Companies House, OpenFIGI, Stooq/yfinance, RSS/GDELT | `adapters/edgar.py:44`, `adapters/uk.py:24`, `adapters/openfigi.py:18`, `adapters/prices.py:30`, `adapters/news.py:27` | CONFIRMED | All cited adapters, constants, and endpoints match code. |
| 47 | §6 | LLM & Dependencies: LangChain ecosystem, Sentence-Transformers `all-MiniLM-L6-v2` | `pyproject.toml:29-33`, `embeddings.py:25` | CONFIRMED | Matches dependencies in `pyproject.toml` and model loading in `embeddings.py`. |
| 48 | §7 | CI Posture: `ci.yml` runs Python CI (3.12/3.13, Ruff, Black, Mypy, 75% coverage); Postgres integration and snapshot workflows | `.github/workflows/ci.yml:24-33`, `.github/workflows/database-snapshot.yml` | CONFIRMED | CI configuration and workflows verified. |
| 49 | §7 | Cost accounting: `tools/run_contract.py:RunCost` defaults to `0.0` USD | `tools/run_contract.py:78-83`, `adapters/base.py:246-293` | **WRONG (citation)** | Dossier cited `adapters/base.py:175` (which is `return manager_id_column(conn) or "id"`); actual cost tracking is `adapters/base.py:246-293`. |
| 50 | §10, §11 | All 8 reuse candidates exist and match roles; proposed directions align with code realities | `adapters/openfigi.py`, `diff_holdings.py`, `etl/point_in_time.py`, `etl/manager_similarity_flow.py`, etc. | CONFIRMED | Components exist, signatures match, and proposed directions address real verified gaps. |

