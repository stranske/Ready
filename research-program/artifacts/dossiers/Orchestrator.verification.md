# Orchestrator dossier — verification table

Verified against clone `clones/Orchestrator` at HEAD `e63a541f84c911a26e9f163ffc111b12629be151` (2026-09-04).
Method: every cited file:line and symbol was opened and verified against the repository code, schema, and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 44 |
| WRONG (corrected in dossier) | 12 |
| UNVERIFIABLE | 1 |
| **Total checked** | **57** |

### Key Findings & Corrections

1. **§4 Hallucinated & drifted symbol names:**
   - **`src/capacity.py:compute_capacity`**: Does not exist. The public arity-normalized interface is `capacity.compute` (`src/capacity.py:505`).
   - **`src/adapters.py:run_agent`**: Does not exist. Subprocess command building and execution are handled by `adapters.build_command` (`src/adapters.py:159`) and `adapters.dispatch` (`src/adapters.py:279`).
   - **`src/feedback.py:update_durability`**: Does not exist. Durability updates are performed via `feedback.record_outcome(run_id, durability=...)` (`src/feedback.py:2525-2565`), as called by `durability_sweep.py:601`.
   - **`src/exp_abcd.py:run_experiment`**: Does not exist. Experiment execution is split across distinct lifecycle functions: `prepare`, `collect`, `evaluate`, `synthesize`, and `followup` (`src/exp_abcd.py:16-23, 1430`).
   - **`src/capability_admission.py:audit`**: Does not exist in `capability_admission.py`. The admission gate function is `admit` (`src/capability_admission.py:470`), while `audit` belongs to `capability_activation_audit.py:audit`.
   - **`src/runtime_ac_gate.py:evaluate_target`**: Does not exist anywhere in the repository. Gate evaluation is performed via `runtime_ac_gate.exercise_gate` and `gate_status` (`src/runtime_ac_gate.py:144, 173`), while verification and grading are executed by `runtime_ac.run_verification` and `evaluate_results` (`src/runtime_ac.py:217, 295`).

2. **§8 Strawman refutation in Claims vs Reality (adversarial check):**
   - The dossier asserted that `docs/contracts/run-contract-v1.md:1-18` claims Orchestrator joins investment entities (`manager:cik_*`, `fund:lei_*`) across tools, refuting it by noting zero implementation code in `src/`.
   - Opening `docs/contracts/run-contract-v1.md:1-18` reveals that the document does NOT claim Orchestrator joins investment entities. It is the generic research-backplane envelope specification owned by Workflows, synced to participant repos, and explicitly states in lines 16–17: *"No participant emits an envelope yet (that is P1+); nothing here is wired into any repo's CI."* Refuting an unmade claim was a false refutation against a strawman (mirroring the exact issue seen in Inv-Man-Intake). The corrected statement reflects that Orchestrator tracks targets strictly by git strings (`owner/repo#number`) and does not emit or consume `run-contract/v1` or financial entity IDs, keeping only the synced spec and validator (`scripts/validate_run_contract.py`).

3. **§2 & §7 Inventory & count drift:**
   - **MCP Tools Count:** `src/mcp_server.py:50-219` defines exactly 10 tools (`capacity_status`, `fleet_summary`, `route_weights`, `capability_advice`, `capability_decline`, `capability_associations`, `owner_questions`, `answer_owner_question`, `record_owner_question`, `resume_hint`), not 9.
   - **Selftests Count:** `verify.selftest_modules()` discovers 94 selftest modules at HEAD, not 88 (88 was the historical count from 2026-08-26 recorded in `.verify-floor.json`).
   - **`src/` Python Module Count:** `src/` contains 107 flat `.py` files at HEAD (`ls clones/Orchestrator/src/*.py | wc -l`), not 99.
   - **Feedback Store Tables:** `src/feedback.py:48-155` defines 15 tables in SQLite (the dossier text listed all 15 names but stated "fourteen tables").

4. **§2 & §9 Route weights export target:**
   - The dossier cited `exports/route-weights.json`. In reality, `src/route_weights_export.py` exports locally to `$ORCH_STATE_DIR/route-weights-export.json`, and when publishing (`--publish` with `ORCH_ROUTE_WEIGHTS_PUBLISH=1`), commits to git branch `exports/route-weights` at target path `config/route-weights.json` (`docs/ROUTE_WEIGHTS_EXPORT.md:1-42`).

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | `compute_capacity` consumes timestamps/seat logs; produces capacity states (`ok`, `reserve`, `drain`, `exhausted`) | `src/capacity.py:compute_capacity` | **WRONG** | Function is `capacity.compute` (`src/capacity.py:505`). Returns 3-tuple `(state, reason, meta)`. Primary states are `ok`, `warn`, `shed`, `unknown`; policies `drain` and `reserve` are emitted in `meta["policy"]`. |
| 2 | `select_agent` consumes task types and learned posteriors; produces agent choices with ε-greedy exploration | `src/router.py:select_agent` | CONFIRMED | `src/router.py:440` defines `select_agent(task_type, cap, ...)`. Uses ε-greedy (`EPSILON = 0.10`, line 35) balancing learned score and cost. |
| 3 | `delegate` and `run_agent` produce isolated git worktrees with CLI timeouts and completion markers | `src/dispatcher.py:delegate`, `src/adapters.py:run_agent` | **WRONG** | `dispatcher.delegate` confirmed (`src/dispatcher.py:217`). However, `adapters.run_agent` does not exist; subprocess commands are built by `adapters.build_command` (`:159`) and executed via `adapters.dispatch` (`:279`). |
| 4 | Atomic claim mutex (`claim`, `release`) creates directory locks per target | `src/claims.py:claim`, `release` | CONFIRMED | `src/claims.py:40` defines `claim()`; `src/claims.py:68` defines `release()`. Manages filesystem directory locks with stale lease reaping. |
| 5 | `relearn` and `update_durability` produce Bayesian routing weights from test verdicts, costs, and durability | `src/feedback.py:relearn`, `update_durability` | **WRONG** | `feedback.relearn` confirmed (`src/feedback.py:3728`). `update_durability` does not exist; durability is recorded via `feedback.record_outcome(run_id, durability=...)` (`:2525`), invoked by `src/durability_sweep.py:601`. |
| 6 | Multi-model duels: `run_experiment` produces win matrices, ratings, and patches via `synthesis_promotion` | `src/exp_abcd.py:run_experiment`, `src/synthesis_promotion.py` | **WRONG** | `run_experiment` does not exist. Experiment lifecycle is split into `prepare` (`:331`), `collect` (`:424`), `evaluate` (`:477`), `synthesize` (`:700`), and `followup` (`:1430`). `synthesis_promotion.py` confirmed. |
| 7 | Capability admission gate (`audit`, `preflight`) produces 9-point validation pass | `src/capability_admission.py:audit`, `preflight` | **WRONG** | `capability_admission.preflight` confirmed (`src/capability_admission.py:517`). However, `audit` does not exist in this module; admission evaluation is `admit` (`:470`). `audit` belongs to `src/capability_activation_audit.py:audit`. |
| 8 | Runtime AC gate (`evaluate_target`) consumes PRs and specs with deliberate-break checks; produces verdicts in `completion_events` | `src/runtime_ac_gate.py:evaluate_target` | **WRONG** | `evaluate_target` does not exist. Gate evaluation is `runtime_ac_gate.exercise_gate` / `gate_status` (`:144, 173`); verification is `runtime_ac.run_verification` / `evaluate_results` (`src/runtime_ac.py:217, 295`). Emits to `completion_events`. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 9 | Entities tracked via standard keys: UUID `run_id`/`attempt_id`, git targets (`owner/repo#number`), events (`event_id`, `sha256:...`), kebab-case capabilities | `src/feedback.py:48-95` | CONFIRMED | Tables `runs`, `completion_events`, and capability registry use these exact identifier schemes. |
| 10 | Local SQLite at `~/.codex/orchestrator/feedback/orchestrator.db` houses fourteen tables | `src/feedback.py:45` | **WRONG (count)** | DB path confirmed (`DB_PATH = Path(os.environ.get("ORCH_FEEDBACK_DB", ...))`). However, schema defines exactly 15 tables (`runs`, `outcomes`, `costs`, `execution_traces`, `execution_attempts`, `completion_events`, `influence_edges`, `route_weights`, `evaluations`, `evaluations_v2`, `human_calibration`, `evidence_gaps`, `evidence_types`, `owner_questions`, `resume_tokens`), not 14. |
| 11 | Versioning via integer `version` in `route_weights`, durability lifecycles, 30-day recency decay, 0.5 model-supersession discount | `src/feedback.py:58, 179, 186` | CONFIRMED | `durability` default 'pending' (:58); `DEFAULT_RELEARN_HALF_LIFE_DAYS = 30.0` (:179); `SUPERSEDED_MODEL_WEIGHT = 0.5` (:186). |
| 12 | `run-contract-v1.md` & `identity-map-conventions.md`: Documented only; no code in `src/` emits or consumes them | `docs/contracts/run-contract-v1.md`, `src/` | CONFIRMED | No occurrences of `run-contract/v1` or `manager:cik_*`/`fund:lei_*` in `src/`. Only `scripts/validate_run_contract.py` exists as a validator. |
| 13 | `schemas/evidence-object-v1.schema.json`: Documented only; unreferenced in `src/` | `docs/contracts/schemas/evidence-object-v1.schema.json` | CONFIRMED | Schema file exists in docs/contracts/schemas/; zero references across `src/`. |
| 14 | `capability-bundle-v1.md`: Partially wired; updates rules in bundle files via `update_capability_bundle`, dispatch unimplemented | `src/repo_knowledge.py:967` | CONFIRMED | `update_capability_bundle()` edits `orchestrator_repo_playbook_rules` in bundle files; remote dispatch is unimplemented. |
| 15 | `agent-runner-output.md`: Documented standard; defines Actions runner parameters synced from Workflows | `docs/contracts/agent-runner-output.md` | CONFIRMED | File exists in `docs/contracts/` defining standard runner parameters. |
| 16 | Active internal contracts: Capability Admission, Rail Exercises, Completion Events, Route Weights Export fully enforced | `src/capability_admission.py`, `src/rail_exercise.py`, `src/feedback.py:83-92`, `src/route_weights_export.py` | CONFIRMED | All 4 modules exist and strictly enforce runtime validation contracts. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement |
|---|---|---|---|---|
| 17 | **Claim: Backplane Entity Interoperability**: Docs in `docs/contracts/run-contract-v1.md:1-18` claim Orchestrator joins investment entities across tools | `docs/contracts/run-contract-v1.md:1-18`, `src/` | **WRONG (strawman refutation)** | `docs/contracts/run-contract-v1.md:1-18` does NOT claim Orchestrator joins investment entities. It is the Workflows-owned research backplane specification synced to participants, and explicitly states in lines 16–17: *"No participant emits an envelope yet (that is P1+); nothing here is wired into any repo's CI."* The true reality is that Orchestrator tracks targets strictly by git strings (`owner/repo#number`) and contains zero lines in `src/` implementing or consuming `run-contract/v1` or financial entity IDs (`manager:cik_*`, `fund:lei_*`), keeping only the synced spec and validator (`scripts/validate_run_contract.py`). |
| 18 | **Claim: Active Remote Fleet Coordination**: Docs describe actively coordinating fleet across 11 repos driving keepalive | `README.md:3-10`, `README.md:37-39` | CONFIRMED | `README.md:3-10` describes active multi-agent fleet coordination, but lines 37–39 and `orchestrate.sh:50-52` confirm remote dispatch was demoted to shadow default on 2026-09-03 after 14 dispatches produced 9 abandoned runs and 0 durable merges. |
| 19 | **Claim: Streamlit Presentation System**: Docs describe shared design system with Streamlit helpers | `design-system/README.md`, `design-system/ds_streamlit.py` | CONFIRMED | `design-system/README.md:50` confirms kit is synced template boilerplate from `stranske/Workflows`. Orchestrator has no web interface or Streamlit app; `ds_streamlit.py` has no callers in `src/`. |
| 20 | **Claim: Automated CI LangSmith Harvesting**: Docs state telemetry is gathered from CI artifacts via `src/langsmith_fetch.py` | `src/langsmith_fetch.py`, `src/langsmith_direct.py:4-8` | CONFIRMED | `src/langsmith_fetch.py` provides GitHub artifact download logic, but `src/langsmith_direct.py:4-8` documents that consumer CI repos never upload artifacts, starving the harvester and requiring direct REST API polling. |
| 21 | **Claim: Autonomous Strategy Duels (H4/H5)**: Docs describe multi-agent duels with synthesis promotion | `PLANNING.md:65-74`, `src/research_scheduler.py` | CONFIRMED | `PLANNING.md:65-74` outlines strategy learning, but `src/research_scheduler.py:455-456, 658-666` skips strategy arms with `strategy_arms_not_launchable`, requiring explicit manual override flags (`--confirm-strategy`, `ORCH_STRATEGY_EXPERIMENT=1`). |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 22 | Exports `exports/route-weights.json` via `src/route_weights_export.py` providing rankings, posteriors, and cost-per-success scores | `src/route_weights_export.py`, `docs/ROUTE_WEIGHTS_EXPORT.md:1-40` | **WRONG (path)** | Path `exports/route-weights.json` does not exist. `src/route_weights_export.py` writes locally to `$ORCH_STATE_DIR/route-weights-export.json` and publishes to git branch `exports/route-weights` at path `config/route-weights.json`. |
| 23 | Emits `~/.codex/handoff/orchestrator.json` and `capacity.json` for external automation to check seat exhaustion | `src/capacity.py`, `src/dispatcher.py` | CONFIRMED | Constants `HEARTBEAT_JSON` and `CAPACITY_JSON` in `dispatcher.py` and `capacity.py` write these exact files. |
| 24 | Exposes cross-vendor token consumption, dollar costs, and run latency from `feedback.py` | `src/feedback.py` | CONFIRMED | Persisted in `costs` and `execution_traces` SQLite tables; queryable via public helpers. |
| 25 | Exports managed invariants into consumer `AGENTS.md` files or `capability-bundle/v1` payloads via `src/repo_knowledge.py:967` | `src/repo_knowledge.py:967` | CONFIRMED | `update_capability_bundle` modifies rules inside `orchestrator_repo_playbook_rules`. |
| 26 | Consumes task discovery & backlog: reads GitHub issue/PR labels (`agent:*`, `task:*`, `status:ready`) | `src/backlog.py` | CONFIRMED | `backlog.py` filters GitHub issues and PRs across repositories using these labels. |
| 27 | Consumes clean git worktrees: requires shallow clones and valid branch heads to spawn worker agent CLIs | `src/provision.py`, `src/dispatcher.py` | CONFIRMED | Worktree creation and management implemented in `provision.py` and invoked by `dispatcher.py`. |
| 28 | Consumes telemetry traces: LangSmith trace metadata tagged with repo names and issue numbers | `src/langsmith_direct.py` | CONFIRMED | `langsmith_direct.py` fetches runs tagged with `repo` and `issue_number`/`pr_number`. |
| 29 | Consumes test verification: test node results and coverage files generated by consumer suites | `src/local_verify.py`, `src/runtime_ac.py` | CONFIRMED | Runs pytest in target worktrees and parses node-level outcomes. |
| 30 | Sibling GitHub Actions workflows (Keepalive, Autofix) consume exported route weights | `docs/ROUTE_WEIGHTS_EXPORT.md:6-8` | **UNVERIFIABLE (off-clone)** | Intended consumer URL is documented, but live consumption by external workflows cannot be verified from local repo clone alone. |
| 31 | Domain entity mismatch: Orchestrator identifies work items exclusively by git targets (`owner/repo#number`), not financial keys (`manager:cik_*`, `fund:lei_*`) | `src/`, `docs/contracts/identity-map-conventions.md` | CONFIRMED | All internal tables and queues key on `target = owner/repo#number`. |
| 32 | Ambiguity over 'Orchestrator': In `stranske/Workflows`, 'Orchestrator' refers to Actions loop concurrency; here it denotes the local fleet manager | `ARCHITECTURE.md:46-50` | CONFIRMED | `ARCHITECTURE.md:46-50` explicitly warns about this exact naming collision. |
| 33 | Task vocabulary: Router task types (`implement`, `review`, `testgen`, `mechanical`) must align with consumer labeling | `src/router.py` | CONFIRMED | `ROUTE_TABLE` in `src/router.py` is keyed by these exact task type names. |

---

## §1, §2, §3, §6, §7, §10, §11, §12 — Supporting Claims

| # | Section | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|---|
| 34 | §1 | Personal-scale multi-agent fleet controller purpose and constraints | `README.md:3-10, 20-33`, `ARCHITECTURE.md:14-43`, `PLANNING.md:9-18` | CONFIRMED | Paragraph text accurately summarizes purpose, constraints, and architecture. |
| 35 | §2 | Fleet Tick entry point `orchestrate.sh` / `src/tick.py`; shadow default; live dispatch gated behind `ORCH_DISPATCH_LANE=1` | `README.md:34-39`, `orchestrate.sh:1-120` | CONFIRMED | `orchestrate.sh:50-52` confirms `ORCH_DISPATCH_LANE` default 0; `README.md:37-39` confirms stats. |
| 36 | §2 | Verification Suite: validates test collection equality against `.verify-floor.json` (631 collected/passed, 26/39 skip ceilings, 88 selftests, 5 gates) | `src/verify.py:1-54`, `.verify-floor.json` | **WRONG (selftest count)** | Collection floor (631), pass floor (631), skip ceilings (26/39), and gates (5) confirmed. However, discovered selftests count is 94 modules at HEAD (`verify.selftest_modules()`), not 88. |
| 37 | §2 | Observability CLI: generates terminal scorecards and JSON dumps | `src/observability_dashboard.py:1-8, 2225-2237`, `src/periodic_report.py` | CONFIRMED | Options and report generation verified in `observability_dashboard.py`. |
| 38 | §2 | Stdio MCP Server: standard-library JSON-RPC server offering 9 tools | `src/mcp_server.py:1-219` | **WRONG (tool count)** | `mcp_server.TOOLS` defines exactly 10 tools, not 9. |
| 39 | §2 | Route export entry point and publish gating behind `ORCH_ROUTE_WEIGHTS_PUBLISH=1` | `src/route_weights_export.py`, `docs/ROUTE_WEIGHTS_EXPORT.md:1-40` | **WRONG (target path)** | Target branch is `exports/route-weights` at `config/route-weights.json`; local path is `$ORCH_STATE_DIR/route-weights-export.json`. |
| 40 | §2 | Presentation UI: `design-system/ds_streamlit.py` is inactive synced template boilerplate | `design-system/README.md:49-51` | CONFIRMED | Synced from `stranske/Workflows`; no Streamlit app in repo. |
| 41 | §2 | Excel/Spreadsheets: absent | None in `src/` | CONFIRMED | Zero spreadsheet libraries or generators in repository. |
| 42 | §3 | `src/` directory contains 99 flat Python modules | `src/` | **WRONG (count)** | `src/` contains 107 flat Python modules at HEAD (`ls clones/Orchestrator/src/*.py | wc -l`), not 99. |
| 43 | §3 | Structure tree files and directories exist as described | Tree paths in §3 | CONFIRMED | `orchestrate.sh`, `pyproject.toml`, `.verify-floor.json`, `tests/` (48 items), `docs/contracts/`, etc. confirmed. |
| 44 | §6 | Data sources: queries GitHub REST/GraphQL; LangSmith REST API at `https://api.smith.langchain.com`; ccusage session files | `src/langsmith_direct.py:52` | CONFIRMED | URL and CLI invocations verified. |
| 45 | §6 | LLM/Agent tooling: executes external CLIs as subprocesses; no LangChain/LangGraph imports in `src/`; pure stdio MCP server | `adapters.py`, `src/mcp_server.py` | CONFIRMED | Subprocess execution verified; zero third-party framework dependencies in `src/`. |
| 46 | §6 | Standard library foundation; optional `PyYAML` in `src/model_profile_trial_bridge.py:249`; runs headlessly on macOS | `src/model_profile_trial_bridge.py:249` | CONFIRMED | Verified imports and optional PyYAML guard. |
| 47 | §7 | CI and test enforcement: Ruff, Black, pytest, combined coverage, strict Mypy (0 exempt modules) | `pyproject.toml:99-127`, `.verify-floor.json:8` | CONFIRMED | `.verify-floor.json:8` records `mypy_exempt_max: 0`. Configs match. |
| 48 | §7 | Gap 1: Discovery unwired (`src/router.py:932`) | `src/router.py:932` | CONFIRMED | Verified exact comment `TODO(discovery): wire the opener/closer discovery to write backlog.json:`. |
| 49 | §7 | Gap 2: Per-tool Codex/Claude split is a v1 TODO | `src/capacity.py:10` | CONFIRMED | Verified exact comment `[ccusage reports one shared active block — per-tool Codex/Claude split is a v1 TODO]`. |
| 50 | §7 | Gap 3: Verifier signals pending | `src/backlog.py:18` | CONFIRMED | Verified exact comment `review/polish come from later verifier signals (TODO)`. |
| 51 | §7 | Gap 4: Starved LangSmith pipeline | `src/langsmith_direct.py:4-8` | CONFIRMED | Verified documentation of starved CI artifact chain. |
| 52 | §7 | Gap 5: Unimplemented backplane run envelope | `docs/contracts/run-contract-v1.md:16-17` | CONFIRMED | Verified admission that no participant emits an envelope yet. |
| 53 | §7 | Gap 6: Human calibration dormant | `PLANNING.md:58-64` | CONFIRMED | Verified absence of human spot-labels. |
| 54 | §7 | Gap 7: Demoted remote dispatch | `README.md:37-39` | CONFIRMED | Verified 14 runs, 9 abandoned, 0 durable merges. |
| 55 | §7 | Gap 8: Unwired outcome triggers | `src/capability_outcome_bridge.py:155` | CONFIRMED | Verified comment on unnameable capabilities due to unwired triggers. |
| 56 | §10 | Reuse candidates (7 modules accurately described) | `src/verify.py`, `src/capacity.py`, `src/mcp_server.py`, etc. | CONFIRMED | All 7 modules exist and serve the described functions. |
| 57 | §12 | 5 colleague takeaway bullets without code identifiers | §12 bullets 1-5 | CONFIRMED | Exactly 5 bullets, zero code identifiers, accurately describing system role and trajectory. |
