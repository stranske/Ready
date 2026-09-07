# Audit Report: stranske/Counter_Risk (2026-09-07)

- **Unit**: `D-audit-Counter_Risk--2026-09-07T04-47-32Z`
- **Target Repository**: `stranske/Counter_Risk`
- **Audit Date**: 2026-09-07
- **Commit SHA**: `aa3173e test: cover reconciliation dormant and dropped series branches (#999)`
- **Auditor**: Gemini via Antigravity (`agy`)
- **Mode**: Track D Demand-Driven Refill Audit (open agent-ready supply dropped to 2 <= 2)

---

## 1. Executive Summary

A comprehensive 8-dimension audit was conducted across the `stranske/Counter_Risk` codebase at tip `aa3173e`.

### Baseline Health
- **Source LOC**: 106 Python modules (25,911 LOC) under `src/counter_risk/`
- **Test LOC**: 177 test modules (39,437 LOC) under `tests/`
- **Linter Status**: `uv run ruff check .` passed with 0 diagnostics
- **Test Suite Status**: 1,472 passed, 1 skipped in 139.16s (`uv run pytest -m "not release and not slow" -n auto -q`)
- **Pre-Audit Supply**: 2 open agent-ready issues (#996, #978) + 2 durable trackers (#724, #499)

### Audit Outcomes
7 high-conviction defects were adversarially verified on the live tip, formatted into strict `AGENT_ISSUE_FORMAT` work orders passing local validation with zero advisories, and filed with `bug` and `priority` repository labels:
- **#1000** [P1]: `Reject non-finite notional values in futures delta computation` (`src/counter_risk/compute/futures_delta.py:495-511`)
- **#1001** [P1]: `Deduplicate and group current-month normalized descriptions in compute_futures_delta` (`src/counter_risk/compute/futures_delta.py:188-264`)
- **#1002** [P2]: `Guard change attribution float parsers against non-finite values` (`src/counter_risk/reports/change_attribution.py:81-90, 93-105`)
- **#1003** [P2]: `Accumulate multi-row counterparties in change attribution prior mapping` (`src/counter_risk/reports/change_attribution.py:198-199`)
- **#1004** [P2]: `Validate non-negative and finite bounds for cash_total_min and cash_total_max` (`src/counter_risk/config.py:96-97, 161-169`)
- **#1005** [P2]: `Bind dynamic GitHub issue reference to FleetRunContext in langsmith telemetry` (`src/counter_risk/observability/langsmith_fleet.py:16, 279`)
- **#1006** [P2]: `Reject non-finite values in repo cash structured and override parsers` (`src/counter_risk/parsers/repo_cash_sources.py:274-282`)

---

## 2. Adversarial Verification & Defect Catalog

### Finding 1: Non-Finite Float Bypass in Futures Delta Extraction (P1)
- **Path**: `src/counter_risk/compute/futures_delta.py:495-511`
- **Defect**: `_extract_notional()` checks `if math.isnan(result):` but omits `math.isinf(result)`. Infinite float values (`"inf"`, `"-inf"`) bypass `InvalidNotionalError` in strict mode and bypass `INVALID_NOTIONAL` structured warnings in default mode. Downstream subtraction `inf - inf` produces `nan`.
- **Reproducer**:
  ```python
  from counter_risk.compute.futures_delta import _extract_notional, compute_futures_delta
  from counter_risk.pipeline.warnings import WarningsCollector
  row = {'Description': 'ESH6', 'Notional': 'inf'}
  wc = WarningsCollector()
  val = _extract_notional(row, row_id='ESH6', row_idx=0, strict=False, collector=wc)
  assert val == float('inf')  # BUG: should be 0.0 with warning
  assert len(wc.warnings) == 0  # BUG: missing INVALID_NOTIONAL warning
  ```
- **Filed**: [stranske/Counter_Risk#1000](https://github.com/stranske/Counter_Risk/issues/1000)

### Finding 2: Prior Notional Multiplied on Split Current-Month Positions (P1)
- **Path**: `src/counter_risk/compute/futures_delta.py:188-264`
- **Defect**: Prior positions are aggregated into `prior_by_key[key]`, but `current_rows` is iterated per raw unaggregated row. When multiple current rows normalize to the same description key (e.g. `ES March 2025` and `ES Mar '25`), each row matches against the full prior sum, multiplying the reported prior notional by the number of split rows and corrupting report totals.
- **Reproducer**:
  ```python
  from counter_risk.compute.futures_delta import compute_futures_delta
  cur = [{'Description': 'ES March 2025', 'Notional': 100.0}, {'Description': "ES Mar '25", 'Notional': 200.0}]
  pri = [{'Description': 'ES MAR 2025', 'Notional': 50.0}]
  res, _ = compute_futures_delta(cur, pri)
  records = res.to_dict(orient='records')
  # Total reported prior: 100.0 (actual prior was 50.0)
  # Total reported change: 200.0 (actual net delta was 250.0)
  ```
- **Filed**: [stranske/Counter_Risk#1001](https://github.com/stranske/Counter_Risk/issues/1001)

### Finding 3: Non-Finite Floats in Change Attribution Parsers (P2)
- **Path**: `src/counter_risk/reports/change_attribution.py:81-90, 93-105`
- **Defect**: `_first_float()` and `_optional_float()` call `float(value)` without verifying `math.isfinite()`. `"nan"` strings parse into `float('nan')`, resulting in `delta = nan`, `unattributed_remainder = nan`, and markdown rendering `nan` with `High` confidence.
- **Reproducer**:
  ```python
  from counter_risk.reports.change_attribution import attribute_changes
  cur = [{'counterparty': 'Bank A', 'notional': 'nan'}]
  pri = [{'counterparty': 'Bank A', 'notional': '100'}]
  res = attribute_changes(cur, pri)
  # row notional_change is nan, confidence is 'High', summary unattributed_remainder is nan
  ```
- **Filed**: [stranske/Counter_Risk#1002](https://github.com/stranske/Counter_Risk/issues/1002)

### Finding 4: Multi-Row Counterparty Silent Overwrite in Change Attribution (P2)
- **Path**: `src/counter_risk/reports/change_attribution.py:198-199`
- **Defect**: `prior_by_exact = {row.counterparty: row for row in prior_rows}` drops earlier rows when a prior counterparty has multiple exposure positions, under-reporting prior notional and distorting period-over-period attribution.
- **Reproducer**:
  ```python
  from counter_risk.reports.change_attribution import attribute_changes
  cur = [{'counterparty': 'JPMorgan', 'notional': 150.0}]
  pri = [{'counterparty': 'JPMorgan', 'notional': 100.0}, {'counterparty': 'JPMorgan', 'notional': 50.0}]
  res = attribute_changes(cur, pri)
  # matched_prior_notional is 50.0 (100.0 was dropped), notional_change is 100.0 instead of 0.0
  ```
- **Filed**: [stranske/Counter_Risk#1003](https://github.com/stranske/Counter_Risk/issues/1003)

### Finding 5: Missing Finite & Non-Negative Validation on Cash Range Bounds (P2)
- **Path**: `src/counter_risk/config.py:96-97, 161-169`
- **Defect**: `WorkflowConfig` permits `NaN` and negative lower bounds for `cash_total_min` and `cash_total_max`. In Python, `5.0 < float('nan')` is `False`, allowing `NaN` bounds to pass validator `_validate_cash_total_range_upper_bound` and silently disabling pipeline cash validation checks.
- **Reproducer**:
  ```python
  from counter_risk.config import WorkflowConfig
  from pathlib import Path
  cfg = WorkflowConfig(
      hist_all_programs_3yr_xlsx=Path('a.xlsx'),
      hist_ex_llc_3yr_xlsx=Path('b.xlsx'),
      hist_llc_3yr_xlsx=Path('c.xlsx'),
      monthly_pptx=Path('m.pptx'),
      cash_total_min=float('nan'),
      cash_total_max=5.0,
  ) # passes without validation error
  ```
- **Filed**: [stranske/Counter_Risk#1004](https://github.com/stranske/Counter_Risk/issues/1004)

### Finding 6: Hardcoded Stale Issue Tag in LangSmith Fleet Telemetry (P2)
- **Path**: `src/counter_risk/observability/langsmith_fleet.py:16, 279`
- **Defect**: `GITHUB_ISSUE: Final = "stranske/Counter_Risk#610"` hardcodes closed issue #610 across all emitted `langsmith-fleet.ndjson` records. `FleetRunContext` lacks a `github_issue` field or environment override mechanism.
- **Filed**: [stranske/Counter_Risk#1005](https://github.com/stranske/Counter_Risk/issues/1005)

### Finding 7: Non-Finite Float Acceptance in Repo Cash Sources (P2)
- **Path**: `src/counter_risk/parsers/repo_cash_sources.py:274-282`
- **Defect**: `_coerce_cash_value()` parses strings with `float(normalized)` without checking `math.isfinite()`. Input strings `"nan"` and `"inf"` return non-finite floats without raising `ValueError`, contaminating `cash_by_counterparty` mappings.
- **Reproducer**:
  ```python
  from counter_risk.parsers.repo_cash_sources import _coerce_cash_value
  from pathlib import Path
  val = _coerce_cash_value('nan', path=Path('cash.csv'), row_index=2)
  assert val != val  # returns float('nan') without error
  ```
- **Filed**: [stranske/Counter_Risk#1006](https://github.com/stranske/Counter_Risk/issues/1006)

---

## 3. Work Order Registry & Pre-Flight Validation

| Issue # | Priority | Title | Relative Code Path | Linter Status |
|---|---|---|---|---|
| [#1000](https://github.com/stranske/Counter_Risk/issues/1000) | P1 (High) | Reject non-finite notional values in futures delta computation | `src/counter_risk/compute/futures_delta.py:495-511` | PASS (0 advisories) |
| [#1001](https://github.com/stranske/Counter_Risk/issues/1001) | P1 (High) | Deduplicate and group current-month normalized descriptions in compute_futures_delta | `src/counter_risk/compute/futures_delta.py:188-264` | PASS (0 advisories) |
| [#1002](https://github.com/stranske/Counter_Risk/issues/1002) | P2 (Normal) | Guard change attribution float parsers against non-finite values | `src/counter_risk/reports/change_attribution.py:81-90` | PASS (0 advisories) |
| [#1003](https://github.com/stranske/Counter_Risk/issues/1003) | P2 (Normal) | Accumulate multi-row counterparties in change attribution prior mapping | `src/counter_risk/reports/change_attribution.py:198-199` | PASS (0 advisories) |
| [#1004](https://github.com/stranske/Counter_Risk/issues/1004) | P2 (Normal) | Validate non-negative and finite bounds for cash_total_min and cash_total_max | `src/counter_risk/config.py:96-97` | PASS (0 advisories) |
| [#1005](https://github.com/stranske/Counter_Risk/issues/1005) | P2 (Normal) | Bind dynamic GitHub issue reference to FleetRunContext in langsmith telemetry | `src/counter_risk/observability/langsmith_fleet.py:16` | PASS (0 advisories) |
| [#1006](https://github.com/stranske/Counter_Risk/issues/1006) | P2 (Normal) | Reject non-finite values in repo cash structured and override parsers | `src/counter_risk/parsers/repo_cash_sources.py:274-282` | PASS (0 advisories) |

---

## 4. Reconciliations & Audit Artifacts

- **Intake Log**: 7 entries recorded to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Durable Ledger**: Updated `Code/Audits/AUDIT_LEDGER.md` with full run metadata.
- **Repository Audit Log**: Updated `Code/Audits/Counter_Risk/README.md`, `2026-09-07-audit-run.md`, `2026-09-07-AUDIT_REPORT.md`, `2026-09-07-verification-log.md`, and issue bodies under `Code/Audits/Counter_Risk/2026-09-07-issue-bodies/`.
- **Checkpoints**: Appended to `artifacts/audits/D-audit-Counter_Risk--2026-09-07T04-47-32Z.CHECKPOINT.md` and `artifacts/audits/CHECKPOINT.md`.
