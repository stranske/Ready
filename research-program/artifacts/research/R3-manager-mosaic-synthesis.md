# R3 — Manager mosaic synthesis, discrepancy detection, and thesis monitoring

**Date:** 2026-09-04  
**Question:** How should a local-first system represent facts from many communication sources about one investment so that (1) every fact links to primary document and page, (2) contradictions are detected, (3) an explicit investment thesis can be monitored as new material arrives, and (4) everything runs without a server?

---

## 1. Problem framing

An allocator diligence file for a single manager is not one database row — it is a **mosaic**: call notes, newsletters, consultant reports, legal terms, regulatory filings, marketing decks, internal DD memos, and structured data packets, arriving on different cadences and often disagreeing on names, numbers, and narrative. The owner already runs three work-side HTML tools (consultant blackline, legal lineage, and a near-complete communications mosaic with discrepancy and thesis monitoring). The fleet repos are the **portable, synthetic-data development path** for the same capabilities.

The non-negotiable product standard: **one-click navigation from any derived statement to the primary document and page**. Everything else — graph ontologies, vector search, LLM extraction — exists to serve that link and to surface when sources disagree.

---

## 2. Requirements mapped to design primitives

| Requirement | Minimum viable representation | Failure mode to avoid |
|---|---|---|
| Primary-source link | `source_id` + structured `locator.page` + bounded `excerpt` | Positional anchors like `text:3` with no quoted text (called out in `clones/Workflows/docs/contracts/schemas/evidence-object-v1.schema.json`) |
| Contradiction detection | Normalized **fact key** + comparable value + multiple `evidence_id`s | Treating every extraction as a new fact with no join key |
| Thesis monitoring | **Thesis claim** objects with expected evidence patterns and verdict enum | Price-triggered or filing-exists alerts without criterion-level verdicts |
| Local-first, no server | Single-file SQLite (+ content-addressed blobs) and static HTML review | Requiring PostgreSQL/MinIO for the analyst path (Manager-Database's production shape) |

---

## 3. External survey (FACTS)

### 3.1 Evidence and claim graph models

- **W3C PROV** defines entities, activities, and agents for provenance interchange; `prov:wasDerivedFrom` links derived entities to sources ([PROV Model Primer](https://www.w3.org/TR/prov-primer/), [PROV-O](https://www.w3.org/TR/2013/PR-prov-o-20130312/)). Useful as vocabulary, not as a runtime requirement.
- **Nanopublications** package an assertion graph, provenance graph, and publication-info graph as citable RDF units ([Nanopublication Guidelines](https://nanopub.net/guidelines/working_draft/)). Strong for scholarly publishing; heavy for a pension work PC.
- **Assertion–evidence separation** appears in newer cross-domain vocabularies (e.g. Cascade Evidence Vocabulary draft: Assertion ≠ EvidenceLink ≠ GroundingActivity, reusing PROV primitives: [Cascade Evidence Vocabulary v1.0-draft](https://www.cascadeprotocol.org/docs/evidence/v1-draft/)).
- **LLM citation verification** research consistently separates claim extraction, evidence retrieval, and entailment checking; systems that extract **verbatim spans** from source PDFs reduce hallucinated citations (RefLens, AAAI 2024: [paper](https://ojs.aaai.org/index.php/AAAI/article/view/42361/46322); ExecutableClaims: [GitHub](https://github.com/aayambansal/ExecutableClaims)).

### 3.2 Local-first knowledge stores

- **SQLite + FTS5 + sqlite-vec** supports hybrid lexical/semantic search in one file, fused with Reciprocal Rank Fusion ([Alex Garcia hybrid search post](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html); [sqlite-vec project](https://github.com/asg017/sqlite-vec)).
- **DuckDB** excels at analytical queries over parquet/CSV holdings and performance series; it is a complement, not a replacement for per-document provenance rows.
- **Kùzu** and similar embedded graph databases help multi-hop queries ("which claims cite the same clause across PPM versions?") but add a new query language and migration path with no current fleet adopter.
- **JSON-LD files** work as interchange artifacts (aligned with backplane manifests) but are weak as the sole query store at mosaic scale.

### 3.3 Thesis monitoring in investment tooling (public descriptions)

- Purpose-built **thesis monitors** (e.g. EvidInvest Thesis Monitor, Helm Terminal) take user-written criteria per holding and return supported / at-risk / contradicted verdicts with **filed-passage citations** ([EvidInvest](https://evidinvest.com/thesis-monitor); [Helm comparison](https://helmterminal.dev/best-thesis-trackers)).
- **Bloomberg PORT** is portfolio/risk/performance analytics, not a communications mosaic or thesis tracker ([Bloomberg PORT](https://professional.bloomberg.com/products/bloomberg-terminal/portfolio-analytics/)).
- **Koyfin** provides screening, charts, and watchlist alerts on price/valuation/news — not manager-communication discrepancy workflows ([Koyfin research teams](https://www.koyfin.com/for-financial-advisors/investment-research-teams-cio/)).

---

## 4. Fleet mapping (FACTS — repo paths)

### 4.1 Workflows — contracts (owner, not runtime)

`clones/Workflows/docs/contracts/` already defines the interchange layer:

- **`evidence-object/v1`** — requires `evidence_id`, `fact_ref`, `source_id`, `method`, `excerpt`, optional `locator.page` and `entity_ref` (`schemas/evidence-object-v1.schema.json`).
- **`identity-map-conventions.md`** — canonical ID shape `entity_type:normalized_identity` and alias/merge discipline.
- **`research-backplane-contract.md`** — opt-in producer/consumer roles; no participant is conformant yet (`status: planned`).

**Tension (FACT):** `identity-map-conventions.md` still declares Manager-Database authoritative for `manager` and Pension-Data for `fund`/`pension` (lines 94–106). The research program has **removed** that as an absolute mandate; the doc and the program charter now disagree until amended.

### 4.2 Inv-Man-Intake — extraction and validation queue

- Persists fields with `document_id`, `source_page`, `source_snippet` (`src/inv_man_intake/data/provenance.py`).
- Confidence gating and duplicate-field resolution (`src/inv_man_intake/extraction/confidence.py`).
- Performance **conflict resolver** with audit entries and escalation thresholds (`src/inv_man_intake/performance/conflict_resolver.py`; tested in `tests/performance/test_conflict_resolver.py`).
- Emits `run-contract/v1` and `artifact-manifest/v1` but **not** conformant `evidence-object/v1` files — `evidence_refs` are page-pointer strings (`src/inv_man_intake/run.py`; dossier `artifacts/dossiers/Inv-Man-Intake.md` §5).
- `aliases_json` hard-coded `None` in integration (`dossier` §5) — weak identity join today.

### 4.3 Manager-Database — public filings, alerts, holdings diffs

- Integer `manager_id` with `cik`, `lei`, `aliases`, `registry_ids` (`schema.sql`; dossier `artifacts/dossiers/Manager-Database.md` §5).
- EDGAR alias resolution script (`scripts/resolve_aliases.py`) appends official names to alias arrays.
- Internal `Evidence` model has `source_id`, `locator`, `excerpt`, `method` but lacks fleet `schema_version`, `evidence_id`, `fact_ref` (`chains/evidence.py`).
- Production stack is Docker + PostgreSQL + MinIO — **not** the owner constraint model for daily analyst use; WASM demo is fixture-scale (`web/wasm_app.py`).

### 4.4 Pension-Data — entity linkage and review queue

- `build_canonical_stable_id` and explicit `merge_canonical_entities` (`src/pension_data/entities/service.py:54–272`).
- Richest fleet evidence helper: `build_evidence_reference` with page, excerpt, method inference (`src/pension_data/extract/common/evidence.py`).
- Review queue routes low-confidence rows (`src/pension_data/review_queue/extraction.py`).
- Emits `run-contract/v1` from one-PDF pilot (`src/pension_data/ops/backplane_emitter.py`) but not separate `evidence-object/v1` artifact files yet.

### 4.5 Doc-Lineage — recurring legal/consultant diffing (scaffold)

- Repo intent: blackline, lineage, tracked variables for PPM/LPA/consultant reports (`clones/Doc-Lineage/README.md`).
- Created 2026-09-04; scope arrives from R1/R2 — **no product code yet**, only Workflows consumer scaffold.

### 4.6 Owner work-side tools (not in clones)

Consultant Tracker, legal lineage, and the near-complete communications mosaic already output HTML with discrepancy and thesis views. Treat them as **reference implementations** whose contracts should be captured, not re-derived from scratch in a fourth parallel HTML tool.

---

## 5. Recommended fact / evidence / thesis schema (JUDGMENT)

**Do not adopt PROV or nanopublications as the on-disk runtime.** Use fleet `evidence-object/v1` plus three small extensions owned by Workflows as JSON Schemas (additive v1 fields, not a new ontology).

### 5.1 Layer model

```
SourceDocument ──< EvidenceObject (evidence-object/v1) ──> Fact
       │                                                    │
       └──────────────────────────────────────────── Discrepancy
ThesisClaim ──< ThesisCheck (verdict + evidence_ids)
```

**SourceDocument** (per investment workspace, SQLite table or JSONL artifact)

| Field | Purpose |
|---|---|
| `source_id` | Content-addressed: `document:<sha256-prefix>` |
| `document_type` | Closed enum: `call_note`, `newsletter`, `consultant_report`, `ppm`, `lpa`, `filing_13f`, `dd_memo`, … |
| `title`, `as_of_date`, `received_at` | Human ordering |
| `storage_uri` | `file://`, SharePoint mirror path, or future Backstop deep link |
| `entity_refs[]` | Canonical IDs the document is *about* |
| `supersedes_source_id` | Lineage from Doc-Lineage |

**Fact** (normalized assertion — the join key for contradictions)

| Field | Purpose |
|---|---|
| `fact_id` | Deterministic hash of `(fact_key, entity_ref, period, normalized_value)` |
| `fact_key` | Registry string, e.g. `fund.net_irr`, `legal.withdrawal_notice_days`, `strategy.capacity_usd` |
| `entity_ref` | `manager:cik_…`, `fund:…` per conventions |
| `value` | Typed JSON (number, string, boolean, range) |
| `period` | Optional `2025-Q4` or `as_of:2025-12-31` |
| `status` | `asserted` \| `superseded` \| `retracted` |
| `primary_evidence_id` | Best evidence link after confidence policy |

**EvidenceObject** — emit **as written** in `evidence-object-v1.schema.json`. Non-negotiable: `excerpt` must be present (string or explicit `null`); `method` must be set; `locator.page` required when the source is paginated.

**Discrepancy** (first-class, reviewable)

| Field | Purpose |
|---|---|
| `discrepancy_id` | Stable hash of `fact_key + entity_ref + period` |
| `fact_ids[]` | Competing facts |
| `discrepancy_kind` | `numeric_delta` \| `sign_conflict` \| `narrative_conflict` \| `missing_in_source` |
| `severity` | Rule-derived; numeric >5% on fee/liquidity terms = high |
| `status` | `open` \| `accepted_primary` \| `immaterial` \| `resolved` |
| `resolution_note` | Analyst text when closed |

Detection rules (JUDGMENT): run deterministic comparators first (normalized numbers, dates, enums); use LLM only for `narrative_conflict` after retrieval of both excerpts. This mirrors Inv-Man-Intake's performance conflict threshold pattern and Pension-Data's confidence routing — do not LLM-first.

**ThesisClaim** (monitoring unit)

| Field | Purpose |
|---|---|
| `thesis_id`, `claim_id` | Group and line item |
| `claim_text` | Owner-written criterion |
| `entity_ref` | Which manager/fund |
| `fact_keys[]` | Which normalized facts can satisfy it |
| `expected_pattern` | Optional: `min`, `max`, `trend_up`, `absent` |
| `evidence_policy` | `require_primary_source`, `allow_marketing_only_with_flag` |

**ThesisCheck** (emitted when new `SourceDocument` or `Fact` arrives)

| Field | Purpose |
|---|---|
| `verdict` | `supported` \| `at_risk` \| `contradicted` \| `insufficient_evidence` |
| `evidence_ids[]` | Must be non-empty for non-`insufficient_evidence` |
| `checked_at`, `trigger_source_id` | Audit |

Align verdict enum with public thesis-monitor products ([EvidInvest](https://evidinvest.com/thesis-monitor)) so owner mental models transfer.

### 5.2 Storage and search (JUDGMENT)

**Primary store:** SQLite per investment (or per manager book) with:

- Relational tables for SourceDocument, Fact, EvidenceObject, Discrepancy, ThesisClaim, ThesisCheck
- FTS5 on `excerpt` + document full text
- sqlite-vec on chunk embeddings for "find similar disclosures" (optional lane; lexical+fact_key covers most discrepancy work)

**Reject for v1:** Kùzu graph DB, centralized JSON-LD triple store, DuckDB as primary provenance store.

**DuckDB role:** analytical sidecar for holdings/performance series imported from Manager-Database or spreadsheets — query, not provenance authority.

**HTML review surface:** static bundle (Pension-Data `apps/web/` pattern) reading `mosaic.bundle.json` + hashed PDFs beside it; every rendered fact carries `data-evidence-id` → opens `storage_uri#page=N`.

### 5.3 LLM extraction with citation verification (JUDGMENT)

Pipeline per document:

1. **Extract** candidate facts with provider (`method: llm` | `parser` | `manual`).
2. **Verify** each candidate: retrieve page text by `locator.page`; check excerpt substring match (Pension-Data + `stranske-pdf-extract` path); fail closed to review queue if no match.
3. **Emit** only verified rows as `evidence-object/v1`.

Do not auto-promote LLM extractions at Inv-Man-Intake's `field_auto_accept_min` without substring verification — the fleet's alpha parsers are fixture-grade (`artifacts/dossiers/Inv-Man-Intake.md` §7).

---

## 6. Identity without a single mandated authority (JUDGMENT)

**Strongest objection:** Declaring any one repo "the identity source of truth" will be wrong for at least one entity class (internal fund names, side-letter vehicles, pre-CIK managers). The owner's removal of the Manager-Database / Inv-Man-Intake mandate is correct.

**Recommended federated approach:**

1. **Wire format:** Keep `identity-map-conventions.md` string shape (`manager:cik_0001067983` preferred; name-anchored fallback allowed with `confidence < 1.0` on the evidence link — already specified lines 108–112).

2. **Authority is per entity-type and per emitting tool, not per repo globally:**
   - Registry IDs (CIK, LEI, EIN) → whoever ingested the registry issues the ID (Manager-Database for EDGAR managers; Pension-Data for plan EINs).
   - Internal fund vehicles → Inv-Man-Intake or the mosaic index after human confirmation.
   - Legal defined terms → Doc-Lineage variable IDs once R1 lands.

3. **Merge records are the join mechanism, not a central resolver service.** Export merge events:
   - Pension-Data: `merge_canonical_entities` (`entities/service.py:199–272`)
   - Manager-Database: alias append via `resolve_aliases.py`
   - Mosaic index: imports both as `identity_alias` rows `{alias_id, canonical_id, asserted_by, evidence_id}`

4. **Mosaic identity index** (small SQLite table, could live in a new repo): resolves `identity_refs` collected from `run-contract/v1` envelopes across repos; flags unresolved joins when two name-anchored IDs appear for the same document set. Workflows does **not** host resolution code (`research-backplane-contract.md` lines 144–149) — only validates format.

5. **Documents are not entities** in the identity map. Use `source_id` / `document:<hash>` for provenance; do not overload `fund:` IDs for PDFs (Pension-Data already drifts with `plan:` vs `pension:` — dossier §9).

**Confidence:** High that federated merge + convention strings beats a new global entity service for this owner. **Would change mind if** Backstop MCP exposes a stable, allocator-wide manager GUID that every work document already carries — then Backstop becomes the external authority and fleet repos become caches.

---

## 7. Critical evaluation — what not to do (JUDGMENT)

| Tempting choice | Verdict | Why |
|---|---|---|
| Rebuild the work-side mosaic in a new fleet repo from zero | **Reject** | Near-complete work tool exists; fleet effort should **spec and port contracts**, not duplicate HTML UX |
| Make Manager-Database the mosaic hub | **Reject for owner path** | Requires server infra; integer IDs diverge from conventions |
| Full PROV/RDF stack | **Reject** | No browser-local query story; owner is non-developer |
| Wait for backplane conformance before mosaic | **Reject** | Pension-Data and Inv-Man-Intake already emit partial artifacts; mosaic can ingest manifests now |
| LLM-only discrepancy detection | **Reject** | False positives on immaterial wording; deterministic fact_key first |

---

## 8. Ranked candidates

| Rank | Candidate | Why it matters | Effort | Prerequisite | Disposition |
|---|---|---|---|---|---|
| 1 | **`mosaic-core` contract pack** — JSON Schemas for Fact, Discrepancy, ThesisClaim, ThesisCheck atop `evidence-object/v1` | Gives the work-side mosaic and fleet repos the same wire format; enables incremental port | S | None | **extend:Workflows** |
| 2 | **`Manager-Mosaic` repo** — SQLite index + static HTML reader per investment; ingests manifests from siblings | Only home for cross-source join the fleet lacks today | M | #1 schemas; sample bundle | **new-repo** |
| 3 | **Evidence-object emitter in Inv-Man-Intake** | Closes the fleet's largest provenance gap for DD packets | M | #1 `fact_key` registry stub | **extend:Inv-Man-Intake** |
| 4 | **Evidence + canonical ID projection in Pension-Data** | Best existing evidence builder; entity merge export | M | Identity export format from #1 | **extend:Pension-Data** |
| 5 | **Canonical `manager:` projection + DD document ingest in Manager-Database** | Links public filings to same manager IDs as mosaic | L | Backplane emitter (#1) | **extend:Manager-Database** |
| 6 | **Doc-Lineage variable IDs → `fact_key` map** | Legal/consultant recurring variables feed discrepancy engine | M | R1/R2 briefs land | **extend:Doc-Lineage** |
| 7 | **Work-side mosaic contract capture** | Document HTML tool's thesis/discrepancy JSON for porting | S | Owner access to work tool | **new-repo** (docs-only charter) or owner export |
| 8 | **sqlite-vec + FTS5 hybrid search module** | "Find all mentions of capacity" across mosaic | S | #2 repo | **adopt-ready-made:sqlite-vec** |
| 9 | **Kùzu embedded graph** | Multi-hop lineage queries | M | Proven shortcoming in SQLite joins | **reject** (v1) |
| 10 | **Nanopublication/RDF primary store** | Academic provenance | L | RDF toolchain on work PC | **reject** |
| 11 | **Adopt EvidInvest/Helm-class SaaS** | Fast thesis monitoring | S | Data egress to vendor | **reject** (proprietary data constraint) |

---

## 9. Open questions for the owner

1. **Work-side mosaic port vs greenfield?**  
   *Default assumed:* Capture the near-complete work tool's data model as the mosaic contract (#7) and implement fleet `Manager-Mosaic` as a conformant reimplementation — not a second divergent design.

2. **Per-investment vs per-manager-book SQLite file?**  
   *Default assumed:* One `.sqlite` + `artifacts/` folder per **investment commitment** (fund position), because thesis and discrepancies are commitment-specific.

3. **Backstop link format for `storage_uri`?**  
   *Default assumed:* `file://` to SharePoint/local mirror until Backstop MCP exists; schema field is URI-agnostic.

4. **Who may assert `accepted_primary` on a Discrepancy?**  
   *Default assumed:* Human analyst only; no auto-resolution except exact duplicate excerpts.

5. **Amend `identity-map-conventions.md` authority table?**  
   *Default assumed:* Rewrite as federated per-entity-type emitters + merge exports, removing "Manager-Database is authoritative on day one" as absolute policy.

---

## 10. Suggested implementation sequence (JUDGMENT)

1. Workflows: publish `mosaic-fact-v1`, `discrepancy-v1`, `thesis-claim-v1` schemas + `fact_key` starter registry (20–30 keys covering fees, liquidity, team, performance, capacity).
2. Manager-Mosaic: SQLite DDL + importer for Pension-Data `run.json` / Inv-Man-Intake manifests + static HTML with one-click page links.
3. Inv-Man-Intake + Pension-Data: emit real `evidence-object/v1` sidecars.
4. Doc-Lineage: map clause variables to `fact_key` when R1 ships.
5. Manager-Database: canonical ID adapter + optional document export lane (lower priority for owner daily path).

---

**STOP SIGNAL:** NEW_CANDIDATES=11
