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
| **Portable-Alpha-Extension-Model** | Monte Carlo Simulation | Portable alpha and active extension fund structure modeling | CLI, Streamlit, Browser/stlite (unverified), Excel/PPTX | **Yes** | N/A — no entities | No run-contract/v1; Scenario.sleeves unwired; README regime caveats stale |
| **Inv-Man-Intake** | Due Diligence | Investment manager intake, DDQs, meeting notes standardization | CLI, Streamlit | **Yes** | Source of qualitative diligence | Unaliased slugs; no provider: prefix |
| **Fine-Art-Archive** | Archive Management | Museum-grade artwork catalog with Wikidata enrichment and dedup | CLI (71 scripts), HTTP API + HTML UI | **Yes** | Artwork identity authority | No fleet entity joins; private corpus constraint |
| **Orchestrator** | Agent Fleet Manager | Routes tasks across Claude, Codex, Cursor, Gemini with quota tracking | CLI, MCP Server, dashboard | **Yes** | Fleet agent orchestration | Remote dispatch demoted; no financial entity IDs |
| **Travel-Plan-Permission** | Travel Governance | Policy compliance checking and travel workbook population | HTTP API, Browser portal (`/portal/draft/new`), CLI | **Yes (alpha)** | TPP integration seam | No run-contract emitter; ERP write-back; security-model REST docs unwired |
| **trip-planner** | Travel Planning | Leisure/business travel planning with compliance integration | FastAPI + React SPA | **Yes** | Consumer of TPP contracts | Live TPP disabled; no source adapters |
| **Template/Ready/WIT** | Infrastructure Templates | Onboarding scaffold for new Python repos with standardized CI | GitHub Actions CI, agent workflows | **Yes** | Fleet contract documentation | No emitters; placeholder code |
| **Collab-Admin** | Governance | Collaboration policies, rubrics, validators, dashboards | CLI validators, Streamlit UI | **Partial** | Review workflow automation | Static dashboard not wired; no backplane registry |
| **learning-management-system** | Training Platform | Source-to-practice learning with knowledge graphs and evidence tracking | FastAPI API + Web UI | **Partial** | Learning fact provenance | No canonical entity IDs; mastery placeholder |

---

## 2. Fleet-Level Shared Vocabulary

### 2.1 Entity Types and Identifier Schemes

**Canonical Entity Types:** `manager` (Manager-Database authoritative), `fund`, `pension` (Pension-Data authoritative), `provider`, `person`, `strategy`.

**Critical Identifier Collisions:**

| Concept | Standard | Actual | Risk |
|---------|----------|--------|------|
| Manager IDs | `manager:<normalized_cik>` | Manager-DB: integer `manager_id`; Counter_Risk: `canonical_key`; Inv-Man-Intake: raw slugs | **HIGH** |
| Fund IDs | `fund:<normalized_lei>` | Pension-Data: EIN+plan_number; Trend_Model: raw CSV labels | **HIGH** |
| Document IDs | `document:<sha256>` | Pension-Data: `plan:`/`document:`; Workflows: `artifact:<hash>` | **MEDIUM** |
| Evidence IDs | `evidence:<sha256[:16]>` | Various internal formats; none conformant | **MEDIUM** |

### 2.2 Contract Schemas Status

**Standardized Contracts:** `run-contract/v1`, `artifact-manifest/v1`, `evidence-object/v1`, `capability-bundle/v1`, `identity-map-conventions`, `langsmith-fleet/v1`.

**Emission Reality:** Only Pension-Data emits conformant `run-contract/v1` and `artifact-manifest/v1`. Trend_Model emits `trend.run_envelope/1`. Multiple repos emit `langsmith-fleet/v1`. No repo emits `evidence-object/v1`.

### 2.3 Document-Type Vocabulary by Domain

**Investment:** Manager-Database (13F-HR, 13D/G, holdings deltas, conviction), Trend_Model (return series, allocations, performance metrics), Counter_Risk (MOSERS/NISA, CPRS, concentration), Pension-Data (Form 5500, PPD, actuarial), PAEM (index returns, Monte Carlo).

**Operational:** Travel-Plan-Permission (TripPlan JSON, ExpenseReport, policy snapshots), trip-planner (proposals, inventory bundles, rankings), Orchestrator (run records, route weights).

**Content:** Fine-Art-Archive (meta.json, manifest.csv, ratings_log.jsonl), learning-management-system (SourceReference, knowledge graph nodes/edges).

**Infrastructure:** Workflows (reusable workflows, sync manifests), Template (contract schemas, validators).

### 2.4 Contract Compliance Summary

| Repo | run-contract/v1 | artifact-manifest/v1 | evidence-object/v1 | identity-map |
|------|------------------|----------------------|---------------------|---------------|
| Workflows | Validator only | Validator only | Validator only | Documented |
| Manager-Database | Not emitted | Not emitted | Internal only | Integer IDs |
| Pension-Data | ✅ Emitted | ✅ Emitted | Hashed refs | Partially followed |
| Counter_Risk | Not emitted | Not emitted | Pointers | No provider: |
| Trend_Model_Project | trend.run_envelope/1 | Not emitted | Not emitted | Raw labels |
| Others | Not emitted | Not emitted | Not emitted | Various |

---

## 3. Cross-Repo Reuse Matrix

### 3.1 Component → Consumer Repos

| Component | Path | Consumers | Status |
|-----------|------|-----------|--------|
| Name Registry + Validation | Counter_Risk: `name_registry.py` | Manager-DB, Pension-Data, Trend_Model, Inv-Man-Intake | Needs provider: prefix |
| Holdings Diff Engine | Manager-DB: `diff_holdings.py` | Counter_Risk, Pension-Data, Inv-Man-Intake | Ready for reuse |
| Point-In-Time Engine | Manager-DB: `etl/point_in_time.py` | Pension-Data, Trend_Model | Bitemporal ready |
| Manifest Builder | Counter_Risk: `pipeline/manifest.py` | All fleet repos | Schema collision risk |
| LangSmith Fleet Emitter | Multiple repos | All fleet repos | Standardized telemetry |
| CUSIP-to-FIGI/LEI Resolver | Manager-DB: `adapters/openfigi.py` | Counter_Risk, Pension-Data, Trend_Model | Persistent caching |
| Bitemporal Fact Model | Pension-Data: `db/models/bitemporal.py` | Manager-DB, Fine-Art-Archive | Assertion/validation time |
| Entity Alias/Merge Engine | Pension-Data: `entities/service.py` | Manager-DB, Counter_Risk, Inv-Man-Intake | Forward lineage |
| Run Contract Validator | Workflows: `scripts/validate_run_contract.py` | All fleet repos | Offline conformance |
| Coverage Guard | Template: `tools/coverage_guard.py` | All fleet repos | Baseline pattern |

### 3.2 Data Flow Dependencies

```
Manager-Database --CIK/LEI--> Counter_Risk
Manager-Database --holdings--> Trend_Model
Pension-Data --fund:pension IDs--> [Fleet Joins] <--manager:cik_*-- Manager-Database
Travel-Plan-Permission <--proposals--> trip-planner
Orchestrator --agent routing--> All Repos
Workflows --CI standards--> All Repos
```

---

## 4. Recommended Reading Order

### 4.1 By Priority Tier

**Tier 1 — Infrastructure:** Workflows → Template/Ready/WIT → Orchestrator
**Tier 2 — Core Analytics:** Manager-Database → Pension-Data → Counter_Risk  
**Tier 3 — Specialized:** Trend_Model_Project → Portable-Alpha-Extension-Model → Inv-Man-Intake → Fine-Art-Archive
**Tier 4 — Operational:** Travel-Plan-Permission → trip-planner → Collab-Admin → learning-management-system

### 4.2 By Objective

- **Integrate systems:** Workflows + Manager-Database + Pension-Data
- **Understand testing:** Workflows + Orchestrator + Template
- **Build extraction:** Pension-Data + Counter_Risk + Manager-Database
- **Create governance:** Collab-Admin + Travel-Plan-Permission + Workflows
- **Model portfolios:** Trend_Model_Project + PAEM + Manager-Database

---

## 5. Critical Observations

### 5.1 Top Vocabulary Collisions

1. **Manager Identifiers:** Manager-Database's integer `manager_id` vs fleet standard `manager:<normalized_cik>` — blocks all cross-repo investment entity joins.
2. **Contract Emission:** Only Pension-Data emits conformant `run-contract/v1`/`artifact-manifest/v1`; backplane workflow skips 5/6 repos.
3. **Evidence Standard:** No repo emits standardized `evidence-object/v1` despite multiple internal evidence formats.
4. **Schema Harmony:** Trend_Model emits `trend.run_envelope/1`, creating namespace collision with fleet `run-contract/v1`.

### 5.2 High-Value Reuse Opportunities

- **Manager-DB OpenFIGI client:** Standardize security identifier resolution
- **Pension-Data entity service:** Resolve entity collision via deterministic IDs
- **Workflows validators:** Production-ready for fleet adoption  
- **Counter_Risk manifest builder:** Standardize run artifact provenance

### 5.3 Strategic Gaps

1. Backplane adoption (1/6 repos conformant)
2. Entity authority reconciliation (integer vs string IDs)
3. Evidence provenance standardization (no conformant emitters)
4. Contract schema harmonization (namespace collisions)

---

*Compiled from 14 verified dossiers: Counter_Risk, Fine-Art-Archive, Inv-Man-Intake, Manager-Database, Orchestrator, Pension-Data, Portable-Alpha-Extension-Model, Template, Travel-Plan-Permission, Collab-Admin, learning-management-system, Trend_Model_Project, trip-planner, Workflows.*