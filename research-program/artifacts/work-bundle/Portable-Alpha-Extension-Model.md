# Portable-Alpha-Extension-Model — dossier (2026-09-04)

Verification scope: source and documentation at repository commit `8ddf6be49b95a18b02cd83aeebc565e8177c967d`, inspected 2026-09-04. Implementation and configured CI are distinguished from runtime success; this audit did not execute the application, Windows package, browser path, or CI.

## 1. Purpose in one paragraph

Portable Alpha Extension Model (PAEM) is a Monte Carlo simulation tool for investment offices exploring **portable alpha** and **active extension** fund structures. It models how capital splits across benchmark exposure, external portable-alpha sleeves, active extension, and internal sleeves, then draws correlated monthly returns and financing paths to produce risk/return statistics (tracking error, CVaR, breach probability, shortfall probability, and related metrics). The primary audience is analysts and portfolio strategists who need scenario exploration without building spreadsheets from scratch. It was designed around **offline, local-first execution**: the deterministic engine runs without network access (`pa_core/tool_descriptor.py` declares `network.deterministic: "offline"`), with a Streamlit dashboard for non-developers and a portable Windows zip path for locked-down PCs. Proprietary index data is expected to stay inside the user's environment (Codespaces or on-prem); public SaaS hosting is explicitly discouraged in `README.md`.

## 2. Who uses it and how (surfaces)

| Surface | Entry point (file) | Who uses it | Status (evidence) |
|--------|-------------------|-------------|-------------------|
| CLI (`pa`, `pa-validate`, `pa-convert-params`) | `pa_core/pa.py`, `pa_core/validate.py`, `pa_core/data/convert.py` | Power users, automation, CI | **Implemented** — `pyproject.toml` registers console scripts; `README.md` documents `pa run --config … --index …`; integration test in `.github/workflows/pr-00-gate.yml` |
| Dashboard (Streamlit) | `dashboard/app.py`, `dashboard/pages/*.py` | Analysts, scenario exploration | **Implemented** — seven pages under `dashboard/pages/`; PR gate runs Streamlit health smoke (`.github/workflows/pr-00-gate.yml` ~L138) |
| Dashboard CLI launcher | `dashboard/cli.py` (`pa-dashboard`) | Same as dashboard | **Implemented** — registered in `pyproject.toml`; historical coverage report lists 0% (`docs/COVERAGE_GAPS.md:4,22`); current coverage was not measured |
| Browser / stlite entry point | `web/index.html:64-82,271-322` | Dashboard in browser, plus Plotly PNG export | **Implemented entry point; runtime unverified** — fetches app sources and mounts `dashboard/app.py` with stlite; the PNG helper is only one part. `README.md:19` still disclaims support; source presence does not establish a working work-environment deployment. |
| Excel / board-pack artifacts | `pa_core/reporting/excel.py`, `pa_core/viz/pptx_export.py` | Reporting, committee packs | **Implemented** — default output `Outputs.xlsx` (`pa_core/contracts.py` `DEFAULT_OUTPUT_FILENAME`); `--pptx`/`--pdf` flags in root `manifest.json` cli_args |
| Run bundles / manifests | `pa_core/manifest.py`, `pa_core/run_artifact_bundle.py` | Reproducibility, run comparison | **Implemented** — `manifest.json` at repo root is a sample; `RunArtifactBundle.save()` writes `bundle.json` with SHA-256 hashes (`pa_core/run_artifact_bundle.py` L59–72) |
| Packaging utilities | `scripts/make_portable_zip.py`, `scripts/create_launchers.py` | IT / desktop deployment | **Implemented** — `pa-make-zip`, `pa-create-launchers` in `pyproject.toml`; `Makefile` `portable-zip` target |

## 3. Structure map

```
pa_core/          Core simulation engine, CLI, agents, data import, reporting, optional LLM
dashboard/        Streamlit UI (wizard, results, stress lab, run logs)
config/           YAML/JSON parameter templates, model registry, LLM slot config
data/             Sample index CSV (e.g. sp500tr_fred_divyield.csv)
docs/             User guides, contracts (run-contract schemas), development notes
docs/contracts/   JSON Schemas + markdown for fleet interoperability (mostly documented, not emitted)
scripts/          Portable zip, launcher creation, run-contract validator
tests/            Pytest suite (current collection count not verified in this audit)
web/              stlite dashboard entry point and Plotly PNG bridge (runtime unverified)
tools/            CI triage utilities
.github/          CI and agent workflows; synced infrastructure plus a repo-specific custom gate
design-system/    UI tokens — boilerplate, not simulation logic
archive/          Retired configs and development logs
```

## 4. Major code features you must understand to extend it

- **Run facade and callers** — `pa_core/facade.py` (`run_single`, `run_sweep`, `export`) exposes programmatic entry points consuming `ModelConfig` + index `pd.Series` and producing returns and summary tables. CLI calls `run_single` (`pa_core/cli.py:1419`), and the Wizard invokes CLI (`dashboard/pages/3_Scenario_Wizard.py:2293-2302`). Not every dashboard path uses the facade: Scenario Grid directly calls `run_parameter_sweep_cached` (`dashboard/pages/5_Scenario_Grid.py:265-267`).
- **Agent / sleeve model** — `pa_core/agents/registry.py` maps names (`ExternalPA`, `ActiveExt`, `InternalPA`, `InternalBeta`, `Base`) to agent classes; `pa_core/simulations.py` `simulate_agents()` wires return/financing streams into per-sleeve paths and a Total overlay contribution.
- **Covariance and return draws** — `pa_core/sim/covariance.py` builds and PSD-projects covariance; `pa_core/sim/paths.py` and `draw_joint_returns` (imported in `pa_core/sweep.py`) produce correlated monthly shocks.
- **Parameter sweep engine** — `pa_core/sweep.py` `run_parameter_sweep()` grids `SweepConfig` parameters, reuses RNG substreams (`pa_core/random.py`), and consolidates numeric summary columns per `pa_core/contracts.py` `SUMMARY_*` fields.
- **Sleeve allocation optimizer** — `pa_core/sleeve_suggestor.py` searches capital weights across `SLEEVE_AGENTS` under TE/CVaR/breach constraints via `MultiObjectiveProblem` (`pa_core/multi_objective.py`); CLI flag `--suggest-sleeves`.
- **Configuration schema** — `pa_core/config.py` + `pa_core/schema.py` (Pydantic `Scenario`, `ModelConfig`) validate YAML; `Scenario.sleeves` is validated but explicitly unwired (`pa_core/schema.py` L155–160).
- **Data import and calibration** — `pa_core/data/importer.py` `DataImportAgent` and `pa_core/data/calibration.py` `CalibrationAgent` turn CSV/XLSX into monthly returns and μ/σ/ρ estimates (`pa_core/calibration.py`); CLI subcommands in `pa_core/pa.py`.
- **Reproducibility manifest** — `pa_core/manifest.py` `ManifestWriter.write()` records git commit, seed, config hash, and input file SHA-256s into `manifest.json`.
- **Run record envelope** — `pa_core/cli.py` `_write_run_record()` emits local `run.json` linking manifest, warnings, and cost stub (`pa_core/contracts.py` `RUN_RECORD_FILENAME`); distinct from fleet `run-contract/v1`.
- **Artifact bundle with integrity** — `pa_core/run_artifact_bundle.py` packages config, manifest, and outputs with content hashes in `bundle.json`.
- **Run-to-run diffing** — `pa_core/reporting/run_diff.py` `build_run_diff()` compares manifests and summary metrics for LLM comparison panels and CLI `--prev-manifest`.
- **Optional LLM layer** — `pa_core/llm/` (LangChain providers, LangSmith tracing) powers Results-page explanations; gated behind `.[llm]` extra (`pyproject.toml` L133–142, `docs/llm_features.md`).

## 5. Data model, identifiers and contracts

**Identifiers.** Simulation entities use string agent names (`ExternalPA`, etc.) and YAML asset/portfolio `id` fields inside `pa_core/schema.py`. Runs are timestamped as `YYYYMMDDTHHMMSSZ` (`pa_core/contracts.py` `RUN_ID_PATTERN`). Config and inputs are fingerprinted with SHA-256 in `manifest.json` (`pa_core/manifest.py:90-102`); `data_files` remains keyed by file path, so this is not a content-addressed storage or lookup system. There is **no database**; persistence is files only (no SQLite/Postgres usage in application code).

**Versioning.** Each run's `manifest.json` snapshots the parsed supplied config or explicit snapshot and records `git_commit` and optional `previous_run` for lineage. `RunArtifactBundle` adds `bundle.json` with per-output hashes. Supersession is informal: compare manifests or use `build_run_diff()`.

**Shipped contracts (`docs/contracts/`).**

| Contract | Documented | Emitted by code | Consumed by code |
|----------|-----------|-----------------|------------------|
| Local `run.json` (run record) | `docs/contracts/run-record.md` | **Yes** — `pa_core/cli.py` `_write_run_record()` | Tests (`tests/test_run_record_warnings.py`); Run Logs instead reads `run.log`, `run_end.json` and the manifest (`dashboard/pages/7_Run_Logs.py:30-68`) |
| `manifest.json` shape | `pa_core/contracts.py` `MANIFEST_*` | **Yes** — `pa_core/manifest.py` | Validation via `validate_manifest_payload()` |
| `artifact-manifest/v1` | `docs/contracts/schemas/artifact-manifest-v1.schema.json` | **No** — `bundle.json` is repo-specific, not schema-conformant | Validator supports it (`scripts/validate_run_contract.py:44-48`); no simulation consumer |
| `run-contract/v1` | `docs/contracts/run-contract-v1.md` | **No** — doc L16–17: "No participant emits an envelope yet" | Validator only: `scripts/validate_run_contract.py` |
| `evidence-object/v1` | `docs/contracts/schemas/evidence-object-v1.schema.json` | **No** | Validator only |
| `identity-map-conventions` | `docs/contracts/identity-map-conventions.md` | **No** — doc notes PAEM has no entities to resolve (L31–32) | **No** |
| `capability-bundle/v1` | `docs/contracts/capability-bundle-v1.md` | No simulation emitter | No simulation consumer; synced automation selects and renders bundles (`.github/scripts/keepalive_prompt_composer.js:31-53`, `.github/scripts/capability_bundle.js:6-19`) |
| Tool descriptor | `pa_core/tool_descriptor.py` | **Yes** — via `pa describe` (`docs/llm_features.md` L11–13) | External discovery only |

## 6. External inputs and dependencies

**Data sources.** Simulation index input is CSV with a required `Monthly_TR` column (`pa_core/data/loaders.py:248-294`; spec in `docs/DATA_IMPORT_SPEC.md`). CSV/XLSX asset imports belong to the separate `DataImportAgent` path (`pa_core/data/importer.py:10-16,60-70`). Sample bundled data: `data/sp500tr_fred_divyield.csv`. No live market API calls in the simulation path.

**LLM / agents.** Optional LangChain stack (`pyproject.toml` `[project.optional-dependencies] llm`). LangSmith tracing in `pa_core/llm/tracing.py`. MCP is not used by PAEM simulation code. GitHub agent workflows under `.github/workflows/agents-*.yml` are repo automation, not runtime features.

**Notable libraries.** NumPy/Pandas (simulation), Pydantic (config), Plotly + Kaleido (charts/static export), Streamlit (UI), python-pptx/xlsxwriter/openpyxl (exports), PyPDF (`pypdf` in dependencies — ancillary). Parquet optional via `pyarrow` extra.

**Install vs file-only.** Core tool requires Python 3.12+ install (`pyproject.toml` `requires-python`). Portable zip (`scripts/make_portable_zip.py`, `docs/PORTABLE_ZIP_GUIDE.md`) can bundle embeddable Python for Windows. The documented supported dashboard uses a Python process (Codespace or local). The browser entry point loads multiple sources and vendored dependencies into stlite (`web/index.html:271-322`); it is not a self-contained single HTML file, and work-environment viability remains unverified. Local Python is available at work, so evaluate that path with synthetic input before relying on browser portability.

## 7. Current state

**Test / CI posture.** Push to `main` runs lint, mypy, pytest with 60% coverage floor (`.github/workflows/ci.yml` L29). PRs go through `pr-00-gate.yml`: Python CI, Codespace validation, Streamlit boot smoke, CLI integration test, and `tests/golden/` tutorial tests. Default pytest excludes `live_llm` markers (`pyproject.toml` L78). Coverage report (`docs/COVERAGE_GAPS.md:4-11`, dated 2025-01-27) cites 66% coverage and 346 passing tests. The retained verification claimed about 1240 collected tests, but no collection output was available to substantiate it; current test count, coverage, and CI results are unverified.

**Implemented vs unverified.** Monte Carlo CLI, dashboard wizard, Excel/PPTX exports, sweeps, sleeve suggestion, and manifest/bundle emission are implemented, with CI jobs configured; this is not a fresh runtime or production certification. Prototype or incomplete: fleet `run-contract/v1` emission, `Scenario.sleeves` wiring, runtime validation of browser-only stlite deployment, dollar-cost accounting (`cost.dollars` is always `null` per `pa_core/cli.py` L941–942).

**Consequential gaps (cited).**

1. `run-contract/v1` not emitted — `docs/contracts/run-contract-v1.md` L16–17; no `scripts/emit_reference_run.sh` (`.github/workflows/backplane-conformance.yml` L51–54 skips).
2. `Scenario.sleeves` unwired — `pa_core/schema.py` L155–160, `README.md` L91.
3. Historical coverage was below the 85% target — `docs/COVERAGE_GAPS.md:4`; CI minimum remains configured at 60% (`.github/workflows/ci.yml:29`). Current measured coverage is unknown.
4. Historical dashboard coverage gaps — `docs/COVERAGE_GAPS.md:22-30` reports wizard 6% and validation UI 0%, but these are not current measurements; tests such as `tests/test_dashboard_cli.py` now exist.
5. No `config/backplane_participants.json` in repo — referenced by conformance workflow but absent from `config/`.
6. Model caveats need reconciliation: `README.md:86-89` says i.i.d. monthly draws and regimes ignored in sweeps, but `pa_core/sweep.py:661-691` builds regime paths and passes them into `draw_joint_returns`; `pa_core/sim/paths.py:745-810` applies regime-specific draws. Regimes are implemented when configured. Forward-looking/non-backtested remains the documented positioning.
7. `docs/ISSUES_BACKLOG.md` lists historical backlog items; several (DataImportAgent, packaging) are now implemented (`pa_core/data/importer.py`, `pyproject.toml` scripts) but backlog not updated.
8. `docs/ISSUES_BACKLOG.md:14` asks to remove Excel/CSV parameter inputs while retaining a converter. The simulation CLI uses YAML (`pa_core/cli.py:442-450`, `pa_core/config.py:1245-1275`), and CSV index input does not refute that migration. However, the deprecated CSV parameter loader still exists for conversion (`pa_core/data/loaders.py:196-245`, `pa_core/data/convert.py:13-21`); do not infer the release-limited backlog item is fully closed from CLI help alone.

## 8. Claims vs reality

These checks distinguish actual source statements from integration assumptions; a hypothetical claim is not attributed to the repository as a promise.

- **Local versus fleet run envelope.** `docs/contracts/run-record.md:3-7` calls local `run.json` the blueprint envelope; it does not explicitly promise fleet `run-contract/v1` compliance. Local emission (`pa_core/cli.py:915-923`) lacks the fleet schema/version fields; `docs/contracts/run-contract-v1.md:16-17` describes emission as future work. The shapes are different; this is an integration gap, not a proven false fleet-compliance claim.
- **Backplane gate.** `.github/workflows/backplane-conformance.yml:49-60` emits a skip message and no reference artifact when `scripts/emit_reference_run.sh` is absent, as it is in this clone. The workflow still invokes an external reusable workflow (`:62-68`); its live outcome and authoritative participant registry were not inspected. An absent local registry alone does not prove fleet-wide nonparticipation.
- **Scenario sleeves.** `README.md:91`, `pa_core/schema.py:155-160`, and `pa_core/reporting/disclaimers.py:25` consistently state the field is validated but unwired. This is an acknowledged limitation, not a contradicted promise.
- **Browser deployment.** `README.md:19` disclaims stlite support, but `web/index.html:271-322` fetches sources and mounts the dashboard with vendored packages, including python-pptx. The previous dossier incorrectly called it only a PNG helper. The implementation exists; end-to-end usability and work-environment compatibility remain unverified.
- **Streamlit backlog.** `docs/ISSUES_BACKLOG.md:12` lists MVP pages while seven numbered pages exist under `dashboard/pages/`. The backlog is stale as a statement of missing pages; file existence does not certify every interaction.
- **Evidence objects.** The schema exists but runtime searches found no PAEM emitter. Its own description says document evidence is outside the role of a pure computational engine (`docs/contracts/schemas/evidence-object-v1.schema.json:5`); do not present absent document provenance as a broken extraction promise.
- **Entity linking.** `docs/contracts/identity-map-conventions.md:31-32` explicitly describes entity resolution as inapplicable to PAEM. Runtime searches found no fleet `identity_refs` emission; arbitrary asset IDs are not a sibling-ID integration.
- **Sweep regimes.** The README assertion that sweeps ignore regimes (`README.md:87`) conflicts with actual regime simulation (`pa_core/sweep.py:661-691`), also exercised by the regression-test source `tests/test_sweep_reproducibility.py:93-141`. The test was read, not executed in this audit.

## 9. Interoperability hooks (for the fleet program)

**What PAEM could OFFER today (existing objects).**

- `manifest.json` — config snapshot, seed, `data_files` hashes, `config_hash`, optional `warnings`/`data_quality` (`pa_core/manifest.py`, `docs/DATA_IMPORT_SPEC.md` L32–38).
- `bundle.json` — portable run folder with hashed outputs (`pa_core/run_artifact_bundle.py`).
- Local `run.json` — pointers to manifest/bundle plus captured warnings (`docs/contracts/run-record.md`).
- `Outputs.xlsx` `Summary` sheet — standardized metric columns (`pa_core/contracts.py` `SUMMARY_REQUIRED_COLUMNS`).
- `pa-tool-descriptor/v1` — privacy/network boundary declaration (`pa_core/tool_descriptor.py`).
- Simulation metrics as tabular facts (AnnReturn, TE, CVaR, etc.) — no document-level provenance.

**What PAEM would CONSUME.**

- Monthly index return CSV with `Monthly_TR` (`pa_core/data/loaders.py:248-294`); CSV/XLSX asset import is a separate calibration path.
- YAML simulation config via `load_config` (`pa_core/config.py:1245-1280`); market/portfolio Scenario YAML via `load_scenario` (`pa_core/validate.py:30-34`).
- Optionally: asset library YAML produced by `CalibrationAgent.to_yaml` (`pa_core/data/calibration.py:208-216`) is loaded by Portfolio Builder (`dashboard/pages/2_Portfolio_Builder.py:86-110`); it is distinct from simulation `ModelConfig` YAML.
- Could ingest canonical entity IDs from siblings for labeling, but **no code path does this today**.

**Collision risks with siblings.**

- PAEM has **no manager/fund/pension entity model**; agent names (`ExternalPA`) are simulation roles, not investable entities — would not join to `manager:cik_*` IDs without an explicit mapping layer.
- Document-type vocabulary is N/A (no filings ingestion).
- `manifest.json` filename is generic and the local payload has neither a fleet `schema_version` nor a tool ID (`pa_core/manifest.py:23-38,108-125`). Consumers must retain external repo/tool context or add a fleet adapter; the separately emitted descriptor names `portable-alpha-extension-model`. The artifact schema description mentions other repositories only as context, not as verified sibling behavior.
- Metric column names (`monthly_TE`, `terminal_AnnReturn`) encode horizon/unit conventions (`pa_core/contracts.py:115-140`); any sibling adapter must explicitly align definitions. This audit did not verify uniqueness across the fleet.

## 10. Reuse candidates

| Component | Path |
|-----------|------|
| Reproducibility manifest writer | `pa_core/manifest.py` |
| Run/summary contract constants | `pa_core/contracts.py` |
| Hashed artifact bundle | `pa_core/run_artifact_bundle.py` |
| PSD covariance builder | `pa_core/sim/covariance.py` |
| Parameter sweep engine | `pa_core/sweep.py` |
| Constrained sleeve optimizer | `pa_core/sleeve_suggestor.py` |
| CSV/XLSX import + calibration | `pa_core/data/importer.py`, `pa_core/data/calibration.py` |
| Run diff engine | `pa_core/reporting/run_diff.py` |
| Run-contract validator (fleet) | `scripts/validate_run_contract.py` |
| Privacy/tool descriptor pattern | `pa_core/tool_descriptor.py` |
| Portable Windows packaging | `scripts/make_portable_zip.py` |

## 11. Proposed direction (evidence-based)

**Finish what is scaffolded**

- Implement `run-contract/v1` emitter projecting local `manifest.json`/`bundle.json` into `run.json` + `artifact-manifest/v1`, plus `scripts/emit_reference_run.sh` so `.github/workflows/backplane-conformance.yml` stops skipping (gap: §8 bullet 2, `run-contract-v1.md` L254–255).
- Wire `Scenario.sleeves` into `simulate_agents` or remove from schema to avoid false confidence (`pa_core/schema.py` L155–160).
- Measure current dashboard coverage before prioritizing tests; the 0–6% figures are historical (`docs/COVERAGE_GAPS.md:4,22-26`). Probe the implemented stlite dashboard with synthetic data and reconcile the README only after runtime evidence.
- Resolve the authoritative participant registry and external reusable workflow before opting into conformance; the local path is absent, but the caller delegates outside this clone (`.github/workflows/backplane-conformance.yml:62-68`).

**New capability (only if product needs it)**

- Add document-style evidence only for a concrete new use case; the existing evidence schema explicitly treats pure computational engines as outside its document-evidence role (`docs/contracts/schemas/evidence-object-v1.schema.json:5`).
- Ingest canonical entity IDs from Manager-Database/Pension-Data for scenario labeling (`identity-map-conventions.md` L36–40 recommends those repos as authority).
- External return series API adapter — not present; all inputs are files today (`pa_core/data/loaders.py`).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- PAEM answers "what happens if we allocate capital across portable alpha and active extension sleeves?" using Monte Carlo simulation, not historical backtesting.
- The easiest on-ramp is the Streamlit Scenario Wizard in a private Codespace or on-prem Python environment; do not upload real index data to public cloud demo hosts.
- Every run can leave a reproducibility trail (saved config, random seed, and file fingerprints) so you can defend a number in a meeting or compare two scenarios side by side.
- Results are gross of fees by default; regime behavior depends on configuration. The written caveats include stale statements, so reconcile them with the selected model settings before presenting a board pack.
- The tool does not know your managers, funds, or filing documents; fleet-wide entity linking is a future integration, not something the current simulation consumes.

