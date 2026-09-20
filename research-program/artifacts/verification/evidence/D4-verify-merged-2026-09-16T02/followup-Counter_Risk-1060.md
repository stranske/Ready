## Why (verified evidence)

Post-merge verification (D4-verify-merged-2026-09-16T02) of stranske/Counter_Risk#1060 (merge `537c913cf54bab0f8bfe59a72edea4bfc575d862`) against #1058 found the behavioral fix in `src/counter_risk/pipeline/run.py` landed, but the **named acceptance gate was not satisfied**.

- Issue #1058 requires the regression in `tests/pipeline/test_reconciliation.py` with `pytest tests/pipeline/test_reconciliation.py --cov=src/counter_risk/pipeline/run.py --cov-report=term-missing`.
- Squash diff adds `tests/pipeline/test_cprs_ch_workbook_total.py` only; `test_reconciliation.py` is untouched.
- PR body in evidence does not record baseline coverage, measured delta, or deliberate-break output for the named command.

## Tasks

- [ ] Move or duplicate the invalid-workbook-total regression into `tests/pipeline/test_reconciliation.py` (or extend that file) so the issue-named gate exercises the same branch.
- [ ] Run `pytest tests/pipeline/test_reconciliation.py --cov=src/counter_risk/pipeline/run.py --cov-report=term-missing` on main and record baseline + delta in the PR body.
- [ ] Add deliberate-break evidence: break the `math.isfinite`/bool guard in `src/counter_risk/pipeline/run.py` → named pytest fails → revert → passes; retain literal output in PR body.

## Acceptance Criteria

- Named test: `pytest tests/pipeline/test_reconciliation.py --cov=src/counter_risk/pipeline/run.py --cov-report=term-missing` exits 0 with coverage delta recorded in the PR body.
- Deliberate-break → revert: remove the finite-total guard in `src/counter_risk/pipeline/run.py` → confirm the new regression in `test_reconciliation.py` FAILS → revert → passes; both runs recorded in PR body.

## Non-Goals

- Do NOT change CI or workflow configuration (#1058 non-goal).
- No scaffolding / TODO-only changes; every task is verified by the gate above.

_Surfaced by D4-verify-merged-2026-09-16T02; verified against squash diff `Counter_Risk-1060.diff` and closed issue #1058 acceptance criteria. Related: #1058, merged PR #1060._
