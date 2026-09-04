# Brief R4: Document Access Substrate — Backstop, MCP, SharePoint, and Claude Code Web

**Question.** What should the owner plan for as the working substrate for document operations at work — given Backstop as system of record, possible SharePoint/local mirrors, MCP servers as connectors, and Claude Code web on a no-terminal work PC?

**Confidence.** High on the mirror-over-MCP direction for *agent batch work* and fleet contract alignment. Medium on SharePoint-as-mirror feasibility without IT-run sync. Low on Backstop document API surface (no public spec) and on any near-term Backstop MCP.

---

## 1. Problem framing

Work documents live in **Backstop** (ION Analytics). The owner builds with AI coding agents at home on public/synthetic data; at work the constraint model is **browser + Office + Claude Code web + file system, no terminal, no installs**. Every derived fact must link in one click to the primary document and page. Three existing work-side HTML tools (consultant blackline, legal lineage, manager-comms thesis monitor) already assume stable document identity and page anchors; they are not in this repo.

The assistant’s position to test: **“plan for the mirror as the working substrate; treat MCP as ingestion and back-link source.”**

**FACTS:** Doc-Lineage’s intent explicitly requires “one-click links back to the source document and page” (`clones/Doc-Lineage/README.md`). Workflows `evidence-object/v1` requires a stable `source_id` plus optional `locator.page` (`clones/Workflows/docs/contracts/schemas/evidence-object-v1.schema.json`). Pension-Data already implements content-hash dedupe, supersession, and `artifact:<hash>` IDs (`clones/Pension-Data/src/pension_data/ingest/artifacts.py`).

---

## 2. Backstop Solutions — documents, APIs, AI

### 2.1 What is publicly known

| Topic | FACTS (sourced) |
|-------|-----------------|
| **Document retrieval product** | **Backstop IntellX** automates retrieval of fund documents from source emails and portals and attaches them to funds/investments ([ionanalytics.com/backstop](https://ionanalytics.com/backstop/)). |
| **REST APIs** | Backstop offers **specially licensed REST APIs** to integrate with third-party systems and reporting engines; marketing copy does not publish document-specific endpoint catalogs ([ionanalytics.com/backstop](https://ionanalytics.com/backstop/), [ionanalytics.com/backstop/services/data-services](https://ionanalytics.com/backstop/services/data-services/)). |
| **Embedded AI** | Backstop has shipped **client-connected LLM** capability embedded in workflows — firms use **approved models only**, with confidentiality as a stated design constraint ([ionanalytics.com/blog/backstop/integrating-deal-investor-workflow-for-gps-and-lps](https://ionanalytics.com/blog/backstop/integrating-deal-investor-workflow-for-gps-and-lps/), [LinkedIn product post](https://www.linkedin.com/posts/backstop-solutions-group_solutions-in-action-voices-of-ion-analytics-activity-7424836642122735616-oep-)). |
| **MCP** | **No public announcement** of a Backstop Solutions Group MCP server or Model Context Protocol integration was found. A separate open-source project named “Backstop” (`github.com/pratyush2514/Backstop`) ships an MCP server for **PostgreSQL** — it is **not** the investment platform ([github.com/pratyush2514/Backstop](https://github.com/pratyush2514/Backstop)). |

**JUDGMENT:** Treat “Backstop MCP is coming” as **vendor hope, not plan dependency**. Until IT or Backstop account team confirms an MCP or documented document-export API, the owner should plan **export paths you control** (scheduled REST job by IT, SharePoint sync folder, or manual bulk export) plus a local manifest layer.

### 2.2 Implications for stable IDs and back-links

**FACTS:** Public materials do not document whether Backstop exposes immutable document IDs, permalink URLs, or page-level anchors to external integrators.

**JUDGMENT:** The mirror manifest must store **both** (a) a mirror-local content hash and path and (b) whatever opaque Backstop URL/ID the export provides — and treat Backstop URLs as **best-effort** until validated against a real export sample at work. Page-level one-click links will come from **derived locators** (PDF page, DOCX section) in `evidence-object/v1`, not from Backstop alone.

---

## 3. MCP servers — SharePoint, OneDrive, Microsoft Graph

### 3.1 Official Microsoft offerings

| Server | Scope | FACTS | Fit for document substrate |
|--------|-------|-------|---------------------------|
| **Microsoft MCP Server for Enterprise** | Entra ID / directory read-only | Preview at `https://mcp.svc.cloud.microsoft/enterprise`; **100 calls/min/user**; Graph throttling applies ([learn.microsoft.com/graph/mcp-server/overview](https://learn.microsoft.com/en-us/graph/mcp-server/overview)) | **Not for documents** — identity/admin scenarios only. |
| **Work IQ / OneDrive Remote MCP** | Files in M365 | Public preview; **~17 file tools**; **5 MB cap per file operation**; large uploads, delta sync, and version enumeration are Graph-API-only; typically requires M365 Copilot licensing ([scalekit.com/blog/onedrive-mcp-vs-api](https://www.scalekit.com/blog/onedrive-mcp-vs-api), [learn.microsoft.com/microsoft-agent-365/mcp-server-reference/odspremoteserver](https://learn.microsoft.com/en-us/microsoft-agent-365/mcp-server-reference/odspremoteserver)) | **Reject as bulk substrate.** Usable for ad-hoc reads of small files inside Copilot-governed agents, not consultant PDF corpora. |
| **SharePoint Embedded MCP** (`@microsoft/spe-mcp`) | SPE containers | Read-only mode, tool profiles, local developer tool ([learn.microsoft.com/sharepoint/dev/embedded/build/sharepoint-embedded-mcp-server](https://learn.microsoft.com/en-us/sharepoint/dev/embedded/build/sharepoint-embedded-mcp-server)) | Relevant only if the pension deploys **SharePoint Embedded** — unlikely for a standard SharePoint doc library mirror. |

### 3.2 Community / third-party MCP servers

| Project | Capabilities (claimed) | Caveats |
|---------|------------------------|---------|
| **ravikant1918/sharepoint-mcp** | List, KQL search, download, metadata, upload; Graph or REST; auto-retry on 429 ([github.com/ravikant1918/sharepoint-mcp](https://github.com/ravikant1918/sharepoint-mcp)) | Requires Entra app registration + secrets; **not** work-PC-no-install friendly unless IT hosts the server; security review required for pension data. |
| **sekops-ch/sharepoint-mcp-server** | Graph search, list sites/drives/items, text file content ([mcpservers.org/servers/sekops-ch/sharepoint-mcp-server](https://mcpservers.org/servers/sekops-ch/sharepoint-mcp-server)) | Text-only content tool — **unsuitable for binary PDF ingestion** without extension. |
| **softeria/ms-365-mcp-server** | Broad Graph surface (mail, files, SharePoint sites) ([mcpservers.org/servers/softeria/ms-365-mcp-server](https://mcpservers.org/servers/softeria/ms-365-mcp-server)) | Large tool surface increases agent misuse risk; still subject to Graph throttling. |

### 3.3 Rate limits and bulk download

**FACTS:** Microsoft Graph and SharePoint use **dynamic throttling** (HTTP 429/503 + `Retry-After`), not fixed per-minute download quotas ([learn.microsoft.com/graph/throttling](https://learn.microsoft.com/en-us/graph/throttling), [learn.microsoft.com/sharepoint/dev/general-development/how-to-avoid-getting-throttled-or-blocked-in-sharepoint-online](https://learn.microsoft.com/en-us/sharepoint/dev/general-development/how-to-avoid-getting-throttled-or-blocked-in-sharepoint-online)). Typical costs: **download = 1 resource unit**, multi-item list/upload = 2 RUs. Tenant-wide app limits scale with license count (e.g. up to **6,250 RUs/min** per app per tenant at 50k+ licenses). Bulk extraction at scale is explicitly steered toward **Microsoft Graph Data Connect**, not interactive MCP ([learn.microsoft.com/graph/throttling](https://learn.microsoft.com/en-us/graph/throttling)).

**JUDGMENT:** MCP is appropriate for **interactive probe, search, and incremental ingest** (tens–hundreds of files per session with backoff). It is **wrong as the runtime read layer** for Doc-Lineage blacklines, consultant variable extraction, or repeated CI — those need **local blobs + manifest**.

**Stable IDs:** Graph `driveItem` IDs are stable for a given item; **paths are not** (moves/renames). Manifests should key on `driveId` + `itemId` (or SharePoint `UniqueId`) plus content `sha256`, not folder path alone.

---

## 4. Claude Code web without a terminal

### 4.1 What works in the browser

**FACTS:**

- Claude Code on the web runs at [claude.ai/code](https://claude.ai/code) on Anthropic-managed VMs; sessions persist across browser close ([code.claude.com/docs/en/claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)).
- **GitHub App authorization during browser onboarding** is a first-class path — **no local terminal required** ([code.claude.com/docs/en/claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)).
- Cloud sessions **clone GitHub remotes** and push branches; they can access **any repo the connected GitHub account can see** ([code.claude.com/docs/en/claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)).
- Without GitHub, `claude --cloud` can **bundle-upload** a local git repo — but that requires the **CLI on a machine with terminal**, not the work browser-only model ([code.claude.com/docs/en/claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)).

### 4.2 What does *not* work for document operations

**FACTS:** Cloud sessions run in **isolated VMs** with restricted network; they do **not** mount the owner’s work filesystem, Backstop, or SharePoint unless exposed via (a) files committed to GitHub, (b) environment/network configuration in a cloud environment, or (c) explicit fetch from URLs the VM can reach ([code.claude.com/docs/en/claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web), [support.claude.com/en/articles/12618689](https://support.claude.com/en/articles/12618689-claude-code-on-the-web)).

**JUDGMENT:** At work, Claude Code web is a **code-and-PR agent against GitHub repos**, not a document browser. To use a mirror substrate with Claude Code web, the mirror’s **manifest and synthetic/public blob samples** must live in a repo the session can clone — not merely on `C:\Users\...\Documents`. Proprietary full mirrors stay on the work perimeter; only **schemas, validators, and public golden files** sync to GitHub for home/dev loops (matches R2’s synthetic corpus rule).

---

## 5. Mirror substrate — fleet-aligned pattern

Pension-Data’s artifact ingest is the closest fleet implementation of what R4 needs (`clones/Pension-Data/src/pension_data/ingest/artifacts.py`):

- Content keyed by `(plan_id, plan_period, source_url)` with **sha256** dedupe.
- New checksum → **supersede** prior active artifact, preserving lineage pointers.
- Deterministic `artifact:<digest>` IDs.

Inv-Man-Intake versions documents by `(fund_id, file_name)` with ordered `version_date` (`clones/Inv-Man-Intake/docs/contracts/core_schema.md`) — logical versioning without content addressing.

Workflows `artifact-manifest/v1` standardizes per-run outputs with `artifact_id`, `path`, `sha256` (`clones/Workflows/docs/contracts/schemas/artifact-manifest-v1.schema.json`).

**JUDGMENT:** The mirror should **unify** these: content-addressed blobs for immutability, logical source keys for supersession, `artifact-manifest/v1` for derived runs (Doc-Lineage blacklines, HTML reviews).

---

## 6. Adversarial test — “mirror = substrate; MCP = ingestion”

| Claim | Verdict | Strongest objection |
|-------|---------|---------------------|
| Agents should read local mirror blobs, not call MCP per fact | **Correct** for batch extraction, diff, and CI | MCP per-read is slow, throttled, and blows context on PDF bytes. |
| MCP is fine for ingestion/back-links | **Mostly correct** | **Overconfident** if ingestion volume is large — need scheduled Graph delta sync or Backstop export, not agent-driven MCP downloads. |
| Mirror replaces Backstop as authority | **Wrong** | Backstop remains **system of record** for permissions, workflow state, and “current” attachment; mirror is a **replica** with explicit `synced_at` and supersession. |
| Local mirror works on no-terminal work PC | **Overconfident** | Populating/updating the mirror without terminal implies **IT automation, SharePoint sync, or manual export** — the assistant elides who runs the ingest job. |
| SharePoint folder = mirror | **Incomplete** | A synced folder lacks manifest, supersession, and content-hash dedupe unless you add the manifest layer. |
| Backstop MCP will simplify this | **Speculative** | No public MCP; embedded LLM is **in-app**, not an external agent tool ([ionanalytics.com/blog/backstop/integrating-deal-investor-workflow-for-gps-and-lps](https://ionanalytics.com/blog/backstop/integrating-deal-investor-workflow-for-gps-and-lps/)). |
| One-click links “just work” from mirror | **Incomplete** | Requires **three URLs** in derived HTML: mirror blob path (or `file://` on work PC), source system URL (Backstop/SharePoint), and page anchor from `evidence-object/v1` locator. |

**Net judgment:** The assistant’s polarity is **directionally right** but **operationally thin**. Plan: **mirror + manifest as agent substrate**; **MCP/Graph/Backstop API as connectors** that *write into* the mirror on a schedule; **Backstop UI** remains authority for “what’s official today.”

---

## 7. Mirror layout specification (`document-mirror/v1`)

Proposed layout (POSIX paths; SharePoint sync maps 1:1):

```
<mirror_root>/
  mirror-manifest.json          # catalog — see schema below
  blobs/
    sha256/
      ab/cd/<full64hex>         # immutable bytes; extension in manifest only
  sources/                      # optional sidecars (export metadata, no secrets)
    backstop/<source_doc_id>.json
    sharepoint/<driveId>_<itemId>.json
  derived/
    <run_id>/                   # Doc-Lineage / consultant tools / HTML reviews
      artifact-manifest.json    # artifact-manifest/v1
      blackline.html
      variables.csv
  .mirror-lock                  # optional ingest lock file
```

**`mirror-manifest.json` (minimum fields):**

```json
{
  "schema_version": "document-mirror/v1",
  "mirror_id": "mirror:<tenant-slug>",
  "updated_at": "2026-09-04T18:00:00Z",
  "documents": [
    {
      "doc_uid": "doc:<stable-logical-key>",
      "logical_key": { "fund_id": "…", "doc_type": "consultant_report", "period": "2025-Q1" },
      "active_blob": "sha256:abcd…",
      "blob_path": "blobs/sha256/ab/cd/abcd…",
      "media_type": "application/pdf",
      "bytes": 1234567,
      "supersedes_doc_uid": "doc:…",
      "source_refs": [
        { "system": "backstop", "id": "…", "url": "https://…", "exported_at": "…" },
        { "system": "sharepoint", "drive_id": "…", "item_id": "…", "web_url": "https://…" }
      ],
      "entity_refs": ["pension:calpers"],
      "synced_at": "2026-09-04T17:55:00Z"
    }
  ]
}
```

**Link contract for HTML outputs:**

1. **Mirror link** — relative path under `<mirror_root>` (works offline on work PC).
2. **Source link** — `source_refs[].url` / `web_url` (opens Backstop or SharePoint).
3. **Page link** — `#page=N` or tool-specific anchor from `evidence-object/v1` `locator.page`.

**JUDGMENT:** Register `document-mirror/v1` as a Workflows satellite schema sibling to `artifact-manifest/v1` — do not overload `artifact-manifest` with source-system URLs.

---

## 8. Minimum home tool — `doc-mirror` CLI

Build at home on **synthetic/public folders only**; same binary validates real exports at work (data never leaves work).

| Command | Behavior |
|---------|----------|
| `doc-mirror init <mirror_root>` | Create directory skeleton + empty manifest. |
| `doc-mirror ingest <mirror_root> <folder> [--source backstop\|sharepoint\|local] [--mapping mapping.json]` | Walk folder; sha256-address blobs; append/ supersede manifest entries; reject path traversal. |
| `doc-mirror validate <mirror_root>` | Verify every `active_blob` exists, hashes match, `supersedes` chain acyclic, JSON schema valid. |
| `doc-mirror export-refs <mirror_root>` | Emit CSV of doc_uid → mirror_path → source_url for HTML tool integration. |

**Implementation judgment:** **New small repo** (`doc-mirror` or `extend:Workflows` scripts only) reusing Pension-Data’s supersession logic patterns — **do not** pull SQLAlchemy/DB into the mirror tool. Phase 1 (S): ingest + validate + golden synthetic fixture. Phase 2 (M): optional Graph delta adapter (Python, run by IT at work, not MCP). Phase 3 (M): Backstop export adapter once API shape is known.

---

## 9. Ranked candidates

| Rank | What | Why it matters | Effort | Prerequisite | Disposition |
|------|------|----------------|--------|--------------|-------------|
| 1 | **`doc-mirror` ingest + validate CLI** | Populates and proves the substrate at home; same tool gates work exports | **S** | none | **new-repo:doc-mirror** |
| 2 | **`document-mirror/v1` JSON schema** | Stable contract for manifest, source refs, supersession | **S** | Workflows contract process | **extend:Workflows** |
| 3 | **HTML triple-link resolver** (mirror + source + page) | Satisfies one-click standard for existing work HTML tools | **S** | document-mirror/v1 | **extend:Doc-Lineage** |
| 4 | **Pension-Data supersession patterns in mirror** | Avoid reinventing checksum/lineage logic | **S** | doc-mirror | **extend:Pension-Data** (library extract or copy) |
| 5 | **Scheduled Graph delta ingest** (non-MCP batch) | Reliable SharePoint/OneDrive sync without agent throttling | **M** | Entra app + IT job runner | **new-repo:doc-mirror** (subcommand) |
| 6 | **ravikant1918/sharepoint-mcp read-only probe** | Discover files/metadata interactively before batch ingest | **S** | Entra credentials | **adopt-ready-made:sharepoint-mcp** |
| 7 | **GitHub public mirror fixture repo** | Lets Claude Code web run against manifest + golden PDFs | **S** | doc-mirror synthetic corpus | **extend:Pension-Data** or **new-repo:doc-mirror-fixtures** |
| 8 | **Official Work IQ OneDrive MCP** | — | **S** | M365 Copilot | **reject** — 5 MB cap, preview instability ([scalekit.com/blog/onedrive-mcp-vs-api](https://www.scalekit.com/blog/onedrive-mcp-vs-api)) |
| 9 | **Microsoft MCP Server for Enterprise** | — | **S** | Entra | **reject** for documents — directory only ([learn.microsoft.com/graph/mcp-server/overview](https://learn.microsoft.com/en-us/graph/mcp-server/overview)) |
| 10 | **MCP-as-runtime document reader** | — | **M** | any MCP | **reject** — rate limits + context cost |
| 11 | **Wait for Backstop MCP** | — | **L** | vendor | **reject** as plan dependency — no public evidence |

---

## 10. Open questions for the owner

1. **Work mirror location:** Is a **local synced folder** (SharePoint → File Explorer) permitted, or must documents stay only inside Backstop’s UI? *(Default assumed: SharePoint or network folder sync allowed; full git mirror of proprietary docs is not.)*

2. **Who runs ingest at work?** Can IT schedule a **nightly Graph or Backstop export job**, or must the owner manually export? *(Default: manual quarterly export + ad-hoc — drives priority of `doc-mirror ingest` UX over delta sync.)*

3. **Backstop export shape:** Do exports include **stable document IDs and deep links**, or only files on disk? *(Default: files + opaque names — manifest will use content hash as primary key until proven otherwise.)*

4. **Claude Code web at work:** Is the pension’s Claude org on **Anthropic cloud sessions** (not Bedrock/Vertex), and is GitHub access to a **private fixtures repo** allowed? *(Default: yes to cloud sessions, private repo for schemas/fixtures only.)*

5. **Identity on manifest `entity_refs`:** With Manager-Database no longer absolute, should mirror entries carry **only `pension:` IDs** until authority is decided? *(Default: yes — optional `entity_refs` with `confidence` flag on unresolved names.)*

---

## 11. Evaluator stance — what would change my mind

- A **Backstop-documented** export API with immutable IDs and licensed MCP would downgrade candidate 11 from reject to adopt — I have **not** seen this as of 2026-09-04.
- If work IT confirms **no local mirror folder**, the substrate shifts to **SharePoint library + manifest stored as SharePoint list/JSON** — same schema, different `blob_path` prefix.
- If Claude Code web gains **native M365/Backstop connectors** (not evidenced today), re-evaluate MCP-as-runtime.

---

NEW_CANDIDATES=11
