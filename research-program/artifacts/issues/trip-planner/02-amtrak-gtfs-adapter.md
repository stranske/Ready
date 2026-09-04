## Why

NEC rail schedules for US Northeast corridor (owner default #14). Verified: `clones/trip-planner/trip_planner/sources/adapters/__init__.py:3-5` exports only `SourceAdapter` base — no GTFS adapter module. **Missing behavior:** no Amtrak schedule ingestion.

## Scope

`AmtrakGtfsAdapter` loading static GTFS ZIP fixture in CI.

## Non-Goals

- Do NOT depend on live GTFS download in CI.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `trip_planner/sources/adapters/amtrak_gtfs.py`.
- [ ] Add `tests/fixtures/gtfs/` minimal stop/route subset.
- [ ] Add `tests/sources/test_amtrak_gtfs_adapter.py`.

## Acceptance Criteria

- [ ] Named test: `tests/sources/test_amtrak_gtfs_adapter.py::test_parses_fixture_trips` passes.
- [ ] **Deliberate-break gate:** corrupt `stop_times.txt` → test **must FAIL** → revert.

_Surfaced by B2-046._
