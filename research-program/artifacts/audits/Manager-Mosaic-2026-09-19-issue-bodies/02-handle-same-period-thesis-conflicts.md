## Why

`evaluate_claim()` selects one matching fact with `max(..., key=(period chronology, evidence_id))` (`src/manager_mosaic/thesis.py:58-75`). For two conflicting values in the same latest period, the lexicographically largest `evidence_id` decides whether a `min` or `max` claim is supported or contradicted. This is a current correctness break: relabeling the same two evidence records changes the thesis verdict even though the economic evidence is unchanged. `ThesisVerdict` already reserves `at_risk` (`src/manager_mosaic/thesis.py:16-21`) but no branch returns it.

## Scope

Define deterministic handling for conflicting matching facts in the latest period and return the relevant evidence identifiers instead of allowing an arbitrary evidence ID tie-break to choose the thesis verdict.

## Non-Goals

- Do not add LLM narrative comparison, alert delivery, dashboards, or persistence.
- Do not change normal single-fact or different-period threshold behavior already covered by `tests/test_thesis_monitoring.py`.
- Scaffold-only completion does not count: a new enum branch without an order-independent conflict regression test and deliberate-break evidence is incomplete.

## Tasks

- [ ] In `src/manager_mosaic/thesis.py::evaluate_claim`, group facts at the latest chronological period and return `at_risk` with the participating `evidence_ids` when those facts imply both supported and contradicted outcomes for the same claim.
- [ ] In `tests/test_thesis_monitoring.py`, add `test_evaluate_claim_same_period_conflict_is_independent_of_evidence_id_order` with the same values assigned to opposite `evidence_id` strings in two inputs.
- [ ] In `tests/test_thesis_monitoring.py::test_evaluate_claim_same_period_conflict_is_independent_of_evidence_id_order`, temporarily restore single-record `evidence_id` tie-breaking, confirm the named test fails, then revert the deliberate break before committing.

## Acceptance Criteria

- [ ] `python3 -m pytest -q --no-cov tests/test_thesis_monitoring.py::test_evaluate_claim_same_period_conflict_is_independent_of_evidence_id_order` passes and yields the same `at_risk` verdict and evidence set for both ID assignments.
- [ ] The deliberate break that restores `src/manager_mosaic/thesis.py` single-record evidence-ID selection makes `tests/test_thesis_monitoring.py::test_evaluate_claim_same_period_conflict_is_independent_of_evidence_id_order` fail; it is reverted and the named test passes again.
- [ ] `python3 -m pytest -q --no-cov tests/test_thesis_monitoring.py tests/test_discrepancy_detection.py` passes.

## Implementation Notes

Keep selection of the latest *period* deterministic. The required change is only for conflicting values at that same latest period; use the existing `ThesisCheck.evidence_ids` tuple to preserve reviewable provenance.
