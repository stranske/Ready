# Counter_Risk Audit Report — 2026-09-09 (Afternoon Refill Run 2)

- **Unit ID**: `D-audit-Counter_Risk--2026-09-09T17-29-35Z`
- **Repository**: `stranske/Counter_Risk`
- **Tip Commit**: `cdfd281866fb5bf23fce6dd22eb4f7367e0876fc`
- **Audit Type**: Track D demand-driven refill audit (supply dropped to 2 <= 2: #1023, #996)
- **Auditor**: Gemini (Antigravity `repo-audit` skill)
- **Status**: 6 verified findings, 6 issues filed (#1031-#1036), all passed GitHub Actions format guard.

---

## 1. Executive Summary

A full 8-dimension audit was conducted on `stranske/Counter_Risk` at HEAD `cdfd281866fb5bf23fce6dd22eb4f7367e0876fc`. Following rapid resolution of the morning audit's 8 issues (#1016-#1022 merged in PRs #1024-#1030), open agent-ready issue supply dropped back to 2 (#1023 and #996), triggering this demand-driven refill audit.

Six distinct, reproducible defect areas were identified, adversarially verified against the codebase, drafted in accordance with `AGENT_ISSUE_FORMAT`, machine-linted via `issue_lint.py`, and filed to GitHub. All 6 issues passed the remote `Agents Issue Format Guard` with status `success`.

---

## 2. Baseline & Verification Environment

- **Commit**: `cdfd281866fb5bf23fce6dd22eb4f7367e0876fc`
- **Language**: Python 3.12+ (26,029 LOC in `src/counter_risk/` across 24 modules)
- **Test Suite**: 1,841 unit & integration tests collected via `uv run pytest` across 162 modules
- **Linter**: `ruff check src/` clean (0 diagnostics)
- **Pre-submit Linter**: `issue_lint.py` verified 0 errors / 0 advisories on all 6 issue bodies

---

## 3. Filed Issues & Verified Findings

| Issue ID | Priority | Category | Title | Affected Target Files |
|---|---|---|---|---|
| [#1031](https://github.com/stranske/Counter_Risk/issues/1031) | P2 | Wiring / Tooling | Support currency and accounting glyphs in pure-Python table PNG renderer | `src/counter_risk/renderers/table_png.py:576-619`, `src/counter_risk/renderers/table_png.py:371-374,544` |
| [#1032](https://github.com/stranske/Counter_Risk/issues/1032) | P2 | Correctness | Coerce finite numeric values in pipeline concentration and limit exposure builders | `src/counter_risk/pipeline/run.py:2270,2283,2333,2348` |
| [#1033](https://github.com/stranske/Counter_Risk/issues/1033) | P2 | Duplication / Correctness | Fix alias fallback and enforce finite floats in drop-in totals numeric extraction | `src/counter_risk/pipeline/run.py:2610-2621`, `src/counter_risk/writers/dropin_templates.py:108` |
| [#1034](https://github.com/stranske/Counter_Risk/issues/1034) | P2 | Correctness | Reject non-finite values during historical three-year workbook rollups | `src/counter_risk/writers/historical_update.py:357-368,465` |
| [#1035](https://github.com/stranske/Counter_Risk/issues/1035) | P2 | Standards / Correctness | Reject NaN and Infinity in manifest schema number type validator | `src/counter_risk/pipeline/manifest_schema.py:488-490,512` |
| [#1036](https://github.com/stranske/Counter_Risk/issues/1036) | P2 | Design / UX | Enforce finite numeric extraction and valid sorting in chat session exposures | `src/counter_risk/chat/session.py:700-714`, `src/counter_risk/chat/utils.py:23-35` |

---

## 4. Technical Analysis of Findings

### 1. Pure-Python Table PNG Glyph Support (`#1031`)
- **Root Cause**: `_GLYPHS` at `src/counter_risk/renderers/table_png.py:576` defined alphanumeric characters, spaces, dashes, dots, and slashes, but omitted `$`, `(`, and `)`.
- **Impact**: When table PNGs are rendered with `formatting_profile="currency"` or `"accounting"`, `_format_render_number` produces strings like `"$125.00"` or `"($15.00)"`. `_glyph_for()` falls back to `_GLYPHS["?"]`, rendering `$125.00` as `?125.00` and negative balances as `??15.00?`.
- **Verification**: `_glyph_for('$') == _GLYPHS['?']` returns `True`.

### 2. Pipeline Exposure Finite Numeric Coercion (`#1032`)
- **Root Cause**: `_build_concentration_exposure_rows` and `_build_limit_exposure_rows` in `src/counter_risk/pipeline/run.py` convert record numbers using `float(record.get(...) or 0.0)` wrapped in `try...except (TypeError, ValueError)`.
- **Impact**: `float('nan')` and `float('inf')` do not trigger `ValueError`, passing un-coerced into `compute_concentration_metrics` (`compute/rollups.py:575`) and `check_limits` (`compute/limits.py:95`), corrupting rollup metrics and bypassing limit checks.
- **Verification**: `_to_float` at `src/counter_risk/pipeline/run.py:4752` provides `math.isfinite` validation; applying it to exposure builders prevents non-finite values from propagating.

### 3. Drop-in Totals Extraction & Alias Fallback (`#1033`)
- **Root Cause**: In `src/counter_risk/pipeline/run.py:2610-2621`, `_row_numeric_value` immediately executes `return 0.0` if an alias key exists with value `None`.
- **Impact**: Given `row = {"cash": None, "Cash": 120.0}` with `aliases = ("cash", "Cash")`, the helper returns `0.0` rather than falling through to `"Cash"`. Additionally, it performs un-guarded `float(value)`, propagating `NaN` and `Inf` into drop-in template proportion calculations.
- **Verification**: `_row_numeric_value({"cash": None, "Cash": 120.0}, aliases=("cash", "Cash"))` returned `0.0` instead of `120.0`.

### 4. Historical Three-Year Rollup Update (`#1034`)
- **Root Cause**: `_coerce_rollup_data` in `src/counter_risk/writers/historical_update.py:357` converts rollup entries using `float(raw_value)` without checking `math.isfinite(numeric_value)`.
- **Impact**: `NaN` and `Inf` are accepted into normalized rollup dictionaries and written directly to historical Excel worksheets in `append_historical_row`.
- **Verification**: `_coerce_rollup_data({'Total': float('nan'), 'TIPS': float('inf')})` returned `{'total': nan, 'tips': inf}` without raising `HistoricalUpdateError`.

### 5. Manifest Schema Number Type Validator (`#1035`)
- **Root Cause**: `_matches_type(value, "number")` in `src/counter_risk/pipeline/manifest_schema.py:488` evaluated `isinstance(value, (int, float)) and not isinstance(value, bool)`.
- **Impact**: Because `isinstance(float('nan'), float)` is `True`, `validate_manifest` accepted `NaN` and `Infinity` in schema number fields, violating RFC 8259 JSON standards and failing in strict parsers.
- **Verification**: `_matches_type(float('nan'), 'number')` returned `True`.

### 6. Chat Session Exposure Extraction & Tolerance Sorting (`#1036`)
- **Root Cause**: `_parse_float` in `src/counter_risk/chat/session.py:700` converted numeric strings/floats without checking `math.isfinite()`.
- **Impact**: When `NaN` reaches `_sort_top_exposure_rows`, `cmp_with_tol` from `chat/utils.py:23` evaluates `cmp_with_tol(nan, 100) == 1` and `cmp_with_tol(100, nan) == 1`, violating strict weak ordering and corrupting exposure sorting.
- **Verification**: Verified tolerance comparison antisymmetry violation directly in Python.

---

## 5. Artifacts & Reconciliation Summary

- **Issue Bodies**: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/2026-09-09-issue-bodies/` (09-14)
- **Canonical Audit Report**: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/2026-09-09-02-AUDIT_REPORT.md`
- **Verification Log**: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/2026-09-09-02-verification-log.md`
- **Audit Run Metadata**: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/2026-09-09-02-audit-run.md`
- **Audit Ledger**: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/AUDIT_LEDGER.md`
- **Intake Log**: `~/.codex/orchestrator/measurement/intake-2026-09-04.log`
- **Checkpoints**: `D-audit-Counter_Risk--2026-09-09T17-29-35Z.CHECKPOINT.md` and `CHECKPOINT.md`
- **Supply Balance**: Replenished from 2 open agent-ready issues to 8 open agent-ready issues.
