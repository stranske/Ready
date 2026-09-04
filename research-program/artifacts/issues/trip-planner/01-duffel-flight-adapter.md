## Why

trip-planner has `SourceAdapter` ABC (`trip_planner/sources/adapters/base.py:15`) but only fixture adapters in production path (`app/services/inventory.py:858` uses `PersistedTripInventoryFixtureAdapter`). Architecture ahead of data (R7).

## Scope

`DuffelFlightAdapter` implementing `SourceAdapter` with test-mode API + recorded fixture for CI.

## Non-Goals

- Do NOT scrape Google Flights (B2-R reject).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `trip_planner/sources/adapters/duffel_flight.py`.
- [ ] Add `tests/sources/test_duffel_adapter_offline.py` per `docs/contracts/source-adapters.md:23-30`.
- [ ] Register adapter in `trip_planner/sources/__init__.py`.

## Acceptance Criteria

- [ ] Named test: `tests/sources/test_duffel_adapter_offline.py::test_emits_raw_snapshot` passes.
- [ ] **Deliberate-break gate:** return empty `RawSnapshot.records` → test **must FAIL** → revert.

_Surfaced by B2-045; owner needs Duffel test account for live verification only._
