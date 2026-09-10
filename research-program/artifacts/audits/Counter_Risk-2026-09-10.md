# Counter_Risk Demand-Driven Audit Refill Report — 2026-09-10

- **Repository**: `stranske/Counter_Risk`
- **Unit**: `D-audit-Counter_Risk--2026-09-10T17-45-12Z`
- **Trigger**: Open agent-ready issue supply dropped to 1 <= 2 (#996).
- **Tip Commit**: `a846d4b098137ea098dfdf62e3c6f0572fb9d18b`
- **Auditor**: Gemini (Antigravity `repo-audit` skill)
- **Status**: 7 verified findings, 7 issues filed, all 7 passed format guard on GitHub Actions.

---

## Executive Summary

A comprehensive, demand-driven refill audit across all 8 dimensions was executed against `stranske/Counter_Risk` at tip commit `a846d4b098137ea098dfdf62e3c6f0572fb9d18b`.

Seven concrete, reproducible defect areas were identified, adversarially verified against the local runtime environment, drafted into machine-linted `AGENT_ISSUE_FORMAT` work orders, and filed to GitHub:

1. **Table PNG Numeric Cell Alignment (`#1044`)**: `_render_cprs_table_png` draws all cell text left-aligned (`x + _CELL_PADDING_X`), ignoring `column.header_align == "right"` for numeric columns (Cash, TIPS, Treasury, Equity, Commodity, Currency, Notional), causing numbers to misalign under right-aligned headers.
2. **Change Attribution Alias Fallback & Boolean Coercion (`#1045`)**: `_optional_float` executes `return None` on encountering the first key with `None` or empty string instead of continuing to subsequent alias keys in `_DELTA_COLUMNS`, and lacks boolean guards (`True` converts to `1.0`).
3. **Rollup Numeric Alias Traversal & Boolean Coercion (`#1046`)**: `_find_numeric` executes `break` instead of `continue` when a candidate key is `None` or empty string, terminating alias traversal prematurely and raising `ValueError`. Also converts `True` to `1.0`.
4. **Limits Notional Fallback on None (`#1047`)**: `_find_notional` immediately raises `ValueError` when encountering candidate keys with `None` or empty string values rather than evaluating remaining fallback keys in `_NOTIONAL_KEYS`.
5. **XLSX Reader Accounting Float Boolean Rejection (`#1048`)**: `coerce_accounting_float` lacks `not isinstance(value, bool)` guard before `isinstance(value, (int, float))`, converting `True` to `1.0` and `False` to `0.0` instead of raising `ValueError`.
6. **PPT Concentration Table Non-Finite and None Formatting (`#1049`)**: `append_concentration_table_slide` uses `f"{float(value):.2%}"` without `math.isfinite()` validation, rendering `None`, `NaN`, and `Inf` as `"None"`, `"nan%"`, and `"inf%"` into slide presentation cells.
7. **Data Quality Pipeline Warning Code Taxonomy Mapping (`#1050`)**: `NO_PRIOR_MATCH` and `NO_PRIOR_MONTH_MATCH` from futures delta and `WRITEBACK_MISSING_DESCRIPTION` and `WRITEBACK_NO_WORKBOOK_MATCH` from MOSERS workbook are missing from `_SEVERITY_BY_CODE` and `_CATEGORY_BY_CODE`, falling back to generic category `"pipeline"` instead of `"data_validation"`.

---

## Filed Issues

| Issue | Priority | Title | Target File:Lines | Status |
|---|---|---|---|---|
| [#1044](https://github.com/stranske/Counter_Risk/issues/1044) | P2 | Right-align numeric data cells under right-aligned column headers in pure-Python table PNG renderer | `src/counter_risk/renderers/table_png.py:293-303` | Guard Success |
| [#1045](https://github.com/stranske/Counter_Risk/issues/1045) | P2 | Fix alias fallthrough and reject booleans in change attribution float parsing | `src/counter_risk/reports/change_attribution.py:96-109` | Guard Success |
| [#1046](https://github.com/stranske/Counter_Risk/issues/1046) | P2 | Fix premature loop termination and reject booleans in rollup numeric field extraction | `src/counter_risk/compute/rollups.py:106-135` | Guard Success |
| [#1047](https://github.com/stranske/Counter_Risk/issues/1047) | P2 | Support fallback keys when earlier candidates contain None in limits notional extraction | `src/counter_risk/compute/limits.py:99-113` | Guard Success |
| [#1048](https://github.com/stranske/Counter_Risk/issues/1048) | P2 | Reject boolean values in XLSX reader accounting float coercion | `src/counter_risk/parsers/_xlsx_reader.py:171-176` | Guard Success |
| [#1049](https://github.com/stranske/Counter_Risk/issues/1049) | P2 | Format non-finite floats and None defensively in PPT concentration table slides | `src/counter_risk/ppt/concentration_table.py:86-98` | Guard Success |
| [#1050](https://github.com/stranske/Counter_Risk/issues/1050) | P2 | Map futures delta and MOSERS workbook warning codes in data quality pipeline taxonomy | `src/counter_risk/pipeline/data_quality.py:11-62` | Guard Success |

---

## Detailed Findings & Adversarial Verification

### Finding 1: Table PNG Numeric Cell Right-Alignment (`#1044`)
- **Location**: `src/counter_risk/renderers/table_png.py:293-303`
- **Defect**: In `_render_cprs_table_png`, cell text rendering X coordinate is unconditionally computed as `x + _CELL_PADDING_X`, regardless of `column.header_align`.
- **Verification**: Verified that columns configured with `header_align="right"` (such as `"Cash"`, `"TIPS"`, `"Treasury"`, `"Equity"`, `"Commodity"`, `"Currency"`, `"Notional"`) draw their headers right-aligned at `x + col_width - _CELL_PADDING_X - _text_width(column.name)`, but data values under those headers are rendered at left padding `x + _CELL_PADDING_X`.
- **Resolution**: Use `x + col_width - _CELL_PADDING_X - _text_width(cell_text)` when `column.header_align == "right"`.

### Finding 2: Change Attribution Alias Fallback & Boolean Coercion (`#1045`)
- **Location**: `src/counter_risk/reports/change_attribution.py:96-109`
- **Defect**: `_optional_float(row, keys)` checks each alias key in `keys`. If a row dictionary has a matching key whose value is `None` or `""`, line 108 executes `return None` immediately without continuing the loop. Furthermore, neither `_optional_float` nor `_first_float` guards against `isinstance(raw, bool)`.
- **Verification**: Evaluated `_optional_float({"delta": None, "daily_change": 42.5}, ("delta", "daily_change"))` returning `None` instead of `42.5`, and `_first_float({"Notional": True}, ("Notional",))` returning `1.0`.
- **Resolution**: Continue candidate iteration on `None` or invalid values, and add `not isinstance(raw, bool)` and `math.isfinite()` guards.

### Finding 3: Rollup Numeric Alias Loop Termination (`#1046`)
- **Location**: `src/counter_risk/compute/rollups.py:106-135`
- **Defect**: In `_find_numeric(row, candidates, ...)`, encountering a candidate key with `None` or whitespace executes `break` instead of `continue`, halting candidate search prematurely and raising `ValueError`.
- **Verification**: Evaluated `_find_numeric({"notional": None, "exposure": 100.0}, ("notional", "exposure"))` raising `ValueError: Missing required numeric field` despite valid fallback candidate `"exposure"`.
- **Resolution**: Change `break` to `continue` and reject boolean inputs.

### Finding 4: Limits Notional Fallback on None (`#1047`)
- **Location**: `src/counter_risk/compute/limits.py:99-113`
- **Defect**: In `_find_notional(row)`, encountering `None` or empty string in a primary candidate key raises `ValueError` immediately without evaluating remaining fallback keys in `_NOTIONAL_KEYS`.
- **Verification**: Evaluated `_find_notional({"notional": None, "exposure": 250000.0})` raising `ValueError: Invalid notional value: None`.
- **Resolution**: Fall through to subsequent candidate keys when candidate values are `None` or empty, and add boolean type checks.

### Finding 5: XLSX Accounting Float Boolean Rejection (`#1048`)
- **Location**: `src/counter_risk/parsers/_xlsx_reader.py:171-176`
- **Defect**: `coerce_accounting_float(value)` checks `isinstance(value, (int, float))` without an upfront `not isinstance(value, bool)` guard.
- **Verification**: Evaluated `coerce_accounting_float(True) == 1.0` and `coerce_accounting_float(False) == 0.0`.
- **Resolution**: Add `if isinstance(value, bool): raise ValueError(...)` before numeric checks.

### Finding 6: PPT Concentration Table Slide Formatting (`#1049`)
- **Location**: `src/counter_risk/ppt/concentration_table.py:86-98`
- **Defect**: `append_concentration_table_slide` uses `f"{float(value):.2%}"` without `math.isfinite()` checking or `None` handling, rendering `"None"`, `"nan%"`, and `"inf%"` in presentation slides.
- **Verification**: Evaluated cell formatting on `None`, `float("nan")`, and `float("inf")` producing unstyled raw strings.
- **Resolution**: Format `None`, non-numeric, and non-finite values as placeholder strings (`"-"` or `"N/A"`).

### Finding 7: Data Quality Pipeline Warning Code Taxonomy (`#1050`)
- **Location**: `src/counter_risk/pipeline/data_quality.py:11-62`
- **Defect**: Warning codes `NO_PRIOR_MATCH`, `NO_PRIOR_MONTH_MATCH` from futures delta and `WRITEBACK_MISSING_DESCRIPTION`, `WRITEBACK_NO_WORKBOOK_MATCH` from MOSERS workbook are missing from `_SEVERITY_BY_CODE` and `_CATEGORY_BY_CODE`.
- **Verification**: Verified `categorize_issue("NO_PRIOR_MATCH")` falls back to category `"pipeline"` instead of `"data_validation"`.
- **Resolution**: Register all four warning codes in `_SEVERITY_BY_CODE` and `_CATEGORY_BY_CODE` with category `"data_validation"`.

---

## 8-Dimension Audit Summary

- **Dimension 1: Code Quality & Correctness**: Change attribution alias fallback and boolean parsing (`#1045`), rollup numeric loop termination and boolean guard (`#1046`), limits notional fallback (`#1047`), and XLSX accounting float boolean coercion guard (`#1048`).
- **Dimension 2: Duplication & Fallback Logic**: Candidate alias traversal across sparse dictionaries with explicit `None` values (`#1045`, `#1046`, `#1047`).
- **Dimension 3: Functionality & Pipeline Wiring**: Pure-Python table PNG numeric cell right alignment under right-aligned headers (`#1044`).
- **Dimension 4: Design & UX**: PPT concentration table presentation slide formatting of `None`, `NaN`, and `Inf` placeholders (`#1049`).
- **Dimension 5: Public Field & Standards**: Data quality pipeline warning code taxonomy classification (`#1050`).
- **Dimension 6: Missed Opportunities**: Consistent candidate key fallthrough semantics on `None` across compute modules (`#1046`, `#1047`).
- **Dimension 7: Tooling**: Deterministic bitmap table PNG coordinate alignment test gates (`#1044`).
- **Dimension 8: Local Automations & CI**: Machine-verified AGENT_ISSUE_FORMAT bodies passing GitHub Actions format guard (`#1044-#1050`).

---

## Intake & Continuity Log

The 7 filed issues have been recorded in:
- `~/.codex/orchestrator/measurement/intake-2026-09-04.log`
- `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/README.md`
- `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/AUDIT_LEDGER.md`
- `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/2026-09-10-02-AUDIT_REPORT.md`
- `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/2026-09-10-02-verification-log.md`
