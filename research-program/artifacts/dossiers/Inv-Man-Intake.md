# Inv-Man-Intake — dossier (2026-09-04)

## 1. Purpose in one paragraph

Inv-Man-Intake is a local headless pipeline for turning manager packages into explainable priority scores and analyst exceptions. It models firm, fund and documents; validates metadata; extracts fields; applies confidence gates; normalizes returns; and writes artifacts (`README.md:3-20`, `src/inv_man_intake/run.py:133-166`). Its constraint is no hosted application or default data egress (`README.md:22-38`, `README.md:50-58`). The deterministic implementation remains much narrower than its multi-format ambition.

## 2. Who uses it and how (surfaces)

| Surface | Entry point (file) | Who uses it | Status with evidence |
|---|---|---|---|
| CLI | `inv-man-ingest`, `src/inv_man_intake/cli/ingest.py` | Ops or an automation runner producing local artifacts | Working for fixture-shaped bundles: it accepts a bundle and output directory and prints run, score, escalation, and artifacts (`pyproject.toml:53-55`, `src/inv_man_intake/cli/ingest.py:46-80`). |
| Python API | `run_pipeline`, `register_intake_bundle*`, `ingest_packet` | Sibling applications and integration code | Partial: callable local interfaces exist, but the primary run delegates to the V1 smoke core (`src/inv_man_intake/run.py:133-166`, `src/inv_man_intake/packet.py:75-147`). |
| Static HTML/Pyodide | `app/index.html`, `app/static_operator_app.js`, bridge | Analyst doing an offline visual review/demo | Working as a local demo surface; it requires an HTTP server, not `file://` (`README.md:50-73`), but it passes uploaded text—not binary file bytes—to Python (`app/static_operator_app.js:458-474`). |
| Queue contract | `validation_queue_api.py` | A Manager-Database-style analyst queue | Scaffold/contract only: documented query and pagination helpers, with no repository HTTP server (`README.md:22-33`). |
| Artifacts | `run.json`, `metadata.json`, `threshold-summary.json`, `explainability.json`, `manifest.json` | Automation and downstream reporting | Working: `run_pipeline` writes and hashes the four named outputs into a manifest (`src/inv_man_intake/run.py:337-363`, `src/inv_man_intake/run_manifest.py:45-94`). |

## 3. Structure map

```text
src/inv_man_intake/        domain package: intake, extraction, performance, scoring, storage, exports, observability
  data/, intake/, storage/ persistent hierarchy, registration, versions, SQLite and files
  extraction/, images/     parsers, confidence/routing, visual artifacts and feedback
  performance/, scoring/   return-series rules, metrics, conflict logic, weights and explanations
  queue/, audit/, export/  assignment/audit value objects and deliverable manifest/brief builders
app/                       static Pyodide operator demonstration and bundled browser assets
config/                    thresholds, scoring TOML, model policy, and a non-authoritative standard-elements stub
docs/                      plan, runbooks, and fleet/domain contracts
tests/                     deterministic unit, integration, browser and reference-fixture coverage
artifacts/                 committed reference run and telemetry examples
scripts/                   local validation/report helpers; workflow automation is synced from stranske/Workflows
.github/, design-system/  CI/agent materials and UI tokens; synced from stranske/Workflows where the manifest says so
```

## 4. Major code features you must understand to extend it

- **Registration — `register_intake_bundle`.** Validates JSON, normalizes or accepts firm/fund IDs, and returns an `IntakeRegistrationResult` plus optional document versions (`src/inv_man_intake/intake/integration.py:41-192`).
- **Packet assembly — `ingest_packet`.** Consumes `PacketFile` bytes and a service; classifies, checks coverage, reconciles, and returns a `ManagerProfile` (`src/inv_man_intake/packet.py:29-147`).
- **Extraction boundary — `ExtractionOrchestrator`.** Bounded primary/fallback attempts create correlation and escalation records; add providers here (`src/inv_man_intake/extraction/orchestrator.py:65-128`).
- **Current parsers.** PDF/PPTX providers emit canonical fields, page/slide provenance, and snippets, but are explicitly fixture-oriented (`src/inv_man_intake/extraction/providers/pdf_primary.py:20-83`, `src/inv_man_intake/extraction/providers/pptx_primary.py:24-86`).
- **Confidence gate.** `evaluate_thresholds` selects highest-confidence duplicates and escalates missing, low-confidence or duplicate mandatory facts (`src/inv_man_intake/extraction/confidence.py:232-288`).
- **Performance path.** Normalization, conflict resolution, metrics and human confirmation are separate; V1 supplies synthetic series (`src/inv_man_intake/v1_smoke.py:274-333`).
- **Scoring.** `compute_score` consumes TOML-backed asset-class weights; `build_explainability_payload` formats contributions (`src/inv_man_intake/v1_smoke.py:325-342`).
- **Versions/provenance.** Filesystem storage hashes bytes and atomically indexes idempotent versions; SQLite records fields and corrections (`src/inv_man_intake/storage/document_store.py:104-194`, `src/inv_man_intake/data/repository.py:306-357`).
- **Artifacts.** The run writer serializes reports and a hashed manifest—the practical hand-off boundary (`src/inv_man_intake/run.py:337-363`, `src/inv_man_intake/run_manifest.py:45-94`).

## 5. Data model, identifiers and contracts

The hierarchy is text-keyed `firms` → `funds` → `documents` (`src/inv_man_intake/data/repository.py:25-56`). Registration derives local firm/fund IDs unless supplied; aliases are JSON (`src/inv_man_intake/intake/integration.py:92-121`). Documents carry SHA-256 and dates; versions are chronological by fund/file, while file storage versions bytes by hash and receipt time (`src/inv_man_intake/data/repository.py:255-276`, `src/inv_man_intake/storage/document_store.py:121-152`). Fields carry document/page/snippet; corrections append (`src/inv_man_intake/data/provenance.py:8-31`).

| Contract/object | Code emits or consumes it? | Reality |
|---|---|---|
| `intake_contract` | Consumed by `validate_intake_payload` in registration | Working local validation (`src/inv_man_intake/intake/integration.py:41-90`). |
| Core schema/provenance history | Emitted to SQLite only when caller supplies a repository/store | Working optional persistence; normal CLI uses memory objects (`src/inv_man_intake/v1_smoke.py:180-193`). |
| `run-contract/v1` | Emitted by `RunResult.to_json` | Partial: it emits envelope fields, identity refs and page pointers (`src/inv_man_intake/run.py:75-130`). |
| `artifact-manifest/v1` | Emitted by `build_manifest` | Working, including hash/size (`src/inv_man_intake/run_manifest.py:45-94`). |
| `evidence-object/v1` | Documented only | No emitter creates objects with required `evidence_id`, `method`, and `excerpt`; current `evidence_refs` are strings (`docs/contracts/schemas/evidence-object-v1.schema.json:8-53`, `src/inv_man_intake/run.py:113-123`). |
| Identity-map convention | Partially emitted; not resolved against an authority | `run.json` emits `firm:` and `fund:` values, but no alias-resolution/backplane adapter consumes canonical forwarded IDs (`src/inv_man_intake/run.py:120-123`, `docs/contracts/identity-map-conventions.md:42-132`). |

## 6. External inputs and dependencies

Inputs are JSON bundles and local files. The contract permits PDF, PPTX, XLSX, DOCX and email notes, but included parsers are narrow PDF/PPTX; Docling is optional (`README.md:11-20`, `src/inv_man_intake/extraction/providers/docling_primary.py:16-88`). SQLite and ordinary files are its persistence; no Docker, server, FastAPI or database server is required. The static app needs local HTTP to fetch Pyodide (`README.md:50-58`).

Python 3.12+, `openpyxl`, `langsmith`, and shared PDF extraction are declared (`pyproject.toml:5-46`). LangSmith is optional; no key means in-memory tracing (`src/inv_man_intake/v1_smoke.py:409-433`). The LLM assistant requires consent and injected client and is not wired to a surface (`src/inv_man_intake/assist/intake_assistant.py:171-219`).

## 7. Current state

The package labels itself alpha (`pyproject.toml:15-22`). Gate: pytest with 80% branch coverage, Ruff and strict mypy (`pyproject.toml:62-117`). Here, targeted acceptance, static-bundle and manifest tests passed: **23 passed in 0.49s**—deterministic wiring, not production document handling (full suite: 116 test modules, 856 tests). Usable: local validation, explicitly configured local persistence, narrow PDF/PPTX extraction, scoring and hashed artifacts. Partial: real multi-format extraction, durable queue, browser upload and capacity evidence. Gaps:

- The main CLI executes `_run_pipeline_core`, which creates in-memory SQLite and an in-memory document store (`src/inv_man_intake/run.py:157-165`, `src/inv_man_intake/v1_smoke.py:180-193`).
- Default durable registration hashes synthesized placeholder content unless a filesystem resolver is supplied (`docs/runbooks/ingestion_lifecycle.md:68-103`).
- PDF parsing is explicitly unsuitable for production OCR/layout reconstruction (`src/inv_man_intake/extraction/providers/pdf_primary.py:20-26`).
- The standard-elements library is a non-authoritative stub and standardness always returns `unknown` (`docs/contracts/standard_element_library.md:3-35`).
- Localhost and remote extraction transports deliberately raise `NotImplementedError` (`src/inv_man_intake/extraction/service.py:59-70`).
- Throughput is explicitly a fixture-only lower bound that excludes real extraction and IO (`README.md:117-119`).
- V1 uses a hard-coded analyst and synthetic performance series (`src/inv_man_intake/v1_smoke.py:274-308`).

## 8. Claims vs reality

- **Claim:** intake contract validation covers PDF, PPTX, XLSX, Word, and email notes (`README.md:11-20`). **Reality:** intake metadata validation indeed accepts all five formats (`docs/contracts/intake_contract.md:41-47`), but end-to-end extraction is strictly narrower: `v1_smoke` only executes extraction for PDF/PPTX inputs and treats a named XLSX fixture as a boundary (`src/inv_man_intake/v1_smoke.py:215-233`). Arbitrary XLSX, Word, and email notes are not extracted by default providers.
- **Claim:** `inv-man-ingest` is production headless (`docs/runbooks/headless_ingest.md:1-18`). **Reality:** it delegates to `v1_smoke._run_pipeline_core`, which instantiates in-memory SQLite and an in-memory document store with synthetic performance series (`src/inv_man_intake/run.py:157-165`, `src/inv_man_intake/v1_smoke.py:180-193`).
- **Claim:** the static SPA is the live operator surface (`README.md:70-73`). **Reality:** it converts uploads to text, then uses fixed keyword rules—not binary-faithful PDF/PPTX ingestion (`app/static_operator_app.js:458-499`, `app/pyodide_packet_bridge.py:114-149`).
- **Claim:** the pipeline emits conformant `run-contract/v1` records with evidence references (`src/inv_man_intake/run.py:79, 113-123`). **Reality:** output envelopes populate `evidence_refs` with raw page-pointer strings (`document:<id>#page=<n>`) rather than `evidence_id` references pointing to validated `evidence-object/v1` records with mandatory excerpts and extraction methods (`docs/contracts/schemas/evidence-object-v1.schema.json:8-53`, `docs/contracts/run-contract-v1.md:15-17, 156-159`).

## 9. Interoperability hooks (for the fleet program)

This repo can offer: `run-contract/v1` envelopes, `artifact-manifest/v1` hashes, firm/fund identity refs, document metadata and SHA-256, extracted fields with `source_doc_id`, page, method, snippet and location, threshold decisions, explainability, and export-manifest provenance (`src/inv_man_intake/run.py:177-245`, `src/inv_man_intake/run_manifest.py:45-94`). A Manager-Database-like sibling can consume `ManagerProfile`, `validation_queue_api` response shapes, or the named JSON artifacts; a backplane collector can consume the run and manifest.

It should consume an authoritative identity-map resolver before joining on firm/fund. Its local generated IDs and free-text `aliases_json` are not guaranteed fleet canonical. It also needs actual `evidence-object/v1` files before a sibling can trust field-level provenance through a generic evidence API. Document vocabulary is another collision point: local types include package-specific labels, the standard-element library is deliberately non-authoritative (`docs/contracts/standard_element_library.md:3-35`), and identity refs emit non-conforming `firm:` prefixes instead of the closed vocabulary `manager:` (`docs/contracts/identity-map-conventions.md:79-132`). Use the contract’s closed entity vocabulary and explicit source-of-truth rule, not these names alone (`docs/contracts/identity-map-conventions.md:79-132`).

## 10. Reuse candidates

- `src/inv_man_intake/storage/document_store.py` — content-addressed local blob/version store with atomic index writes.
- `src/inv_man_intake/run_manifest.py` — safe, hashed named-artifact manifest builder.
- `src/inv_man_intake/extraction/service.py` — provider/service transport seam, including local Docling adapter.
- `src/inv_man_intake/extraction/orchestrator.py` — bounded retry, attempt audit, correlation and escalation envelope.
- `src/inv_man_intake/data/repository.py` — small SQLite hierarchy and append-only field-correction repository.
- `src/inv_man_intake/scoring/explainability.py` — deterministic component explanation formatter.
- `app/static_operator_app.js` and `app/pyodide_packet_bridge.py` — browser-local Pyodide packaging pattern, but only after replacing the text-only upload bridge.

## 11. Proposed direction (evidence-based)

- **Finish what is scaffolded:** make `run_pipeline` construct durable SQLite/filesystem stores and pass real-byte resolution through every input, replacing its smoke-core dependency (`src/inv_man_intake/run.py:157-165`, `docs/runbooks/ingestion_lifecycle.md:68-103`).
- **Finish what is scaffolded:** promote Docling or real format-specific providers behind `ExtractionService`, and stop presenting regex PDF/PPTX fixture extraction as a multi-format solution (`src/inv_man_intake/extraction/service.py:104-140`, `src/inv_man_intake/extraction/providers/pdf_primary.py:20-26`).
- **Finish what is scaffolded:** replace synthetic `_performance_series` and hard-coded assignment with extracted, persisted performance inputs and an actual queue adapter (`src/inv_man_intake/v1_smoke.py:274-308`).
- **Finish what is scaffolded:** emit one validated `evidence-object/v1` per extracted fact, carrying existing snippets, method, confidence and `SourceLocation`, then point `evidence_refs` at those IDs (`docs/contracts/schemas/evidence-object-v1.schema.json:8-99`).
- **New capability:** integrate an authoritative firm/fund identity resolver and persist aliases/provenance of the resolution; do not federate generated local slugs as truth (`docs/contracts/identity-map-conventions.md:94-132`).
- **New capability:** make the browser pass binary bytes to appropriate browser-capable parsers, or label it honestly as a text-preview demo (`app/static_operator_app.js:458-499`).
- **New capability:** measure a real-cost, representative package batch before committing to same-business-day service levels (`README.md:117-119`).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- It is a local-first way to inspect manager packages and generate a scored, traceable review packet without sending documents to a hosted application by default.
- Today it is strongest for controlled, text-bearing PDF and presentation examples—not arbitrary office documents or scanned manager materials.
- It can preserve document versions, hashes and page-level source pointers when configured with local durable storage.
- Treat the score as a transparent prioritization aid; exceptions and conflicts are designed for analyst review, not automatic investment decisions.
- For hand-off to another office tool, use the run record and hashed artifact list, but settle firm and fund identity in a shared authoritative system first.

Verified 2026-09-04T17:25:00Z by gemini: 50 claims checked, 3 corrected, 1 unverifiable.
