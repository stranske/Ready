# Brief R5: Robust Output Surfaces for a No-Install Work PC

**Question.** Hand-built HTML reports work today but are brittle. What durable options exist for interactive, linkable, data-driven outputs that run from a file or a browser with no installation — and what single **output contract** (data files + renderer) should the fleet standardize on?

**Confidence.** High that **data artifacts + a vendored static renderer** beats hand-built HTML and beats stlite for fleet-wide *published outputs*. Medium on SharePoint as the primary delivery channel without IT-confirmed sync. Low that any one third-party framework (Evidence, Observable) fits the no-terminal work-PC constraint without a home-build CI step.

---

## 1. Problem framing

The owner produces investment work products — consultant blacklines, legal clause trackers, manager-comms thesis monitors, pension fact reviews — as **HTML today**, authored or patched by AI agents. That works until layout, numbers, or evidence links drift. The constraint model: **browser + Office + Claude Code web + file system, no terminal, no installs**; proprietary data never leaves the work perimeter; every derived fact must link in one click to the primary document and page.

**FACTS:** Doc-Lineage's stated intent is a Python library plus static/offline review surface producing HTML and CSV with one-click source links (`clones/Doc-Lineage/README.md`). Workflows `evidence-object/v1` requires `source_id`, `method`, `excerpt`, and optional `locator.page` (`clones/Workflows/docs/contracts/schemas/evidence-object-v1.schema.json`). `artifact-manifest/v1` names hashed run artifacts with kinds including `report`, `data`, and `evidence` (`clones/Workflows/docs/contracts/schemas/artifact-manifest-v1.schema.json`).

**JUDGMENT:** The failure mode is not "HTML vs something else" — it is **HTML whose data and presentation are fused**. The fix is separating **regenerable data artifacts** from a **small, shared renderer** the owner never hand-edits.

---

## 2. What the fleet already does

| Repo / surface | Pattern | Evidence | Fit for R5 |
|----------------|---------|----------|------------|
| **Pension-Data** | Pipeline emits JSON; `build_workspace_bundle.py` produces `workspace.json`; static `apps/web/` loads bundle via HTTP, PWA, or "Load Local Bundle" | `clones/Pension-Data/apps/web/README.md`, `apps/contracts/runtime-contract.json`, `apps/web/app.js:498-504` (evidence links via `artifactBaseUrl`) | **Closest to target contract** — data-driven, offline-capable, design-system styled |
| **Inv-Man-Intake** | Headless run writes `run.json` + manifest; `OnePagerModel` is JSON for renderers; Tier-A static Pyodide SPA planned | `clones/Inv-Man-Intake/docs/design/operator-application.md`, `src/inv_man_intake/export/one_pager.py` | Right **content model**; browser path still immature (text-only upload bridge) |
| **Manager-Database** | Full Streamlit app compiled to stlite/Pyodide static demo with vendored runtime | `clones/Manager-Database/scripts/build_wasm_demo.py`, dossier §2 | Proven **zero-install interactive demo**, heavy payload |
| **Trend_Model_Project** | stlite bundles real Streamlit app; `presentation_safe` profile blocks LLM/upload; vendored wheels, no CDN | `clones/Trend_Model_Project/demo/wasm/README.md` | Reference for **CSP-safe WASM packaging** |
| **Portable-Alpha-Extension-Model** | Streamlit + Codespaces for terminal-free use; **explicitly rejects** stlite (kaleido, python-pptx) | `clones/Portable-Alpha-Extension-Model/README.md:19` | **JUDGMENT:** interactive quant dashboards need server or Codespace, not WASM |
| **Doc-Lineage** | Scaffold only; targets HTML + CSV blackline outputs | `clones/Doc-Lineage/README.md` | Future consumer of shared renderer |
| **Design system** | `tokens.css` + `components.css` + `ds_streamlit.py` synced from Workflows Template | `clones/Template/design-system/README.md` | Shared visual contract for static HTML renderers |

**JUDGMENT:** The fleet is **not starting from zero** — Pension-Data's workspace bundle + static web app is the embryonic standard. stlite is a **parallel track for demos**, not the publish path for consultant/legal/manager HTML products.

---

## 3. Option evaluation

### 3.1 Static-app frameworks

| Option | FACTS | File size / CSP | Local / SharePoint | Regeneration | Non-dev maintainer |
|--------|-------|-----------------|--------------------|--------------|-------------------|
| **Pension-Data static renderer + JSON bundle** | Vanilla JS, vendored Plotly, service-worker offline cache (`apps/web/README.md`) | Small renderer (~MB); data separate; no inline-script CSP fight if assets are sibling files | Needs **HTTP** (`serve_local.py` at home); `file://` unreliable for fetch (`stlitepack` docs: [github.com/hsma-tools/stlitepack](https://github.com/hsma-tools/stlitepack)) | Re-run pipeline → replace `workspace.json` | Owner loads new bundle; never edits HTML |
| **stlite / Pyodide** | Whole Python+Streamlit in browser; large cold start ([whitphx stlite post](https://www.whitphx.info/posts/20221104-streamlit-wasm-stlite/)) | **10–50+ MB** typical; Trend_Model vendors wheels to avoid CDN ([demo/wasm/README.md](clones/Trend_Model_Project/demo/wasm/README.md)) | Same HTTP requirement; offline after first load | Rebuild WASM site when code *or* data changes | **Poor** — rebuild is developer workflow |
| **Observable Framework** | SSG; data loaders at build time ([observablehq.com/framework/what-is-framework](https://observablehq.com/framework/what-is-framework)) | Moderate `dist/`; precomputed snapshots | Static `dist/` on any host | `npm run build` when data changes | Needs Node toolchain — **not work-PC friendly** |
| **Evidence.dev** | SQL+Markdown → static SvelteKit; DuckDB-WASM in browser ([openapps.pro/apps/evidence](https://openapps.pro/apps/evidence)) | DuckDB WASM **~34 MB**; Cloudflare 25 MB limit ([github.com/evidence-dev/evidence/discussions/3259](https://github.com/evidence-dev/evidence/discussions/3259)) | Static host; CDN option breaks air-gap | Build-time SQL refresh | BI-as-code — owner would edit `.md` + SQL, not ideal |
| **DuckDB-WASM + Perspective** | DuckDB supports self-hosted WASM bundles ([duckdb.org/docs/clients/wasm/instantiation](https://duckdb.org/docs/clients/wasm/instantiation)) | Large WASM; threaded mode needs cross-origin isolation | Embeddable in custom static shell | Rebuild Parquet/JSON inputs | **JUDGMENT:** adopt as **optional explorer widget** inside fleet renderer, not whole stack |
| **Quarto `embed-resources: true`** | Single self-contained HTML ([quarto.org/docs/output-formats/html-basics.html](https://quarto.org/docs/output-formats/html-basics.html)) | File can be **very large** (embedded plots); render needs network once | E-mail/Dropbox/SharePoint file share | Re-render `.qmd` when data changes | Owner edits Quarto with agent help at home; ship HTML to work |

### 3.2 Office-native delivery

| Option | FACTS | Verdict |
|--------|-------|---------|
| **Excel + Power Query** | Native on work PC; refresh from folder/SharePoint | **JUDGMENT: adopt for tabular exports** — manifest CSV/Parquet → workbook; not for narrative blacklines |
| **Word tracked changes** | Doc-Lineage targets DOCX blackline ([R2 brief](artifacts/research/R2-consultant-report-diffing.md)); python-redlines generates `w:ins`/`w:del` | **JUDGMENT: adopt for legal/consultant review** — HTML is view; Word is authority for redlines |
| **Office add-ins** | Require deployment/sideloading | **reject** under no-install constraint ([learn.microsoft.com/sharepoint/allow-or-prevent-custom-script](https://learn.microsoft.com/en-us/sharepoint/allow-or-prevent-custom-script)) |

### 3.3 PDF / verification HTML

**FACTS:** Quarto and pipeline HTML can embed verification hashes in footer metadata. Pension-Data manifest already carries `sha256` per artifact (`artifact-manifest-v1.schema.json`).

**JUDGMENT:** Published HTML should display **manifest digest + run_id** and link to `evidence-object/v1` records — not a separate PDF pipeline unless the audience requires print.

### 3.4 SharePoint and local-file linking

**FACTS:**

- Opening HTML from SharePoint document libraries uses a **sandboxed iframe**: no external HTTP, scripts, stylesheets, or fonts unless embedded; links open in new tabs ([spdenis.com/sharepoint-html-pages](https://spdenis.com/sharepoint-html-pages-what-they-can-and-cannot-do/)).
- SharePoint Online **CSP enforcement begins March 1, 2026**, blocking untrusted and inline scripts ([techcommunity.microsoft.com/sharepoint-csp](https://techcommunity.microsoft.com/blog/spblog/sharepoint-online-content-security-policy-csp-enforcement-dates-and-guidance/4472662)).
- `file://` opening breaks fetch/CORS for multi-file static apps ([stlitepack README](https://github.com/hsma-tools/stlitepack)).

**JUDGMENT:** For work delivery, plan three tiers: (1) **self-contained single HTML** (Quarto embed-resources or inlined bundle) for SharePoint double-click; (2) **synced folder + internal static host** (loopback or intranet) for Pension-Data multi-file renderer; (3) **JSON bundle + renderer** where the owner uses "Load Local Bundle" from synced files. Do **not** assume SharePoint can host a multi-asset stlite site without embedding everything.

### 3.5 Offline operation

| Pattern | Offline after first load? | Evidence |
|---------|---------------------------|----------|
| Pension-Data PWA + cached bundle | Yes — service worker + `localStorage` saved views | `apps/web/README.md`, `app.js:5-6` |
| stlite demo | Yes — vendored runtime | `Trend_Model_Project/demo/wasm/README.md:118-119` |
| Observable / Evidence `dist/` | Yes — static assets | Framework docs |
| Excel Power Query | Yes — with cached query results | Office behavior |

---

## 4. Recommended output contract

### 4.1 Contract shape (name: **output-substrate/v1**)

**JUDGMENT — propose this as fleet standard:**

```
run-contract/v1          # who ran what, when, on which inputs
artifact-manifest/v1     # named outputs + sha256 + kind
evidence-object/v1[]     # one file per attributable fact (page, excerpt, method)
data/                    # domain payloads (JSON, CSV, Parquet)
view/                    # renderer input — ONE of:
  workspace-bundle.json  # Pension-Data tabular + provenance (generalized)
  report-spec.json       # Inv-Man-Intake OnePagerModel pattern (narrative + scorecards)
  blackline-bundle.json  # Doc-Lineage diff + variable snapshots (future)
renderer/                # vendored static shell (shared design-system, no CDN)
sources/                 # optional mirror pointers (Backstop URL, driveItem id, local path)
```

**Renderer rules:**

1. **Never embed proprietary data in HTML source** — only load via manifest-listed files.
2. **One-click evidence:** every displayed fact resolves `evidence_id` → `source_id` + `locator.page` → opens mirror PDF/DOCX (Pension-Data pattern: `artifactBaseUrl` + encoded fragment, `app.js:498-504`).
3. **Shared chrome:** `design-system/tokens.css` + `components.css` from Workflows Template (`clones/Template/design-system/README.md`).
4. **Regeneration:** owner replaces `data/` + `view/` artifacts; renderer version bumps rarely.

### 4.2 What to reject as primary

| Approach | Why |
|----------|-----|
| Hand-built HTML | Unmergeable; breaks evidence links silently |
| stlite for published reports | Rebuild cost, size, PAEM-incompatible deps ([PAEM README:19](clones/Portable-Alpha-Extension-Model/README.md)) |
| Evidence / Observable as fleet standard | Requires Node build on every data change — home-only |
| MCP/runtime queries in the browser | R4 already rejects MCP as document runtime |
| Office add-ins | Install/deploy barrier |

### 4.3 What to keep as secondary channels

- **stlite demos** (Manager-Database, Trend_Model) for interactive exploration on synthetic data.
- **Quarto self-contained HTML** for board one-offs generated at home.
- **Excel workbooks** fed from manifest CSV exports for allocator tables.
- **Word tracked-changes** from Doc-Lineage for legal/consultant review authority.

---

## 5. Intermediate steps (ordered)

1. **Publish `output-substrate/v1` schema in Workflows** — extend `artifact-manifest/v1` kinds with `view-bundle`; document `workspace-bundle` required fields (already in `runtime-contract.json`).
2. **Extract shared `renderer-shell/` into Workflows Template** — factor Pension-Data `apps/web/` (bundle loader, evidence link builder, offline cache) into a reusable package; design-system already synced.
3. **Generalize `OnePagerModel` → `report-spec.json`** in Inv-Man-Intake; Tier-A SPA (#723) becomes a second renderer profile, not a separate HTML product.
4. **Emit `evidence-object/v1` files** from Pension-Data and Inv-Man-Intake (today: hashes/strings only — dossiers §5).
5. **Doc-Lineage consumes `blackline-bundle.json`** + same renderer shell for diff HTML (R1/R2 scope).
6. **Migrate work-side HTML tools** (consultant tracker, legal lineage, comms monitor) to emit view bundles; keep one legacy HTML adapter quarter.
7. **CI gate:** golden `view-bundle.json` + renderer smoke test with **no network** (pattern: `Inv-Man-Intake/tests/test_stlite_no_external_cdn.py` adapted for static shell).

---

## 6. FACTS vs JUDGMENTS (summary)

**FACTS (sourced or repo-cited):**

- Pension-Data separates generated `workspace.json` from static renderer and supports local bundle load (`apps/web/README.md`).
- Inv-Man-Intake `OnePagerModel.as_dict()` is explicitly for HTML/print renderers without rendering HTML (`one_pager.py:44-47`).
- Manager-Database and Trend_Model ship vendored stlite/Pyodide with no CDN (`demo/wasm/README.md`, `test_stlite_no_external_cdn.py`).
- PAEM rejects WASM because of kaleido and python-pptx (`README.md:19`).
- SharePoint HTML sandbox blocks external resources; CSP tightens March 2026 (Microsoft Tech Community, Denis Molodsov blog).
- DuckDB WASM bundles exceed common static-host size limits (~25–34 MB) ([Evidence discussion #3259](https://github.com/evidence-dev/evidence/discussions/3259)).
- Quarto `embed-resources: true` produces standalone HTML ([quarto.org/docs/output-formats/html-basics.html](https://quarto.org/docs/output-formats/html-basics.html)).

**JUDGMENTS (labeled):**

- **JUDGMENT:** Standardize on **data artifacts + vendored static renderer**, not stlite, for fleet HTML products.
- **JUDGMENT:** stlite remains the **interactive demo lane** only.
- **JUDGMENT:** SharePoint favors **single-file** outputs; multi-file renderer needs synced folder + local HTTP or intranet host.
- **JUDGMENT:** Non-developer maintenance = "regenerate bundle and open" — not edit HTML, Markdown SQL, or Python.
- **JUDGMENT:** DuckDB-WASM fits as an **optional embedded table engine** inside the shared renderer, not as Evidence-the-framework.

---

## 7. Ranked candidates

| Rank | Candidate | Why it matters | Effort | Prerequisite | Disposition |
|------|-----------|----------------|--------|--------------|-------------|
| 1 | **output-substrate/v1 contract** (manifest + view-bundle + evidence objects + renderer) | Stops hand-built HTML; one regeneration story | **M** | Workflows schema PR | **extend:Workflows** |
| 2 | **Shared renderer-shell** (Pension-Data `apps/web` factored) | One viewer for pension, intake, lineage products | **M** | output-substrate/v1 | **extend:Pension-Data** → Template |
| 3 | **workspace-bundle.json** (generalized tabular view) | Powers drilldown tables, charts, CSV export | **S** | renderer-shell | **extend:Pension-Data** |
| 4 | **report-spec.json** (OnePagerModel generalized) | Manager scorecards, explainability, one-pagers | **S** | renderer-shell | **extend:Inv-Man-Intake** |
| 5 | **blackline-bundle.json** + diff HTML view | Consultant/legal YoY products (R2) | **L** | Doc-Lineage engine | **extend:Doc-Lineage** |
| 6 | **Excel manifest export** (CSV from artifact-manifest) | Native work-PC tables with refresh | **S** | output-substrate/v1 | **extend:Workflows** |
| 7 | **Quarto embed-resources publish lane** | Board one-off self-contained HTML | **S** | home render CI | **adopt-ready-made:quarto** |
| 8 | **Word tracked-changes export** (Doc-Lineage) | Authoritative redlines for counsel | **M** | Doc-Lineage diff engine | **extend:Doc-Lineage** |
| 9 | **stlite demo channel** (Manager-Database pattern) | Interactive synthetic exploration | **M** | vendored runtime | **adopt-ready-made:stlite** (demos only) |
| 10 | **DuckDB-WASM table widget** inside renderer | Client-side filter/pivot on bundled Parquet | **M** | renderer-shell | **adopt-ready-made:duckdb-wasm** |
| 11 | **Evidence.dev full stack** | — | **L** | Node CI | **reject** — build + size + air-gap |
| 12 | **Observable Framework** | — | **M** | Node CI | **reject** — same |
| 13 | **Office add-ins** | — | **L** | IT deploy | **reject** — install barrier |
| 14 | **Hand-built HTML** (status quo) | — | — | — | **reject** |
| 15 | **SharePoint multi-file stlite host** | — | **L** | IT | **reject** — sandbox + size |

---

## 8. Open questions for the owner

1. **Delivery path at work:** Is a **synced SharePoint/local folder** plus double-click acceptable, or must outputs open from **Backstop links only**? *(Default: synced folder allowed; renderer uses Load Local Bundle or self-contained HTML.)*

2. **Internal HTTP:** Can the work PC open `http://127.0.0.1` or an **intranet static host** for multi-file renderers, or is **single-file-only** mandatory? *(Default: single-file for SharePoint, loopback allowed for review — mirrors Pension-Data `serve_local.py` posture.)*

3. **Authority format for redlines:** Is **Word tracked-changes** the sign-off artifact, with HTML as read-only view? *(Default: yes — aligns with Doc-Lineage and R2.)*

4. **Interactive vs publish:** Which existing HTML tools need **live filtering** (favors DuckDB widget) vs **static snapshot** sufficiency? *(Default: static snapshot for consultant/legal; interactive for manager surveillance demos.)*

5. **Build location:** Confirm all regeneration stays **home CI / Claude Code web**, with only bundles crossing to work. *(Default: yes — matches proprietary-zone rule.)*

---

## 9. Evaluator stance

The orchestrator brief is directionally right: stop hand-building HTML. The strongest objection to "standardize on stlite because the fleet already uses Pyodide" is **PAEM's explicit WASM rejection** and the **regeneration tax** — every data refresh would require a developer rebuild, which violates the non-developer maintainer goal. stlite is correct for **demos**; it is wrong for **published artifacts**.

What would change my mind: (a) a stlitepack workflow that loads **only data archives** at runtime without Python code changes, proven under SharePoint sandbox; (b) IT approving a permanent intranet static host with CSP-trusted script sources; (c) Evidence shrinking DuckDB WASM below 10 MB bundled.

---

NEW_CANDIDATES=15
