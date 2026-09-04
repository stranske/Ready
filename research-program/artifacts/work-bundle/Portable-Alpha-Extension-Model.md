# Portable-Alpha-Extension-Model — dossier (2026-09-04)

## 1. Purpose in one paragraph

Portable Alpha Extension Model (PAEM) is a Monte Carlo simulation tool for investment offices exploring **portable alpha** and **active extension** fund structures. It models how capital splits across benchmark exposure, external portable-alpha sleeves, active extension, and internal sleeves, then draws correlated monthly returns and financing paths to produce risk/return statistics (tracking error, CVaR, breach probability, shortfall probability, and related metrics). The primary audience is analysts and portfolio strategists who need scenario exploration without building spreadsheets from scratch. It was designed around **offline, local-first execution**: the deterministic engine runs without network access (`pa_core/tool_descriptor.py` declares `network.deterministic: "offline"`), with a Streamlit dashboard for non-developers and a portable Windows zip path for locked-down PCs. Proprietary index data is expected to stay inside the user's environment (Codespaces or on-prem); public SaaS hosting is explicitly discouraged in `README.md`.

## 2. Who uses it and how (surfaces)

| Surface | Entry point (file) | Who uses it | Status (evidence) |
|--------|-------------------|-------------|-------------------|
| CLI (`pa`, `pa-validate`, `pa-convert-params`) | `pa_core/pa.py`, `pa_core/validate.py`, `pa_core/data/convert.py` | Power users, automation, CI | **Working** — `pyproject.toml` registers console scripts; `README.md` documents `pa run --config … --index …`; integration test in `.github/workflows/pr-00-gate.yml` |
| Dashboard (Streamlit) | `dashboard/app.py`, `dashboard/pages/*.py` | Analysts, scenario exploration | **Working** — seven pages under `dashboard/pages/`; PR gate runs Streamlit health smoke (`.github/workflows/pr-00-gate.yml` ~L138) |
| Dashboard CLI launcher | `dashboard/cli.py` (`pa-dashboard`) | Same as dashboard | **Working** — registered in `pyproject.toml`; low test coverage (`docs/COVERAGE_GAPS.md` lists `dashboard/cli.py` at 0%) |
| Static HTML / stlite helper | `web/index.html` | Plotly PNG export in browser | **Partial** — `web/index.html` mounts stlite for off-screen Plotly rendering only; `README.md` L19 states the full WASM/stlite app path is **not** claimed as supported |
| Excel / board-pack artifacts | `pa_core/reporting/excel.py`, `pa_core/viz/pptx_export.py` | Reporting, committee packs | **Working** — default output `Outputs.xlsx` (`pa_core/contracts.py` `DEFAULT_OUTPUT_FILENAME`); `--pptx`/`--pdf` flags in root `manifest.json` cli_args |
| Run bundles / manifests | `pa_core/manifest.py`, `pa_core/run_artifact_bundle.py` | Reproducibility, run comparison | **Working** — `manifest.json` at repo root is a sample; `RunArtifactBundle.save()` writes `bundle.json` with SHA-256 hashes (`pa_core/run_artifact_bundle.py` L59–72) |
| Packaging utilities | `scripts/make_portable_zip.py`, `scripts/create_launchers.py` | IT / desktop deployment | **Working** — `pa-make-zip`, `pa-create-launchers` in `pyproject.toml`; `Makefile` `portable-zip` target |

## 3. Structure map

```
pa_core/          Core simulation engine, CLI, agents, data import, reporting, optional LLM
dashboard/        Streamlit UI (wizard, results, stress lab, run logs)
config/           YAML/JSON parameter templates, model registry, LLM slot config
data/             Sample index CSV (e.g. sp500tr_fred_divyield.csv)
docs/             User guides, contracts (run-contract schemas), development notes
docs/contracts/   JSON Schemas + markdown for fleet interoperability (mostly documented, not emitted)
scripts/          Portable zip, launcher creation, run-contract validator
tests/            Pytest suite (~1240 tests collected per local `pytest --collect-only`)
web/              stlite/Plotly static helper (not a full app shell)
tools/            CI triage utilities
.github/          CI, agent workflows — synced from stranske/Workflows (per `CLAUDE.md`)
design-system/    UI tokens — boilerplate, not simulation logic
archive/          Retired configs and development logs
```

## 4. Major code features you must understand to extend it

- **Canonical run pipeline** — `pa_core/facade.py` (`run_single`, `run_sweep`, `export`) is the single simulation entry used by CLI and dashboard; consumes `ModelConfig` + index `pd.Series`, produces per-agent return arrays and a summary `DataFrame`.
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

**Identifiers.** Simulation entities use string agent names (`ExternalPA`, etc.) and YAML asset/portfolio `id` fields inside `pa_core/schema.py`. Runs are timestamped as `YYYYMMDDTHHMMSSZ` (`pa_core/contracts.py` `RUN_ID_PATTERN`). Config and inputs are content-addressed via SHA-256 in `manifest.json` (`pa_core/manifest.py` `_hash_file`). There is **no database**; persistence is files only (no SQLite/Postgres usage in application code).

**Versioning.** Each run's `manifest.json` snapshots the full parsed config and records `git_commit` and optional `previous_run` for lineage. `RunArtifactBundle` adds `bundle.json` with per-output hashes. Supersession is informal: compare manifests or use `build_run_diff()`.

**Shipped contracts (`docs/contracts/`).**

| Contract | Documented | Emitted by code | Consumed by code |
|----------|-----------|-----------------|------------------|
| Local `run.json` (run record) | `docs/contracts/run-record.md` | **Yes** — `pa_core/cli.py` `_write_run_record()` | Dashboard run logs, tests (`tests/test_run_record_warnings.py`) |
| `manifest.json` shape | `pa_core/contracts.py` `MANIFEST_*` | **Yes** — `pa_core/manifest.py` | Validation via `validate_manifest_payload()` |
| `artifact-manifest/v1` | `docs/contracts/schemas/artifact-manifest-v1.schema.json` | **No** — `bundle.json` is repo-specific, not schema-conformant | **No** |
| `run-contract/v1` | `docs/contracts/run-contract-v1.md` | **No** — doc L16–17: "No participant emits an envelope yet" | Validator only: `scripts/validate_run_contract.py` |
| `evidence-object/v1` | `docs/contracts/schemas/evidence-object-v1.schema.json` | **No** | Validator only |
| `identity-map-conventions` | `docs/contracts/identity-map-conventions.md` | **No** — doc notes PAEM has no entities to resolve (L31–32) | **No** |
| `capability-bundle/v1` | `docs/contracts/capability-bundle-v1.md` | **No** | **No** |
| Tool descriptor | `pa_core/tool_descriptor.py` | **Yes** — via `pa describe` (`docs/llm_features.md` L11–13) | External discovery only |

## 6. External inputs and dependencies

**Data sources.** User-supplied CSV/XLSX index return files (`pa_core/data/loaders.py` `load_index_returns`; spec in `docs/DATA_IMPORT_SPEC.md`). Sample bundled data: `data/sp500tr_fred_divyield.csv`. No live market API calls in the simulation path.

**LLM / agents.** Optional LangChain stack (`pyproject.toml` `[project.optional-dependencies] llm`). LangSmith tracing in `pa_core/llm/tracing.py`. MCP is not used by PAEM simulation code. GitHub agent workflows under `.github/workflows/agents-*.yml` are repo automation, not runtime features.

**Notable libraries.** NumPy/Pandas (simulation), Pydantic (config), Plotly + Kaleido (charts/static export), Streamlit (UI), python-pptx/xlsxwriter/openpyxl (exports), PyPDF (`pypdf` in dependencies — ancillary). Parquet optional via `pyarrow` extra.

**Install vs file-only.** Core tool requires Python 3.12+ install (`pyproject.toml` `requires-python`). Portable zip (`scripts/make_portable_zip.py`, `docs/PORTABLE_ZIP_GUIDE.md`) can bundle embeddable Python for Windows. Dashboard requires a running Python process (Codespace or local); not a static single-file app.

## 7. Current state

**Test / CI posture.** Push to `main` runs lint, mypy, pytest with 60% coverage floor (`.github/workflows/ci.yml` L29). PRs go through `pr-00-gate.yml`: Python CI, Codespace validation, Streamlit boot smoke, CLI integration test, and `tests/golden/` tutorial tests. Default pytest excludes `live_llm` markers (`pyproject.toml` L78). Coverage report (`docs/COVERAGE_GAPS.md`, dated 2025-01-27) cites 66% coverage and 346 passing tests; local collection shows ~1240 tests defined (environment may affect execution).

**Production-usable vs prototype.** Monte Carlo CLI, dashboard wizard, Excel/PPTX exports, sweeps, sleeve suggestion, and manifest/bundle emission are implemented and gated in CI. Prototype or incomplete: fleet `run-contract/v1` emission, `Scenario.sleeves` wiring, full browser-only stlite deployment, dollar-cost accounting (`cost.dollars` is always `null` per `pa_core/cli.py` L941–942).

**Consequential gaps (cited).**

1. `run-contract/v1` not emitted — `docs/contracts/run-contract-v1.md` L16–17; no `scripts/emit_reference_run.sh` (`.github/workflows/backplane-conformance.yml` L51–54 skips).
2. `Scenario.sleeves` unwired — `pa_core/schema.py` L155–160, `README.md` L91.
3. Coverage below 85% target — `docs/COVERAGE_GAPS.md` L4; CI minimum 60% (`.github/workflows/ci.yml` L29).
4. Dashboard pages largely untested — `docs/COVERAGE_GAPS.md` L22–30 (wizard 6%, validation UI 0%).
5. No `config/backplane_participants.json` in repo — referenced by conformance workflow but absent from `config/`.
6. Model limitations documented as intentional — i.i.d. monthly draws, no regimes in sweeps, forward-looking not backtested (`README.md` L86–89).
7. `docs/ISSUES_BACKLOG.md` lists historical backlog items; several (DataImportAgent, packaging) are now implemented (`pa_core/data/importer.py`, `pyproject.toml` scripts) but backlog not updated.
8. `docs/ISSUES_BACKLOG.md` item 10 ("Remove Excel/CSV parameter inputs; keep converter for one release") is completed: CLI parameter input is strictly YAML (`pa_core/cli.py:442-449`); CSV/XLSX parameter ingestion was removed from the simulation entry point, and `pa_core/data/convert.py` (`pa-convert-params`) was provided as the transition converter. CSV inputs are accepted only for market index return series (`--index`), not model parameters.

## 8. Claims vs reality

- **Claim: PAEM's `run.json` satisfies the fleet `run-contract/v1` envelope.** `docs/contracts/run-record.md:3-7` defines `run.json` as fulfilling the "blueprint `run_contract` standard", which can be conflated with the fleet standard. In reality, `docs/contracts/run-contract-v1.md:16–17` explicitly notes that no participant emits `run-contract/v1` yet; code emits a **different** local `run.json` (`docs/contracts/run-record.md`, `pa_core/cli.py:910–928`) without `schema_version: run-contract/v1`.
- **Claim: Backplane conformance gate validates PAEM runs.** `.github/workflows/backplane-conformance.yml:49–55`: without `emit_reference_run.sh`, the job prints "No emitter wired yet; the conformance gate will skip."
- **Claim: Scenario YAML `sleeves` field drives simulation.** README and `pa_core/schema.py:155–160` say it is validated only; `pa_core/reporting/disclaimers.py:25` repeats this in board packs.
- **Claim: Pure browser / stlite deployment.** README line 19 explicitly disclaims the stlite path because Kaleido and python-pptx are not Pyodide-viable; `web/index.html` is a Plotly render helper, not the full dashboard.
- **Claim: ISSUES_BACKLOG "Streamlit MVP pages" as open work.** Seven pages exist under `dashboard/pages/`; backlog (`docs/ISSUES_BACKLOG.md:12`) is stale relative to code.
- **Claim: Evidence objects with document provenance.** Schemas exist (`docs/contracts/schemas/evidence-object-v1.schema.json`) but no PAEM module writes `evidence-object/v1` JSON.
- **Claim: Entity IDs for fleet join.** `docs/contracts/identity-map-conventions.md:31–32` assigns PAEM "1/3, N/A" — no `identity_refs` emission in run artifacts.

## 9. Interoperability hooks (for the fleet program)

**What PAEM could OFFER today (existing objects).**

- `manifest.json` — config snapshot, seed, `data_files` hashes, `config_hash`, optional `warnings`/`data_quality` (`pa_core/manifest.py`, `docs/DATA_IMPORT_SPEC.md` L32–38).
- `bundle.json` — portable run folder with hashed outputs (`pa_core/run_artifact_bundle.py`).
- Local `run.json` — pointers to manifest/bundle plus captured warnings (`docs/contracts/run-record.md`).
- `Outputs.xlsx` `Summary` sheet — standardized metric columns (`pa_core/contracts.py` `SUMMARY_REQUIRED_COLUMNS`).
- `pa-tool-descriptor/v1` — privacy/network boundary declaration (`pa_core/tool_descriptor.py`).
- Simulation metrics as tabular facts (AnnReturn, TE, CVaR, etc.) — no document-level provenance.

**What PAEM would CONSUME.**

- Monthly index return CSV/XLSX (`pa_core/data/loaders.py`).
- YAML scenario/config files (`pa_core/config.py` `load_config`).
- Optionally: calibrated μ/σ/ρ from an asset library YAML produced by `CalibrationAgent` (`pa_core/data/calibration.py`).
- Could ingest canonical entity IDs from siblings for labeling, but **no code path does this today**.

**Collision risks with siblings.**

- PAEM has **no manager/fund/pension entity model**; agent names (`ExternalPA`) are simulation roles, not investable entities — would not join to `manager:cik_*` IDs without an explicit mapping layer.
- Document-type vocabulary is N/A (no filings ingestion).
- `manifest.json` filename is generic — fleet tools should key on `schema_version` or tool id (`portable-alpha-extension-model` in descriptor) to avoid conflating with Trend_Model `run_meta.json` or Counter_Risk manifests mentioned in `artifact-manifest-v1.schema.json` description.
- Metric column names (`monthly_TE`, `terminal_AnnReturn`) are PAEM-specific; siblings using different annualization or horizon labels need a translation table.

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
- Raise test coverage on dashboard critical paths — wizard and validation UI at 0–6% (`docs/COVERAGE_GAPS.md` L22–26).
- Add `config/backplane_participants.json` entry when opting into fleet conformance (referenced in `backplane-conformance.yml` L22 but missing from `config/`).

**New capability (only if product needs it)**

- Map simulation outputs to `evidence-object/v1` if fleet orchestration needs attributable facts (schema exists; no emitter).
- Ingest canonical entity IDs from Manager-Database/Pension-Data for scenario labeling (`identity-map-conventions.md` L36–40 recommends those repos as authority).
- External return series API adapter — not present; all inputs are files today (`pa_core/data/loaders.py`).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- PAEM answers "what happens if we allocate capital across portable alpha and active extension sleeves?" using Monte Carlo simulation, not historical backtesting.
- The easiest on-ramp is the Streamlit Scenario Wizard in a private Codespace or on-prem Python environment; do not upload real index data to public cloud demo hosts.
- Every run can leave a reproducibility trail (saved config, random seed, and file fingerprints) so you can defend a number in a meeting or compare two scenarios side by side.
- Results are gross of fees by default, assume independent monthly draws, and ignore market regimes unless you configure otherwise — read the caveats slide in any generated board pack before presenting.
- The tool does not know your managers, funds, or filing documents; fleet-wide entity linking is a future integration, not something the current simulation consumes.

*Evidence-checked against source repositories; verification metadata omitted from work bundle.*
