# Brief R4: Document Access Substrate — Backstop, MCP, SharePoint, and Claude Code Web

**Question.** What should the owner plan for as the working substrate for document operations at work — given Backstop as system of record, an existing synced folder mirror, possible MCP connectors, and Claude Code web?

**Confidence.** High on mirror-plus-manifest as the agent substrate (the mirror already exists; the identity layer does not). Medium on SharePoint Graph ingest without IT-run jobs. Low on Backstop document API surface and any near-term Backstop MCP.

---

## 1. Problem framing

Work documents live in **Backstop** (ION Analytics). At work the confirmed runtime is **browser + Office + Claude Code + local Python (non-PATH) + PowerShell + synced folder tree** — not “browser-only, no Python” (`artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md` §A). Nothing server-hosted or database-backed runs there; every tool is a local script, COM-driven Office file, or static HTML page opened via `file://` deep links that **work in production** (same source, §A3, §D).

The document library is **already a mirror**: one folder per manager, then per document category (~3,800 PDFs, 480+ Excel, 170+ Word in the manager portion). There are **no stable document IDs** — filename is the de facto key; supersession is an ad hoc numeric-prefix convention; one tool already keys OCR side-files by **content hash** because path-based keys orphaned data on rename (same source, §C9–10).

Three HTML tools (consultant blackline, legal lineage, manager-comms thesis monitor) ship today with named schemas that must anchor any shared design (same source, §D). Fleet contracts require stable `source_id` plus `locator.page` on evidence (`clones/Workflows/docs/contracts/schemas/evidence-object-v1.schema.json`) and per-run `artifact-manifest/v1` outputs (`clones/Workflows/docs/contracts/schemas/artifact-manifest-v1.schema.json`). Doc-Lineage’s README now pins scope to identity, OCR-mandatory extraction, and those work-side field names (`clones/Doc-Lineage/README.md`).

The assistant’s position to test: **“plan for the mirror as the working substrate; treat MCP as ingestion and back-link source.”**

**JUDGMENT:** Correct polarity, but understated. The mirror is not hypothetical — the gap is a **manifest and identity layer** on top of the existing tree, plus OCR sidecars and triple-link HTML. MCP/connector search already exists for interactive discovery; bulk retrieval is **untested** (same source, §C11).

---

## 2. Backstop Solutions — documents, APIs, AI

| Topic | FACTS (sourced) |
|-------|-----------------|
| **IntellX** | Automates retrieval of fund documents from emails/portals into Backstop ([ionanalytics.com/backstop/resource/intellx-2/](https://ionanalytics.com/backstop/resource/intellx-2/)). |
| **REST APIs** | “Specially licensed REST APIs” for third-party integration; no public document-endpoint catalog ([ionanalytics.com/backstop/services/data-services/](https://ionanalytics.com/backstop/services/data-services/)). |
| **Embedded AI** | Client-connected LLM inside Backstop workflows; approved models only; confidentiality stated as design constraint ([ionanalytics.com/blog/backstop/integrating-deal-investor-workflow-for-gps-and-lps/](https://ionanalytics.com/blog/backstop/integrating-deal-investor-workflow-for-gps-and-lps/)). |
| **MCP** | **No public announcement** of a Backstop/ION MCP server. An unrelated open-source “Backstop” project exposes PostgreSQL MCP ([github.com/pratyush2514/Backstop](https://github.com/pratyush2514/Backstop)) — not the investment platform. |

**JUDGMENT:** Do not block on “Backstop MCP.” Plan export paths you control: licensed REST (IT), SharePoint sync (already in use), or connector-based retrieval. Backstop remains **system of record** for permissions and “current” attachment; the mirror is a **replica** with `synced_at` and supersession.

**FACTS:** Public materials do not document immutable document IDs, permalink URLs, or page anchors for external integrators. Direct stable links into “the document system” (vs. file path) are **unknown/untested** at work (same source, §A4).

**JUDGMENT:** Manifest entries need **three link targets**: mirror-relative path (offline), best-effort Backstop/SharePoint URL, and page anchor from `evidence-object/v1` `locator.page`.

---

## 3. MCP servers — SharePoint, OneDrive, Microsoft Graph

### 3.1 Official Microsoft

| Server | FACTS | Document substrate fit |
|--------|-------|------------------------|
| **Microsoft MCP Server for Enterprise** | Entra/directory read-only preview at `https://mcp.svc.cloud.microsoft/enterprise`; **100 calls/min/user**; Graph throttling applies ([learn.microsoft.com/graph/mcp-server/overview](https://learn.microsoft.com/en-us/graph/mcp-server/overview)). M365 APIs deferred to Agent 365 ([github.com/mcp/microsoft/EnterpriseMCP](https://github.com/mcp/microsoft/EnterpriseMCP)). | **Reject** for documents. |
| **Work IQ MCP** (SharePoint, OneDrive, Mail, Teams) | Preview; admin-governed in M365 admin center; read-only unless writes enabled; consumptive billing ([learn.microsoft.com/microsoft-agent-365/tooling-servers-overview](https://learn.microsoft.com/en-us/microsoft-agent-365/tooling-servers-overview)). | Interactive agent tooling, not batch corpus ingest. Third-party analysis cites **~5 MB per-file cap** on OneDrive MCP tools vs. full Graph for large files ([scalekit.com/blog/onedrive-mcp-vs-api](https://www.scalekit.com/blog/onedrive-mcp-vs-api)) — treat as a risk flag until validated on tenant. |
| **SharePoint Embedded MCP** (`@microsoft/spe-mcp`) | Read-only developer tool for SPE containers ([learn.microsoft.com/sharepoint/dev/embedded/build/sharepoint-embedded-mcp-server](https://learn.microsoft.com/en-us/sharepoint/dev/embedded/build/sharepoint-embedded-mcp-server)). | Only if pension deploys SPE — unlikely for standard doc library. |

### 3.2 Community servers

| Project | FACTS | Caveat |
|---------|-------|--------|
| **ravikant1918/sharepoint-mcp** | List, search, download, metadata, upload via Graph/REST ([github.com/ravikant1918/sharepoint-mcp](https://github.com/ravikant1918/sharepoint-mcp)). | Needs Entra app + hosted server or local install; security review for pension data. |
| **softeria/ms-365-mcp-server** | Broad Graph surface including files ([mcpservers.org/servers/softeria/ms-365-mcp-server](https://mcpservers.org/servers/softeria/ms-365-mcp-server)). | Large tool surface; agent misuse risk. |

### 3.3 Rate limits and stable IDs

**FACTS:** Graph/SharePoint use **dynamic throttling** (HTTP 429/503, `Retry-After`), not fixed download quotas ([learn.microsoft.com/graph/throttling](https://learn.microsoft.com/en-us/graph/throttling)). Bulk extraction at tenant scale is steered toward **Microsoft Graph Data Connect**, not interactive MCP.

**FACTS:** Graph `driveItem` `id` is stable for an item; **paths are not** after moves/renames.

**JUDGMENT:** MCP fits **interactive probe and incremental ingest** (tens–hundreds of files with backoff). It is wrong as the **runtime read layer** for blacklines, variable extraction, or repeated runs — those need local blobs + manifest. At work, connector search over mail/chat/document library **already exists**; treat MCP as overlapping capability, not a prerequisite.

---

## 4. Claude Code web without a terminal

**FACTS:**

- Cloud sessions run at `claude.ai/code` on Anthropic VMs; persist across browser close ([code.claude.com/docs/en/claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)).
- **GitHub App authorization during browser onboarding** is first-class — no local terminal required ([code.claude.com/docs/en/web-quickstart](https://code.claude.com/docs/en/web-quickstart)).
- Sessions **clone GitHub remotes** and push branches; access any repo the connected account can see.
- VMs do **not** mount the work filesystem, Backstop, or SharePoint unless exposed via GitHub, cloud env config, or reachable URLs ([code.claude.com/docs/en/claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)).
- Non-GitHub repos can be bundle-uploaded — but that requires **CLI on a machine with terminal**, not the work browser-only path for the owner.

**JUDGMENT:** At work, Claude Code web is a **code-and-PR agent against GitHub repos**, not a document browser. Proprietary mirrors stay on the work perimeter; **schemas, validators, and public/synthetic golden files** sync to GitHub for home/dev loops. Work-side document ops run via **local Python/PowerShell** driven by the in-environment assistant — a materially stronger substrate than this brief’s original constraint model assumed.

---

## 5. Mirror substrate — fleet-aligned pattern

Pension-Data’s artifact ingest is the closest fleet implementation: content keyed with **sha256** dedupe, supersession chain, deterministic `artifact:<digest>` IDs (`clones/Pension-Data/src/pension_data/ingest/artifacts.py`).

**JUDGMENT:** The work mirror should **add** this logic without relocating files: content-addressed blob references (or hash-verified paths into the existing tree), logical keys for supersession, `artifact-manifest/v1` for derived runs. OCR text sidecars keyed by `sha256` (already practiced at work) become a first-class `derived/ocr/` convention with `method: "ocr"` on evidence objects.

**FACTS:** A real minority of legal PDFs are scanned images; one OCR pass recovered 20+ documents and 500+ pages previously skipped by text-only pipelines (same source, §C8). Any coverage metric without OCR is **wrong**.

---

## 6. Adversarial test — “mirror = substrate; MCP = ingestion”

| Claim | Verdict | Strongest objection |
|-------|---------|---------------------|
| Agents should read local mirror blobs, not MCP per fact | **Correct** | MCP per-read is slow, throttled, and blows context on PDF bytes. |
| MCP is fine for ingestion/back-links | **Mostly correct** | **Overconfident** at ~3,800 PDFs — need scheduled Graph delta or folder-walk ingest, not agent-driven downloads. Connector bulk path is **untested**. |
| Mirror replaces Backstop as authority | **Wrong** | Backstop stays system of record; mirror is replica with explicit lineage. |
| “Plan for mirror” means greenfield | **Wrong** | Mirror **exists**; plan for **manifest overlay**, not new storage. |
| Local substrate works without terminal | **Revised** | Owner may not use terminal, but **Python + COM + static HTML already run**; ingest can be assistant-driven scripts, not IT-only. |
| Filename-as-ID is sufficient | **Wrong** | Proven failure mode: renames orphan OCR and break cross-tool joins; content hash + logical key required. |
| Backstop MCP will simplify this | **Speculative** | No public MCP; embedded LLM is in-app, not an external agent tool. |
| One-click links “just work” | **Incomplete** | Needs mirror path + source URL + page anchor; path-config bugs already occurred in production (same source, §D). |

**Net judgment:** Directionally right, operationally thin on **who maintains the manifest** and **OCR coverage**. Plan: existing folder tree + `document-mirror/v1` manifest; connectors/MCP write into or validate against the manifest; Backstop UI stays authority for “official today.”

---

## 7. Mirror layout specification (`document-mirror/v1`)

Non-destructive overlay on the existing manager → category tree (paths may point **into** the live tree rather than copying bytes):

```
<mirror_root>/
  mirror-manifest.json
  blobs/                        # optional; use when copying off-library
    sha256/ab/cd/<full64hex>
  ocr/                          # sha256-keyed text sidecars (work pattern)
    ab/cd/<full64hex>.txt
  sources/                      # export metadata, no secrets
    backstop/<opaque_id>.json
    sharepoint/<driveId>_<itemId>.json
  derived/<run_id>/
    artifact-manifest.json      # artifact-manifest/v1
    blackline.html
    variables.csv
```

**Minimum `mirror-manifest.json` fields:** `schema_version: "document-mirror/v1"`, `doc_uid`, `logical_key` (manager, category, period — aligned to folder names), `active_blob` or `mirror_relpath`, `sha256`, `media_type`, `supersedes_doc_uid`, `source_refs[]` (backstop + sharepoint), `ocr_sha256` (nullable), `synced_at`.

**Link contract:** (1) mirror-relative or `file://` path, (2) `source_refs[].url` / `web_url`, (3) `#page=N` or tool anchor. Register schema in Workflows alongside `artifact-manifest/v1` — do not overload artifact-manifest with source-system URLs.

**Schema alignment:** Derived variable ledgers should reuse work-side names — e.g. consultant `change_type` / `tier` / segment vocabulary; legal `Date|Tier|Theme|Category|Change|From|To`; comms `mentions[].src` pointers (same source, §D).

---

## 8. Minimum home tool — `doc-mirror` CLI

Build at home on **synthetic/public folders only**; same binary validates real exports at work (data never leaves work).

| Command | Behavior |
|---------|----------|
| `init <mirror_root>` | Skeleton + empty manifest. |
| `ingest <mirror_root> <folder> [--mode overlay\|copy] [--mapping mapping.json]` | Walk folder; compute sha256; map to logical keys from relative path; append/supersede; optional OCR sidecar hook. |
| `validate <mirror_root>` | Hash match, acyclic supersession, schema valid, every `mentions`-style pointer resolvable. |
| `export-refs <mirror_root>` | CSV: `doc_uid → mirror_path → source_url → page` for HTML tools. |

**JUDGMENT:** **New small repo** (`doc-mirror`), reusing Pension-Data supersession patterns without SQLAlchemy. Phase 1 (S): ingest + validate + synthetic fixture. Phase 2 (M): Graph delta adapter (IT-scheduled, not MCP). Phase 3 (M): Backstop export adapter once API shape is known.

---

## 9. Ranked candidates

| Rank | What | Why | Effort | Prerequisite | Disposition |
|------|------|-----|--------|--------------|-------------|
| 1 | **`doc-mirror` ingest + validate CLI** | Proves substrate at home; gates work overlay | S | none | **new-repo:doc-mirror** (B2-024) |
| 2 | **`document-mirror/v1` schema** | Manifest, source refs, OCR sidecar, supersession | S | Workflows process | **extend:Workflows** (B2-023) |
| 3 | **HTML triple-link resolver** | One-click standard for three work HTML tools | S | B2-023 | **extend:Doc-Lineage** (B2-025) |
| 4 | **Shared PDF extract + OCR fallback** | Replaces three divergent work implementations | M | B2-023 | **extend:Doc-Lineage** (B2-004) |
| 5 | **Graph delta ingest (non-MCP batch)** | Reliable sync without agent throttling | M | Entra app + IT job | **extend:doc-mirror** (B2-026) |
| 6 | **sharepoint-mcp read-only probe** | Discovery before batch ingest | S | Entra + security review | **adopt-ready-made:sharepoint-mcp** (B2-027) |
| 7 | **public-doc-fixtures golden corpus** | Claude Code web can clone schemas + PDFs | M | B2-023 | **new-repo:public-doc-fixtures** (B2-037) |
| 8 | **Work IQ OneDrive MCP as bulk substrate** | — | S | M365 Copilot | **reject** (B2-R08) — preview, file-size risk |
| 9 | **Microsoft MCP Server for Enterprise for docs** | — | S | Entra | **reject** (B2-R09) — directory only |
| 10 | **MCP-as-runtime document reader** | — | M | any MCP | **reject** (B2-R10) |
| 11 | **Wait for Backstop MCP** | — | L | vendor | **reject** (B2-R11) |

---

## 10. Open questions for the owner

1. **Manifest placement:** Store `mirror-manifest.json` at the library root, or in a sibling `_meta/` folder to avoid sync churn? *(Default: `_meta/` at mirror root.)*

2. **Connector bulk retrieval:** Will you run a one-time test of bulk list/download via the existing connector before building Graph automation? *(Default: yes — outcome changes priority of B2-026 vs. assistant-driven folder walks.)*

3. **Backstop deep links:** Do exports or UI expose stable document URLs? *(Default: unknown — manifest uses sha256 primary until proven otherwise.)*

4. **Git on shared drive:** Is a git working tree on the synced library permitted? *(Default: no — sync churn risk flagged at work, §E16.)*

5. **`entity_refs` authority:** With Manager-Database no longer absolute, carry optional `entity_refs` with `confidence` until identity authority is decided? *(Default: yes — per `clones/Workflows/docs/contracts/identity-map-conventions.md`.)*

---

## 11. Evaluator stance

- **Backstop-documented** export API + MCP would reopen candidate 11 — not seen as of 2026-09-04.
- If connector bulk test **fails**, shift ingest to **path-walk + hash** on the existing sync folder (no new infrastructure).
- If IT forbids manifest files on the share, store manifest in a **local-only `_meta`** path with relative pointers into the library.

---

NEW_CANDIDATES=0
