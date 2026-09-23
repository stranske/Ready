## Why (verified evidence)

The deprecated `trip_plan_from_minimal` adapter applies caller overrides via `TripPlan.model_copy(update=...)` without re-validation, so invalid `trip_id`, `status`, and transport values become trusted `TripPlan` instances.

- `src/travel_plan_permission/conversion.py:36-50` — builds `overrides` then `return plan_input.plan.model_copy(update=overrides)` with no `TripPlan.model_validate`.
- Reproduction on tip: `trip_plan_from_minimal(payload, trip_id=None, status="not-a-status")` returns a plan with `trip_id is None` and `status == "not-a-status"`.

## Tasks

- [ ] In `src/travel_plan_permission/conversion.py:50`, replace bare `model_copy` with `TripPlan.model_validate(plan_input.plan.model_copy(update=overrides))` (or equivalent validated rebuild).
- [ ] Keep the deprecation warning; do not expand the public surface of this helper.

## Acceptance Criteria

- Named test: `tests/python/test_minimal_conversion.py::test_trip_plan_from_minimal_validates_overrides` — `trip_id=None` and `status="not-a-status"` raise `ValidationError`.
- Deliberate-break → revert: restore unvalidated `model_copy` → named test FAILS → revert.

## Non-Goals

- Do NOT remove `trip_plan_from_minimal` in this issue (callers still migrate to `load_trip_plan_input`).
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Reproduction:_
```python
import json, warnings
from pathlib import Path
from travel_plan_permission.conversion import trip_plan_from_minimal
payload = json.loads(Path("tests/fixtures/sample_trip_plan_minimal.json").read_text())
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    p = trip_plan_from_minimal(payload, trip_id=None, status="not-a-status")
print(p.trip_id, p.status)  # None not-a-status
```

_Surfaced by Track D repo-audit 2026-09-23; verified on clone tip._
