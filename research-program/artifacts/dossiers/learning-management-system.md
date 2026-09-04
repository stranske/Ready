# learning-management-system — dossier (2026-09-04)
## 1. Purpose in one paragraph

This is a database-backed learning prototype for one person now and, later, analyst training, company onboarding, and public education. It turns source material into a knowledge graph, prompts, learner attempts, feedback, and scheduled reviews rather than acting as a document repository (README.md:1-14; src/lms/main.py:104-129). Its operating constraint is an API-first FastAPI service with PostgreSQL, designed to keep personal and institutional data distinct through explicit scope fields and, for a firm, preferably separate databases (docs/product/project-plan.md:304-316; src/lms/settings.py:32-60). It tests a learning loop; it is not a validated analyst-training or office-wide governance platform.

## 2. Who uses it and how (surfaces)

| surface | entry point (file) | who uses it | status (working / partial / scaffold) with evidence |
| --- | --- | --- | --- |
| API | `src/lms/main.py:create_app` | integrations, authors, administrators | working: mounts authenticated routers for sources, graph, prompts, evidence, feedback, cases, capability, scheduling, LLM, and inspection (src/lms/main.py:104-127). |
| UI | `src/lms/ui/api.py`; `src/lms/ui/*.py` | learner, author, support/admin | working prototype: server-rendered `/app/*` routes and static assets, not a separate SPA (docs/development/web-prototype.md:1-22; src/lms/main.py:118-129). |
| CLI | `src/lms/__main__.py:main` | owner/operator | working: research validation, source drift scan, Markdown/CSV import, typed JSONL export/import, auth and demo utilities are registered (src/lms/__main__.py:34-260). |
| PWA/static HTML | `src/lms/ui/static/`; `docs/screenshots/` | mobile prototype users and reviewers | partial: manifest and worker are served, but the worker explicitly has no offline sync; snapshots are HTML structural artifacts (docs/development/web-prototype.md:24-34,44-73). |
| artifacts | JSONL from `src/lms/export_import.py` | backup/import and prospective sibling tools | working for LMS records: exports ordered typed rows with conservative redaction defaults and validates/imports them (src/lms/export_import.py:97-118,281-349). |

## 3. Structure map

```text
src/lms/             Application: FastAPI routers, SQLAlchemy models, services, UI, CLI.
  graphs|sources|... Domain packages for authored knowledge, provenance, learning activity and policy.
alembic/             Schema migrations.
tests/               Unit, API, end-to-end demo, UI snapshot, and deployment-contract tests.
docs/                Product decisions, contracts, deployment, research registry, and handoff records.
scripts/             Operational validators and automation helpers.
config/              Model, coverage, and source-of-truth configuration.
.github/             Consumer automation, synced from stranske/Workflows.
design-system/       Shared design material; skipped as boilerplate here.
```

## 4. Major code features you must understand to extend it

- Knowledge graph authoring stores typed nodes and directed edges with status, source, provenance and scope. An edge means “source requires target”; normal cross-scope edges are forbidden (src/lms/graphs/models.py:53-112,115-190). This orientation is a contract importers must preserve.
- Markdown intake parses H1/H2 sections, creates a source reference plus draft conceptual node for each, and turns nesting into draft prerequisite edges (`import_markdown_notes`, src/lms/importers/markdown.py:74-178). It is the most direct path from research notes to usable records.
- CSV graph intake validates a fixed column contract, case-folded `(scope, title)` uniqueness, known prerequisites, then emits nodes, source records, and edges (`import_csv_graph`, src/lms/importers/csv_graph.py:17-133,136-209). It is the spreadsheet-friendly authoring bridge.
- Source provenance records a stable locator, passage range, SHA-256 content hash, visibility, and drift status; drift scans write audit events (`SourceReference`, src/lms/sources/models.py:17-79; `scan_source_references`, src/lms/sources/repository.py:217-367). This is the closest existing evidence object for a research workflow.
- Attempts/evidence capture performance, confidence, support, scoring method and observed/inferred status; `record_score` normalizes these to 0–1 (src/lms/evidence/models.py:28-32,40-151; src/lms/evidence/scoring.py:8-20). Downstream mastery, feedback and review depend on it.
- Scheduling maps evidence to explainable Again/Hard/Good/Easy rules, then uses FSRS-6 state with hot/warm/cold retention policies (`evidence_to_fsrs_rating`, src/lms/scheduling/fsrs_adapter.py:135-222; `review`, src/lms/scheduling/fsrs_engine.py:37-114,166-209). It makes review timing inspectable rather than a hard-coded calendar.
- Feedback, rubrics, hints, model answers and revision requests turn assessment into a next action; rubric scoring can create remediation metadata (src/lms/feedback/repository.py:239-253; src/lms/feedback/scoring.py:60-261). This is the core teaching workflow, not merely scoring.
- Capability targets, estimates, gaps and maintenance plans model “what work can this learner do?” (src/lms/capability/models.py:52-319). They bridge to analyst-role learning but not job-performance validation.
- The LLM wrapper centralizes provider choice, budget reservation, PII redaction, trace classification, structured outputs and citation constraints (`LLMClient.complete`, src/lms/llm/client.py:64-192). It is a strong integration seam; individual feature code should not call a model directly.
- Typed JSONL export/import orders records and validates relationships before applying an import (src/lms/export_import.py:97-118,281-349,451-566). It is the current portable data interchange, not a fleet run envelope.

## 5. Data model, identifiers and contracts

Every persisted entity uses a random UUID string primary key from `new_uuid()`; user email and username are unique, but knowledge nodes have no global stable ID beyond UUID/title/scope (src/lms/auth/models.py:18-20,28-47; src/lms/graphs/models.py:83-99). PostgreSQL is the runtime persistence target, accessed through SQLAlchemy and Alembic; a driverless Render URL is normalized to psycopg v3 (src/lms/db/session.py:16-62; src/lms/settings.py:32-61). Records generally keep created/updated timestamps but there is no graph-version, document-supersession, or canonical alias-resolution model. Source content changes are tracked only as hashes plus `current/stale/missing` drift status (src/lms/sources/models.py:57-74).

| contract/object | emitted or consumed? | finding |
| --- | --- | --- |
| LMS typed JSONL | emitted and consumed | `export_jsonl` / `import_jsonl` serialize and apply LMS table records (src/lms/export_import.py:281-349). |
| `run-contract/v1`, `artifact-manifest/v1`, `evidence-object/v1` | validator consumes; LMS runtime does not emit | `scripts/validate_run_contract.py` validates schemas (lines 32-68,207-259); no `src/lms` reference to these names was found. |
| identity-map conventions | documented only for LMS data | the convention defines canonical `type:id` formats (docs/contracts/identity-map-conventions.md:42-77), while LMS uses UUIDs and has no mapper. |
| capability bundle | documented only | `docs/contracts/capability-bundle-v1.md:1-12` describes a Workflows artifact, not an LMS model or exporter. |

## 6. External inputs and dependencies

Inputs are Markdown, CSV graphs, source locators/content, learner answers, and optionally Anthropic completions. Libraries: FastAPI/Pydantic, SQLAlchemy/Alembic/psycopg, Mistune, pandas, FSRS and Argon2 (pyproject.toml:13-55). The real provider is Anthropic; without a key the default is deterministic fake output (src/lms/llm/providers.py:1-7,101-142,307-328). LangSmith is configuration/documentation for optional trace export, not a concrete SDK integration. Docker Compose and Render describe a FastAPI + Postgres installation; this UI requires the server and database (docs/development/deployment.md:1-20; docker-compose.yml:1-52).

## 7. Current state

The tested core is credible prototype software: `uv run pytest -q -m 'not slow'` passed 1,124 tests, skipped one deferred Playwright smoke, deselected eight slow tests, and reported 89.65% coverage. CI invokes lint, Black, mypy and pytest on Python 3.12/3.13 with an 80% threshold (Makefile:1-44; .github/workflows/ci.yml:1-32). Production use remains bounded by these gaps:

- Mastery is explicitly a deterministic FSRS-4.5-inspired placeholder, computed on demand rather than a validated estimator (src/lms/mastery/policy.py:11-31; src/lms/mastery/service.py:16-74).
- Browser accessibility/visual behavior is not tested in the required gate; Playwright is opt-in and skipped by default (docs/development/web-prototype.md:75-123).
- PWA offline sync and meaningful caching are deferred (docs/development/web-prototype.md:24-34).
- Runtime research registry APIs are deliberately deferred indefinitely; registry entities are YAML rather than database records (docs/product/research-domain-model.md:1-5).
- Firm-grade row-level security, institutional role separation, and the preferred separate-database boundary are future posture, not implemented controls (docs/product/project-plan.md:304-316).
- The live Anthropic gate has an entirely unchecked verification list, so unit tests do not establish a live provider deployment (docs/llm/PROVIDER_LIVE_VERIFICATION.md:58-98).
- Courses, modules, lessons and certification entities remain explicitly deferred (README.md:241).

## 8. Claims vs reality

- The product plan says cross-scope linkage requires an explicit `GraphReference` row (docs/product/project-plan.md:304-315). The runtime model instead has only `KnowledgeEdge.is_graph_reference`; there is no `GraphReference` class or table in `src/lms` (src/lms/graphs/models.py:115-190). The document overstates the implemented representation.
- The backplane workflow describes an emission/conformance gate ( .github/workflows/backplane-conformance.yml:3-12), but its repo-specific emitter is intentionally unwired and prints “No emitter wired yet,” so it skips (lines 45-55). This repo does not currently produce fleet run artifacts.
- Deployment documentation labels a specific hosted service as current (docs/development/deployment.md:58-63). A source-only shallow clone cannot prove that service is live, authenticated, migrated, or using real LLM credentials; treat it as an operator note, not verified current state.

## 9. Interoperability hooks (for the fleet program)

The useful offers are source-grounded learning facts: `SourceReference` carries locator, page/line range, content hash and visibility; nodes/edges carry scope and provenance; evidence, rubric, capability-gap and review records export through LMS JSONL (src/lms/sources/models.py:34-79; src/lms/graphs/models.py:53-190; src/lms/export_import.py:97-118). It can consume sibling document extracts as CSV graphs or Markdown notes.

The hard interoperability risk is identity: siblings expect canonical `entity_type:normalized_identity` references (docs/contracts/identity-map-conventions.md:42-61), whereas this app exposes UUIDs and free-text titles. Do not publish LMS UUIDs as manager/fund/person IDs. Add a canonical entity reference before joining investment-office entities. `SourceReference` provenance and fleet `evidence-object/v1` overlap but are not schema-compatible.

## 10. Reuse candidates

- Provenance hash/drift scan: `src/lms/sources/repository.py`.
- Markdown-to-graph importer: `src/lms/importers/markdown.py`.
- CSV graph validator/importer: `src/lms/importers/csv_graph.py`.
- Redaction/budget/provider wrapper: `src/lms/llm/client.py` and `redaction.py`.
- Retention-tier FSRS adapter: `src/lms/scheduling/fsrs_engine.py` and `fsrs_adapter.py`.
- Dependency-aware JSONL export/import: `src/lms/export_import.py`.

## 11. Proposed direction (evidence-based)

- Finish scaffolded work: replace the mastery placeholder only after collecting and evaluating evidence, keeping its estimator version visible (src/lms/mastery/policy.py:11-31).
- Finish scaffolded work: decide whether to activate real-browser accessibility testing; the present gate cannot assess it (docs/development/web-prototype.md:59-60,75-108).
- Finish scaffolded work: wire a deterministic reference emitter if this repo is to participate in the fleet backplane ( .github/workflows/backplane-conformance.yml:45-55).
- Finish scaffolded work: complete and record the live-provider gate before treating study-coach output as a production capability (docs/llm/PROVIDER_LIVE_VERIFICATION.md:58-98).
- New capability: introduce a canonical external-entity field and identity resolver adapter; keep UUIDs as local keys and emit fleet IDs only after resolution (docs/contracts/identity-map-conventions.md:94-130).
- New capability: define a genuine evidence-object adapter from `SourceReference` plus an attributed fact, rather than relabeling LMS records.
- New capability: implement firm deployment authorization and RLS only together with the planned database separation, not as superficial UI roles (docs/product/project-plan.md:304-316).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- It turns sources into practice and review; it is not a finished corporate LMS.
- It can support analyst-training design, not prove analyst competence or investment performance.
- Its strength is traceability from source passage to learner response.
- It needs a server and PostgreSQL; it is not an offline desktop tool.
- Before integration, agree on shared entity identifiers and data-boundary rules.
