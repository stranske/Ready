# Fleet Index — Shared Vocabulary and Cross-Repo Overview

*Generated 2026-09-04T18:00:00Z from 14 verified dossiers.*

---

## 1. Fleet Overview Table

| Repo | Category | One-line Purpose | Primary Surface | Production-Usable? | Backplane Role | Biggest Gap |
|------|----------|------------------|-----------------|-------------------|----------------|-------------|
| **Workflows** | Infrastructure Hub | Central CI/CD, agent orchestration, contract standards for 13 repos | GitHub Actions, keepalive loop | **Yes** | Fleet standards authority | Only 1/6 repos emit conformant run-contract/v1 |
| **Manager-Database** | Investment Surveillance | Tracks external managers, 13F holdings, conviction scores, activism campaigns | FastAPI + Streamlit + WASM | **Yes** | Entity authority for manager:cik_* | Integer manager_id vs string manager:<id> collision |
| **Pension-Data** | Pension Analytics | Extracts funded status, allocations, fees from pension docs | CLI, FastAPI, Static HTML | **Partial** | Canonical pension:fund:consultant IDs | Manager-DB reconciliation not wired |
| **Counter_Risk** | Risk Reporting | Monthly counterparty exposure reporting replacing MOSERS | Excel, Tkinter GUI, macro workbook | **Yes** | Local name_registry authority | No provider: prefix; no run-contract emitter |
| **Trend_Model_Project** | Portfolio Construction | Manager-of-managers trend-following with walk-forward backtesting | CLI, Streamlit, WASM, Jupyter | **Yes** | Consumer of canonical fund IDs | Emits trend.run_envelope/1 not fleet run-contract/v1 |
| **Portable-Alpha-Extension-Model** | Monte Carlo Simulation | Portable alpha and active extension fund structure modeling | CLI, Streamlit, Excel/PPTX | **Yes** | N/A — no entities | No run-contract/v1; Scenario.sleeves unwired |
| **Inv-Man-Intake** | Due Diligence | Investment manager intake, DDQs, meeting notes standardization | CLI, Streamlit | **Yes** | Source of qualitative diligence | Unaliased slugs; no provider: prefix |
| **Fine-Art-Archive** | Archive Management | Museum-grade artwork catalog with Wikidata enrichment and dedup | CLI (71 scripts), HTTP API + HTML UI | **Yes** | Artwork identity authority | No fleet entity joins; private corpus constraint |
| **Orchestrator** | Agent Fleet Manager | Routes tasks across Claude, Codex, Cursor, Gemini with quota tracking | CLI, MCP Server, dashboard | **Yes** | Fleet agent orchestration | Remote dispatch demoted; no financial entity IDs |
| **Travel-Plan-Permission** | Travel Governance | Policy compliance checking and travel workbook population | HTTP API, Browser portal, CLI | **Yes** | TPP integration seam | No run-contract emitter; ERP write-back missing |
| **trip-planner** | Travel Planning | Leisure/business travel planning with compliance integration | FastAPI + React SPA | **Yes** | Consumer of TPP contracts | Live TPP disabled; no source adapters |
| **Template/Ready/WIT** | Infrastructure Templates | Onboarding scaffold for new Python repos with standardized CI | GitHub Actions CI, agent workflows | **Yes** | Fleet contract documentation | No emitters; placeholder code |
| **Collab-Admin** | Governance | Collaboration policies, rubrics, validators, dashboards | CLI validators, Streamlit UI | **Partial** | Review workflow automation | Static dashboard not wired; no backplane registry |
| **learning-management-system** | Training Platform | Source-to-practice learning with knowledge graphs and evidence tracking | FastAPI API + Web UI | **Partial** | Learning fact provenance | No canonical entity IDs; mastery placeholder |

---

## 2. Fleet-Level Shared Vocabulary

### 2.1 Entity Types and Identifier Schemes

**Canonical Entity Types (from identity-map-conventions.md):**
- `manager` — External asset managers (Manager-Database **authoritative**)
- `fund` — Investment funds/strategies
- `pension` — Pension plans/entities (Pension-Data **authoritative**) 
- `provider` — Service providers
- `person` — Individuals
- `strategy` — Investment strategies

**Identifier Scheme Collisions:**

| Concept | Standard Format | Actual Implementations | Collision Risk |
|---------|----------------|----------------------|----------------|
| Manager IDs | `manager:<normalized_cik>` | Manager-Database: integer `manager_id`; Counter_Risk: local `canonical_key`; Inv-Man-Intake: raw slugs | **HIGH** — fragments on joins |
| Fund IDs | `fund:<normalized_lei>` | Pension-Data: EIN+plan_number; Trend_Model: raw CSV column labels | **HIGH** — no standard resolution |
| Document IDs | `document:<sha256>` | Pension-Data emits `plan:`/`document:`; Workflows uses `artifact:<hash>` | **MEDIUM** — inconsistent prefixes |
| Evidence IDs | `evidence:<sha256[:16]>` | stranske_pdf_extract: `evidence:<hash>`; PAEM: none; Manager-DB: internal `Evidence` | **MEDIUM** — schema divergence |
| Run IDs | UUID or timestamp | PAEM: `YYYYMMDDTHHMMSSZ`; Counter_Risk: no run IDs | **LOW** — per-repo uniqueness |

### 2.2 Document-Type Vocabulary

**Standardized Contract Schemas:**
- `run-contract/v1` — Run envelope with schema_version, inputs, outputs, cost, evidence_refs
- `artifact-manifest/v1` — Artifact catalog with producer, timestamp, items array
- `evidence-object/v1` — Attributed facts with schema_version, fact_ref, evidence_id, source_document
- `capability-bundle/v1` — Agent capability packaging contract
- `identity-map-conventions` — Entity typing and ID formatting rules
- `langsmith-fleet/v1` — NDJSON telemetry for fleet observability

**Emission Status by Contract:**

| Contract | Emitted By | Validated By | Schema Location |
|----------|------------|--------------|----------------|
| `run-contract/v1` | **Pension-Data only** (conformant) | Workflows validator | `docs/contracts/run-contract-v1.md` |
| `artifact-manifest/v1` | **Pension-Data** (conformant) | Workflows validator | `schemas/artifact-manifest-v1.schema.json` |
| `evidence-object/v1` | **None** currently | Workflows validator | `schemas/evidence-object-v1.schema.json` |
| `identity-map-conventions` | **Documented only** | All dossiers reference | `identity-map-conventions.md` |
| `langsmith-fleet/v1` | **Multiple** (Manager-DB, Orchestrator, PAEM, Counter_Risk, trip-planner) | Workflows validator | `langsmith-fleet-v1.md` |

### 2.3 Document-Type Vocabulary by Domain

**Investment Domain:**
- **Manager-Database**: 13F-HR, 13D/G filings, holdings deltas, conviction scores, activism events
- **Trend_Model_Project**: Manager return series, portfolio allocations, walk-forward windows, performance metrics
- **Counter_Risk**: MOSERS/NISA Excel, CPRS files, concentration metrics, limit breaches
- **Pension-Data**: Form 5500, PPD data, actuarial measures, funded status, allocations
- **Portable-Alpha-Extension-Model**: Index returns CSV/XLSX, Monte Carlo paths, sleeve configurations

**Operational Domain:**
- **Travel-Plan-Permission**: TripPlan JSON, ExpenseReport JSON, Policy snapshots, Approval packages
- **trip-planner**: Trip proposals, Inventory bundles, Ranked result sets, Route context maps
- **Orchestrator**: Run records, Route weights, Capability bundles, Completion events
- **Collab-Admin**: Time logs, Expense logs, Friction logs, Review YAML, Submission packets

**Content Domain:**
- **Fine-Art-Archive**: meta.json sidecars, manifest.csv, ratings_log.jsonl, research_requests.jsonl
- **learning-management-system**: SourceReference with locator/path/line, Evidence records, Knowledge graph nodes/edges

**Infrastructure Domain:**
- **Workflows**: Reusable workflows, Sync manifests, Capability bundles, Agent runner outputs
- **Template/Ready/WIT**: Placeholder code, Contract schemas, Validation scripts

### 2.4 Contract Compliance Matrix

| Repo | run-contract/v1 | artifact-manifest/v1 | evidence-object/v1 | identity-map-conventions |
|------|------------------|----------------------|---------------------|-------------------------|
| Workflows | ⚠️ Validator only | ⚠️ Validator only | ⚠️ Validator only | ✅ Documented |
| Manager-Database | ❌ Not emitted | ❌ Not emitted | ⚠️ Internal Evidence | ❌ Integer IDs |
| Pension-Data | ✅ **Emitted & conformant** | ✅ **Emitted & conformant** | ⚠️ Hashed refs only | ⚠️ Partially followed |
| Counter_Risk | ❌ Not emitted | ❌ Not emitted | ⚠️ Evidence pointers | ❌ No provider: prefix |
| Trend_Model_Project | ❌ Emits trend.run_envelope/1 | ❌ Not emitted | ❌ Not emitted | ⚠️ Raw CSV labels |
| Portable-Alpha-Extension-Model | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ✅ N/A (no entities) |
| Inv-Man-Intake | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ❌ Unaliased slugs |
| Fine-Art-Archive | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ✅ N/A (artwork IDs) |
| Orchestrator | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ❌ Git refs only |
| Travel-Plan-Permission | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ❌ Org-local IDs |
| trip-planner | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ❌ Internal keys |
| Template/Ready/WIT | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ✅ Documented |
| Collab-Admin | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ✅ Documented |
| learning-management-system | ❌ Not emitted | ❌ Not emitted | ❌ Not emitted | ❌ UUIDs only |

---

## 3. Cross-Repo Reuse Matrix

### 3.1 Component → Potential Consumer Repos

| Component | Path | Consumer Repos | Reuse Notes |
|-----------|------|----------------|-------------|
| **Name Registry + Validation** | Counter_Risk: `name_registry.py`, `config/name_registry.yml` | Manager-Database, Pension-Data, Trend_Model, Inv-Man-Intake | **Collision**: Needs provider: prefix for fleet joins |
| **Holdings Diff Engine** | Manager-Database: `diff_holdings.py` | Counter_Risk, Pension-Data, Inv-Man-Intake | **Ready**: Handles 13F amendments, restatements |
| **Point-In-Time Engine** | Manager-Database: `etl/point_in_time.py` | Pension-Data, Trend_Model | **Ready**: Bitemporal knowledge_time isolation |
| **Manifest Builder + Schema** | Counter_Risk: `pipeline/manifest.py`, `manifest_schema.py` | **All fleet repos** | **Gap**: Schema version collisions |
| **LangSmith Fleet Emitter** | Multiple repos | **All fleet repos** | **Ready**: Standardized telemetry |
| **CUSIP-to-FIGI/LEI Resolver** | Manager-Database: `adapters/openfigi.py` | Counter_Risk, Pension-Data, Trend_Model | **Ready**: Persistent caching |
| **Bitemporal Fact Model** | Pension-Data: `db/models/bitemporal.py` | Manager-Database, Fine-Art-Archive | **Ready**: Assertion/validation time separation |
| **Entity Alias/Merge Engine** | Pension-Data: `entities/service.py` | Manager-Database, Counter_Risk, Inv-Man-Intake | **Ready**: Forward lineage tracking |
| **Deterministic Artifact Dedupe** | Pension-Data: `ingest/artifacts.py` | **All ingestion repos** | **Ready**: SHA-256 content addressing |
| **Run Contract Validator** | Workflows: `scripts/validate_run_contract.py` | **All fleet repos** | **Ready**: Offline conformance checking |
| **Coverage Guard** | Template/Ready: `tools/coverage_guard.py` | **All fleet repos** | **Ready**: Baseline breach pattern |
| **PDF Extraction Contract** | Workflows: `stranske_pdf_extract` | Manager-Database, Inv-Man-Intake, Counter_Risk, Pension-Data | **Scaffold**: Migration pending |
| **Policy Engine** | Travel-Plan-Permission: `policy.py` | trip-planner, Collab-Admin | **Ready**: YAML-driven rule evaluation |
| **Ranking Engine** | trip-planner: `ranking/base.py` | Trend_Model, Manager-Database | **Ready**: Multicriteria scoring |
| **WASM Packaging** | Multiple repos | **All browser-target repos** | **Ready**: Pyodide/stlite patterns |

### 3.2 Data Flow Dependencies

```
Manager-Database --CIK/LEI--> Counter_Risk
                     |         (name_registry)
                     v
            Manager-Database --holdings--> Trend_Model
                     |
                     +--conviction--> Investment Decisions
                     |
Pension-Data --fund:pension IDs--> [Fleet Joins] <--manager:cik_*-- Manager-Database
                     |
                     v
            Pension-Data --acts--> Counter_Risk (future)

Travel-Plan-Permission <--proposals--> trip-planner
            |
            v
   Approval packages --> Accounting Systems (future)

Orchestrator --agent routing--> All Repos (CLI surfaces)
            |
            v
   Workflows --CI standards--> All Repos
```

### 3.3 Integration Seams (Current vs. Planned)

**Active Integration Seams:**
- **Workflows → All Repos**: CI/CD automation, sync manifests, agent workflows
- **Travel-Plan-Permission → trip-planner**: Planner integration contract, handoff endpoints
- **Manager-Database → Siblings**: Planned but unwired (entity resolution pending)
- **Pension-Data → Fleet**: Backplane conformant run-contract and artifact-manifest emission

**Planned Integration Seams:**
- **Manager-Database → Counter_Risk**: Manager entity resolution for exposure joins
- **Pension-Data → Manager-Database**: Fund/manager cross-references
- **All → Workflows**: Backplane run-contract conformance (1 of 6 currently active)

---

## 4. Recommended Reading Order for a Colleague

### 4.1 Tier 1 — Infrastructure Foundations (Read First)
1. **Workflows** — Understand the fleet's CI/CD standards, contract schemas, and automation patterns
2. **Template/Ready/WIT** — Learn the onboarding template and validation expectations
3. **Orchestrator** — Comprehend the agent routing and quota management system

### 4.2 Tier 2 — Core Investment Analytics (Read Second)
4. **Manager-Database** — Master entity authority and surveillance capabilities
5. **Pension-Data** — Study document-to-fact extraction and canonical ID patterns
6. **Counter_Risk** — Review risk reporting workflows and local registry patterns

### 4.3 Tier 3 — Specialized Domains (Read Third)
7. **Trend_Model_Project** — Portfolio construction and backtesting methodologies
8. **Portable-Alpha-Extension-Model** — Monte Carlo simulation and sleeve optimization
9. **Inv-Man-Intake** — Due diligence intake and standardization patterns
10. **Fine-Art-Archive** — Archive management and metadata enrichment (analogous patterns)

### 4.4 Tier 4 — Operational Systems (Read Fourth)
11. **Travel-Plan-Permission** — Policy compliance and governance automation
12. **trip-planner** — Travel planning and integration patterns
13. **Collab-Admin** — Governance workflows and review automation
14. **learning-management-system** — Learning traceability and evidence patterns

### 4.2 Study Strategy by Objective

**If you need to...**
- **Integrate systems**: Start with Workflows + Manager-Database + Pension-Data
- **Understand testing**: Workflows + Orchestrator + Template
- **Build extraction pipelines**: Pension-Data + Counter_Risk + Manager-Database
- **Create governance**: Collab-Admin + Travel-Plan-Permission + Workflows
- **Model portfolios**: Trend_Model_Project + Portable-Alpha-Extension-Model + Manager-Database

---

## 5. Critical Observations and Recommendations

### 5.1 Most Pressing Vocabulary Collisions

**Priority 1 — Entity Identifiers:** Manager-Database's integer `manager_id` must be reconciled with the fleet standard `manager:<normalized_cik>`. Without this, any cross-repo join on investment entities will fragment. Pension-Data's `plan_id` + `plan_period` pattern is consistent internally but needs mapping to `pension:<ein_plan_number>` for fleet consumption.

**Priority 2 — Contract Emission:** Only Pension-Data currently emits conformant `run-contract/v1` and `artifact-manifest/v1`. The backplane conformance workflow skips 5 of 6 registered repos due to missing emitters. Trend_Model_Project emits `trend.run_envelope/1` which is a different schema.

**Priority 3 — Evidence Standardization:** Evidence objects exist in various forms: Pension-Data's hashed reference strings, Manager-Database's internal `Evidence` class (missing schema fields), Counter_Risk's local evidence pointers. None emit the standardized `evidence-object/v1` schema.

### 5.2 High-Value Reuse Opportunities

1. **Manager-Database's OpenFIGI client** — Already used for CUSIP-to-FIGI/Ticker/LEI resolution with persistent caching. Could standardize security identifier resolution across Counter_Risk, Pension-Data, and Trend_Model.

2. **Pension-Data's entity service** — Deterministic ID generation, alias matching, and forward lineage. Critical for resolving the manager/fund/pension entity collision.

3. **Workflows' validation scripts** — `validate_run_contract.py` and coverage guards are production-ready for fleet-wide adoption.

4. **Counter_Risk's manifest builder** — Proven pattern for run artifact provenance that could be standardized across repos.

### 5.3 Strategic Gaps Requiring Attention

1. **Backplane Adoption**: Only 1 of 6 repos emits conformant run-contracts. This is the single biggest blocker to fleet interoperability.

2. **Entity Authority**: Manager-Database is declared authoritative for manager entities, but its integer IDs don't match fleet conventions. This must be resolved before any meaningful cross-repo analytics.

3. **Evidence Provenance**: Multiple repos track source documents and extractions, but none use the standardized evidence-object schema. This prevents auditable cross-repo fact attribution.

4. **Contract Schema Harmonization**: Trend_Model_Project emits `trend.run_envelope/1`, Counter_Risk has local manifests. These need alignment or explicit mapping to fleet standards.

---

*Compiled from 14 verified dossiers: Counter_Risk, Fine-Art-Archive, Inv-Man-Intake, Manager-Database, Orchestrator, Pension-Data, Portable-Alpha-Extension-Model, Template, Travel-Plan-Permission, Collab-Admin, learning-management-system, Trend_Model_Project, trip-planner, Workflows.*