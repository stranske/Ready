# PAEM Track D — Dashboard / Reporting / Portability Audit

**Unit:** `D-audit-Portable-Alpha-Extension-Model--2026-09-07T04-47-31Z`  
**Base:** `main` @ `59cb12be9d4b06434d41bc1b71612167ea6d9cfc`  
**Scope:** `dashboard/`, `pa_core/reporting/`, `pa_core/run_artifact_bundle.py`, `pa_core/manifest.py`, `pa_core/data/`, `scripts/make_portable_zip.py` (+ tests)  
**Executor:** Cursor Composer (read-only; no issues filed)  
**CI reference:** run `34015303572` (green on current head)

## Summary

| Metric | Value |
|--------|------:|
| Verified findings | 6 |
| High | 1 |
| Medium | 5 |
| Duplicates of closed issues | 1 (partial) |
| Refuted speculative candidates | 3 |

## Findings index

| ID | Title | Severity | Duplicate? |
|----|-------|----------|------------|
| F1 | `--bundle` ships stale `manifest.json` (pre-finalize) | High | No |
| F2 | `RunArtifactBundle.verify()` ignores `index_hash` | Medium | No |
| F3 | Run Logs cwd `manifest.json` fallback shows wrong provenance | Medium | No |
| F4 | Relative `manifest_path` in `run_end.json` breaks off output dir | Medium | No |
| F5 | `ManifestWriter` silently omits missing index from `data_files` | Medium | No |
| F6 | Bundled asset sample not shipped for pip-style installs | Medium | Partial (#2026) |

---

## F1 — `--bundle` captures pre-finalize manifest (missing warnings/cost)

**Evidence:** `pa_core/cli.py:1414-1415`, `pa_core/cli.py:2100-2101`, `pa_core/cli.py:930-944` (`_emit_run_end` → `_finalize_manifest_timing`)

**Trigger:** `pa run --bundle /path/to/bundle --log-json --index-frequency daily` (any run that emits captured warnings).

**Expected:** `bundle/manifest.json` matches the finalized `manifest.json` beside outputs (includes `warnings`, `cost`, final `run_timing`).

**Actual:** `_maybe_write_bundle()` runs **before** `_emit_run_end()`, which alone calls `_finalize_manifest_timing()` to append `warnings`, `cost`, and updated timing. Bundle manifest lacks captured warnings and cost; `run_timing` differs.

**Severity:** High — portable bundles advertise integrity but ship incomplete provenance.

**Test gate:** Extend `tests/test_run_artifact_bundle.py` (or `tests/test_run_record_warnings.py`) to run CLI with `--bundle` and assert `bundle/manifest.json == finalized manifest.json` for `warnings` and `cost`.

**Related closed issue:** #1834 (run.json envelope) — **not duplicate** (different artifact: `bundle/manifest.json` vs `run.json`).

**Repro:** `repros/repro_bundle_manifest_stale.py`

```bash
PYTHONPATH=clones/Portable-Alpha-Extension-Model /tmp/paem-audit-20260907-venv/bin/python \
  artifacts/audits/paem-20260907/repros/repro_bundle_manifest_stale.py
```

---

## F2 — `RunArtifactBundle.verify()` does not validate `index_hash`

**Evidence:** `pa_core/run_artifact_bundle.py:59-70` (stores `index_hash`), `pa_core/run_artifact_bundle.py:99-143` (`verify()` checks config/manifest/output hashes only)

**Trigger:** Tamper `index_hash` in `bundle.json` after `save()`.

**Expected:** `verify()` returns `False` or re-hashes bundled index input.

**Actual:** `verify()` returns `True`; `load()` returns tampered hash. No index file is bundled to hash against.

**Severity:** Medium — index provenance can be altered without detection.

**Test gate:** Add `tests/test_run_artifact_bundle.py::test_verify_fails_on_index_hash_tamper`.

**Related closed issue:** none in dedup set.

**Repro:** `repros/repro_bundle_index_hash_verify.py`

---

## F3 — Run Logs displays arbitrary cwd `manifest.json` when `run_end.json` absent

**Evidence:** `dashboard/pages/7_Run_Logs.py:58-63`

**Trigger:** `runs/<id>/run.log` exists; `run_end.json` missing; unrelated `manifest.json` in Streamlit cwd.

**Expected:** Page shows manifest linked to the selected run, or a clear “not found” state.

**Actual:** Fallback `Path.cwd().glob("manifest.json")` picks the first root manifest (often from a different run). Repro shows `{"provenance":"STALE_ROOT_MANIFEST"}`.

**Severity:** Medium — analysts misread run provenance in the dashboard.

**Test gate:** `tests/test_dashboard_run_logs_page.py` should assert fallback does **not** surface unrelated manifests (currently `test_run_logs_with_log_and_manifest` encodes the buggy fallback).

**Related closed issue:** #1901 (disk handoff) — **not duplicate** (session-state vs wrong-manifest display).

**Repro:** `repros/repro_run_logs_stale_manifest.py`

---

## F4 — Relative `manifest_path` in `run_end.json` is cwd-dependent

**Evidence:** `pa_core/logging_utils.py:161-162`, `pa_core/contracts.py:278-289`, `dashboard/pages/7_Run_Logs.py:58-59`

**Trigger:** CLI writes `run_end.json` with `manifest_path: "manifest.json"` (relative to output cwd). Dashboard or tooling cwd ≠ run output directory.

**Expected:** Resolved absolute path, or resolution relative to `run_end.json` parent.

**Actual:** `manifest_path_from_run_end()` returns `Path("manifest.json")`; `.exists()` is false when cwd is parent directory (triggers F3 fallback).

**Severity:** Medium — breaks manifest linkage for JSON-logged runs viewed from project root.

**Test gate:** `tests/test_contracts.py::test_manifest_path_from_run_end` should cover relative paths resolved against `run_end.json` parent.

**Related closed issue:** none exact; complements F3.

**Repro:** `repros/repro_manifest_relative_cwd.py`

---

## F5 — `ManifestWriter` silently drops missing data files from `data_files`

**Evidence:** `pa_core/manifest.py:102`

**Trigger:** `ManifestWriter.write(..., data_files=[config, missing_index.csv])` where index path does not exist at write time.

**Expected:** Error, or explicit `data_files` entry marking missing inputs.

**Actual:** Missing path omitted with no warning; manifest implies only config was hashed. Reproducibility audit cannot detect absent index.

**Severity:** Medium — silent provenance gap on misconfigured or moved inputs.

**Test gate:** `tests/test_manifest.py` regression asserting missing `data_files` entries fail loudly or record `null` hash.

**Related closed issue:** #1835 (data-quality promotion) — **not duplicate** (quality metrics vs silent omission).

**Repro:** `repros/repro_manifest_missing_data_files.py`

---

## F6 — Bundled asset sample path breaks under pip-style install layout

**Evidence:** `dashboard/utils.py:144-147`, `dashboard/utils.py:172-174`, `pyproject.toml:84-89` (`templates/` not in `package-data`)

**Trigger:** `pip install` (dashboard under `site-packages/dashboard/`); open Asset Library → “Use bundled sample asset data”.

**Expected:** Sample CSV loads like index sample (`bundled_sample_index_path()` uses `data` package-data).

**Actual:** `bundled_asset_timeseries_path()` resolves to `site-packages/templates/asset_timeseries_wide_returns.csv`, which is not shipped. `sample_available` is false; first-timers blocked unless they upload.

**Severity:** Medium — portability gap between repo checkout / portable zip vs pip install.

**Test gate:** `tests/test_dashboard_*` asserting `bundled_asset_timeseries_path().exists()` when only installed packages are present (or move asset CSV into `data` package-data like index).

**Related closed issue:** #2026 (closed) — **partial duplicate**: repo-checkout bundled path was added; pip-install path still missing.

**Repro:** `repros/repro_pip_asset_sample_missing.py`

---

## Refuted speculative candidates

| Candidate | Why not filed |
|-----------|----------------|
| Plotly `engine='kaleido'` `TypeError` in audit venv | Environmental plotly/kaleido version skew; CI `34015303572` green; not reproduced under repo test stubs. |
| `build_windows_portable_zip` skips `get_default_excludes()` | Real code smell (`scripts/make_portable_zip.py:282-292`) but not executable-proven on this host (non-Windows); source-only zip path applies excludes correctly. |
| `run_diff` ignores `data_files` hash deltas | Design limitation, not an observed end-user failure in dashboard/reporting paths within scope. |

---

## Coverage notes

- Read: `7_Run_Logs.py`, `dashboard/utils.py`, `pa_core/manifest.py`, `pa_core/run_artifact_bundle.py`, `pa_core/reporting/run_diff.py`, `pa_core/reporting/export_packet.py`, `pa_core/data/importer.py`, `pa_core/data/loaders.py`, `scripts/make_portable_zip.py`, corresponding tests.
- Runtime: repro scripts via `/tmp/paem-audit-20260907-venv/bin/python`; Run Logs behavior via `runpy` fake Streamlit (same technique as `tests/test_dashboard_run_logs_page.py`).
- Dedup checked against closed issues #1833–1835, #1854, #1899–1907, #2018–2052 via `issues.json`.

## Artifacts

| Path | Description |
|------|-------------|
| `repros/repro_bundle_manifest_stale.py` | F1 |
| `repros/repro_bundle_index_hash_verify.py` | F2 |
| `repros/repro_run_logs_stale_manifest.py` | F3 |
| `repros/repro_manifest_relative_cwd.py` | F4 |
| `repros/repro_manifest_missing_data_files.py` | F5 |
| `repros/repro_pip_asset_sample_missing.py` | F6 |
