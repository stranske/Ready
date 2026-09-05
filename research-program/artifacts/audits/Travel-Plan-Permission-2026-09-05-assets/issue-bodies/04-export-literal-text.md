# [P1] Preserve untrusted export text as literal spreadsheet cells

## Why

Current break: vendor =1+1 and cost center =2+2 become formula cells in the generated workbook, and are emitted unchanged in CSV. `src/travel_plan_permission/export.py:62` copies vendor and cost-center strings into export rows, `src/travel_plan_permission/export.py:85` writes CSV rows, and `src/travel_plan_permission/export.py:110` appends those strings into openpyxl cells. Independent inspection of the saved XLSX reports data_type f for B2 and E2. The goal is faithful export of expense metadata as text. Only benign arithmetic formulas were used in verification; no external data access was attempted.

## Scope

Literal-text handling for user-controlled vendor, cost-center and receipt-link fields in CSV and XLSX exports, preserving numeric amount cells.

## Non-Goals

Changing accounting schema, disabling all hyperlinks or evaluating formulas during tests. Scaffold-only completion does NOT count: escaping only the displayed portal text while downloaded workbooks retain formula cells is a failure of this issue.

## Tasks

- [ ] In `src/travel_plan_permission/export.py`, serialize user-controlled XLSX text with explicit text cell semantics so leading formula characters cannot change cell type.
- [ ] In `src/travel_plan_permission/export.py`, apply and document a CSV literal-text policy for leading formula or control prefixes without altering amount values or permitted receipt URLs.
- [ ] Add `test_export_preserves_literal_user_text` to `tests/python/test_export_service.py` for equals, plus, minus, at-sign and leading whitespace and control variants; inspect saved cell types and parsed CSV fields.

## Acceptance Criteria

- [ ] Run pytest `tests/python/test_export_service.py::test_export_preserves_literal_user_text`; workbook B2 and E2 preserve the supplied strings with text types, CSV follows the documented policy, and C2 remains numeric.
- [ ] Deliberate-break gate: restore direct user text writes in `src/travel_plan_permission/export.py`; `tests/python/test_export_service.py::test_export_preserves_literal_user_text` must fail its formula-type or CSV-prefix assertions; revert the break.

## Implementation Notes

Audited remote main: 3ba14a8541b97338586ab6c253ea30e2aed7b86e.

formula-proof.json captures f cell types for benign formulas. The browser expense route also exported a vendor value beginning with equals. No matching issue appears in the current 150-issue inventory.

Guidance: [OWASP CSV injection](https://owasp.org/www-community/attacks/CSV_Injection) explains that CSV quoting alone is insufficient and mitigations depend on the consuming spreadsheet. Document and test the supported import behavior; do not promise universal safety across spreadsheet engines.
