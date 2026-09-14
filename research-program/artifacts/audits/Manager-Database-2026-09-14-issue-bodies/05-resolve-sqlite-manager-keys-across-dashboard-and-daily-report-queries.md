## Why

Current local SQLite break: `scripts/seed_managers.py:48` creates managers.id, but `ui/dashboard.py:364` and `ui/dashboard.py:1023` select manager_id directly. `ui/daily_report.py:32`, `ui/daily_report.py:57`, and `ui/daily_report.py:102` repeat the hardcoded join. Matched synthetic databases differing only in that primary-key name return 2 versus 0 manager rows, 2 versus 0 QC warnings, 1 versus 0 news rows; the no-view daily-diff fallback crashes with no such column m.manager_id.

## Scope

Dashboard selector/QC summary and daily-report manager joins across both supported SQLite primary-key spellings; preserve Postgres behavior.

## Non-Goals

Do not rename user database columns or remove QC/empty-state behavior. Scaffold-only completion does NOT count: repairing the selector while daily-report joins still fail is a failure of this issue.

## Tasks

- [ ] Use `resolve_manager_id_column` from `adapters/base.py` in the manager queries in `ui/dashboard.py`, aliasing IDs to the existing output field.
- [ ] Apply the same resolved key to daily-diff fallback, news, and activism joins in `ui/daily_report.py`, keeping dialect-specific placeholders.
- [ ] Extend `tests/test_dashboard.py` and `tests/test_daily_report_views.py` with matched id and manager_id fixtures, including absent mv_daily_report, stale filings, news, and activism.

## Acceptance Criteria

- [ ] pytest tests/test_dashboard.py tests/test_daily_report_views.py must pass; new key-matrix tests return the same manager IDs, QC warnings, diffs, news and activism records for both schemas without a swallowed SQL error.
- [ ] Deliberate-break gate: Restore one hardcoded manager_id join in `ui/daily_report.py`; its new id-schema case in `tests/test_daily_report_views.py` must fail; revert and rerun.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Closed 1649 fixed upload and closed 1651 fixed activism API; current upload and dashboard-news fixes are controls, not duplicate targets. The browser demo uses manager_id and does not expose this schema difference.
