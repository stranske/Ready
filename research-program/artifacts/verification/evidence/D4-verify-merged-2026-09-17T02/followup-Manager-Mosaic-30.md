## Why (verified evidence)

`stranske/Manager-Mosaic#30` merged the thesis evaluator for `#13`, but the issue requires a deliberate-break demonstration on `evaluate_claim()` that is absent from the squash diff and PR body.

- `src/manager_mosaic/thesis.py::evaluate_claim` correctly returns `contradicted` for below-threshold `min` claims (merge SHA `9a85f2eeec75e09ea7c7a296bc91d4a0def886ed`).
- Issue `#13` acceptance criteria require inverting the comparison so a below-threshold fact returns `supported`, confirming `tests/test_thesis_monitoring.py::test_evaluate_claim_marks_contradicted_when_irr_below_min_threshold` FAILS, then reverting.
- PR #30 body leaves the deliberate-break checklist unchecked and provides no RED/GREEN transcript.

## Tasks

- [ ] In a follow-up PR linked to `#13`, temporarily invert the `min` comparison in `src/manager_mosaic/thesis.py::evaluate_claim` so an 8.5 IRR fact returns `supported`.
- [ ] Run `pytest tests/test_thesis_monitoring.py::test_evaluate_claim_marks_contradicted_when_irr_below_min_threshold -q` and capture failing output.
- [ ] Revert and capture passing output; paste both blocks in the PR body.

## Acceptance Criteria

- Named test: `tests/test_thesis_monitoring.py::test_evaluate_claim_marks_contradicted_when_irr_below_min_threshold` passes on `main`.
- Deliberate-break → revert: invert the `min` comparison in `evaluate_claim` → confirm the named test FAILS → revert and confirm it passes. Paste RED and GREEN blocks in the PR.

## Non-Goals

- Do not add LLM narrative evaluation, alerting, or dashboards.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-17T02; verified by reading squash diff for PR #30 at merge SHA `9a85f2ee`._
