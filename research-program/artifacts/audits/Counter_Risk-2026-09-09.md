# Counter_Risk Refill Audit Run Report — 2026-09-09

Unit: `D-audit-Counter_Risk--2026-09-09T05-14-45Z`
Title: `Audit stranske/Counter_Risk and file issues (supply 1 <= 2)`
Audited tip: `0cf9d1f93f18e95ae818a7c2be660893096b797f` (remote `main`)
Audit date: 2026-09-09

## Executive Summary

Track D demand-driven audit refill executed for repository `stranske/Counter_Risk`. The fleet's supply of agent-ready issues had fallen to 1 <= 2 (#996). A full 8-dimension repository audit was performed against the live codebase at commit `0cf9d1f`. Eight defects and documentation issues were adversarially verified against live source lines and executed tests, formatted into canonical `AGENT_ISSUE_FORMAT` work orders, linted against `.github/scripts/issue_format.py` (0 advisories), and filed directly to GitHub with `gh issue create`.

All 8 filed issues passed GitHub Actions `Agents Issue Format Guard` without any format rejections or `needs-human` labels. All intake logs, durable audit records, repo READMEs, and the global `AUDIT_LEDGER.md` have been updated.

## Filed & Verified Issues

| Finding ID | Priority | GitHub Issue | Title | Dimensions | Status |
|---|---|---|---|---|---|
| CR-1 | P1 | [#1018](https://github.com/stranske/Counter_Risk/issues/1018) | Reject infinite exposure limits before evaluation | 1, 3 | Filed & Verified |
| CR-2 | P1 | [#1016](https://github.com/stranske/Counter_Risk/issues/1016) | Preserve the complete PyInstaller directory in assembled releases | 3, 7 | Filed & Verified |
| CR-3 | P1 | [#1017](https://github.com/stranske/Counter_Risk/issues/1017) | Launch the GUI executable from the assembled bin directory | 3, 4 | Filed & Verified |
| CR-4 | P2 | [#1019](https://github.com/stranske/Counter_Risk/issues/1019) | Collapse duplicate Repo rows when applying authoritative cash | 1, 2 | Filed & Verified |
| CR-5 | P2 | [#1020](https://github.com/stranske/Counter_Risk/issues/1020) | Reconcile split current rows before matching prior attribution | 1, 2 | Filed & Verified |
| CR-6 | P2 | [#1021](https://github.com/stranske/Counter_Risk/issues/1021) | Reject non-finite notional breakdown values in drop-in template writer | 1, 3 | Filed & Verified |
| CR-7 | P2 | [#1022](https://github.com/stranske/Counter_Risk/issues/1022) | Validate finite and non-negative bounds for historical WAL row appends | 1, 3 | Filed & Verified |
| CR-8 | P3 | [#1023](https://github.com/stranske/Counter_Risk/issues/1023) | Correct the dated HHI threshold attribution in operator guidance | 5 | Filed & Verified |

## Verification Details & Evidence

1. **CR-1 ([#1018](https://github.com/stranske/Counter_Risk/issues/1018)): Infinite configured limit accepted (`src/counter_risk/limits_config.py:23`, `src/counter_risk/compute/limits.py:277`)**
   - *Mechanism*: `LimitEntry` specifies `limit_value: float = Field(gt=0)` with no `math.isfinite` check. Pydantic accepts `float("inf") > 0`. When evaluated in `check_limits`, `actual - inf` results in `-inf`, which drops the negative difference and produces zero breach findings even when exposure is massive.
   - *Verification*: Tested loading YAML containing `limit_value: .inf`; 100 exposure against 50 produced 1 breach, whereas 100 exposure against infinity produced 0 breaches.

2. **CR-2 ([#1016](https://github.com/stranske/Counter_Risk/issues/1016)): Release assembly drops companion runtime and data files (`src/counter_risk/build/release.py:268,284,374`, `release.spec:40,66`)**
   - *Mechanism*: `release.spec` sets `exclude_binaries=True` on `EXE` and collects libraries, DLLs, and dependencies via `COLLECT` into a one-directory layout. However, `_copy_bundled_executable` in `release.py:284` copies only the standalone executable file into `bundle_dir/bin`, omitting the entire collected folder. The resulting binary cannot run on machines without external Python environments.
   - *Verification*: Traced `shutil.copy2` execution; verified that companion DLLs and libraries produced by PyInstaller COLLECT are excluded from the release bundle.

3. **CR-3 ([#1017](https://github.com/stranske/Counter_Risk/issues/1017)): GUI launcher omits assembled bin path (`src/counter_risk/build/release.py:281,303`, `run_counter_risk_gui.cmd:19,24,30-60`)**
   - *Mechanism*: `build/release.py:281` places the executable into `%~dp0bin\counter-risk.exe` and instructs operators to double-click `run_counter_risk_gui.cmd`. However, `run_counter_risk_gui.cmd` checks `%~dp0dist\counter-risk\counter-risk.exe` (dev path) and `%~dp0counter-risk.exe` (root), then falls back to python/venv/global commands. It never checks `%~dp0bin\counter-risk.exe`.
   - *Verification*: Inspected batch script branch sequence; verified that no branch resolves the assembled release bin folder.

4. **CR-4 ([#1019](https://github.com/stranske/Counter_Risk/issues/1019)): Duplicate Repo rows inflate authoritative cash (`src/counter_risk/pipeline/run.py:1107,1120,1131,4097`)**
   - *Mechanism*: `_inject_repo_cash_into_cprs_ch` builds `existing_repo_by_key` with `.setdefault()`, which captures only the first matching row for a normalized counterparty. When authoritative cash is applied, only the first row is updated, leaving duplicate normalized rows intact in `records`. Downstream `_aggregate_cprs_ch_series_totals` sums every row with the normalized name, inflating total Cash.
   - *Verification*: Executed probe with duplicate rows (10 and 20 Cash) replaced by authoritative 100 Cash; aggregation produced 120 Cash instead of 100 Cash.

5. **CR-5 ([#1020](https://github.com/stranske/Counter_Risk/issues/1020)): Split current attribution reuses prior balance (`src/counter_risk/reports/change_attribution.py:215,224,231`, `src/counter_risk/pipeline/run.py:2069`)**
   - *Mechanism*: Prior rows are grouped and aggregated in `_index_prior_rows`, but current rows are iterated as unaggregated records. When current counterparty rows are split across multiple entries, every split row matches the same prior balance and deducts the full prior notional amount multiple times.
   - *Verification*: Probe with total current notional 300 and prior 250 with change +50: split into 100 (+25) and 200 (+25) produced summed change -200 and prior 500.

6. **CR-6 ([#1021](https://github.com/stranske/Counter_Risk/issues/1021)): Drop-in template writer accepts non-finite breakdown values (`src/counter_risk/writers/dropin_templates.py:104,350,381,398`)**
   - *Mechanism*: `_coerce_breakdown` parses float values without checking `math.isfinite`. When `fill_dropin_template` is called with NaN or Inf in the breakdown mapping, the non-finite values are accepted and written directly to openpyxl worksheet cells.
   - *Verification*: Executed `_coerce_breakdown({"Total": float("nan"), "Cash": float("inf")})`; verified it returns `{'Total': nan, 'Cash': inf}` without raising ValueError.

7. **CR-7 ([#1022](https://github.com/stranske/Counter_Risk/issues/1022)): Validate finite and non-negative bounds for historical WAL appends (`src/counter_risk/writers/historical_update.py:732,798-800`)**
   - *Mechanism*: `append_wal_row` casts `wal_value` directly to float and assigns it to the target worksheet cell without verifying that `wal_value` is non-negative and finite.
   - *Verification*: Traced `append_wal_row` parameters and cell assignments; confirmed lack of boundary checks.

8. **CR-8 ([#1023](https://github.com/stranske/Counter_Risk/issues/1023)): Correct dated HHI threshold attribution in operator guidance (`docs/concentration_metrics.md:77-80`)**
   - *Mechanism*: Concentration metrics guidance attributes 0.25 (2,500 HHI) to undated DOJ "highly concentrated" market standards. The 2023 DOJ/FTC Merger Guidelines lowered the threshold to 1,800.
   - *Verification*: Cross-referenced text with current official DOJ antitrust merger guidelines.

## Intake Log Entries Appended

Appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`:
```text
Counter_Risk|01-package-payload.md|https://github.com/stranske/Counter_Risk/issues/1016
Counter_Risk|02-gui-release-launcher.md|https://github.com/stranske/Counter_Risk/issues/1017
Counter_Risk|04-finite-limit.md|https://github.com/stranske/Counter_Risk/issues/1018
Counter_Risk|05-repo-cash-duplicate.md|https://github.com/stranske/Counter_Risk/issues/1019
Counter_Risk|06-current-attribution.md|https://github.com/stranske/Counter_Risk/issues/1020
Counter_Risk|07-dropin-template-finite-breakdown.md|https://github.com/stranske/Counter_Risk/issues/1021
Counter_Risk|08-historical-wal-bounds.md|https://github.com/stranske/Counter_Risk/issues/1022
Counter_Risk|03-hhi-doc-reference.md|https://github.com/stranske/Counter_Risk/issues/1023
```

## Durable Audit Artifact Locations

- Checkpoint File: `/Users/teacher/.codex/automations/research-program/artifacts/audits/D-audit-Counter_Risk--2026-09-09T05-14-45Z.CHECKPOINT.md`
- Run Report: `/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-09.md`
- Durable Audit Folder: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/`
  - `2026-09-09-audit-run.md`
  - `2026-09-09-00-repo-map.md`
  - `2026-09-09-AUDIT_REPORT.md`
  - `2026-09-09-verification-log.md`
  - `2026-09-09-issue-bodies/` (01 through 08)
  - `README.md`
- Global Audit Ledger: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/AUDIT_LEDGER.md`
