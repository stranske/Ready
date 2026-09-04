# stranske/trip-planner — dossier (2026-09-04)

## 1. Purpose in one paragraph
`trip-planner` coordinates leisure travel and policy-compliant business travel for corporate personnel. Users define trip parameters, evaluate lodging and activities, balance schedules, compare scenarios, and track budgets. For business travel, it evaluates packages against company policies to generate approval proposals. Designed around a local-first constraint, it runs inside a corporate network or on an offline workstation without cloud dependencies. It defaults to local SQLite storage and deterministic scoring, gating external LLM connections and remote microservices behind data-zone controls (`TRIP_PLANNER_DATA_ZONE`).

## 2. Who uses it and how (surfaces)
| Surface | Entry point (file) | Who uses it | Status (working / partial / scaffold) with evidence |
| :--- | :--- | :--- | :--- |
| **REST Web API** | `trip_planner/app/main.py` | Browser SPA, test runners | **Working**. FastAPI backend for auth, trips, workspace, and proposals (`routes/`). Verified in `tests/app/test_trip_routes.py`. |
| **Web UI (SPA)** | `frontend/src/main.tsx` | Travelers, travel managers | **Working**. React 19 / Vite SPA (`src/router.tsx`) covering onboarding, trip creation, and workspace. Verified via Playwright canary (`scripts/run_two_trip_ui_canary.sh`). |
| **Operator CLI** | `scripts/seed_demo_data.py` | Developers, test automation | **Working**. Seeds demo user (`demo@trip-planner.local`); `scripts/check_full_product_verification.py` verifies product journeys. |
| **Map Card** | `frontend/src/components/maps/TripMap.tsx` | Travelers checking routes | **Partial (Bounded Fallback)**. Renders Google Maps when the JS API loads with a key; otherwise falls back to bounded SVG schematics per `docs/contracts/route-context-map-target.md`. Live distance/geometry verification remains a follow-up (`docs/reports/runtime-seam-audit.md:30`, Issue `#1191`). |
| **TPP Remote Client** | `trip_planner/integrations/tpp/client.py` | Compliance teams, expense systems | **Partial (Integration Seam)**. HTTP client with circuit breaking (`_CircuitBreaker`). Disabled by default (`live_tpp=off`), using local evaluation (`trip_planner/business/approval_ready.py`). |
| **Legacy HTML Generator** | `scripts/build_html.py` | Legacy demo reviewers | **Scaffold / Broken Legacy**. Renders static HTML from `data/`. Requires unlisted `jinja2`; `tests/test_build_html.py` is skipped in pytest (`pyproject.toml:65`). |

## 3. Structure map
```
stranske/trip-planner/
├── trip_planner/                  # Core Python package
│   ├── app/                       # FastAPI routes, schemas, workspace services
│   ├── business/                  # Policy rules and approval packages
│   ├── contracts/                 # Canonical domain contracts (options, trips)
│   ├── options/                   # Activities, lodging, transit, bundles
│   ├── ranking/                   # Scoring engines for leisure/business
│   ├── persistence/               # SQLAlchemy models and migrations
│   ├── state/                     # Repositories for trips and scenarios
│   ├── integrations/              # External client adapters (tpp/)
│   └── resources/                 # Seeded JSON catalog files
├── frontend/                      # React 19 / Vite web client
├── docs/                          # Architecture epics and contracts/
├── scripts/                       # Operational, verification, and test scripts
├── tests/                         # Pytest test suite
├── data/                          # Legacy JSON datasets
└── Synced from stranske/Workflows: # Workflows CI and backplane scripts
```

## 4. Major code features you must understand to extend it
- **Workspace State Aggregator** (`trip_planner.app.services.workspace:get_workspace_payload`): Assembles workspace JSON from `trip_id`, credentials, and db session. Why it matters: Central hydration nexus for frontend views.
- **Conversational Planner Engine** (`trip_planner.app.services.planner:submit_planner_turn`): Executes planning dialogue within privacy redactions. Why it matters: Powers conversational planning with deterministic fallback.
- **Multicriteria Scenario Ranking Engine** (`trip_planner.ranking.leisure:LeisureRankingEngine`, `trip_planner.ranking.business:BusinessRankingEngine`): Evaluates candidate bundles against traveler/business preference profiles. Why it matters: Drives comparative evaluation across alternative itineraries.
- **Mixed-Inventory Feasibility Pipeline** (`trip_planner.itinerary.feasibility:evaluate_bundle_feasibility`): Validates lodging, transit, and activity timings to produce a `FeasibilityAssessment` over an `InventoryBundle`. Why it matters: Prevents impossible schedules reaching travelers.
- **Corporate Policy & Approval Compiler** (`trip_planner.business.approval_ready:build_approval_ready_package`): Compiles profiles, proposals, and evaluations into an `ApprovalReadyPackage`. Why it matters: Converts travel plans into auditable compliance proposals for executive sign-off.
- **Revealed Preference Learning Engine** (`trip_planner.preferences.revealed_preference:build_revealed_preference_update`): Adjusts preference weights dynamically from user interaction events. Why it matters: Continuously adapts suggestions without repetitive questionnaires.
- **Fault-Tolerant TPP Client** (`trip_planner.integrations.tpp.client:HTTPTPPIntegrationClient`, `_CircuitBreaker`): Wraps remote policy queries with exponential backoff and circuit breaking. Why it matters: Isolates the workspace from service outages.

## 5. Data model, identifiers and contracts
Entities use typed string IDs: `trip_id` (e.g., `trip-leisure-kyoto-draft`) is the root container; `user_id` and `session_id` identify accounts and sessions (authenticated via SHA-256 `token_hash`); `saved_scenario_id` tracks scenario collections (`current_version_id` points to the active version head); `proposal_id` and `proposal_version` identify corporate proposals; catalog items use `option_id`, `destination_id`, `activity_id`, `lodging_id`, and `bundle_id`; options carry `source_id`, and the source-ingestion layer tracks `snapshot_id` on `RawSnapshot` records.

Persistence uses SQLAlchemy 2.0 with Alembic migrations (`trip_planner/persistence/db.py`), defaulting to SQLite at `[app-data-dir]/trip_planner.db`, normalizing to PostgreSQL when `TRIP_PLANNER_DATABASE_URL` is set.

### Contract Audit (`docs/contracts/*`):
- **Emitted and Consumed**: `trip-plan-proposal.md`, `tpp-approval-ready.md`, `route-context-map-target.md`, `inventory-bundle.md`, `business-ranking.md`, `ranking-results.md`, `activity-option.md`, `lodging-option.md`, `transport-option.md`, `canonical-state-seam.md`, and TPP contracts.
- **Documented Only**: Synced Workflows contracts (`run-contract-v1.md`, `schemas/evidence-object-v1.schema.json`, `schemas/artifact-manifest-v1.schema.json`, `identity-map-conventions.md`, `capability-bundle-v1.md`, `agent-runner-output.md`).

## 6. External inputs and dependencies
- **Data Sources**: Internal JSON files in `trip_planner/resources/` (options, destinations, policies) and legacy JSON in `data/`. No external travel APIs are wired; `trip_planner/sources/adapters/` contains only an abstract `base.py`.
- **LLM and Agent Usage**: Optional planning via `langchain-core==1.5.3` and `langchain-openai==1.4.1`. Blocked under `TRIP_PLANNER_DATA_ZONE=proprietary` without authorized endpoint markers. Falls back to deterministic heuristics when unconfigured. Writes `langsmith-fleet/v1` records to `langsmith-fleet.ndjson`; no LangGraph or MCP servers exist.
- **Key Libraries & Runtime**: FastAPI, Uvicorn, SQLAlchemy 2.0, Alembic, psycopg[binary] on backend; Vite, React 19, TypeScript on frontend. Runs locally with Python 3.12+ and SQLite; production uses Netlify and Render.

## 7. Current state
- **Test and CI Posture**: Gated via `.github/workflows/ci.yml` and `pr-00-gate.yml`. Runs Ruff, Black, Mypy, and Pytest on Python 3.12/3.13, enforcing a 90% coverage floor (`stranske/Workflows` reusable `reusable-10-ci-python.yml` via `ci.yml`) and complexity ceiling of 25 (`scripts/measure_complexity.py`). Runtime CI validates full-stack connectivity (`scripts/check_full_stack_runtime.sh`) and Playwright browser journeys (`scripts/run_two_trip_ui_canary.sh`).
- **Production-Usable vs Prototype**: Persistence, authentication, trip/scenario CRUD, budget tracking, and rule-based policy evaluations are production-usable. Live data ingestion, live Google Maps geometry, and remote TPP governance are prototype/deferred seams.
- **Consequential Gap Signals**:
  1. *No live source adapters*: `trip_planner/sources/adapters/base.py` exists without concrete implementations.
  2. *Live remote TPP deferred*: `scripts/check_full_product_verification.py:504` (`tpp_prerequisite_status`) skips remote TPP when `live_tpp=off`.
  3. *Route distance verification deferred*: Live distance/geometry verification remains a design follow-up (`docs/reports/runtime-seam-audit.md:30`, Issue `#1191`).
  4. *Broken legacy script*: `scripts/build_html.py` imports unlisted `jinja2`, skipped in `pyproject.toml:65`.
  5. *Absence of longitudinal memory*: Cross-trip standing preferences are deferred (`docs/effortless-travel-roadmap.md:57-58`).
  6. *Keyword matching planner routing*: Deterministic planner intent routing uses keyword checks, not semantic or vector recall (`docs/langchain-planner-runtime-epic.md:28`, `trip_planner/app/services/planner_routing.py:154-167`).

## 8. Claims vs reality
- **Claim: Research-backplane participant emitting `run-contract/v1` envelopes** (`docs/contracts/run-contract-v1.md`). Reality: Zero code in `trip_planner/` emits or consumes it; `scripts/validate_run_contract.py` is opt-in and no-ops (SKIP) when the repo is absent from the registry passed via `--registry` (this repo ships no `config/backplane_participants.json` entry).
- **Claim: Extensible external source adapter framework** (`docs/contracts/source-adapters.md`). Reality: Only `trip_planner/sources/adapters/base.py` exists; all inventory loads from static files in `trip_planner/resources/`.
- **Claim: Functional legacy demo quick start** (`README.md:95-100`). Reality: `scripts/build_html.py` crashes on fresh installs because `jinja2` is omitted from `pyproject.toml` dependencies; tests are suppressed in `pyproject.toml:65`.
- **Claim: Semantic planner memory** (`docs/langchain-planner-runtime-epic.md`). Reality: Planner routing and offline fallback use keyword matching (`trip_planner/app/services/planner_routing.py:154-167`, `trip_planner/app/services/planner.py:975-979`); the epic still lists semantic recall for scattered planning notes as an open gap (`docs/langchain-planner-runtime-epic.md:28`).
- **Claim: Live remote policy integration** (`docs/contracts/tpp-proposal-execution.md`). Reality: Remote HTTP transport runs disabled (`live_tpp=off`), relying on local rules in `approval_ready.py`.

## 9. Interoperability hooks (for the fleet program)
- **What this repo could OFFER to sibling repos**:
  - `TripPlanProposal` (`trip_planner.business.policy_contracts:TripPlanProposal`): Travel proposals specifying dates, costs, options, and justifications for pre-travel authorization in `stranske/Travel-Plan-Permission`.
  - `ApprovalReadyPackage` (`trip_planner.business.approval_ready:ApprovalReadyPackage`): Audit packages linking itineraries to policy scores, sign-off roles, and receipt requirements for enterprise accounting.
  - `RankedResultSet` (`trip_planner.ranking.models:RankedResultSet`): Ranked scenarios with multi-attribute utility breakdowns for resource optimization.
  - `langsmith-fleet/v1` Telemetry: Sanitized JSON records reporting agent latency, token usage, and status to centralized fleet dashboards.
- **What this repo would CONSUME from sibling repos**:
  - Corporate Travel Policies: Nightly lodging limits and per-diem allowances via `TPPPolicyRequirement` payloads (`policy_sync.py`).
  - Travel Authorizations: Approval/rejection decisions from `Travel-Plan-Permission` (`PersistedEvaluationResult` in `results.py`).
  - Investment Calendar Events: Target company meetings or due diligence schedules ingested into `required_presence_windows`.
- **Potential Collisions**: Internal keys (`user_id`) conflict with corporate Active Directory / SSO GUIDs; unvalidated strings (`organization_id`) conflict with Legal Entity Identifiers (LEI); local slugs (`kyoto`) conflict with IATA codes (`NRT`); internal `DimensionEvidenceRecord` lacks standard `evidence-object-v1` hashes and page citations.

## 10. Reuse candidates
- `trip_planner/integrations/tpp/client.py` (`_CircuitBreaker`): Host-keyed HTTP circuit breaker with exponential backoff and typed error taxonomy.
- `trip_planner/ranking/base.py` (`BaseRankingEngine`): Multicriteria scoring and ranking engine with explanation generation.
- `trip_planner/observability/langsmith_fleet.py`: Anonymizing LangSmith telemetry exporter hashing private entity IDs.
- `scripts/measure_complexity.py`: Standalone AST-based PR complexity ceiling enforcer.
- `trip_planner/sources/quality.py` (`SourceQualityScorer`): Epistemic source credibility and trust-tier scoring calculator.
- `trip_planner/app/services/workspace_map_payloads.py`: Bounded route geometry generator with SVG fallback.
- `trip_planner/persistence/models/session.py` (`AuthSession`) with helpers in `trip_planner/app/services/auth.py`: Lightweight bearer token session service with sliding renewal.

## 11. Proposed direction (evidence-based)
### Finish What Is Scaffolded:
- **Concrete Source Adapters**: Build connectors in `trip_planner/sources/adapters/` against an open travel API to replace static JSON fixtures.
- **Live TPP Client in Staging**: Activate HTTP transport in `trip_planner/integrations/tpp/client.py` against a running `Travel-Plan-Permission` container in CI.
- **Route Geometry Seam (#1191)**: Complete server-side distance matrix verification when Google Maps credentials exist (`docs/reports/runtime-seam-audit.md:30`).
- **Modernize Legacy Scripts**: Restore `jinja2` to `pyproject.toml` dependencies and re-enable `tests/test_build_html.py`, or remove `scripts/build_html.py`.

### New Capabilities:
- **Adopt Run Contracts**: Implement emission of `run-contract/v1` envelopes and `artifact-manifest-v1` files in `trip_planner/app/services/`.
- **Corporate SSO**: Replace local password auth with SAML/OIDC integration, mapping traveler profiles to directory IDs.
- **Due Diligence Calendar Ingestion**: Ingest corporate calendar feeds (.ics/API) to generate business presence windows for deal teams.
- **Vectorized Planner Memory**: Upgrade planner recall from keyword routing to local vector embeddings per `docs/langchain-planner-runtime-epic.md:28`.

## 12. What a colleague needs to know (5 bullets, no code identifiers)
- **What the tool does**: Dual-purpose travel portal allowing professionals to build, visualize, and budget vacations or business trips in a browser.
- **Current data limitations**: All flight, hotel, and activity options are generated from internal demo catalogs rather than live reservation systems.
- **Corporate compliance automation**: Checks planned itineraries against spend caps and policies, assembling justification packages for management sign-off.
- **Security and data privacy**: Runs securely inside an enterprise network, keeping itineraries on local servers so confidential plans are never sent to external AI.
- **Institutional interoperability**: Built to connect with corporate single sign-on, expense tools, and deal calendars to streamline due diligence travel.

*Evidence-checked against source repositories; verification metadata omitted from work bundle.*
