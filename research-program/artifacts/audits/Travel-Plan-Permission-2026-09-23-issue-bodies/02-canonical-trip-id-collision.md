## Why (verified evidence)

Canonical intake assigns `trip_id` from departure date and traveler name only (`TRIP-{date}-{slug}`), so two distinct trips for the same traveler on the same day collide. Downstream planner and portal state keyed by `trip_id` can overwrite or alias unrelated trips.

- `src/travel_plan_permission/canonical.py:136-137` — `_default_trip_id` uses only `depart_date` and `traveler_name`.
- `src/travel_plan_permission/canonical.py:198-205` — `canonical_trip_plan_to_model` always sets `trip_id=_default_trip_id(plan)` when the caller does not supply one.
- Reproduction: two `load_trip_plan_input` payloads from `tests/fixtures/sample_trip_plan_minimal.json` with `city_state` changed to Chicago vs Denver both yield `TRIP-20251001-JANE-DOE`.

## Tasks

- [ ] Extend `_default_trip_id` in `src/travel_plan_permission/canonical.py:136-137` with a collision-resistant suffix (destination hash, purpose slug, or UUID) while preserving human-readable prefixes where possible.
- [ ] Document the stability expectation in `schemas/trip_plan.min.schema.json` or contract docs if callers must supply explicit IDs for idempotent replays.

## Acceptance Criteria

- Named test: `tests/python/test_canonical_trip_plan.py::test_canonical_conversion_generates_distinct_ids_for_distinct_same_day_trips` — same traveler and `depart_date`, different destinations; assert `trip_id` values differ.
- Deliberate-break → revert: restore date+name-only ID → named test FAILS → revert.

## Non-Goals

- Do NOT break callers that pass an explicit `trip_id` in canonical payloads.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Reproduction:_
```python
import copy, json
from pathlib import Path
from travel_plan_permission.canonical import load_trip_plan_input
payload = json.loads(Path("tests/fixtures/sample_trip_plan_minimal.json").read_text())
p1 = copy.deepcopy(payload); p1["city_state"] = "Chicago, IL"
p2 = copy.deepcopy(payload); p2["city_state"] = "Denver, CO"
assert load_trip_plan_input(p1).plan.trip_id == load_trip_plan_input(p2).plan.trip_id  # observed True on tip
```

_Surfaced by Track D repo-audit 2026-09-23; verified on clone tip._
