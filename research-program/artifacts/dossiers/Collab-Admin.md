# Collab-Admin — dossier (2026-09-04)

## 1. Purpose in one paragraph

Collab-Admin is the **governance and instrumentation control plane** for a fixed-term collaboration between Tim (repo owner/merger) and an external collaborator working across four defined workstreams: trend-model clarity, agent integration, consumer-repo usability, and marketplace planning (`README.md` lines 3–13, `config/project.yml` lines 14–22). It does not run investment research, parse filings, or score managers. Instead it holds the operating policies (`docs/00-charter.md` through `docs/14-workflows-ecosystem.md`), rubrics, submission and review templates, time/expense/friction log schemas, validation scripts, and dashboards that make paid collaboration auditable on GitHub. The design constraint is **PR-only, fork-first, secrets-light work**: month 1 is forks-only with no banking (`config/project.yml` lines 10–12; `docs/01-operating-model.md` lines 11–18), the Trend workstream forbids AI assistance (`config/project.yml` line 13; `docs/09-trend-review-protocol.md` lines 5–7), and automation delegates heavy lifting to the shared `stranske/Workflows` repo via thin GitHub Actions callers (`docs/14-workflows-ecosystem.md` lines 5–9).

## 2. Who uses it and how (surfaces)

| Surface | Entry point | Who uses it | Status (evidence) |
|---------|-------------|-------------|-------------------|
| CLI — log validators | `scripts/validate_time_log.py`, `validate_expense_log.py`, `validate_friction_log.py` | Collaborator, owner at month-end | **Working** — schema + weekly 40h cap enforced (`validate_time_log.py` lines 16–24, 31–35); invoked in `ci_admin.yml` lines 65–91 |
| CLI — rubric/config validators | `scripts/validate_rubrics.py`, `validate_config.py` | CI, local dev | **Working** — called from `ci_admin.yml` lines 12–60 |
| CLI — submission/review helpers | `scripts/validate_submission_packet.py`, `create_review_record.py`, `create_revision_issues.py`, `generate_month_end.py` | Collaborator, reviewer | **Partial** — scripts exist and have tests (`tests/scripts/test_validate_submission_packet.py`); submission validation **not** wired into any workflow (grep shows no CI reference) |
| CLI — trend memo validator | `scripts/validate_trend_references.py` | Trend workstream author | **Working** — reference-format parser with category rules (`validate_trend_references.py` lines 24–40) |
| CLI — static dashboard builder | `scripts/build_static_dashboard.py` | Owner, scheduled automation | **Partial** — full aggregator implemented and tested (`tests/scripts/test_build_static_dashboard.py`); **not** called by `build_dashboard.yml` (workflow writes timestamp only, lines 21–24) |
| CLI — ecosystem reporter | `scripts/collect_ecosystem_status.py` | Owner | **Working** — scans `.github/workflows` for reusable-workflow refs (`collect_ecosystem_status.py` lines 1–8, 24–26) |
| CLI — backplane contract validator | `scripts/validate_run_contract.py` | Fleet conformance CI | **Partial** — validator implemented (`validate_run_contract.py` lines 1–18); no `config/backplane_participants.json`, no `emit_reference_run.sh`, no fixture dir despite doc references |
| Streamlit UI | `streamlit_app/app.py` (+ `review_console.py`, `github_client.py`) | Owner (local) | **Working** — time charts, review loading, GitHub Issues/PRs/CI, review YAML writer (`app.py` lines 454–665; tests in `tests/streamlit_app/`) |
| Static markdown artifact | `dashboards/public/dashboard.md` | Shared read-only view in private repo | **Scaffold** — README forbids numeric scoring (`dashboards/public/README.md` lines 1–4); committed file is only a timestamp (`dashboard.md` lines 1–3) |
| GitHub Actions automation | `.github/workflows/pr-00-gate.yml`, `ci_admin.yml`, `agents-*.yml`, `autofix.yml` | All contributors via PR | **Working** — Gate delegates Python CI to Workflows (`pr-00-gate.yml` lines 62–79); 40+ workflow files present |
| YAML review artifacts | `reviews/YYYY-MM/pr-<n>.yml` per `reviews/README.md` | Reviewer | **Scaffold** — format documented (`reviews/README.md` lines 20–31); directory empty except README |
| CSV log artifacts | `logs/time/`, `logs/expenses/`, `logs/friction/` | Collaborator | **Scaffold** — template at `logs/time_log_template.csv`; `logs/time/` empty (`.gitkeep` only) |
| Python package (installable) | `src/my_project/__init__.py` | CI coverage gate | **Scaffold** — template `greet`/`add` only (`src/my_project/__init__.py` lines 7–29); package name in `pyproject.toml` is `collab-admin` but code lives under `my_project` |

## 3. Structure map

```
Collab-Admin/
├── config/           # project.yml workstreams, dashboard_public.yml, LLM slot/registry JSON
├── docs/             # charter, operating model, security, workstream protocols (00–14)
│   └── contracts/    # run-contract, evidence-object, capability-bundle specs + JSON schemas
├── rubrics/          # YAML rubric packs indexed by rubric_index.yml
├── templates/        # submission_packet.md, review_record.yml, workflow templates
├── scripts/          # validators, dashboard builders, month-end, langchain agent helpers
│   ├── langchain/    # issue optimizer, verifier, dedup, decomposer (used by agents-*.yml)
│   └── runner_lib/   # shared agent-runner prompt/dispatch utilities
├── streamlit_app/    # local dashboard + review console
├── dashboards/public/# committed markdown dashboard output
├── logs/             # time/expense/friction CSV templates and month-end memos (.gitignored data)
├── reviews/          # git-tracked YAML review records
├── tools/            # pep517 backend, LLM registry, CI triage helpers
├── tests/            # 98 pytest cases for scripts, streamlit, template package
├── design-system/    # shared UI tokens (synced from stranske/Workflows per design-system/README.md)
├── .github/          # workflows, agents registry, codex prompts (mostly synced from stranske/Workflows)
└── node_modules/     # Octokit deps for .github scripts (vendored; skip for architecture)
```

## 4. Major code features you must understand to extend it

- **Time log validation** — `scripts/validate_time_log.py` enforces seven-column CSV schema, categories, GitHub links, and 40h ISO-week caps; consumed by `ci_admin.yml` and `streamlit_app/app.py`.
- **Rubric gate** — `scripts/validate_rubrics.py` checks `rubrics/*.yml` structure against `rubric_index.yml`; anchors the review standard.
- **Submission packet linter** — `scripts/validate_submission_packet.py` / `validate_submission_packet_pr.py` verify PR markdown sections; **not wired to CI**.
- **Review lifecycle** — `create_review_record.py` → `reviews/YYYY-MM/pr-N.yml` → `create_revision_issues.py`, triggered by `auto-revision-issues.yml`.
- **Dashboard builders** — `build_static_dashboard.py` aggregates logs, reviews, CI NDJSON, ecosystem JSON into markdown; Streamlit `app.py` adds live charts and `review_console.py` YAML writer.
- **Month-end compiler** — `generate_month_end.py` joins time, expense, and review inputs per `docs/08-month-end-settlement.md`.
- **Trend citation linter** — `validate_trend_references.py` enforces `path#Lx-Ly` references per `docs/09-trend-review-protocol.md`.
- **Agent automation layer** — `scripts/langchain/*` plus `runner_lib/core.py` power `agents-*.yml` workflows; model picks from `tools/llm_registry.py` and `config/llm_slots.json`.
- **Backplane validator** — `validate_run_contract.py` checks `run-contract/v1` and satellite schemas; skips when `config/backplane_participants.json` is absent.

## 5. Data model, identifiers and contracts

**Identifiers.** Workstream ids (`ws1_trend`…`ws4_marketplace`) and names in `config/project.yml`; reviews keyed by `pr_number` at `reviews/YYYY-MM/pr-<n>.yml` (`reviews/README.md`); rubrics by YAML stem; time rows by date/repo/issue_or_pr (`validate_time_log.py` `REQUIRED`). No manager/fund/pension IDs here — those belong to siblings (`identity-map-conventions.md`).

**Persistence.** File-only: git-tracked YAML/Markdown/CSV and JSON configs; no SQLite/Postgres. Live collaborator logs are gitignored (`README.md` line 53).

**Versioning.** One review file per PR; one month-end memo per `YYYY-MM`; contract docs carry `schema_version`; supersession is git history only.

**Shipped contracts (`docs/contracts/`).**

| Contract | Emitter in this repo | Consumer in this repo |
|----------|---------------------|----------------------|
| `run-contract-v1.md` + schema | **None** — doc states "No participant emits an envelope yet" (`run-contract-v1.md` lines 15–17) | `scripts/validate_run_contract.py` (validator only) |
| `evidence-object-v1.schema.json` | **None** | Validator via `INGEST_SCHEMA_FILES` in `validate_run_contract.py` lines 45–48 |
| `artifact-manifest-v1.schema.json` | **None** | Same validator manifest cross-check |
| `identity-map-conventions.md` | **None** | Convention-only ingest token (`INGEST_CONVENTION_ONLY` line 52) |
| `capability-bundle-v1.md` + schema | **None** | **Documented only** — no Collab-Admin script imports capability-bundle schema |
| `agent-runner-output.md` | **N/A (spec for Workflows runners)** | Referenced by agent workflows; outputs produced in GitHub Actions, not local Python |

## 6. External inputs and dependencies

| Category | Details |
|----------|---------|
| Human inputs | PR descriptions using `templates/submission_packet.md`; CSV time/expense/friction logs; YAML review records |
| GitHub | REST API via `requests` in `streamlit_app/github_client.py` (`GITHUB_API` line 12); Actions for all CI/agent automation; requires secrets listed in `README.md` lines 135–141 (`CODEX_AUTH_JSON`, app tokens, PATs) |
| stranske/Workflows | Reusable workflows at `@main` for Gate CI, keepalive, autofix, verifier, backplane conformance (`ci.yml` line 28, `backplane-conformance.yml` line 55) |
| LLM / agents | LangChain-style modules under `scripts/langchain/`; model registry in `config/model_registry.json` and `tools/llm_registry.py`; optional `tools/requirements-llm.txt` |
| Python stack | `pyproject.toml`: Streamlit, pandas, Altair, PyYAML, requests; dev: pytest, ruff, mypy, black |
| Node (limited) | `node_modules/@octokit/*` for GitHub App scripts under `.github/scripts` |
| Install vs file-only | Validators and Streamlit run locally after `pip install -e ".[dev]"` (`README.md` lines 117–124). No Docker compose or server deployment for the governance app itself. Agent automation requires GitHub-hosted runners and external CLI agents (Codex, Claude Code). |

No PDF/DOCX parsing, no Excel integration, no embeddings pipeline in this repo (embedding helper exists in `tools/embedding_provider.py` for Workflows tooling, not Collab-Admin business logic).

## 7. Current state

**Test/CI posture.** 98 pytest cases; 80% coverage gate on `src/my_project` template (`pyproject.toml` lines 48–50, 65). **Gate** (`pr-00-gate.yml` lines 62–78) runs Workflows Python CI; **collab-admin-ci** (`ci_admin.yml`) validates rubrics/logs/docs in parallel. Backplane conformance is opt-in no-op (`backplane-conformance.yml` lines 40–46).

**Usable now:** policies, rubrics, log validators, local Streamlit, agent workflows, revision-issue automation.

**Scaffold:** template package, empty review/time data, timestamp-only static dashboard, no `run.json` emission, submission packet not in CI.

**Top gaps:** static dashboard not using `build_static_dashboard.py` (`ADMIN_SETUP_CHECKLIST.md` line 82; `build_dashboard.yml` lines 21–24); no `backplane_participants.json` (`run-contract-v1.md` lines 15–17); missing backplane fixtures (`validate_run_contract.py` line 412); `my_project` vs `collab_admin` naming drift (`pyproject.toml` line 89); stale `Issues.txt` / checklist on revision workflow (lines 72–81 vs existing `auto-revision-issues.yml`); fork secret limits (`docs/01-operating-model.md` lines 17–18); trend no-AI policy not machine-enforced (`config/project.yml` line 12).

## 8. Claims vs reality

- **README "Automated dashboard generation from review data"** (`README.md` line 99) vs **`build_dashboard.yml` writes only `# Dashboard` + UTC timestamp** (lines 21–24) while `scripts/build_static_dashboard.py` (670 lines) is unused in CI.
- **`docs/ADMIN_SETUP_CHECKLIST.md` Phase P4 marked ✅** (lines 79–82) but same doc lists **TODO: Enhance static dashboard content beyond timestamp** — partial at best.
- **`docs/contracts/run-contract-v1.md` "validator, fixtures"** (lines 27–28) vs **no `tests/fixtures/backplane/` and no participant registry file** in repo.
- **`README.md` repository structure lists `ci_admin.yml` and Gate as key workflows** but **`pr-00-gate.yml` does not invoke `ci_admin.yml`** — admin validations are a separate PR workflow; easy to miss if only watching Gate status.
- **`templates/submission_packet.md` required on every PR** (`docs/01-operating-model.md` line 9) vs **`validate_submission_packet.py` not referenced in any `.github/workflows/*.yml`** — compliance is manual.
- **`Issues.txt` claims workflow copy blocked** (lines 72–81) vs **`auto-revision-issues.yml` already present** in `.github/workflows/` — queue file is stale.

## 9. Interoperability hooks (for the fleet program)

**Offers:** workstream/deliverable checklists (`config/project.yml`, `streamlit_app/app.py` `WORKSTREAM_DELIVERABLES`); rubric packs (`rubrics/`); submission/review templates; friction-log and trend-citation validators; ecosystem status JSON (`collect_ecosystem_status.py`); hosted contract schema copies (`docs/contracts/schemas/`).

**Consumes:** Workflows reusable workflows; sibling repos via `reference_packs.py` / `cross-repo-smoke.yml`; future `run-contract/v1` and `evidence-object/v1` inputs if registered; canonical entity IDs from Manager-Database/Pension-Data per `identity-map-conventions.md`.

**Collision risks:** repo-local PR/issue numbers; workstream name `Trend_Model_Project` vs repo `Trend_Model`; time-log `category` enums vs investment taxonomies; rubric levels are review grades, not fund scores.

## 10. Reuse candidates

| Component | Path |
|-----------|------|
| CSV time/expense/friction validators | `scripts/validate_time_log.py`, `validate_expense_log.py`, `validate_friction_log.py` |
| Rubric YAML schema checker | `scripts/validate_rubrics.py` |
| Submission packet markdown linter | `scripts/validate_submission_packet.py` |
| Static markdown dashboard builder | `scripts/build_static_dashboard.py` |
| Review follow-up issue automator | `scripts/create_revision_issues.py` |
| Trend memo reference linter | `scripts/validate_trend_references.py` |
| Workflows ecosystem scanner | `scripts/collect_ecosystem_status.py` |
| Streamlit review YAML console | `streamlit_app/review_console.py` |
| LLM slot/registry resolution | `tools/llm_registry.py` + `config/llm_slots.json` |
| Workflow state fingerprint gate | `scripts/state_fingerprint.py` |
| Backplane run-contract validator | `scripts/validate_run_contract.py` |

## 11. Proposed direction (evidence-based)

**Finish scaffolded:** wire `build_static_dashboard.py` into `build_dashboard.yml`; add submission-packet check to Gate/`ci_admin.yml`; add backplane fixtures/registry if this repo should gate contracts; fix `my_project`/`collab_admin` naming; refresh stale `Issues.txt` and checklist.

**New capability:** optional governance `run.json` if joining backplane as bridge; machine-check trend no-AI attestation; fold ecosystem status into static dashboard (`docs/13-project-instrumentation-roadmap.md` lines 27–34).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- This repository is the **rulebook and scoreboard** for a paid GitHub collaboration—not a tool that analyzes investments or managers.
- All real work still happens in other repositories; this one defines how submissions, reviews, time logs, and rubrics must look before Tim merges a pull request.
- Day-to-day visibility for the owner is a **local Streamlit dashboard** plus a **markdown status page** meant for sharing inside the private repo without exposing numeric grades.
- Heavy automation (testing pull requests, running coding agents, auto-fixing lint) is borrowed from a shared **Workflows** repository; Collab-Admin mostly contains configuration and documentation that points at it.
- Several "done" checklist items are **visually complete but thin**—especially the public dashboard and research backplane run records—so treat green CI as necessary but not sufficient for operational completeness.
