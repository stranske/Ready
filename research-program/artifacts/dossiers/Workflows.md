# Workflows — dossier (2026-09-04)

## 1. Purpose in one paragraph

The Workflows repository provides central automation, continuous integration (CI/CD), and multi-agent orchestration for an investment office fleet of 15 registered first-party consumer repositories. It eliminates configuration divergence by serving as the source of truth for reusable GitHub Actions workflows, downstream templates, and cross-repo data exchange contracts. Operating under strict serverless constraints, the repository maintains zero persistent services or databases, executing headless via Python (3.12+) and Node.js within GitHub Actions and developer shells with cryptographically verified artifact manifests.

## 2. Who uses it and how (surfaces)

| Surface | Entry Point | Who Uses It | Status with Evidence |
| :--- | :--- | :--- | :--- |
| **GitHub Actions CI** | [pr-00-gate.yml](clones/Workflows/.github/workflows/pr-00-gate.yml) | Fleet repos, developers, bots | **Working**: Sole required merge check enforcing linting, tests, seals ([README.md:108](clones/Workflows/README.md#L108)). |
| **Agent Keepalive Engine** | [keepalive_loop.js](clones/Workflows/.github/scripts/keepalive_loop.js) | Coding agents (Codex, Claude) | **Working**: Event-driven loop injecting test feedback into prompts ([README.md:71](clones/Workflows/README.md#L71), [README.md:83](clones/Workflows/README.md#L83)). |
| **Consumer Sync Engine** | [maint-68-sync-consumer-repos.yml](clones/Workflows/.github/workflows/maint-68-sync-consumer-repos.yml) | Fleet maintainers | **Working**: Compiles [sync-manifest.yml](clones/Workflows/.github/sync-manifest.yml) to push delivery PRs ([README.md:16](clones/Workflows/README.md#L16)). |
| **Fleet Review CLI** | [repo_review_coordinator.py](clones/Workflows/scripts/repo_review_coordinator.py) | Human repo owners | **Working**: Coordinates multi-agent audits into decision packets ([REPO_REVIEW_PROCESS.md:55](clones/Workflows/docs/ops/REPO_REVIEW_PROCESS.md#L55)). |
| **Backplane Validator CLI** | [validate_run_contract.py](clones/Workflows/scripts/validate_run_contract.py) | Research tools | **Partial**: Validator works; only 1 of 6 producer repos is conformant ([backplane_participants.json:32](clones/Workflows/config/backplane_participants.json#L32)). |
| **Metrics Dashboards** | [metrics_dashboard_generator.py](clones/Workflows/scripts/metrics_dashboard_generator.py) | Investment leadership | **Partial**: Generator runs; host export is paused ([langsmith_fleet_registry.json:19](clones/Workflows/config/langsmith_fleet_registry.json#L19)). |
| **App Baseline Kit (API)** | [app-baseline-kit](clones/Workflows/packages/app-baseline-kit) | Quantitative models | **Working**: Golden metrics and snapshots in Trend_Model_Project ([README.md:24-26](clones/Workflows/packages/app-baseline-kit/README.md#L24-L26)). |
| **PDF Extraction (API)** | [stranske_pdf_extract](clones/Workflows/packages/stranske_pdf_extract) | Ingestion tools | **Scaffold**: Protocol exists; zero fleet repos migrated ([DESIGN.md:3](clones/Workflows/packages/stranske_pdf_extract/docs/DESIGN.md#L3)). |

## 3. Structure map

```text
stranske/Workflows/
├── .github/          # Reusable workflows, composite actions, Node.js keepalive scripts
├── config/           # Fleet registries (backplane participants, LangSmith, review profiles)
├── docs/             # Contracts, JSON schemas, integration guides, operator playbooks
├── packages/         # Subpackages (app-baseline-kit, stranske_pdf_extract)
├── scripts/          # Manifest compiler, repo review engine, validators, LangChain tools
├── src/              # Metric parsers (ndjson_parser.py) and CI autofix test fixtures
├── templates/        # Canonical consumer templates synced to downstream repositories
├── tests/            # 327 Python test files and 92 Node.js test suites
└── tools/            # Model evaluators, LLM client providers, and CI triage utilities
```
*(Note: Downstream repositories vendor standard CI files synced from [templates/consumer-repo/](clones/Workflows/templates/consumer-repo) via [.github/sync-manifest.yml](clones/Workflows/.github/sync-manifest.yml).)*

## 4. Major code features you must understand to extend it

- **PR Gate Orchestrator ([pr-00-gate.yml](clones/Workflows/.github/workflows/pr-00-gate.yml) + [detect-changes.js](clones/Workflows/.github/scripts/detect-changes.js))**: Consumes diffs and [path-classification.yml](clones/Workflows/.github/path-classification.yml) to produce dynamic CI job toggles and unified commit status; skips heavy suites for docs while strictly enforcing delivery seals on code.
- **Consumer Sync Compiler ([sync_manifest_compiler.py](clones/Workflows/scripts/sync_manifest_compiler.py))**: Consumes [sync-manifest.yml](clones/Workflows/.github/sync-manifest.yml) and templates to emit per-repo file sync plans; eliminates configuration drift across 15 registered consumer repositories.
- **Event-Driven Keepalive Loop ([keepalive_loop.js](clones/Workflows/.github/scripts/keepalive_loop.js) + [reusable-16-agents.yml](clones/Workflows/.github/workflows/reusable-16-agents.yml))**: Consumes CI failure events and logs to produce structured prompt appendices and agent dispatches; drives autonomous iterative code repairs until tests pass.
- **Capability Bundle Selector ([capability_bundle.js](clones/Workflows/.github/scripts/capability_bundle.js) + [keepalive_prompt_composer.js](clones/Workflows/.github/scripts/keepalive_prompt_composer.js))**: Consumes repo context and [capability-bundle-v1.schema.json](clones/Workflows/docs/contracts/schemas/capability-bundle-v1.schema.json) to emit prompt instructions; injects specialized playbooks without letting agents modify their own constraints.
- **Dual-Model Verifier Gate ([reusable-agents-verifier.yml](clones/Workflows/.github/workflows/reusable-agents-verifier.yml) + [pr_verifier.py](clones/Workflows/scripts/langchain/pr_verifier.py))**: Consumes merged diffs and acceptance criteria to produce verdicts requiring unanimous agreement between two LLM judges in compare mode (documented defaults: gpt-5.6-terra + claude-sonnet-5 per [README.md:90](clones/Workflows/README.md#L90)); prevents regressions.
- **Backplane Conformance Validator ([validate_run_contract.py](clones/Workflows/scripts/validate_run_contract.py))**: Consumes run envelopes (`run.json`) and manifests (`manifest.json`) against backplane schemas; produces verification reports enforcing SHA-256 integrity across research tools.
- **Fleet Review Consensus Engine ([repo_review_coordinator.py](clones/Workflows/scripts/repo_review_coordinator.py) + [repo_review_evaluator.py](clones/Workflows/scripts/repo_review_evaluator.py))**: Consumes multi-agent audits and human input ([repo_review_feedback.json](clones/Workflows/config/repo_review_feedback.json)) to produce decision packets and staged queues; maintains architectural alignment under human governance.
- **Document Provenance Ladder ([contract.py](clones/Workflows/packages/stranske_pdf_extract/src/stranske_pdf_extract/contract.py))**: Consumes PDF byte streams to produce content-hashed locators (`evidence:<sha256[:16]>`) and bounding-box locators; links extracted financial metrics directly to source coordinates.

## 5. Data model, identifiers and contracts

### Identifiers and Persistence

- **Identifiers**: Entities follow `<entity_type>:<normalized_identity>` ([identity-map-conventions.md:44-62](clones/Workflows/docs/contracts/identity-map-conventions.md#L44-L62)) across closed types: `manager`, `fund`, `pension`, `provider`, `person`, `strategy`. Artifacts use SHA-256 hashes (`^[a-f0-9]{64}$`, [artifact-manifest-v1.schema.json:73](clones/Workflows/docs/contracts/schemas/artifact-manifest-v1.schema.json#L73)). Evidence objects use locator hashes (`evidence:<sha256[:16]>`, [contract.py:96](clones/Workflows/packages/stranske_pdf_extract/src/stranske_pdf_extract/contract.py#L96)). Capability bundles use `capability_id` plus a SHA-256 payload hash ([capability-bundle-v1.md:5](clones/Workflows/docs/contracts/capability-bundle-v1.md#L5)).
- **Persistence**: Zero database infrastructure. State is stored in version-controlled Git files (JSON, YAML), append-only NDJSON logs, and GitHub Actions artifacts.
- **Versioning**: Explicit `schema_version` strings (`run-contract/v1`). Downstream sync deliveries on `sync/workflows-delivery` require exact-head commit SHA verification before merging.

### Shipped Contracts Status

- **run-contract/v1** ([run-contract-v1.md](clones/Workflows/docs/contracts/run-contract-v1.md)): **Consumed & Validated** by [validate_run_contract.py:207](clones/Workflows/scripts/validate_run_contract.py#L207); Workflows is excluded as emitter ([backplane_participants.json:250](clones/Workflows/config/backplane_participants.json#L250)); emitted by Pension-Data.
- **evidence-object/v1** ([evidence-object-v1.schema.json](clones/Workflows/docs/contracts/schemas/evidence-object-v1.schema.json)): **Validated / Documented Only** by [validate_run_contract.py:130-179](clones/Workflows/scripts/validate_run_contract.py#L130-L179) (consumer ingest path) and schema self-test at [:403](clones/Workflows/scripts/validate_run_contract.py#L403); verifier does not yet project outputs here ([pr-verification-evidence-plan.md:50](clones/Workflows/docs/orchestrator/pr-verification-evidence-plan.md#L50)).
- **identity-map-conventions.md** ([identity-map-conventions.md](clones/Workflows/docs/contracts/identity-map-conventions.md)): **Documented Only**. Regex validated; resolution delegated to Manager-Database and Pension-Data.
- **artifact-manifest/v1** ([artifact-manifest-v1.schema.json](clones/Workflows/docs/contracts/schemas/artifact-manifest-v1.schema.json)): **Consumed & Validated** by [validate_run_contract.py:228](clones/Workflows/scripts/validate_run_contract.py#L228); emitted by Pension-Data.
- **capability-bundle/v1** ([capability-bundle-v1.md](clones/Workflows/docs/contracts/capability-bundle-v1.md)): **Emitted & Consumed** by [capability_bundle.js:6](clones/Workflows/.github/scripts/capability_bundle.js#L6) and [keepalive_prompt_composer.js:7](clones/Workflows/.github/scripts/keepalive_prompt_composer.js#L7).
- **langsmith-fleet/v1** ([langsmith-fleet-v1.md](clones/Workflows/docs/contracts/langsmith-fleet-v1.md)): **Consumed & Validated** by [langsmith_fleet.py:23](clones/Workflows/scripts/langsmith_fleet.py#L23); Workflows host export paused ([langsmith_fleet_registry.json:19](clones/Workflows/config/langsmith_fleet_registry.json#L19)).
- **agent-runner-output.md** ([agent-runner-output.md](clones/Workflows/docs/contracts/agent-runner-output.md)): **Emitted & Consumed** across runner workflows ([reusable-codex-run.yml](clones/Workflows/.github/workflows/reusable-codex-run.yml), [reusable-claude-run.yml](clones/Workflows/.github/workflows/reusable-claude-run.yml)).

## 6. External inputs and dependencies

- **Data Sources**: GitHub REST/GraphQL APIs via [token_load_balancer.js](clones/Workflows/.github/scripts/token_load_balancer.js); Git trees from 15 consumer repos ([maint-68-sync-consumer-repos.yml](clones/Workflows/.github/workflows/maint-68-sync-consumer-repos.yml)); local PDF byte streams for extraction testing ([stranske_pdf_extract](clones/Workflows/packages/stranske_pdf_extract)).
- **LLM Frameworks**: Router ([llm_provider.py](clones/Workflows/tools/llm_provider.py)) supporting OpenAI, Anthropic, Gemini, GitHub Models. LangChain (`langchain>=1.3.4` in [pyproject.toml:61](clones/Workflows/pyproject.toml#L61)), FAISS (`faiss-cpu`), LangSmith tracing ([langsmith_fleet.py](clones/Workflows/scripts/langsmith_fleet.py)), and agent CLI runners.
- **Key Libraries & Runtime**: `pydantic>=2.13.4`, `jsonschema>=4.26.0`, `PyYAML>=6.0.0`, `pdfplumber`, `pypdf`, optional `docling`. Serverless and local-first: zero web daemons or databases; runs on Python 3.12+ and Node.js 20+.

## 7. Current state

- **Test and CI Posture**: Gated by [pr-00-gate.yml](clones/Workflows/.github/workflows/pr-00-gate.yml), aggregating `python-ci`, `docs-guard`, `github-scripts-tests`, `packages-pdf-extract`, and delivery seals. Enforces 327 Python test files in `tests/` and 92 JavaScript test suites in `.github/scripts/__tests__/`. Developers run fast checks via [dev_check.sh](clones/Workflows/scripts/dev_check.sh).
- **Production-Usable vs Prototype**:
  - *Production-Usable*: Reusable CI workflows, consumer sync (`maint-68`/`maint-71`), keepalive loop, agent runners, baseline harness (`app-baseline-kit`), backplane validator ([validate_run_contract.py](clones/Workflows/scripts/validate_run_contract.py)).
  - *Prototype / Scaffold*: [stranske_pdf_extract](clones/Workflows/packages/stranske_pdf_extract) is a scaffold deliverable ([DESIGN.md:3](clones/Workflows/packages/stranske_pdf_extract/docs/DESIGN.md#L3)); backplane adoption is partial with 1 of 6 producer repos conformant ([backplane_participants.json:32](clones/Workflows/config/backplane_participants.json#L32)); Workflows host LangSmith export paused ([langsmith_fleet_registry.json:19](clones/Workflows/config/langsmith_fleet_registry.json#L19)); model profile trials run read-only ([README.md:111-113](clones/Workflows/README.md#L111-L113)).
- **Consequential Known Gaps**:
  1. Detect-job output verification un-wired in Gate CI ([pr-verification-evidence-plan.md:48](clones/Workflows/docs/orchestrator/pr-verification-evidence-plan.md#L48)).
  2. Verifier outputs not projected into `evidence-object/v1` format ([pr-verification-evidence-plan.md:50](clones/Workflows/docs/orchestrator/pr-verification-evidence-plan.md#L50)).
  3. Verifier remediation is advisory-only without closed-loop dispatch ([pr-verification-evidence-plan.md:65](clones/Workflows/docs/orchestrator/pr-verification-evidence-plan.md#L65), [README.md:73](clones/Workflows/README.md#L73)).
  4. Workflows host LangSmith artifact export paused since 2026-06-13 ([langsmith_fleet_registry.json:19-24](clones/Workflows/config/langsmith_fleet_registry.json#L19-L24)).
  5. Backplane blockers in Counter_Risk (missing pandas), Manager-Database, and Inv-Man-Intake ([backplane_participants.json:110,168,194](clones/Workflows/config/backplane_participants.json#L110)).
  6. Agent runner spec marks Gemini as future despite active workflow ([agent-runner-output.md:23](clones/Workflows/docs/contracts/agent-runner-output.md#L23)).

## 8. Claims vs reality

- **Research Backplane Adoption**: Program docs still describe P0 landing with no participant emission yet ([research-backplane-contract.md:6-8](clones/Workflows/docs/contracts/research-backplane-contract.md#L6-L8), [run-contract-v1.md:15-17](clones/Workflows/docs/contracts/run-contract-v1.md#L15-L17)). *Reality*: Pension-Data is conformant; five other producer repos remain `planned` with `issue_deferred` entries (three cite explicit operational blockers; two defer until repo-local issues are selected) ([backplane_participants.json:7-233](clones/Workflows/config/backplane_participants.json#L7-L233)).
- **Unified PDF Extraction**: README claims `stranske_pdf_extract` replaces four diverging implementations ([packages/stranske_pdf_extract README:3](clones/Workflows/packages/stranske_pdf_extract/README.md#L3)). *Reality*: Remains scaffold deliverable 5 ([DESIGN.md:3,10](clones/Workflows/packages/stranske_pdf_extract/docs/DESIGN.md#L3-L10)); zero fleet repos have migrated.
- **Closed-Loop Verification**: README depicts automated issue-to-merge with verifier follow-up ([README.md:45-72](clones/Workflows/README.md#L45-L72)). *Reality*: Verifier remediation requires label-triggered follow-up (`verify:create-issue` / `verify:create-new-pr`); automatic follow-up issue creation is explicitly a non-goal ([README.md:73](clones/Workflows/README.md#L73), [pr-verification-evidence-plan.md:65](clones/Workflows/docs/orchestrator/pr-verification-evidence-plan.md#L65)).
- **Observability Dogfooding**: Docs cite live verifier and pipeline metrics ([README.md:92](clones/Workflows/README.md#L92)). *Reality*: Workflows' own `langsmith-fleet.ndjson` artifact export is paused since 2026-06-13 to stop zero-signal churn (cloud LangSmith tracing remains active per registry note) ([langsmith_fleet_registry.json:19-24](clones/Workflows/config/langsmith_fleet_registry.json#L19-L24)).
- **Trend Analysis Code**: Directory implies quantitative modeling code. *Reality*: Files are intentionally broken CI autofix test fixtures excluded from coverage ([pyproject.toml:201](clones/Workflows/pyproject.toml#L201), [src/trend_analysis README:1-12](clones/Workflows/src/trend_analysis/README.md#L1-L12)).

## 9. Interoperability hooks (for the fleet program)

- **Offers**: Standard schemas (`run-contract/v1`, `evidence-object/v1`, `artifact-manifest/v1` in [docs/contracts/schemas/](clones/Workflows/docs/contracts/schemas)); offline conformance CLI ([validate_run_contract.py](clones/Workflows/scripts/validate_run_contract.py)); regression testing kit ([app-baseline-kit](clones/Workflows/packages/app-baseline-kit)); shared PDF extraction contract ([contract.py](clones/Workflows/packages/stranske_pdf_extract/src/stranske_pdf_extract/contract.py)); staged issue backlogs ([repo_review_evaluator.py](clones/Workflows/scripts/repo_review_evaluator.py)).
- **Consumes**: Replayable run envelopes (`run.json`), manifests (`manifest.json`), LangSmith trace streams (`langsmith-fleet.ndjson`), and Git trees from downstream repositories.
- **Collisions & ID Incompatibilities**: Backplane requires `<entity_type>:<normalized_identity>` ([identity-map-conventions.md:44](clones/Workflows/docs/contracts/identity-map-conventions.md#L44)). Fleet docs note sibling repos may still use raw CSV column names, unaliased slugs, or internal integer/UUID IDs until they adopt the conventions; evidence locator formats also differ (`evidence:<hash>` vs. `doc#page=n` vs. bounding-box tuples) — specifics require per-repo verification outside this clone.

## 10. Reuse candidates

- **API Snapshot Regression Engine** ([snapshot.py](clones/Workflows/packages/app-baseline-kit/baseline_kit/snapshot.py)): Order-stable, redacted JSON response normalizer for pytest snapshot testing without numpy/pandas.
- **Directional Invariant Evaluator** ([directional.py](clones/Workflows/packages/app-baseline-kit/baseline_kit/directional.py)): Metamorphic comparator asserting quantitative directional invariants (control vs variant).
- **Attributable Document Provenance Model** ([contract.py](clones/Workflows/packages/stranske_pdf_extract/src/stranske_pdf_extract/contract.py)): Dataclasses for bounding-box locators (`BBox`) and content-hashed evidence links (`EvidenceRef`).
- **Tiered Fallback Orchestrator** ([orchestration.py](clones/Workflows/packages/stranske_pdf_extract/src/stranske_pdf_extract/orchestration.py)): Tiered fallback ladder handling graceful degradation across sequential extraction providers.
- **Multi-Repo Manifest Compiler** ([sync_manifest_compiler.py](clones/Workflows/scripts/sync_manifest_compiler.py)): Deterministic multi-repo configuration compiler parsing declarative manifests and detecting drift.
- **Analytical Run Envelope Validator** ([validate_run_contract.py](clones/Workflows/scripts/validate_run_contract.py)): Standalone CLI validating analytical JSON outputs, schema compliance, and SHA-256 checksums.
- **GitHub Token Load Balancer** ([token_load_balancer.js](clones/Workflows/.github/scripts/token_load_balancer.js)): Production Node.js utility distributing GitHub API calls across tokens with rate-limit backoff.
- **Path-Aware CI Change Classifier** ([detect-changes.js](clones/Workflows/.github/scripts/detect-changes.js)): High-speed git diff classifier dynamically toggling CI build matrices based on modified paths.

## 11. Proposed direction (evidence-based)

### Finish What Is Scaffolded

- Complete `stranske_pdf_extract` migration in `Manager-Database` and `Inv-Man-Intake` ([DESIGN.md:3](clones/Workflows/packages/stranske_pdf_extract/docs/DESIGN.md#L3)).
- Unblock backplane producers in `Counter_Risk`, `Manager-Database`, and `Inv-Man-Intake` ([backplane_participants.json:110,168,194](clones/Workflows/config/backplane_participants.json#L110)).
- Resume host LangSmith artifact export in [langsmith_fleet_registry.json:19-24](clones/Workflows/config/langsmith_fleet_registry.json#L19-L24) before review deadline.
- Wire detect-job verification into [pr-00-gate.yml](clones/Workflows/.github/workflows/pr-00-gate.yml) ([pr-verification-evidence-plan.md:48](clones/Workflows/docs/orchestrator/pr-verification-evidence-plan.md#L48)).

### New Capabilities

- Close verifier loop with automated remediation dispatches emitting `evidence-object/v1` ([pr-verification-evidence-plan.md:50-52](clones/Workflows/docs/orchestrator/pr-verification-evidence-plan.md#L50-L52)).
- Upgrade [agents-model-profile-trial.yml](clones/Workflows/.github/workflows/agents-model-profile-trial.yml) from quarantine telemetry to automated model scoring ([README.md:111-113](clones/Workflows/README.md#L111-L113)).
- Provide entity resolution client in `packages/` to query `Manager-Database` and `Pension-Data` ([identity-map-conventions.md:44](clones/Workflows/docs/contracts/identity-map-conventions.md#L44)).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- **Firm-Wide Software Hub**: Serves as the master management and quality control center for the 13 software applications across the investment office.
- **Autonomous Coding Agents**: Deploys AI agents to diagnose bug reports, write code updates, and re-run test suites until requirements are satisfied.
- **Universal Safety Guardrails**: Enforces centralized automated checks on every code update, protecting financial models and mathematical calculations from accidental breakage.
- **Cross-Tool Research Standards**: Establishes common data rules allowing portfolio models, pension databases, and risk analytics to exchange research and cite document sources.
- **Mature Operations, Emerging Integration**: Testing and maintenance pipelines operate reliably daily, while deeper cross-tool analytical data sharing is actively rolling out across models.

Verified 2026-09-04T18:06:00Z by composer: 38 claims checked, 12 corrected, 1 unverifiable
