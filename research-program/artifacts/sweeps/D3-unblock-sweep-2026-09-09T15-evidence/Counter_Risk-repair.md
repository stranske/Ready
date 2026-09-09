# Counter_Risk CI Repair Specification
**Failure**: `black --check --line-length 100` failed on main commit `cdfd281` (PR #1030).
**File**: `src/counter_risk/writers/historical_update.py`
**Fix**: Reformat `worksheet.cell(...)` calls at lines 804-813 using Black 26.5.1.
