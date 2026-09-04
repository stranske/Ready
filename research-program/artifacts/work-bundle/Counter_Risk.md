# Counter_Risk — dossier (2026-09-04)

## 1. Purpose in one paragraph

Counter_Risk replaces the legacy MOSERS spreadsheet workflow for monthly counterparty exposure reporting (`README.md:3-4`). It ingests MOSERS/NISA Excel workbooks, CPRS clearing-house and FCM files, and optional repo-cash sources, then produces updated historical Excel workbooks, a refreshed monthly PowerPoint, and a timestamped run folder with audit artifacts (`README.md:10-19`). Non-technical operators are meant to run it via a packaged Windows executable, Tkinter GUI, or Excel macro workbook—not by cloning the repo (`README.md:6-8`). The pipeline is local-first (files on disk); optional LangChain chat and LangSmith tracing need credentials when enabled (`README.md:155-178`).

## 2. Who uses it and how (surfaces)

| Surface | Entry point | Who uses it | Status | Evidence |
| --- | --- | --- | --- | --- |
| CLI | `counter-risk` → `counter_risk.cli:main` (`pyproject.toml:75`) | Maintainers; CI | **Working** | `README.md:182-189`; `tests/pipeline/test_run_pipeline.py` |
| GUI (Tkinter) | `counter-risk gui` (`docs/gui_runner.md:29`) | Windows operators | **Working** (unverified on Windows) | Runs on a worker thread (`gui/runner.py:588-590`) returning via `root.after` (`:573`); operator-facing errors via `format_gui_run_failure` (`runner_launch.py:86-96`); Tk discovery-selection dialog (`gui/runner.py:338-360,466,539`); headless smoke (`gui_runner.md:57-59`) |
| Excel macro workbook | `Runner.xlsm` | Intended primary operators | **Working** (one gap) | 7 Form-Control buttons wired to VBA via `xl/drawings/vmlDrawing1.vml` (`RunAll_Click`…`OpenPPTFolder_Click`), `legacyDrawing` in `sheet1.xml`, `Config` sheet + 7 `RunnerConfig_*` Named Ranges (builder `build/xlsm.py:124-137`). Gap: no "Ask about this run" control |
| Static HTML demo | `web/index.html` | Demo/CI only | **Fixture-only** | "fixture-only and no-egress" (`web/index.html:57-59`) |
| Run artifacts | `pipeline/run.py` output folder | Operators; review | **Working** (caveats) | `manifest.json` validated pre-write (`pipeline/manifest.py:194-196`); PPT COM needs Windows + `pywin32` (`pyproject.toml:42`) |
| Chat assistant | `counter_risk.chat.session` | Optional operator Q&A | **Partial** | LangChain when credentialed (`README.md:157-158`); offline stub via `OFFLINE_MODE=1` (`chat/session.py:206-211`) |
| Mapping diff CLI | `mapping_diff_report` (`pyproject.toml:71`) | Registry maintainers | **Working** | `docs/name_registry.md:60-65` |
| Fleet NDJSON | `observability/langsmith_fleet.py` | Fleet dashboard | **Working** | emitted from `pipeline/run.py:626`; contract per `docs/langsmith_fleet.md:3-6` |

## 3. Structure map

```
Counter_Risk/
├── src/counter_risk/   # CLI, pipeline, parsers, writers, compute, chat, GUI
├── config/             # Workflow YAML, name_registry, limits
├── tests/              # 160 test modules
├── docs/               # Runbooks, contracts, audit reports (docs/audit/)
├── scripts/            # CI helpers, validate_run_contract.py
├── templates/, assets/templates/  # Excel/PPT templates for writers
├── Runner.xlsm         # Operator macro workbook (button-driven)
├── web/                # Static fixture-replay demo page
├── .github/            # CI/Gate — synced from stranske/Workflows
└── design-system/, node_modules/  # Not on operator path; boilerplate/dev
```

`src/counter_risk/pipeline/` orchestrates the monthly run. `parsers/` reads vendor Excel/PDF layouts. `writers/` and `outputs/` emit workbooks and staged PPT artifacts. `compute/` holds concentration, limits, and risk proxies. `docs/contracts/` ships fleet schemas (mostly not emitted yet). `docs/audit/` holds the 2026 in-repo audit — **historical, partly superseded** (see §8). `.github/` workflow logic is owned by `stranske/Workflows` (`AGENTS.md:48-51`).

## 4. Major code features you must understand to extend it

- **Pipeline orchestration (`pipeline/run.py`)** — Single integration point: parse → reconcile → compute → write → manifest. Consumes `WorkflowConfig` and file paths; produces all run artifacts.

- **Workflow config (`config.py`, `config/*.yml`)** — Pydantic YAML with `extra="forbid"` (`config.py:18,27,36,85`); defines inputs (`config.py:87-121`), reconciliation policy, cash sources, and pluggable `output_generators` stages (`README.md:22-51`, field at `config.py:118-120`).

- **Parsers (`parsers/nisa*.py`, `cprs_ch.py`, `cprs_fcm.py`, `daily_holdings_pdf.py`)** — Extract counterparty totals and futures from MOSERS/CPRS layouts; typed failures via `pipeline/parsing_types.py`.

- **Name registry (`name_registry.py`, `config/name_registry.yml`)** — Maps raw spellings to stable `canonical_key` + `display_name` (`docs/name_registry.md:7-12`); used by reconciliation, writers, and limits.

- **Reconciliation (`pipeline/reconciliation.py`)** — Compares parsed names to historical headers and registry inclusion; `strict` vs `warn` policy from config (`docs/audit/20-functionality-wiring.md:11`).

- **MOSERS writers (`writers/mosers_workbook.py`, `historical_update.py`)** — Builds variant workbooks and appends historical rows; stamps `as_of_date` when provided (`mosers_workbook.py:121-123`).

- **Output registry (`outputs/registry.py`)** — Stage-based PPT/historical generators; the four stages (`historical`, `ppt_master`, `ppt_refresh`, `ppt_post_distribution`) are the enum at `config.py:40`.

- **Compute (`compute/rollups.py`, `compute/limits.py`)** — `concentration_metrics.csv`, optional `risk_rankings.csv`, `limit_breaches.csv` (`docs/concentration_metrics.md`, `docs/limit_monitoring.md`). `check_limits` scopes each `percent_of_total` denominator to the limit's own `entity_type` granularity (`limits.py:246-248,272-274`; granularity map `:36-42`).

- **Manifest (`pipeline/manifest.py`, `evidence.py`, `manifest_schema.py`)** — `counter-risk-manifest/v1` (`manifest_schema.py:12`) with hashes, provenance, data-quality, and per-exposure evidence pointers (`README.md:122-127`); validated before write (`manifest.py:194-196`); status colour map `manifest.py:27`.

- **LangSmith fleet (`observability/langsmith_fleet.py`)** — Dashboard-safe NDJSON without raw positions (`docs/langsmith_fleet.md`), written at `pipeline/run.py:626`.

- **Chat (`chat/session.py`, `chat/providers/langchain_runtime.py`)** — Optional LLM run explanations; not on the critical reporting path.

## 5. Data model, identifiers and contracts

**Entities.** Counterparties use `canonical_key` in `config/name_registry.yml` (snake_case) with `aliases` and `display_name` (`name_registry.py:76-78`). Keys are local—not emitted as fleet `provider:<id>` strings (`docs/contracts/identity-map-conventions.md:25-27`). Manager-Database is declared authoritative for cross-repo `provider` joins (`identity-map-conventions.md:100-101`).

**Runs.** File-based persistence under operator output root; repeat runs suffix `_1`, `_2` (`gui_runner.md:51-54`). `manifest.json` uses `manifest_schema_version: "counter-risk-manifest/v1"` (`manifest_schema.py:12`) and SHA-256 `input_hashes` keyed by logical names like `mosers_all_programs_xlsx` (`manifest.py:110`; `config.py:89`; `README.md:124-125`).

| Contract | Emits / consumes |
| --- | --- |
| `counter-risk-manifest/v1` | **EMITS** — `ManifestBuilder`, `validate_manifest` |
| Manifest `evidence` on exposures | **EMITS** — `pipeline/evidence.py` (local shape, not full `evidence-object/v1`) |
| `langsmith-fleet/v1` | **EMITS** — `langsmith_fleet.py`, from `run.py:626` |
| `run-contract/v1`, `artifact-manifest/v1` | **Documented only** — zero `run.json` matches in `src/`; validator at `scripts/validate_run_contract.py`; backplane workflow skips absent emitters (`docs/contracts/run-contract-v1.md:16-17`, `backplane-conformance.yml:49-55`) |
| `evidence-object/v1`, `identity_refs` | **Documented only** — schemas present, no standalone emission (`identity-map-conventions.md:134-137`) |
| `capability-bundle/v1` | **Documented only** — Workflows keepalive contract |

## 6. External inputs and dependencies

**Inputs:** MOSERS/NISA Excel, 3-year historical workbooks, monthly PPT template, CPRS files, optional repo-cash CSV/XLSX/PDF — the authoritative set is the `WorkflowConfig` field list at `config.py:89-108`, where only `hist_all_programs_3yr_xlsx`, `hist_ex_llc_3yr_xlsx`, `hist_llc_3yr_xlsx` and `monthly_pptx` are required; repo-cash layering is documented at `README.md:55-71` and `cash_source_type` accepts `pdf` (`config.py:92`). No live market APIs in the core path.

**LLM/agents:** Optional chat via `langchain-openai` / `langchain-anthropic` (`pyproject.toml:39-40`); LangSmith opt-in, records `telemetry-offline flag` without a key (`langsmith_fleet.md:37-40`). GitHub agent workflows are repo automation from `stranske/Workflows`, not part of the monthly run.

**Libraries:** `openpyxl`, `python-pptx`, `pandas`, `Pillow`, `stranske-pdf-extract` (Workflows git dep), `pywin32` on Windows for COM (`pyproject.toml:33-42`). Maintainers use Python 3.12+; operators target the PyInstaller bundle (`gui_runner.md:9-13`). No Docker on the operator path.

## 7. Current state

**CI:** 160 test modules. PR Gate runs `not release and not slow` (`pr-00-gate.yml:76`). Main CI enforces 80% coverage on Python 3.12/3.13 (`ci.yml:28,30-31`). Package status: Alpha (`pyproject.toml:25`).

**Usable today:** Maintainer CLI with fixtures (`tests/pipeline/test_run_pipeline.py`). The two operator surfaces the 2026 in-repo audit called BLOCKERs are now wired: `Runner.xlsm` has real Form-Control buttons bound to its VBA macros, and the Tk GUI runs off the main thread with a discovery-selection dialog and operator-facing error text (see §2). What remains unproven is the **frozen Windows bundle** — PyInstaller path resolution and the packaged tkinter GUI have not been exercised on Windows from this repo, and that verification cannot be done off-platform.

**Top gaps:** (1) no `run.json` / backplane envelope emitter (`docs/contracts/run-contract-v1.md:16-17`); (2) `canonical_key` not exported with a `provider:` prefix for fleet joins (`identity-map-conventions.md:25-27`); (3) frozen-bundle + Windows operator verification outstanding, including the absent operator run doc (`docs/audit/AUDIT_REPORT.md:71`); (4) `Runner.xlsm` "Ask about this run" has no control or handler; (5) `docs/audit/REMAINING_WORK.md` is stale — several items in its "NOT yet done" list (#6 XLSM buttons, #7 discover `input()`, #9 worker thread, #10 error messages, #17 `as_of_date`) are on `main`, so it should not be read as a live backlog.

## 8. Claims vs reality

- **LangChain chat "instead of stubs"** (`README.md:157-158`) — True when credentialed; the offline stub remains for tests, gated on `OFFLINE_MODE=1` (`chat/session.py:206-211`, `README.md:169-170`).

- **Standard limit/concentration outputs** (`README.md:17-19`) — Produced when config resolves. **Correction to a widely-repeated claim:** fail-severity limit breaches *do* escalate the data-quality status to RED. `pipeline/data_quality.py:229-248` passes `severity="fail"` whenever `fail_breach_count > 0` or `max_severity == "fail"`; `_derive_overall_status` (`:392-397`) then returns `"fail"`, which `manifest.py:27` renders as `RED`, asserted by `tests/pipeline/test_manifest_data_quality.py:234`. The `"LIMIT_BREACHES": "warn"` entry at `data_quality.py:21` is only the `_SEVERITY_BY_CODE` **default** consumed by `_make_finding` (`:404-414`) when no explicit severity is supplied — i.e. warning-only breaches. The in-repo audit's contrary BLOCKER (`docs/audit/AUDIT_REPORT.md:9`, citing the pre-fix `data_quality.py:20`) is **stale**.

- **Research backplane run envelope** (`docs/contracts/run-contract-v1.md`) — Documented and validatable; the pipeline does not emit `run.json` (zero matches in `src/`), and the doc itself states no participant emits an envelope yet.

- **Packaged operator path** (`gui_runner.md:24-26`) — Launcher and `run_counter_risk_gui.cmd` exist. The audit's XLSM and GUI blockers are resolved; its frozen-bundle path-resolution finding is **unverifiable off-Windows** and should be treated as open.

- **Browser app** — `web/index.html` is explicitly fixture-only (`web/index.html:57-59`); no WASM runtime (no `pyodide`/`wasm`/`stlite` references).

- **Audit BLOCKER on mixed limit denominators** (`docs/audit/20-functionality-wiring.md:45-53`) — **Fixed, not merely stale.** `check_limits` computes `denominator_by_entity_type` up front (`limits.py:246-248`) and divides matched notional by the denominator for that limit's own `entity_type` (`:272-274`), scoped by `_denominator_rows_for_entity_type` (`:136-147`) against `_ENTITY_GRANULARITY` (`:36-42`). The specific coverage hole the audit named — "nothing exercises `_build_limit_exposure_rows` -> `check_limits` together" — is closed by `tests/compute/test_limits.py:148` (`test_percent_of_total_scopes_denominator_to_matching_granularity`) and `tests/pipeline/test_run_pipeline.py:262`.

- **Audit BLOCKER "GUI discover mode calls `input()`"** (`docs/audit/AUDIT_REPORT.md:64`) — **Wrong for the current GUI.** `gui/runner.py:466` constructs `_DiscoveryPromptBridge` (`:338-360`), which marshals selection onto the Tk main thread, and `:539` installs it via `set_discovery_selection_prompt`; `resolve_discovery_selections` prefers the installed callback (`io/discover.py:312-315`), and `DiscoverySelectionRequiredError` is caught at `gui/runner.py:547`. The stdin `input()` at `io/discover.py:243` is the bare-CLI fallback only.

- **Audit BLOCKER "Runner.xlsm buttons are inert text"** (`docs/audit/AUDIT_REPORT.md:63`) — **Wrong for the shipped workbook.** `xl/drawings/vmlDrawing1.vml` carries seven `FmlaMacro` bindings (`RunAll_Click`, `RunExTrend_Click`, `RunTrend_Click`, `OpenOutputFolder_Click`, `OpenManifest_Click`, `OpenSummary_Click`, `OpenPPTFolder_Click`), `xl/worksheets/sheet1.xml` references `legacyDrawing`, and the `Config` sheet the VBA reads is present with its 7 `RunnerConfig_*` Named Ranges (builder `build/xlsm.py:124-137`). Still true: no "Ask about this run" control.

- **Audit MAJORs "GUI freezes on Tk main thread" / "surfaces raw exit codes"** (`docs/audit/AUDIT_REPORT.md:67-68`) — Both **resolved**: worker thread at `gui/runner.py:588-590` with `root.after(0, _finish)` (`:573`); failures formatted by `format_gui_run_failure` → `format_launch_error_for_runner` → `map_runner_error_to_operator_message` (`runner_launch.py:86-96`).

- **HHI sign handling** (`rollups.py:583`) — Magnitudes are taken via `_exposure_magnitude` before shares are computed (`:583`), so the HHI at `:593` sums squared absolute shares.

## 9. Interoperability hooks (for the fleet program)

**Offers:** `manifest.json` (exposures, evidence, data-quality, hashes); `concentration_metrics.csv`; `limit_breaches.csv`; optional risk-proxy CSVs; `langsmith-fleet.ndjson`; mapping-diff output; `name_registry.yml` as local alias authority.

**Consumes (planned):** Manager-Database `manager:`/`provider:` IDs; Pension-Data fund/pension IDs—neither wired in code today. Workflows `run-contract/v1` orchestration when an emitter lands.

**Collision risks:** Local `canonical_key` (e.g. `citibank`, `config/name_registry.yml:9`) lacks a `provider:` prefix—naïve joins with Manager-Database will fragment; there is not a single `provider:` string in the registry or `name_registry.py`. Variant names (`all_programs`, `ex_trend`, `trend`) are MOSERS-specific. `input_hashes` keys are Counter_Risk-local logical names.

## 10. Reuse candidates

| Component | Path |
| --- | --- |
| Name registry + validation | `name_registry.py`, `config/name_registry.yml` |
| Mapping diff report | `reports/mapping_diff.py`, `cli/mapping_diff_report.py` |
| Manifest builder + schema | `pipeline/manifest.py`, `manifest_schema.py` |
| LangSmith fleet emitter | `observability/langsmith_fleet.py` |
| CPRS raw XLSX reader | `parsers/_xlsx_reader.py` |
| Output generator registry | `outputs/registry.py` |
| Run-contract validator | `scripts/validate_run_contract.py` |
| Pure-Python table PNG | `renderers/table_png.py` |
| XLSM Config-sheet + Named-Range injector | `build/xlsm.py` |

## 11. Proposed direction (evidence-based)

**Finish scaffolded:** Emit `run.json` + `scripts/emit_reference_run.sh` so the backplane conformance gate stops skipping (`backplane-conformance.yml:49-55`); export `provider:<canonical_key>` identity refs (`identity-map-conventions.md:134-137`); add the "Ask about this run" control + handler to `Runner.xlsm`; write the operator-facing Windows run doc and verify the frozen bundle end-to-end on Windows (`docs/audit/AUDIT_REPORT.md:71`) — this is the only remaining BLOCKER-class item, and it needs a real Windows host.

**Housekeeping that prevents repeat errors:** `docs/audit/REMAINING_WORK.md` and the BLOCKER list in `docs/audit/AUDIT_REPORT.md:9-11` are now materially wrong about `main` and are being cited downstream as current state. Either stamp them "historical — superseded <date>" or fold the surviving items into issues, so the next reader does not re-report fixed defects.

**New capability:** Cross-validate registry keys against Manager-Database exports; consolidate numeric coercers (`docs/audit/10-parsers.md`); resolve the hanging slow test noted in `docs/audit/REMAINING_WORK.md` so a full-suite number is trustworthy.

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- This tool automates the monthly counterparty exposure package that used to live in MOSERS spreadsheets—Excel history, board PowerPoint, and an auditable run folder.
- Operators should use a Windows button (desktop app or Excel workbook), not GitHub; both button surfaces are now wired, though the packaged Windows bundle has not been proven on a Windows machine.
- Every run writes a manifest and plain-language data-quality summary; review yellow and red before distributing—a hard limit breach does now show red.
- New bank name spellings in source files need a registry update before charts and limits pick them up correctly.
- Fleet-wide shared run records and global entity IDs are documented but not yet emitted—treat this repo's CSV and JSON run files as the interoperability surface for now. And be careful with the review documents stored inside this repo: they predate several fixes and are wrong about the current state in at least four places, so check the working code before repeating one of their findings.
*Evidence-checked against source repositories; verification metadata omitted from work bundle.*
