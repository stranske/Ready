# Counter_Risk — dossier (2026-09-04)

## 1. Purpose in one paragraph

Counter_Risk replaces the legacy MOSERS spreadsheet workflow for monthly counterparty exposure reporting (`README.md:3-4`). It ingests MOSERS/NISA Excel workbooks, CPRS clearing-house and FCM files, and optional repo-cash sources, then produces updated historical Excel workbooks, a refreshed monthly PowerPoint, and a timestamped run folder with audit artifacts (`README.md:10-19`). Non-technical operators are meant to run it via a packaged Windows executable, Tkinter GUI, or Excel macro workbook—not by cloning the repo (`README.md:6-8`). The pipeline is local-first (files on disk); optional LangChain chat and LangSmith tracing need credentials when enabled (`README.md:155-178`).

## 2. Who uses it and how (surfaces)

| Surface | Entry point | Who uses it | Status | Evidence |
| --- | --- | --- | --- | --- |
| CLI | `counter-risk` → `counter_risk.cli:main` (`pyproject.toml:75`) | Maintainers; CI | **Working** | `README.md:182-189`; `tests/pipeline/test_run_pipeline.py` |
| GUI (Tkinter) | `counter-risk gui` (`docs/gui_runner.md:29`) | Windows operators | **Partial** | Headless smoke exists (`gui_runner.md:57-59`); audit flags UI freeze and raw errors (`AUDIT_REPORT.md:67-68`) |
| Excel macro workbook | `Runner.xlsm` | Intended primary operators | **Scaffold** | Buttons inert, no Form Controls (`AUDIT_REPORT.md:63-64`, `REMAINING_WORK.md:28-29`) |
| Static HTML demo | `web/index.html` | Demo/CI only | **Fixture-only** | "fixture-only and no-egress" (`web/index.html:57-59`) |
| Run artifacts | `pipeline/run.py` output folder | Operators; review | **Working** (caveats) | `manifest.json` validated pre-write (`manifest.py:194-196`); PPT COM needs Windows + `pywin32` |
| Chat assistant | `counter_risk.chat.session` | Optional operator Q&A | **Partial** | LangChain when credentialed (`README.md:157-158`); offline stub via `COUNTER_RISK_CHAT_OFFLINE_MODE=1` |
| Mapping diff CLI | `mapping_diff_report` (`pyproject.toml:71`) | Registry maintainers | **Working** | `docs/name_registry.md:60-65` |
| Fleet NDJSON | `observability/langsmith_fleet.py` | Fleet dashboard | **Working** | `langsmith-fleet.ndjson` per `docs/langsmith_fleet.md:3-6` |

## 3. Structure map

```
Counter_Risk/
├── src/counter_risk/   # CLI, pipeline, parsers, writers, compute, chat, GUI
├── config/             # Workflow YAML, name_registry, limits
├── tests/              # ~160 test modules
├── docs/               # Runbooks, contracts, audit reports
├── scripts/            # CI helpers, validate_run_contract.py
├── templates/          # Excel/PPT templates for writers
├── web/                # Static fixture-replay demo page
├── .github/            # CI/Gate — synced from stranske/Workflows
└── design-system/, node_modules/  # Not on operator path; boilerplate/dev
```

`src/counter_risk/pipeline/` orchestrates the monthly run. `parsers/` reads vendor Excel/PDF layouts. `writers/` and `outputs/` emit workbooks and staged PPT artifacts. `compute/` holds concentration, limits, and risk proxies. `docs/contracts/` ships fleet schemas (mostly not emitted yet). `.github/` workflow logic is owned by `stranske/Workflows` (`AGENTS.md:48-51`).

## 4. Major code features you must understand to extend it

- **Pipeline orchestration (`pipeline/run.py`)** — Single integration point: parse → reconcile → compute → write → manifest. Consumes `WorkflowConfig` and file paths; produces all run artifacts.

- **Workflow config (`config.py`, `config/*.yml`)** — Pydantic YAML with `extra="forbid"`; defines inputs, reconciliation policy, cash sources, and pluggable `output_generators` stages (`README.md:24-51`).

- **Parsers (`parsers/nisa*.py`, `cprs_ch.py`, `cprs_fcm.py`, `daily_holdings_pdf.py`)** — Extract counterparty totals and futures from MOSERS/CPRS layouts; typed failures via `pipeline/parsing_types.py`.

- **Name registry (`name_registry.py`, `config/name_registry.yml`)** — Maps raw spellings to stable `canonical_key` + `display_name` (`docs/name_registry.md:7-12`); used by reconciliation, writers, and limits.

- **Reconciliation (`pipeline/reconciliation.py`)** — Compares parsed names to historical headers and registry inclusion; `strict` vs `warn` policy from config (`audit/20-functionality-wiring.md:11`).

- **MOSERS writers (`writers/mosers_workbook.py`, `historical_update.py`)** — Builds variant workbooks and appends historical rows; stamps `as_of_date` when provided (`mosers_workbook.py:121-123`).

- **Output registry (`outputs/registry.py`)** — Stage-based PPT/historical generators (`historical`, `ppt_master`, `ppt_refresh`, `ppt_post_distribution`).

- **Compute (`compute/rollups.py`, `compute/limits.py`)** — `concentration_metrics.csv`, optional `risk_rankings.csv`, `limit_breaches.csv` (`docs/concentration_metrics.md`, `docs/limit_monitoring.md`).

- **Manifest (`pipeline/manifest.py`, `evidence.py`, `manifest_schema.py`)** — `counter-risk-manifest/v1` with hashes, provenance, data-quality, and per-exposure evidence pointers (`README.md:122-127`); validated before write (`manifest.py:194-196`).

- **LangSmith fleet (`observability/langsmith_fleet.py`)** — Dashboard-safe NDJSON without raw positions (`docs/langsmith_fleet.md`).

- **Chat (`chat/session.py`, `chat/providers/langchain_runtime.py`)** — Optional LLM run explanations; not on the critical reporting path.

## 5. Data model, identifiers and contracts

**Entities.** Counterparties use `canonical_key` in `config/name_registry.yml` (snake_case) with `aliases` and `display_name` (`name_registry.py:76-78`). Keys are local—not emitted as fleet `provider:<id>` strings (`identity-map-conventions.md:25-27`). Manager-Database is declared authoritative for cross-repo `provider` joins (`identity-map-conventions.md:100-101`).

**Runs.** File-based persistence under operator output root; repeat runs suffix `_1`, `_2` (`gui_runner.md:51-54`). `manifest.json` uses `manifest_schema_version: "counter-risk-manifest/v1"` (`manifest_schema.py:12`) and SHA-256 `input_hashes` keyed by logical names like `mosers_all_programs_xlsx`.

| Contract | Emits / consumes |
| --- | --- |
| `counter-risk-manifest/v1` | **EMITS** — `ManifestBuilder`, `validate_manifest` |
| Manifest `evidence` on exposures | **EMITS** — `pipeline/evidence.py` (local shape, not full `evidence-object/v1`) |
| `langsmith-fleet/v1` | **EMITS** — `langsmith_fleet.py` |
| `run-contract/v1`, `artifact-manifest/v1` | **Documented only** — no `run.json` in pipeline; validator at `scripts/validate_run_contract.py`; backplane workflow skips (`run-contract-v1.md:16-17`, `backplane-conformance.yml:49-55`) |
| `evidence-object/v1`, `identity_refs` | **Documented only** — schemas present, no standalone emission |
| `capability-bundle/v1` | **Documented only** — Workflows keepalive contract |

## 6. External inputs and dependencies

**Inputs:** MOSERS/NISA Excel, 3-year historical workbooks, monthly PPT template, CPRS files, optional repo-cash CSV/XLSX/PDF (`README.md:55-71`). No live market APIs in the core path.

**LLM/agents:** Optional chat via `langchain-openai` / `langchain-anthropic` (`pyproject.toml:39-40`); LangSmith opt-in (`langsmith_fleet.md:37-40`). GitHub agent workflows are repo automation from `stranske/Workflows`, not part of the monthly run.

**Libraries:** `openpyxl`, `python-pptx`, `pandas`, `Pillow`, `stranske-pdf-extract` (Workflows git dep), `pywin32` on Windows for COM (`pyproject.toml:33-42`). Maintainers use Python 3.12+; operators target PyInstaller bundle (`gui_runner.md:9-13`). No Docker on the operator path.

## 7. Current state

**CI:** ~160 test modules. PR Gate runs `not release and not slow` (`pr-00-gate.yml:76-77`). Main CI enforces 80% coverage on Python 3.12/3.13 (`ci.yml:31-32`). Package status: Alpha (`pyproject.toml:25`).

**Usable today:** Maintainer CLI with fixtures (`tests/pipeline/test_run_pipeline.py`). **Not production-ready** for no-install Windows operators per in-repo audit (`AUDIT_REPORT.md:11`): Runner.xlsm unwired, GUI discover calls `input()` (`io/discover.py:243`), COM PPT needs `pywin32`. Backplane `run.json` emitter absent.

**Top gaps:** (1) Runner buttons inert (`AUDIT_REPORT.md:63-64`); (2) GUI discover/`input()` (`REMAINING_WORK.md:17-18`); (3) `LIMIT_BREACHES` coded as warn not fail (`data_quality.py:21`); (4) no `run.json` (`run-contract-v1.md:16-17`); (5) `canonical_key` not exported for fleet joins (`identity-map-conventions.md:25-27`); (6) audit-fix branch not merged (`REMAINING_WORK.md:16-37`). Note: some audit calc findings (limit denominator, HHI sign) appear fixed on current `main` (`limits.py:246-275`, `rollups.py:583`)—re-verify before trusting.

## 8. Claims vs reality

- **LangChain chat "instead of stubs"** (`README.md:157-158`) — True when credentialed; offline stub remains for tests (`chat/session.py:206-211`).

- **Standard limit/concentration outputs** (`README.md:17-19`) — Produced when config resolves; `severity: fail` breaches still yield YELLOW data-quality status (`data_quality.py:21`), not RED.

- **Research backplane run envelope** (`run-contract-v1.md`) — Documented and validatable; pipeline does not emit `run.json` (no matches in `src/`).

- **Packaged operator path** (`gui_runner.md:24-26`) — Launcher exists; audit documents frozen-bundle and XLSM blockers (`AUDIT_REPORT.md:9-11`).

- **Browser app** — `web/index.html` is explicitly fixture-only (`web/index.html:57-59`); no WASM runtime.

- **Audit BLOCKER on mixed limit denominators** (`audit/20-functionality-wiring.md:45-53`) — Possibly stale: `check_limits` now scopes denominators per `entity_type` (`limits.py:246-275`).

## 9. Interoperability hooks (for the fleet program)

**Offers:** `manifest.json` (exposures, evidence, data-quality, hashes); `concentration_metrics.csv`; `limit_breaches.csv`; optional risk-proxy CSVs; `langsmith-fleet.ndjson`; mapping-diff output; `name_registry.yml` as local alias authority.

**Consumes (planned):** Manager-Database `manager:`/`provider:` IDs; Pension-Data fund/pension IDs—neither wired in code today. Workflows `run-contract/v1` orchestration when emitter lands.

**Collision risks:** Local `canonical_key` (e.g. `citibank`) lacks `provider:` prefix—naïve joins with Manager-Database will fragment. Variant names (`all_programs`, `ex_trend`, `trend`) are MOSERS-specific. `input_hashes` keys are Counter_Risk-local logical names.

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

## 11. Proposed direction (evidence-based)

**Finish scaffolded:** Wire Runner.xlsm controls (`AUDIT_REPORT.md:63-64`); fix GUI discover `input()` (`io/discover.py:243`); emit `run.json` + `emit_reference_run.sh` (`backplane-conformance.yml:49-55`); escalate fail-severity limits to RED (`data_quality.py:21`); export `provider:<canonical_key>` identity refs (`identity-map-conventions.md:134-137`).

**New capability:** Cross-validate registry keys against Manager-Database exports; integration test for limit denominators at clearing-house granularity; consolidate numeric coercers (`audit/10-parsers.md`); operator Windows runbook verification (`AUDIT_REPORT.md:71`).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- This tool automates the monthly counterparty exposure package that used to live in MOSERS spreadsheets—Excel history, board PowerPoint, and an auditable run folder.
- Operators should use a Windows button (desktop app or Excel workbook), not GitHub; developers maintain name lists, limits, and workflow settings in this repo.
- Every run writes a manifest and plain-language data-quality summary; review yellow/red before distributing, knowing hard limit breaches may still show yellow today.
- New bank name spellings in source files need a registry update before charts and limits pick them up correctly.
- Fleet-wide shared run records and global entity IDs are documented but not yet emitted—treat this repo's CSV and JSON run files as the interoperability surface for now.
