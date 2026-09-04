# Travel-Plan-Permission dossier — verification table

Verified against clone `clones/Travel-Plan-Permission` at HEAD `d67298fb1928ffd6084602a0b3454bc190ed79cf` (2026-09-04).
Method: every cited file:line/symbol opened and verified against current code and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 49 |
| WRONG (corrected in dossier) | 4 |
| UNVERIFIABLE | 1 |
| **Total checked** | **54** |

### Key Findings & Corrections

1. **§4 Canonical intake return type and validation mechanism:** The dossier stated that `load_trip_plan_input()` validates `schemas/trip_plan.min.schema.json` into `TripPlan` + `CanonicalTripPlan`. Opening `src/travel_plan_permission/canonical.py:219-226` shows that it validates against the Pydantic model `CanonicalTripPlan` (aligned with `schemas/trip_plan.min.schema.json`) rather than directly executing JSON Schema validation, and returns a `TripPlanInput` dataclass holding `plan: TripPlan` and `canonical: CanonicalTripPlan | None` (rather than a tuple or raw model pair). Blessed loader designated in `Issues.txt:29-50` (Issue 4).
2. **§5 Identifiers citation mismatch:** The dossier cited `planner_client.py:71-78` for `proposal_id` and `execution_id`. In `src/travel_plan_permission/planner_client.py`, lines 71-78 contain retry exception attributes (`self.attempts = attempts`) and `urllib_transport()`. The identifiers `proposal_id` and `execution_id` are defined on contract models in `src/travel_plan_permission/policy_contract_models.py:231-233, 448-450` (`PlannerProposalSubmissionResponse` and `PlannerProposalEvaluationResult`) and used as parameters in client methods in `src/travel_plan_permission/planner_client.py:150-196` (`get_proposal_execution`, `get_evaluation_result`, `poll_proposal_execution`).
3. **§5 Expense report schema consumption:** The dossier table marked `schemas/expense_report.min.schema.json` as **Consumed** in models/tests. Inspection across all Python files confirms that no Python module loads, parses, or validates `schemas/expense_report.min.schema.json`. `ExpenseReport` in `src/travel_plan_permission/models.py:321` is an independent Pydantic model. The JSON Schema file is instead validated via external Node AJV CLI tooling per `README.md:23, 25` against `tests/fixtures/sample_expense_report_minimal.json`.
4. **§8 "Full pre-trip and post-trip experience" claim framing (adversarial check):** The dossier refuted `ORCHESTRATION_PLAN.md:9` by treating "Full pre-trip and post-trip experience" as an operational overclaim contradicted by missing LLM, vendor search, and ERP write functionality. Opening `docs/ORCHESTRATION_PLAN.md:7-12` reveals that line 9 explicitly labels this as a **"Long-term"** goal, contrasted with short-term template filling (line 10), and line 12 explicitly confirms that LLM agents, vendor search, and graph OCR are "planned capabilities, not implemented runtime behavior" (marked `STATUS:NOT_IMPLEMENTED` in lines 21-24). Refuting a documented roadmap goal as a false capability claim was an inaccurate refutation; the corrected dossier frames this as a documented scope boundary rather than an unfulfilled claim.
5. **§12 Bullet 5 code identifier cleanup:** Removed the hyphenated repository identifier `trip-planner` from bullet 5 to strictly honor the section rule ("5 bullets, no code identifiers").

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | `load_trip_plan_input()` validates `schemas/trip_plan.min.schema.json` into `TripPlan` + `CanonicalTripPlan`; blessed loader per `Issues.txt` Issue 4 | `src/travel_plan_permission/canonical.py:219-226`, `Issues.txt:29-50` | **WRONG** | Validates incoming payload against Pydantic model `CanonicalTripPlan` (aligned with schema) and returns a `TripPlanInput` dataclass containing `plan: TripPlan` and `canonical: CanonicalTripPlan \| None`. Designated blessed loader in `Issues.txt:29-50`. |
| 2 | `PolicyEngine` runs YAML rules from `config/policy.yaml` on `PolicyContext`; returns blocking/advisory `PolicyResult` | `src/travel_plan_permission/policy.py:42-50, 459-570`, `config/policy.yaml:1-32` | CONFIRMED | `PolicyEngine.validate(context)` executes configured rules and returns `list[PolicyResult]` each containing rule ID, severity, passed boolean, and message. |
| 3 | `policy_api.py` functions (`check_trip_plan`, `get_policy_snapshot`, `submit_proposal`, etc.) feed HTTP routes, portal review, and orchestration | `src/travel_plan_permission/policy_api.py:1-50, 484, 820, 1145` | CONFIRMED | Façade functions present, well-typed, and reused across HTTP handlers, portal review, and orchestration graphs. |
| 4 | `workbook_population.py` / `workbook_ooxml.py` fill `templates/*.xlsx` via `config/excel_mappings.yaml`; `UnfilledMappingReport` lists missing cells | `src/travel_plan_permission/workbook_population.py:15-43`, `src/travel_plan_permission/workbook_ooxml.py:1-40`, `config/excel_mappings.yaml:1-30`, `src/travel_plan_permission/policy_contract_models.py:515-531` | CONFIRMED | Populates template cells while preserving formulas/styles; `UnfilledMappingReport` records unmapped cells, dropdowns, and checkboxes. |
| 5 | `planner_http_routes.py` + `planner_auth.py` (bootstrap/static/OIDC bearer tokens) | `src/travel_plan_permission/planner_http_routes.py:1-30`, `src/travel_plan_permission/planner_auth.py:24, 75-120` | CONFIRMED | Implements bearer token verification with three configurable auth modes: bootstrap-token, static, and OIDC (Azure AD, Okta, Google). |
| 6 | `http_service.py`, `portal_review.py`, `portal_handoff.py` for draft/review/download; handoff cookie cannot submit | `README.md:148-153`, `src/travel_plan_permission/portal_handoff.py:1-40`, `src/travel_plan_permission/portal_review.py:1-35` | CONFIRMED | Portal endpoints support draft review and spreadsheet download; `/portal/handoff` issues HttpOnly capability cookie that rejects `/portal/submit/{draft_id}`. |
| 7 | `persistence/resolver.py` → SQLite default, Postgres optional, legacy JSON import | `README.md:155-166`, `src/travel_plan_permission/persistence/resolver.py:1-50` | CONFIRMED | Default SQLite store at `var/portal-runtime-state.sqlite3`, Postgres via `TPP_PORTAL_DATABASE_URL`, automatic one-time migration from legacy JSON. |
| 8 | `ApprovalEngine` (`approval.py`) on `config/approval_rules.yaml`; used by `expense_review.py` | `src/travel_plan_permission/approval.py:10-40`, `config/approval_rules.yaml:1-14`, `src/travel_plan_permission/expense_review.py:12-14` | CONFIRMED | Rules evaluated by category and amount threshold; imported and called by expense review workflow. |
| 9 | `orchestration/graph.py` deterministic LangGraph/fallback nodes; no LLM | `src/travel_plan_permission/orchestration/graph.py:1-50`, `docs/ORCHESTRATION_PLAN.md:21-24` | CONFIRMED | LangGraph graph compiles when library is present; deterministic fallback executor executes nodes when absent; zero LLM calls in runtime. |
| 10 | `audit.py` append-only events; `export.py` CSV/XLSX accounting handoff (100-report cap) | `src/travel_plan_permission/audit.py:6-25`, `src/travel_plan_permission/export.py:18-35` | CONFIRMED | SQLite append-only audit events table; `ExportService._validate_batch` raises `ValueError` if report count exceeds 100. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 11 | Identifiers are org-local: `trip_id` on `TripPlan`, plus `proposal_id` / `execution_id` for planner flows; closed `ExpenseCategory` enum | `src/travel_plan_permission/planner_client.py:71-78`, `src/travel_plan_permission/models.py:26-34` | **WRONG** | `planner_client.py:71-78` cites `attempts` and `urllib_transport`. Identifiers `proposal_id` and `execution_id` are defined in `src/travel_plan_permission/policy_contract_models.py:231-233, 448-450` and used in `src/travel_plan_permission/planner_client.py:150-196`. `ExpenseCategory` enum confirmed in `models.py:26-34`. |
| 12 | Persistence: portal state in SQLite/Postgres; audit in SQLite; validation snapshots on disk by `trip_id`; receipts reference files by `Receipt.file_reference` | `src/travel_plan_permission/persistence/resolver.py:1-50`, `src/travel_plan_permission/audit.py:6-9`, `src/travel_plan_permission/snapshots.py:143-153`, `src/travel_plan_permission/receipts.py:18-32` | CONFIRMED | All storage mechanisms confirmed; `Receipt` model in `receipts.py:18-32` stores `file_reference: str` with allowed extension validation. |
| 13 | Versioning: policy snapshots use `PlannerVersionContract` / `PolicySnapshotFreshness`; `ValidationSnapshot` hash-chains runs | `src/travel_plan_permission/snapshots.py:49-65`, `src/travel_plan_permission/policy_contract_models.py:136-155` | CONFIRMED | `ValidationSnapshot` maintains `previous_hash` and `chain_hash`; policy snapshot models track version contract and freshness enum. |
| 14 | TripPlan minimal schema consumed by `canonical.py`, validated in CI schema jobs | `schemas/trip_plan.min.schema.json`, `src/travel_plan_permission/canonical.py:98-121`, `README.md:17-26` | CONFIRMED | `CanonicalTripPlan` pydantic model implements the schema; AJV CLI validates schema against fixtures in CI. |
| 15 | Planner integration v1 emitted/consumed — HTTP routes and `TravelPlanPermissionClient` | `docs/contracts/planner-integration.md`, `src/travel_plan_permission/planner_http_routes.py`, `src/travel_plan_permission/planner_client.py:97` | CONFIRMED | Full client and server implementations for policy snapshot, proposal submission, execution status, and evaluation results. |
| 16 | Expense report schema consumed in models/tests | `schemas/expense_report.min.schema.json`, `src/travel_plan_permission/models.py:321` | **WRONG** | `schemas/expense_report.min.schema.json` is not consumed or loaded by any Python file in `models` or `tests`. `models.py:321` defines `ExpenseReport` as an independent Pydantic model. Schema is validated using external AJV CLI per `README.md:23, 25`. |
| 17 | run-contract/v1 documented only — doc states “No participant emits an envelope yet”; validator exists but `config/backplane_participants.json` absent and no emitter in `src/` | `docs/contracts/run-contract-v1.md:15-17`, `scripts/validate_run_contract.py:1-20`, `.github/workflows/backplane-conformance.yml:54` | CONFIRMED | Opt-in doc explicit on line 16; validator exists; backplane participants file absent; CI backplane step confirms no emitter wired. |
| 18 | identity-map conventions documented only — no `identity_refs` emission in product code | `docs/contracts/identity-map-conventions.md:1-15` | CONFIRMED | Convention doc present; no entity ID translation or `identity_refs` field emitted anywhere in `src/`. |
| 19 | evidence-object/v1 documented only | `docs/contracts/schemas/evidence-object-v1.schema.json:1-20` | CONFIRMED | Satellite schema present in documentation tree; no evidence object generator or serializer in `src/`. |
| 20 | capability-bundle/v1 documented only (Workflows keepalive contract) | `docs/contracts/capability-bundle-v1.md:1-12` | CONFIRMED | Keepalive contract specification documented; not referenced in runtime code. |
| 21 | agent-runner-output consumed by CI/agent workflows, not product runtime | `docs/contracts/agent-runner-output.md:1-15` | CONFIRMED | Workflows runner specification; consumed by automation scripts, not runtime application. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement |
|---|---|---|---|---|
| 22 | **Claim: “Full pre-trip and post-trip experience”** | `docs/ORCHESTRATION_PLAN.md:7-12, 21-24`, `docs/accounting-integration.md:39` | **WRONG (claim framing)** | `ORCHESTRATION_PLAN.md:9` explicitly defines this as an explicit **"Long-term"** goal, not an assertion of current operational capability. In fact, line 12 and lines 21-24 explicitly declare LLM agents, vendor search, and graph OCR as `STATUS:NOT_IMPLEMENTED`. The operational boundary described is accurate, but framing it as an overclaim refuted by reality mischaracterizes a documented roadmap goal. |
| 23 | **Claim: Security REST API** | `docs/security-model.md:17-27`, `src/travel_plan_permission/security.py:84-100`, `src/travel_plan_permission/http_service.py` | CONFIRMED | `docs/security-model.md:17-27` and `security.py:84-100` specify `/api/itineraries`, `/api/approvals/*`, `/api/exports/*`, but `http_service.py` registers zero routes for these paths. |
| 24 | **Claim: Backplane runs** | `docs/contracts/run-contract-v1.md:15-17`, `.github/workflows/backplane-conformance.yml:54` | CONFIRMED | Contract states no participant emits an envelope yet (`run-contract-v1.md:16-17`); validator exists but `config/backplane_participants.json` is missing and backplane CI step echoes "No emitter wired yet". |
| 25 | **Claim: Receipt OCR** | `src/travel_plan_permission/receipts.py:107-121`, `docs/ORCHESTRATION_PLAN.md:23`, `src/travel_plan_permission/expense_review.py:38-40` | CONFIRMED | `ReceiptProcessor.extract_from_image` exists behind optional `ocr` extra, but orchestration never calls it (`ORCHESTRATION_PLAN.md:23`); expense review only parses pre-extracted `ocr_text` strings. |
| 26 | **Claim: Issues.txt orchestration CI** | `Issues.txt:112-114`, `.github/workflows/ci.yml:61-87` | CONFIRMED | `Issues.txt:112-114` leaves `- [ ] Ensure at least one CI run installs .[orchestration]` unchecked, whereas `.github/workflows/ci.yml:61-87` already has an active `orchestration` CI job testing LangGraph. |
| 27 | **Claim: OIDC** | `src/travel_plan_permission/planner_auth.py:24`, `render.yaml:22-23` | CONFIRMED | `planner_auth.py` implements full OIDC JWT verification, but the public Render deployment sets `TPP_AUTH_MODE=bootstrap-token` with synthetic fixtures. |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 28 | Offer: Canonical TripPlan JSON | `schemas/trip_plan.min.schema.json:1-100` | CONFIRMED | Canonical JSON schema provides standard contract for trip intake. |
| 29 | Offer: Policy evaluation result | `src/travel_plan_permission/policy_contract_models.py:444-470` | CONFIRMED | `PlannerProposalEvaluationResult` carries `execution_id`, `proposal_id`, `outcome`, and underlying `policy_result`. |
| 30 | Offer: Policy snapshot | `src/travel_plan_permission/policy_contract_models.py:136-160` | CONFIRMED | `PlannerPolicySnapshot` provides freshness timestamp, rules status, and list of requirements. |
| 31 | Offer: Planner proposal lifecycle IDs | `docs/contracts/planner-integration.md:40-90` | CONFIRMED | `proposal_id`, `execution_id`, and `trip_id` are defined and enforced across the HTTP handshake. |
| 32 | Offer: Excel travel workbook bytes | `src/travel_plan_permission/policy_api.py:1145-1250`, `config/excel_mappings.yaml:1-50` | CONFIRMED | Renders populated `.xlsx` binary buffers adhering to organization template. |
| 33 | Offer: Expense export batch | `src/travel_plan_permission/export.py:20`, `docs/accounting-integration.md:15-25` | CONFIRMED | `ExportService.schema` defines fixed 6-column CSV/Excel export order. |
| 34 | Offer: Audit events CSV | `src/travel_plan_permission/audit.py:44-54` | CONFIRMED | `CSV_FIELDS` defines standard 9-column schema exported by `tpp-audit-export`. |
| 35 | Offer: Validation snapshots | `src/travel_plan_permission/snapshots.py:49-65` | CONFIRMED | `ValidationSnapshot` provides hash-chained serialized policy verification records. |
| 36 | Consume: Partial trip context from `trip-planner` | `src/travel_plan_permission/portal_handoff.py:1-50` | CONFIRMED | `POST /portal/handoff` accepts JSON payload and issues draft-scoped capability cookie. |
| 37 | Consume: Planner proposal payloads | `tests/fixtures/planner_integration/proposal_submission.json` | CONFIRMED | Fixture payload matches `PlannerProposalEvaluationRequest` schema. |
| 38 | Consume: Receipt metadata and optional OCR text | `src/travel_plan_permission/receipts.py:18-32`, `src/travel_plan_permission/models.py:250-280` | CONFIRMED | Models parse vendor, total, date, file reference, and optional OCR text. |
| 39 | Consume: Sibling integration with `trip-planner` | `docs/contracts/planner-integration.md`, `src/travel_plan_permission/cross_repo_smoke.py:31-38` | **UNVERIFIABLE (off-clone runtime)** | Local contracts and smoke test scaffolding exist, but live end-to-end communication with sibling `trip-planner` requires external active services and network setup. |
| 40 | Collision risk: `trip_id` is a free-form string on `TripPlan`, not a fleet canonical ID | `src/travel_plan_permission/models.py:140-160`, `docs/contracts/identity-map-conventions.md:40-80` | CONFIRMED | Does not emit or consume fleet canonical entity syntax (`manager:cik_*` / `fund:lei_*`). |
| 41 | Collision risk: `ExpenseCategory` enum may not align with external accounting taxonomies | `src/travel_plan_permission/models.py:26-34` | CONFIRMED | Closed 6-member StrEnum (`airfare`, `lodging`, `ground_transport`, `meals`, `conference_fees`, `other`). |
| 42 | Collision risk: `cost_center` is a plain string on `TripPlan` without shared registry | `src/travel_plan_permission/canonical.py:103`, `src/travel_plan_permission/models.py:145` | CONFIRMED | Free-form string without validation against an organizational cost-center registry. |
| 43 | Collision risk: Policy version strings are TPP-local | `src/travel_plan_permission/policy_versioning.py:49-75` | CONFIRMED | Semantic version tracking and migration planning are repo-local. |
| 44 | Collision risk: Public demo fixtures must never be confused with production entity data | `render.yaml:1-6` | CONFIRMED | Explicit header warning in `render.yaml` that public service is synthetic-only. |

---

## §1, §2, §3, §6, §7, §10, §11 — Supporting Claims

| # | Section | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|---|
| 45 | §1 | Purpose and reproducible workflow | `README.md:5-6`, `pyproject.toml:62` | CONFIRMED | Stated purpose in README and `tpp-planner-service` script entry point. |
| 46 | §2 | CLI spreadsheet fill entry point | `src/travel_plan_permission/cli.py`, `README.md:35-41`, `tests/python/test_cli.py` | CONFIRMED | Console script `fill-spreadsheet` mapped to `cli:main`. |
| 47 | §2 | Cross-repo smoke CI job | `.github/workflows/ci.yml:89-236` | CONFIRMED | Job `cross-repo-smoke` checks out pinned `trip-planner` SHA. Total file length is 236 lines. |
| 48 | §2 | Portal and demo review endpoints | `README.md:91-102`, `tests/python/test_portal_review.py` | CONFIRMED | Routes `/portal`, `/portal/requests/new`, `/portal/review/{id}` confirmed in `http_service.py`. |
| 49 | §3 | Sync manifest management for CI workflows | `AGENTS.md:27-29` | CONFIRMED | Confirms synced workflows and scripts are managed via `.github/sync-manifest.yml` in Workflows. |
| 50 | §6 | Dependencies: Python 3.12+, FastAPI, openpyxl, reportlab, optional langgraph, psycopg, pytesseract | `pyproject.toml:7, 19-56` | CONFIRMED | Declared in project core and optional dependency sections. |
| 51 | §6 | Receipt allowed formats: PDF, PNG, JPEG, HEIC, 10MB limit | `src/travel_plan_permission/receipts.py:14-15` | CONFIRMED | `ALLOWED_RECEIPT_TYPES` and `MAX_RECEIPT_SIZE_BYTES` match exactly. |
| 52 | §7 | CI gate aggregation and test coverage: ≥80% branch coverage, Alpha classifier | `pyproject.toml:11, 104-118` | CONFIRMED | Classifiers mark `Development Status :: 3 - Alpha`; coverage config sets `branch = true` and `fail_under = 80`. |
| 53 | §7 | Backplane conformance emitter placeholder | `.github/workflows/backplane-conformance.yml:54` | CONFIRMED | Script step echoes "No emitter wired yet; the conformance gate will skip (opt-in)." |
| 54 | §11 | Proposed direction: workflow sync open, expense portal export-only | `Issues.txt:264-269`, `docs/accounting-integration.md:39` | CONFIRMED | Open sync task in `Issues.txt`; export-only boundary in `docs/accounting-integration.md`. |
