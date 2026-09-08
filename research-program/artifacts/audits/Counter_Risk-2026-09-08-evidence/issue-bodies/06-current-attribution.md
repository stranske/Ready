# [P2] Reconcile split current rows before matching prior attribution

## Why

`src/counter_risk/reports/change_attribution.py:215` aggregates prior rows, while its loop at line 224 still matches each ungrouped current row to the same prior balance at line 231. In the actual CSV writer path, `src/counter_risk/pipeline/run.py:2069` infers prior balances and passes them to this report. Lead-seat output probes used a current total of 300 and supplied total NotionalChange of 50: one row emitted change 50 and prior 250; splitting the same total into 100 and 200 with changes 25 each emitted summed change -200 and prior 500, with no pipeline warning. Direct helper controls also reproduced the duplicate prior use. The defect requires split or duplicate current counterparty rows; no claim is made that the bundled fixture has them.

## Scope

Current and prior aggregation consistency in change attribution, including the generated CSV integration path and supplied deltas.

## Non-Goals

No new financial model, source-format rewrite or upstream workflow change. Scaffold-only or partial completion does NOT count as done; the behavior and test gates must be delivered.

## Tasks

- [ ] In `src/counter_risk/reports/change_attribution.py`, group current rows consistently with prior lookup keys before matching, retaining deterministic labels and summed supplied deltas with explicit missing-delta semantics.
- [ ] Extend `tests/test_change_attribution_report.py` with split-versus-single controls asserting conserved current notional, prior notional and total change.
- [ ] Extend `tests/pipeline/test_run_pipeline.py` to drive `_write_change_attribution_outputs` and parse its CSV for the single notional 300 with change 50 versus split notional 100 with change 25 and notional 200 with change 25 cases.

## Acceptance Criteria

- [ ] `python -m pytest tests/test_change_attribution_report.py tests/pipeline/test_run_pipeline.py -q -m "not slow and not release"` passes with a new split-current-conservation regression.
- [ ] The generated CSV has summed current 300, prior 250 and change 50 for both shapes; splitting or permuting current rows cannot duplicate prior notional.
- [ ] Deliberate-break gate: restore the ungrouped current iteration in `src/counter_risk/reports/change_attribution.py`; the new split-current-conservation test must fail with the duplicated prior; restore aggregation and rerun.

## Implementation Notes

Adjacent to closed #1003, which fixed prior-row overwrite only, and #1001, which groups current rows in futures_delta. This is a distinct remaining current-side report gap. The first lead integration probe used an unsupported delta alias and skipped output; the corrected probe uses the actual NotionalChange field and reproduces the CSV defect.
