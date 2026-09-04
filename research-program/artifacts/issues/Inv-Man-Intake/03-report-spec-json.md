## Why

OnePagerModel is renderer-oriented but no `report-spec.json` fleet profile exists. Verified: `clones/Inv-Man-Intake/tests/export/test_one_pager.py:1-30` exercises one-pager export without any `report-spec.json` assertion, and `grep -r report-spec clones/Inv-Man-Intake/src` returns no matches. **Missing behavior:** no output-substrate profile emission. **Depends on:** Pension-Data B2-029 renderer-shell, Workflows B2-028.

## Scope

Emit `report-spec.json` alongside one-pager exports referencing output-substrate profile.

## Non-Goals

- Do NOT fork Pension-Data web app.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/inv_man_intake/export/report_spec.py`.
- [ ] Wire into existing one-pager export path (`tests/export/test_one_pager.py` reference).
- [ ] Add `tests/export/test_report_spec.py`.

## Acceptance Criteria

- [ ] Named test: `tests/export/test_report_spec.py::test_report_spec_validates` passes.
- [ ] **Deliberate-break gate:** remove `renderer_profile` → test **must FAIL** → revert.

_Surfaced by B2-031._
