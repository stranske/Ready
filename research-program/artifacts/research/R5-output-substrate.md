# Brief R5: Robust Output Surfaces for a No-Install Work PC

**Question.** Hand-built HTML reports work today but are brittle. What durable options exist for interactive, linkable, data-driven outputs that run from a file or a browser with no installation — and what single **output contract** (data files + renderer) should the fleet standardize on?

**Confidence.** High that **structured data artifacts + a shared, vendored renderer** beats hand-built HTML and beats unverified WASM for published work products. Medium on whether work PCs can use loopback HTTP for multi-file renderers (Python exists; `serve_local.py` is unprobed there). Low that Evidence, Observable, or stlite can become the fleet publish standard without violating the no-server constraint or passing a work-side WASM probe.

---

## 1. Problem framing (revised constraint model)

The owner produces consultant blacklines, legal clause trackers, manager-comms thesis monitors, and pension fact reviews as **HTML today**, authored or patched by AI agents. That works until layout, numbers, or evidence links drift.

**FACTS (work environment, 2026-09-04):** A real local Python interpreter exists (not on `PATH`, but usable by absolute path, including `pip` for pure-Python packages). Excel and Word are driven via COM today. Static local HTML pages are in **production use**, and **local-file deep links to specific pages of local documents work** — defects were path-configuration bugs, not platform refusal (`artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md` §A1, §A3). WebAssembly/stlite has **never been tested** there. Nothing server-hosted or database-backed runs in that environment. Proprietary data never leaves the work perimeter; every derived fact must link in one click to the primary document and page.

**FACTS (fleet contracts):** Workflows `evidence-object/v1` requires `source_id`, `method`, `excerpt`, and optional `locator.page` (`clones/Workflows/docs/contracts/schemas/evidence-object-v1.schema.json`). `artifact-manifest/v1` names hashed run artifacts with kinds including `report`, `data`, and `evidence` (`clones/Workflows/docs/contracts/schemas/artifact-manifest-v1.schema.json`).

**JUDGMENT:** The failure mode is not "HTML vs something else" — it is **HTML whose data and presentation are fused**. The fix is separating **regenerable data artifacts** from a **small, shared renderer** the owner never hand-edits. The earlier "browser-only, no Python" model was too pessimistic; the earlier "standardize on stlite because the fleet uses Pyodide" model was too optimistic for the work PC.

---

## 2. What exists today (work side + fleet)

### 2.1 Work-side tools (authoritative field names)

Three production tools already implement the target pattern incompletely: structured ledgers in, linked HTML (and Office files) out (`INFORMATION-REQUEST-RESPONSE.md` §D).

| Tool | Structured store | HTML pattern | Key ledger fields |
|------|------------------|--------------|-------------------|
| Consultant tracker | Change, continuity, persistence, stale-flag ledgers + section crosswalk | Coverage grid with page-deep links | `change_type`, segment vocab `VERBATIM/NEAR_VERBATIM/REVISED/NEW/DROPPED`, tiers `T1/T2/T3` |
| Legal lineage | Material ledger | Markdown + optional Excel | `Date \| Tier \| Theme \| Category \| Change \| From \| To` |
| Comms synthesis | Hand-edited structured file | Single-page HTML (newest renderer) | `fund`, `periods`, `entries`, `themes`, `documents`, `gaps` with per-mention `src` pointers |

**FACTS:** The work environment appendix names three duplicated implementations to absorb: one shared PDF-extraction library, one shared **structured-store → linked-HTML** renderer (a fourth about to be written), and one shared document-identity convention (`INFORMATION-REQUEST-RESPONSE.md` appendix). PowerPoint deck building is the highest-leverage gap — nearly all manager decks are hand-copied; exactly two have manifest-gated build pipelines.

**JUDGMENT:** Any fleet schema must **project onto these field names**, not invent parallel vocabularies. Identity and evidence authority remain open design questions (Manager-Database and Inv-Man-Intake are no longer assumed sources of truth).

### 2.2 Fleet repos (home development)

| Repo / surface | Pattern | Evidence | Fit for R5 |
|----------------|---------|----------|------------|
| **Deliverable-Render** | New repo: structured store → HTML hub + manifest-gated PPTX + DOCX; WASM forbidden until probed | `clones/Deliverable-Render/README.md` | **Implementation home** for the shared renderer the work env needs |
| **Pension-Data** | Pipeline emits `workspace.json`; static `apps/web/` with Load Local Bundle, PWA, vendored Plotly | `clones/Pension-Data/apps/web/README.md`, `apps/contracts/runtime-contract.json` | **Reference renderer** — data-driven, offline-capable; evidence links via `artifactBaseUrl` (`app.js:498-504`) |
| **Inv-Man-Intake** | Headless run writes `run.json` + manifest; `OnePagerModel.as_dict()` for renderers without HTML (`one_pager.py:44-47`) | `clones/Inv-Man-Intake/docs/design/operator-application.md` | Right **narrative content model**; Tier-A Pyodide path unverified at work |
| **Manager-Database / Trend_Model** | stlite/Pyodide static demos, vendored wheels, no CDN | `clones/Manager-Database/scripts/build_wasm_demo.py`, `Trend_Model_Project/demo/wasm/README.md` | Proven **home** interactive demos; **unverified** at work |
| **Portable-Alpha-Extension-Model** | Streamlit + Codespaces; explicitly rejects stlite (kaleido, python-pptx) | `clones/Portable-Alpha-Extension-Model/README.md:19` | Quant dashboards need server or Codespace, not WASM publish path |
| **Design system** | `tokens.css` + `components.css` synced from Workflows Template | `clones/Template/design-system/README.md` | Shared visual contract for static HTML renderers |

---

## 3. Option evaluation

### 3.1 Static-app frameworks

| Option | FACTS | File size / CSP | Local / SharePoint | Regeneration | Non-dev maintainer |
|--------|-------|-----------------|--------------------|--------------|-------------------|
| **Structured store + vendored static renderer** (Deliverable-Render / Pension-Data pattern) | Vanilla JS, vendored assets, optional PWA cache | Small renderer (~MB); data separate | Work: **single HTML + `file://` doc links confirmed**; fleet multi-file mode may need loopback HTTP (`serve_local.py`) or Load Local Bundle | Re-run pipeline → replace data/view artifacts | "Regenerate and open" — never edit HTML |
| **stlite / Pyodide** | Whole Python+Streamlit in browser; large cold start ([stlite overview](https://github.com/whitphx/stlite)) | **10–50+ MB** typical; Trend_Model vendors wheels to avoid CDN (`demo/wasm/README.md`) | **Untested at work**; `index.html` fetches sibling assets (problematic under SharePoint sandbox) | Rebuild when code *or* data changes | **Poor** for published artifacts |
| **Observable Framework** | SSG; data loaders at build time ([Observable Framework](https://observablehq.com/framework/what-is-framework)) | Moderate `dist/` | Static `dist/` on any host | `npm run build` when data changes | Needs Node — home-only |
| **Evidence.dev** | SQL+Markdown → static SvelteKit; DuckDB-WASM in browser ([Evidence](https://openapps.pro/apps/evidence)) | DuckDB WASM **~34 MB**; host limits ~25 MB ([discussion #3259](https://github.com/evidence-dev/evidence/discussions/3259)) | Static host; CDN breaks air-gap | Build-time SQL refresh | BI-as-code — wrong maintainer model |
| **DuckDB-WASM + Perspective** | Self-hosted WASM bundles supported ([DuckDB WASM docs](https://duckdb.org/docs/clients/wasm/instantiation)) | Large WASM payload | Embeddable in custom shell | Rebuild inputs | **JUDGMENT:** optional explorer widget inside fleet renderer, not whole stack |
| **Quarto `embed-resources: true`** | Single self-contained HTML ([Quarto HTML basics](https://quarto.org/docs/output-formats/html-basics.html)) | Can be very large | E-mail/synced-folder share | Re-render `.qmd` at home | Board one-offs with agent help |

### 3.2 Office-native delivery

| Option | FACTS | Verdict |
|--------|-------|---------|
| **Excel + COM / ledger export** | Excel COM confirmed at work; consultant and legal tools already emit workbooks | **JUDGMENT: adopt** for tabular ledgers — manifest CSV → workbook refresh |
| **Word tracked changes** | Work tools already generate DOCX memos; python-redlines path in fleet (B2-011) | **JUDGMENT: adopt** for legal/consultant sign-off — HTML is read-only view |
| **Manifest-gated PowerPoint** | One proven manager-deck pipeline with completeness gate at work | **JUDGMENT: adopt** — highest-leverage gap; generalize via Deliverable-Render `render/pptx` |
| **Office add-ins** | Require deployment/sideloading | **reject** under no-install constraint |

### 3.3 SharePoint, CSP, and local-file linking

**FACTS:**

- SharePoint HTML in document libraries runs in a **sandboxed iframe**: external HTTP scripts/styles blocked unless embedded; links open new tabs ([SharePoint HTML pages guide](https://spdenis.com/sharepoint-html-pages-what-they-can-and-cannot-do/)).
- SharePoint Online **CSP enforcement** tightens from March 2026 ([Microsoft Tech Community](https://techcommunity.microsoft.com/blog/spblog/sharepoint-online-content-security-policy-csp-enforcement-dates-and-guidance/4472662)).
- Work environment: **`file://` deep links from saved HTML to local PDF pages work in production** — this is the verification path today's tools depend on (`INFORMATION-REQUEST-RESPONSE.md` §A3).
- Pension-Data fleet renderer uses HTTP `artifactBaseUrl` for evidence links (`app.js:498-504`) — a different link profile than work-side `file://`.

**JUDGMENT:** Plan **two evidence-link profiles** in the output contract: (1) **`local-file`** — relative or absolute paths + page fragment for work synced-folder delivery; (2) **`artifact-http`** — Pension-Data loopback/intranet pattern. SharePoint favors **self-contained single HTML** (Quarto embed-resources or fully inlined bundle); multi-file renderer uses synced folder + double-click HTML or Load Local Bundle.

### 3.4 Offline operation

| Pattern | Offline? | Evidence |
|---------|----------|----------|
| Work-side single HTML + local doc mirror | Yes — no network once files are synced | Work env §A3, §D |
| Pension-Data PWA + cached bundle | Yes — service worker + `localStorage` | `apps/web/README.md` |
| stlite demo (home) | Yes — vendored runtime | `demo/wasm/README.md:118-119` |
| Excel workbooks | Yes — with cached data | Office behavior |

---

## 4. Recommended output contract

### 4.1 Name: **output-substrate/v1**

**JUDGMENT — fleet standard:**

```
run-contract/v1              # who ran what, when, on which inputs
artifact-manifest/v1         # named outputs + sha256 + kind
evidence-object/v1[]         # attributable facts (page, excerpt, method; method includes "ocr")
data/                        # domain payloads (JSON, CSV)
view/                        # renderer input — ONE profile per product:
  workspace-bundle.json      # Pension-Data tabular + provenance (generalized)
  report-spec.json           # Inv-Man-Intake OnePagerModel pattern
  consultant-ledger-bundle.json   # maps work change/continuity/persistence ledgers
  legal-material-ledger.json      # seven-column material ledger
  comms-mosaic-bundle.json          # fund/periods/entries/themes model
  blackline-bundle.json      # Doc-Lineage diff snapshots (future)
renderer/                    # vendored static shell (design-system, no CDN)
sources/                     # mirror pointers: local path, content-hash, optional driveItem id
link_profile: local-file | artifact-http
```

**Renderer rules:**

1. **Never embed proprietary data in HTML source** — only load via manifest-listed files (or inline a single generated bundle at render time).
2. **One-click evidence:** every displayed fact resolves `evidence_id` → `source_id` + `locator.page` → opens mirror PDF/DOCX using the active `link_profile`.
3. **Shared chrome:** `design-system/tokens.css` + `components.css` from Workflows Template.
4. **OCR-aware:** `method: "ocr"` on evidence objects where text layer was absent; coverage metrics must include OCR'd corpus.
5. **Regeneration:** owner or assistant re-runs pipeline; replaces `data/` + `view/`; renderer version bumps rarely.

### 4.2 What to reject as primary

| Approach | Why |
|----------|-----|
| Hand-built HTML | Unmergeable; silent link drift; fourth renderer rewrite imminent |
| stlite for published reports | Unverified at work; rebuild tax; PAEM-incompatible deps |
| Evidence / Observable as fleet standard | Node build on every change; DuckDB size |
| Server/database runtime | Blocked at work regardless of tool maturity |
| Office add-ins | Install/deploy barrier |

### 4.3 Secondary channels (keep)

- **stlite demos** (Manager-Database, Trend_Model) on synthetic data — after work-side WASM probe.
- **Quarto self-contained HTML** for board one-offs generated at home.
- **Excel workbooks** from manifest CSV for allocator tables.
- **Word tracked-changes** for legal/consultant authority.
- **Manifest-gated PPTX** for recurring manager decks.

---

## 5. Intermediate steps (ordered)

1. **Publish `output-substrate/v1` in Workflows** — extend `artifact-manifest/v1` kinds with `view-bundle`; document `link_profile` and view-profile schemas.
2. **Implement shared renderer in Deliverable-Render** — factor Pension-Data `apps/web/` evidence-link builder and bundle loader; add `local-file` link profile matching work-side deep links.
3. **Define `structured-store/v1`** — projection layer mapping work tool field names (§D) onto evidence-object refs without renaming owner vocabularies.
4. **Three view-profile adapters** — consultant-ledger, legal-material-ledger, comms-mosaic bundles consumed by the same renderer shell.
5. **Generalize `OnePagerModel` → `report-spec.json`** in Inv-Man-Intake; Doc-Lineage → `blackline-bundle.json` (R1/R2).
6. **Manifest-gated PPTX lane** in Deliverable-Render — generalize the one proven work-side deck pipeline.
7. **Work-side WASM probe** (`render/probe`) — binary pass/fail before any stlite delivery plan.
8. **CI gate:** golden view-bundle + renderer smoke test with **no network** (adapt `Inv-Man-Intake/tests/test_stlite_no_external_cdn.py` for static shell).

---

## 6. FACTS vs JUDGMENTS (summary)

**FACTS:**

- Work PC runs Python (off-PATH), COM-driven Office, and production HTML with working `file://` page links (`INFORMATION-REQUEST-RESPONSE.md`).
- WASM/stlite is untested at work; Deliverable-Render forbids WASM dependency until probe (`Deliverable-Render/README.md:11`).
- Three work tools use known ledger field names; three renderer implementations are duplicated (`INFORMATION-REQUEST-RESPONSE.md` §D, appendix).
- Pension-Data separates `workspace.json` from static renderer with Load Local Bundle (`apps/web/README.md`).
- SharePoint HTML sandbox blocks external resources; CSP tightens March 2026 (Microsoft, Denis Molodsov).
- OCR fallback recovered 20+ legal documents silently excluded from prior text-only analysis (`INFORMATION-REQUEST-RESPONSE.md` §C8).

**JUDGMENTS:**

- Standardize on **data artifacts + vendored static renderer** in Deliverable-Render, not stlite, for published HTML products.
- stlite remains the **interactive demo lane** only, pending work probe.
- Support **`local-file` and `artifact-http` link profiles** — do not assume Pension-Data's localhost pattern is the work default.
- Non-developer maintenance = regenerate bundle and open; editing HTML, SQL, or Python is a failure mode.
- Regeneration can run **at work** (Python exists) as well as home CI — only bundles cross zones, not raw manager data.

---

## 7. Ranked candidates

| Rank | Candidate | Why it matters | Effort | Prerequisite | Disposition |
|------|-----------|----------------|--------|--------------|-------------|
| 1 | **output-substrate/v1 contract** | Stops hand-built HTML; one regeneration story | M | Workflows schema | **extend:Workflows** (B2-028) |
| 2 | **Deliverable-Render shared renderer** | Absorbs 3 work-side + fleet duplicate HTML implementations | M | output-substrate/v1 | **extend:Deliverable-Render** |
| 3 | **structured-store/v1** (work-field-aligned) | No translation step between work tools and fleet | S | output-substrate/v1 | **extend:Workflows** |
| 4 | **local-file evidence link profile** | Matches production work verification path | S | renderer shell | **extend:Deliverable-Render** |
| 5 | **consultant-ledger view profile** | Consultant tracker HTML without hand-build | M | structured-store/v1 | **extend:Deliverable-Render** |
| 6 | **comms-mosaic view profile** | Fourth renderer rewrite avoided | M | structured-store/v1 | **extend:Deliverable-Render** |
| 7 | **manifest-gated PPTX builder** | Highest-leverage deck gap at work | M | structured-store/v1 | **extend:Deliverable-Render** |
| 8 | **workspace-bundle.json** (generalized) | Pension drilldown tables, charts | S | renderer shell | **extend:Pension-Data** (B2-030) |
| 9 | **report-spec.json** (OnePagerModel) | Manager scorecards, explainability | S | renderer shell | **extend:Inv-Man-Intake** (B2-031) |
| 10 | **blackline-bundle.json** + diff HTML | Consultant/legal YoY (R2) | L | Doc-Lineage engine | **extend:Doc-Lineage** (B2-009) |
| 11 | **Excel manifest export** | Native work-PC tables | S | output-substrate/v1 | **extend:Workflows** (B2-032) |
| 12 | **work-side WASM/stlite probe** | Unblocks or kills stlite hypothesis | S | none | **extend:Deliverable-Render** |
| 13 | **Quarto embed-resources lane** | Board one-off self-contained HTML | S | home render CI | **adopt-ready-made:quarto** (B2-033) |
| 14 | **Word tracked-changes export** | Authoritative redlines | M | Doc-Lineage diff | **extend:Doc-Lineage** (B2-034) |
| 15 | **stlite demo channel** | Interactive synthetic exploration | M | WASM probe pass | **adopt-ready-made:stlite** (B2-035, demos only) |
| 16 | **DuckDB-WASM table widget** | Client-side filter on bundled Parquet | M | renderer shell | **adopt-ready-made:duckdb-wasm** (B2-036) |
| 17 | **Evidence.dev full stack** | — | L | Node CI | **reject** (B2-R12) |
| 18 | **Observable Framework** | — | M | Node CI | **reject** (B2-R13) |
| 19 | **Office add-ins** | — | L | IT deploy | **reject** (B2-R14) |
| 20 | **Hand-built HTML** (status quo) | — | — | — | **reject** (B2-R15) |

---

## 8. Open questions for the owner

1. **Link profile at work:** Must evidence links stay **`file://` to the synced mirror** (today's production pattern), or is **`http://127.0.0.1`** acceptable for multi-file renderers? *(Default: `local-file` primary; loopback secondary for Pension-Data-style apps.)*

2. **Regeneration location:** With Python confirmed at work, should pipelines run **there via assistant** (faster iteration) or only **home CI** with bundles synced in? *(Default: both allowed; only artifact bundles cross zones.)*

3. **Authority format for redlines:** Is **Word tracked-changes** the sign-off artifact, HTML read-only? *(Default: yes.)*

4. **PowerPoint deliverable:** Are manifest-gated decks a **required** output channel alongside HTML for recurring manager reviews? *(Default: yes for annual diligence; HTML for analyst drilldown.)*

5. **Interactive vs snapshot:** Which tools need live client-side filtering (DuckDB widget) vs static snapshot sufficiency? *(Default: static for consultant/legal/comms; interactive only for synthetic surveillance demos.)*

---

## 9. Evaluator stance

The orchestrator direction — stop hand-building HTML — is correct. The strongest objection to the **prior** R5 draft is that it assumed a too-pessimistic work PC (no Python, `file://` broken) and a too-optimistic fleet path (stlite as publish channel). The 2026-09-04 answers invert both: **Python and `file://` deep links are proven; stlite is not.**

What would change my mind: (a) WASM probe passes under work browser policy with acceptable cold-start; (b) IT blocks all loopback HTTP, forcing single-file-only — then Quarto embed-resources becomes primary, not Pension-Data multi-file; (c) work-side tools resist structured-store migration because hand-edited fields (comms synthesis) need a gentler incremental path.

---

NEW_CANDIDATES=7
