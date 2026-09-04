# Counter_Risk dossier — verification table

Verified against clone `clones/Counter_Risk` at HEAD `3f3ae3df95a0f826f0f3a7c8bc0a71f5cd3092d5` (2026-09-04 14:35 UTC).
Method: every cited file:line/symbol opened. Zip-inspected `Runner.xlsm` parts directly. No claim marked WRONG without reading the current code.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 39 |
| WRONG (corrected in dossier) | 5 |
| CITE-DRIFT (substance right, citation fixed) | 6 |
| UNVERIFIABLE | 2 |
| **Total checked** | **52** |

All 5 WRONG findings are the same failure mode: the dossier repeated a claim from the **in-repo audit** (`docs/audit/AUDIT_REPORT.md`, `REMAINING_WORK.md`) without re-opening the code. That audit predates the fixes — its own citations use pre-fix line numbers (`data_quality.py:20`, `io/discover.py:242`), which is the tell. `docs/audit/REMAINING_WORK.md` is itself now a stale document.

## §4 — Major code features

| Claim | Cite | Verdict | Note |
| --- | --- | --- | --- |
| Pipeline orchestration single integration point | `pipeline/run.py` | CONFIRMED | exists; 2500+ lines, parse→…→manifest |
| Pydantic YAML with `extra="forbid"` | `config.py` | CONFIRMED | `config.py:18,27,36,85` |
| Pluggable `output_generators` stages | `README.md:24-51` | CONFIRMED | `README.md:22-51`; field at `config.py:118-120` |
| Parsers for NISA/CPRS/PDF layouts | `parsers/nisa*.py`, `cprs_ch.py`, `cprs_fcm.py`, `daily_holdings_pdf.py` | CONFIRMED | all present (`nisa.py`, `nisa_all_programs.py`, `nisa_ex_trend.py`, `nisa_trend.py`) |
| Typed parse failures | `pipeline/parsing_types.py` | CONFIRMED | exists |
| Registry maps raw→`canonical_key`+`display_name` | `docs/name_registry.md:7-12` | CONFIRMED | exact |
| Reconciliation `strict` vs `warn` from config | `audit/20-functionality-wiring.md:11` | CONFIRMED (cite-drift) | text exact; path is `docs/audit/20-functionality-wiring.md` |
| MOSERS writer stamps `as_of_date` | `writers/mosers_workbook.py:121-123` | CONFIRMED | exact; this is REMAINING_WORK #17, now landed |
| Output registry: 4 stages | `outputs/registry.py` | **CITE-DRIFT** | registry exists, but the stage enum is `config.py:40`, not `outputs/registry.py` |
| Compute emits concentration / risk / breach CSVs | `compute/rollups.py`, `compute/limits.py` | CONFIRMED | both present; `README.md:17-19` |
| Manifest validated before write | `pipeline/manifest.py:194-196` | CONFIRMED | `validate_manifest` raises pre-write at :194-196 |
| `counter-risk-manifest/v1` w/ hashes+provenance | `README.md:122-127` | CONFIRMED | `README.md:13`, :122-127 |
| LangSmith NDJSON without raw positions | `docs/langsmith_fleet.md` | CONFIRMED | :3-6; wired at `pipeline/run.py:626` |
| Chat optional, off critical path | `chat/session.py`, `providers/langchain_runtime.py` | CONFIRMED | both present |

## §5 — Data model, identifiers, contracts

| Claim | Cite | Verdict | Note |
| --- | --- | --- | --- |
| `canonical_key`/`aliases`/`display_name` fields | `name_registry.py:76-78` | CONFIRMED | exact lines |
| Keys are local, not `provider:<id>` | `identity-map-conventions.md:25-27` | CONFIRMED | exact; zero `provider:` strings in registry or module |
| Manager-Database authoritative for `provider` joins | `identity-map-conventions.md:100-101` | CONFIRMED | exact |
| Repeat runs suffix `_1`, `_2` | `gui_runner.md:51-54` | CONFIRMED | exact |
| `manifest_schema_version: "counter-risk-manifest/v1"` | `manifest_schema.py:12` | CONFIRMED | `MANIFEST_SCHEMA_VERSION` at line 12 exactly |
| `input_hashes` keyed by logical names | — | CONFIRMED | `manifest.py:110`; `config.py:89`; `README.md:124-125` |
| EMITS manifest / evidence / langsmith-fleet | `pipeline/evidence.py`, `langsmith_fleet.py` | CONFIRMED | all present and called from `run.py` |
| `run-contract/v1` documented only, no `run.json` | `run-contract-v1.md:16-17` | CONFIRMED | doc says "No participant emits an envelope yet"; **0** `run.json` matches in `src/` |
| Backplane workflow skips absent emitter | `backplane-conformance.yml:49-55` | CONFIRMED | "No emitter wired yet; the conformance gate will skip (opt-in)." |
| `evidence-object/v1`, `identity_refs` documented only | `identity-map-conventions.md:134-137` | CONFIRMED | exact |
| `capability-bundle/v1` documented only | — | CONFIRMED | no emitter in `src/` |

## §8 — Claims vs reality (checked hardest)

| Dossier claim | Cite | Verdict | Correct statement |
| --- | --- | --- | --- |
| LangChain chat "instead of stubs"; offline stub remains | `README.md:157-158`, `chat/session.py:206-211` | CONFIRMED | `_LocalStubProvider` at :206-211; gated on `COUNTER_RISK_CHAT_OFFLINE_MODE=1` (`README.md:169-170`) |
| **`severity: fail` breaches still yield YELLOW, not RED** | `data_quality.py:21` | **WRONG** | Fail-severity breaches **do** escalate to RED. `data_quality.py:229-248` sets `severity="fail"` when `fail_breach_count > 0` or `max_severity == "fail"`; `_derive_overall_status` (`:392-397`) returns `"fail"`; `manifest.py:27` maps `fail`→`RED`. Asserted by `tests/pipeline/test_manifest_data_quality.py:234` (`overall_status == "fail"`). Line 21's `"warn"` is only the `_SEVERITY_BY_CODE` **default**, consumed by `_make_finding` (`:404-414`) when no explicit severity is passed — i.e. warning-only breaches. |
| Research backplane: no `run.json` emitted | `run-contract-v1.md` | CONFIRMED | 0 matches in `src/` |
| Packaged operator path: launcher exists, blockers documented | `gui_runner.md:24-26`, `AUDIT_REPORT.md:9-11` | CONFIRMED (cite-drift) | quotes exact; path is `docs/audit/AUDIT_REPORT.md`. Frozen-bundle state itself UNVERIFIABLE off-Windows |
| Browser app fixture-only, no WASM | `web/index.html:57-59` | CONFIRMED | exact; zero `pyodide`/`wasm`/`stlite` strings |
| Audit BLOCKER on mixed limit denominators "**possibly** stale" | `limits.py:246-275` | **WRONG (understated)** | Definitively **fixed**, not "possibly". `check_limits` builds `denominator_by_entity_type` (`limits.py:246-248`) and divides by the per-`entity_type` denominator (`:272-274`); scoping via `_denominator_rows_for_entity_type` (`:136-147`) against `_ENTITY_GRANULARITY` (`:36-42`). The gap the audit named ("nothing exercises `_build_limit_exposure_rows` -> `check_limits` together") is closed by `tests/compute/test_limits.py:148` `test_percent_of_total_scopes_denominator_to_matching_granularity` and `tests/pipeline/test_run_pipeline.py:262` |
| HHI sign handling fixed | `rollups.py:583` | CONFIRMED | `_exposure_magnitude` applied before share/square at `:583`; HHI at `:593` |

## §7 / §2 / §11 — gap statements that restate §8

| Dossier claim | Cite | Verdict | Correct statement |
| --- | --- | --- | --- |
| **Runner.xlsm buttons inert, no Form Controls → "Scaffold"** | `AUDIT_REPORT.md:63-64`, `REMAINING_WORK.md:28-29` | **WRONG** | `Runner.xlsm` now ships **7 Form-Control buttons wired to VBA**: `xl/drawings/vmlDrawing1.vml` carries `FmlaMacro` refs `RunAll_Click`, `RunExTrend_Click`, `RunTrend_Click`, `OpenOutputFolder_Click`, `OpenManifest_Click`, `OpenSummary_Click`, `OpenPPTFolder_Click`; `xl/worksheets/sheet1.xml` references `legacyDrawing`; the `Config` sheet is present with 7 `RunnerConfig_*` Named Ranges (builder: `build/xlsm.py:124-137`). Residual: no "Ask about this run" control (no `Ask` string in the VML) |
| **GUI discover calls `input()`** | `io/discover.py:243`, `REMAINING_WORK.md:17-18` | **WRONG** | Not on the GUI path. `gui/runner.py:466` builds `_DiscoveryPromptBridge` (`:338-360`, marshals to the Tk main thread) and `:539` installs it via `set_discovery_selection_prompt`; `resolve_discovery_selections` prefers the installed callback (`discover.py:312-315`) and `DiscoverySelectionRequiredError` is caught at `gui/runner.py:547`. `non_interactive_discovery_prompt` (`discover.py:288-297`) fails fast elsewhere. The `input()` at `discover.py:243` is the **bare-CLI** fallback only |
| **GUI freezes on main thread; surfaces raw exit codes** | `AUDIT_REPORT.md:67-68` | **WRONG (stale)** | Both fixed. Run executes on a worker thread (`gui/runner.py:588-590`) and returns via `root.after(0, _finish)` (`:573`); failures go through `format_gui_run_failure` (`runner_launch.py:86-96`) → `format_launch_error_for_runner` → `map_runner_error_to_operator_message`, plus `_show_operator_error` |
| PR Gate runs `not release and not slow` | `pr-00-gate.yml:76-77` | CONFIRMED | `pytest_markers` at `:76` |
| Main CI: 80% coverage on 3.12/3.13 | `ci.yml:31-32` | CONFIRMED (cite-drift) | `python-versions` at `:28`, `coverage: true` at `:30`, `coverage-min: '80'` at `:31` |
| ~160 test modules | — | CONFIRMED | exactly 160 `test_*.py` |
| Alpha classifier | `pyproject.toml:25` | CONFIRMED | exact |
| `canonical_key` not exported for fleet joins | `identity-map-conventions.md:25-27` | CONFIRMED | still true |
| audit-fix branch not merged | `REMAINING_WORK.md:16-37` | **UNVERIFIABLE / stale doc** | Branch status not visible from the clone, but items #6, #7, #9, #10 and #17 from that "NOT yet done" list are demonstrably **on main** (see rows above). Treat `REMAINING_WORK.md` as a historical record, not current state |

## §6 / §9 / §10

| Claim | Cite | Verdict | Note |
| --- | --- | --- | --- |
| Inputs: MOSERS/NISA xlsx, 3yr historical, monthly PPT, CPRS, optional repo cash CSV/XLSX/PDF | `README.md:55-71` | **CITE-DRIFT** | Substance right, cite wrong: `README.md:55-71` is the *Repo Cash Source Configuration* section only. The full input set is `config.py:89-108` (`hist_*_3yr_xlsx` and `monthly_pptx` are the only non-optional paths); `cash_source_type` includes `pdf` at `config.py:92` |
| Optional chat deps | `pyproject.toml:39-40` | CONFIRMED | exact |
| LangSmith opt-in | `langsmith_fleet.md:37-40` | CONFIRMED | exact; `no_secret` status without a key |
| Libraries incl. `stranske-pdf-extract`, `pywin32` win32-only | `pyproject.toml:33-42` | CONFIRMED | exact; `pywin32` marker at `:42` |
| PyInstaller operator bundle | `gui_runner.md:9-13` | CONFIRMED | `pyinstaller release.spec` |
| `.github/` owned by Workflows | `AGENTS.md:48-51` | CONFIRMED | exact |
| Collision risk: local `citibank` key, no `provider:` prefix | — | CONFIRMED | `config/name_registry.yml:9`; zero `provider:` strings |
| All 8 reuse-candidate paths | §10 table | CONFIRMED | 11/11 cited paths exist (incl. `scripts/validate_run_contract.py`, `renderers/table_png.py`) |
| CLI entry points | `pyproject.toml:71,75` | CONFIRMED | `mapping_diff_report` at `:71`, `counter-risk` at `:75` |
| Mapping diff CLI usage | `docs/name_registry.md:60-65` | CONFIRMED | exact |
| COM PPT needs Windows | — | UNVERIFIABLE (off-platform) | `pywin32` marker confirmed; runtime not testable on macOS |

## Path corrections applied to the dossier

`AUDIT_REPORT.md` → `docs/audit/AUDIT_REPORT.md`; `REMAINING_WORK.md` → `docs/audit/REMAINING_WORK.md`; `audit/20-functionality-wiring.md` → `docs/audit/20-functionality-wiring.md`; `audit/10-parsers.md` → `docs/audit/10-parsers.md`. Neither audit file exists at the repo root.
