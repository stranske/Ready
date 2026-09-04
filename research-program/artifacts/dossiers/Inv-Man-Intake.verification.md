# Inv-Man-Intake dossier — verification table

Verified against clone `clones/Inv-Man-Intake` at HEAD `8778d10c1e3240c9e008c2a223e910e05bf631f2` (2026-09-04).
Method: every cited file:line/symbol opened and verified against current code and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 46 |
| WRONG (corrected in dossier) | 3 |
| UNVERIFIABLE | 1 |
| **Total checked** | **50** |

### Key Findings & Corrections

1. **§4 Registration return type:** The dossier stated that `register_intake_bundle` returns an `IngestRecord`. Opening `src/inv_man_intake/intake/integration.py:41-192` shows that it returns `IntakeRegistrationResult` (which carries `accepted`, `package_id`, `status`, `errors`, `warnings`, and `persisted_documents`). `IngestRecord` is an internal object created and stored on `IngestionService`.
2. **§8 Format handling refutation (adversarial check):** The dossier refuted `README.md:11-20` by asserting that the README claims "all five listed formats are handled" when only PDF/PPTX are extracted. Opening `README.md:13` reveals that the README specifically claims **"Intake contract validation for PDF, PPTX, XLSX, Word, and email-note package inputs"**, which is completely true and verified by `docs/contracts/intake_contract.md:41-47` and `src/inv_man_intake/intake/integration.py:41-90`. Refuting multi-format extraction against a contract-validation claim was a false refutation against a strawman. The corrected statement clarifies that intake validation handles all 5 formats while execution/extraction handles only PDF/PPTX.
3. **§8 Evidence-object interoperability claim attribution:** The dossier cited `docs/contracts/run-contract-v1.md:156-159` as claiming evidence-object interoperability. However, `run-contract-v1.md:15-17` explicitly warns: *"No participant emits an envelope yet (that is P1+); nothing here is wired into any repo's CI."* The actual overclaim/gap originates in `src/inv_man_intake/run.py:79, 113-123`, where the pipeline stamps its emitted record `"schema_version": "run-contract/v1"` but populates `evidence_refs` with unstandardized page-pointer strings (`document:<id>#page=<n>`) instead of valid `evidence-object/v1` IDs.
4. **Path / link fixes:** All markdown citations in the original dossier were prefixed with `../` (e.g. `[README.md:3-20](../README.md)`), which broke resolution from `artifacts/dossiers/`. All citations have been sanitized to clean repo-relative paths.

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | `register_intake_bundle` validates JSON, normalizes firm/fund IDs, returns IngestRecord | `src/inv_man_intake/intake/integration.py:41-150` | **WRONG** | Returns `IntakeRegistrationResult` (with `persisted_documents`), not `IngestRecord`. Line range extends to `:41-192`. |
| 2 | `ingest_packet` consumes `PacketFile` bytes & service, returns `ManagerProfile` | `src/inv_man_intake/packet.py:29-147` | CONFIRMED | `PacketFile` (:29-36), `ManagerProfile` (:51-73), `ingest_packet` (:75-147). |
| 3 | `ExtractionOrchestrator` bounded primary/fallback attempts create correlation & escalation | `src/inv_man_intake/extraction/orchestrator.py:65-128` | CONFIRMED | Bounded retry loop, `AttemptRecord`, correlation ID, and escalation records confirmed. |
| 4 | PDF/PPTX providers emit canonical fields, page/slide provenance, snippets; fixture-oriented | `src/inv_man_intake/extraction/providers/pdf_primary.py:20-83`, `src/inv_man_intake/extraction/providers/pptx_primary.py:24-86` | CONFIRMED | Both classes present, regex/stream parsing, explicit fixture-only docstrings. |
| 5 | `evaluate_thresholds` selects highest-confidence duplicates, escalates missing/duplicate | `src/inv_man_intake/extraction/confidence.py:232-288` | CONFIRMED | Deduplicates by max confidence (:235-246), evaluates coverage, flags duplicate/missing mandatory fields (:259-277). |
| 6 | Performance normalization, conflict resolution, metrics separate; synthetic V1 series | `src/inv_man_intake/v1_smoke.py:274-333` | CONFIRMED | `_performance_series()` generates synthetic monthly inputs; conflict resolution, normalization, metrics, and queue assignment staged separately. |
| 7 | `compute_score` consumes TOML weights; `build_explainability_payload` formats contributions | `src/inv_man_intake/v1_smoke.py:325-342` | CONFIRMED | `compute_score` uses `weights_for_registry()` (`config/scoring_weights/*.toml` via `tomllib`), explainability formatted. |
| 8 | Filesystem storage hashes bytes, atomically indexes versions; SQLite records fields/corrections | `src/inv_man_intake/storage/document_store.py:104-194`, `src/inv_man_intake/data/repository.py:306-357` | CONFIRMED | `FilesystemDocumentStore` writes temp files and replaces atomic index; `FieldProvenanceRepository` appends corrections. |
| 9 | Run writer serializes reports and hashed manifest | `src/inv_man_intake/run.py:337-363`, `src/inv_man_intake/run_manifest.py:45-94` | CONFIRMED | Writes 4 JSON reports + `manifest.json` with SHA-256 and byte sizes. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 10 | Hierarchy is text-keyed `firms` → `funds` → `documents` | `src/inv_man_intake/data/repository.py:25-56` | CONFIRMED | Schema script defines tables with `TEXT PRIMARY KEY` and foreign keys. |
| 11 | Registration derives local firm/fund IDs unless supplied; aliases stored as JSON | `src/inv_man_intake/intake/integration.py:92-121` | CONFIRMED | `_stable_identifier` normalizes fallback IDs; `aliases_json` column maintained. |
| 12 | Documents carry SHA-256 and dates; versions chronological by fund/file | `src/inv_man_intake/data/repository.py:255-276` | CONFIRMED | `list_document_versions` queries ordered by `version_date ASC, received_at ASC`. |
| 13 | File storage versions bytes by hash and receipt time | `src/inv_man_intake/storage/document_store.py:121-152` | CONFIRMED | `build_version_id` combines SHA-256 and ISO received timestamp. |
| 14 | Fields carry document/page/snippet; corrections append | `src/inv_man_intake/data/provenance.py:8-31` | CONFIRMED | `ExtractedFieldRecord` and `CorrectionRecord` dataclasses define these fields. |
| 15 | `intake_contract` consumed by `validate_intake_payload` in registration | `src/inv_man_intake/intake/integration.py:41-90` | CONFIRMED | Calls `validate_intake_payload(bundle)` and handles structured validation errors. |
| 16 | Core schema/provenance history emitted to SQLite only with supplied store; CLI uses in-memory | `src/inv_man_intake/v1_smoke.py:180-193` | CONFIRMED | CLI calls `_run_pipeline_core` with `sqlite3.connect(":memory:")` and `InMemoryDocumentStore`. |
| 17 | `run-contract/v1` emitted by `RunResult.to_json` | `src/inv_man_intake/run.py:75-130` | CONFIRMED | Emits envelope, inputs, outputs, fields, latency, warnings, and provenance. |
| 18 | `artifact-manifest/v1` emitted by `build_manifest` with hash/size | `src/inv_man_intake/run_manifest.py:45-94` | CONFIRMED | Constructs schema-valid manifest mapping artifact paths to SHA-256 and size in bytes. |
| 19 | `evidence-object/v1` documented only; current `evidence_refs` are strings | `docs/contracts/schemas/evidence-object-v1.schema.json:8-53`, `src/inv_man_intake/run.py:113-123` | CONFIRMED | Schema requires `evidence_id`, `method`, `excerpt`; `run.py` only emits `document:<id>#page=<n>` strings. |
| 20 | Identity-map convention partially emitted; not resolved against authority | `src/inv_man_intake/run.py:120-123`, `docs/contracts/identity-map-conventions.md:42-132` | CONFIRMED | Emits non-canonical `firm:<id>` (convention closed vocabulary specifies `manager:`), with no external resolver. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement |
|---|---|---|---|---|
| 21 | **Claim: all five listed formats are handled** | `README.md:11-20`, `src/inv_man_intake/v1_smoke.py:215-233` | **WRONG (false refutation)** | `README.md:13` claims **intake contract validation** for 5 formats, not multi-format extraction. Intake validation genuinely validates metadata for all 5 formats (`docs/contracts/intake_contract.md:41-47`). The true gap is that execution/extraction is only implemented for PDF/PPTX fixtures and a boundary XLSX. |
| 22 | **Claim: `inv-man-ingest` is production headless** | `docs/runbooks/headless_ingest.md:1-18`, `src/inv_man_intake/run.py:157-165`, `src/inv_man_intake/v1_smoke.py:180-193` | CONFIRMED | Runbook describes it as the production orchestrator-callable counterpart to smoke pipeline, but it delegates directly to `_run_pipeline_core` using in-memory SQLite and synthetic series. |
| 23 | **Claim: static SPA is live operator surface** | `README.md:70-73`, `app/static_operator_app.js:458-499`, `app/pyodide_packet_bridge.py:114-149` | CONFIRMED | README lines 70-73 declare it the sole live surface, but uploaded files are passed as text strings to Pyodide where `_BrowserTextProvider` uses fixed keyword matching (`"summit arc"`, `"aum"`, etc.) rather than binary PDF/PPTX parsing. |
| 24 | **Claim: run contract supplies evidence-object interoperability** | `docs/contracts/run-contract-v1.md:156-159`, `src/inv_man_intake/run.py:113-123`, `docs/contracts/schemas/evidence-object-v1.schema.json:3-58` | **WRONG (claim attribution)** | `docs/contracts/run-contract-v1.md:15-17` explicitly notes no participant emits an envelope yet. The actual defect is in `src/inv_man_intake/run.py:79, 113-123`, which stamps `"run-contract/v1"` while emitting raw page-pointer strings instead of valid `evidence-object/v1` IDs. |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 25 | Offers `run-contract/v1` envelopes, `artifact-manifest/v1` hashes, identity refs, metadata, fields, thresholds, explainability | `src/inv_man_intake/run.py:177-245`, `src/inv_man_intake/run_manifest.py:45-94` | CONFIRMED | `RunResult` and `build_manifest` construct these exact payload structures. |
| 26 | Manager-Database sibling can consume `ManagerProfile`, `validation_queue_api` response shapes, or artifacts | `src/inv_man_intake/validation_queue_api.py`, `src/inv_man_intake/packet.py:51-74` | **UNVERIFIABLE (off-clone)** | Shapes and export helpers exist locally; consumption by external sibling requires external test. |
| 27 | Must consume authoritative identity-map resolver before joining on firm/fund | `docs/contracts/identity-map-conventions.md:79-132` | CONFIRMED | Manager-Database is authoritative for `manager`; Inv-Man-Intake generated slugs and free-text aliases are non-authoritative. |
| 28 | Needs actual `evidence-object/v1` files before field provenance can be trusted via generic API | `docs/contracts/schemas/evidence-object-v1.schema.json:8-53`, `src/inv_man_intake/run.py:113-123` | CONFIRMED | Fleet evidence schema requires `evidence_id`, `method`, and `excerpt`; current string pointers cannot satisfy schema. |
| 29 | Document vocabulary collision: package labels, non-authoritative stub, non-standard `firm:` prefix | `docs/contracts/standard_element_library.md:3-35`, `docs/contracts/identity-map-conventions.md:79-132` | CONFIRMED | Element stub returns `unknown`; `identity_refs` emits `firm:` which is outside closed entity vocabulary (`manager`). |

---

## §1, §2, §6, §7, §10, §11 — Supporting Claims

| # | Section | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|---|
| 30 | §1 | Headless intake pipeline, purpose, and no-egress constraints | `README.md:3-20, 22-38, 50-58`, `src/inv_man_intake/run.py:133-166` | CONFIRMED | Stated constraints and headless pipeline design verified. |
| 31 | §2 | CLI surface working for fixture bundles | `pyproject.toml:53-55`, `src/inv_man_intake/cli/ingest.py:46-80` | CONFIRMED | Console script entry point and argument parsing confirmed. |
| 32 | §2 | Python API partial; delegates to smoke core | `src/inv_man_intake/run.py:133-166`, `src/inv_man_intake/packet.py:75-147` | CONFIRMED | `run_pipeline` delegates to `_run_pipeline_core`. |
| 33 | §2 | Static Pyodide demo requires local HTTP, text upload | `README.md:50-73`, `app/static_operator_app.js:458-474` | CONFIRMED | Direct `file://` unsupported; text passed to Pyodide. |
| 34 | §2 | Queue contract scaffold only, no HTTP server | `src/inv_man_intake/validation_queue_api.py`, `README.md:22-33` | CONFIRMED | In-process query/filter functions only; no web framework. |
| 35 | §2 | Run writes 4 JSON outputs and hashes into manifest | `src/inv_man_intake/run.py:337-363`, `src/inv_man_intake/run_manifest.py:45-94` | CONFIRMED | Verified output artifact files and hashing. |
| 36 | §6 | Docling dependency is optional | `README.md:11-20`, `src/inv_man_intake/extraction/providers/docling_primary.py:16-88` | CONFIRMED | Guarded import raising `MissingDoclingDependencyError`. |
| 37 | §6 | Python 3.12+, openpyxl, langsmith, stranske-pdf-extract | `pyproject.toml:5-46` | CONFIRMED | Dependencies declared in project metadata. |
| 38 | §6 | LangSmith optional; in-memory tracing fallback | `src/inv_man_intake/v1_smoke.py:409-433` | CONFIRMED | Checks `LANGSMITH_API_KEY`; defaults to in-memory tracer. |
| 39 | §6 | LLM assistant requires consent/client, not wired to UI | `src/inv_man_intake/assist/intake_assistant.py:171-219` | CONFIRMED | Guarded function requiring explicit consent and injected client. |
| 40 | §7 | Alpha classifier, 80% branch coverage, Ruff, strict mypy | `pyproject.toml:15-22, 62-117` | CONFIRMED | Settings in `pyproject.toml` confirmed. |
| 41 | §7 | Targeted tests pass 23 in ~0.5s | `tests/test_v1_acceptance_smoke.py`, `tests/test_offline_static_bundle.py`, `tests/test_packet_pipeline.py` | CONFIRMED | Exact 23 tests collected and passed in 0.59s (repo total: 116 test files, 856 tests). |
| 42 | §7 | Main CLI creates in-memory SQLite and document store | `src/inv_man_intake/run.py:157-165`, `src/inv_man_intake/v1_smoke.py:180-193` | CONFIRMED | Verified instantiation of `:memory:` database and memory store. |
| 43 | §7 | Default durable registration hashes placeholder content | `docs/runbooks/ingestion_lifecycle.md:68-103` | CONFIRMED | Uses `deterministic_fixture_content` unless resolver passed. |
| 44 | §7 | PDF primary provider unsuitable for OCR/layout | `src/inv_man_intake/extraction/providers/pdf_primary.py:20-26` | CONFIRMED | Provider docstring explicitly notes limitation. |
| 45 | §7 | Standard element library stub returns `unknown` | `docs/contracts/standard_element_library.md:3-35` | CONFIRMED | `classify_element_standardness` returns `unknown`. |
| 46 | §7 | Future transport backends raise `NotImplementedError` | `src/inv_man_intake/extraction/service.py:59-70` | CONFIRMED | `StubServiceTransportBackend.extract_document` raises error. |
| 47 | §7 | Throughput command reports synthetic lower-bound | `README.md:117-119` | CONFIRMED | Readme explicitly notes it excludes real extraction/IO cost. |
| 48 | §7 | V1 uses hard-coded analyst and synthetic performance | `src/inv_man_intake/v1_smoke.py:274-308` | CONFIRMED | `analyst_001` and `_performance_series()` hardcoded. |
| 49 | §10 | All 8 reuse candidate paths exist and match roles | `storage/document_store.py`, `run_manifest.py`, `extraction/service.py`, `extraction/orchestrator.py`, `data/repository.py`, `scoring/explainability.py`, `app/static_operator_app.js`, `app/pyodide_packet_bridge.py` | CONFIRMED | All 8 components present and implement the cited responsibilities. |
| 50 | §11 | Evidence-backed proposed directions | `run.py`, `service.py`, `pdf_primary.py`, `v1_smoke.py`, schemas | CONFIRMED | All recommendations align directly with verified implementation gaps. |
