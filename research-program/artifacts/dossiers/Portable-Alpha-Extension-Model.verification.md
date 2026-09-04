# Portable-Alpha-Extension-Model dossier — verification table

Verified against clone `clones/Portable-Alpha-Extension-Model` at HEAD `8ddf6be49b95a18b02cd83aeebc565e8177c967d` (2026-09-04).
Method: every cited file:line/symbol opened and verified against current code and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 52 |
| WRONG (corrected in dossier) | 1 |
| UNVERIFIABLE | 0 |
| **Total checked** | **53** |

### Key Findings & Corrections

1. **§7 Gap 8: Parameter Inputs vs Index Returns (Correction):** The original dossier asserted: *"ISSUES_BACKLOG.md item 10 ('Remove Excel/CSV parameter inputs') not done — CLI still accepts CSV index + YAML config."* Opening `docs/ISSUES_BACKLOG.md:14`, `pa_core/cli.py:442-450`, and `pa_core/data/convert.py` reveals this is an erroneous refutation. Item 10 explicitly specified *"Remove Excel/CSV parameter inputs; keep converter for one release"*. Parameter input was indeed transitioned exclusively to YAML (`pa_core/cli.py:442-449`), CSV parameter parsing was removed from the simulation execution path, and `pa_core/data/convert.py` was implemented to provide the transition converter (`pa convert` / `pa-convert-params`). The CLI accepts CSV exclusively for market index return series (`--index`), not model parameters. Item 10 was completed.
2. **§8 Claim 1: Fleet Run Envelope vs Blueprint Run Record (Attribution & Refutation):** The dossier refutes that the fleet run envelope is wired. Opening `docs/contracts/run-record.md:3-7` shows that `run.json` was implemented to fulfill the blueprint `run_contract` standard (*"The blueprint `run_contract` standard requires each run to be representable as a single JSON object... `run.json` is that envelope"*). However, `docs/contracts/run-contract-v1.md:16-17` explicitly notes that no participant emits the fleet `run-contract/v1` envelope yet. `pa_core/cli.py:910-928` emits the local `run.json` shape (`manifest_path`, `run_end_path`, `bundle_path`, `warnings`, `cost`), which does not contain `schema_version: run-contract/v1` or the fleet envelope structure. The refutation is confirmed, with attribution clarified to avoid conflating the local blueprint run record with the fleet contract.
3. **§8 Backplane Conformance Gate & Participants Config:** Confirmed that `.github/workflows/backplane-conformance.yml:51-54` checks for `./scripts/emit_reference_run.sh` and skips when absent. Furthermore, `config/backplane_participants.json` is absent from `config/`, confirming PAEM is not active in the backplane conformance gate.
4. **§4 & §8 Sleeve Model Unwired Status:** Confirmed that while `pa_core/agents/registry.py` and `pa_core/simulations.py` simulate agents, `Scenario.sleeves` in `pa_core/schema.py:155-160` is validated only and completely unwired from the simulation runtime, as also documented on line 91 of `README.md` and line 25 of `pa_core/reporting/disclaimers.py`.

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | Canonical run pipeline: `run_single`, `run_sweep`, `export` single entry used by CLI and dashboard; consumes `ModelConfig` + index `pd.Series`, produces per-agent return arrays and summary `DataFrame` | `pa_core/facade.py:1-24, 147-172, 284-326, 569-615, 679-700`, `pa_core/cli.py:1419` | CONFIRMED | `run_single`, `run_sweep`, and `export` provide the canonical entrypoints. CLI delegates to `run_single` (`cli.py:1419`), and `RunArtifacts` contains `returns: dict[str, ArrayLike]` and `summary: pd.DataFrame`. |
| 2 | Agent / sleeve model: `pa_core/agents/registry.py` maps names (`ExternalPA`, `ActiveExt`, `InternalPA`, `InternalBeta`, `Base`) to agent classes; `simulate_agents()` wires return/financing streams into per-sleeve paths and Total overlay contribution | `pa_core/agents/registry.py:15-21, 52-70`, `pa_core/simulations.py:86-138` | CONFIRMED | `_AGENT_MAP` maps all 5 named agent classes; `simulate_agents` iterates over agents, computes monthly returns, applies optional fees, and appends `Total` overlay contribution. |
| 3 | Covariance and return draws: `build_cov_matrix` and `nearest_psd` build and PSD-project covariance; `paths.py` and `draw_joint_returns` produce correlated monthly shocks | `pa_core/sim/covariance.py:13-18, 112-140`, `pa_core/sim/paths.py:18-28`, `pa_core/sweep.py:35` | CONFIRMED | `build_cov_matrix` clips volatilities, builds correlation matrix, and projects to nearest PSD matrix. `draw_joint_returns` in `paths.py` draws joint correlated shocks. |
| 4 | Parameter sweep engine: `run_parameter_sweep()` grids `SweepConfig` parameters, reuses RNG substreams, and consolidates numeric summary columns per `SUMMARY_*` fields | `pa_core/sweep.py:31-38, 369-420, 840-855`, `pa_core/random.py:1-50`, `pa_core/contracts.py:31` | CONFIRMED | `run_parameter_sweep()` handles parameter gridding and RNG derivation via `spawn_rngs`/`_derive_regime_rng`; `sweep_results_to_dataframe` filters columns matching `SUMMARY_NUMERIC_COLUMNS`. |
| 5 | Sleeve allocation optimizer: `sleeve_suggestor.py` searches capital weights across `SLEEVE_AGENTS` under TE/CVaR/breach constraints via `MultiObjectiveProblem`; CLI flag `--suggest-sleeves` | `pa_core/sleeve_suggestor.py:12-23, 60-120`, `pa_core/multi_objective.py:1-50`, `pa_core/cli.py:593` | CONFIRMED | `SLEEVE_AGENTS = ("ExternalPA", "ActiveExt", "InternalPA")`, `MultiObjectiveProblem` imported and used; `--suggest-sleeves` CLI option registered. |
| 6 | Configuration schema: `pa_core/config.py` + `pa_core/schema.py` (`Scenario`, `ModelConfig`) validate YAML; `Scenario.sleeves` is validated but explicitly unwired | `pa_core/config.py:1245-1280`, `pa_core/schema.py:145-161` | CONFIRMED | Pydantic models validate YAML; `sleeves` field docstring and comment on lines 155-161 explicitly note it is unwired. |
| 7 | Data import and calibration: `DataImportAgent` and `CalibrationAgent` turn CSV/XLSX into monthly returns and μ/σ/ρ estimates; CLI subcommands in `pa_core/pa.py` | `pa_core/data/importer.py:10-40`, `pa_core/data/calibration.py:82-140`, `pa_core/calibration.py:17-45`, `pa_core/pa.py:183` | CONFIRMED | `DataImportAgent` and `CalibrationAgent` fully implemented; `pa calibrate` registered as CLI subcommand. |
| 8 | Reproducibility manifest: `ManifestWriter.write()` records git commit, seed, config hash, and input file SHA-256s into `manifest.json` | `pa_core/manifest.py:22-60` | CONFIRMED | `ManifestWriter` hashes input data files and config file via `_hash_file` and writes JSON manifest with commit, seed, and parameters. |
| 9 | Run record envelope: `_write_run_record()` emits local `run.json` linking manifest, warnings, and cost stub; distinct from fleet `run-contract/v1` | `pa_core/cli.py:910-928, 939-948`, `pa_core/contracts.py:59-70` | CONFIRMED | `_write_run_record` writes `run.json` with `manifest_path`, `run_end_path`, `bundle_path`, `warnings`, and `cost` (`dollars: null`). |
| 10 | Artifact bundle with integrity: `RunArtifactBundle` packages config, manifest, and outputs with content hashes in `bundle.json` | `pa_core/run_artifact_bundle.py:50-75` | CONFIRMED | `RunArtifactBundle.save()` copies outputs and writes `bundle.json` containing SHA-256 hashes of config, manifest, and output files. |
| 11 | Run-to-run diffing: `build_run_diff()` compares manifests and summary metrics for LLM comparison panels and CLI `--prev-manifest` | `pa_core/reporting/run_diff.py:23-42`, `pa_core/cli.py:588` | CONFIRMED | `build_run_diff` generates config diffs and metric deltas; CLI registers `--prev-manifest`. |
| 12 | Optional LLM layer: `pa_core/llm/` (LangChain providers, LangSmith tracing) powers Results-page explanations; gated behind `.[llm]` extra | `pyproject.toml:133-142`, `docs/llm_features.md:1-35`, `pa_core/llm/tracing.py` | CONFIRMED | Optional dependency extra `llm` specifies pinned LangChain and LangSmith packages; tracing and helper functions gated behind optional imports. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 13 | Simulation entities use string agent names (`ExternalPA`, etc.) and YAML asset/portfolio `id` fields inside `pa_core/schema.py` | `pa_core/schema.py:45-175`, `pa_core/agents/registry.py:15-21` | CONFIRMED | `Asset.id`, `Portfolio.id` are strings; agent identifiers are string keys (`ExternalPA`, `ActiveExt`, etc.). |
| 14 | Runs are timestamped as `YYYYMMDDTHHMMSSZ` (`RUN_ID_PATTERN`) | `pa_core/contracts.py:13` | CONFIRMED | `RUN_ID_PATTERN = re.compile(r"^\d{8}T\d{6}Z$")` strictly matches ISO-compact UTC timestamps. |
| 15 | Config and inputs are content-addressed via SHA-256 in `manifest.json` (`_hash_file`) | `pa_core/manifest.py:48-56` | CONFIRMED | Uses `hashlib.sha256()` to hash files and data blocks. |
| 16 | Persistence is files only (no database, no SQLite/Postgres in app code) | `pa_core/`, `dashboard/` | CONFIRMED | Grep across `pa_core` and `dashboard` confirms zero database drivers, connections, or SQL queries. |
| 17 | Versioning: `manifest.json` snapshots config, records `git_commit` & optional `previous_run`; `RunArtifactBundle` writes `bundle.json` | `pa_core/manifest.py:23-39`, `pa_core/run_artifact_bundle.py:59-72` | CONFIRMED | Lineage tracking via `git_commit` and `previous_run`; bundle hashes recorded. |
| 18 | Shipped contract: Local `run.json` documented in `docs/contracts/run-record.md`, emitted by `pa_core/cli.py:910-928`, consumed by dashboard run logs and tests | `docs/contracts/run-record.md:1-25`, `pa_core/cli.py:910-928`, `tests/test_run_record_warnings.py:1-60` | CONFIRMED | Shape defined in markdown contract and matches emitted payload in `_write_run_record`. |
| 19 | Shipped contract: `manifest.json` shape documented in `pa_core/contracts.py`, emitted by `pa_core/manifest.py`, validated by `validate_manifest_payload()` | `pa_core/contracts.py:38-57, 292-310`, `pa_core/manifest.py:58-85` | CONFIRMED | Constants and validator `validate_manifest_payload()` enforce and verify manifest structure. |
| 20 | Shipped contract: `artifact-manifest/v1` documented in `docs/contracts/schemas/artifact-manifest-v1.schema.json`, not emitted or consumed | `docs/contracts/schemas/artifact-manifest-v1.schema.json:1-60` | CONFIRMED | JSON schema present in repo; `bundle.json` is a custom format, not conforming to this schema. |
| 21 | Shipped contract: `run-contract/v1` documented in `docs/contracts/run-contract-v1.md`, not emitted; consumed by validator script only | `docs/contracts/run-contract-v1.md:16-17`, `scripts/validate_run_contract.py:1-50` | CONFIRMED | Documentation explicitly states no participant emits envelope yet; validator script exists in `scripts/`. |
| 22 | Shipped contract: `evidence-object/v1` documented in `docs/contracts/schemas/evidence-object-v1.schema.json`, not emitted; validator only | `docs/contracts/schemas/evidence-object-v1.schema.json:1-55`, `scripts/validate_run_contract.py:48` | CONFIRMED | Schema exists and is checked by validator script; no simulation or reporting module emits it. |
| 23 | Shipped contract: `identity-map-conventions` documented in `docs/contracts/identity-map-conventions.md`, not emitted or consumed | `docs/contracts/identity-map-conventions.md:31-32` | CONFIRMED | Doc states PAEM has no entities to resolve (1/3, N/A); no `identity_refs` in emitted runs. |
| 24 | Shipped contract: `capability-bundle/v1` documented in `docs/contracts/capability-bundle-v1.md`, not emitted or consumed | `docs/contracts/capability-bundle-v1.md:1-30` | CONFIRMED | Contract document present in repo; no code references or emits it. |
| 25 | Shipped contract: Tool descriptor in `pa_core/tool_descriptor.py`, emitted via `pa describe`, external discovery only | `pa_core/tool_descriptor.py:8-77`, `docs/llm_features.md:11-13`, `pa_core/pa.py:125` | CONFIRMED | `get_tool_descriptor()` returns static dictionary declaring boundaries and permissions. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim / refutation | Cite | Verdict | Evidence / Correct statement |
|---|---|---|---|---|
| 26 | **Claim: Fleet run envelope is wired.** Refutation: `docs/contracts/run-contract-v1.md:16-17` states no participant emits `run-contract/v1` yet; code emits a *different* local `run.json` (`docs/contracts/run-record.md`, `pa_core/cli.py:915-923`) without `schema_version: run-contract/v1`. | `docs/contracts/run-contract-v1.md:16-17`, `docs/contracts/run-record.md:3-7`, `pa_core/cli.py:910-928` | CONFIRMED | Refutation holds. `docs/contracts/run-record.md:3-7` defines `run.json` as fulfilling the blueprint `run_contract` standard, which can be conflated with the fleet contract. But `run-contract-v1.md:16-17` confirms no participant emits `run-contract/v1`, and `cli.py` emits the local shape. |
| 27 | **Claim: Backplane conformance gate validates PAEM runs.** Refutation: `.github/workflows/backplane-conformance.yml:49-55`: without `emit_reference_run.sh`, the job prints "No emitter wired yet; the conformance gate will skip." | `.github/workflows/backplane-conformance.yml:49-55` | CONFIRMED | Refutation holds. `scripts/emit_reference_run.sh` does not exist, causing workflow step to echo skip notice and exit cleanly. |
| 28 | **Claim: Scenario YAML `sleeves` field drives simulation.** Refutation: README and `pa_core/schema.py:155-160` say it is validated only; `pa_core/reporting/disclaimers.py:25` repeats this in board packs. | `README.md:91`, `pa_core/schema.py:155-160`, `pa_core/reporting/disclaimers.py:25` | CONFIRMED | Refutation holds. `Scenario.sleeves` is explicitly documented and implemented as unwired (validated for `capital_share` sum to 1, but completely ignored during return simulation). |
| 29 | **Claim: Pure browser / stlite deployment.** Refutation: README line 19 explicitly disclaims stlite path because Kaleido and python-pptx are not Pyodide-viable; `web/index.html` is a Plotly render helper, not the full dashboard. | `README.md:19`, `web/index.html:20-55` | CONFIRMED | Refutation holds. README explicitly states the pure client-side WASM/stlite path is not claimed; `web/index.html` is an off-screen renderer communicating over BroadcastChannel `pa-render`. |
| 30 | **Claim: ISSUES_BACKLOG "Streamlit MVP pages" as open work.** Refutation: Seven pages exist under `dashboard/pages/`; backlog (`docs/ISSUES_BACKLOG.md:12`) is stale relative to code. | `docs/ISSUES_BACKLOG.md:12`, `dashboard/pages/` | CONFIRMED | Refutation holds. `dashboard/pages/` contains 7 implemented pages (`1_Asset_Library.py` through `7_Run_Logs.py`). |
| 31 | **Claim: Evidence objects with document provenance.** Refutation: Schemas exist (`docs/contracts/schemas/evidence-object-v1.schema.json`) but no PAEM module writes `evidence-object/v1` JSON. | `docs/contracts/schemas/evidence-object-v1.schema.json:1-55`, `pa_core/` | CONFIRMED | Refutation holds. Schema is checked by `scripts/validate_run_contract.py`, but no simulation or export code produces evidence objects. |
| 32 | **Claim: Entity IDs for fleet join.** Refutation: `docs/contracts/identity-map-conventions.md:31-32` assigns PAEM "1/3, N/A" — no `identity_refs` emission in run artifacts. | `docs/contracts/identity-map-conventions.md:31-32`, `pa_core/manifest.py:22-40` | CONFIRMED | Refutation holds. Contract doc explicitly notes PAEM has no entities to resolve; simulation artifacts emit no `identity_refs`. |

---

## §9 — Interoperability hooks (for the fleet program)

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 33 | Offers `manifest.json`: config snapshot, seed, `data_files` hashes, `config_hash`, optional `warnings`/`data_quality` | `pa_core/manifest.py:22-40`, `docs/DATA_IMPORT_SPEC.md:32-38` | CONFIRMED | Confirmed in `Manifest` dataclass and `ManifestWriter.write()`. |
| 34 | Offers `bundle.json`: portable run folder with hashed outputs | `pa_core/run_artifact_bundle.py:59-72` | CONFIRMED | Confirmed in `RunArtifactBundle.save()`. |
| 35 | Offers Local `run.json`: pointers to manifest/bundle plus captured warnings | `docs/contracts/run-record.md:13-22`, `pa_core/cli.py:915-923` | CONFIRMED | Emitted in `_write_run_record()`. |
| 36 | Offers `Outputs.xlsx` Summary sheet: standardized metric columns (`SUMMARY_REQUIRED_COLUMNS`) | `pa_core/contracts.py:115-140`, `pa_core/reporting/excel.py` | CONFIRMED | `SUMMARY_REQUIRED_COLUMNS` strictly defines the summary table schema. |
| 37 | Offers `pa-tool-descriptor/v1`: privacy/network boundary declaration | `pa_core/tool_descriptor.py:8-77` | CONFIRMED | Implemented in static descriptor dictionary. |
| 38 | Offers simulation metrics as tabular facts without document-level provenance | `pa_core/facade.py:147-172` | CONFIRMED | Simulation outputs tabular numeric metrics per agent; no filing text or excerpt pointers exist. |
| 39 | Consumes monthly index return CSV/XLSX | `pa_core/data/loaders.py:50-194` | CONFIRMED | `load_index_returns` handles CSV and Excel return time series. |
| 40 | Consumes YAML scenario/config files | `pa_core/config.py:1245-1280` | CONFIRMED | `load_config` parses YAML into `ModelConfig`. |
| 41 | Consumes calibrated μ/σ/ρ from asset library YAML produced by `CalibrationAgent` | `pa_core/data/calibration.py:82-217` | CONFIRMED | `CalibrationAgent` outputs calibrated parameters to asset library format. |
| 42 | Consumes canonical entity IDs from siblings: no code path does this today | `pa_core/schema.py`, `pa_core/config.py` | CONFIRMED | Codebase has no entity resolution or ID ingestion mechanism. |
| 43 | Collision risk: No manager/fund/pension entity model; simulation agent roles (`ExternalPA`, etc.) cannot join to `manager:cik_*` without mapping layer | `pa_core/agents/registry.py:15-21`, `docs/contracts/identity-map-conventions.md:31-32` | CONFIRMED | Agent names represent theoretical simulation functions, not legal entities or managers. |
| 44 | Collision risk: Document-type vocabulary is N/A (no filings ingestion) | `pa_core/` | CONFIRMED | Confirmed: PAEM does not ingest or classify regulatory or financial filings. |
| 45 | Collision risk: `manifest.json` filename is generic; tools must key on schema_version or tool id | `pa_core/contracts.py:39`, `docs/contracts/schemas/artifact-manifest-v1.schema.json:5-10` | CONFIRMED | Manifest filename is `manifest.json`; collision possible if stored in unpartitioned root. |
| 46 | Collision risk: Metric column names (`monthly_TE`, `terminal_AnnReturn`) are PAEM-specific; requires translation table for siblings | `pa_core/contracts.py:115-140` | CONFIRMED | Metric names include explicit prefixes (`monthly_`, `terminal_`) unique to PAEM. |

---

## §1, §2, §6, §7, §10, §11 — Supporting Claims

| # | Section | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|---|
| 47 | §1 | Offline execution boundary and no SaaS policy | `pa_core/tool_descriptor.py:18-21`, `README.md:17` | CONFIRMED | `tool_descriptor.py` declares deterministic engine offline; README explicitly discourages public SaaS hosting for proprietary index data. |
| 48 | §2 | Surfaces: CLI console scripts, Streamlit dashboard, static helper, Excel/PPTX exports, packaging | `pyproject.toml:194-200`, `.github/workflows/pr-00-gate.yml:138,183`, `web/index.html`, `pa_core/contracts.py:87`, `Makefile:90` | CONFIRMED | All entry points, scripts, and workflows verified. |
| 49 | §6 | External dependencies: NumPy, Pandas, Pydantic, Plotly, Streamlit, etc.; optional LLM extra | `pyproject.toml:113-142`, `pa_core/llm/tracing.py` | CONFIRMED | Base and optional dependencies in `pyproject.toml` verified. |
| 50 | §7 | CI/test posture & coverage floor | `.github/workflows/ci.yml:29`, `pr-00-gate.yml`, `pyproject.toml:78`, `docs/COVERAGE_GAPS.md:4-11` | CONFIRMED | `coverage-min: "60"` in `ci.yml`; pytest collect-only yields 1240 tests (docs report cites 346 passing tests as of 2025-01-27). |
| 51 | §7 | Consequential gap 8: `ISSUES_BACKLOG.md` item 10 status | `docs/ISSUES_BACKLOG.md:14`, `pa_core/cli.py:442-450`, `pa_core/data/convert.py` | **WRONG (corrected)** | Dossier claimed item 10 ("Remove Excel/CSV parameter inputs") is not done because CLI accepts CSV index + YAML config. In reality, item 10 is completed: parameter inputs were converted strictly to YAML (`pa_core/cli.py:442-449`), CSV parameter parsing was removed from simulation execution, and `pa_core/data/convert.py` (`pa-convert-params`) was provided as the transition converter. CSV inputs are accepted only for market index return series (`--index`), not model parameters. |
| 52 | §10 | All 11 reuse candidate paths exist and match roles | `pa_core/manifest.py`, `pa_core/contracts.py`, `pa_core/run_artifact_bundle.py`, `pa_core/sim/covariance.py`, `pa_core/sweep.py`, `pa_core/sleeve_suggestor.py`, `pa_core/data/importer.py`, `pa_core/data/calibration.py`, `pa_core/reporting/run_diff.py`, `scripts/validate_run_contract.py`, `pa_core/tool_descriptor.py`, `scripts/make_portable_zip.py` | CONFIRMED | All 11 components exist and perform the described functions. |
| 53 | §11 | Evidence-backed proposed directions | `pa_core/schema.py:155-160`, `.github/workflows/backplane-conformance.yml:51-54`, `docs/COVERAGE_GAPS.md:22-26` | CONFIRMED | Proposed directions align directly with verified implementation gaps. |
