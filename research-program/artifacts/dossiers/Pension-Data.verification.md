# Pension-Data dossier — verification table

Verified against clone `clones/Pension-Data` at HEAD `917aced81c5103b101030027f5d3b16274f8ad08` (2026-09-04).
Method: every cited file:line/symbol opened and verified against current code and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 55 |
| WRONG (corrected in dossier) | 1 |
| CITE-DRIFT (substance right, citation refined) | 6 |
| UNVERIFIABLE (off-network live HTTP) | 1 |
| **Total checked** | **63** |

### Key Findings & Corrections

1. **§8 Desktop Tauri Rust refutation (adversarial check):** The original dossier asserted in §8 that "the Tauri directory has manifest/build configuration only and no Rust application source". Opening `apps/mac-desktop/src-tauri/src/main.rs:1-8` demonstrates that Rust application source **does exist**: an 8-line minimal Tauri entry point (`tauri::Builder::default().run(...)`) alongside `build.rs` and `Cargo.toml`. Claiming "no Rust application source" was an overstated refutation. The true state is that the Tauri shell is a minimal boilerplate wrapper, `src-ui/` is empty (.gitkeep) until `scripts/sync_web_ui.sh` is executed, and the desktop track remains an unreleased scaffold lacking signed/notarized release flows, measured device benchmarks, desktop-specific features, and local sidecar parity (`apps/mac-desktop/IMPLEMENTATION_PLAN.md:14-26`). Both §8 and §2 have been corrected.
2. **§4 Function vs Contract/Type citation drifts:**
   - In `pdf_pipeline.py:120-154`, lines 120-144 define `PDFParserResult` and stage contracts, while `parse_pdf_to_funded_input` is defined at lines 492-542. `hybrid_backend.py` ends at line 332 (citation said 221-334).
   - In `document_orchestration.py:84-175`, lines 84-175 define orchestration stage enums, outcome models, and ledger contracts; `run_document_orchestration` itself is at lines 717-862.
   - In `extract/persistence.py:39-171`, lines 39-171 define staging column sets and contract metadata; `build_extraction_persistence_artifacts` is at lines 941-1089.
   - In `one_pdf_pilot.py:282-460`, `run_one_pdf_pilot` extends through line 498 to return the complete artifact dictionary.
3. **§6 & §7 pyproject.toml citation drifts:**
   - The `langchain` optional dependency table is at `pyproject.toml:45-51` (lines 34-41 are `fastapi ... postgres`).
   - The 80% coverage threshold is enforced at `pyproject.toml:100` (`fail_under = 80`), while lines 57-69 define dev test tooling (lines 64-68 are `app-baseline-kit`, `pytest-regressions`, `numpy`, `pandas`).
4. **Path / link sanitization:** All 54 markdown citations in the original dossier were prefixed with `../` (inherited from `clones/Pension-Data/dossier-out/DOSSIER.md`), breaking resolution when viewed from `artifacts/dossiers/`. All citations have been sanitized to clean repo-relative paths.
5. **Exact test count confirmed:** Pytest execution with repo paths confirmed exactly 1,382 passed and 4 skipped (1,386 total collected), perfectly matching the dossier claim.
6. **Unverifiable off-network calls:** SEC EDGAR and PPD live HTTP client endpoints cannot be reached due to sandbox network isolation; verified that recorded fixtures and offline caches are used in test suites.

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | `run_one_pdf_pilot` consumes PDF & metadata, invokes parser/orchestration, writes artifacts & manifest | `src/pension_data/ops/one_pdf_pilot.py:282-460` | CONFIRMED (cite-drift) | Substance exact. Function spans lines 282-498 to return the full artifact path mapping. |
| 2 | `parse_pdf_to_funded_input` produces raw input, attempts, confidence, escalation; `run_hybrid_table_extraction` cross-checks | `src/pension_data/parser/pdf_pipeline.py:120-154`, `src/pension_data/parser/hybrid_backend.py:221-334` | CONFIRMED (cite-drift) | `PDFParserResult` defined at `pdf_pipeline.py:120-144`; `parse_pdf_to_funded_input` at `:492-542`. `hybrid_backend.py:221-332` defines routing, disagreement logic, and `run_hybrid_table_extraction` (:290-331). |
| 3 | `run_document_orchestration` covers discovery, immutable ingestion, extraction, validation, publishing | `src/pension_data/ops/document_orchestration.py:84-175` | CONFIRMED (cite-drift) | Lines 84-175 define stages, outcomes, ledger, and state contracts; function `run_document_orchestration` spans `:717-862`. |
| 4 | `build_extraction_persistence_artifacts` & adapters project observations to shared staging rows | `src/pension_data/extract/persistence.py:39-171` | CONFIRMED (cite-drift) | Lines 39-171 define column tuples and contract dict; `build_extraction_persistence_artifacts` is at `:941-1089`. |
| 5 | `route_confidence_row` assigns routing; `build_extraction_review_queue` creates auditable queue rows | `src/pension_data/quality/confidence.py:14-83`, `src/pension_data/review_queue/extraction.py:38-104` | CONFIRMED | Exact lines: auto-accept (0.90), warning (0.75), high-priority review at `confidence.py:14-83`; queue builder with audit entries at `extraction.py:38-104`. |
| 6 | `build_canonical_stable_id`, source linking, merges, matching, lineage | `src/pension_data/entities/service.py:54-104`, `src/pension_data/entities/service.py:199-272` | CONFIRMED | `build_canonical_stable_id` at :54-68, `create_canonical_entity` at :74-104; `merge_canonical_entities` with forward lineage at :199-272. |
| 7 | Raw artifacts deduplicated by hash & superseded; staged facts retain bitemporal times | `src/pension_data/ingest/artifacts.py:24-35`, `src/pension_data/ingest/artifacts.py:127-161`, `src/pension_data/db/models/core_facts.py:48-75` | CONFIRMED | Deduplication & supersession exact at `artifacts.py:24-35, 127-161`; `BitemporalFactContext` with `valid_from`, `asserted_at`, `superseded_at` at `core_facts.py:48-75`. |
| 8 | `compute_derived_metrics` produces funded gap, unfunded ratio, cash flow, contribution coverage | `src/pension_data/quant/metric_engine.py:70-116`, `src/pension_data/quant/metric_engine.py:241-345` | CONFIRMED | Catalog definitions at :70-116; `compute_derived_metrics` implementation with lineage formulas and source fact IDs at :241-345. |
| 9 | `build_backplane_reference_run` converts pilot manifest into `artifact-manifest/v1` and `run-contract/v1` | `src/pension_data/ops/backplane_emitter.py:104-235` | CONFIRMED | Exact function lines 104-235; writes `manifest.json` and `run.json` with hashes, latency, warnings, and provenance. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 10 | Natural key is `plan_id` + `plan_period`, separated by effective/ingestion dates | — | CONFIRMED | Standard key across `one_pdf_pilot.py:290-297`, `document_orchestration.py:94-103`, `core_facts.py:51-54`. |
| 11 | Fact IDs use deterministic `fact:<sha256-prefix>` (20 hex chars) | `src/pension_data/extract/common/ids.py:9-13`, `src/pension_data/extract/persistence.py:214-274` | CONFIRMED | `ids.py:9-13` builds `fact:<digest[:20]>`; `persistence.py:225-236` calls `_stable_id("fact", ...)`. |
| 12 | Document IDs use `artifact:<hash>` (24 hex chars) and supersede prior active | `src/pension_data/ingest/artifacts.py:24-35` | CONFIRMED | `_artifact_id` computes `artifact:<digest[:24]>` from key payload, checksum, and timestamp. |
| 13 | Security keys prefer CUSIP, then ticker, then normalized name | `src/pension_data/extract/investment/security_positions.py:89-97` | CONFIRMED | `_security_id` prioritizes `cusip:`, then `ticker:`, then `name:`. |
| 14 | Form 5500 joins use normalized nine-digit EIN plus three-digit plan number | `src/pension_data/entities/models.py:30-46` | CONFIRMED | `SponsorPlanKey` validates exactly 9-digit EIN and 3-digit plan number (:37-46). |
| 15 | SQLite is local default; PostgreSQL required for production, needs `psycopg` extra | `src/pension_data/db/strategy.py:15-16`, `src/pension_data/db/strategy.py:46-98` | CONFIRMED | `DEFAULT_LOCAL_SQLITE_URL` (:15); `resolve_database_config` requires postgresql for production (:54-55); `connect_database` imports `psycopg` (:92-98). |
| 16 | Staged core metrics persisted idempotently, closing prior assertions on restatement | `src/pension_data/db/staging_persistence.py:96-172` | CONFIRMED | `persist_staging_core_metrics` handles `ON CONFLICT DO NOTHING`, sets `superseded_at` and `restated = True` on existing active assertions. |
| 17 | Repo ships contracts and emits one-PDF manifest + validated `run-contract/v1` envelope | `tests/ops/test_backplane_emitter.py:91-150` | CONFIRMED | `test_reference_run_validates_strictly` asserts schema conformance against `run-contract/v1` and `artifact-manifest/v1`. |
| 18 | Constructs local `EvidenceReference` with page, excerpt, method; envelope carries hashed strings | `src/pension_data/extract/common/evidence.py:89-157`, `src/pension_data/ops/backplane_emitter.py:147-150` | CONFIRMED | `build_evidence_reference` constructs `EvidenceReference` with anchors; `backplane_emitter.py:148` maps to `evidence:<sha256[:16]>`. |
| 19 | Query run records implemented; test guard prevents repo checkout leakage | `docs/contracts/query-run-record-contract.md:27-47` | CONFIRMED | Exact lines 27-47; notes session-scoped `_no_run_artifacts_written_into_checkout` guard in `tests/conftest.py`. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement / Evidence |
|---|---|---|---|---|
| 20 | README calls `/api` routes "deterministic", but analytical routes return fixture rows | `README.md:32-37`, `src/pension_data/api/app.py:41-105` | CONFIRMED | `README.md:32-37` advertises deterministic API routes; `api/app.py:71` uses `_fixture_funding_trend_inputs()` and `:95` uses `_fixture_metric_history_rows()`. |
| 21 | Findings contract advertises explain/compare, but routes return HTTP 501 | `docs/contracts/reviewable-findings-artifact-contract.md:51-58`, `src/pension_data/api/app.py:106-127` | CONFIRMED | Contract specifies `explain` and `compare` (:51-58); routes raise `HTTPException(status_code=501)` (:115, 123). |
| 22 | **Desktop README presents `tauri:build`, but Tauri directory has "manifest/build configuration only and no Rust application source"** | `apps/mac-desktop/README.md:18-32`, `apps/mac-desktop/IMPLEMENTATION_PLAN.md:3-26` | **WRONG (false refutation / overstated)** | **Rust application source does exist.** `apps/mac-desktop/src-tauri/src/main.rs:1-8` contains an 8-line working Tauri entry point (`tauri::Builder::default().run(...)`) alongside `build.rs` and `Cargo.toml`. What is actually true: `src-ui/` is unpopulated until `scripts/sync_web_ui.sh` runs, and the desktop app is an unreleased scaffold lacking signing/notarization, measured benchmarks, desktop features, and local sidecar parity (`IMPLEMENTATION_PLAN.md:14-26`). Refuting the command by claiming zero Rust source existed was a false refutation. |
| 23 | Backplane contract says "No participant emits an envelope yet"; stale for Pension-Data | `docs/contracts/run-contract-v1.md:15-17`, `src/pension_data/ops/one_pdf_pilot_cli.py:117-131` | CONFIRMED | `run-contract-v1.md:16-17` says "No participant emits an envelope yet"; `one_pdf_pilot_cli.py:124-131` explicitly generates and emits `run.json` and `manifest.json`. |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 24 | Export canonical `manager:`, `fund:`, consultant, pension IDs; entity-linkage contract | `docs/contracts/entity-linkage-contract.md:11-30` | CONFIRMED | Rules at :11-20 (`manager:`, `fund:`, `consultant:`), linkage statuses (`resolved`, `ambiguous`, `not_disclosed`) at :21-26. |
| 25 | Emits document checksum lineage, fact IDs, staging rows, confidence queues, locators, metrics, backplane | `src/pension_data/ops/backplane_emitter.py:158-235` | CONFIRMED | Manifest and run envelope contain full artifact listings, data quality findings, evidence references, and latency. |
| 26 | Consumes upstream source documents, local holdings, PPD/EDGAR formats | — | CONFIRMED | Verified parsers and ingestion clients in `sources/ppd`, `sources/edgar`, `extract/investment/security_positions.py`. |
| 27 | Vocabulary collision: emits `plan:` and `document:` whereas fleet conventions reserve `pension:` | `src/pension_data/ops/backplane_emitter.py:151-154`, `docs/contracts/identity-map-conventions.md:79-88` | CONFIRMED | `backplane_emitter.py:152-153` produces `plan:...` and `document:...`; conventions table (:81-88) defines `pension` and omits `document`. |
| 28 | Manager IDs fallback to normalized names while fleet policy prefers registry IDs (Manager-Database authoritative) | `docs/contracts/identity-map-conventions.md:94-121` | CONFIRMED | Manager-Database is authoritative for manager (:100-101); registry IDs preferred (:116-118). |

---

## §2 — Surfaces

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 29 | CLI `one-pdf-pilot` takes PDF + metadata, writes pilot and backplane artifacts | `src/pension_data/ops/one_pdf_pilot_cli.py:97-137`, `tests/ops/test_one_pdf_pilot_cli.py:63-104` | CONFIRMED | `main()` parses CLI args, runs pilot, invokes backplane emitter, tested in `test_one_pdf_pilot_cli.py`. |
| 30 | Python API health/config & saved views work with fixtures; NL/findings return 501 | `src/pension_data/api/app.py:28-136` | CONFIRMED | Lines 40-132 define `create_app` with `/health`, `/config`, fixture-backed `/api/saved-views`, and 501 routes. |
| 31 | Static HTML/PWA validates/displays JSON bundle, saves views; demo bundle | `apps/web/index.html`, `apps/web/app.js:149-254`, `apps/web/README.md:17-18` | CONFIRMED | `normalizeWorkspaceBundle` validates schema; localStorage saves views; README states checked-in bundle is fixture demo. |
| 32 | Artifacts emits parser, staging, warnings, coverage, manifest, backplane JSON | `src/pension_data/ops/one_pdf_pilot.py:282-460`, `src/pension_data/ops/backplane_emitter.py:104-235` | CONFIRMED | All 10 artifact files produced by `run_one_pdf_pilot` and 2 by `build_backplane_reference_run`. |
| 33 | macOS desktop Electron has window shell, Tauri has minimal main, unreleased scaffold | `apps/mac-desktop`, `apps/mac-desktop/IMPLEMENTATION_PLAN.md:14-26` | CONFIRMED (corrected) | Corrected to acknowledge `src-tauri/src/main.rs` while confirming unfinished state tracked in `IMPLEMENTATION_PLAN.md:14-26`. |

---

## §1, §3, §6, §7, §10, §11 — Remaining sections

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 34 | Purpose & intended users (allocators, executives, policy analysts) | `docs/Planning/PENSION_DATA_PLAN.md:5-13` | CONFIRMED | Exact user personas listed at lines 7-10. |
| 35 | In-perimeter privacy & zero-egress design constraint | `docs/deploy/IN_PERIMETER_REAL_DATA_REVIEW.md:3-18` | CONFIRMED | Explains localhost loopback, stdlib serving, and zero public SaaS egress. |
| 36 | Structure map accurately reflects repo directory layout | — | CONFIRMED | All directories (`src/pension_data/`, `apps/`, `config/`, `docs/`, `scripts/`, `tests/`, `.github/`) verified. |
| 37 | Test suite contains 1,386 tests | — | CONFIRMED | Exact count: 1,386 nodeids collected in pytest. |
| 38 | External inputs: PDFs, CSV/XLS holdings, PPD API, Form 5500, EDGAR 13F XML | — | CONFIRMED | Parsers and clients present for all named formats. |
| 39 | PPD client uses standard library urllib, tests use cache/fixtures | `src/pension_data/sources/ppd/client.py:1-14` | CONFIRMED | Client docstring and implementation confirmed. |
| 40 | EDGAR client enforces User-Agent, tests use recorded fixtures | `src/pension_data/sources/edgar/client.py:12-16` | CONFIRMED | Client docstring and fixtures confirmed. |
| 41 | PDF parsing uses `pypdf` + `stranske-pdf-extract`; XML uses `defusedxml`; XLS uses `openpyxl` | `pyproject.toml:22-48`, `src/pension_data/extract/investment/security_positions.py:184-208` | CONFIRMED | Dependencies listed in `pyproject.toml` and lazy import in `security_positions.py`. |
| 42 | Optional LangChain dependencies require `[langchain]` extra and API keys | `pyproject.toml:34-41`, `src/pension_data/langchain/foundation.py:104-143` | CONFIRMED (cite-drift) | `foundation.py:104-143` confirmed; `[langchain]` extra is at `pyproject.toml:45-51`. |
| 43 | No Docker requirement; PostgreSQL required for shared persistence | — | CONFIRMED | No Dockerfile present; SQLite default with optional PostgreSQL backend. |
| 44 | Test suite execution: 1,382 passed, 4 skipped | — | CONFIRMED | Executed `pytest -q tests` under Python 3.12: 1382 passed, 4 skipped in 4.95s. |
| 45 | CI runs Ruff, Black, mypy, pytest on Python 3.12/3.13 with 80% coverage | `pyproject.toml:64-68`, `.github/workflows/ci.yml:24-32` | CONFIRMED (cite-drift) | `ci.yml:24-32` exact; `pyproject.toml:100` sets `fail_under = 80`. |
| 46 | Gap: analyst UI & LangChain findings explicitly incomplete | `README.md:99-105` | CONFIRMED | Exact text under "Roadmap Gaps". |
| 47 | Gap: API fixture-only data and three 501 LLM endpoints | `src/pension_data/api/app.py:41-127` | CONFIRMED | Verified in `create_app`. |
| 48 | Gap: desktop lacks signing, measured device data, features, sidecar, tests | `apps/mac-desktop/IMPLEMENTATION_PLAN.md:14-26` | CONFIRMED | Tasks marked incomplete `[ ]` in plan. |
| 49 | Gap: live source network paths not exercised in test gate | — | UNVERIFIABLE (off-network) | Tests intentionally avoid external network calls; cannot exercise live APIs in sandbox. |
| 50 | Gap: Cloudflare Pages workflow refuses non-fixture bundles | `.github/workflows/web-cloudflare-pages.yml:103-116` | CONFIRMED | Step explicitly enforces `data_origin == "fixture"`. |
| 51 | Gap: run-contract-v1 doc is stale regarding envelope emission | `docs/contracts/run-contract-v1.md:15-17` | CONFIRMED | Verified stale doc against working emitter. |
| 52 | Reuse: source artifact dedupe and supersession | `src/pension_data/ingest/artifacts.py` | CONFIRMED | Exists and verified. |
| 53 | Reuse: canonical evidence parsing, IDs, excerpts, method mapping | `src/pension_data/extract/common/evidence.py` | CONFIRMED | Exists and verified. |
| 54 | Reuse: entity aliases, matching, merge and forward lineage | `src/pension_data/entities/` | CONFIRMED | Exists and verified. |
| 55 | Reuse: bitemporal assertion and overlap controls | `src/pension_data/db/models/bitemporal.py` | CONFIRMED | Exists and verified. |
| 56 | Reuse: read-only SQL/NL guardrails and replay records | `src/pension_data/query/`, `src/pension_data/langchain/nl_sql_chain.py` | CONFIRMED | Exists and verified. |
| 57 | Reuse: generated static workspace bundle and loopback server | `scripts/web/` | CONFIRMED | Exists and verified. |
| 58 | Direction: connect API saved views/history to database | `src/pension_data/api/app.py:41-105` | CONFIRMED | Accurate recommendation. |
| 59 | Direction: inject approved LangChain chains into disabled routes | `src/pension_data/api/app.py:106-127` | CONFIRMED | Accurate recommendation. |
| 60 | Direction: make Tauri application buildable, add signing/benchmarks | `apps/mac-desktop/IMPLEMENTATION_PLAN.md:14-26` | CONFIRMED | Accurate recommendation. |
| 61 | Direction: update stale backplane doc and emit evidence-object/v1 | `docs/contracts/run-contract-v1.md:15-17`, `docs/contracts/schemas/evidence-object-v1.schema.json:8-99` | CONFIRMED | Accurate recommendation. |
| 62 | Direction: add controlled live-source ingestion recipe | `src/pension_data/sources/ppd/client.py:1-14` | CONFIRMED | Accurate recommendation. |
| 63 | Direction: establish manager-ID reconciliation with Manager-Database | `docs/contracts/identity-map-conventions.md:94-130` | CONFIRMED | Accurate recommendation. |

