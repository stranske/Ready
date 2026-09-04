# Collab-Admin dossier verification

Scope: adversarial source check of every claim in dossier sections 4, 5, 8, and 9 against `clones/Collab-Admin`. “Unverifiable” means cited local evidence does not establish the proposition; it does not prove it false.

| # | Section | Claim checked | Result | Evidence / correction |
|---:|---|---|---|---|
| 1 | 4 | Time validator requires seven columns, categories, GitHub links, 40h cap, and is consumed by CI and Streamlit. | WRONG | Checks seven columns, category values, optional GitHub-shaped links, and cap; CI invokes it, Streamlit does not. `scripts/validate_time_log.py:16-114`; `ci_admin.yml:65-91`; `streamlit_app/app.py:458-480`. |
| 2 | 4 | Rubric gate checks structure against `rubric_index.yml`. | WRONG | It skips index structure and validates non-index files. `scripts/validate_rubrics.py:11-12,45-62`. |
| 3 | 4 | Packet helpers validate fields and are not wired into CI. | CONFIRMED | Parser is implemented; no workflow reference was found. `scripts/validate_submission_packet.py:20-97`; `scripts/validate_submission_packet_pr.py:17-22`. |
| 4 | 4 | Review records feed revision-issue creation through a workflow. | CONFIRMED | Workflow filters review YAML and runs creator. `reviews/README.md:20-37`; `.github/workflows/auto-revision-issues.yml:1-13,98-112`. |
| 5 | 4 | Static builder aggregates inputs; Streamlit provides charts and YAML console. | CONFIRMED | `scripts/build_static_dashboard.py:543-669`; `streamlit_app/app.py:454-665`; `streamlit_app/review_console.py:72-105`. |
| 6 | 4 | Month-end compiler combines time, expense, and review inputs. | CONFIRMED | `scripts/generate_month_end.py:204-255`. |
| 7 | 4 | Trend validator enforces categorized references and minima. | CONFIRMED | `scripts/validate_trend_references.py:24-66,113-178`. |
| 8 | 4 | All agent-workflow model choices come from registry/slot files. | WRONG | Helpers and registry defaults exist; universal runtime selection is not demonstrated. `agents-80-pr-event-hub.yml:324-437`; `autofix.yml:511-582`; `tools/llm_registry.py:1-28`. |
| 9 | 4 | Validator automatically skips when local registry is absent. | WRONG | It requires a registry argument and skips based on supplied entry/status; caller has no emitter. `scripts/validate_run_contract.py:7-18,308-389`; `.github/workflows/backplane-conformance.yml:25-58`. |
| 10 | 5 | Four workstream IDs/names are configured. | CONFIRMED | `config/project.yml:14-22`. |
| 11 | 5 | Reviews use one monthly `pr-<n>.yml` per PR. | CONFIRMED | `reviews/README.md:3-31`. |
| 12 | 5 | Time records require date/repo/issue-or-PR fields. | CONFIRMED | `scripts/validate_time_log.py:16-24`. |
| 13 | 5 | Rubrics are identified by YAML stem. | CONFIRMED | `streamlit_app/review_console.py:20-31`. |
| 14 | 5 | No manager/fund/pension identifiers are in repo. | WRONG | Copied identity conventions contain these IDs. `docs/contracts/identity-map-conventions.md:19-40,81-106`. |
| 15 | 5 | Persistence is file based; SQLite/PostgreSQL are not configured. | CONFIRMED | Ignored/log artifact model is file based; no database config found. `.gitignore:34-41`. |
| 16 | 5 | Live collaborator logs are ignored. | CONFIRMED | `.gitignore:34-41`. |
| 17 | 5 | Month-end writes one named memo per requested month. | CONFIRMED | `scripts/generate_month_end.py:204-255`. |
| 18 | 5 | Contract schemas carry explicit versions. | CONFIRMED | `scripts/validate_run_contract.py:32-52,210-218`. |
| 19 | 5 | Supersession is only Git history. | UNVERIFIABLE | No cited local source establishes an exclusive mechanism. |
| 20 | 5 | This clone emits no run-contract envelope. | CONFIRMED | No local registry/emitter; caller executes one only if added. `.github/workflows/backplane-conformance.yml:36-45`. |
| 21 | 5 | Validator consumes evidence-object schema. | CONFIRMED | `scripts/validate_run_contract.py:44-52,159-170`. |
| 22 | 5 | Validator cross-checks artifact manifests. | CONFIRMED | `scripts/validate_run_contract.py:210-252`. |
| 23 | 5 | Identity-map ingestion is convention-only. | CONFIRMED | `scripts/validate_run_contract.py:50-52,159-165`. |
| 24 | 5 | Capability-bundle schema is docs-only locally. | CONFIRMED | Doc/schema present; no script import found. `docs/contracts/capability-bundle-v1.md:1-12`; `docs/contracts/schemas/capability-bundle-v1.schema.json:1-19`. |
| 25 | 5 | Agent-runner contract is referenced by local agent workflows. | WRONG | It specifies external Workflows runners; no direct local workflow reference found. `docs/contracts/agent-runner-output.md:7-24`. |
| 26 | 8 | README promises dashboard generation while scheduled workflow writes timestamp. | CONFIRMED | `README.md:93-107`; `.github/workflows/build_dashboard.yml:20-24`. |
| 27 | 8 | P4 is fully complete despite a TODO. | WRONG | It is explicitly qualified “Basic” and retains TODO. `docs/ADMIN_SETUP_CHECKLIST.md:79-82`. |
| 28 | 8 | Contract docs promise local fixture/registry ownership. | WRONG | Docs assign them to Workflows. `docs/contracts/run-contract-v1.md:24-32`. |
| 29 | 8 | Gate and admin CI are separate. | CONFIRMED | `.github/workflows/pr-00-gate.yml:62-79`; `.github/workflows/ci_admin.yml:1-7`. |
| 30 | 8 | Submission packets are policy-required but manual here. | CONFIRMED | `docs/01-operating-model.md:5-10`; no workflow validator invocation found. |
| 31 | 8 | `Issues.txt` is stale about workflow copy. | CONFIRMED | `Issues.txt:64-81`; `.github/workflows/auto-revision-issues.yml:1-13,98-112`. |
| 32 | 9 | Repo offers local workstream/rubric/template/validator/status/schema components. | CONFIRMED | `streamlit_app/app.py:19-48`; `scripts/collect_ecosystem_status.py:1-26`; `docs/contracts/schemas/`. |
| 33 | 9 | It presently consumes siblings through reference packs and smoke tests. | WRONG | Mechanisms are optional/unconfigured: no config and smoke needs variables. `scripts/reference_packs.py:16-18,55-72`; `.github/workflows/cross-repo-smoke.yml:1-45`. |
| 34 | 9 | Future opt-in backplane and canonical-ID hooks exist. | CONFIRMED | `docs/contracts/run-contract-v1.md:15-17`; `docs/contracts/identity-map-conventions.md:94-106`. |
| 35 | 9 | Dossier collision risks are stated/tested fleet risks. | UNVERIFIABLE | Plausible but no local source models/tests them. |
| 36 | 9 | Rubric levels are not fund scores. | CONFIRMED | Review-rubric and domain-ID sources are distinct. `reviews/README.md:20-31`; `docs/contracts/identity-map-conventions.md:81-106`. |

Summary: 36 claims checked; 9 wrong claims corrected; 2 claims unverifiable.
