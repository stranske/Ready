title:	Reject negative item counts and negative tier distributions in maintenance capacity estimation
state:	CLOSED
author:	stranske
labels:	bug, priority:normal
comments:	1
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	672
--
## Why

In `estimate_capacity` and `_weighted` (`src/lms/maintenance/budget.py:118-160`), input parameters `active_items` and `tier_counts` values are processed without validating that counts are non-negative integers. Negative `active_items` (e.g. `-50`) produces invalid utilization ratios (`-50 / capacity < 0.0`) and inflates remaining capacity headroom (`max(0, capacity - active_items)`), while negative values in `tier_counts` (e.g. `{"hot": -10, "warm": 5}`) corrupt weighted interval calculations and first-month review estimates.

## Scope

In `src/lms/maintenance/budget.py:118-160`:

```python
def _weighted(values: dict[str, float], tier_counts: dict[str, int] | None) -> float:
    """Weight per-tier constants by how many items actually use each tier."""
    counts = {tier: (tier_counts or {}).get(tier, 0) for tier in RETENTION_TIERS}
    total = sum(counts.values())
    if total == 0:
        return values[WARM]
    return sum(values[tier] * n for tier, n in counts.items()) / total


def estimate_capacity(
    settings: BudgetSettings,
    *,
    active_items: int,
    tier_counts: dict[str, int] | None = None,
    anchor_share: float = 0.5,
) -> CapacityEstimate:
    """Estimate capacity, validating anchor_share via items_affordable_per_day."""
    per_day, limited_by = items_affordable_per_day(settings, anchor_share=anchor_share)
    interval = mean_interval_days(tier_counts)
    capacity = max(1, int(per_day * interval))
    utilisation = active_items / capacity if capacity else 1.0
```

## Implementation Notes

1. In `src/lms/maintenance/budget.py`, validate in `estimate_capacity` that `if active_items < 0: raise ValueError("active_items must be a non-negative integer")`.
2. In `_weighted`, validate that if `tier_counts` is provided, all counts are non-negative integers (`if any(count < 0 for count in counts.values()): raise ValueError("tier counts must be non-negative integers")`).
3. In `tests/maintenance/test_tiers_horizon_budget.py`, add unit tests asserting `ValueError` is raised on negative `active_items` or negative `tier_counts`.

## Tasks

- [ ] In `src/lms/maintenance/budget.py`, add validation rejecting negative `active_items` and negative `tier_counts` in `estimate_capacity` and `_weighted`.
- [ ] In `tests/maintenance/test_tiers_horizon_budget.py`, add test cases asserting `ValueError` on negative item counts and negative tier distributions.

## Acceptance Criteria

- [ ] Running `pytest tests/maintenance/test_tiers_horizon_budget.py` passes cleanly.
- [ ] Calling `estimate_capacity(settings, active_items=-10)` raises `ValueError("active_items must be a non-negative integer")`.
- [ ] Calling `estimate_capacity(settings, active_items=10, tier_counts={"hot": -2})` raises `ValueError("tier counts must be non-negative integers")`.
- [ ] Deliberately breaking the validation logic causes the targeted tests to fail.

## Non-Goals

- Changing the capacity estimation formula or default budget settings constants in `src/lms/maintenance/budget.py`.
- Scaffold-only completion does NOT count: adding placeholder functions without enforcing non-negative bounds in `estimate_capacity` is a failure of this issue.

