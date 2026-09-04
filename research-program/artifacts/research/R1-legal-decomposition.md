# R1 — Legal Fund-Document Decomposition and Lineage

**Date:** 2026-09-04 · **Author:** Cursor (Composer) · **Status:** Research brief for Doc-Lineage activation

## Executive summary

**JUDGMENT:** Decomposing PPM/LPA/side-letter families into tracked clause variables with page-level provenance is **buildable at home on public data** using a staged pipeline: structure-aware PDF parse → clause segmentation → vocabulary-keyed extraction → clause-aligned diff → corpus rarity scoring. Commercial tools (Kira, Luminance, Ontra, Harvey-class) solve the same problem with proprietary ML + enterprise hosting; they are useful **design references only** and do not fit the owner's no-install, static-output constraint on the work PC.

**JUDGMENT:** The fleet already has the right *containers* (`Doc-Lineage` repo intent, `evidence-object/v1`, `stranske_pdf_extract` provenance model) but **no product code yet** — `clones/Doc-Lineage/README.md` explicitly waits for this brief. Entity lineage in `Pension-Data` and intake lineage in `Inv-Man-Intake` are **entity/run** lineage, not **document-family** lineage; reuse the event-graph *pattern*, not the code.

**Confidence:** High on architecture and public-data feasibility; medium on extraction accuracy for fund-specific terms (gates, key-person, MFN) without a labeled fund-LPA corpus. **Would change my mind:** A labeled evaluation set of 20+ real LP-side redlines showing >90% clause-alignment F1 with the proposed MVP.

---

## 1. Problem decomposition (four capabilities)

### 1.1 Document families and supersession

**FACTS:** Fund legal stacks form typed families: PPM (offering), LPA (governing), side letters (LP-specific overlays), subscription docs, amendments/restated agreements. Supersession is explicit in text ("amends and restates the Original Agreement dated…") and in filing metadata. EDGAR Exhibit-10 and charter exhibits routinely file amended-and-restated LPAs ([SEC EX-10.5 example](https://web.archive.org/web/20250101000000/https://www.sec.gov/Archives/edgar/data/1393818/000119312524249809/d896208dex105.htm)).

**JUDGMENT:** Family detection is **two-signal**: (a) metadata — document type label, fund name, effective date, parties; (b) textual — high paragraph-level overlap with a prior version (template lineage) or shared defined-term block. Do **not** rely on filename or Backstop folder structure alone. Model supersession as a directed acyclic graph of `document_version` nodes with typed edges: `replaces`, `amends`, `side_letter_of`, `incorporates_by_reference`. This mirrors `successor` events in `clones/Pension-Data/src/pension_data/entities/lineage.py` but applies to **documents**, not entities.

### 1.2 Clause and defined-term variables

**FACTS:** Industry vocabularies exist at three layers:
- **ILPA Model LPA** (whole-of-fund and deal-by-deal, Delaware-based, July 2020) — sections on key-person, GP removal, indemnification, waterfall, expenses ([ILPA Model LPA — WOF PDF](https://ilpa.org/wp-content/uploads/2020/07/ILPA-Model-Limited-Partnership-Agreement-WOF.pdf)).
- **ILPA DDQ 2.0** (2021) — 20 diligence topics including fund terms, valuation, reporting ([ILPA DDQ 2.0 PDF](https://ilpa.org/wp-content/uploads/2021/11/ILPA-DDQ-2.0.pdf)).
- **Research NLP taxonomies** — CUAD: 41 clause categories, span extraction task on 510 commercial contracts ([CUAD](https://www.atticusprojectai.org/cuad/)); LEDGAR: ~100k provisions from SEC Exhibit-10, 100 provision-type labels in LexGLUE ([LEDGAR paper](https://aclanthology.org/2020.lrec-1.155.pdf)).

**FACTS:** CUAD categories include Governing Law, Renewal Term, Anti-Assignment; they skew M&A/commercial, not PE fund-specific (no "gate", "key person", "MFN"). LEDGAR includes Governing Laws, Arbitration, Termination — closer to operative clauses but not fund economics.

**JUDGMENT:** Build a **fund-clause vocabulary** as a fleet data file mapping:
`vocabulary_key` → {ILPA section refs, CUAD/LEDGAR nearest labels, DDQ question IDs, value schema}. Start with ~25 keys covering the owner's list: withdrawal/redemption, gates, lock-up, key-person, MFN, governing law/venue, fees, indemnification, valuation policy, plus document metadata (parties, effective date). Extraction is **retrieve-then-quote**: locate section by heading/number → extract span → normalize to typed value → attach `evidence-object/v1`.

**FACTS:** LLM structured extraction with citation grounding is the current SOTA for long contracts; the task is defined as returning verbatim supporting spans, not legal conclusions ([TU Delft clause-extraction survey](https://repository.tudelft.nl/file/File_e0c6743a-a0db-46b6-8227-557db173ea98)). NLI-based template comparison achieves high accuracy on contract-vs-template diff ([EMNLP 2024 NLLP](https://doi.org/10.18653/v1/2024.nllp-1.11)).

### 1.3 Blacklines (version and cross-manager)

**FACTS:** Reliable long-document diff requires **clause alignment before comparison** — arbitrary chunking causes false omissions ([LawLion AI redline guide](https://thelawlion.com/blog/how-can-ai-compare-two-versions-of-a-legal-document)). Best practice: match by section number first, semantic similarity fallback ([LegaLens approach](https://github.com/Aliipou/legalens)). Academic work uses bidirectional entailment between template and contract clauses ([EMNLP 2024 NLLP](https://doi.org/10.18653/v1/2024.nllp-1.11)).

**JUDGMENT:** MVP blackline stack:
1. **Structural align** — section/clause IDs from parsed outline.
2. **Textual diff** — word-level on aligned pairs (`difflib` / diff-match-patch).
3. **Semantic classify** — label change as `boilerplate | numeric | rights_expansion | rights_contraction | new_clause | deleted_clause` using rules + optional LLM on aligned pairs only.

Cross-manager comparison reuses the same alignment against a **canonical variable key**, not raw section numbers (managers reorder sections).

### 1.4 Uniqueness (corpus-relative rarity)

**JUDGMENT:** "Unusual" = low corpus frequency of the **normalized value** or **embedding cluster** for a `vocabulary_key`, not raw text hash (legalese repeats). Pipeline: extract variables across corpus → bucket by key → compute rarity (inverse document frequency on normalized values; flag outliers >2σ from cluster centroid). Surface as an HTML column "corpus percentile" with drill-down to peer clauses. **Caveat:** Public EDGAR corpus over-represents registered-fund and listed-affiliate structures; calibrate on pension board materials for LP-relevant baselines.

---

## 2. State of the art and open building blocks

### 2.1 Datasets and benchmarks

| Resource | Size | Relevance to fund docs | URL |
|----------|------|------------------------|-----|
| CUAD | 510 contracts, 41 clause types, span labels | Clause taxonomy seed; weak on fund terms | https://www.atticusprojectai.org/cuad/ |
| LEDGAR / LexGLUE | ~100k provisions, 100 types | EDGAR contract language; provision classification | https://huggingface.co/datasets/coastalcph/lex_glue |
| ILPA Model LPA | 2 waterfall variants | Gold-standard section structure for LPA | https://ilpa.org/wp-content/uploads/2020/07/ILPA-Model-Limited-Partnership-Agreement-WOF.pdf |
| ILPA DDQ 2.0 | Question taxonomy | Maps diligence questions → clause keys | https://ilpa.org/wp-content/uploads/2021/11/ILPA-DDQ-2.0.pdf |
| EDGAR Exhibit-10 | Open-ended | Real LPAs/PPM excerpts, version chains | https://web.archive.org/web/20250101000000/https://www.sec.gov/edgar/search/ |

**JUDGMENT:** No public dataset labels fund-specific gates/MFN/key-person at span level. Home evaluation must be **bootstrapped**: ILPA model LPA as pseudo-ground-truth + manual labels on 10–15 EDGAR LPAs.

### 2.2 Open-source libraries

| Library | Role | Fit for owner constraint |
|---------|------|--------------------------|
| **Docling** | PDF/DOCX → structured Markdown/JSON with layout, tables, reading order ([GitHub](https://github.com/docling-project/docling)) | Home dev: yes. Work PC delivery: pre-run; ship static JSON/HTML only |
| **LexNLP** | Rule-based legal segmentation, amounts, dates ([GitHub](https://github.com/LexPredict/lexpredict-lexnlp)) | AGPL; good for deterministic features; heavy deps |
| **ContractEx** | CUAD classification, comparison task, pipeline composability ([PyPI](https://pypi.org/project/contractex/)) | Alpha; useful patterns; not production-proven |
| **stranske_pdf_extract** | Fleet provenance contract: `SourceLocation`, `EvidenceRef`, bbox ([contract.py](clones/Workflows/packages/stranske_pdf_extract/src/stranske_pdf_extract/contract.py)) | Scaffold per `DESIGN.md`; right target for Doc-Lineage adoption |

**JUDGMENT:** Docling + fleet `evidence-object/v1` + custom fund vocabulary beats adopting LexNLP wholesale (license, divergence from fleet contracts).

### 2.3 Commercial framing (design reference only)

**FACTS:** Kira combines lawyer-trained extraction models with optional GenAI grounded in validated extractions; emphasizes grid-based cross-document Q&A with citations ([Kira ebook](https://kirasystems.com/files/ebooks/KiraSystems-Ebook-AiDrivenContractAnalysis.pdf), [Litera Grid Chat](https://www.litera.com/blog/kira-grid-chat-cross-document-due-diligence)). Luminance and Ontra similarly pair extraction with workflow — enterprise SaaS, not portable static HTML.

**JUDGMENT:** Adopt their **information architecture** (document → clause field grid → citation-backed cell → diff view), not their runtime.

---

## 3. Constraint-model fit

**FACTS:** Owner work environment: browser + Office + Claude Code web + filesystem; **no terminal, no installs** (treat as binding). Outputs today are HTML. One-click provenance to primary document + page is mandatory.

**JUDGMENT:** Split architecture:
- **Build lane (home / CI):** Python pipeline produces `run.json`, `manifest.json`, `evidence/*.json`, `variables.ndjson`, `blackline.html`, bundled PDF page images or deep links.
- **Consume lane (work PC):** Open static HTML; links use `file://` or SharePoint-relative paths to mirrored PDFs; no server, no pip install.

**JUDGMENT:** Reject any design requiring runtime LLM on the work PC for v1. Pre-compute extractions; HTML is the API.

**FACTS:** `evidence-object/v1` requires `schema_version`, `evidence_id`, `fact_ref`, `source_id`, `method`, `excerpt`, optional `locator.page` ([schema](clones/Workflows/docs/contracts/schemas/evidence-object-v1.schema.json)).

---

## 4. Recommended schema: "clause as variable"

```json
{
  "schema_version": "clause-variable/v1",
  "variable_id": "cv:sha256…",
  "vocabulary_key": "redemption.withdrawal_rights",
  "document_version_id": "docver:…",
  "normalized_value": {
    "type": "schedule",
    "notice_days": 90,
    "frequency": "quarterly",
    "gate_applies": true
  },
  "status": "present|absent|ambiguous",
  "defined_terms": ["Withdrawal Date", "Eligible Partner"],
  "evidence": {
    "schema_version": "evidence-object/v1",
    "evidence_id": "ev:…",
    "fact_ref": "redemption.withdrawal_rights",
    "source_id": "doc:sha256…",
    "method": "llm|parser|rule",
    "excerpt": "…≤2000 chars…",
    "locator": { "page": 42, "section": "7.3", "bbox": [72, 400, 540, 520] }
  },
  "confidence": 0.87,
  "extracted_at": "2026-09-04T…Z"
}
```

**JUDGMENT:** `vocabulary_key` is the cross-manager join key. `normalized_value` is type-specific JSON Schema per key (publish in `Doc-Lineage/vocab/`). `document_version_id` links to lineage graph. Identity for `source_id`: content-hash of PDF bytes (`doc:<sha256>`) until Backstop MCP exposes stable IDs.

**Lineage graph (companion file `lineage.ndjson`):**

```json
{
  "edge_id": "le:…",
  "edge_type": "replaces|amends|side_letter_of",
  "from_version_id": "docver:…",
  "to_version_id": "docver:…",
  "effective_date": "2024-11-01",
  "evidence_excerpt": "amends and restates…"
}
```

---

## 5. Minimum viable Doc-Lineage pipeline

Per `clones/Doc-Lineage/README.md`, the repo is scaffold-only. **JUDGMENT:** MVP in four phases:

| Phase | Deliverable | Depends on |
|-------|-------------|------------|
| **M0** | `vocab/fund-clauses.v1.yaml` + JSON Schema for top 25 keys | None |
| **M1** | `ingest` — PDF → structured text + page map (Docling adapter → `stranske_pdf_extract` contract) | M0 |
| **M2** | `extract` — vocabulary-keyed variables + `evidence-object/v1` per hit | M1 |
| **M3** | `diff` — pairwise blackline HTML between versions; `lineage.ndjson` from supersession heuristics | M2 |
| **M4** | `corpus` — rarity scores across ingested EDGAR set; uniqueness column in comparison view | M2 + public corpus |

**Emit** `run-contract/v1` envelope per pipeline run for fleet interoperability ([run-contract-v1.md](clones/Workflows/docs/contracts/run-contract-v1.md)).

**Reuse:** `Inv-Man-Intake` `build_lineage_packet` pattern for run assembly ([lineage.py](clones/Inv-Man-Intake/src/inv_man_intake/audit/lineage.py)); Pension-Data `successor` edge validation for DAG checks ([lineage.py](clones/Pension-Data/src/pension_data/entities/lineage.py)).

**Out of MVP:** Side-letter ↔ LPA conflict resolution, MFN propagation, automated legal advice, real-time Backstop sync.

---

## 6. Public test corpora

| Corpus | Content | Use | Access |
|--------|---------|-----|--------|
| **EDGAR Exhibit-10 LPAs** | Amended/restated partnership agreements filed by fund affiliates | Lineage chains, clause extraction, cross-manager compare | [SEC EDGAR search](https://web.archive.org/web/20250101000000/https://www.sec.gov/edgar/search/) — filter exhibit type, query "limited partnership agreement" |
| **EDGAR Form S-1 / 10-K PPM excerpts** | Offering materials for listed fund vehicles | PPM-style disclosure variables | Same |
| **ILPA Model LPA (WOF + D×D)** | Canonical section text | Vocabulary validation, pseudo-gold spans | [ILPA PDF](https://ilpa.org/wp-content/uploads/2020/07/ILPA-Model-Limited-Partnership-Agreement-WOF.pdf) |
| **Public pension board packets** | Consultant recommendations, occasionally redacted legal summaries | Uniqueness baseline closer to LP practice | Pension-Data already ingests public pension reports ([dossier](artifacts/dossiers/Pension-Data.md)) — legal exhibits sparse but useful for integration tests |
| **CUAD subset** | Commercial contracts | Classifier benchmarking only | [HuggingFace](https://huggingface.co/datasets/theatticusproject/cuad) |

**JUDGMENT:** Primary gold-path test set = **10 EDGAR LPA pairs** with visible "amends and restates" language + **ILPA model** as control. Pension board materials are secondary until R6 corpora brief lands.

---

## 7. Fleet integration notes

- **Doc-Lineage** is the intended owner repo; zero product code today.
- **Identity/evidence authority is open** per owner directive — default to content-addressed `doc:<sha256>` with optional `manager:` / `fund:` aliases when a fleet resolver exists.
- **Do not** fold this into `Inv-Man-Intake` (manager packets) or `Pension-Data` (pension reports) — those are different document typologies; share contracts only.
- Owner's existing work-side legal lineage tool (HTML, not in repo) validates the UX; Doc-Lineage should **match or exceed** its one-click page links, not reinvent weaker provenance.

---

## 8. Ranked candidates

| Rank | What | Why it matters | Effort | Prerequisite | Disposition |
|------|------|----------------|--------|--------------|-------------|
| 1 | **Fund-clause vocabulary v1** (`vocab/fund-clauses.v1.yaml`) | Stable join key across managers, DDQ, and blacklines | S | None | extend:Doc-Lineage |
| 2 | **Doc-Lineage M1–M3 pipeline** (ingest → extract → diff → static HTML) | Delivers the owner's legal lineage capability on public data | L | #1 | extend:Doc-Lineage |
| 3 | **Wire provenance to `evidence-object/v1` + `stranske_pdf_extract`** | One-click page/bbox citations fleet-wide | M | Workflows pdf-extract scaffold | extend:Doc-Lineage, extend:Workflows |
| 4 | **EDGAR LPA harvest script + 10-pair evaluation set** | Reproducible test data without proprietary docs | M | SEC EDGAR access | extend:Doc-Lineage |
| 5 | **Clause-alignment blackline engine** (section-ID + semantic fallback) | Year-over-year and cross-manager compare | M | M1 structured parse | extend:Doc-Lineage |
| 6 | **Corpus rarity / uniqueness scorer** | Surfaces non-market terms | M | M2 + EDGAR corpus | extend:Doc-Lineage |
| 7 | **ContractEx or LexNLP as extraction backend** | Off-the-shelf clause tasks | S | License review | reject — AGPL/heavy deps; fleet vocabulary approach is cleaner |
| 8 | **Kira / Luminance / Ontra adoption** | Commercial accuracy | L | Enterprise budget, data egress | reject — violates no-install, no-egress constraint |

---

## 9. Open questions for the owner

1. **Document identity on the work PC:** Should HTML link to Backstop URLs (when MCP arrives), SharePoint paths, or local mirror filenames? **Default assumed:** relative path in a synced folder; `source_id` = content hash.
2. **Scope of v1 vocabulary:** All ILPA LPA sections (~80+) or the 25-key MVP list? **Default:** 25 keys aligned to your existing work-side tool variables.
3. **Consultant reports in Doc-Lineage:** Shared diff engine with R2, or separate repos? **Default:** shared `Doc-Lineage` diff library, separate vocab files (`fund-clauses` vs `consultant-sections`).
4. **Identity resolver:** When manager/fund IDs are needed on variables, which repo owns the mapping? **Default:** deferred; optional `entity_refs[]` on variables, populated manually until fleet decides.

---

## STOP SIGNAL

NEW_CANDIDATES=8

---

## Citation corrections 2026-09-04

| Original (unreachable to automated check) | Action |
|-----|--------|
| ILPA Model LPA hub (`ilpa.org/.../model-limited-partnership-agreement/`) | **(a)** Replaced with `https://ilpa.org/wp-content/uploads/2020/07/ILPA-Model-Limited-Partnership-Agreement-WOF.pdf` (same source; hub page returns 403 to automated checks). |
| ILPA DDQ hub (`ilpa.org/.../due-diligence-questionnaire/`) | **(a)** Replaced with `https://ilpa.org/wp-content/uploads/2021/11/ILPA-DDQ-2.0.pdf` (same source; hub page returns 403 to automated checks). |
| SEC EX-10.5 filing (`sec.gov/Archives/edgar/data/1393818/.../d896208dex105.htm`) | **(a)** Replaced with Internet Archive snapshot of the same EX-10.5 filing (SEC returns 403 to automated checks). |
| SEC EDGAR search (`sec.gov/edgar/search/`) | **(a)** Replaced with Internet Archive snapshot of the same EDGAR full-text search UI (SEC returns 403 to automated checks). |
