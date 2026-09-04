# Personal-repo reuse note — FAA, Reader, trip-planner → work fleet

**Date:** 2026-09-04 · **Scope:** Patterns and components from three personal repositories that can accelerate Inv-Man-Intake, Manager-Database, Pension-Data, Doc-Lineage, and shared infrastructure (Workflows). Each entry names a path, what it does, whether to **lift code** or **copy the pattern**, and a concrete adoption step.

**Judgment upfront:** The strongest reusable assets are *disciplines* (human-confirms-machine, registration never refutes sameness, content-hash immutability, data-zone egress gates), not domain modules. Lifting ranking or dedup code wholesale into investment tools would couple unrelated domains; lifting small, tested primitives (file locks, circuit breakers, provenance ledgers) is lower risk.

---

## Fine-Art-Archive

### Sidecar schema + field provenance ledger
**Path:** `clones/Fine-Art-Archive/src/fine_art_archive/sidecar.py`, `provenance.py`, `schemas/meta.schema.json`  
**What it does:** One JSON record per entity with `schema_version`, strict validation, and an additive `field_provenance` ledger (status, source, note, `prior_value`) per fact.  
**Lift vs pattern:** **Copy the pattern.** Pension-Data and Inv-Man-Intake already have field-level provenance tables; Doc-Lineage should adopt the same status vocabulary (`not_researched`, `available`, `conflicting`, …) for clause variables.  
**Adoption:** In Doc-Lineage, define `tracked-variable/v1` rows with a `field_provenance` block mirroring FAA; wire `provenance.completeness_report()` logic as a CI gate on synthetic EDGAR fixtures before first blackline ship.

### Registration confirms sameness (never refutes it)
**Path:** `clones/Fine-Art-Archive/src/fine_art_archive/identity/work_qid_uniqueness.py` (`WorkQidClaims`)  
**What it does:** Before assigning a canonical ID, scan incumbents; on collision, **decline** the write and record a note naming the holder. Registration can only confirm sameness; dedup passes adjudicate merges.  
**Lift vs pattern:** **Copy the pattern.**  
**Adoption:** In Pension-Data `entities/service.py`, add a pre-write guard on `manager:` / `fund:` canonical IDs: collision → queue row, never silent overwrite. In Inv-Man-Intake `register_intake_bundle`, treat duplicate firm/fund alias resolution the same way.

### Verification cascade (layered, blocking)
**Path:** `clones/Fine-Art-Archive/src/fine_art_archive/collect/verify.py`  
**What it does:** Composes checks (aspect ratio, perceptual hash, optional CLIP) into a `VerificationReport` with per-check `PASS`/`FAIL`/`SKIP` and an overall gate before acquisition commits.  
**Lift vs pattern:** **Copy the pattern** (interface + report shape).  
**Adoption:** Doc-Lineage M1 ingest: Layer 1 = PDF byte-hash + page count; Layer 2 = section-ID fingerprint; Layer 3 = semantic alignment score. Block blackline emit on `FAIL`. Inv-Man-Intake extraction orchestrator already has escalation records—map them to the same report struct.

### Concurrent-writer discipline
**Path:** `clones/Fine-Art-Archive/src/fine_art_archive/fixity.py` (`_sidecar_file_lock`, `_write_sidecar_atomic`); `api/main.py` (JSONL compaction under lock)  
**What it does:** Per-file `fcntl` locks, temp-file atomic replace, read errors propagate (writers cannot compact a log they failed to load). Manifest rebuild is separate from per-sidecar mutation.  
**Lift vs pattern:** **Lift the lock/atomic-write helpers** into Workflows `packages/` as `stranske_atomic_io` (≈40 lines); **copy the one-writer policy** elsewhere.  
**Adoption:** Manager-Database offline WASM demo and Inv-Man-Intake Pyodide operator app: document single-writer SQLite like Reader. Doc-Lineage artifact dir: one run writer per `run_id/`.

### Manifest gate (catalog ≠ corpus)
**Path:** `clones/Fine-Art-Archive/scripts/build_manifest.py`, `api/store.py`  
**What it does:** UI and batch jobs list only works present in `manifest.csv`; promotion requires explicit rebuild.  
**Lift vs pattern:** **Copy the pattern.**  
**Adoption:** Pension-Data review PWA: separate `published_facts.csv` manifest from raw staging tables; Inv-Man-Intake `run_manifest.py` already hashes outputs—add an explicit "analyst-visible" manifest slice the static app reads.

### Run-contract validator (opt-in)
**Path:** `clones/Fine-Art-Archive/scripts/validate_run_contract.py`  
**What it does:** Role-aware validation of `run-contract/v1` and `artifact-manifest/v1`; SKIP when repo not registered.  
**Lift vs pattern:** **Already lifted** via Workflows sync—do not fork.  
**Adoption:** Register FAA as `candidate` producer in Workflows `config/backplane_participants.json`; emit from one enrichment batch script to close the scaffold gap noted in the FAA dossier §8.

---

## Reader

### Adult confirms AI drafts
**Path:** `Principles.md` (P-A3, P-E3); `standards/progress.py` (`record_evidence` → `confirm_evidence`); app scoring flows  
**What it does:** Machine proposes miscues, questions, and provisional game evidence; **only adult-confirmed rows** become stored truth or mastery updates. Measurement (WCPM) stays separate from intervention (P-F2).  
**Lift vs pattern:** **Copy the pattern** (two-phase propose/confirm API).  
**Adoption:** Inv-Man-Intake `assist/intake_assistant.py` and Pension-Data `quality/confidence.py`: split `proposed_value` from `confirmed_value`; auto-accept only above threshold, else analyst queue. Manager-Database RAG: mark LLM answers `draft` until analyst pins citations.

### Local-first + serialized one-writer
**Path:** `README.md` (Dropbox-synced `reader.db`); `docs/draft_sync.md`  
**What it does:** Canonical SQLite on disk; **never two servers writing one DB**; drafts merge by `updated_at` with background reconcile.  
**Lift vs pattern:** **Copy the pattern.**  
**Adoption:** Document the same handoff in Inv-Man-Intake runbooks for shared `FAA_WORKS_DIR`-style intake roots; Pension-Data PostgreSQL deploy guide: single migration writer, read replicas optional.

### Standards evidence module
**Path:** `standards/schema_standards.sql`, `standards/progress.py`, `standards/README.md`  
**What it does:** CASE-ingested skill graph, evidence ledger, mastery rollup; `practice_kind='transfer'` never moves mastery; crosswalk is adult-mediated.  
**Lift vs pattern:** **Copy the pattern** (ledger + rollup), not the CASE ingest.  
**Adoption:** Pension-Data: map `fact:<hash>` staging rows to an evidence ledger table with `confirmed_by`; Doc-Lineage tracked variables use the same confirm path before export to Pension-Data staging.

### Principles registry (evidence-graded design constitution)
**Path:** `Principles.md`  
**What it does:** Each design rule carries mechanism, evidence level, anti-patterns, review cadence—copied from LMS `research_registry/schemas.py`.  
**Lift vs pattern:** **Copy the pattern** into each work repo as `docs/PRINCIPLES.md` stub.  
**Adoption:** Workflows template sync adds a one-page principles skeleton; Doc-Lineage principle P-1: "blackline classification is human-auditable."

---

## trip-planner

### Data-zone egress gate
**Path:** `clones/trip-planner/trip_planner/app/services/planner_runtime_config.py` (`TRIP_PLANNER_DATA_ZONE`)  
**What it does:** `proprietary` zone blocks OpenAI unless endpoint is explicitly authorized; defaults to deterministic fallback.  
**Lift vs pattern:** **Lift code** (small module) into Workflows `tools/data_zone.py`; wire per repo.  
**Adoption:** Inv-Man-Intake and Manager-Database: gate LangSmith and remote extraction behind `*_DATA_ZONE=proprietary`; CI runs with `synthetic` only.

### Source quality scorer
**Path:** `clones/trip-planner/trip_planner/sources/quality.py` (`SourceQualityScorer`)  
**What it does:** Fuses freshness, channel fit, provenance strength, and conflict state into a bounded confidence label for ranking explanations.  
**Lift vs pattern:** **Lift code** with renamed category priors (replace `managed_travel_policy` → `regulatory_filing`, etc.).  
**Adoption:** Inv-Man-Intake `extraction/confidence.py`: delegate duplicate-source resolution weights to shared scorer; Pension-Data `sources/ppd` and `sources/edgar` adapters attach `SourceRecord` metadata.

### HTTP circuit breaker
**Path:** `clones/trip-planner/trip_planner/integrations/tpp/client.py` (`_CircuitBreaker`)  
**What it does:** Host-keyed breaker with exponential backoff and typed error taxonomy for remote policy calls.  
**Lift vs pattern:** **Lift code** to Workflows `packages/` (already mirrored in Manager-Database dossier §10).  
**Adoption:** Manager-Database `adapters/edgar.py` and Pension-Data HTTP clients: wrap SEC/PPD calls; open breaker → fixture fallback in CI.

### Multicriteria ranking engine
**Path:** `clones/trip-planner/trip_planner/ranking/base.py` (`BaseRankingEngine`)  
**What it does:** Weighted attribute scoring with explanation payloads for ranked scenarios.  
**Lift vs pattern:** **Copy the pattern** (engine interface + explanation dict), not leisure/business profiles.  
**Adoption:** Inv-Man-Intake `scoring/`: emit per-dimension contributions matching `RankedResultSet` shape for manager prioritization dashboards.

### Complexity ceiling enforcer
**Path:** `clones/trip-planner/scripts/measure_complexity.py`  
**What it does:** AST-based cyclomatic complexity gate (ceiling 25) in CI.  
**Lift vs pattern:** **Lift code** via Workflows sync to all Python repos missing it.  
**Adoption:** Add to Workflows `reusable-10-ci-python.yml` optional job; enable in Doc-Lineage from day one.

---

## Cross-repo adoption matrix

| Work target | Highest-value imports | First step |
|-------------|----------------------|------------|
| **Inv-Man-Intake** | Reader confirm gate; trip-planner data-zone + source quality; FAA provenance statuses | Add `proposed`/`confirmed` field writes in `data/provenance.py`; register scorer categories in `config/thresholds.toml` |
| **Manager-Database** | trip-planner circuit breaker (lift); FAA atomic IO; Reader draft-vs-truth for RAG | Wrap `adapters/edgar.py` with breaker; require analyst pin on `chains/evidence.py` outputs |
| **Pension-Data** | FAA registration guard; Reader evidence ledger; trip-planner source quality | Extend `entities/service.py` collision decline; add `confirm_evidence` analogue to `review_queue/extraction.py` |
| **Doc-Lineage** (greenfield) | FAA sidecar + verify + provenance; Reader confirm; Pension-Data hash lineage | Ship M1 with `doc:<sha256>` IDs, variable ledger, static HTML page links per R1/R2 briefs |
| **Workflows / infra** | FAA `validate_run_contract` (done); trip-planner `measure_complexity`, data-zone, circuit breaker; Reader principles template | One PR: `tools/data_zone.py` + sync manifest entry; principles template in `templates/consumer-repo/docs/` |

---

## What not to reuse

- **FAA preference learning** (`preference/bradley_terry.py`, `selection/lenses.py`): domain-specific taste model; not transferable to manager scoring without new labels.
- **Reader FSRS scheduling**: depends on LMS mastery graph; Pension-Data has its own bitemporal facts—do not merge schedulers.
- **trip-planner leisure ranking profiles**: business policy compiler shape is useful; vacation weights are not.
- **FAA DINOv2 / vision dedup**: operational GPU cache off-repo; Inv-Man-Intake image path should use `stranske_pdf_extract`, not art embeddings.

---

## Confidence and open risks

**Confidence: high** on discipline patterns (confirm gate, registration guard, data zone, atomic IO)—they are small, tested, and align with existing fleet contracts. **Medium** on lifting `SourceQualityScorer` without calibrating investment-specific category priors. **Low** on any cross-domain ranking lift until asset-class weights are validated against Inv-Man-Intake fixtures.

**Would change my mind:** If Workflows `stranske_pdf_extract` ships first, Doc-Lineage and Inv-Man-Intake should prefer its `EvidenceRef` contract over FAA sidecar fields for page citations—FAA provenance becomes a pattern reference only.

Verified against dossiers and clone paths under `research-program/clones/` and Reader at `~/Library/CloudStorage/Dropbox/Learning/Code/Reader` on 2026-09-04.
