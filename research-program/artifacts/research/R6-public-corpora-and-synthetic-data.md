# R6 — Public and Synthetic Corpora for Home Development

**Date:** 2026-09-04 · **Author:** Cursor (Composer) · **Status:** Research brief for fleet corpus strategy

## Executive summary

**JUDGMENT:** Home development can stand in for the owner's Backstop document mix using a **small, curated public corpus** (~2–5 GB retained) plus a **synthetic mutation layer** for diff/lineage ground truth. No single public dataset replicates allocator-side DD packets; the best proxy stack is: (1) CalPERS/SWIB investment-committee PDFs for consultant reports and board materials, (2) SEC IAPD Form ADV bulk + EDGAR EX-10 LPAs for regulatory/legal, (3) ILPA DDQ 2.0 as the DDQ skeleton, (4) Oaktree Howard Marks memos for manager letters, (5) N-CSR/N-PORT for audited fund financials. **Do not duplicate** Pension-Data's PPD/Form 5500/13F lane or Manager-Database's 13F/13D holdings lane — extend those repos only where document-type coverage is missing.

**JUDGMENT (strongest objection):** Public pension IC packets over-index on **large-plan consultant reviews** (Wilshire, Callan, Meketa) and under-represent **mid-market PE/VC DDQs, side letters, and manager-specific marketing**. Synthetic data must carry evaluation ground truth; public corpora alone cannot validate extraction accuracy on gates, MFN, or capacity claims without manual labels.

**Confidence:** High on source availability and licensing for SEC/ILPA/Oaktree materials; medium on pension-site harvest stability (JS-heavy portals). **Would change my mind:** Owner confirms their plan publishes IC packets with the same attachment structure as CalPERS — then narrow the harvest list to that plan only.

---

## 1. Fleet baseline — what already downloads (avoid duplication)

| Repo | Existing sources / adapters | Gap vs owner's documents |
|------|----------------------------|--------------------------|
| **Pension-Data** | PPD API client (`clones/Pension-Data/src/pension_data/sources/ppd/client.py`); EDGAR 13F-HR client (`.../sources/edgar/client.py`); Form 5500 Schedule SB/MB fixture adapter (`.../sources/form5500.py`); pension plan source map with CalPERS/NYSLRS/TX ERS seeds (`config/sources/source_map_v1.csv`); `scripts/source_collection/build_pension_sources.py` for plan annual-report discovery | No IAPD ADV, no EX-10 LPA harvest, no IC agenda/consultant PDF crawl, no DDQ templates, no manager letters |
| **Manager-Database** | EDGAR 13F/13D/G via `adapters/edgar.py`; Companies House (`adapters/uk.py`); news/RSS; OpenFIGI; price scrapers; synthetic fixtures in `data/raw/parsed.json` | No Form ADV, no fund legal docs, no pension board materials; dossier flags missing HTML filing regression corpus (issue #1151) |
| **Inv-Man-Intake** | Fixture PDF/PPTX extraction (`src/inv_man_intake/extraction/providers/`); Standard Element Library stub (`docs/contracts/standard_element_library.md`) | No real manager DDQ corpus; `non_authoritative: true` stub only |
| **Doc-Lineage** | Intent only (`clones/Doc-Lineage/README.md`); replay/benchmark tooling copied from Workflows scaffold | Zero document fixtures |

**FACTS:** Pension-Data's replay harness expects golden JSON/JSONL corpora with `document_id`, `content`, and evaluation metadata (`clones/Pension-Data/tools/replay/harness.py`). Manager-Database stores raw filings in MinIO in production but tests use mocks (`clones/Manager-Database/tests/data/`).

---

## 2. Public corpora by document category

### 2.1 Manager regulatory filings — Form ADV (IAPD)

**FACTS:** SEC publishes Form ADV Part 1 structured data (CSV inside ZIP archives), Part 2 brochure PDFs, and Part 3 CRS PDFs on the FOIA Form ADV data page ([SEC Form ADV Data](https://www.sec.gov/foia-services/frequently-requested-documents/form-adv-data)). Current filings are also viewable per firm on IAPD ([adviserinfo.sec.gov](https://adviserinfo.sec.gov/)). Monthly compilation reports describe column-to-ADV-item mappings ([SEC IA Information Reports](https://www.sec.gov/data-research/sec-markets-data/information-about-registered-investment-advisers-exempt-reporting-advisers)). SEC EDGAR access requires a descriptive `User-Agent` ([SEC EDGAR FAQ for developers](https://www.sec.gov/os/webmaster-faq#developers)).

**FACTS:** FINRA's IARD Query API terms restrict Firm Registration Data to FINRA members or IARD-entitled firms ([FINRA API Terms, Firm Registration Data](https://developer.finra.org/sites/default/files/2024-07/Developer%20API%20-%20Specific%20Terms%20-%20Firm%20Registration%20Data%20%2807-17-2024%29%20%281%29.pdf)) — not a home-dev path.

**JUDGMENT:** Use **SEC bulk ZIPs** (Part 1 + brochure PDF dumps), not FINRA API or paid sec-api.io, for home corpus. Retain ~50 adviser CRDs spanning hedge, PE, and traditional (e.g., Bridgewater CRD 105631, Oaktree CRD 104028) plus 10 state-registered midsize advisers. Ground truth: Part 1 field values from CSV keyed by `crd_number`; Part 2/CRS extraction targets are **manual span labels** on 5 brochures (AUM, fees, conflicts, custody).

### 2.2 Fund legal documents — LPAs/PPM via EDGAR exhibits

**FACTS:** Material contracts file as **Exhibit 10** attachments on 8-K, 10-K, S-1, etc. ([SEC EDGAR search](https://www.sec.gov/search-filings)). Real amended-and-restated LPAs appear as EX-10 HTML/PDF (e.g., [Starwood REIT OP LPA EX-10.2](https://www.sec.gov/Archives/edgar/data/1711929/000119312526346339/ck0001711929-ex10_2.htm), [JLLIPT Sixth A&R LPA EX-10.1](https://www.sec.gov/Archives/edgar/data/1314152/000131415226000084/exhibit101-sixtharlpaofjll.htm)). EDGAR full-text search supports `"limited partnership agreement"` + `form-type:EX-10` queries.

**JUDGMENT:** Harvest **15–25 LPAs** with explicit version chains ("amends and restates… dated…") via EDGAR full-text search + `edgartools` ([edgartools](https://github.com/mrabino1/edgartools)). Filter to private-fund-affiliate operating partnerships and BDC interval funds; exclude employment agreements. Ground truth: ILPA Model LPA section headings as pseudo-labels (R1 vocabulary) + 10 manually tagged clause spans per doc. Size: ~50–150 MB HTML/PDF.

### 2.3 Consultant reports and pension board materials

**FACTS — plans with full public IC packets (PDF, multi-attachment):**

| Plan | Public IC materials | Format | URL |
|------|---------------------|--------|-----|
| CalPERS | Investment Committee agendas, consultant trust-level reviews, attachments, transcripts | PDF per item + attachments | [CalPERS Board Meetings](https://www.calpers.ca.gov/about/board/board-meetings) |
| SWIB (Wisconsin) | Board + Investment Committee books (Callan, consultant reports embedded) | Large consolidated PDFs | [SWIB Meetings](https://www.swib.state.wi.us/meetings/) |
| NYC systems | Investment meeting webcasts; agendas vary by system | Webcast + some PDF agendas | [NYC Comptroller Investment Meetings](https://comptroller.nyc.gov/services/financial-matters/pension/investment-meetings/) |
| CalPERS archive (unofficial) | 2013–2026 IC action items with linked materials | Curated HTML index | [calpers-votes.com](https://calpers-votes.com/) |

**FACTS:** Pension-Data already seeds CalPERS in `config/sources/source_map_v1.csv` (`ca-calpers`, `calpers.ca.gov`, `investment_report` hints) but does not crawl IC agenda items.

**JUDGMENT:** **Primary golden pair:** CalPERS Trust Level Review consultant report year-over-year (e.g., March 2025 vs March 2026 agenda items on [invest-202603-0](https://www.calpers.ca.gov/about/board/board-meetings/invest-202603-0)). **Secondary:** SWIB quarterly Callan books for layout-drift stress tests. Retain 8 plans × 3 years × 2 meetings ≈ 48 PDFs (~500 MB–2 GB). Ground truth: manually label 12 recurring section boundaries per consultant (performance, policy, recommendation) on the CalPERS pair; use transcripts where published for quote verification.

### 2.4 Manager letters and marketing

**FACTS:** Oaktree publishes Howard Marks' complete public memo anthology as a single PDF ([Oaktree Complete Collection](https://www.oaktreecapital.com/docs/default-source/memos/the-complete-collection.pdf?sfvrsn=)); individual memos are also on [oaktreecapital.com/insights/memos](https://www.oaktreecapital.com/insights/memos). Community mirrors exist ([investing_memos GitHub](https://github.com/l33tquant/investing_memos)).

**JUDGMENT:** Legally reusable for **research and fixture development** when cited and not republished commercially; treat Oaktree PDF as the authoritative source, not GitHub mirrors. Use 30+ year-over-year memos for blackline and thesis-monitoring tests. Ground truth: memo date + title metadata; synthetic numeric mutations for contradiction-detection tests. Bridgewater publishes research at [bridgewater.com/research](https://www.bridgewater.com/research) but lacks a single bulk archive — lower priority.

### 2.5 DDQs — ILPA and AIMA templates

**FACTS:** ILPA DDQ 2.0 is free PDF with 20 topic areas and appendices ([ILPA DDQ 2.0 PDF](https://ilpa.org/wp-content/uploads/2021/11/ILPA-DDQ-2.0.pdf)). AIMA publishes modular DDQs (hedge, private credit, digital assets, managed accounts) for **AIMA members** with platform licensing terms ([AIMA DDQs](https://www.aima.org/sound-practices/due-diligence-questionnaires.html)).

**JUDGMENT:** **ILPA DDQ 2.0 is the home-dev canonical template** — map questions to Inv-Man-Intake Standard Element Library keys. Generate **synthetic filled DDQs** by programmatically answering ILPA questions with faker data + intentional conflicts between sections (e.g., AUM in Cover Sheet ≠ Track Record table). Reject AIMA templates for home corpus unless owner has membership (default: no).

### 2.6 Audited financial statements — public funds and N-CSR

**FACTS:** Registered funds file certified shareholder reports on **Form N-CSR** (annual) and N-CSRS (semi-annual) on EDGAR ([SEC Form N-CSR search](https://www.sec.gov/edgar/search/#/q=N-CSR&category=form-cat1)). N-PORT filings carry portfolio holdings. Pension plan audited financials appear in CAFRs discoverable via Pension-Data's `build_pension_sources.py` and PPD.

**JUDGMENT:** For **fund-level** audited financials, sample 20 N-CSR filings across mutual funds and interval funds (HTML/XBRL era) via `edgartools`. For **plan-level** statements, reuse Pension-Data annual-report PDFs already targeted by source collection — do not build a parallel CAFR crawler. Ground truth: XBRL tags where present; otherwise table cell coordinates + expected numeric values on 5 filings.

---

## 3. Synthetic-document generation for tests

| Approach | FACTS | Fit | Ground-truth strategy |
|----------|-------|-----|----------------------|
| **Template + controlled mutation** | DOCX/PDF generated from Jinja2 or `python-docx` with seeded RNG | Best for diff/lineage engines | Mutation manifest JSON: `{doc_id, base_hash, mutations:[{section, op, old, new}]}` |
| **ILPA DDQ synthetic fill** | ILPA template is structured Q&A | Inv-Man-Intake element coverage | Answer key YAML per generated packet |
| **Layout-preserving PDF clone** | Docling export → edit text layer → re-render | Consultant report drift | Store original bbox map; mutations are explicit string replacements |
| **LLM paraphrase variants** | LLM rewrites sections with temperature > 0 | Semantic alignment tests only | **Require** deterministic seed + retained source paragraph IDs; human review 10% sample |
| **Public doc corruption** | Inject OCR noise, page reorder, table shift | Parser robustness | Known corruption recipe per file |

**JUDGMENT:** Prefer **template mutation** over LLM generation for regression tests — LLM variants lack stable ground truth unless mutation prompts are logged and verified by substring match. Align synthetic bundles with Pension-Data replay contract (`corpus_id`, `corpus_schema_version` in `tools/replay/harness.py`).

---

## 4. Corpus plan by fleet tool

| Tool | Corpora | License / terms | Retained size | Ground-truth strategy |
|------|---------|-----------------|---------------|----------------------|
| **Doc-Lineage** | EDGAR EX-10 LPA chains (15–25); ILPA Model LPA PDF; CalPERS consultant YoY pair; Oaktree memo YoY subset; synthetic LPA mutations (50 variants) | SEC public domain; ILPA template free for reference; Oaktree client memos — research use with attribution | ~300 MB + 50 MB synthetic | Clause vocabulary keys (R1); mutation manifest; manual 10-doc span labels |
| **Mosaic synthesis** (future `Manager-Mosaic`) | Same manager across: ADV Part 2 brochure + Oaktree memo + EDGAR 13F (from Manager-Database fixtures) + synthetic DDQ with planted conflicts | As above | ~200 MB cross-source bundle | `fact_key` registry; planted contradictions with known `accepted_primary` |
| **Inv-Man-Intake** | ILPA DDQ 2.0 template; 10 synthetic filled DDQs; 3 public ADV Part 2 brochures; 2 CalPERS consultant PDFs | ILPA free; SEC public | ~150 MB | Standard Element Library coverage matrix; expected field values in YAML |
| **Manager-Database** | Retain existing 13F/13D fixtures; add **10 ADV Part 1 rows** (CSV join) + **5 Part 2 PDFs** for document embedding tests; do not re-download 13F at scale | SEC public | ~100 MB incremental | CSV field match for Part 1; holdings assertions stay on existing XML fixtures |
| **Pension-Data** | Extend source map: CalPERS IC crawl + SWIB meetings; 5 plan CAFR PDFs via existing collector; golden replay rows for consultant sections | Plan websites — public meeting materials | ~1 GB (optional local cache) | Replay harness comparable fields; consultant normalizers in `extract/governance/consultants.py` |

---

## 5. Ranked candidates

| Rank | What | Why it matters | Effort | Prerequisite | Disposition |
|------|------|----------------|--------|--------------|-------------|
| 1 | **`public-doc-fixtures` manifest repo** — content-addressed catalog (`corpus_id`, SHA-256, source URL, license, tool tags) | Single home for all fleet golden docs; enables Claude Code web without duplicating blobs per repo | **M** | Workflows `artifact-manifest/v1` | **new-repo** |
| 2 | **CalPERS IC packet harvester** extending `build_pension_sources.py` | Supplies consultant/board golden pairs R2 requires | **M** | source_map_v1 CalPERS row | **extend:Pension-Data** |
| 3 | **SEC Form ADV bulk ingest** (Part 1 CSV + Part 2/CRS PDF subset) | Stands in for manager regulatory filings absent from fleet | **M** | CRD pick list | **extend:Manager-Database** |
| 4 | **EDGAR EX-10 LPA harvest script** with version-chain metadata | Doc-Lineage legal lineage without proprietary LPAs | **M** | edgartools | **extend:Doc-Lineage** |
| 5 | **Synthetic mutation harness** (template DOCX/PDF + mutation manifest JSON) | Deterministic diff/lineage ground truth | **M** | Doc-Lineage segmenter | **extend:Doc-Lineage** |
| 6 | **ILPA DDQ synthetic fill generator** → Inv-Man-Intake bundles | DDQ extraction tests without manager data | **S** | Standard Element Library data file | **extend:Inv-Man-Intake** |
| 7 | **Oaktree Marks memo time-series slice** (1990–2025, yearly picks) | Manager letter blackline + thesis monitoring | **S** | public-doc-fixtures manifest | **adopt-ready-made:oaktree-memos** |
| 8 | **N-CSR sample ingest** (20 funds, latest annual) | Audited financial statement parser tests | **M** | edgartools | **extend:Pension-Data** |
| 9 | **Pension-Data replay corpus expansion** for consultant sections | Wires public PDFs into existing 1,382-test gate | **S** | #2 harvester output | **extend:Pension-Data** |
| 10 | **FINRA IARD API for ADV** | — | **S** | IARD entitlement | **reject** — restricted to entitled firms |
| 11 | **sec-api.io bulk EDGAR/ADV datasets** | — | **S** | paid subscription | **reject** — SEC primary sources suffice for home dev |
| 12 | **AIMA DDQ modules as home corpus** | — | **S** | AIMA membership | **reject** (default) — ILPA covers PE/VC DDQ shape |

---

## 6. Open questions for the owner

1. **Home corpus storage:** May downloaded public PDFs live in a **private GitHub fixtures repo** (~2 GB), or only on local disk? *(Default: private repo with LFS for PDFs; manifests in git, blobs in LFS.)*

2. **Plan proxy:** Is your state's IC packet structure closer to **CalPERS** (per-item PDFs + attachments) or **SWIB** (consolidated board book)? *(Default: CalPERS-style — drives harvester design.)*

3. **AIMA membership:** Do you have AIMA access for hedge-fund DDQ modules? *(Default: no — ILPA-only DDQ corpus.)*

4. **Manual labeling budget:** Can you label **~2 hours** of clause/section spans on 10 public docs for ground truth? *(Default: yes — without it, extraction metrics are unanchored.)*

---

## 7. Evaluator stance

Public corpora get the fleet to **80% document-type coverage** but **<50% term-specific accuracy** on fund legal variables without labels. The highest ROI is not more downloading — it is **#1 manifest + #5 synthetic mutations** so every diff test has a machine-readable answer key. I would deprioritize Manager-Database ADV ingest (#3) until Doc-Lineage and Inv-Man-Intake consume the manifest — otherwise ADV PDFs become orphaned blobs.

---

**STOP SIGNAL:** NEW_CANDIDATES=12
