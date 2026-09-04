# Travel-Plan-Permission dossier — verification table

Verified against clone `clones/Travel-Plan-Permission` at HEAD `d67298fb1928ffd6084602a0b3454bc190ed79cf` (2026-09-04).
Method: every cited file:line/symbol opened and verified against current code and documentation.
Attempt 2 resumed from retained artifact; prior pass corrections re-checked and five additional citation/claim defects found.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 44 |
| WRONG (corrected in dossier) | 9 |
| UNVERIFIABLE | 1 |
| **Total checked** | **54** |

### Key Findings & Corrections

1. **§4 Canonical intake Issues.txt cite:** Retained dossier cited `Issues.txt:29-50` for Issue 4 blessed loader. Lines 29-50 are Issue 1 acceptance criteria; Issue 4 and the `load_trip_plan_input()` designation are at `Issues.txt:136-153`.
2. **§2 Portal new-request route:** Registered route is `GET /portal/draft/new` (`http_service.py:1629`), not `/portal/requests/new`. README still documents the stale path at `README.md:94`.
3. **§5 ExpenseReport model line cite:** `ExpenseReport` is defined at `models.py:563`, not `models.py:321` (which is `TripPlan.trip_id`). Consumption status ("Contract schema", not Python-consumed) remains correct.
4. **§5 Identifiers citation mismatch (retained from prior pass):** `planner_client.py:71-78` holds retry exception attributes, not `proposal_id`/`execution_id`. Identifiers are on `policy_contract_models.py:231-233, 448-450` and used in `planner_client.py:150-196`.
5. **§4 Canonical intake return type (retained from prior pass):** `load_trip_plan_input()` validates via Pydantic `CanonicalTripPlan` and returns `TripPlanInput`, not a raw `TripPlan` + `CanonicalTripPlan` pair.
6. **§5 Expense report schema consumption (retained from prior pass):** No Python module loads `schemas/expense_report.min.schema.json`; AJV CLI validates it externally.
7. **§8 "Full pre-trip and post-trip experience" framing (retained from prior pass):** `ORCHESTRATION_PLAN.md:9` labels this as a long-term goal, not a current-capability claim; refuting it as operational overclaim was inaccurate.
8. **§9 cost_center collision risk:** `cost_center` is a plain string on `CanonicalTripPlan` (`canonical.py:103`) and `ExpenseReport` (`models.py:569`), not on `TripPlan` (`models.py:321` is `trip_id`).
9. **§9 Receipt consume cite:** Receipt/ExpenseItem parsing cites corrected from `models.py:250-280` (exception-approval code) to `receipts.py:18-32` and `models.py:519-537`.

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | `load_trip_plan_input()` validates canonical intake via Pydantic `CanonicalTripPlan`; returns `TripPlanInput`; blessed loader per Issues.txt Issue 4 | `src/travel_plan_permission/canonical.py:219-226`, `Issues.txt:136-153` | **WRONG** | Function behavior confirmed. Blessed-loader designation is Issue 4 at `Issues.txt:136-153`, not lines 29-50 (Issue 1 acceptance criteria). |
| 2 | `PolicyEngine` runs YAML rules from `config/policy.yaml` on `PolicyContext`; returns blocking/advisory `PolicyResult` | `src/travel_plan_permission/policy.py:459-570`, `config/policy.yaml:1-32` | CONFIRMED | `PolicyEngine.validate(context)` executes configured rules and returns `list[PolicyResult]`. |
| 3 | `policy_api.py` functions feed HTTP routes, portal review, and orchestration | `src/travel_plan_permission/policy_api.py` | CONFIRMED | Façade functions present and reused across HTTP handlers, portal review, and orchestration graphs. |
| 4 | `workbook_population.py` / `workbook_ooxml.py` fill templates via `config/excel_mappings.yaml`; `UnfilledMappingReport` lists missing cells | `src/travel_plan_permission/workbook_population.py`, `src/travel_plan_permission/policy_contract_models.py:515-531` | CONFIRMED | Populates template cells; `UnfilledMappingReport` records unmapped cells, dropdowns, and checkboxes. |
| 5 | `planner_http_routes.py` + `planner_auth.py` (bootstrap/static/OIDC bearer tokens) | `src/travel_plan_permission/planner_http_routes.py`, `src/travel_plan_permission/planner_auth.py:24, 75-120` | CONFIRMED | Bearer token verification with bootstrap-token, static, and OIDC modes (Azure AD, Okta, Google). |
| 6 | `http_service.py`, `portal_review.py`, `portal_handoff.py` for draft/review/download; handoff cookie cannot submit | `README.md:148-153`, `src/travel_plan_permission/portal_handoff.py` | CONFIRMED | Handoff capability cookie rejects `/portal/submit/{draft_id}`. |
| 7 | `persistence/resolver.py` → SQLite default, Postgres optional, legacy JSON import | `README.md:155-166`, `src/travel_plan_permission/persistence/resolver.py` | CONFIRMED | Default SQLite at `var/portal-runtime-state.sqlite3`; Postgres via `TPP_PORTAL_DATABASE_URL`. |
| 8 | `ApprovalEngine` on `config/approval_rules.yaml`; used by `expense_review.py` | `src/travel_plan_permission/approval.py:41-67`, `src/travel_plan_permission/expense_review.py:12-14` | CONFIRMED | `ApprovalEngine` starts at line 41; imported and used by expense review workflow. |
| 9 | `orchestration/graph.py` deterministic LangGraph/fallback nodes; no LLM | `src/travel_plan_permission/orchestration/graph.py`, `docs/ORCHESTRATION_PLAN.md:21-24` | CONFIRMED | Deterministic nodes only; `STATUS:NOT_IMPLEMENTED` for LLM/vendor/OCR graph nodes. |
| 10 | `audit.py` append-only events; `export.py` CSV/XLSX accounting handoff (100-report cap) | `src/travel_plan_permission/audit.py:6-25`, `src/travel_plan_permission/export.py:18-35` | CONFIRMED | Append-only audit module doc + `ExportService._validate_batch` 100-report cap. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 11 | Identifiers are org-local: `trip_id` on `TripPlan`, plus `proposal_id` / `execution_id` for planner flows; closed `ExpenseCategory` enum | `src/travel_plan_permission/policy_contract_models.py:231-233, 448-450`, `src/travel_plan_permission/models.py:26-34` | **WRONG** | Identifier fields confirmed on contract models and client methods. Prior cite `planner_client.py:71-78` was incorrect. |
| 12 | Persistence: portal state in SQLite/Postgres; audit in SQLite; validation snapshots on disk by `trip_id`; receipts reference files by `Receipt.file_reference` | `src/travel_plan_permission/persistence/resolver.py`, `src/travel_plan_permission/audit.py:6-9`, `src/travel_plan_permission/snapshots.py:143-153`, `src/travel_plan_permission/receipts.py:18-32` | CONFIRMED | All storage mechanisms confirmed. |
| 13 | Versioning: policy snapshots use `PlannerVersionContract` / `PolicySnapshotFreshness`; `ValidationSnapshot` hash-chains runs | `src/travel_plan_permission/snapshots.py:49-65` | CONFIRMED | `ValidationSnapshot` maintains `previous_hash` and `chain_hash`. |
| 14 | TripPlan minimal schema consumed by `canonical.py`, validated in CI schema jobs | `schemas/trip_plan.min.schema.json`, `src/travel_plan_permission/canonical.py` | CONFIRMED | `CanonicalTripPlan` pydantic model implements the schema; AJV CLI validates fixtures in CI. |
| 15 | Planner integration v1 emitted/consumed — HTTP routes and `TravelPlanPermissionClient` | `docs/contracts/planner-integration.md`, `src/travel_plan_permission/planner_http_routes.py`, `src/travel_plan_permission/planner_client.py` | CONFIRMED | Full client and server implementations for planner HTTP contract. |
| 16 | Expense report schema consumed in models/tests | `schemas/expense_report.min.schema.json`, `src/travel_plan_permission/models.py:563` | **WRONG** | Schema not loaded by Python; `ExpenseReport` at `models.py:563` is independent Pydantic model. AJV CLI validates schema externally. |
| 17 | run-contract/v1 documented only — no emitter, no `config/backplane_participants.json` | `docs/contracts/run-contract-v1.md:15-17`, `scripts/validate_run_contract.py`, `.github/workflows/backplane-conformance.yml:54` | CONFIRMED | Doc line 16: "No participant emits an envelope yet"; participants file absent; CI echoes no emitter. |
| 18 | identity-map conventions documented only — no `identity_refs` emission in product code | `docs/contracts/identity-map-conventions.md` | CONFIRMED | No `identity_refs` in `src/`. |
| 19 | evidence-object/v1 documented only | `docs/contracts/schemas/evidence-object-v1.schema.json` | CONFIRMED | Schema present; no generator in `src/`. |
| 20 | capability-bundle/v1 documented only (Workflows keepalive contract) | `docs/contracts/capability-bundle-v1.md` | CONFIRMED | Documented; not referenced in runtime code. |
| 21 | agent-runner-output consumed by CI/agent workflows, not product runtime | `docs/contracts/agent-runner-output.md` | CONFIRMED | Workflows specification; not product runtime. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement |
|---|---|---|---|---|
| 22 | **Claim: "Full pre-trip and post-trip experience"** | `docs/ORCHESTRATION_PLAN.md:7-12, 21-24`, `docs/accounting-integration.md:39` | **WRONG (claim framing)** | Line 9 is an explicit long-term goal; lines 12 and 21-24 mark LLM/vendor/OCR as `STATUS:NOT_IMPLEMENTED`. Framing as operational overclaim mischaracterizes a documented roadmap goal. |
| 23 | **Claim: Security REST API** | `docs/security-model.md:17-27`, `src/travel_plan_permission/security.py:84-100` | CONFIRMED | Permissions defined for `/api/itineraries` and `/api/approvals/*`; no matching route handlers in `src/`. |
| 24 | **Claim: Backplane runs** | `docs/contracts/run-contract-v1.md:15-17`, `.github/workflows/backplane-conformance.yml:54` | CONFIRMED | No emitter wired; participants registry absent. |
| 25 | **Claim: Receipt OCR** | `src/travel_plan_permission/receipts.py:107-121`, `docs/ORCHESTRATION_PLAN.md:23`, `src/travel_plan_permission/expense_review.py:38-40` | CONFIRMED | `extract_from_image` exists behind optional `ocr` extra; orchestration never calls it; expense review parses pre-extracted `ocr_text` only. |
| 26 | **Claim: Issues.txt orchestration CI** | `Issues.txt:112-114`, `.github/workflows/ci.yml:61-87` | CONFIRMED | Issues.txt checkbox still open; `orchestration` CI job already installs `.[orchestration]` and runs LangGraph tests. |
| 27 | **Claim: OIDC** | `src/travel_plan_permission/planner_auth.py:24`, `render.yaml:22-23` | CONFIRMED | OIDC providers supported in code; public Render demo uses `bootstrap-token`. |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 28 | Offer: Canonical TripPlan JSON | `schemas/trip_plan.min.schema.json` | CONFIRMED | Canonical JSON schema for trip intake. |
| 29 | Offer: Policy evaluation result | `src/travel_plan_permission/policy_contract_models.py:444` | CONFIRMED | `PlannerProposalEvaluationResult` at line 444. |
| 30 | Offer: Policy snapshot | `src/travel_plan_permission/policy_contract_models.py:136` | CONFIRMED | `PlannerPolicySnapshot` at line 136. |
| 31 | Offer: Planner proposal lifecycle IDs | `docs/contracts/planner-integration.md` | CONFIRMED | `proposal_id`, `execution_id`, `trip_id` enforced across HTTP handshake. |
| 32 | Offer: Excel travel workbook bytes | `src/travel_plan_permission/policy_api.py`, `config/excel_mappings.yaml` | CONFIRMED | Populated `.xlsx` via template mappings. |
| 33 | Offer: Expense export batch | `src/travel_plan_permission/export.py:20`, `docs/accounting-integration.md` | CONFIRMED | `ExportService.schema` defines 6-column export order. |
| 34 | Offer: Audit events CSV | `src/travel_plan_permission/audit.py:80-90` | CONFIRMED | `CSV_FIELDS` defines 9-column audit export schema. |
| 35 | Offer: Validation snapshots | `src/travel_plan_permission/snapshots.py:49-65` | CONFIRMED | Hash-chained `ValidationSnapshot` records. |
| 36 | Consume: Partial trip context from `trip-planner` | `src/travel_plan_permission/portal_handoff.py` | CONFIRMED | `POST /portal/handoff` issues draft-scoped capability cookie. |
| 37 | Consume: Planner proposal payloads | `tests/fixtures/planner_integration/proposal_submission.json` | CONFIRMED | Fixture matches planner submission contract. |
| 38 | Consume: Receipt metadata and optional OCR text | `src/travel_plan_permission/receipts.py:18-32`, `src/travel_plan_permission/models.py:519-537` | **WRONG** | Claim confirmed; prior cite `models.py:250-280` pointed at exception-approval code, not `ExpenseItem`/`Receipt`. |
| 39 | Consume: Sibling integration with `trip-planner` | `docs/contracts/planner-integration.md`, `src/travel_plan_permission/cross_repo_smoke.py` | **UNVERIFIABLE (off-clone runtime)** | Contracts and smoke scaffolding exist; live end-to-end with sibling requires external checkout and running services. |
| 40 | Collision risk: `trip_id` is a free-form string, not a fleet canonical ID | `src/travel_plan_permission/models.py:321`, `docs/contracts/identity-map-conventions.md` | CONFIRMED | No fleet canonical entity syntax in models. |
| 41 | Collision risk: `ExpenseCategory` enum may not align with external taxonomies | `src/travel_plan_permission/models.py:26-34` | CONFIRMED | Closed 6-member StrEnum. |
| 42 | Collision risk: `cost_center` is a plain string without shared registry | `src/travel_plan_permission/canonical.py:103`, `src/travel_plan_permission/models.py:569` | **WRONG** | Prior claim "on TripPlan" was incorrect; field is on `CanonicalTripPlan` and `ExpenseReport`, not `TripPlan`. |
| 43 | Collision risk: Policy version strings are TPP-local | `src/travel_plan_permission/policy_versioning.py:49-75` | CONFIRMED | `PolicyVersion` is repo-local semantic versioning. |
| 44 | Collision risk: Public demo fixtures must not be confused with production data | `render.yaml:1-6` | CONFIRMED | `render.yaml` header marks synthetic-only deployment. |

---

## §1, §2, §3, §6, §7, §10, §11 — Supporting Claims

| # | Section | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|---|
| 45 | §1 | Purpose and reproducible workflow | `README.md:5-6`, `pyproject.toml:62` | CONFIRMED | README purpose and `tpp-planner-service` entry point. |
| 46 | §2 | CLI spreadsheet fill entry point | `src/travel_plan_permission/cli.py`, `README.md:35-41`, `tests/python/test_cli.py` | CONFIRMED | Console script `fill-spreadsheet` mapped to `cli:main`. |
| 47 | §2 | Cross-repo smoke CI job | `.github/workflows/ci.yml:89-236` | CONFIRMED | Job `cross-repo-smoke` checks out pinned `trip-planner` SHA. |
| 48 | §2 | Portal and demo review endpoints | `http_service.py:1609, 1629, 1753`, `tests/python/test_portal_review.py` | **WRONG** | Routes are `/portal`, `/portal/draft/new`, `/portal/review/{draft_id}`; README still documents stale `/portal/requests/new`. |
| 49 | §3 | Sync manifest management for CI workflows | `AGENTS.md:27-29` | CONFIRMED | Synced workflows managed via `.github/sync-manifest.yml` in Workflows. |
| 50 | §6 | Dependencies: Python 3.12+, FastAPI, openpyxl, reportlab, optional langgraph, psycopg, pytesseract | `pyproject.toml:7, 19-56` | CONFIRMED | Declared in project core and optional dependency sections. |
| 51 | §6 | Receipt allowed formats: PDF, PNG, JPEG, HEIC, 10MB limit | `src/travel_plan_permission/receipts.py:14-15` | CONFIRMED | `ALLOWED_RECEIPT_TYPES` and `MAX_RECEIPT_SIZE_BYTES` match. |
| 52 | §7 | CI gate aggregation and test coverage: ≥80% branch coverage, Alpha classifier | `pyproject.toml:11, 104-118` | CONFIRMED | Alpha classifier; `fail_under = 80` with `branch = true`. |
| 53 | §7 | Backplane conformance emitter placeholder | `.github/workflows/backplane-conformance.yml:54` | CONFIRMED | Echoes "No emitter wired yet; the conformance gate will skip (opt-in)." |
| 54 | §11 | Proposed direction: workflow sync open, expense portal export-only | `Issues.txt:264-269`, `docs/accounting-integration.md:39` | CONFIRMED | Open sync task; export-only boundary documented. |
