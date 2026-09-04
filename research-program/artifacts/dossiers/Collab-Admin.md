# Collab-Admin — dossier (2026-09-04)

## 1. Purpose in one paragraph

Collab-Admin is a governance and instrumentation repository for a collaboration: policies, rubrics, submission templates, review workflows, time/expense tracking, dashboards, and validation scripts (`README.md` lines 3–15). Configuration declares four workstreams: Trend_Model_Project, Agent Integration, Consumer Usability, and Marketplace Plan (`config/project.yml` lines 14–22). It is not an investment-research engine. Work moves Issue → PR → reviewed artifact; month 1 uses collaborator forks and Tim is sole merger (`docs/01-operating-model.md` lines 5–23). Trend understanding deliverables prohibit AI assistance (`docs/09-trend-review-protocol.md` lines 1–8). Thin caller automation uses `stranske/Workflows` as source of truth (`docs/14-workflows-ecosystem.md` lines 5–10).

## 2. Who uses it and how (surfaces)

| Surface | Entry point | Who uses it | Status (evidence) |
|---------|-------------|-------------|-------------------|
| CLI — log validators | `scripts/validate_time_log.py`, `validate_expense_log.py`, `validate_friction_log.py` | Collaborator, CI | **Working with scope limits** — time validation checks seven columns, category values, optional GitHub-shaped links, and 40-hour ISO-week caps; CI invokes all three families (`validate_time_log.py` lines 16–114; `ci_admin.yml` lines 65–139). |
| CLI — rubric/config validators | `scripts/validate_rubrics.py`, `validate_config.py` | CI, local dev | **Working** — CI calls both; rubric validation checks basic fields on non-index YAML, not index linkage (`ci_admin.yml` lines 12–60; `validate_rubrics.py` lines 11–12, 45–62). |
| CLI — submission/review helpers | Packet, review-record, revision-issue, and month-end scripts | Collaborator, reviewer | **Partial** — packet validation has tests, but no workflow invokes either packet validator. |
| CLI — trend memo validator | `scripts/validate_trend_references.py` | Trend author | **Working** — parses categorized `path#Lx-Ly` references and minima (`validate_trend_references.py` lines 24–66, 113–178). |
| CLI — static dashboard builder | `scripts/build_static_dashboard.py` | Owner, scheduled automation | **Partial** — code and tests exist, but scheduled workflow writes only a heading/timestamp (`build_static_dashboard.py` lines 543–669; `build_dashboard.yml` lines 20–24). |
| CLI — ecosystem reporter | `scripts/collect_ecosystem_status.py` | Owner | **Working** — collects reusable-workflow references and agent-PR state (`collect_ecosystem_status.py` lines 1–9, 65–160). |
| CLI — backplane contract validator | `scripts/validate_run_contract.py` | Future opt-in conformance | **Partial** — code/schemas are present, but clone has no local registry, emitter, or fixtures; opt-in depends on a supplied registry (`validate_run_contract.py` lines 7–18, 192–204, 308–389). |
| Streamlit UI | `streamlit_app/app.py`, `review_console.py`, `github_client.py` | Owner running locally | **Working locally; external data conditional** — renders logs/reviews/charts and invokes YAML console; GitHub results depend on API success (`app.py` lines 454–665; `review_console.py` lines 72–105). |
| Static markdown artifact | `dashboards/public/dashboard.md` | Private-repo readers | **Scaffold** — numeric scoring is forbidden and committed dashboard is only a timestamp (`dashboards/public/README.md` lines 1–4; `dashboard.md` lines 1–3). |
| GitHub Actions automation | Gate, admin CI, agent workflows, autofix | Contributors via PR | **Working** — Gate calls Workflows reusable Python CI; clone contains 37 workflow files, not 40+ (`pr-00-gate.yml` lines 62–79). |
| YAML review artifacts | `reviews/YYYY-MM/pr-<n>.yml` | Reviewer | **Scaffold** — format documented; no review record is present beyond README (`reviews/README.md` lines 3–37). |
| CSV log artifacts | `logs/time/`, `logs/expenses/`, `logs/friction/` | Collaborator | **Scaffold** — tracked templates and `.gitkeep`; live CSVs ignored (`.gitignore` lines 34–41). |
| Python package | `src/my_project/__init__.py` | CI coverage gate | **Scaffold** — only `greet`/`add`; distribution is `collab-admin` while Ruff's first-party name is `collab_admin` (`src/my_project/__init__.py` lines 1–29; `pyproject.toml` lines 6–11, 88–90). |

## 3. Structure map

```
Collab-Admin/
├── config/            # project, dashboard, model configuration
├── docs/contracts/    # copied Workflows contract specifications/schemas
├── rubrics/           # review rubrics and index
├── templates/         # submission and review templates
├── scripts/           # validators, reports, agent helpers
├── streamlit_app/     # local dashboard and review console
├── dashboards/public/ # committed markdown output
├── logs/              # ignored live CSVs and tracked templates
├── reviews/           # review records
├── tools/             # packaging, LLM registry, CI utilities
└── .github/           # CI and agent/thin-caller workflows
```

## 4. Major code features you must understand to extend it

- **Time log validation** checks header, category enum, optional GitHub-shaped artifact links, date range, and 40-hour ISO-week total. It does not require an artifact link, and Streamlit does not call it (`scripts/validate_time_log.py` lines 16–114; `streamlit_app/app.py` lines 458–480).
- **Rubric gate** parses `rubrics/*.yml` and checks required fields on non-index entries; it does not validate `rubric_index.yml` links (`scripts/validate_rubrics.py` lines 11–12, 45–62).
- **Submission packet linter** parses required labelled fields from a file or PR description but has no workflow invocation in this clone (`scripts/validate_submission_packet.py` lines 20–97; `scripts/validate_submission_packet_pr.py` lines 17–22).
- **Review lifecycle** supports stub creation, monthly review storage, and revision issue creation when review YAML changes (`reviews/README.md` lines 20–37; `auto-revision-issues.yml` lines 1–13, 98–112).
- **Dashboard builders** aggregate time/review/CI/ecosystem inputs; Streamlit renders local data and a YAML-producing review console (`build_static_dashboard.py` lines 543–669; `app.py` lines 454–665; `review_console.py` lines 72–105).
- **Month-end compiler** reads month-specific time, expense, and review inputs and writes `logs/month_end/YYYY-MM.md` (`generate_month_end.py` lines 204–255).
- **Trend citation linter** checks categorized `path#Lx-Ly` references and minimum counts (`validate_trend_references.py` lines 24–66, 113–178).
- **Agent automation components** invoke local `scripts/langchain`/`runner_lib` helpers. Registry code reads LLM slot and registry JSON, but source evidence does not establish that every workflow uses that registry for runtime model selection (`agents-80-pr-event-hub.yml` lines 324–437; `autofix.yml` lines 511–582; `tools/llm_registry.py` lines 1–28).
- **Backplane validator** is role-aware and takes a registry at execution time; local caller has no emitter (`validate_run_contract.py` lines 7–18, 308–389; `backplane-conformance.yml` lines 25–58).

## 5. Data model, identifiers and contracts

**Identifiers.** Configuration defines workstream IDs/names. Reviews conventionally use `reviews/YYYY-MM/pr-<n>.yml`; time rows require date, hours, repo, issue-or-PR, category, description, and artifact link (`config/project.yml` lines 14–22; `reviews/README.md` lines 3–31; `validate_time_log.py` lines 16–24). It is inaccurate to claim manager/fund/pension identifiers are absent: copied identity conventions contain them (`identity-map-conventions.md` lines 19–40, 81–106).

**Persistence.** Local artifacts are YAML, Markdown, CSV, and JSON. No SQLite or PostgreSQL configuration was found; live logs and month-end outputs are ignored while templates are tracked (`.gitignore` lines 34–41).

**Versioning.** Review convention is one YAML per PR and month-end writes a named file per requested month (`reviews/README.md` lines 3–18; `generate_month_end.py` lines 204–255). Contract schema versions are explicit. Exclusive Git-history supersession is not established by local evidence.

**Shipped contracts (`docs/contracts/`).**

| Contract | Emitter in this clone | Consumer in this clone |
|----------|-----------------------|------------------------|
| `run-contract-v1.md` + schema | No local emitter or registry | Validator, given a registry and documents |
| `evidence-object-v1.schema.json` | None found | Validator maps token to schema |
| `artifact-manifest-v1.schema.json` | None found | Validator cross-checks manifest for producer/bridge |
| `identity-map-conventions.md` | None | Convention-only ingest token |
| `capability-bundle-v1.md` + schema | None found | Documentation/schema only; no script import found |
| `agent-runner-output.md` | N/A: Workflows-runner spec | No direct local workflow reference found |

## 6. External inputs and dependencies

Human inputs are PR packets, CSV logs, and review YAML. Streamlit uses `requests` for GitHub data; CI and agents run in GitHub Actions. Python dependencies include Streamlit, pandas, Altair, PyYAML, and requests (`pyproject.toml` lines 24–39). Workflows callers reference `stranske/Workflows` at `main` (`pr-00-gate.yml` lines 62–79; `backplane-conformance.yml` lines 53–58). Registry helpers exist locally, but deployed model-selection behavior was not verified.

## 7. Current state

The clone collects 98 pytest tests, but `pytest --collect-only` still fails its 80% coverage threshold afterward; this does not establish a passing suite (`pyproject.toml` lines 48–65). Policies, rubrics, validators, local Streamlit, revision-issue automation, and agent helpers are usable source components. Material gaps are timestamp-only static output, absent local backplane registry/emitter/fixtures, template-package naming drift, and stale `Issues.txt` workflow text. No inspected workflow enforced the no-AI configuration rule.

## 8. Claims vs reality

- **README dashboard-generation claim** is not met by the local scheduled workflow: it writes only `# Dashboard` and a UTC timestamp, while the fuller builder is not invoked (`README.md` lines 93–107; `build_dashboard.yml` lines 20–24; `build_static_dashboard.py` lines 543–669).
- **Static Dashboard P4** is complete only as “Basic”; the checklist retains a TODO for content beyond timestamp (`ADMIN_SETUP_CHECKLIST.md` lines 79–82). That is qualified incompleteness, not an unqualified false-completion claim.
- **Run-contract docs do not promise local Collab-Admin fixtures/registry.** They assign registry, validator, fixtures, and reusable workflow to Workflows (`run-contract-v1.md` lines 24–32). Missing local copies make this clone unwired, not a refutation of that ownership model.
- **Gate and admin CI are separate.** Gate calls reusable Python CI and does not invoke `ci_admin.yml`, whose triggers are independent (`pr-00-gate.yml` lines 62–79; `ci_admin.yml` lines 1–7).
- **Submission packets are policy-required but manually enforced here.** The operating model expects them; no workflow invocation of the packet validators was found (`docs/01-operating-model.md` lines 5–10; `validate_submission_packet.py` lines 20–97).
- **`Issues.txt` is stale about revision workflow copy status.** It says copy is blocked, while `.github/workflows/auto-revision-issues.yml` exists and invokes the script (`Issues.txt` lines 64–81; `auto-revision-issues.yml` lines 1–13, 98–112).

## 9. Interoperability hooks (for the fleet program)

**Offers:** local workstream/deliverable presentation, rubrics, submission/review templates, validators, ecosystem status collection, and copied contract schemas (`app.py` lines 19–48; `collect_ecosystem_status.py` lines 1–26; `docs/contracts/schemas/`).

**Consumes:** active reusable Workflows callers. Cross-repo smoke and reference packs are optional rather than currently configured: no `.github/reference_packs.json` exists and smoke requires repository variables (`cross-repo-smoke.yml` lines 1–45; `reference_packs.py` lines 16–18, 55–72). Backplane documentation and canonical-ID conventions are opt-in; this clone is not locally registered (`run-contract-v1.md` lines 15–17; `identity-map-conventions.md` lines 94–106).

**Collision risks:** repo-local PR/issue numbers and rubric-vs-domain semantics are reasonable concerns, but no cited source defines or tests a fleet collision model. Treat these as hypotheses pending cross-repository evidence.

## 10. Reuse candidates

| Component | Path |
|-----------|------|
| CSV validators | `scripts/validate_time_log.py`, `validate_expense_log.py`, `validate_friction_log.py` |
| Rubric structural checker | `scripts/validate_rubrics.py` |
| Submission packet parser | `scripts/validate_submission_packet.py` |
| Static markdown dashboard builder | `scripts/build_static_dashboard.py` |
| Review follow-up automator | `scripts/create_revision_issues.py` |
| Trend reference linter | `scripts/validate_trend_references.py` |
| Ecosystem collector | `scripts/collect_ecosystem_status.py` |
| Streamlit YAML review generator | `streamlit_app/review_console.py` |
| LLM registry utility | `tools/llm_registry.py` |
| State fingerprint helper | `scripts/state_fingerprint.py` |
| Backplane validator | `scripts/validate_run_contract.py` |

## 11. Proposed direction (evidence-based)

Wire the static builder into the scheduled dashboard workflow; add packet validation to a PR workflow; reconcile `Issues.txt` and the checklist with the existing revision workflow; and resolve package naming. Add a local backplane registry, fixtures, and emitter only if this repo is deliberately made a participant. Verify model-selection integration before treating the registry helpers as active governance control.

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- This is the collaboration’s rulebook and review scaffold, not an investment-analysis system.
- Work is designed around forked pull requests, owner-controlled merging, and review artifacts.
- The owner dashboard is local; GitHub visibility depends on available API access.
- Heavy automation comes from shared workflows through callers.
- Static dashboard and backplane integration are incomplete, so generic green CI is not end-to-end evidence.

Verified 2026-09-04T15:55:23Z by Codex: 36 claims checked, 9 corrected, 2 unverifiable
