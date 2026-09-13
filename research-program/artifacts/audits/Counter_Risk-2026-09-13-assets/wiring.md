# Counter_Risk wiring audit — 2026-09-13

**Unit:** `D-audit-Counter_Risk--2026-09-13T18-41-41Z`  
**SHA:** `6e2a87b27be9a23d388155e37ed01675b1e27dc7`  
**Scope:** pipeline / outputs / writers / build / config / runtime_paths / gui / config / web_demo / associated tests  
**Dimensions:** repo-audit d1 (functionality/wiring), d2 (observed UX/status), d3 (contracts/provenance)

## Index

| ID | Severity | Title | Proof |
|----|----------|-------|-------|
| W-1 | **MAJOR** | Manifest `config_snapshot` disagrees with `input_hashes` after NISA MOSERS generation | `wiring-proof-config-snapshot-mismatch.py` |
| W-2 | **MAJOR** | Top-level `ppt_status=skipped` yields `PPT_GENERATION_SKIPPED` when distribution deck succeeded | `wiring-proof-ppt-status-skew.py` |
| W-3 | **MEDIUM** | `export_pdf=True` silently ignored when `enable_distribution_output=False` | `wiring-proof-export-pdf-silent-skip.py` |
| W-4 | **MEDIUM** | `exposure_summary_xlsx` and `screenshot_inputs` omitted from `input_hashes` | `wiring-proof-input-hash-gaps.py` |
| W-5 | **MEDIUM** | Concentration-table append runs after distribution standalone validation | (static order; see W-5) |

**Counts:** 5 new verified findings (2 MAJOR, 3 MEDIUM); 4 refuted/duplicate candidates listed below.

Run proofs from clone root:

```bash
cd <clone> && PYTHONPATH=src .venv/bin/python <artifacts>/wiring-proof-*.py
```

---

## W-1 — Manifest `config_snapshot` disagrees with `input_hashes` after NISA generation

**Severity:** MAJOR (provenance / audit replay defect)

**Evidence**

- `src/counter_risk/pipeline/run.py:1564-1623` — `_prepare_runtime_config` generates `run_dir/*-mosers-input.xlsx` and overwrites `mosers_*_xlsx` on `runtime_config`.
- `src/counter_risk/pipeline/run.py:662-666` — `input_hashes` built from `_resolve_input_paths(runtime_config)` but `ManifestBuilder` receives pre-mutation `config`.
- `src/counter_risk/pipeline/manifest.py:432-442` — `config_snapshot` serializes the `WorkflowConfig` passed to `ManifestBuilder` (the stale object).

**Reachable trigger**

Any workflow with `raw_nisa_*_xlsx` set (documented NISA-first path). Worse when YAML also lists legacy `mosers_*_xlsx`: parsing uses the generated run-dir workbook while the snapshot still shows the external YAML path.

**Expected / actual**

- Expected: `config_snapshot.mosers_all_programs_xlsx` matches the path whose bytes are hashed under `input_hashes["mosers_all_programs_xlsx"]`.
- Actual: snapshot shows `tests/fixtures/MOSERS…` (or `null` when only raw NISA is configured); hash is `run_dir/all_programs-mosers-input.xlsx` with a different SHA-256.

**Proof:** `wiring-proof-config-snapshot-mismatch.py` (PASS at SHA above).

**Disconfirming evidence checked**

- `run_pipeline_with_config` re-serializes config before `run_pipeline`, but `_prepare_runtime_config` mutations are not reflected back into the manifest builder input.
- Tests assert `raw_nisa_*` keys appear in `input_hashes` (`tests/pipeline/test_run_pipeline.py:3509`) but do not assert snapshot/hash path alignment.

**Dedup:** No open issue in `issues.json` for snapshot vs runtime_config divergence.

---

## W-2 — `ppt_status=skipped` misreports successful distribution PPT generation

**Severity:** MAJOR (misleading operator / fleet status)

**Evidence**

- `src/counter_risk/pipeline/run.py:2721-2727,2867-2870` — returned `PptProcessingResult.status` is the **link-refresh** status only, not overall PPT deliverable health.
- `src/counter_risk/pipeline/run.py:2773-2831` — distribution deck is still derived when refresh is `SKIPPED` (non-Windows default).
- `src/counter_risk/pipeline/data_quality.py:217-232` — `ppt_status == "skipped"` always emits `PPT_GENERATION_SKIPPED` (warn).
- `tests/pipeline/test_monthly_pipeline_ppt_outputs.py:336-388` — asserts `ppt_outputs.distribution.status == "success"` with master refresh skipped; does not check data-quality skew.

**Reachable trigger**

Every macOS/Linux CI run and any Windows host without COM link refresh: refresh returns `SKIPPED`, distribution `.pptx` is written, manifest `ppt_status` is `skipped`, `DATA_QUALITY_SUMMARY.txt` shows yellow **PowerPoint generation was skipped**.

**Expected / actual**

- Expected: warn on link refresh only; overall status reflects that distribution artifact exists.
- Actual: `ppt_status=skipped`, `PPT_GENERATION_SKIPPED` finding, `overall_status=warn` despite `ppt_outputs.distribution.status=success` and file on disk.

**Proof:** `wiring-proof-ppt-status-skew.py` (PASS).

**Disconfirming evidence checked**

- Per-output `ppt_outputs` entries are correct; bug is the aggregate `ppt_status` → data-quality mapping, not missing files.
- `tests/test_ppt_status_reporting.py:99` codifies `ppt_status == "skipped"` as intended for unsupported environments — conflicts with distribution success path.

**Dedup:** Not covered by existing `issues.json` entries (closest: generic PPT deliverable issues, not this status skew).

---

## W-3 — `export_pdf=True` silently ignored when distribution output disabled

**Severity:** MEDIUM (silent output loss)

**Evidence**

- `src/counter_risk/config.py:115-116` — independent flags `enable_distribution_output` and `export_pdf`.
- `src/counter_risk/pipeline/run.py:2757-2768,2835-2845` — `pdf_export` generator (stage `ppt_post_distribution`) runs only inside the `enable_distribution_output` branch.
- `src/counter_risk/gui/runner.py:200-203` — GUI can pass `--export-pdf` regardless of distribution flag.
- `src/counter_risk/outputs/pdf_export.py:54-56` — skip log only if generator is invoked; it is never loaded when distribution branch is skipped.

**Reachable trigger**

Workflow YAML with `enable_distribution_output: false` (tested in `tests/pipeline/test_monthly_pipeline_ppt_outputs.py:273-333`) plus CLI/GUI `--export-pdf`.

**Expected / actual**

- Expected: PDF export or explicit warning/validation error when `export_pdf` conflicts with distribution disable.
- Actual: zero PDF files, empty warnings list, no manifest finding.

**Proof:** `wiring-proof-export-pdf-silent-skip.py` (PASS).

**Dedup:** No matching entry in `issues.json`.

---

## W-4 — Optional runtime inputs missing from `input_hashes`

**Severity:** MEDIUM (incomplete provenance)

**Evidence**

- `src/counter_risk/pipeline/run.py:917-944` — `_resolve_input_paths` enumerates MOSERS/hist/PPT/cash paths only.
- `src/counter_risk/config.py:104,111` — `exposure_summary_xlsx`, `screenshot_inputs` are valid config fields used in production:
  - WAL generator: `run.py:3843-3856`
  - Screenshot replacement: `run.py:579-593,3158-3179`
- `src/counter_risk/pipeline/run.py:662-664` — manifest hashes only `_resolve_input_paths` keys.

**Reachable trigger**

- `output_generators` includes `historical_wal_workbook` with `exposure_summary_xlsx` set.
- `enable_screenshot_replacement: true` with `screenshot_inputs` (or auto-generated CPRS screenshots merged into `runtime_config`).

**Expected / actual**

- Expected: files that materially affect outputs appear in `input_hashes` (or a documented supplemental block).
- Actual: no hash entries; fleet replay cannot detect substitution of exposure summary or screenshot PNG sources.

**Proof:** `wiring-proof-input-hash-gaps.py` (PASS).

**Dedup:** Partial overlap with closed-style issues about evidence on `top_exposures` (`issues.json` mentions evidence provenance) but not input-hash coverage for these config fields.

---

## W-5 — Concentration table appended after distribution standalone validation

**Severity:** MEDIUM (stage ordering / false validation signal)

**Evidence**

- `src/counter_risk/pipeline/run.py:2807-2824` — `validate_distribution_ppt_standalone` runs inside `_write_outputs` before return.
- `src/counter_risk/pipeline/run.py:647-659` — `append_concentration_table_slide` mutates the same distribution `.pptx` **after** `_write_outputs` returns, immediately before manifest write.
- `docs/concentration_metrics.md` — documents `include_concentration_table_in_ppt: true` as supported.

**Reachable trigger**

`include_concentration_table_in_ppt: true` with concentration metrics present (non-default but supported).

**Expected / actual**

- Expected: final distribution artifact is what validation attested (or validation re-run post-append).
- Actual: manifest and validation reflect pre-append deck; optional slide added afterward without re-validation or hash update.

**Disconfirming evidence checked**

- Append uses python-pptx only (unlikely to reintroduce external relationships), but the pipeline explicitly raises on failed standalone validation — that guarantee no longer applies to the shipped file.

**Dedup:** None in `issues.json`.

---

## Refuted / duplicate candidates

| Candidate | Verdict | Reason |
|-----------|---------|--------|
| Map `NO_PRIOR_MATCH` / `WRITEBACK_*` in `data_quality.py` (`issues.json` P2) | **REFUTED on SHA** | Already present at `src/counter_risk/pipeline/data_quality.py:25-28,55-58`. Issue body is stale vs `main`. |
| Runner/GUI open-manifest uses next free run folder | **DUPLICATE / FIXED** | `open_manifest` / VBA `ResolveManifestPath` use `resolve_existing_output_dir` (`runner_launch.py:328-329`, `RunnerLaunch.bas:285-286`). Standalone `resolve_manifest_path()` helper still uses next-free, but production open paths are correct. |
| GUI worker-thread / discovery `input()` blockers | **REFUTED** | Dossier §8; `gui/runner.py:538-547` uses `_DiscoveryPromptBridge`. |
| Mixed limit denominators BLOCKER | **REFUTED (prior fix)** | `compute/limits.py:246-274`; dossier §8. |
| `demo_artifact.py` / `web_demo.py` duplicated helpers (orientation AST digest) | **LOW / NOT NEW** | Maintenance duplication only; both surfaces are demo/fixture-only (`web/index.html:57-59`). No wrong-output path. |
| `_export_distribution_pdf` dead helper | **NOT REPORTED** | Superseded by registry `pdf_export` generator; tests call helper directly (`tests/test_pdf_export.py`). Not operator-facing loss. |

---

## AST duplicate helpers (orientation baseline)

Per `orientation.json`, unchanged duplicate bodies at SHA:

- `demo_artifact.py` ↔ `web_demo.py`: `_resolve_config_path`, `_fixture_sources`, `_write_data_quality_summary`, `_artifact_relative_path`, `_normalize_manifest_paths`
- `compute/limits.py:49` ↔ `compute/rollups.py:78`: `_iter_rows`

No new wiring defect beyond known demo duplication.

---

## Checkpoint

Phases completed: orientation → scoped read → caller trace → adversarial verification → proof scripts → report.

See `D-audit-Counter_Risk--2026-09-13T18-41-41Z-wiring.CHECKPOINT.md`.
