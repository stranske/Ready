title:	Validate retention tier enum membership in maintenance item tier updates
state:	CLOSED
author:	stranske
labels:	bug, priority:normal
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
number:	670
--
## Why

In `set_item_tier` (`src/lms/maintenance/service.py:289-312`), the `retention_tier` parameter is assigned directly to `item.retention_tier` and `card.retention_tier` without validating that `retention_tier in RETENTION_TIERS` (`'hot'`, `'warm'`, `'cold'`). When an unsupported tier (e.g. `"ultra-hot"` or `"invalid"`) is provided, `session.flush()` crashes with a database `IntegrityError` violating the `maintenance_item_retention_tier_valid` CHECK constraint (`src/lms/maintenance/models.py:70-73`) rather than raising a clean `ValueError`.

## Scope

In `src/lms/maintenance/service.py:289-312`:

```python
def set_item_tier(
    session: Session,
    *,
    item: MaintenanceItem,
    retention_tier: str,
) -> MaintenanceItem:
    """Change an item's retention tier and keep its live card in step.

    The tier lives on the item, but scheduling reads it from the card state,
    so changing one without the other would leave the item advertising a
    tier it does not actually use.
    """
    item.retention_tier = retention_tier
    card = get_card_state(
        session,
        learner_id=item.learner_id,
        subject_id=item.id,
        subject_type=SUBJECT_MAINTENANCE_ITEM,
    )
    if card is not None:
        card.retention_tier = retention_tier
    session.flush()
    return item
```

In `src/lms/maintenance/models.py:70-73`:

```python
    __table_args__ = (
        CheckConstraint(
            f"retention_tier IN ({_sql_values(RETENTION_TIERS)})",
            name="maintenance_item_retention_tier_valid",
        ),
    )
```

## Implementation Notes

1. In `src/lms/maintenance/service.py`, ensure `RETENTION_TIERS` is imported from `lms.scheduling.fsrs_engine` or `lms.maintenance.models`.
2. In `set_item_tier`, validate `if retention_tier not in RETENTION_TIERS: raise ValueError(f"unknown retention_tier {retention_tier!r}; expected one of {RETENTION_TIERS}")`.
3. In `tests/maintenance/test_tiers_horizon_budget.py`, add unit test cases verifying that calling `set_item_tier` with an invalid tier raises `ValueError` before modifying session state.

## Tasks

- [ ] In `src/lms/maintenance/service.py`, validate `retention_tier in RETENTION_TIERS` within `set_item_tier`.
- [ ] In `tests/maintenance/test_tiers_horizon_budget.py`, add test cases asserting `ValueError` when `set_item_tier` receives invalid tier strings.

## Acceptance Criteria

- [ ] Running `pytest tests/maintenance/test_tiers_horizon_budget.py` passes cleanly.
- [ ] Calling `set_item_tier(session, item=item, retention_tier="ultra-hot")` raises `ValueError("unknown retention_tier 'ultra-hot'; expected one of ('hot', 'warm', 'cold')")`.
- [ ] Calling `set_item_tier(session, item=item, retention_tier="warm")` successfully updates both item and card state.
- [ ] Deliberately breaking the validation logic causes the targeted tests to fail.

## Non-Goals

- Modifying existing FSRS review intervals or changing the definition of `RETENTION_TIERS`.
- Scaffold-only completion does NOT count: adding placeholder functions without wiring tier validation in `set_item_tier` is a failure of this issue.

