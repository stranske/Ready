# Pension-Data dossier — verification table

Verified against clone `clones/Pension-Data` at HEAD `ddda7b96aa8998780297f44cdca0f243f7ce598a` (2026-09-04, attempt 2).
Method: every cited file:line/symbol opened and verified against current code and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 61 |
| WRONG (corrected in dossier) | 0 |
| CITE-DRIFT (substance right, citation refined) | 1 |
| UNVERIFIABLE (off-network live HTTP) | 1 |
| **Total checked** | **63** |

### Key Findings (attempt 2)

1. **Clone HEAD advanced** from `917aced` (attempt 1) to `ddda7b9` (`chore: sync workflow templates`). All 63 claims re-checked on current HEAD; no substance regressions found.
2. **§4/§2 `run_one_pdf_pilot` cite drift:** Function return dict now ends at line 505 (not 498). Dossier citations updated from `282-498` to `282-505`.
3. **§8 Desktop Tauri (adversarial re-check):** Prior correction holds. `apps/mac-desktop/src-tauri/src/main.rs:1-8` contains a working 8-line Tauri entry point; `src-ui/` holds only `.gitkeep` until `scripts/sync_web_ui.sh` runs. Claiming "no Rust application source" would be a false refutation.
4. **Pytest counts re-executed:** `pytest -q` → 1,382 passed, 4 skipped (1,386 collected); matches §7 claim.
5. **Unverifiable off-network calls:** PPD and EDGAR live HTTP endpoints remain unreachable in sandbox; fixture/cache paths confirmed in client docstrings and tests.

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | `run_one_pdf_pilot` consumes PDF & metadata, invokes parser/orchestration, writes artifacts & manifest | `src/pension_data/ops/one_pdf_pilot.py:282-505` | CONFIRMED (cite-drift) | Function defined `:282`; return dict spans `:478-505`. |
| 2 | `parse_pdf_to_funded_input` produces raw input, attempts, confidence, escalation; `run_hybrid_table_extraction` cross-checks | `src/pension_data/parser/pdf_pipeline.py:120-144, 492-542`, `src/pension_data/parser/hybrid_backend.py:221-332` | CONFIRMED | `PDFParserResult` at `:120-144`; `parse_pdf_to_funded_input` at `:492-542`; `run_hybrid_table_extraction` at `hybrid_backend.py:290-331`. |
| 3 | `run_document_orchestration` covers discovery, immutable ingestion, extraction, validation, publishing | `src/pension_data/ops/document_orchestration.py:84-175, 717-862` | CONFIRMED | Stage enums/outcomes at `:84-175`; function at `:717-862`. |
| 4 | `build_extraction_persistence_artifacts` & adapters project observations to shared staging rows | `src/pension_data/extract/persistence.py:39-171, 941-1089` | CONFIRMED | Column tuples at `:39-171`; function at `:941-1089`. |
| 5 | `route_confidence_row` assigns routing; `build_extraction_review_queue` creates auditable queue rows | `src/pension_data/quality/confidence.py:14-83`, `src/pension_data/review_queue/extraction.py:38-104` | CONFIRMED | Thresholds 0.90/0.75 at `confidence.py:14-83`; queue builder with audit trail at `extraction.py:38-104`. |
| 6 | `build_canonical_stable_id`, source linking, merges, matching, lineage | `src/pension_data/entities/service.py:54-104, 199-272` | CONFIRMED | `build_canonical_stable_id` at `:54-68`; `merge_canonical_entities` with forward lineage at `:199-272`. |
| 7 | Raw artifacts deduplicated by hash & superseded; staged facts retain bitemporal times | `src/pension_data/ingest/artifacts.py:24-35, 127-161`, `src/pension_data/db/models/core_facts.py:48-75` | CONFIRMED | `_artifact_id` and supersession at `artifacts.py:24-35, 127-161`; `BitemporalFactContext` at `core_facts.py:48-75`. |
| 8 | `compute_derived_metrics` produces funded gap, unfunded ratio, cash flow, contribution coverage | `src/pension_data/quant/metric_engine.py:70-116, 241-345` | CONFIRMED | Catalog at `:70-116`; implementation with lineage at `:241-345`. |
| 9 | `build_backplane_reference_run` converts pilot manifest into `artifact-manifest/v1` and `run-contract/v1` | `src/pension_data/ops/backplane_emitter.py:104-235` | CONFIRMED | Writes `manifest.json` and `run.json` at `:104-235`. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 10 | Natural key is `plan_id` + `plan_period`, separated by effective/ingestion dates | — | CONFIRMED | Standard key across orchestration and staging models. |
| 11 | Fact IDs use deterministic `fact:<sha256-prefix>` (20 hex chars) | `src/pension_data/extract/common/ids.py:9-13`, `src/pension_data/extract/persistence.py:214-274` | CONFIRMED | `stable_id` at `ids.py:9-13`; `_stable_id("fact", ...)` at `persistence.py:225-236`. |
| 12 | Document IDs use `artifact:<hash>` (24 hex chars) and supersede prior active | `src/pension_data/ingest/artifacts.py:24-35` | CONFIRMED | `_artifact_id` computes `artifact:<digest[:24]>`. |
| 13 | Security keys prefer CUSIP, then ticker, then normalized name | `src/pension_data/extract/investment/security_positions.py:89-97` | CONFIRMED | `_security_id` priority order exact. |
| 14 | Form 5500 joins use normalized nine-digit EIN plus three-digit plan number | `src/pension_data/entities/models.py:30-46` | CONFIRMED | `SponsorPlanKey` validates 9-digit EIN and 1–3 digit plan number. |
| 15 | SQLite is local default; PostgreSQL required for production, needs `psycopg` extra | `src/pension_data/db/strategy.py:15-16, 46-98` | CONFIRMED | `DEFAULT_LOCAL_SQLITE_URL` at `:15`; production requires postgresql at `:54-55`; `psycopg` import at `:92-98`. |
| 16 | Staged core metrics persisted idempotently, closing prior assertions on restatement | `src/pension_data/db/staging_persistence.py:96-172` | CONFIRMED | `ON CONFLICT DO NOTHING` plus `superseded_at`/`restated` updates. |
| 17 | Repo ships contracts and emits one-PDF manifest + validated `run-contract/v1` envelope | `tests/ops/test_backplane_emitter.py:91-150` | CONFIRMED | `test_reference_run_validates_strictly` and CLI integration test. |
| 18 | Constructs local `EvidenceReference` with page, excerpt, method; envelope carries hashed strings | `src/pension_data/extract/common/evidence.py:89-157`, `src/pension_data/ops/backplane_emitter.py:147-150` | CONFIRMED | `build_evidence_reference` at `:89-157`; hashed refs at `backplane_emitter.py:147-150`. |
| 19 | Query run records implemented; test guard prevents repo checkout leakage | `docs/contracts/query-run-record-contract.md:27-47` | CONFIRMED | Artifact layout and `_no_run_artifacts_written_into_checkout` guard documented. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement / Evidence |
|---|---|---|---|---|
| 20 | README calls `/api` routes "deterministic", but analytical routes return fixture rows | `README.md:32-37`, `src/pension_data/api/app.py:41-105` | CONFIRMED | README line 33 advertises deterministic `/api` routes; `api/app.py:71,95` call `_fixture_*` helpers. |
| 21 | Findings contract advertises explain/compare, but routes return HTTP 501 | `docs/contracts/reviewable-findings-artifact-contract.md:51-58`, `src/pension_data/api/app.py:106-127` | CONFIRMED | Contract at `:55-56`; routes raise 501 at `:115,123`. |
| 22 | Desktop README presents `tauri:build`; Tauri shell is minimal boilerplate, `src-ui/` empty, unreleased scaffold | `apps/mac-desktop/README.md:18-32`, `apps/mac-desktop/src-tauri/src/main.rs:1-8`, `apps/mac-desktop/IMPLEMENTATION_PLAN.md:14-26` | CONFIRMED | Rust entry point exists (`main.rs:1-8`); `src-ui/` contains only `.gitkeep`; Phase 2–4 tasks remain open in plan. |
| 23 | Backplane contract says "No participant emits an envelope yet"; stale for Pension-Data | `docs/contracts/run-contract-v1.md:15-17`, `src/pension_data/ops/one_pdf_pilot_cli.py:117-131` | CONFIRMED | Stale doc at `:16-17`; CLI emits `run.json` and `manifest.json` at `:124-131`. |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 24 | Export canonical `manager:`, `fund:`, consultant, pension IDs; entity-linkage contract | `docs/contracts/entity-linkage-contract.md:11-30` | CONFIRMED | ID rules at `:13-17`; linkage statuses at `:23-25`. |
| 25 | Emits document checksum lineage, fact IDs, staging rows, confidence queues, locators, metrics, backplane | `src/pension_data/ops/backplane_emitter.py:158-235` | CONFIRMED | Manifest and run envelope contain full artifact listings and provenance. |
| 26 | Consumes upstream source documents, local holdings, PPD/EDGAR formats | — | CONFIRMED | Parsers and ingestion clients present. |
| 27 | Vocabulary collision: emits `plan:` and `document:` whereas fleet conventions reserve `pension:` | `src/pension_data/ops/backplane_emitter.py:151-154`, `docs/contracts/identity-map-conventions.md:79-88` | CONFIRMED | `identity_refs` at `:151-154`; conventions table omits `document`. |
| 28 | Manager IDs fallback to normalized names while fleet policy prefers registry IDs (Manager-Database authoritative) | `docs/contracts/identity-map-conventions.md:94-121` | CONFIRMED | Authority order and registry-ID preference exact. |

---

## §2 — Surfaces

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 29 | CLI `one-pdf-pilot` takes PDF + metadata, writes pilot and backplane artifacts | `src/pension_data/ops/one_pdf_pilot_cli.py:97-137`, `tests/ops/test_one_pdf_pilot_cli.py:63-104` | CONFIRMED | `main()` at `:97-137`; tested at `test_one_pdf_pilot_cli.py:63-104`. |
| 30 | Python API health/config & saved views work with fixtures; NL/findings return 501 | `src/pension_data/api/app.py:28-136` | CONFIRMED | `create_app` with fixture-backed routes and three 501 endpoints. |
| 31 | Static HTML/PWA validates/displays JSON bundle, saves views; demo bundle | `apps/web/index.html`, `apps/web/app.js:149-254`, `apps/web/README.md:17-18` | CONFIRMED | `normalizeWorkspaceBundle` at `app.js:149-181`; localStorage at `:183-205`; README fixture note at `:17-18`. |
| 32 | Artifacts emits parser, staging, warnings, coverage, manifest, backplane JSON | `src/pension_data/ops/one_pdf_pilot.py:282-505`, `src/pension_data/ops/backplane_emitter.py:104-235` | CONFIRMED | All artifact paths in return dict; backplane emitter adds two files. |
| 33 | macOS desktop Electron has window shell, Tauri has minimal main, unreleased scaffold | `apps/mac-desktop`, `apps/mac-desktop/IMPLEMENTATION_PLAN.md:14-26` | CONFIRMED | `src-tauri/src/main.rs` present; open tasks in plan. |

---

## §1, §3, §6, §7, §10, §11 — Remaining sections

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 34 | Purpose & intended users (allocators, executives, policy analysts) | `docs/Planning/PENSION_DATA_PLAN.md:5-13` | CONFIRMED | User personas at lines 7-10. |
| 35 | In-perimeter privacy & zero-egress design constraint | `docs/deploy/IN_PERIMETER_REAL_DATA_REVIEW.md:3-18` | CONFIRMED | Loopback serving and zero-egress guarantees. |
| 36 | Structure map accurately reflects repo directory layout | — | CONFIRMED | All named directories verified. |
| 37 | Test suite contains 1,386 tests | — | CONFIRMED | `pytest --collect-only` → 1,386 nodeids. |
| 38 | External inputs: PDFs, CSV/XLS holdings, PPD API, Form 5500, EDGAR 13F XML | — | CONFIRMED | Parsers and clients present for all formats. |
| 39 | PPD client uses standard library urllib, tests use cache/fixtures | `src/pension_data/sources/ppd/client.py:1-14` | CONFIRMED | Docstring and implementation confirmed. |
| 40 | EDGAR client enforces User-Agent, tests use recorded fixtures | `src/pension_data/sources/edgar/client.py:12-16` | CONFIRMED | Docstring and fixture strategy confirmed. |
| 41 | PDF parsing uses `pypdf` + `stranske-pdf-extract`; XML uses `defusedxml`; XLS uses `openpyxl` | `pyproject.toml:22-56`, `src/pension_data/extract/investment/security_positions.py:184-208` | CONFIRMED | Dependencies and lazy `openpyxl` import confirmed. |
| 42 | Optional LangChain dependencies require `[langchain]` extra and API keys | `pyproject.toml:45-51`, `src/pension_data/langchain/foundation.py:104-143` | CONFIRMED | Extra at `pyproject.toml:45-51`; key checks at `foundation.py:122-126`. |
| 43 | No Docker requirement; PostgreSQL required for shared persistence | — | CONFIRMED | No Dockerfile; SQLite default with optional PostgreSQL. |
| 44 | Test suite execution: 1,382 passed, 4 skipped | — | CONFIRMED | Executed `pytest -q`: 1382 passed, 4 skipped in 6.71s. |
| 45 | CI runs Ruff, Black, mypy, pytest on Python 3.12/3.13 with 80% coverage | `pyproject.toml:57-69, 100`, `.github/workflows/ci.yml:24-32` | CONFIRMED | Reusable workflow at `ci.yml:24-32`; `fail_under = 80` at `pyproject.toml:100`. |
| 46 | Gap: analyst UI & LangChain findings explicitly incomplete | `README.md:99-105` | CONFIRMED | "Roadmap Gaps" section exact. |
| 47 | Gap: API fixture-only data and three 501 LLM endpoints | `src/pension_data/api/app.py:41-127` | CONFIRMED | Verified in `create_app`. |
| 48 | Gap: desktop lacks signing, measured device data, features, sidecar, tests | `apps/mac-desktop/IMPLEMENTATION_PLAN.md:14-26` | CONFIRMED | Open tasks at `:14-26`. |
| 49 | Gap: live source network paths not exercised in test gate | — | UNVERIFIABLE (off-network) | Tests use fixtures/cache; live APIs unreachable in sandbox. |
| 50 | Gap: Cloudflare Pages workflow refuses non-fixture bundles | `.github/workflows/web-cloudflare-pages.yml:103-116` | CONFIRMED | `data_origin != "fixture"` raises exit at `:112-116`. |
| 51 | Gap: run-contract-v1 doc is stale regarding envelope emission | `docs/contracts/run-contract-v1.md:15-17` | CONFIRMED | Stale against working emitter. |
| 52 | Reuse: source artifact dedupe and supersession | `src/pension_data/ingest/artifacts.py` | CONFIRMED | Module verified. |
| 53 | Reuse: canonical evidence parsing, IDs, excerpts, method mapping | `src/pension_data/extract/common/evidence.py` | CONFIRMED | Module verified. |
| 54 | Reuse: entity aliases, matching, merge and forward lineage | `src/pension_data/entities/` | CONFIRMED | Package verified. |
| 55 | Reuse: bitemporal assertion and overlap controls | `src/pension_data/db/models/bitemporal.py` | CONFIRMED | Module verified. |
| 56 | Reuse: read-only SQL/NL guardrails and replay records | `src/pension_data/query/`, `src/pension_data/langchain/nl_sql_chain.py` | CONFIRMED | Modules verified. |
| 57 | Reuse: generated static workspace bundle and loopback server | `scripts/web/` | CONFIRMED | Directory verified. |
| 58 | Direction: connect API saved views/history to database | `src/pension_data/api/app.py:41-105` | CONFIRMED | Accurate recommendation. |
| 59 | Direction: inject approved LangChain chains into disabled routes | `src/pension_data/api/app.py:106-127` | CONFIRMED | Accurate recommendation. |
| 60 | Direction: make Tauri application buildable, add signing/benchmarks | `apps/mac-desktop/IMPLEMENTATION_PLAN.md:14-26` | CONFIRMED | Accurate recommendation. |
| 61 | Direction: update stale backplane doc and emit evidence-object/v1 | `docs/contracts/run-contract-v1.md:15-17`, `docs/contracts/schemas/evidence-object-v1.schema.json:8-99` | CONFIRMED | Accurate recommendation. |
| 62 | Direction: add controlled live-source ingestion recipe | `src/pension_data/sources/ppd/client.py:1-14` | CONFIRMED | Accurate recommendation. |
| 63 | Direction: establish manager-ID reconciliation with Manager-Database | `docs/contracts/identity-map-conventions.md:94-130` | CONFIRMED | Accurate recommendation. |
