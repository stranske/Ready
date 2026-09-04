# Track C: Skill Curriculum and Tool-Literacy Loop (LMS-Connected)

**Date:** 2026-09-04  
**Inputs:** `artifacts/skill-coverage/COVERAGE_MATRIX.md`, `artifacts/dossiers/00-INDEX.md`, LMS clone (`learning-management-system`), owner problem statement.  
**Confidence:** High on coverage read and LMS wiring (evidence-bound). Medium on hour estimates (depends on owner prior exposure). Low on Office add-ins timing (no fleet CENTRAL surface yet).

---

## 1. Honest coverage read: learn what you already built

The owner's stated problem — *"your ability to do work outstrips my ability to understand it"* — is accurate and asymmetric. The fleet is not a beginner's sandbox; it is a production-adjacent portfolio where agents, CI belts, extraction pipelines, and contract validators already run. The curriculum must therefore bias toward **comprehension and judgment**, not greenfield implementation. Categories marked **CENTRAL** in the coverage matrix are load-bearing; the owner should **study them in situ** before building parallel abstractions.

### 1.1 Learn-first (CENTRAL depth exists — do not rebuild)

| Category | Where it lives | What to learn (non-coder framing) |
|---|---|---|
| **Agent orchestration** | Orchestrator (`dispatcher`, `tick`, MCP server); Workflows (`agents-auto-pilot`, codex-belt) | How tasks route across agents, what a "rail" is, when the fleet asks you a question vs. proceeds |
| **LangChain (product chains)** | Manager-Database RAG chains; Trend_Model LLM patches; PAEM provider; Workflows integration layer | Chains as *pipelines*: input document → structured steps → output; not "a library" but a wiring pattern |
| **LangSmith tracing** | Workflows fleet conformance; MD/IMI/TMP/PAEM emitters | Traces as flight recorders: what ran, what failed, what to inspect when behavior drifts |
| **Structured extraction** | Inv-Man-Intake, TMP, PAEM, LMS | Schema-first extraction: define the shape of truth before calling a model; validate on the way out |
| **Document parsing** | Counter_Risk PDF parsers; IMI Docling; Workflows `stranske_pdf_extract` | Parser = boundary between messy files and typed records; eval harnesses prove parser quality |
| **Diff / lineage** | Pension-Data entity lineage; IMI audit lineage | Lineage answers "where did this number come from and what changed?" — essential for trust |
| **Data pipelines / ETL** | Manager-Database Prefect flows; Counter_Risk pipeline; Pension-Data ingest | Scheduled jobs that move data with checkpoints; failure modes are operational, not theoretical |
| **Entity resolution** | Counter_Risk name registry; Pension-Data matching; Fine-Art-Archive artist lookup | Same real-world thing, many strings — registries and merge rules prevent silent duplication |
| **CI / test infrastructure** | Workflows coverage guard, deliberate-break gate; WIT cross-repo harness | Tests as contracts: a deliberate break must fail; golden files freeze expected behavior |
| **Static / offline apps** | TMP/PAEM/IMI Pyodide paths; LMS PWA shell | Apps that run without cloud egress — architecture for air-gapped review |
| **Packaging** | Counter_Risk PyInstaller; PAEM portable zip | Shipping a folder someone can double-click — different problem than "it works on my machine" |
| **Eval harnesses (partial)** | Pension-Data `eval_harness`; WF PDF extract evals; LMS `eval_sets` | Golden inputs → expected outputs; regression when prompts or models change |

**Strongest objection to "learn only":** CENTRAL does not mean *understood*. Workflows alone bundles LangSmith conformance, consumer sync, PDF extraction, and repo-review scoring — four distinct competencies hiding under one repo name. The curriculum must **decompose by surface and contract**, not by repository folder.

### 1.2 Gaps where building (or adopting) is justified

| Category | Fleet posture | Curriculum stance |
|---|---|---|
| **Knowledge graphs (graph DB)** | None (`networkx`/`neo4j`/`kuzu`) | Build literacy on LMS SQL graph first; adopt graph DB only if query patterns outgrow relational edges |
| **OpenTelemetry** | None; LangSmith + custom scripts | Add OTel in one pilot repo — observability standard the industry expects beyond LangSmith |
| **LangGraph (second product)** | Only Travel-Plan-Permission is CENTRAL | Extend TPP pattern or add graph to Orchestrator routing — learn TPP first |
| **MCP clients in consumers** | Only Orchestrator has a server | Learn Orch MCP; add read-only client in Workflows for fleet introspection |
| **Hybrid / vector RAG at scale** | Only Manager-Database CENTRAL on pgvector | Learn MD stack; extend only if second domain needs semantic search |
| **Playwright (product-grade)** | Scattered USED | Centralize pattern in LMS or trip-planner — UI contract testing |
| **Office add-ins** | No CENTRAL surface | Deferred module — plan substrate (R4 mirror) before add-in work |
| **Prompt/version management** | Ad hoc per repo | New cross-fleet convention via Workflows + LMS prompt tables |
| **Cost governance** | LMS budget reservation only | Extend LMS `LLMClient` pattern fleet-wide |
| **Agent red-teaming** | None systematic | New eval strand in Pension-Data or Workflows |

**Judgment:** The owner already *includes* many elements. The gap is **explicit mental models and spaced verification**, not missing GitHub repos. Building new repos before completing the tool-literacy loop would widen the comprehension gap.

---

## 2. Curriculum: modules mapped to named repos

Each module teaches one 2026-era AI-tool-builder competency through a **concrete artifact already in the fleet**. Format: *what it teaches* · *prerequisite* · *estimated study hours* (reading + structured exercises; assessment time excluded).

### Tier 0 — Fleet vocabulary (prerequisite for all)

| Module | Repo | What it teaches | Prerequisite | Hours |
|---|---|---|---|---|
| **0A Contracts & identity** | Workflows + `00-INDEX` | `run-contract/v1`, entity ID collisions, why joins fail | None | 4 |
| **0B "What is a surface?"** | Any dossier | CLI vs API vs static app vs CI — how to read a repo without code | 0A | 2 |

### Tier 1 — Platform layer (learn, don't rebuild)

| Module | Repo | What it teaches | Prerequisite | Hours |
|---|---|---|---|---|
| **1 MCP & agent tools** | Orchestrator | MCP as capability surface; stdio JSON-RPC; owner-question loop; tool allowlists | 0B | 5 |
| **2 Fleet CI & agent belt** | Workflows | Consumer sync, deliberate-break gates, LangSmith fleet conformance | 0A | 6 |
| **3 LangSmith tracing** | Workflows + Manager-Database | Trace anatomy, fleet emitter, observability-driven debugging | 1 | 4 |
| **4 Structured extraction** | Inv-Man-Intake | Provider pattern, schema validation, regression evals | 0B | 5 |
| **5 Document parsing + eval** | Workflows (`stranske_pdf_extract`) | Parser packages, golden PDF evals, retrieval of fields not pages | 4 | 5 |
| **6 Entity resolution** | Counter_Risk + Pension-Data | Name registry, deterministic matching, alias forward lineage | 0A | 4 |
| **7 Data contracts & schema evolution** | Pension-Data | `run-contract/v1` emission, bitemporal facts, Alembic migrations | 0A, 6 | 6 |
| **8 ETL orchestration** | Manager-Database | Prefect flows, idempotent ingest, daily diff — workflow engines in production | 7 | 5 |
| **9 Diff & lineage** | Pension-Data + Inv-Man-Intake | Entity lineage models, audit packets, "what changed?" UX | 6, 7 | 4 |

### Tier 2 — Product patterns (extend carefully)

| Module | Repo | What it teaches | Prerequisite | Hours |
|---|---|---|---|---|
| **10 LangGraph state machines** | Travel-Plan-Permission | Graph nodes, deterministic orchestration, fallback paths without LLM | 1 | 4 |
| **11 RAG & hybrid retrieval** | Manager-Database | Embeddings, pgvector, chunking; retrieval evaluation (precision@k on held-out queries) | 4, 8 | 6 |
| **12 Agent evaluation & red-teaming** | Pension-Data | `eval_harness`, golden one-PDF pilot, adversarial cases | 5, 7 | 6 |
| **13 Prompt/version management** | learning-management-system | `Prompt` model, publication states, source linkage, drift scan | 4 | 4 |
| **14 Human-in-the-loop design** | Orchestrator + Workflows | Owner questions, approval cards, shadow dispatch, when agents must stop | 1, 2 | 4 |
| **15 Cost governance** | learning-management-system | Budget reservation, redaction, trace classification in `LLMClient` | 13 | 3 |
| **16 Security of agent tooling** | Orchestrator | Read-only MCP tools, subprocess isolation, quota caps, no credential bleed | 1 | 4 |
| **17 Static/offline delivery** | Portable-Alpha-Extension-Model | Pyodide bundle, portable zip, zero-egress demos | 0B | 4 |
| **18 Packaging & release** | Counter_Risk | PyInstaller pipeline, release guards, artifact manifests | 17 | 4 |
| **19 Browser automation** | learning-management-system | Playwright smoke, UI contract tests (opt-in gate) | 0B | 3 |
| **20 Knowledge graphs (conceptual)** | learning-management-system | `KnowledgeNode`/`KnowledgeEdge`, prerequisites, competency links — not Neo4j | 13 | 5 |

### Tier 3 — Field essentials to add (build or adopt)

| Module | Repo | What it teaches | Prerequisite | Hours |
|---|---|---|---|---|
| **21 OpenTelemetry** | Workflows (new script) | Distributed traces beyond LangSmith; correlate CI job → agent → API | 3 | 5 |
| **22 MCP client consumption** | Workflows (extend) | Call Orchestrator MCP from CI for fleet status; pattern for future connectors | 1, 2 | 4 |
| **23 Retrieval evaluation framework** | Manager-Database | Labeled query set, MRR/ndcg, chunk ablation — prove RAG changes help | 11 | 5 |
| **24 Data pipeline orchestration (alt)** | Manager-Database | Prefect vs Dagster decision record; stick with Prefect unless DAG complexity forces change | 8 | 2 |
| **25 Office add-ins / COM bridge** | Collab-Admin (future) | Excel/Word as surfaces; manifest + mirror substrate (R4) | 0B, R4 brief | 6 |
| **26 Graph DB adoption (conditional)** | Doc-Lineage (rename or repurpose) | When SQL edges fail: Kùzu/Neo4j for document dependency graphs | 20, 9 | 8 |

**Note on Doc-Lineage:** The repo name implies capability the code does not yet carry. Module 26 is the honest "build here or abandon the name" decision — not a hidden prerequisite.

**Ambition vs draft list:** The draft list (MCP, evals, extraction, hybrid search, graphs, LangGraph, OTel, Prefect, Playwright, Office, packaging) is covered above. Added 2026 essentials: red-teaming (12), prompt versioning (13), contracts/evolution (7), observability debugging (3, 21), cost governance (15), agent security (16), HITL (14), retrieval eval (23).

---

## 3. Tool-literacy loop design

### 3.1 Problem restatement

The loop answers: *"Your repo R has tools X, Y, Z in place. Do you know what they do, what feeds them, and what breaks if they're wrong?"* — assessed over time without reading code.

### 3.2 Components

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│ Repo inventory  │────▶│ Concept graph    │────▶│ LMS items           │
│ extractor       │     │ (curriculum ↔    │     │ (prompts +          │
│ (per repo,      │     │  repo artifacts) │     │  maintenance items) │
│  on change)     │     └──────────────────┘     └──────────┬──────────┘
└─────────────────┘                                         │
                                                            ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│ Mastery dashboard│◀───│ Capability gap   │◀───│ FSRS scheduler      │
│ (per repo)       │     │ analysis         │     │ (review queue)      │
└─────────────────┘     └──────────────────┘     └─────────────────────┘
```

#### A. Repo inventory extractor

**Output schema (per repo, versioned JSON):**

- `surfaces`: CLI entrypoints, HTTP routes, static apps, CI workflows (from `pyproject.toml` scripts, FastAPI routers, `.github/workflows/`)
- `libraries`: load-bearing deps with CENTRAL/USED classification (reuse coverage-matrix grep rules)
- `patterns`: named design patterns (e.g., "fleet LangSmith emitter", "Prefect flow", "golden eval")
- `contracts`: emitted/consumed schemas (`run-contract/v1`, etc.)
- `feeds_and_breaks`: for each pattern, upstream inputs and failure symptoms (from README + dossier, LLM-assisted draft, human-published)

**Refresh trigger:** git push to `main` or weekly cron; diff against prior inventory → `SourceReference` drift scan.

**First implementation home:** `Workflows/scripts/repo_inventory_extract.py` (fleet-wide, already has conformance tooling). Consumes shallow clones; writes `artifacts/inventories/<repo>.json`.

#### B. Concept graph

Maps curriculum modules (§2) to inventory keys via `KnowledgeNode` records:

- `imported_from`: `repo://Workflows#langsmith_fleet_conformance`
- `edge_type`: `prerequisite`, `supports-competency`
- `knowledge_type`: `conceptual` (architecture), `procedural` (operate/debug), `judgment` (when to use)

LMS already supports CSV/Markdown importers (`src/lms/importers/csv_graph.py`, `markdown.py`) and author UI at `/app/author/graph` (`graph_design.py`).

#### C. LMS item generation (source-grounded)

For each inventory entry *e* in repo *R*:

1. Create `SourceReference` with `stable_locator` = git path + commit SHA (`sources/models.py`; API `POST /source-references`).
2. Create `KnowledgeNode` (draft) titled *"R: {e.pattern_name}"*.
3. Generate `Prompt` or `MaintenanceItem`:
   - **Prompt** (graph strand): "Explain what {e} does in {R}, what feeds it, and one failure mode." Linked via `prompt_source_references`.
   - **MaintenanceItem** (job strand): quick-recall variant — "Name the three inputs to {e} in {R}."

Generation uses `LLMClient.complete` with structured output (`llm/client.py`), citations constrained to inventory + README excerpts. Items land in `draft` until owner approves via `/app/maintenance/review` or drafts UI (`drafts.py`).

**Question templates (fixed):**

1. What is it? (structure, not code)
2. What feeds it? (data/contracts upstream)
3. What breaks if it's wrong? (symptoms, blast radius)
4. How would you verify it? (test surface, trace, manifest)

#### D. Spaced assessment

On attempt completion (`evidence/api.py` → `record_score`):

- `evidence_to_fsrs_rating` maps performance to Again/Hard/Good/Easy (`scheduling/fsrs_adapter.py`)
- `ReviewCardState` persists stability/difficulty (`scheduling/models.py`)
- `ReviewQueueItem` surfaces due reviews (`GET /app/learner/reviews`, `review_queue_router`)

Remediation triggers on `high-confidence-error` or `repeated-incorrect-attempts` (`RemediationTrigger`).

#### E. Mastery dashboard per repo

`CapabilityTarget` per repo: title *"Tool literacy: {R}"*, linked `knowledge_node_ids` = all nodes with `imported_from` matching `repo://R#*`.

Pipeline:

1. `POST /capability/targets` → create target
2. `POST /capability/estimates` → score from evidence (`CapabilityEstimate`)
3. `POST /capability/gap` → `GapAnalysis` with `weak_node_ids`
4. UI: `/app/learner/capability` (`capability_gap.py`)

Mastery policy remains placeholder (`mastery/policy.py`) — acceptable for v1 if **capability estimates** drive the dashboard; replace mastery estimator when evidence accumulates.

### 3.3 What must exist in the LMS (current vs needed)

| Need | Exists today | Gap |
|---|---|---|
| Source grounding | `SourceReference`, drift scan | Add `repo-inventory` source_type |
| Concept map | `KnowledgeNode`, `KnowledgeEdge`, `/knowledge` API | Bulk import from inventory JSON |
| Assessments | `Prompt`, `MaintenanceItem`, `Attempt`, `EvidenceRecord` | Generator service + approval workflow |
| Spaced review | FSRS `ReviewCardState`, `/learners/{id}/review-queue` | Wire inventory nodes to scheduler on publish |
| Per-repo dashboard | `CapabilityTarget`, estimates, gap UI | Template target per repo; auto-link nodes |
| LLM generation guardrails | `LLMClient`, budgets, redaction | Prompt template for inventory Q&A |
| Courses/modules | **Deferred** (README §) | Not required — graph + capability targets suffice |

**Routes to use (already mounted in `main.py`):** `/source-references`, `/knowledge/*`, `/prompts`, `/capability/*`, `/learners/*/review-queue`, `/llm/*`, UI `/app/learner`, `/app/author/graph`, `/app/maintenance/*`.

### 3.4 First slice (build order)

1. **Inventory extractor for 3 repos** (Workflows, Orchestrator, Manager-Database) — deterministic JSON, no LLM.
2. **LMS import script** — JSON → `SourceReference` + draft `KnowledgeNode` rows.
3. **10 hand-authored prompts** for Workflows (prove question quality before LLM generation).
4. **One `CapabilityTarget`: "Tool literacy: Workflows"** — run attempt → review → gap analysis manually.
5. **Automate prompt generation** for remaining inventory entries; owner reviews in drafts UI.
6. **CI hook** — inventory diff on Workflows PR; stale `SourceReference` flags.

**Scope control:** Do not block on courses API, Neo4j, or fleet-wide inventory until slice 1–4 pass a deliberate-break test in LMS.

---

## 4. Sequence and time budget

**Owner assessment cap:** ≤30 min/week ≈ 3–4 review sessions × 7–8 min (FSRS-driven, not calendar cramming).

**Total curriculum:** ~98 study hours + ~26 weeks of assessments (one module ≈ one week of reviews after initial study block).

### Recommended sequence

| Phase | Weeks | Modules | Study hours | Weekly assessment |
|---|---|---|---|---|
| **Foundation** | 1–3 | 0A, 0B, 1, 2 | 17 | 2–3 items (new nodes) |
| **Observability & extraction** | 4–7 | 3, 4, 5, 13 | 18 | 3–4 items |
| **Data & trust** | 8–11 | 6, 7, 8, 9 | 19 | 3–4 items |
| **Agents & evaluation** | 12–15 | 10, 12, 14, 16 | 18 | 3 items |
| **Delivery surfaces** | 16–18 | 11, 17, 18, 19 | 17 | 2–3 items |
| **Graph & governance** | 19–21 | 15, 20, 23 | 14 | 2–3 items |
| **Fleet extensions** | 22–24 | 21, 22, 24 | 11 | 2 items |
| **Conditional** | 25+ | 25, 26 | 14 | as needed |

**Parallel rule:** Study hours are self-paced reading (dossiers, diagrams, 15-min "explain aloud" exercises). Only the review queue consumes the 30 min/week cap. If reviews backlog, pause new modules — spacing only works if retrieval stays current.

**Tool-literacy loop rollout:** Start in week 2 (module 1) with Workflows inventory; by week 4, assessments should reference *your* repo artifacts, not generic definitions.

---

## 5. Calibrated dissent and open questions

**What this gets right:** Treats the fleet as the textbook; connects LMS models that already exist; separates learn-first from build-next.

**Strongest risk:** LLM-generated questions may sound plausible while misstating repo behavior. Mitigation: every generated item requires draft → publish with `SourceReference` citation; wrong items become regression fixtures.

**Would change my mind if:** Owner time budget drops below 15 min/week — then collapse to maintenance items only (idea/recall) and defer graph prerequisites.

**OWNER_QUESTION default:** Should per-repo mastery targets be `personal` scope only, or `institutional` for future analyst onboarding? **Default:** `personal` until firm DB separation ships (LMS project plan §304–316). Proceed with personal scope.

---

*Artifact: Track C1. Method: coverage matrix + dossier index + LMS source inspection. No new dossier files written.*
