# Orchestrator — dossier (2026-09-04)

## 1. Purpose in one paragraph
The Orchestrator coordinates subscription-tier command-line coding agents (Claude Code, OpenAI Codex, Cursor, Gemini via Antigravity, Mistral Vibe) across roughly eleven GitHub repositories. It deterministically routes tasks based on empirical performance and costs while strictly managing expiring subscription quotas (rolling 5-hour bursts and weekly drain limits). Designed for an investment office technical owner on a single macOS workstation, the tool runs locally without external database servers, containers, or background daemons. To prevent SQLite lockups under cloud storage, canonical code is separated from local runtime state, and human decisions use non-blocking, auto-expiring prompts that prevent fleet stalls (`README.md:3-10, 20-33`, `ARCHITECTURE.md:14-43`, `PLANNING.md:9-18`).

## 2. Who uses it and how (surfaces)
| Surface | Entry Point | Who Uses It | Status (Evidence) |
|---|---|---|---|
| CLI (Fleet Tick) | `orchestrate.sh` / `src/tick.py` | Automated macOS launchd daemon (`com.stranske.orchestrator`, hourly at :40) and human operators | Working; shadow execution by default. Live dispatch is gated behind `ORCH_DISPATCH_LANE=1` since 2026-09-03 after 14 dispatches produced 9 abandoned runs and 0 durable outcomes (`README.md:34-39`, `orchestrate.sh:1-120`). |
| CLI (Verification Suite) | `src/verify.py` | Developers, coding agents prior to commit, and CI runner (`pr-00-gate.yml`) | Working; strictly validates test collection equality against `.verify-floor.json` (631 collected/passed, bounded skip ceilings, 94 selftest modules, 5 gates; `src/verify.py:1-54`). |
| CLI (Observability) | `src/observability_dashboard.py` / `src/periodic_report.py` | Human operator assessing fleet health, seat quotas, and learner convergence | Working; generates terminal scorecards and JSON dumps across productivity, quality, and live capacity (`src/observability_dashboard.py:1-8, 2225-2237`). |
| API / Stdio (MCP Server) | `src/mcp_server.py` | Local Claude Code or desktop agent sessions via Model Context Protocol | Working; standard-library stdio JSON-RPC server offering 10 tools for capacity status, route weights, capability advice, and question answering (`src/mcp_server.py:1-219`). |
| Artifacts (Route Export) | `src/route_weights_export.py` | Sibling GitHub Actions workflows (Keepalive, Autofix) via `config/route-weights.json` on branch `exports/route-weights` | Working / Partial; generates local routing tables (`$ORCH_STATE_DIR/route-weights-export.json`) and handoff heartbeats, but remote git branch publishing is gated behind `ORCH_ROUTE_WEIGHTS_PUBLISH=1` (`docs/ROUTE_WEIGHTS_EXPORT.md:1-40`). |
| UI / Web (Presentation) | `design-system/ds_streamlit.py` | None in this repository | Scaffold / Inactive; synced boilerplate from `stranske/Workflows` template; Orchestrator contains no running Streamlit app or web service (`design-system/README.md:49-51`). |
| Excel / Spreadsheets | None | None | Absent; no Excel or spreadsheet generation or parsing libraries exist in `src/`. |

## 3. Structure map
```
.
├── orchestrate.sh             # Main entrypoint script managing execution loops, mirror sync, and cadence jobs
├── pyproject.toml             # Tool configurations (pytest, coverage, mypy, black) for a non-package repository
├── .verify-floor.json         # Strict test count floor (631 collected/passed) and skip ceiling definitions
├── src/                       # Core application logic containing 107 flat, unencapsulated Python modules
│   ├── capacity.py            # Multi-window subscription quota tracking and seat dispatchability gates
│   ├── router.py              # Learned agent selection engine balancing performance, costs, and exploration
│   ├── dispatcher.py          # Process-isolated worktree runner and agent execution harness
│   ├── feedback.py            # SQLite learning store recording runs, attempts, costs, and durable outcomes
│   ├── capabilities.py        # Authoritative capability registry, liveness tracking, and usage accounting
│   ├── capability_admission.py# Prospective 9-point quality gate for adding and reviving capabilities
│   ├── exp_abcd.py            # Multi-agent A/B/C/D duel runner and cross-evaluator matrix
│   ├── repo_knowledge.py      # Fleet repository playbooks, invariant gotchas, and bundle exports
│   ├── mcp_server.py          # Zero-dependency stdio Model Context Protocol server
│   └── verify.py              # Subprocess-aware test orchestrator enforcing floor equality
├── tests/                     # Test suite containing 45+ pytest files and rail exercise fixtures
│   └── rail_exercises/        # Disposable fixture environments for deterministic rail contract testing
├── docs/                      # Technical manuals, CI system baselines, and cross-repo protocol specs
│   └── contracts/             # Schemas and specifications for run envelopes, identity maps, and capability bundles
├── config/                    # Fleet configuration files including expected CI checks
├── prompts/                   # Prompt templates for specialized agent roles (triage, decomposer, prompt agent)
├── scripts/                   # Standalone helper scripts for lint baselines, dependency checking, and schema checks
└── tools/                     # Code quality utility scripts including coverage floor enforcement
```
*Note on synced boilerplate:* The `design-system/` directory (CSS tokens and Streamlit helpers) and `.github/` automation workflows/prompts are centrally maintained in and synced from `stranske/Workflows` via `.github/sync-manifest.yml`.

## 4. Major code features you must understand to extend it
- **Subscription Quota Engine (`src/capacity.py:compute`)**: Consumes timestamps and seat logs; produces capacity states (`ok`, `warn`, `shed`, `unknown`) and policy metadata (`drain`, `reserve`). It exhausts prepaid quotas before reset windows.
- **Learned Agent Router (`src/router.py:select_agent`)**: Consumes task types and learned posteriors; produces agent choices with ε-greedy exploration. It routes tasks to whichever agent historically performs best at lowest cost.
- **Worktree Dispatcher (`src/dispatcher.py:delegate`, `src/adapters.py:build_command`, `dispatch`)**: Consumes prompts and targets; produces isolated git worktrees with CLI timeouts and completion markers, protecting main branches.
- **Atomic Claim Mutex (`src/claims.py:claim`, `release`)**: Consumes targets (`owner/repo#number`) and process IDs; produces directory locks, preventing duplicate work across concurrent runs.
- **The Brain Feedback Store (`src/feedback.py:relearn`, `record_outcome`)**: Consumes test verdicts, costs, and durability sweeps (via `record_outcome(run_id, durability=...)`); produces Bayesian routing weights based on production code longevity.
- **Multi-Model Duels & Synthesis (`src/exp_abcd.py:prepare`, `collect`, `evaluate`, `synthesize`, `followup`, `src/synthesis_promotion.py`)**: Consumes competing implementations; produces win matrices, ratings, and synthesized patches (`src/synthesis_promotion.py`) to benchmark models on identical tasks.
- **Capability Admission Gate (`src/capability_admission.py:admit`, `preflight`)**: Consumes capability declarations; produces a mandatory 9-point validation pass verifying callers, heartbeats, and tests, preventing dormant features (`src/capability_activation_audit.py:audit` provides activation audits).
- **Runtime Acceptance Criteria Gate (`src/runtime_ac_gate.py:exercise_gate`, `gate_status`, `src/runtime_ac.py:run_verification`, `evaluate_results`)**: Consumes PRs and test specs with deliberate-break checks; produces binary gate verdicts in `completion_events`, ensuring objective compliance.

## 5. Data model, identifiers and contracts
Entities are tracked via standard keys: runs via UUID `run_id` and `attempt_id`; targets via git strings (`owner/repo#number`); events via `event_id` and hashes (`sha256:...`); and capabilities via kebab-case keys (`frontend-verifier`, `runtime-ac-gate`).

**Persistence**: Local SQLite at `~/.codex/orchestrator/feedback/orchestrator.db` (`src/feedback.py:45`) houses fifteen tables: `runs`, `outcomes`, `costs`, `execution_traces`, `execution_attempts`, `completion_events`, `influence_edges`, `route_weights`, `evaluations`, `evaluations_v2`, `human_calibration`, `evidence_gaps`, `evidence_types`, `owner_questions`, and `resume_tokens`. Ephemeral state lives in `~/.codex/orchestrator/` JSON files and claim directories.

**Versioning**: Applied via integer `version` keys in `route_weights`, durability lifecycles (`pending` -> `durable`, `reverted`, `reworked`, `reopened`, `broke_later`), 30-day recency decay, and 0.5 model-supersession discounts (`src/feedback.py:58, 179, 186`).

**Contracts (`docs/contracts/*`)**:
- `run-contract-v1.md` & `identity-map-conventions.md`: **Documented only**; no code in `src/` emits or consumes `run-contract/v1` or financial entity IDs (`manager:cik_*`, `fund:lei_*`).
- `schemas/evidence-object-v1.schema.json`: **Documented only**; unreferenced in `src/`.
- `capability-bundle-v1.md`: **Partially wired**; `src/repo_knowledge.py:967` updates rules in bundle files via `update_capability_bundle`, but dispatch is unimplemented.
- `agent-runner-output.md`: **Documented standard**; defines Actions runner parameters synced from Workflows.
- *Active internal contracts*: Capability Admission (`src/capability_admission.py`), Rail Exercises (`src/rail_exercise.py`), Completion Events (`src/feedback.py:83-92`), and Route Weights Export (`src/route_weights_export.py`) are fully enforced.

## 6. External inputs and dependencies
- **Data Sources**: Queries GitHub REST/GraphQL APIs via `gh` CLI or HTTP for issues, PRs, and artifacts. Ingests execution traces and costs directly from the LangSmith REST API (`https://api.smith.langchain.com`) via standard library HTTP requests in `src/langsmith_direct.py`. Ingests local agent logs and `ccusage` session files.
- **LLM / Agent Tooling**: Executes external agent CLIs as isolated subprocesses (`claude`, `codex`, `cursor`, `agy`, `vibe`, `aider`). Does not import LangChain or LangGraph runtime libraries in `src/`. Implements an in-house, zero-dependency Model Context Protocol (MCP) server over stdio JSON-RPC (`src/mcp_server.py`).
- **Libraries & Environment**: Built almost entirely on the Python standard library (`sqlite3`, `subprocess`, `urllib.request`, `json`, `hashlib`, `pathlib`, `argparse`, `ast`). Only third-party runtime package is optional `PyYAML` (`yaml`, `src/model_profile_trial_bridge.py:249`). Runs headlessly on macOS with zero external database servers, containers, or daemon web servers.

## 7. Current state
**Test and CI Posture**: `src/verify.py` strictly enforces `.verify-floor.json` counts: exactly 631 collected/passed tests, bounded skip ceilings (max 26 CI runner, max 39 mirror), 94 selftest modules, and 5 capability gates. Remote CI (`pr-00-gate.yml`) runs Ruff, Black, pytest, combined coverage, and Mypy (0 exempt modules; `pyproject.toml:99-127`, `.verify-floor.json:8`).

**Production-Usable vs. Prototype**: Usable: local quota tracking, Bayesian routing, isolated execution, claim locks, SQLite persistence, MCP server, and verification harness. Prototype/gated: remote dispatch lane (shadow default), Thompson exploration (evaluated, kept off), strategy duels (blocked from cron), and automated redirect apply.

**Consequential Gaps & Signals**:
1. *Discovery Unwired*: `src/router.py:932` carries `TODO(discovery): wire the opener/closer discovery to write backlog.json:`.
2. *Per-Tool Quotas Incomplete*: `src/capacity.py:10` notes `[per-tool Codex/Claude split is a v1 TODO]`.
3. *Verifier Signals Pending*: `src/backlog.py:18` states `review/polish come from later verifier signals (TODO)`.
4. *Starved LangSmith Pipeline*: `src/langsmith_direct.py:4-8` notes consumer CI repos do not upload artifacts, forcing direct API polling.
5. *Unimplemented Backplane*: `docs/contracts/run-contract-v1.md:16-17` admits: "No participant emits an envelope yet (that is P1+)."
6. *Human Calibration Dormant*: `PLANNING.md:58-64` records zero human spot-labels, leaving bias regression uncalibrated.
7. *Demoted Remote Dispatch*: `README.md:37-39` records remote dispatch demotion to shadow on 2026-09-03 after 14 runs produced 9 abandonments.
8. *Unwired Outcome Triggers*: `src/capability_outcome_bridge.py:155` notes capability outcomes cannot be attributed because triggers remain unwired.

## 8. Claims vs reality
- **Backplane Entity Interoperability**: Docs in `docs/contracts/run-contract-v1.md:1-18` define the shared research backplane contract, while the dossier claimed Orchestrator joins investment entities (`manager:cik_*`, `fund:lei_*`) across tools. *Reality*: `docs/contracts/run-contract-v1.md:16-17` explicitly clarifies that no participant emits an envelope yet (P1+); Orchestrator identifies targets purely by git references (`owner/repo#number`) and contains zero lines in `src/` implementing or consuming `run-contract/v1` or financial entity IDs, retaining only the synced specification and validator (`scripts/validate_run_contract.py`).
- **Active Remote Fleet Coordination**: Docs describe actively coordinating a fleet across 11 repos driving keepalive automation (`README.md:3-10`). *Reality*: Remote dispatch is deactivated by default; demoted to shadow on 2026-09-03 after 14 dispatches in 30 days yielded 9 abandoned runs and 0 durable merges (`README.md:37-39`).
- **Streamlit Presentation System**: Docs describe a shared design system with Streamlit helpers (`design-system/README.md`, `design-system/ds_streamlit.py`). *Reality*: Vendored boilerplate synced from `stranske/Workflows`. Orchestrator has no web interface, no Streamlit app, and no UI entry point; `ds_streamlit.py` is never called in `src/`.
- **Automated CI LangSmith Harvesting**: Docs state telemetry is gathered from CI artifacts via `src/langsmith_fetch.py`. *Reality*: As admitted in `src/langsmith_direct.py:4-8`, consumer repos never upload artifacts, starving the harvester and necessitating direct REST API queries.
- **Autonomous Strategy Duels (H4/H5)**: Docs describe multi-agent duels with synthesis promotion (`PLANNING.md:65-74`). *Reality*: `src/research_scheduler.py` explicitly refuses to auto-launch strategy duel arms from scheduled ticks, keeping evaluation stalled.

## 9. Interoperability hooks (for the fleet program)
- **What this repo could OFFER to sibling repos**:
  - *Learned Routing Snapshot*: Exports `config/route-weights.json` on git branch `exports/route-weights` (and local `$ORCH_STATE_DIR/route-weights-export.json`) via `src/route_weights_export.py`, providing rankings, posteriors, and cost-per-success scores per agent and task type.
  - *Fleet Capacity Heartbeat*: Emits `~/.codex/handoff/orchestrator.json` and `capacity.json` for external automation to check seat exhaustion.
  - *Reconciled Telemetry Aggregates*: Exposes cross-vendor token consumption, dollar costs, and run latency from `feedback.py`.
  - *Repository Playbook Rules*: Exports managed invariants into consumer `AGENTS.md` files or `capability-bundle/v1` payloads via `src/repo_knowledge.py:967`.
- **What this repo would CONSUME from sibling repos**:
  - *Task Discovery & Backlog*: Reads GitHub issue and PR labels (`agent:*`, `task:*`, `status:ready`) from consumer repositories.
  - *Clean Git Worktrees*: Requires shallow clones and valid branch heads to spawn worker agent CLIs.
  - *Telemetry Traces*: Consumes LangSmith trace metadata tagged with repository names and issue numbers.
  - *Test Verification*: Consumes test node results and coverage files generated by consumer test suites.
- **Identifier Collisions and Vocabulary Conflicts**:
  - *Domain Entity Mismatch*: Orchestrator identifies work items exclusively by git targets (`owner/repo#number`), whereas investment siblings use financial keys (`manager:cik_*`, `fund:lei_*`).
  - *Ambiguity over 'Orchestrator'*: In `stranske/Workflows`, 'Orchestrator' refers to Actions loop concurrency; here it denotes the local fleet manager (`ARCHITECTURE.md:46-50`).
  - *Task Vocabulary*: Router task types (`implement`, `review`, `testgen`, `mechanical`) must strictly align with consumer labeling.

## 10. Reuse candidates
- `src/verify.py` & `src/env_prereq.py`: Test verification floor and skip-ceiling harness enforcing collection equality.
- `src/capacity.py`: Multi-window rolling subscription quota and burst allocation tracker.
- `src/mcp_server.py`: Zero-dependency, pure standard library Model Context Protocol stdio server.
- `src/dispatcher.py` & `src/adapters.py`: Subprocess execution harness with timeouts, stream logging, and completion markers.
- `src/router.py` & `src/feedback.py`: Bayesian prior-to-posterior agent router balancing success rates against execution costs.
- `src/durability_sweep.py`: Multi-day git durability auditor verifying whether merged code survived without rework.
- `src/claims.py`: Atomic filesystem mutex with stale-lease reaping for crash-resilient local locking.

## 11. Proposed direction (evidence-based)
- **Finish what is scaffolded**:
  - *Decommission or Re-architect Remote Dispatch*: Given a 64% abandonment rate (9 of 14) and 0 durable outcomes (`README.md:37-39`), either prune remote dispatch code or rebuild it around exact-head merge guards.
  - *Implement Backplane Run Contract Emitter*: Build a `run-contract/v1` exporter in `src/` to satisfy `docs/contracts/run-contract-v1.md:16-17`.
  - *Prune Starved Actions LangSmith Harvester*: Remove `src/langsmith_fetch.py` and standardize on direct API client in `src/langsmith_direct.py:4-8`.
  - *Connect Discovery to Approved-Issue Queues*: Resolve `TODO(discovery)` in `src/router.py:932` by integrating backlog discovery directly with Workflows queues rather than polling labels (`ARCHITECTURE.md:40-43`).
- **New capability**:
  - *Bridge Financial Entity Identifiers to Task Context*: Ingest `docs/contracts/identity-map-conventions.md` into `src/repo_knowledge.py` so agents receive canonical firm and fund identifiers.
  - *Establish Human Spot-Calibration Tooling*: Add a lightweight CLI command to record human scores, activating dormant regression bias correction in `src/feedback.py` (`PLANNING.md:58-64`).
  - *Remove Non-Functional Design System Boilerplate*: Purge unused `design-system/` files or document an exception in `AGENTS.md` to prevent confusion about non-existent web interfaces.

## 12. What a colleague needs to know (5 bullets, no code identifiers)
- **Automated AI Traffic Controller**: Acts as an automated dispatcher for commercial AI coding tools, assigning programming jobs to whichever tool has proven best at that specific work.
- **Subscription Quota Maximizer**: Tracks usage limits across prepaid AI subscriptions (like 5-hour and weekly caps), routing work to tools with expiring allowances to avoid out-of-pocket API fees.
- **Judged by Code Longevity**: Evaluates tools based on whether generated code passed automated tests, merged cleanly, and remained in production days later without being rewritten or rolled back.
- **Completely Local and Contained**: Runs entirely on a local computer without database servers or cloud containers, using throwaway workspaces so flawed code cannot corrupt working projects.
- **Shifted from Cloud Automation to Local Research**: After finding that automated cloud tasks were frequently abandoned, the system shifted to operate primarily as an offline testbed for evaluating AI performance and advising on resource allocation.

Verified 2026-09-04T17:30:00Z by gemini: 57 claims checked, 12 corrected, 1 unverifiable.
