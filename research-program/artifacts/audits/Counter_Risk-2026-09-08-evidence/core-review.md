# Counter_Risk core review — 2026-09-08

## Scope and baseline

- **Scope:** `src/counter_risk/pipeline`, `parsers`, `writers`, `outputs`, `compute`, and `reports`, plus their corresponding tests and configuration.
- **Baseline:** `e2a1bacf37503217e00e467aa72198988777afa4`.
- **Bounded verification:** `PYTHONPATH=src .venv/bin/python -m pytest -q tests/compute/test_limits.py tests/test_change_attribution_report.py tests/pipeline/test_run_pipeline.py -m 'not slow and not release'` from the target-repo root: **167 passed, 31 deselected**.
- **Dedup source:** the supplied open-and-closed snapshot has 3 open and 117 closed issues. The three open items are #996, #724, and #499; none overlaps the defects below. Targeted closed-body checks were also made for #1006 and #1003.

## Verified, new recommendations

### CR-CORE-1 — A `.inf` limit value disables an otherwise breached control

- **Severity:** P1 / MAJOR. **Confidence:** high.
- **Evidence:** `src/counter_risk/limits_config.py:21-27` constrains `limit_value` only with `Field(gt=0)`, so positive infinity is accepted. `src/counter_risk/compute/limits.py:269-279` calculates `breach_amount = actual_value - limit.limit_value` and suppresses it when `<= 0`; an infinite limit therefore produces no breach. `src/counter_risk/pipeline/run.py:2377-2419` loads `config/limits.yml`, invokes `check_limits`, and treats an empty result as zero breaches.
- **Reachability:** operator-edited YAML is the normal limit-control input. YAML parses `limit_value: .inf` as `float('inf')`; the Pydantic model accepts it, then the normal pipeline loading path consumes it.
- **Matched-control repro (Python 3.12, target clone):** one row `{counterparty: Acme, notional: 100.0}` plus a finite absolute limit of 50 produced one breach (`breach_amount=50.0`). The identical row plus `limit_value=float('inf')` produced `[]`. `yaml.safe_load` followed by `LimitsConfig.model_validate` also accepted `limit_value: .inf` as `inf`.
- **Recommended task:** add a finite-value validator for `LimitEntry.limit_value` in `src/counter_risk/limits_config.py`, and add YAML/model and `check_limits` regression cases in `tests/compute/test_limits.py` (or a focused limits-config test). The test must demonstrate `.inf` is rejected before evaluation while a finite breached limit still emits its breach.
- **Dedup disposition:** **new.** Targeted snapshot search found the older closed #45 limit-monitoring implementation, but no open or closed issue covering finite validation of `LimitEntry.limit_value`. This is distinct from closed #1004, which validates only `WorkflowConfig.cash_total_min` and `cash_total_max`.

### CR-CORE-2 — Repo-cash upsert leaves duplicate CPRS-CH Repo rows live, inflating Cash history

- **Severity:** P2 / MAJOR conditional on a duplicate Repo source row. **Confidence:** high on the defect and repro; medium on its observed frequency in operator workbooks.
- **Evidence:** `src/counter_risk/pipeline/run.py:1107-1113` explicitly states that a second Repo record must not survive because the Cash sheet aggregates records. But `src/counter_risk/pipeline/run.py:1114-1120` indexes only the first duplicate with `setdefault`; `src/counter_risk/pipeline/run.py:1128-1131` overwrites only that one record. `src/counter_risk/pipeline/run.py:4084-4100` subsequently sums every Repo record by normalized counterparty for the historical sheet.
- **Reachability:** `src/counter_risk/pipeline/run.py:450-463` invokes daily Repo-cash application during every normal pipeline run, and `src/counter_risk/pipeline/run.py:1078-1088` routes the result into the CPRS-CH rows used by historical output.
- **Matched-control repro (Python 3.12, target clone):** with one `repo/CIBC` row holding Cash 10 and authoritative cash `{CIBC: 100}`, `_inject_repo_cash_into_cprs_ch` returned one CIBC row with Cash `[100]`, aggregate 100. With two normalized-equivalent Repo rows (Cash 10 and 20), the same call returned Cash `[100, 20]`, aggregate **120**, despite the authoritative total being 100.
- **Recommended task:** in `src/counter_risk/pipeline/run.py`, either collapse all normalized-equivalent Repo records to exactly one authoritative row or fail/warn under the configured reconciliation policy before historical aggregation. Add a focused regression in `tests/pipeline/test_run_pipeline.py` that proves the one-row control stays at 100 and two normalized-equivalent rows cannot write an aggregate above 100.
- **Dedup disposition:** **new.** Closed #1006 is limited to non-finite values in `src/counter_risk/parsers/repo_cash_sources.py`; it does not cover duplicate records already present in parsed CPRS-CH Repo data. Closed #34 concerns initial Daily Holdings ingestion, not the upsert/aggregation seam.

### CR-CORE-3 — Change attribution applies one prior balance to each split current counterparty row

- **Severity:** P2 / MAJOR conditional on split current totals. **Confidence:** high on the accounting mismatch and repro; medium on source frequency.
- **Evidence:** `src/counter_risk/reports/change_attribution.py:132-142` aggregates prior rows only. `src/counter_risk/reports/change_attribution.py:209-216` creates those prior indexes but leaves `current_rows` ungrouped; the per-current-row loop at `:224-268` retrieves the same exact prior aggregate for every duplicate current row. Pipeline output uses the All Programs totals directly in `src/counter_risk/pipeline/run.py:2052-2080`.
- **Reachability:** a duplicated current counterparty in the parsed totals reaches `attribute_changes` unchanged. The emitted CSV/Markdown is an operator report artifact, so its reported rows and summed moves are materially misleading.
- **Matched-control repro (Python 3.12, target clone):** one current `CIBC=300` and prior `CIBC=50` yielded change 250. Splitting the identical current total into `CIBC=100` and `CIBC=200` with the same prior yielded rows `(100, 50, 50)` and `(200, 50, 150)`, whose reported change total is **200**, not the correct `300 - 50 = 250`.
- **Recommended task:** group/aggregate current rows by the same exact/normalized key semantics before matching, preserving a deterministic display label and an appropriate supplied-delta validation rule. Add a regression in `tests/test_change_attribution_report.py` that compares the one-row control and split-current case and asserts the total current, prior, and change reconcile.
- **Dedup disposition:** **new but adjacent to closed #1003.** The targeted #1003 body and current implementation address only multi-row **prior** aggregation. Its non-goals do not add current-row grouping. Closed #1001 groups split current rows in `src/counter_risk/compute/futures_delta.py`, a different report path.

## Candidates rejected after verification

| Candidate | Evidence and disposition |
| --- | --- |
| Non-finite structured Repo Cash remains accepted | **REJECTED — fixed.** `src/counter_risk/parsers/repo_cash_sources.py:275-284` now calls `math.isfinite` and raises on non-finite cash. This corresponds to closed #1006 and is present at the audited head. |
| Prior-row overwrite in change attribution | **REJECTED — fixed.** `src/counter_risk/reports/change_attribution.py:132-142` accumulates same-key prior notions, matching closed #1003. The remaining CR-CORE-3 current-side case is materially different and separately reproved above. |
| Mixed-sign concentration HHI | **REJECTED — fixed/covered.** `src/counter_risk/compute/rollups.py:581-593` computes magnitudes before shares; the bounded baseline includes the existing mixed-sign concentration coverage. No new defect recommended. |
| `top_changes` accepts a direct non-finite `notional_change` mapping | **REJECTED — insufficient core-path evidence.** `src/counter_risk/compute/rollups.py:409-435` is permissive for arbitrary public helper callers, but the normal parser boundary rejects non-finite source numerics (`src/counter_risk/parsers/_xlsx_reader.py:156-205`; `src/counter_risk/parsers/cprs_ch.py:237-258`). I did not establish a normal pipeline path that delivers such a value, so this should not become an issue. |

## Risk and handoff

These are report/control correctness defects, not demonstrated current-workbook incidents. CR-CORE-1 is the strongest recommendation because a syntactically valid config value silently disables a risk control. CR-CORE-2 and CR-CORE-3 should be filed only with their conditional trigger made explicit in the issue body; the probes establish wrong results when duplicate rows occur, but do not prove duplicates exist in the supplied fixtures.
