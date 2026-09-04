# B3 — Interoperability Architecture: Identity, Typology, Tracked Variables, Lineage

**Date:** 2026-09-04 · **Author:** Cursor (Composer) · **Status:** Research architecture for fleet mutual intelligibility  
**Inputs:** `artifacts/dossiers/00-INDEX.md`, Workflows/Inv-Man-Intake/Pension-Data contracts, Manager-Database identity code, R1–R4 briefs  
**Owner constraint:** No single repo is the mandated identity or evidence authority; the design must work with the existing resource set.

---

## Executive judgment

**JUDGMENT:** Fleet interoperability is achievable without a central resolver or new service. The correct shape is **convention-first federation**: Workflows owns wire formats and closed vocabularies (synced like today's `run-contract/v1` set); each repo keeps its native storage and resolution logic; **cross-walk files** and optional `identity-map/v1` artifacts bridge joins at export time. A shared identity *library* is worth adding only as deterministic normalization helpers (CIK padding, token folding) — not as a runtime authority.

**JUDGMENT:** The strongest objection to the current `identity-map-conventions.md` is its "authoritative repo" table: it contradicts the owner's no-single-authority constraint and papers over the integer `manager_id` vs `manager:cik_*` collision. B3 replaces "authority" with **declared resolution surfaces** — repos that *publish* canonical IDs and alias maps, without mandating that all consumers route through them.

**JUDGMENT:** `tracked-variable/v1` (one family for legal clauses, report sections, and thesis claims) is the right unification layer proposed in R1/R2/R3. It should embed `evidence-object/v1` and dual provenance (document+page **and** mirror path + source-system URL).

**Confidence:** High on wire-format extension and adoption via Workflows sync; medium on cross-repo join rates without mandatory alias backfill; low on Backstop permalink stability until a real export sample exists (R4). **Would change my mind:** Two independent repos joining ≥90% of shared manager mentions via federation cross-walks alone, without any repo claiming authority.

---

## 1. Identity layer

### 1.1 Problem statement

The fleet index documents **HIGH** collision risk on manager and fund identifiers: Manager-Database uses integer `manager_id` with `cik`/`lei`/`aliases text[]` (`schema.sql`); Pension-Data emits `manager:<normalized_token>` via `build_canonical_stable_id` (`entities/service.py:54–67`); Inv-Man-Intake uses slug-only firm names with `aliases_json` unset; Counter_Risk has validated `canonical_key` values that never surface in run outputs. Document IDs split across `document:<sha256>`, `artifact:<digest>`, and `plan:` prefixes. No repo yet emits conformant standalone `evidence-object/v1` files despite internal evidence models in Pension-Data and Manager-Database.

Mutual intelligibility requires: (a) a **stable interchange ID** for joins, (b) **alias maps** that do not require a central database, and (c) explicit **confidence** when resolution is best-effort.

### 1.2 Options evaluated

| Option | Description | Strengths | Weakest objection |
|--------|-------------|-----------|-------------------|
| **A. Shared identity library (Workflows-synced)** | Python package or `scripts/identity/` synced fleet-wide: `normalize_cik`, `to_canonical_id(entity_type, keys)`, `load_crosswalk(path)` | Matches contract-sync pattern; offline/deterministic; no new infra | **Still needs a cross-walk source** — a library without published maps does not fix Inv-Man-Intake slugs; risk of becoming a shadow authority if it hosts merge decisions |
| **B. Small identity service** | HTTP API resolving names → canonical IDs, backed by Manager-DB or a new DB | Single query endpoint; familiar pattern | **Violates owner constraint** and prototype scope (`identity-map-conventions.md` §"global entity service … explicitly out of scope"); adds ops burden; makes work-PC/no-server path depend on network |
| **C. Convention + cross-walk files** | Workflows owns ID *format* and `identity-map/v1` JSON Schema; authoritative repos *publish* maps as versioned artifacts; consumers resolve locally | Works with existing Manager-DB `resolve_aliases.py`, Pension-Data `merge_canonical_entities`, Counter_Risk registry; no runtime coupling | Join quality depends on map freshness; requires discipline to emit maps on schedule |
| **D. Status quo (conventions only, no maps)** | Keep `identity-map-conventions.md` emission rules | Zero new files | **Fails silently** — Inv-Man-Intake "Summit Arc Advisors" vs "…LLC" fragmentation persists; dossier shows 1/6 repos conformant on run-contract |

### 1.3 Recommendation: C + thin A

**Adopt convention + cross-walk federation**, with **thin normalization helpers** synced from Workflows (option A scoped to formatting only).

**Rationale:**

1. **Matches existing production code.** Manager-Database already resolves EDGAR names into `aliases` arrays (`resolve_aliases.py:112–191`). Pension-Data already merges canonical entities forward. Counter_Risk already validates `canonical_key`. None of this should move to Workflows — only the *export shape* should align.

2. **Satisfies no-single-authority.** Multiple repos may publish overlapping maps for the same `entity_type`. Consumers apply a **merge policy** (see §1.4), not a single upstream.

3. **Rejects the identity service** for the prototype. The fleet's analyst path is local-first (R3, R4); a resolver service is the wrong failure mode.

4. **Rejects library-as-authority.** Sync `tools/identity_normalize.py` (CIK/LEI padding, `normalize_entity_token` compatible folding) — not `resolve_manager(name) → id`.

### 1.4 Canonical ID format (retain, clarify)

Keep the regex and shape from `identity-map-conventions.md`:

```
^[a-z0-9_]+:[a-z0-9][a-z0-9_.:-]*$
```

Examples unchanged: `manager:cik_0001067983`, `fund:lei_5493001kjtiigc8y1r12`, `pension:calpers`.

**Amendment:** Replace the "authoritative source-of-truth repo" table with **resolution surfaces**:

| `entity_type` | Primary resolution surface (publishes maps) | Secondary surfaces |
|---------------|---------------------------------------------|--------------------|
| `manager` | Manager-Database (`manager_id` + `cik` + `aliases`) | Pension-Data manager tokens in extractions |
| `fund` | Pension-Data `build_canonical_stable_id` | Inv-Man-Intake `funds` table |
| `pension` | Pension-Data plan IDs | — |
| `provider` | Counter_Risk name registry | Manager-Database `registry_ids` |
| `person` | Pension-Data / Manager-Database signatory extractions | — |
| `strategy` | Inv-Man-Intake asset-class registry | Trend_Model column labels (consumer, must map in) |

When surfaces disagree, emit **both** IDs in `identity_refs` with `data_quality.conflict: true` on the run envelope — do not pick a silent winner.

### 1.5 Cross-walk artifact (`identity-map/v1`)

Published as a run artifact (not a live API), regenerated on schedule or after alias resolution jobs:

```json
{
  "schema_version": "identity-map/v1",
  "publisher": "stranske/Manager-Database",
  "published_at": "2026-09-04T18:00:00Z",
  "entity_type": "manager",
  "entries": [
    {
      "canonical_id": "manager:cik_0001067983",
      "aliases": ["berkshire hathaway inc", "berkshire hathaway"],
      "native_keys": { "manager_id": 42, "cik": "0001067983", "lei": null },
      "supersedes_ids": ["manager:berkshire_hathaway"],
      "confidence": 1.0
    }
  ]
}
```

**Join algorithm (consumer-local):**

1. Normalize surface string via shared token rules.
2. Match against `aliases` in all ingested maps for the `entity_type` (order-independent).
3. On multiple canonical hits → surface conflict on run; on zero hits → emit name-anchored fallback ID with `confidence < 1.0` on linked evidence.
4. Walk `supersedes_ids` chains to current ID (same discipline as Pension-Data entity merge).

Integer `manager_id` **never** appears in `identity_refs`; it lives only in `native_keys` for round-trip to Manager-Database.

---

## 2. Document typology

### 2.1 Requirement

Cross-repo pipelines (Doc-Lineage, Inv-Man-Intake, Pension-Data orchestration, consultant HTML tools) must refer to the same **document type** when routing extractors, coverage gates, and mirror ingest rules. Today each repo uses local enums or implicit conventions (dossier §2.3 lists 13F-HR, Form 5500, DDQ, consultant reports, etc. without a fleet registry).

### 2.2 Closed vocabulary with aliases

Workflows owns `document-type-vocabulary/v1` — a JSON data file synced fleet-wide, structurally mirroring Inv-Man-Intake's Standard Element Library pattern (`standard_element_library.md`: types are data, not Python enums).

**Core types (v1 seed, ~30 entries):**

| `doc_type_id` | Covers | Alias examples (repo-local → fleet) |
|---------------|--------|-------------------------------------|
| `legal.ppm` | Private placement memorandum | `PPM`, `offering_memorandum` |
| `legal.lpa` | Limited partnership agreement | `LPA`, `partnership_agreement` |
| `legal.side_letter` | LP-specific side letter | `side_letter`, `sideletter` |
| `legal.amendment` | Amended/restated agreement | `amendment`, `amended_and_restated` |
| `dd.diligence_questionnaire` | DDQ / RFI | `DDQ`, `due_diligence_questionnaire` |
| `dd.manager_presentation` | Marketing/deck PDF | `pitch_deck`, `presentation` |
| `dd.call_notes` | Meeting/call notes | `meeting_notes`, `call_note` |
| `report.consultant_review` | Consultant trust review | `consultant_report`, `trust_review` |
| `report.manager_letter` | Manager periodic letter | `quarterly_letter`, `investor_letter` |
| `report.board_packet` | Board agenda attachment | `board_book`, `agenda_attachment` |
| `regulatory.form_5500` | ERISA Form 5500 | `5500`, `form5500` |
| `regulatory.form_13f` | 13F-HR holdings | `13F`, `13F-HR` |
| `regulatory.form_13d` | 13D/G activism | `13D`, `13G` |
| `financial.actuarial_valuation` | Actuarial / PPD | `PPD`, `actuarial_report` |
| `operational.exposure_workbook` | Counterparty exposure | `MOSERS`, `CPRS` (Counter_Risk) |
| `operational.trip_plan` | Travel governance | `TripPlan`, `trip_plan_json` |

**Schema sketch:**

```json
{
  "schema_version": "document-type-vocabulary/v1",
  "version": "2026.09.04",
  "types": {
    "legal.lpa": {
      "label": "Limited Partnership Agreement",
      "aliases": ["lpa", "limited_partnership_agreement", "partnership_agreement"],
      "default_extractors": ["doc_lineage.clause_variable"],
      "related_entity_types": ["manager", "fund"]
    }
  }
}
```

Repos map inbound labels through `aliases` at ingest; **never** branch on repo-specific strings in shared code. Inv-Man-Intake's `doc_types` keys in the standard element library become **subset references** into this vocabulary (`dd.diligence_questionnaire` → element list).

### 2.3 Document instance IDs

Unify on **content-addressed primary keys** with logical secondary keys:

- **Interchange ID:** `document:<sha256>` (full content hash of normalized bytes)
- **Run/manifest ID:** `artifact:<24-hex>` (Pension-Data pattern for supersession chains)
- **Mirror UID:** `doc:<stable-logical-key>` (R4 `document-mirror/v1`)

A `document-registry/v1` row links all three plus `doc_type_id`, `entity_refs[]`, and `source_refs[]` (Backstop URL, SharePoint `driveId`+`itemId`). This is the bridge between Pension-Data's `artifact:` IDs and Inv-Man-Intake's `(fund_id, file_name)` versioning.

---

## 3. Tracked-variable schema

### 3.1 One family for clause, report-section, thesis-claim

R1 (legal clauses), R2 (consultant sections), and R3 (thesis monitoring) converge on the same unit: an **asserted claim** with ontology key, typed value, evidence, and supersession. Differences are vocabulary files only.

**`tracked-variable/v1` schema sketch:**

```json
{
  "schema_version": "tracked-variable/v1",
  "variable_id": "var:8f3a2b1c9d4e",
  "ontology_key": "legal.withdrawal.notice_days",
  "ontology_family": "clause",
  "document_id": "document:abc123…",
  "artifact_id": "artifact:def456…",
  "entity_ref": "manager:cik_0001067983",
  "period": "2025-Q4",
  "status": "present",
  "value_text": "90 days written notice",
  "value_structured": { "notice_days": 90, "unit": "calendar" },
  "change_class": null,
  "confidence": 0.91,
  "supersedes_variable_id": null,
  "provenance": {
    "document": {
      "source_id": "document:abc123…",
      "locator": { "page": 42, "section": "7.3", "bbox": [72, 400, 540, 520] }
    },
    "mirror": {
      "mirror_root": "/path/to/mirror",
      "blob_path": "blobs/sha256/ab/cd/abc123…",
      "page_anchor": "#page=42"
    },
    "source_system": {
      "system": "backstop",
      "url": "https://…",
      "exported_at": "2026-09-04T12:00:00Z"
    }
  },
  "evidence": {
    "schema_version": "evidence-object/v1",
    "evidence_id": "ev:…",
    "fact_ref": "legal.withdrawal.notice_days",
    "source_id": "document:abc123…",
    "method": "parser",
    "excerpt": "…≤2000 chars…",
    "locator": { "page": 42, "section": "7.3" },
    "entity_ref": "manager:cik_0001067983",
    "confidence": 0.91
  },
  "extracted_at": "2026-09-04T18:00:00Z",
  "extractor_run_id": "sha256:…"
}
```

### 3.2 Field semantics

| Field | Purpose |
|-------|---------|
| `ontology_key` | Cross-manager join key (`consultant.performance_attribution`, `legal.gate.provisions`, `thesis.capacity_constraint`) |
| `ontology_family` | `clause` \| `report_section` \| `thesis_claim` — selects vocabulary file, same wire shape |
| `document_id` vs `artifact_id` | `document_id` is content hash; `artifact_id` is ingest-run identity with supersession chain |
| `provenance.document` | Primary anchor for one-click page navigation (owner non-negotiable) |
| `provenance.mirror` | Local blob path for offline work PC (R4) |
| `provenance.source_system` | Backstop/SharePoint back-link; best-effort until API validated |
| `evidence` | Embedded `evidence-object/v1` — required `method`, `excerpt` (string or explicit null) |
| `supersedes_variable_id` | Variable-level lineage when re-extraction replaces a prior value |

**Thesis claims** add optional `thesis_id`, `claim_text`, `expected_pattern`, and link to `fact_keys[]` per R3 — still `tracked-variable/v1` with `ontology_family: "thesis_claim"`.

### 3.3 Ontology ownership

| Family | Vocabulary owner | Example keys |
|--------|------------------|--------------|
| `clause` | Doc-Lineage `vocab/legal-clauses.json` | `legal.withdrawal.notice_days`, `legal.key_person.trigger` |
| `report_section` | Doc-Lineage `vocab/consultant-sections.json` + Inv-Man-Intake element keys | `consultant.trust_level.market_overview` |
| `thesis_claim` | Per-workspace `thesis-vocabulary.json` (owner-authored) | `thesis.gp_alignment`, `thesis.liquidity_runway` |

Workflows syncs **schema**; domain repos sync **vocabulary data** as artifacts, not as Workflows-owned judgment.

---

## 4. Lineage and supersession model

### 4.1 Two existing patterns to unify

**Pension-Data artifact supersession** (`ingest/artifacts.py`): keyed by `(plan_id, plan_period, source_url)`; new checksum supersedes active row; `supersedes_artifact_id` / `superseded_by_artifact_id` form a doubly-linked chain; `lineage_for_artifact()` walks acyclic history.

**Inv-Man-Intake document versioning** (`core_schema.md`): keyed by `(fund_id, file_name)`; ordered by `version_date`, then `received_at`, then `document_id`; no content-hash supersession in the contract today.

**JUDGMENT:** Neither pattern alone is sufficient. Content-addressed supersession (Pension-Data) is correct for **blob identity**; logical key ordering (Inv-Man-Intake) is correct for **human filename semantics**. The unified model uses both layers.

### 4.2 Unified lineage graph

```
LogicalDocument (fund_id + file_name OR plan_id + period + doc_type)
    └── DocumentVersion (document_id = sha256, version_date, received_at)
            └── ArtifactRun (artifact_id, supersedes_artifact_id)  [Pension-Data]
            └── TrackedVariable (variable_id, supersedes_variable_id)
```

**Edge types:**

| Edge | From → To | Semantics |
|------|-----------|-----------|
| `content_supersedes` | `artifact:a` → `artifact:b` | Same logical source URL/key, new bytes (Pension-Data) |
| `version_successor` | `document:v1` → `document:v2` | Inv-Man-Intake ordering on same `(fund_id, file_name)` |
| `family_amends` | `legal.lpa:v2020` → `legal.amendment:v2024` | R1 `amends` / `replaces` edges |
| `variable_supersedes` | `var:old` → `var:new` | Re-extraction or correction |

**Rules:**

1. **Acyclicity:** Validators reject cycles in `supersedes_*` chains (Pension-Data already guards in `lineage_for_artifact`).
2. **Active pointer:** Each logical document has exactly one `active_document_id` and one `active_artifact_id` per ingest key.
3. **Forward resolution:** Merged entity IDs and superseded artifact IDs resolve forward at read time; stored history is immutable.
4. **Corrections vs supersession:** Inv-Man-Intake field corrections (`provenance_history.md`) are append-only on `extracted_fields`; a correction on the same `document_id` produces a new `variable_id` with `supersedes_variable_id` pointing to the prior extraction — corrections do not rewrite blobs.

### 4.3 Lineage artifact (`lineage-edges/v1`)

Emit as NDJSON alongside Doc-Lineage runs for cross-repo consumption:

```json
{
  "schema_version": "lineage-edges/v1",
  "edge_id": "le:…",
  "edge_type": "content_supersedes",
  "from_id": "artifact:a",
  "to_id": "artifact:b",
  "effective_date": "2024-11-01",
  "evidence_excerpt": "amends and restates…"
}
```

---

## 5. Extension of `run-contract/v1` and `evidence-object/v1`

**JUDGMENT:** Do not replace these contracts. Add **satellite schemas** and optional envelope fields. This matches Workflows' stated stance: participants project existing state into conformant envelopes (`run-contract-v1.md` §Design Decision).

### 5.1 `run-contract/v1` extensions (additive)

| New optional field | Content |
|--------------------|---------|
| `identity_map_ref` | `artifact:identity-map.json` published this run |
| `document_types[]` | `doc_type_id` values processed |
| `tracked_variable_refs[]` | `variable_id` list for orchestrator threading |
| `lineage_ref` | `artifact:lineage.ndjson` |
| `mirror_ref` | `artifact:mirror-manifest.json` when run consumed a mirror |

Registry `required_sections` updated per participant — extraction tools require `evidence_refs` + `identity_refs`; pure compute tools omit them (unchanged).

### 5.2 `evidence-object/v1` extensions (additive)

Add optional properties (non-breaking in JSON Schema):

```json
{
  "mirror_locator": {
    "blob_path": "blobs/sha256/…",
    "page_anchor": "#page=42"
  },
  "source_system_locator": {
    "system": "backstop",
    "url": "https://…"
  },
  "tracked_variable_id": "var:…"
}
```

`source_id` remains the **content-addressed document ID** for determinism. Mirror and Backstop URLs are navigational duplicates, not join keys — **strongest objection** if treated as primary IDs (R4: Backstop permalinks unverified).

### 5.3 `artifact-manifest/v1` kinds

Extend `kind` enum additively: `identity_map`, `tracked_variables`, `lineage`, `vocabulary`, `mirror_catalog`. Validators accept unknown kinds in `additionalProperties` repos until Workflows schema bump.

### 5.4 What stays out of scope

- Replacing Pension-Data's internal `EvidenceReference` or Manager-Database's `chains/evidence.py` — adapters emit `evidence-object/v1` at the manifest boundary.
- Mandating a single evidence authority — any producer may emit evidence; consumers dedupe by `(fact_ref, source_id, excerpt_hash)`.

---

## 6. Adoption plan

### 6.1 First adopters (ordered)

| Phase | Repo | Role | Deliverable |
|-------|------|------|-------------|
| **P0** | Workflows | Schema owner | Satellite schemas + vocabulary seed + sync manifest entries + validator fixtures |
| **P1** | Pension-Data | Producer (partial conformant today) | Emit standalone `evidence-object/v1` files; publish `identity-map/v1` for pension/fund/manager tokens; wire `tracked-variable/v1` on consultant extractions |
| **P1** | Manager-Database | Map publisher | Export `identity-map/v1` after `resolve_aliases.py`; map `manager_id` → `manager:cik_*` in `native_keys` only |
| **P2** | Inv-Man-Intake | Producer | Populate `aliases_json`; map `doc_types` to fleet vocabulary; emit `tracked-variable/v1` from `extracted_fields` |
| **P2** | Doc-Lineage | Producer | Own clause/section vocabularies; emit lineage + variables per R1/R2 |
| **P3** | Counter_Risk | Map publisher | Export provider cross-walk from `name_registry.py` |
| **P3** | learning-management-system | Consumer | Ingest `evidence-object/v1` + `tracked-variable/v1` per backplane consumer role |

### 6.2 Conformance tests

Add under Workflows `tests/fixtures/backplane/`:

1. **`valid_identity_map.json`** — schema validation + alias uniqueness per `canonical_id`
2. **`valid_tracked_variable.json`** — embedded evidence passes `evidence-object-v1`; `provenance.document.locator.page` present for PDF sources
3. **`valid_lineage_chain.json`** — acyclic `supersedes_*` walk matches Pension-Data test vectors (`tests/ingest/test_artifacts.py`)
4. **`crosswalk_join.json`** — synthetic two-map federation resolves alias → canonical ID
5. **Deliberate-break tests** — integer `manager_id` in `identity_refs` must fail validator

Extend `scripts/validate_run_contract.py` with `--identity-map`, `--tracked-variables`, `--lineage` flags (offline, deterministic).

### 6.3 Exact files to add in Workflows (for fleet sync)

**New schemas (Workflows `docs/contracts/schemas/`):**

- `identity-map-v1.schema.json`
- `tracked-variable-v1.schema.json`
- `lineage-edges-v1.schema.json`
- `document-type-vocabulary-v1.schema.json`
- `document-mirror-v1.schema.json` (from R4; sibling to artifact-manifest)

**New specs (Workflows `docs/contracts/`):**

- `interop-architecture-v1.md` (this document, condensed normative subset)
- `document-type-vocabulary-v1.md`
- `tracked-variable-v1.md`

**Seed data (Workflows `docs/contracts/data/`):**

- `document-type-vocabulary.json` (v1 seed table from §2.2)
- `fixtures/identity-map-manager-sample.json`

**Sync manifest entries (append to `.github/sync-manifest.yml`):**

```yaml
  - source: docs/contracts/tracked-variable-v1.md
    target: docs/contracts/tracked-variable-v1.md
  - source: docs/contracts/schemas/tracked-variable-v1.schema.json
    target: docs/contracts/schemas/tracked-variable-v1.schema.json
  - source: docs/contracts/schemas/identity-map-v1.schema.json
    target: docs/contracts/schemas/identity-map-v1.schema.json
  - source: docs/contracts/schemas/lineage-edges-v1.schema.json
    target: docs/contracts/schemas/lineage-edges-v1.schema.json
  - source: docs/contracts/schemas/document-type-vocabulary-v1.schema.json
    target: docs/contracts/schemas/document-type-vocabulary-v1.schema.json
  - source: docs/contracts/data/document-type-vocabulary.json
    target: docs/contracts/data/document-type-vocabulary.json
  - source: tools/identity_normalize.py
    target: tools/identity_normalize.py
```

**Templates (consumer-repo):**

- `tests/backplane/test_interop_schemas.py` — stub that loads synced schemas and runs fixture validation
- `.github/workflows/backplane-conformance.yml` — already synced; extend inputs for new artifact kinds

**Amend existing:**

- `identity-map-conventions.md` — replace "authoritative repo" with "resolution surfaces" (§1.4)
- `config/backplane_participants.json` — add `required_artifacts` per participant

Consumer sync flow unchanged: `maint-68-sync-consumer-repos.yml` copies manifest entries; repos opt in via `backplane_participants.json`.

---

## 7. Risks and falsification

| Risk | Severity | Mitigation | Falsifier (design wrong if…) |
|------|----------|------------|------------------------------|
| Alias map staleness | High | Scheduled `identity-map/v1` publish from Manager-DB + Inv-Man-Intake; `synced_at` on maps | >25% of join attempts fail after 30 days with no map update |
| Integer `manager_id` leakage | High | Validator rejects non-canonical `identity_refs`; adapter layer only | Any conformant run passes `manager_id:42` as `identity_ref` |
| Vocabulary churn | Medium | Additive `document-type-vocabulary` versions; aliases never removed in v1 | Breaking rename forces coordinated fleet deploy |
| Triple-URL provenance drift | Medium | `tracked-variable/v1` bundles document+mirror+source; HTML tools consume one JSON | Analysts report >1 click to reach source page in user testing |
| Federation conflicts | Medium | Surface `data_quality.conflict` when maps disagree | Silent wrong joins detected in mosaic discrepancy review |
| Evidence duplication | Low | Dedupe key `(fact_ref, source_id, excerpt_hash)` | Storage/query cost exceeds SQLite comfort on single-book mosaic |
| Backstop URL instability | High (unverified) | Treat `source_system` as best-effort; mirror hash is truth | Real export shows permalinks break on metadata edit |
| Scope creep to identity service | Medium | Explicit non-goal in `interop-architecture-v1.md` | Any P0 issue proposes HTTP resolver |

**Primary falsification test:** Run the P1 integration recipe: Pension-Data extraction on a public Form 5500 PDF → emit `run-contract/v1` + `tracked-variable/v1` for one consultant field + `identity-map/v1` cross-walk entry → Inv-Man-Intake ingests and joins on `ontology_key` + `entity_ref` without manual slug editing. If this fails after map publish, the federation model is insufficient and a stronger coordination mechanism (shared library with bundled golden maps, not a service) is required.

---

## Summary

Fleet interoperability is **contract extension + federated cross-walks**, not central resolution. Workflows syncs schemas, vocabulary seeds, and normalization helpers; Pension-Data and Manager-Database publish identity maps and supersession lineage; Inv-Man-Intake and Doc-Lineage emit `tracked-variable/v1` with dual provenance; `run-contract/v1` and `evidence-object/v1` gain optional satellite references without breaking existing emitters. The design is **wrong** if conformant envelopes still cannot join managers across repos without ad hoc string matching, or if evidence cannot be traced to document page and mirror path in one structured object.

---

*Word count: ~3,450 (body). Schema sketches inline. No `artifacts/dossiers/<Repo>.md` files created.*
