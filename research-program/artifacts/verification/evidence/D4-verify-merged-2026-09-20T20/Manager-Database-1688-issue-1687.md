title:	fix(etl): initialize PostgreSQL manager similarity storage
state:	MERGED
author:	stranske
labels:	agent:codex, agents:keepalive, autofix, codex, verify:compare
comments:	6
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1687
--
## Summary

PostgreSQL calls to `ensure_manager_similarity_table()` previously returned without creating or checking storage. The helper now creates `manager_similarity` and its two indexes using idempotent PostgreSQL DDL, preserves the caller transaction, and adds the nullable cosine column to legacy tables. Foreign keys use the canonical PostgreSQL `managers.manager_id`; `FLOAT(24)` matches the existing schema's `REAL` precision.

Closes #1653

## Tasks

- [x] Add the PostgreSQL DDL branch to `ensure_manager_similarity_table()`.
- [x] Cover schema creation, indexes, repeated initialization and error propagation using a non-SQLite connection.
- [x] Preserve legacy SQLite rows and verify repeated initialization still works.

## Acceptance Criteria

- [x] `python3 -m pytest tests/test_manager_similarity_flow.py -v`: 8 passed.
- [x] PostgreSQL mock connection receives table creation DDL with the canonical manager foreign keys, ordered-pair constraint, timestamp and similarity fields.
- [x] Removing the PostgreSQL branch makes the same module fail: 2 failed, 6 passed. Restoring it gives 8 passed. Logs captured in the opener run evidence directory `20260919T160115Z`.

<!-- deliberate-break: test=tests/test_manager_similarity_flow.py::test_ensure_manager_similarity_table_creates_postgres_schema test-file=tests/test_manager_similarity_flow.py break-file=etl/manager_similarity_flow.py command="python3 -m pytest tests/test_manager_similarity_flow.py::test_ensure_manager_similarity_table_creates_postgres_schema -q" -->

## Validation

- `python3 -m pytest tests/test_manager_similarity_flow.py tests/test_schema.py -v`: 26 passed.
- Ruff and Black checks on both changed files passed.
- Focused mypy with `--follow-imports=silent` passed for both changed files. Broad import-following mypy reports 12 existing errors in five unchanged API/ETL modules.
- PostgreSQL behavior is covered with mock connections and canonical schema inspection; a live PostgreSQL server was unavailable locally.


<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

- **Bug Fixes**
  - Improved manager similarity data storage compatibility for PostgreSQL and SQLite.
  - Existing SQLite data is preserved when upgrading the table structure.
  - Added stronger data integrity checks, including required relationships and similarity value constraints.
  - Added indexes to support more efficient similarity-related operations.
  - Repeated setup is now handled safely without disrupting the caller’s transaction.
  - Added support for upgrading existing tables with cosine similarity data.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->
