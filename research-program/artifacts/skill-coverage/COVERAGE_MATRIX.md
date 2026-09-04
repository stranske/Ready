# Fleet AI/Engineering Skill Coverage Matrix

Generated from grep across `pyproject.toml`, `requirements*`, `src/`, `scripts/`, `.github/` in 17 sibling repos (shallow clones).  
Excluded generated `dossier-out/` and vendored `vendor/` / `archives/` trees.

**Legend:** `NONE` = no evidence · `IMPORTED` = dependency or thin wrapper only · `USED` = real but non-core · `CENTRAL` = load-bearing product or platform surface

**Repos (columns):** CA=Collab-Admin · CR=Counter_Risk · DL=Doc-Lineage · FAA=Fine-Art-Archive · IMI=Inv-Man-Intake · MD=Manager-Database · Orch=Orchestrator · PD=Pension-Data · PAEM=Portable-Alpha-Extension-Model · Ready · Template · TPP=Travel-Plan-Permission · TMP=Trend_Model_Project · WF=Workflows · WIT=Workflows-Integration-Tests · LMS=learning-management-system · TP=trip-planner

---

## 1. Coverage matrix

| Category | CA | CR | DL | FAA | IMI | MD | Orch | PD | PAEM | Ready | Template | TPP | TMP | WF | WIT | LMS | TP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LangChain | USED | USED | IMPORTED | IMPORTED | USED | **CENTRAL** | USED | USED | **CENTRAL** | IMPORTED | IMPORTED | IMPORTED | **CENTRAL** | **CENTRAL** | USED | IMPORTED | IMPORTED |
| LangGraph | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | **CENTRAL** | NONE | USED | NONE | NONE | NONE |
| LangSmith tracing | IMPORTED | USED | IMPORTED | IMPORTED | **CENTRAL** | **CENTRAL** | USED | IMPORTED | **CENTRAL** | IMPORTED | IMPORTED | IMPORTED | **CENTRAL** | **CENTRAL** | USED | IMPORTED | IMPORTED |
| LangSmith / other evals | NONE | NONE | NONE | NONE | USED | NONE | NONE | **CENTRAL** | USED | NONE | NONE | NONE | USED | USED | NONE | USED | USED |
| MCP servers or clients | NONE | NONE | NONE | NONE | NONE | NONE | **CENTRAL** | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE |
| Structured extraction (schemas) | IMPORTED | USED | IMPORTED | USED | **CENTRAL** | USED | NONE | USED | **CENTRAL** | IMPORTED | IMPORTED | USED | **CENTRAL** | USED | IMPORTED | **CENTRAL** | USED |
| Embeddings / vector search | IMPORTED | NONE | IMPORTED | IMPORTED | IMPORTED | **CENTRAL** | NONE | NONE | NONE | IMPORTED | IMPORTED | NONE | NONE | USED | NONE | NONE | NONE |
| Knowledge graphs (networkx/kuzu/neo4j) | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE |
| OpenTelemetry / observability | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE |
| Workflow orchestration (Prefect/Dagster/Airflow) | NONE | NONE | NONE | NONE | NONE | **CENTRAL** | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE |
| Browser automation | NONE | NONE | NONE | NONE | USED | USED | NONE | NONE | USED | NONE | NONE | NONE | USED | NONE | NONE | USED | USED |
| Document parsing | NONE | **CENTRAL** | NONE | NONE | **CENTRAL** | NONE | NONE | USED | USED | NONE | NONE | USED | USED | **CENTRAL** | NONE | NONE | NONE |
| Diff / blackline / lineage | NONE | USED | NONE | NONE | **CENTRAL** | NONE | USED | **CENTRAL** | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE |
| Static / offline apps | USED | USED | NONE | NONE | **CENTRAL** | USED | NONE | NONE | **CENTRAL** | NONE | NONE | NONE | **CENTRAL** | NONE | NONE | USED | USED |
| Packaging / portable builds | NONE | **CENTRAL** | NONE | NONE | NONE | USED | NONE | NONE | **CENTRAL** | NONE | NONE | USED | USED | NONE | NONE | NONE | USED |
| CI / test infrastructure | USED | USED | USED | USED | USED | USED | USED | USED | USED | USED | USED | USED | USED | **CENTRAL** | **CENTRAL** | USED | USED |
| Agent frameworks / multi-agent | USED | USED | USED | USED | USED | USED | **CENTRAL** | USED | USED | USED | USED | USED | USED | **CENTRAL** | USED | USED | USED |
| Data pipelines / ETL | NONE | **CENTRAL** | NONE | NONE | USED | **CENTRAL** | NONE | **CENTRAL** | NONE | NONE | NONE | USED | USED | NONE | NONE | **CENTRAL** | **CENTRAL** |
| Entity resolution / alias registries | NONE | **CENTRAL** | NONE | **CENTRAL** | USED | USED | NONE | **CENTRAL** | NONE | NONE | NONE | NONE | NONE | USED | NONE | NONE | USED |

---

## 2. Per-category notes (USED / CENTRAL evidence)

### LangChain
- **MD CENTRAL:** `chains/rag_search.py`, `chains/holdings_analysis.py`, `chains/filing_summary.py`
- **TMP CENTRAL:** `src/trend_analysis/llm/chain.py`, `tools/langchain_client.py`
- **PAEM CENTRAL:** `pa_core/llm/config_patch_chain.py`, `pa_core/llm/provider.py`
- **WF CENTRAL:** `scripts/langchain/integration_layer.py`, `tools/langchain_client.py` (fleet sync source)
- **CR USED:** `src/counter_risk/chat/providers/langchain_runtime.py`
- **IMI/PD/Orch USED:** `tools/langchain_client.py`, `scripts/langchain/eval_runner.py` (PD)
- **Fleet-wide USED/IMPORTED:** `scripts/langchain/*` agent CI scripts (issue formatter, dedup, verifier) synced from WF consumer template; classify IMPORTED when only `tools/langchain_client.py` + agent scripts, no product chains

### LangGraph
- **TPP CENTRAL:** `src/travel_plan_permission/orchestration/graph.py` (declared in `pyproject.toml`)
- **WF USED:** `scripts/repo_review_evaluator.py` (LangGraph referenced in repo-review scoring)

### LangSmith tracing
- **WF CENTRAL:** `scripts/langsmith_fleet.py`, `scripts/langsmith_observability_health.py`, `scripts/langsmith_fleet_conformance.py`
- **MD CENTRAL:** `llm/langsmith_fleet.py`, `llm/tracing.py`
- **IMI CENTRAL:** `src/inv_man_intake/observability/langsmith_fleet.py`, `langsmith_sink.py`
- **TMP CENTRAL:** `src/trend_analysis/llm/tracing.py`
- **PAEM CENTRAL:** `pa_core/llm/langsmith_fleet.py`, `pa_core/llm/tracing.py`
- **CR USED:** `src/counter_risk/observability/langsmith_fleet.py`
- **Orch USED:** `src/langsmith_fetch.py`
- **IMPORTED (many repos):** `scripts/langchain/trace_utils.py` via Workflows consumer sync

### LangSmith / other evals
- **PD CENTRAL:** `scripts/langchain/eval_runner.py`, `src/pension_data/langchain/eval_harness.py`, `tests/langchain/test_eval_harness.py`, `.github/workflows/one-pdf-pilot-golden.yml`
- **TMP USED:** `tools/prompt_evaluator.py`, `tools/eval_config_patch.py`
- **WF USED:** `packages/stranske_pdf_extract/tests/test_eval.py`
- **TP USED:** `tests/baseline/test_golden.py`
- **PAEM USED:** `tests/golden/test_tutorial_golden.py`, `tests/golden/test_scenario_smoke.py`
- **IMI USED:** `src/inv_man_intake/extraction/regression.py`, `tests/extraction/test_extraction_regression.py`
- **LMS USED:** `src/lms/llm/eval_sets.py`

### MCP servers or clients
- **Orch CENTRAL:** `src/mcp_server.py` — stdio JSON-RPC MCP server exposing read-only fleet tools + bounded owner-question actions

### Structured extraction (schemas)
- **IMI CENTRAL:** `src/inv_man_intake/extraction/service.py`, provider modules under `extraction/providers/`
- **TMP CENTRAL:** `src/trend_analysis/config/models.py`, `src/trend_analysis/llm/chain.py` (Pydantic + structured LLM patches)
- **PAEM CENTRAL:** `pa_core/wizard_schema.py`, `pa_core/schema.py`
- **LMS CENTRAL:** `src/lms/llm/client.py` (structured-output validation), domain `*/schemas.py` modules
- **MD USED:** `chains/filing_summary.py`, `tools/run_contract.py`
- **PD USED:** `src/pension_data/entities/matching.py`
- **FAA/TPP/TP USED:** `src/fine_art_archive/parsers/semantic.py`, `src/travel_plan_permission/policy_contract_models.py`, `trip_planner/candidates/models.py`

### Embeddings / vector search
- **MD CENTRAL:** `embeddings.py`, `chains/rag_search.py`, `schema.sql` (`embedding vector(384)`), `api/search.py`
- **WF USED:** `tools/embedding_provider.py`, `scripts/langchain/semantic_matcher.py` (issue dedup / label matching)
- **IMPORTED (fleet):** `tools/embedding_provider.py` present in most consumer repos for agent workflows only

### Knowledge graphs
- No `networkx`, `kuzu`, or `neo4j` usage found. (LMS `lms/graphs/` is a competency-graph domain model on SQLAlchemy, not a graph DB library.)

### OpenTelemetry / observability
- No `opentelemetry` imports or dependencies found fleet-wide. Observability is LangSmith-centric + custom metrics scripts (`scripts/autopilot_metrics_collector.py`, `tools/coverage_guard.py`).

### Workflow orchestration
- **MD CENTRAL:** Prefect flows in `etl/ingest_flow.py`, `etl/edgar_flow.py`, `etl/daily_diff_flow.py`, and sibling `etl/*_flow.py`

### Browser automation
- **TMP USED:** `.github/workflows/pr-12-playwright.yml`, `tools/playwright/`
- **LMS USED:** `tests/ui/test_playwright_smoke.py`, `tests/ui/test_m6_screenshots.py`
- **PAEM USED:** `scripts/capture_wizard.py`
- **MD USED:** `scripts/capture_ui_screenshots.py`
- **IMI USED:** `tests/app/test_static_spa_browser_e2e.py`, `scripts/verify_static_spa_pyodide.py`
- **TP USED:** `frontend/package.json` (Playwright devDependency)

### Document parsing
- **IMI CENTRAL:** `src/inv_man_intake/extraction/providers/docling_primary.py`, `pptx_primary.py`; `eval/benchmarks/docling_field_accuracy.py`
- **CR CENTRAL:** `src/counter_risk/parsers/daily_holdings_pdf.py`, `parsers/cprs_*.py`
- **WF CENTRAL:** `packages/stranske_pdf_extract/` (dedicated PDF extraction package with eval harness)
- **PD/TPP/PAEM/TMP USED:** `src/pension_data/ops/document_orchestration.py`, `src/travel_plan_permission/workbook_ooxml.py`, `pa_core/reporting/excel.py`, `src/trend_analysis/export/`

### Diff / blackline / lineage
- **PD CENTRAL:** `src/pension_data/entities/lineage.py`, `src/pension_data/db/models/entity_lineage.py`
- **IMI CENTRAL:** `src/inv_man_intake/audit/lineage.py`, `src/inv_man_intake/packet.py`
- **CR USED:** `src/counter_risk/reports/change_attribution.py`, `src/counter_risk/reports/mapping_diff.py`
- **Orch USED:** `src/synthesis_promotion.py`, `tests/rail_exercises/completion-event-lineage/`
- **Note:** `Doc-Lineage` repo is currently a Workflows consumer scaffold (`src/my_project/`); no product lineage logic despite the name.

### Static / offline apps
- **TMP CENTRAL:** `streamlit_app/app.py`, `scripts/build_wasm_demo.py`, `scripts/fetch_offline_runtime.py`
- **PAEM CENTRAL:** `dashboard/app.py`, `web/index.html` (bundled stlite/Pyodide), `scripts/fetch_offline_web_runtime.py`
- **IMI CENTRAL:** `app/pyodide_packet_bridge.py`, `scripts/fetch_offline_runtime.py`
- **CA USED:** `streamlit_app/app.py`, `streamlit_app/review_console.py`
- **MD USED:** `ui/launch.py`, `scripts/build_wasm_demo.py`
- **CR USED:** `tests/test_web_demo_smoke.py`
- **LMS USED:** `src/lms/ui/static/` (offline-capable PWA shell), `lms/ui/shell.py`
- **TP USED:** `frontend/` SPA + packaging tests

### Packaging / portable builds
- **CR CENTRAL:** `src/counter_risk/build/release.py`, `tests/test_pyinstaller_guard.py`, `.github/workflows/release.yml`
- **PAEM CENTRAL:** `scripts/make_portable_zip.py`, `.github/workflows/release-packaging.yml`
- **TMP/MD USED:** `docker-compose.yml`, wheel/export bundles (`src/trend_analysis/export/bundle.py`)
- **TPP/TP USED:** `scripts/verify_install.py`, `tools/build_backend/`, `tests/test_packaging.py`

### CI / test infrastructure
- **WF CENTRAL:** `scripts/check_deliberate_break.py`, `tools/coverage_guard.py`, `tools/coverage_trend.py`, reusable CI workflows
- **WIT CENTRAL:** cross-repo integration test harness; `tests/test_langsmith_trace_smoke.py`, `config/coverage-baseline.json`
- **Fleet-wide USED:** `scripts/check_deliberate_break.py`, `tests/baseline/`, golden tests, `--cov` gates in `.github/workflows/pr-00-gate.yml`

### Agent frameworks / multi-agent
- **Orch CENTRAL:** `src/dispatcher.py`, `src/tick.py`, `src/capabilities.py`, `src/router.py`, rail-exercise harnesses
- **WF CENTRAL:** `.github/workflows/agents-auto-pilot.yml`, `scripts/orchestrator_skill.py`, codex-belt workflows (`agents-71/72/73-*`)
- **Fleet-wide USED:** `.github/workflows/agents-auto-pilot.yml`, `agents-dedup.yml`, `agents-issue-intake.yml` synced to consumer repos

### Data pipelines / ETL
- **MD CENTRAL:** `etl/` (Prefect flows), `alembic/versions/`
- **CR CENTRAL:** `src/counter_risk/pipeline/run.py`, reconciliation + manifest provenance
- **PD CENTRAL:** `src/pension_data/ingest/`, `src/pension_data/db/models/`
- **TP CENTRAL:** `trip_planner/persistence/alembic/`, `trip_planner/persistence/db.py`
- **LMS CENTRAL:** `src/lms/db/base.py`, SQLAlchemy models across domain packages
- **IMI/TMP/TPP USED:** `src/inv_man_intake/data/migrations/`, `src/trend_analysis/io/market_data.py`, pandas-heavy TPP services

### Entity resolution / alias registries
- **CR CENTRAL:** `src/counter_risk/name_registry.py`, `config/name_registry.yml`
- **PD CENTRAL:** `src/pension_data/entities/matching.py`, `src/pension_data/entities/lookup_service.py`
- **FAA CENTRAL:** `src/fine_art_archive/identity/artist_lookup.py`, `enrichment/work_qid_search.py`
- **IMI USED:** `tests/intake/test_identity_resolution.py`
- **TP USED:** `trip_planner/sources/resolution.py`, `trip_planner/sources/dedup.py`
- **MD USED:** `utils/identifiers.py`, `identifier_resolution_cache` in schema
- **WF USED:** `scripts/langchain/issue_dedup.py`, `scripts/duplicate_detection.py`

---

## 3. Gaps (no CENTRAL use anywhere)

| Category | Fleet posture |
|---|---|
| **Knowledge graphs** (`networkx`, `kuzu`, `neo4j`) | No adoption |
| **OpenTelemetry** | No adoption; LangSmith + custom scripts only |
| **LangGraph** | Only **TPP** is CENTRAL; no second load-bearing graph |
| **MCP** | Only **Orchestrator** implements a server; no consumer-repo MCP clients in code |
| **Browser automation** | Scattered USED (Playwright in TMP/LMS/TP); no CENTRAL product dependency |
| **Embeddings / vector search** | Only **MD** is CENTRAL; rest is agent-side semantic matching |

---

## 4. Surprises (sophisticated pieces the owner may not realize exist)

1. **Workflows is the real platform layer** — not just CI YAML: LangSmith fleet conformance (`scripts/langsmith_fleet_conformance.py`), consumer-repo sync template, `packages/stranske_pdf_extract` with its own eval suite, and `repo_review_evaluator.py` (LangGraph-aware backlog scoring).
2. **Orchestrator MCP server** (`src/mcp_server.py`) — custom stdio MCP exposing fleet capacity, route weights, and owner-question loop; zero third-party MCP SDK.
3. **Manager-Database stack depth** — Prefect ETL + pgvector embeddings + LangChain RAG chains + stlite WASM demo path in one repo.
4. **Counter_Risk PyInstaller release pipeline** — `src/counter_risk/build/release.py` with guard tests; rare in the fleet.
5. **Pension-Data eval harness** — `eval_harness.py` + golden one-PDF pilot workflow; most mature non-LangSmith eval story.
6. **learning-management-system** — full FastAPI + SQLAlchemy LMS with custom `lms/llm/client.py` (structured output, eval sets, budgets) and competency **graphs** domain model; largely independent of the LangChain consumer template.
7. **Fine-Art-Archive identity layer** — Wikidata/Getty artist resolution, work-QID search, preference learning (`preference/rocchio.py`, `bradley_terry.py`); no LangChain in product code.
8. **Inv-Man-Intake offline bridge** — Pyodide/stlite packet bridge for zero-egress intake review (`app/pyodide_packet_bridge.py`).
9. **Doc-Lineage repo name ≠ capability** — currently mirrors Workflows consumer scaffold; lineage logic lives in PD/IMI/CR instead.
10. **Fleet-wide agent belt** — codex-belt dispatcher/worker workflows (`agents-71/72/73-*`) present in every repo; multi-agent ops are production infrastructure, not experiments.

---

*Method: ripgrep for library names and idioms per category; manual verification of CENTRAL claims; consumer-template boilerplate downgraded when confined to `scripts/langchain/` and `.github/workflows/agents-*`.*
