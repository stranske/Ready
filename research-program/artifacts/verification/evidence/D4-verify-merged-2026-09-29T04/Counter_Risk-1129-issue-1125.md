title:	[P2] D4 follow-up: deliberate-break transcript for merged PR #1124 (#1073)
state:	CLOSED
author:	stranske
labels:	priority:normal
comments:	2
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1125
--
## Why (verified evidence)

D4-verify-merged-2026-09-27T03 read squash diff for stranske/Counter_Risk#1124 (merge `d7701d6019d8…`) against #1073. The CPRS-CH workbook regression now lives in `tests/pipeline/test_reconciliation.py` (deletes standalone `tests/pipeline/test_cprs_ch_workbook_total.py`). Local run: `pytest tests/pipeline/test_reconciliation.py --cov=counter_risk.pipeline.run --cov-report=term-missing -q` → 24 passed with coverage recorded in the PR body.

Issue #1073 acceptance still requires **both** deliberate-break runs recorded in the PR/issue with literal pytest output (break `math.isfinite`/bool guard in `src/counter_risk/pipeline/run.py` → regression FAILS → revert → passes). PR #1124 describes the break narratively without pasted FAIL output.

## Tasks

- [ ] Temporarily remove the finite-total guard in `src/counter_risk/pipeline/run.py` (`_extract_mosers_program_notional_from_cprs_ch` / reconciliation path exercised by the moved tests), run `pytest tests/pipeline/test_reconciliation.py -k invalid_workbook -q` (or the parametrized invalid-notional cases), capture FAIL transcript.
- [ ] Revert the guard, re-run, capture PASS transcript, and post RED/GREEN blocks on #1073 (or add under `docs/evidence/issue-1073-reconciliation-deliberate-break.md`).

## Acceptance Criteria

- Named test: `pytest tests/pipeline/test_reconciliation.py --cov=src/counter_risk/pipeline/run.py --cov-report=term-missing` exits 0 on `main` (already satisfied).
- Deliberate-break → revert: guard removal causes the moved invalid-workbook regression to FAIL; restore causes pass; **literal pytest output** for both runs attached to #1073.

## Non-Goals

- Do NOT move tests back out of `test_reconciliation.py`.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-27T03; verified against `Counter_Risk-1124.diff` and issue #1073. Related: #1073, merged PR #1124._

