# stranske Staging Fleet — dossier (2026-09-04)

This dossier covers three sibling staging repositories: **stranske/Template**, **stranske/Ready**, and **stranske/Workflows-Integration-Tests** (WIT). Together they form the onboarding and validation layer for the organization's Python consumer-repo fleet, which plugs into the central **stranske/Workflows** automation library. None of these repos implement investment research logic; they ship workflow wiring, contract documentation, and placeholder application code.

## 1. Purpose in one paragraph

The staging fleet solves a governance problem: every new Python tool in the investment office should share the same GitHub Actions CI, commercial AI coding assistant-based agent keepalive, coverage policy, and (eventually) research-backplane run records—while keeping product code local. **Template** is the GitHub *template repository* used to mint new consumer repos (`docs/SETUP_CHECKLIST.md` §1.1: `gh repo create … --template stranske/Template`). **Ready** is the long-lived conformance repo that exercises the full Workflows surface, including coverage baseline soft-gating that Template omits (`Ready/README.md` “Coverage Baseline”, `config/coverage-baseline.json`). **WIT** is a thin integration consumer that stress-tests the reusable Python CI workflow and reports failures back to Workflows (`Workflows-Integration-Tests/README.md`, `.github/workflows/ci.yml`). The operating constraint is *consumer-repo discipline*: workflow logic is synced from Workflows (`AGENTS.md` “Cross-Repo Policy”); each repo only owns files such as `ci.yml`, `autofix-versions.env`, and `src/`.

## 2. Who uses it and how (surfaces)

| Surface | Entry point | Who uses it | Status (evidence) |
|---------|-------------|-------------|-------------------|
| GitHub Actions — PR Gate | `.github/workflows/pr-00-gate.yml` | Developers, agents | **Working** (`pr-00-gate.yml` L1–22) |
| GitHub Actions — push CI | `.github/workflows/ci.yml` | CI on `main` | **Working** — `reusable-10-ci-python.yml@main` (`ci.yml` L34) |
| Agent keepalive | `agents-81-gate-followups.yml` + `agents-80-pr-event-hub.yml` | Service bot | **Working** in Template/Ready (`agents-81-gate-followups.yml` L290–301); **legacy** `agents-keepalive-loop.yml` in WIT |
| Issue intake | `agents-issue-intake.yml` | Owners with `agent:codex` | **Working** (workflow present; flow in `README.md` L84–93) |
| WIT multi-matrix CI | `Workflows-Integration-Tests/.github/workflows/ci.yml` | Workflows maintainers | **Working** (four CI jobs + notifier, L17–180) |
| Local dev/test | `pyproject.toml`, `pytest` | Developers | **Working** (`tests/test_main.py`, `tests/test_example.py`) |
| Backplane validator | `scripts/validate_run_contract.py` | CI (opt-in) | **Partial** — no emitter, no `config/backplane_participants.json` |
| Coverage guard | `tools/coverage_guard.py` | Maintainers | **Working in Ready**; **partial in Template** (no baseline file) |
| Design tokens | `design-system/tokens.css` | Future apps | **Scaffold** — no `src/` consumer (`design-system/README.md`) |
| Issue queue | `Issues.txt` | Humans | **Scaffold** — references missing `main.py` (`Issues.txt` L37–38) |

No end-user UI, API server, Excel add-in, or application database exists in any staging repo.

## 3. Structure map

```
Template/  Ready/          # Nearly identical consumer scaffolds
├── .github/               # Workflows + scripts synced from stranske/Workflows
├── config/                # LLM slots/registry; Ready adds coverage-baseline.json
├── docs/contracts/        # run-contract, evidence-object, identity-map schemas
├── scripts/               # LangChain issue tools, validate_run_contract.py
├── tools/                 # coverage_guard, llm_registry, langchain_client
├── src/my_project/        # Placeholder package (greet, add)
├── tests/                 # pytest; Ready adds test_coverage_baseline.py
└── design-system/         # Shared CSS tokens (synced)

Ready-only: smoke/codex-smoke.txt, config/coverage-baseline.json

Workflows-Integration-Tests/
├── .github/workflows/ci.yml   # Multi-config reusable CI + failure notify
├── src/example/               # add() only
├── tests/                     # Script/tool integration tests
└── scripts/, tools/           # Subset of fleet sync tooling
```

Skipped as synced boilerplate: `.github/scripts/node_modules/` (vendored; guarded by `tests/test_repo_hygiene.py` L24–31).

## 4. Major code features you must understand to extend it

- **PR Gate** — `pr-00-gate.yml` classifies changes, runs reusable Python CI, aggregates coverage, appends keepalive checklists (`pr-00-gate.yml` L24–45, L859–953). Every agent iteration requires Gate success.

- **Thin CI delegation** — `ci.yml` forwards lint/mypy/pytest to Workflows (`ci.yml` L34–39). WIT exists to regression-test this contract.

- **Keepalive via Gate Followups** — `agents-81-gate-followups.yml` calls `keepalive_loop.js` to dispatch commercial AI coding assistant (`agents-81-gate-followups.yml` L290–332). README still names the older `agents-keepalive-loop.yml` (`README.md` L69–76).

- **LLM slot resolution** — `tools/llm_registry.py` reads `config/llm_slots.json` and `model_registry.json`, emitting `SelectionDecision` without fabricated scores (`llm_registry.py` L31–50).

- **LangChain client** — `tools/langchain_client.py` builds provider clients with OpenAI → Anthropic → GitHub Models fallback (`langchain_client.py` L1–6). Feeds `scripts/langchain/*` issue tools.

- **Coverage guard** — `tools/coverage_guard.py` compares runs to `config/coverage-baseline.json` (`coverage_guard.py` L20–26). Ready locks `line` key precedence in `tests/test_coverage_baseline.py` L34–44.

- **Run-contract validator** — `scripts/validate_run_contract.py` checks `run-contract/v1` against JSON Schema; SKIPs when registry absent (`validate_run_contract.py` L35–42).

- **Backplane conformance stub** — `backplane-conformance.yml` skips without `emit_reference_run.sh` (`backplane-conformance.yml` L49–55).

- **Issue semantic tooling** — `scripts/langchain/integration_layer.py` merges classifier labels onto parsed issues (`integration_layer.py` L19–37).

- **WIT failure notifier** — `ci.yml` opens `integration-failure` issues on `stranske/Workflows` (`ci.yml` L90–180).

## 5. Data model, identifiers and contracts

**Application data:** Only `greet`/`add` in `src/my_project/__init__.py` or WIT's `add` in `src/example/__init__.py`. No database or run ledger.

| Contract | Location | Emitted? | Consumed? |
|----------|----------|----------|-----------|
| `run-contract/v1` | `docs/contracts/run-contract-v1.md` | **No** (“No participant emits an envelope yet”, L15–17) | Validator only (`validate_run_contract.py`) |
| `evidence-object/v1` | `schemas/evidence-object-v1.schema.json` | **No** | Validator only |
| `artifact-manifest/v1` | `schemas/artifact-manifest-v1.schema.json` | **No** | Conformance workflow paths (`backplane-conformance.yml` L66–67) |
| `capability-bundle/v1` | `docs/contracts/capability-bundle-v1.md` | **No** | Documented only |
| Identity map | `docs/contracts/identity-map-conventions.md` | **No** | Documented only — IDs like `manager:cik_0001067983` (L63–72) |

**Identifiers:** Entity IDs follow `<entity_type>:<normalized_identity>` (`identity-map-conventions.md` L44–61). Agent control uses GitHub labels (`README.md` L105–110). LLM slots named in `config/llm_slots.json` L2–17.

**Persistence:** File-based only (`coverage-trend-history.ndjson` per `coverage_guard.py` L23). No SQLite/Postgres.

## 6. External inputs and dependencies

GitHub Actions and secrets (`README.md` L141–147) drive all automation. Reusable workflows come from `stranske/Workflows@main` (`ci.yml` L34). Local dev needs Python ≥3.12 (`pyproject.toml` L10) with pytest/ruff/mypy (`pyproject.toml` L26–31). Workflow-only LangChain pins live in `tools/requirements-llm.txt` L10–15. commercial AI coding assistant CLI runs via Workflows reusables in the `agent-standard` environment (`README.md` L88–91, L153–154). No public market-data APIs, filings fetchers, or PDF parsers appear in any staging `src/`. `tools/embedding_provider.py` exists as fleet tooling without a staging `src/` caller.

## 7. Current state

Template and Ready enforce 80% coverage on `src/` (`pyproject.toml` L58). Gate runs on PRs; push CI on `main` (`ci.yml` L26–28). WIT runs four CI matrices plus daily cron (`ci.yml` L6–7).

**Usable:** CI, Gate, agent workflows (with secrets). **Prototype:** `src/` placeholder code. **Not wired:** research backplane emission.

**Key gaps:** (1) no `run.json` emitter (`backplane-conformance.yml` L54–55); (2) Template lacks `coverage-baseline.json` while Gate uses empty `coverage-min` (`pr-00-gate.yml` L203) vs Ready's `"80"` (`test_coverage_baseline.py` L56–78); (3) README/Python version mismatch (`README.md` L7 vs `pyproject.toml` L10); (4) `Issues.txt` references absent `main.py` (L37–38); (5) WIT README cites missing `tools.integration_repo` (`README.md` L17); (6) WIT baseline uses `coverage` not `line` (`config/coverage-baseline.json` L2); (7) WIT retains legacy agent workflows; (8) Gate bootstrap warning (`pr-00-gate.yml` L5–10).

## 8. Claims vs reality

- **Python 3.11+** claimed (`README.md` L7); `pyproject.toml` requires ≥3.12 (L10).
- **`agents-keepalive-loop.yml` as current architecture** (`README.md` L69–76); Template uses `agents-81-gate-followups.yml` (L290–301).
- **Ready README title “Template”** (`Ready/README.md` L1) despite Ready-specific baseline section (L78–91).
- **`python -m tools.integration_repo` in WIT** (`Workflows-Integration-Tests/README.md` L17); module absent from WIT `tools/`.
- **`run-contract/v1` participation** (`run-contract-v1.md` L15–16); no `config/backplane_participants.json` in any staging repo.
- **`Issues.txt` creates `main.py`** (L37–38); only `src/my_project/__init__.py` exists.

## 9. Interoperability hooks (for the fleet program)

**Offer:** known-good consumer workflow bundle (`docs/SETUP_CHECKLIST.md`); contract schemas in `docs/contracts/`; validator (`scripts/validate_run_contract.py`); LLM config shape (`config/llm_slots.json`); agent issue format (`docs/AGENT_ISSUE_FORMAT.md`); WIT as live `reusable-10-ci-python.yml` probe.

**Consume:** Workflows reusables; future `run-contract/v1` and `evidence-object/v1` instances; canonical entity IDs per `identity-map-conventions.md`.

**Collision risks:** placeholder package names `my_project`/`example`; WIT `coverage` vs Ready `line` baseline keys; identity authority assumed in Manager-Database/Pension-Data (`identity-map-conventions.md` L34–40) while staging repos emit no `identity_refs`.

## 10. Reuse candidates

- `scripts/validate_run_contract.py` — offline envelope conformance.
- `tools/coverage_guard.py` + `tools/coverage_trend.py` — baseline breach pattern.
- `tools/llm_registry.py` + `tools/langchain_client.py` — slot-based model routing.
- `docs/contracts/schemas/*.schema.json` — portable fleet contracts.
- `design-system/tokens.css` — shared visual tokens.
- `Ready/tests/test_coverage_baseline.py` — CI/baseline alignment guard.
- `Workflows-Integration-Tests/.github/workflows/ci.yml` — multi-matrix regression harness.

## 11. Proposed direction (evidence-based)

**Finish scaffolded:** align README keepalive/Python-version text; fix `Issues.txt` layout; rename Ready README header; normalize WIT baseline key or document divergence; remove stale WIT `integration_repo` instruction.

**New capability:** add `config/backplane_participants.json` + emitter when opting into backplane; decide Template vs Ready baseline policy; migrate WIT off legacy agent workflows; confirm agent registry limits (`.github/agents/registry.yml` L92 TODO).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- These three repositories are **infrastructure templates**, not research tools—they standardize automated testing and AI-assisted development for new Python projects.
- **Template** starts new repos; **Ready** is the “does everything still work?” canary; **Workflows-Integration-Tests** checks the shared CI system from the outside.
- Automation logic lives mainly in a separate **Workflows** repository—fix agent behavior there, not in synced copies here.
- Investment “run record” and evidence contracts are **documented but not yet produced** by staging repos.
- Agent automation requires administrator setup of secrets, environments, and branch protection before it will run reliably.
*Evidence-checked against source repositories; verification metadata omitted from work bundle.*
