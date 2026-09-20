title:	fix(ci): scheduled EDGAR alert transaction preserves streamlit delivery (#1685)
state:	MERGED
author:	stranske
labels:	agent:cursor, agent:retry, agents:keepalive, autofix, autofix:patch, verify:compare
comments:	12
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1686
--
## Summary
- Fix `fetch_and_store` so successful scheduled EDGAR runs do not roll back already-committed `alert_history` delivery records in `finally`.
- Align cleanup with `ingest_flow`: rollback only on exception after per-filing commits.

## Context
`CI` / Postgres chain integration fails on `main`:
```
FAILED tests/test_alert_postgres_integration.py::test_scheduled_edgar_alert_transaction[success]
AssertionError: assert [] == [(['streamlit'],)]
```

The callback-failure parametrization already passed; the success path lost committed alert rows during unconditional `finally` cleanup.

## Test plan
- [ ] `pytest tests/test_alert_postgres_integration.py::test_scheduled_edgar_alert_transaction -v` (with `MGRDB_PG_TEST_URL`)
- [ ] `pytest tests/test_alert_postgres_integration.py tests/test_chain_postgres_integration.py -v`
- [ ] Postgres chain integration CI job green on `main`

Closes #1685

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **Bug Fixes**
  * Improved transaction handling during filing and alert processing.
  * Successful processing now preserves saved filing, holdings, document, and alert updates instead of rolling them back during cleanup.
  * Failed processing continues to roll back incomplete changes, helping prevent partial or inconsistent records.
  * Filing and alert results are now handled more reliably across successful and unsuccessful processing attempts.
* **Tests**
  * Added coverage to verify that successful processing preserves committed records and failed processing rolls back incomplete changes.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->
