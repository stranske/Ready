title:	fix(ci): test_scheduled_edgar_alert_transaction[success] returns empty channel list
state:	CLOSED
author:	stranske
labels:	agents:formatted, bug, priority:high
comments:	8
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1685
--
## Summary

Latest `CI` on `main` fails in `Postgres chain integration` ([run 35186583849](https://github.com/stranske/Manager-Database/actions/runs/35186583849), 2026-09-17):

```
FAILED tests/test_alert_postgres_integration.py::test_scheduled_edgar_alert_transaction[success]
AssertionError: assert [] == [(['streamlit'],)]
```

`Agents PR Health` on `main` is green; this is a product/integration defect in the postgres alert transaction path, not a gate-formatting issue.

## Tasks

- [ ] Reproduce locally with `pytest tests/test_alert_postgres_integration.py::test_scheduled_edgar_alert_transaction[success] -v` against `MGRDB_PG_TEST_URL`.
- [ ] Fix the scheduled EDGAR alert transaction so success path records `[('streamlit',)]` channels (see `tests/test_alert_postgres_integration.py:359`).
- [ ] Run `pytest tests/test_chain_postgres_integration.py -v` against `MGRDB_PG_TEST_URL` to confirm the postgres chain integration job passes.

## Acceptance Criteria

- `pytest tests/test_alert_postgres_integration.py tests/test_chain_postgres_integration.py -v` passes with postgres available.
- Latest `CI` workflow on `main` concludes success.

Filed by D3 unblock sweep 2026-09-17T18 — no prior tracking issue found. Repaired by D3 unblock sweep 2026-09-13T16 (task 3 concrete path; format guard unblock).

