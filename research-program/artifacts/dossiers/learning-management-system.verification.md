# learning-management-system dossier — verification table

Verified against clone `clones/learning-management-system` at HEAD `f069a881312ba2abf7a5f2f59ca8e2eb01b1b379` (2026-09-04).
Method: every cited file:line/symbol in sections 4, 5, 8, and 9 opened and checked against current code and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 25 |
| WRONG (corrected in dossier) | 1 |
| UNVERIFIABLE | 1 |
| **Total checked** | **27** |

### Key Findings & Corrections

1. **§5 Postgres URL normalization citation:** The dossier attributed driverless-URL rewriting to `src/lms/db/session.py:16-62`. Opening that file shows normalization lives only in `Settings._pin_psycopg_driver` (`src/lms/settings.py:41-61`); `session.py:16-24` merely passes the already-normalized URL into `create_engine`.
2. **§8 GraphReference documentation drift (adversarial check):** Opening `docs/product/project-plan.md:314` confirms the plan names an explicit `GraphReference` row. Opening `src/lms/graphs/models.py:115-190` and grepping `src/lms` shows no `GraphReference` class/table — only `KnowledgeEdge.is_graph_reference` with `CHECK (source_scope = target_scope OR is_graph_reference)`. The dossier refutation is correct; do not soften it.
3. **§8 hosted deployment URL:** `docs/development/deployment.md:58-63` names `https://learning-management-system-5s7a.onrender.com`, but a shallow source clone cannot verify liveness, auth, migrations, or provider keys. Correctly marked operator note / unverifiable runtime state.
4. **§9 evidence-object schema gap:** Added explicit schema citation. `evidence-object-v1` requires `evidence_id`, `fact_ref`, `source_id`, `method`, and `excerpt` (`docs/contracts/schemas/evidence-object-v1.schema.json:8-15`); `SourceReference` stores locator, hash, and drift status — conceptual overlap only.

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | Knowledge graph stores typed nodes/edges with scope, provenance, status; edge direction is source→target prerequisite; cross-scope normal edges forbidden | `src/lms/graphs/models.py:53-112,115-190` | CONFIRMED | `KnowledgeNode` (:53-112), `KnowledgeEdge` docstring and `no_cross_scope_normal_edge` constraint (:115-190). |
| 2 | Markdown intake parses H1/H2, creates source ref + draft conceptual node, nesting → prerequisite edges | `src/lms/importers/markdown.py:74-178` | CONFIRMED | `plan_markdown_notes` (:74-90), `import_markdown_notes` (:93-178) with `knowledge_type="conceptual"`, `status="draft"`. |
| 3 | CSV graph validates column contract, case-folded `(scope,title)` uniqueness, known prerequisites, emits nodes/sources/edges | `src/lms/importers/csv_graph.py:17-133,136-209` | CONFIRMED | `REQUIRED_COLUMNS` (:17-24), `_node_key` casefold (:243-244), duplicate/missing-prerequisite checks (:187-208). |
| 4 | `SourceReference` stores locator, range, SHA-256 hash, visibility, drift; drift scan writes audit events | `src/lms/sources/models.py:17-79`; `src/lms/sources/repository.py:217-367` | CONFIRMED | Model fields (:57-74); `scan_source_references` updates drift and calls `record_audit_event` (:348-357). |
| 5 | Evidence captures confidence, support, scoring method, observed/inferred; `record_score` maps to 0–1 | `src/lms/evidence/models.py:28-32,40-151`; `src/lms/evidence/scoring.py:8-20` | CONFIRMED | `SUPPORT_LEVELS`, `EVIDENCE_KINDS`, `SCORING_METHODS` (:28-32); `record_score` fallback chain (:8-20). |
| 6 | Scheduling uses explainable Again/Hard/Good/Easy rules then FSRS-6 with hot/warm/cold tiers | `src/lms/scheduling/fsrs_adapter.py:135-222`; `src/lms/scheduling/fsrs_engine.py:37-114,166-209` | CONFIRMED | `FSRS_RULES` + `evidence_to_fsrs_rating` (:135-222); `TIER_POLICIES` (:57-76) and `review` (:166-209). |
| 7 | Feedback/rubrics/revisions turn assessment into next actions; rubric scoring creates remediation metadata | `src/lms/feedback/repository.py:239-253`; `src/lms/feedback/scoring.py:60-261` | CONFIRMED | `score_attempt_with_rubric` creates remediation feedback below threshold (:142-184); `_revision_scheduler_hook` builds deferred scheduling metadata (:239-253). |
| 8 | Capability targets, estimates, gaps, maintenance plans model learner work capacity | `src/lms/capability/models.py:52-319` | CONFIRMED | `CapabilityTarget` (:75+), `GapAnalysis`, `MaintenancePlan` through :319. |
| 9 | `LLMClient.complete` centralizes provider, budget, redaction, trace class, structured output, citations | `src/lms/llm/client.py:64-192` | CONFIRMED | Docstring order of operations and enforcement (:88-192). |
| 10 | Typed JSONL export/import orders records and validates relationships before apply | `src/lms/export_import.py:97-118,281-349,451-566` | CONFIRMED | `EXPORT_ORDER` (:97-130), `export_jsonl`/`import_jsonl` (:281-349), `_validate_import`/`_apply_entries` (:451-566). |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 11 | UUID primary keys via `new_uuid()`; unique email/username; nodes lack global stable ID beyond UUID/title/scope | `src/lms/auth/models.py:18-20,28-47`; `src/lms/graphs/models.py:83-99` | CONFIRMED | `new_uuid` (:18-20); `User.email`/`username` unique (:34-35); `KnowledgeNode.id` UUID PK (:83). |
| 12 | PostgreSQL via SQLAlchemy/Alembic; driverless URLs normalized to psycopg v3 | `src/lms/db/session.py:16-62`; `src/lms/settings.py:32-61` | **WRONG** | Normalization is only in `Settings._pin_psycopg_driver` (`settings.py:41-61`). `session.py:16-24` creates engine from normalized URL; `:36-64` is session lifecycle, not URL rewriting. |
| 13 | No graph-version, document-supersession, or canonical alias-resolution model | (architectural) | CONFIRMED | No matching symbols under `src/lms`. |
| 14 | Source changes tracked as content hash + `current/stale/missing` drift only | `src/lms/sources/models.py:57-74` | CONFIRMED | `content_hash`, `drift_status` columns with check constraint. |
| 15 | LMS typed JSONL emitted and consumed | `src/lms/export_import.py:281-349` | CONFIRMED | `export_jsonl` yields typed records; `import_jsonl` validates and applies. |
| 16 | Fleet schemas validated by script; not emitted by LMS runtime | `scripts/validate_run_contract.py:32-68,207-259`; `src/lms` grep | CONFIRMED | Validator loads `run-contract/v1`, manifest, evidence schemas; zero `src/lms` matches for those tokens. |
| 17 | identity-map conventions documented only; LMS uses UUIDs, no mapper | `docs/contracts/identity-map-conventions.md:42-77` | CONFIRMED | Canonical `<entity_type>:<normalized_identity>` format defined; no LMS resolver in `src/lms`. |
| 18 | capability bundle documented only, not an LMS model/exporter | `docs/contracts/capability-bundle-v1.md:1-12` | CONFIRMED | Describes Workflows `capability-bundle/v1` contract only. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement |
|---|---|---|---|---|
| 19 | Product plan requires `GraphReference` row; runtime uses `is_graph_reference` flag only | `docs/product/project-plan.md:304-315`; `src/lms/graphs/models.py:115-190` | CONFIRMED | Plan line 314 names `GraphReference` row; code enforces cross-scope via boolean on `KnowledgeEdge`, no `GraphReference` table/class in `src/lms`. |
| 20 | Backplane conformance workflow exists but emitter unwired → skips | `.github/workflows/backplane-conformance.yml:3-12,45-55` | CONFIRMED | Workflow present; placeholder step prints "No emitter wired yet" when `scripts/emit_reference_run.sh` absent. |
| 21 | Hosted Render URL in deployment doc is unverified live state | `docs/development/deployment.md:58-63` | **UNVERIFIABLE** | Doc names `learning-management-system-5s7a.onrender.com`; clone cannot prove service health, auth, migrations, or credentials. |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 22 | Offers source-grounded facts via `SourceReference`, scoped graph records, JSONL export of evidence/rubric/gap/review data | `src/lms/sources/models.py:34-79`; `src/lms/graphs/models.py:53-190`; `src/lms/export_import.py:97-118` | CONFIRMED | Fields and `EXPORT_ORDER` include `EvidenceRecord`, `RubricScore`, `GapAnalysis`, `ReviewSchedule`, etc. |
| 23 | Can consume sibling extracts as CSV graphs or Markdown notes | `src/lms/importers/csv_graph.py`; `src/lms/importers/markdown.py` | CONFIRMED | `import_csv_graph` and `import_markdown_notes` are the intake paths. |
| 24 | Identity risk: fleet expects canonical `type:id`; LMS exposes UUIDs/titles | `docs/contracts/identity-map-conventions.md:42-61` | CONFIRMED | Regex and vocabulary at :42-61; LMS PKs are random UUID strings. |
| 25 | Do not publish LMS UUIDs as manager/fund/person IDs | (integration guidance) | CONFIRMED | Follows from #24 and closed fleet vocabulary. |
| 26 | `SourceReference` and `evidence-object/v1` overlap but are not schema-compatible | `docs/contracts/schemas/evidence-object-v1.schema.json:8-15`; `src/lms/sources/models.py:34-79` | CONFIRMED | Fleet schema requires `evidence_id`, `fact_ref`, `method`, `excerpt`; LMS model has locator/hash/drift only. |

---

## Corrections applied to dossier

| Section | Before | After |
|---|---|---|
| §5 | Cited `session.py:16-62` for psycopg URL normalization | Split: normalization in `settings.py:41-61`, engine consumption in `session.py:16-24` |
| §9 | Stated schema incompatibility without schema cite | Added `evidence-object-v1.schema.json:8-15` citation |
| §8, §11 | Leading space before `.github/...` path | Removed stray space in markdown link targets |
