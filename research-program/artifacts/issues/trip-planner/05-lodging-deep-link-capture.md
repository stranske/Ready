## Why

Honest lodging lane without OTA APIs (R7 §5). Verified: `clones/trip-planner/trip_planner/sources/adapters/__init__.py:3-5` lists only the base adapter — no lodging module. **Depends on:** provenance contracts (`docs/contracts/source-adapters.md:21`; verified `clones/trip-planner/docs/contracts/source-adapters.md`).

## Scope

Capture flow storing deep links + `ProvenanceReference` seeds per `source-adapters.md:21`.

## Non-Goals

- Do NOT implement live OTA search (B2-R24 reject).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `trip_planner/sources/adapters/lodging_deep_link.py`.
- [ ] Add `tests/sources/test_lodging_deep_link.py`.

## Acceptance Criteria

- [ ] Named test: `tests/sources/test_lodging_deep_link.py::test_provenance_seed_present` passes.
- [ ] **Deliberate-break gate:** drop provenance → test **must FAIL** → revert.

_Surfaced by B2-050._
