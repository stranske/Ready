# Travel-Plan-Permission — dossier (2026-09-04)

## 1. Purpose in one paragraph

Travel-Plan-Permission (TPP) automates the travel-request approval and expense-reimbursement workflow for an investment-office-style organization. The README (`README.md:5-6`) states the goal plainly: make the travel plan approval and reimbursement process reproducible. The system is built around a canonical TripPlan JSON contract (`schemas/trip_plan.min.schema.json`), deterministic policy evaluation (`src/travel_plan_permission/policy.py`), and population of the organization’s existing Excel travel workbook (`templates/Travel_Itinerary_Form_Jan_1_2026_revised.xlsx` via `src/travel_plan_permission/workbook_population.py`). It was designed to run as a local or hosted Python service (`tpp-planner-service` in `pyproject.toml:62`) with a small server-rendered browser portal (`src/travel_plan_permission/http_service.py`), while exposing a bearer-token HTTP seam for the sibling `trip-planner` repo (`docs/contracts/planner-integration.md`). Real proprietary travel data is intended for on-prem or internal deployment; the public Render service is explicitly fixtures-only (`render.yaml:1-6`, `TPP_DEMO_MODE=1`).

## 2. Who uses it and how (surfaces)

| Surface | Entry point | Who uses it | Status (evidence) |
| --- | --- | --- | --- |
| CLI — spreadsheet fill | `fill-spreadsheet` → `src/travel_plan_permission/cli.py` | Developers, batch operators converting TripPlan JSON to Excel | **Working** — documented in `README.md:35-41`; tested in `tests/python/test_cli.py` |
| CLI — planner smoke | `tpp-planner-smoke` → `src/travel_plan_permission/planner_smoke.py` | Integrators validating a running HTTP service | **Working** — `README.md:175-185`; `tests/python/test_planner_smoke.py` |
| CLI — cross-repo smoke | `tpp-cross-repo-smoke` → `src/travel_plan_permission/cross_repo_smoke.py` | CI / integrators pairing with `trip-planner` | **Working** — CI job `cross-repo-smoke` in `.github/workflows/ci.yml:89-236` |
| CLI — audit export/prune | `tpp-audit-export`, `tpp-audit-prune` → `src/travel_plan_permission/audit.py` | Finance/compliance admins | **Working** — `src/travel_plan_permission/audit.py:17-18`; `tests/python/test_audit.py` |
| CLI — orchestration demo | `orchestration-demo` → `src/travel_plan_permission/orchestration/example.py` | Developers exercising LangGraph path | **Working (demo)** — optional `langgraph` extra; CI orchestration job `.github/workflows/ci.yml:61-87` |
| HTTP API — planner seam | `tpp-planner-service` → `src/travel_plan_permission/http_service.py`, `src/travel_plan_permission/planner_http_routes.py` | `trip-planner` and automation clients | **Working** — routes `/api/planner/*`, `/readyz`; contract in `docs/contracts/planner-integration.md` |
| Browser UI — portal | `/portal`, `/portal/draft/new`, `/portal/review/{draft_id}` in `src/travel_plan_permission/http_service.py` | Travelers, managers (demo/review) | **Working** — `http_service.py:1609, 1629, 1753`; `tests/python/test_portal_review.py` (README still documents stale `/portal/requests/new` at `README.md:94`) |
| Browser UI — handoff | `POST /portal/handoff` → `src/travel_plan_permission/portal_handoff.py` | `trip-planner` sending partial trip context | **Working** — restrictive cookie capability; `tests/python/test_portal_handoff.py` |
| Browser UI — expense portal | `/portal/expenses/new` in `src/travel_plan_permission/http_service.py` | Travelers submitting receipts post-trip | **Partial** — export path works (`docs/expense-workflow.md:26-31`); no ERP write-back (`docs/accounting-integration.md:39`) |
| Excel artifacts | `policy_api.fill_travel_spreadsheet`, `ExportService` | Travelers, accounting | **Working** — `src/travel_plan_permission/policy_api.py`, `src/travel_plan_permission/export.py`; golden tests under `tests/baseline/` |
| Static hosted demo | `render.yaml` + `src/travel_plan_permission/demo_seed.py` | Non-developer demo reviewers | **Working (synthetic only)** — `TPP_DEMO_MODE=1`; `docs/no-terminal-demo.md` |
| Documented but unwired REST API | `docs/security-model.md` tables for `/api/itineraries`, `/api/approvals/*` | N/A | **Scaffold** — permissions defined in `src/travel_plan_permission/security.py:84-100` but no matching route registration in `src/` |

## 3. Structure map

```
Travel-Plan-Permission/
├── src/travel_plan_permission/   # Core library: policy, portal, planner HTTP, persistence, orchestration
├── schemas/                      # Canonical JSON Schema for TripPlan and ExpenseReport
├── config/                       # YAML policy, approval rules, provider registry, Excel mappings
├── templates/                    # Organization Excel workbook templates (Jan 2026 revisions)
├── docs/                         # Runbooks, policy API, contracts (planner + backplane specs)
│   └── contracts/                # planner-integration, run-contract-v1, identity-map (mostly documented)
├── tests/                        # pytest suite, planner fixtures, golden approval baselines
├── scripts/                      # Schema validation, run-contract validator, complexity guard
├── tools/                        # CI helpers, optional LangChain client (not product runtime)
├── .github/                      # CI, gate, agent thin callers — largely synced from stranske/Workflows
└── design-system/                # UI assets (not central to current portal; server-rendered Jinja)
```

Boilerplate skipped above: `node_modules` under `.github/scripts/`, and workflow/prompt files managed via the Workflows sync manifest (`AGENTS.md:27-29`).

## 4. Major code features you must understand to extend it

- **Canonical TripPlan intake** — `load_trip_plan_input()` (`src/travel_plan_permission/canonical.py:219-226`) validates input against Pydantic model `CanonicalTripPlan` (aligned with `schemas/trip_plan.min.schema.json`) into a `TripPlanInput` dataclass holding `plan` (`TripPlan`) and `canonical` (`CanonicalTripPlan | None`); designated blessed loader per `Issues.txt:136-153` (Issue 4).
- **Policy-lite engine** — `PolicyEngine` (`src/travel_plan_permission/policy.py:459-570`) runs YAML rules from `config/policy.yaml` on `PolicyContext`; returns a list of blocking/advisory `PolicyResult` records.
- **Policy API façade** — `src/travel_plan_permission/policy_api.py` functions (`check_trip_plan`, `get_policy_snapshot`, `submit_proposal`, etc.) feed HTTP routes, portal review, and orchestration.
- **Spreadsheet pipeline** — `src/travel_plan_permission/workbook_population.py` / `src/travel_plan_permission/workbook_ooxml.py` fill `templates/*.xlsx` via `config/excel_mappings.yaml`; `UnfilledMappingReport` (`src/travel_plan_permission/policy_contract_models.py:515-531`) lists missing cells.
- **Planner HTTP + auth** — `src/travel_plan_permission/planner_http_routes.py` + `src/travel_plan_permission/planner_auth.py:24, 75-120` (bootstrap/static/OIDC bearer tokens).
- **Portal + handoff** — `src/travel_plan_permission/http_service.py`, `src/travel_plan_permission/portal_review.py`, `src/travel_plan_permission/portal_handoff.py` for draft/review/download; handoff cookie cannot submit (`README.md:148-153`).
- **Persistence** — `src/travel_plan_permission/persistence/resolver.py` → SQLite default, Postgres optional, legacy JSON import (`README.md:155-166`).
- **Post-trip approval** — `ApprovalEngine` (`src/travel_plan_permission/approval.py:10-40`) on `config/approval_rules.yaml`; used by `src/travel_plan_permission/expense_review.py:12-14`.
- **Orchestration** — `src/travel_plan_permission/orchestration/graph.py` deterministic LangGraph/fallback nodes; no LLM (`docs/ORCHESTRATION_PLAN.md:21-24`).
- **Audit + export** — `src/travel_plan_permission/audit.py:6-25` append-only events; `src/travel_plan_permission/export.py:18-35` CSV/XLSX accounting handoff (100-report cap).

## 5. Data model, identifiers and contracts

**Identifiers** are org-local: `trip_id` on `TripPlan`, plus `proposal_id` / `execution_id` for planner flows (`src/travel_plan_permission/policy_contract_models.py:231-233, 448-450`, `src/travel_plan_permission/planner_client.py:150-196`). Expense categories are a closed enum (`src/travel_plan_permission/models.py:26-34`), not fleet canonical IDs.

**Persistence:** portal state in SQLite/Postgres (`src/travel_plan_permission/persistence/resolver.py`); audit in SQLite (`src/travel_plan_permission/audit.py:6-9`); validation snapshots on disk by `trip_id` (`src/travel_plan_permission/snapshots.py:143-153`). Receipts reference files by `Receipt.file_reference` only (`src/travel_plan_permission/receipts.py:18-32`).

**Versioning:** policy snapshots use `PlannerVersionContract` / `PolicySnapshotFreshness`; `ValidationSnapshot` hash-chains runs (`src/travel_plan_permission/snapshots.py:49-65`).

**Shipped contracts and emit/consume status:**

| Contract | Location | Code status |
| --- | --- | --- |
| TripPlan minimal schema | `schemas/trip_plan.min.schema.json` | **Consumed** by `canonical.py`, validated in CI schema jobs |
| Planner integration v1 | `docs/contracts/planner-integration.md` + `tests/fixtures/planner_integration/` | **Emitted/consumed** — HTTP routes and `TravelPlanPermissionClient` |
| Expense report schema | `schemas/expense_report.min.schema.json` | **Contract schema** validated via external AJV CLI (`README.md:23-25`) against fixtures; `src/travel_plan_permission/models.py:563` implements an independent `ExpenseReport` Pydantic model (not consumed directly in Python) |
| run-contract/v1 | `docs/contracts/run-contract-v1.md` + `docs/contracts/schemas/` | **Documented only** — doc states “No participant emits an envelope yet” (`run-contract-v1.md:16-17`); validator exists (`scripts/validate_run_contract.py`) but `config/backplane_participants.json` is absent and no `run.json` emitter in `src/` |
| identity-map conventions | `docs/contracts/identity-map-conventions.md` | **Documented only** — no `identity_refs` emission in product code |
| evidence-object/v1 | `docs/contracts/schemas/evidence-object-v1.schema.json` | **Documented only** |
| capability-bundle/v1 | `docs/contracts/capability-bundle-v1.md` | **Documented only** (Workflows keepalive contract) |
| agent-runner-output | `docs/contracts/agent-runner-output.md` | **Consumed by CI/agent workflows**, not product runtime |

## 6. External inputs and dependencies

**Data sources.** User-supplied TripPlan JSON, receipt uploads (PDF/PNG/JPEG/HEIC per `src/travel_plan_permission/receipts.py:14-15`), and YAML/Excel configuration in `config/`. Demo mode seeds from `tests/fixtures/*.json` (`render.yaml:2-3`). No SEC filings, market data, or manager-database feeds.

**Sibling repo.** `trip-planner` is the primary external integrator; cross-repo smoke checks out a pinned SHA (`.github/trip-planner-pinned-ref`) and exercises handoff plus planner HTTP (`src/travel_plan_permission/cross_repo_smoke.py:31-38`).

**LLM/agent usage.** Product `src/` has no LangChain/OpenAI imports (`docs/ORCHESTRATION_PLAN.md:21`). LangGraph is an optional orchestration dependency (`pyproject.toml:51-53`). `tools/langchain_client.py` and `config/llm_slots.json` support CI/agent automation, not the travel portal runtime. Receipt OCR uses optional `pytesseract` (`pyproject.toml:47-50`, `src/travel_plan_permission/receipts.py:107-121`).

**Notable libraries.** FastAPI + Uvicorn (HTTP), Pydantic v2 (models), openpyxl (Excel), reportlab (approval PDFs), PyJWT (auth), Jinja2 (portal HTML), httpx (planner client).

**Deployment modes.** Local CLI needs Python 3.12+ install (`pyproject.toml:7`). HTTP service needs a running process (or Render web service). Public demo is browser-only with synthetic data. Postgres requires `psycopg` extra. OCR requires system Tesseract plus `ocr` extra. No Docker compose in this repo’s product path (Render uses `pip install -e .`).

## 7. Current state

**Test/CI posture.** Default pytest excludes `perf` markers, enforces ≥80% coverage (`pyproject.toml:91-118`). `ci.yml` delegates lint/typecheck/test to `stranske/Workflows` reusable Python CI, adds module-size and complexity guards, LangGraph orchestration tests, and a cross-repo smoke job against pinned `trip-planner`. `pr-00-gate.yml` aggregates required checks for PR keepalive. Schema validation uses AJV (`README.md:17-26`). Package classifiers mark **Alpha** (`pyproject.toml:11`).

**Production-usable vs prototype.** Deterministic policy checks, spreadsheet generation, planner HTTP contract, portal draft/review, audit export, and accounting CSV/XLSX export appear production-grade with broad test coverage. Prototype or bounded: public Render demo (synthetic only), optional OCR, LangGraph orchestration (deterministic nodes only), backplane run envelopes, ERP integration, and the documented `/api/itineraries` REST surface.

**Consequential gaps (cited):** no `run.json` emitter (`docs/contracts/run-contract-v1.md:15-17`, `.github/workflows/backplane-conformance.yml:54`); missing `config/backplane_participants.json`; security-model REST routes documented but unwired (`docs/security-model.md:17-27` vs `src/travel_plan_permission/planner_http_routes.py`); LLM/vendor search not implemented (`docs/ORCHESTRATION_PLAN.md:21-22`); accounting export-only (`docs/accounting-integration.md:39`); workflow sync open (`Issues.txt:264-269`); stale Issues.txt orchestration checkbox (`Issues.txt:112-114` vs `.github/workflows/ci.yml:61-87`); alpha classifier (`pyproject.toml:11`).

## 8. Claims vs reality

- **“Full pre-trip and post-trip experience”** (`docs/ORCHESTRATION_PLAN.md:9`) — Documented as an explicit **long-term vision/goal** rather than a claim of current operational capability. Current runtime is deterministic (policy check, spreadsheet population, review portal, accounting export); LLM intake, vendor search, graph OCR, and ERP writes are explicitly unbuilt (`docs/ORCHESTRATION_PLAN.md:12, 21-24`, `docs/accounting-integration.md:39`).
- **Security REST API** (`docs/security-model.md:17-27`) — permissions in `src/travel_plan_permission/security.py:84-100` only; no `/api/itineraries` or `/api/approvals/*` route handlers in `src/`.
- **Backplane runs** — validator + docs exist; no `config/backplane_participants.json`, no emitter (`docs/contracts/run-contract-v1.md:15-17`, `.github/workflows/backplane-conformance.yml:54`).
- **Receipt OCR** — `extract_from_image` in `src/travel_plan_permission/receipts.py:107-121` exists behind optional `ocr` extra, but orchestration never calls it (`docs/ORCHESTRATION_PLAN.md:23`), and expense review only parses pre-extracted `ocr_text` strings (`src/travel_plan_permission/expense_review.py:38-40`).
- **Issues.txt orchestration CI** (`Issues.txt:112-114`) stale vs `.github/workflows/ci.yml:61-87`.
- **OIDC** supported in code (`src/travel_plan_permission/planner_auth.py:24`) but public demo uses bootstrap tokens (`render.yaml:22-23`).

## 9. Interoperability hooks (for the fleet program)

**What TPP can OFFER to siblings**

| Artifact | Schema / type | Provenance |
| --- | --- | --- |
| Canonical TripPlan JSON | `schemas/trip_plan.min.schema.json` | Source document = user/planner input |
| Policy evaluation result | `PlannerProposalEvaluationResult` (`src/travel_plan_permission/policy_contract_models.py:444`) | Tied to `execution_id`, policy version |
| Policy snapshot | `PlannerPolicySnapshot` (`src/travel_plan_permission/policy_contract_models.py:136`) | Versioned rules + requirements list |
| Planner proposal lifecycle IDs | `proposal_id`, `execution_id`, `trip_id` | HTTP contract (`docs/contracts/planner-integration.md`) |
| Excel travel workbook bytes | Org template via `fill_travel_spreadsheet` | Mapped cells from `config/excel_mappings.yaml` |
| Expense export batch | CSV/XLSX via `ExportService.schema` | `docs/accounting-integration.md` column order |
| Audit events CSV | `audit.py` `CSV_FIELDS` | Actor, event type, target_id |
| Validation snapshots | `ValidationSnapshot` JSON files | `trip_id` + `policy_version` hash chain |

**What TPP would CONSUME**

- Partial trip context from `trip-planner` via `POST /portal/handoff` (`src/travel_plan_permission/portal_handoff.py`).
- Planner proposal payloads conforming to `tests/fixtures/planner_integration/proposal_submission.json`.
- Receipt metadata and optional OCR text into `Receipt` / `ExpenseItem` models (`src/travel_plan_permission/receipts.py:18-32`, `src/travel_plan_permission/models.py:519-537`).
- Sibling integration: runtime consumption by `trip-planner` of planner HTTP API and handoff cookie capability.

**Collision risks with siblings**

- `trip_id` is a free-form string on `TripPlan`, not a fleet `manager:cik_*` or `fund:lei_*` canonical ID (`docs/contracts/identity-map-conventions.md` vocabulary does not appear in TPP models).
- `ExpenseCategory` enum (`airfare`, `lodging`, etc.) may not align with accounting or pension-data taxonomies.
- `cost_center` is a plain string on `CanonicalTripPlan` and `ExpenseReport`, not a fleet registry field (`src/travel_plan_permission/canonical.py:103`, `src/travel_plan_permission/models.py:569`).
- Policy version strings are TPP-local (`PolicyVersion` in `src/travel_plan_permission/policy_versioning.py`), not synchronized with external policy-management systems.
- Public demo fixtures must never be confused with production entity data (`render.yaml:1-6`).

## 10. Reuse candidates

- `src/travel_plan_permission/canonical.py` — canonical JSON → typed model conversion with validation.
- `src/travel_plan_permission/policy.py` + `config/policy.yaml` — configurable rule engine pattern.
- `src/travel_plan_permission/policy_api.py` — stable façade for orchestration and HTTP adapters.
- `src/travel_plan_permission/workbook_population.py` + `src/travel_plan_permission/workbook_ooxml.py` — template-driven Excel population with unfilled-cell reporting.
- `src/travel_plan_permission/planner_client.py` — typed HTTP client with polling semantics for long-running policy evaluations.
- `src/travel_plan_permission/persistence/` — SQLite/Postgres/JSON portal store with legacy import.
- `src/travel_plan_permission/audit.py` — append-only audit log with retention pruning.
- `src/travel_plan_permission/snapshots.py` — hash-chained validation snapshots for regression replay.
- `src/travel_plan_permission/export.py` — accounting export with pluggable receipt URL signing.
- `src/travel_plan_permission/approval.py` — YAML-driven threshold approval engine.
- `scripts/validate_run_contract.py` — backplane envelope validator (when emission is added).

## 11. Proposed direction (evidence-based)

**Finish scaffolded:** align or delete security-model REST docs with actual routes; add backplane registry + reference-run emitter; sync Workflows (`Issues.txt:264-269`); wire portal OCR if promised (`docs/expense-workflow.md:11`).

**New capability:** emit `run-contract/v1` from planner executions; ERP write adapter after export schema freezes (`docs/accounting-integration.md:39`); LLM nodes only after privacy boundary (`docs/ORCHESTRATION_PLAN.md:24`); enterprise OIDC templates beyond demo (`render.yaml`).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- This tool enforces your organization’s travel policy and fills the official Excel travel form from structured trip data, so approvals start from a consistent, checkable packet rather than ad hoc emails.
- The main live integration is with the separate trip-planning app: that app sends trip details in; this repo checks policy, hosts the review portal, and returns approval readiness—not flight booking.
- Real employee travel data should stay on internal or on-prem deployments; the public website is a synthetic demo only and must not receive production trips or receipts.
- Post-trip reimbursement today means generating accounting-ready spreadsheets and tracking review status; it does not automatically post into your general ledger or expense system yet.
- The codebase is actively tested (high coverage, cross-repo smoke with the companion trip planning application) but still labeled alpha: some documentation describes future REST APIs and fleet-wide run records that are not fully wired.

Verified 2026-09-04T23:23:20Z by composer: 54 claims checked, 9 corrected, 1 unverifiable.
