## Why

Current break on tip 54e4f406: `ui/dashboard.py:48-64` queries `filings` unconditionally, so a SQLite bootstrap that only creates `managers` (the default local path after `POST /managers`) raises `DatabaseError: no such table: filings` when the Historical Filing Trend section renders. Closed #1647 fixed a wrong column name, not a missing table. Product contract MDB-6 marks this as partial (`docs/PRODUCT_CONTRACT.md:23`).

## Scope

Dashboard filing-trend loading and rendering when the database has managers but no filings schema yet; preserve existing counts when the table exists.

## Non-Goals

Do not remove the Historical Filing Trend section or change demo-database seed data. Scaffold-only completion does NOT count: try/except that hides the error without returning an empty, labeled frame is a failure of this issue.

## Tasks

- [ ] Guard `load_delta()` in `ui/dashboard.py:48-64` so a missing `filings` table returns an empty dataframe with the expected `date` and `filings` columns instead of raising.
- [ ] Update `render_historical_filing_trend()` in `ui/dashboard.py:1198-1199` to show an explicit empty-state caption when no filing rows exist.
- [ ] Add `tests/test_dashboard.py::test_load_delta_returns_empty_frame_without_filings_table` covering a managers-only SQLite file.

## Acceptance Criteria

- Named test: `tests/test_dashboard.py::test_load_delta_returns_empty_frame_without_filings_table` must pass and assert zero rows with the expected columns.
- Deliberate-break → revert: remove the guard in `ui/dashboard.py:48-64`; the named test must fail with `no such table: filings`; revert and rerun pytest tests/test_dashboard.py.

## Implementation Notes

Verified at 54e4f406: SQLite file containing only `CREATE TABLE managers(...)` triggers the error when `load_delta()` runs. Existing `test_load_delta_counts` in `tests/test_dashboard.py:443` covers populated filings and remains the control case.
