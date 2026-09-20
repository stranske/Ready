title:	fix(etl): implement Postgres schema check in ensure_manager_similarity_table
state:	CLOSED
author:	stranske-automation-bot
labels:	bug, priority:normal, testing
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
number:	1653
--
## Why

In `etl/manager_similarity_flow.py:27-47`, the function `ensure_manager_similarity_table(conn)` executes table creation DDL only when `isinstance(conn, sqlite3.Connection)`.

When executed against a PostgreSQL connection, `ensure_manager_similarity_table(conn)` executes no statements and provides no fallback or table verification. This inconsistency contrasts with all other table ensure functions across the codebase (such as `etl/conviction_flow.py`, `alerts/db.py`, and `etl/activism_detection.py`), which provide PostgreSQL DDL branches.

## Scope

- Implement PostgreSQL DDL execution in `ensure_manager_similarity_table()` in `etl/manager_similarity_flow.py:27-47` matching dialect patterns used across `etl/`.
- Add test coverage in `tests/test_manager_similarity_flow.py` verifying table creation DDL execution on PostgreSQL connections.

## Implementation Notes

- Mirror the PostgreSQL table creation schema in `etl/conviction_flow.py` using `BIGINT`, `TIMESTAMPTZ`, and `FLOAT` types.
- Ensure idempotent execution using `CREATE TABLE IF NOT EXISTS manager_similarity (...)`.

## Non-Goals

- Modifying similarity computation algorithms or vector embedding distance metrics.
- Adding scaffold-only stubs, mocks, or empty bypass functions without wiring up the real implementation does NOT count as done and constitutes a failure of this issue.

## Tasks

- [ ] Add PostgreSQL dialect DDL branch to function `ensure_manager_similarity_table()` in `etl/manager_similarity_flow.py`.
- [ ] Add test cases in `tests/test_manager_similarity_flow.py` asserting PostgreSQL DDL executes on non-SQLite connection instances.

## Acceptance Criteria

- Running `pytest tests/test_manager_similarity_flow.py` executes without errors.
- Calling `ensure_manager_similarity_table(pg_conn)` on a PostgreSQL mock connection executes DDL creating table `manager_similarity`.
- Verification gate: deliberately break the implementation by omitting PostgreSQL handling in `etl/manager_similarity_flow.py` and verify `pytest tests/test_manager_similarity_flow.py` fails.

