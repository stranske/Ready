title:	Enforce enum validation for source type, visibility, drift status, and role in source reference helpers
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
number:	669
--
## Why

In `create_source_reference` (`src/lms/sources/repository.py:79-121`) and `update_source_reference` (`src/lms/sources/repository.py:148-182`), input arguments for `source_type`, `source_visibility`, `multi_source_role`, and `drift_status` are assigned to `SourceReference` without Python validation against the domain enums `SOURCE_TYPES`, `SOURCE_VISIBILITIES`, `MULTI_SOURCE_ROLES`, and `DRIFT_STATUSES`. Supplying an invalid enum causes `session.flush()` to raise an unhandled `IntegrityError` from SQLite/Postgres CHECK constraints (`source_type_valid`, `source_visibility_valid`, `drift_status_valid`, `multi_source_role_valid` in `src/lms/sources/models.py:38-55`) instead of raising `ValueError`.

## Scope

In `src/lms/sources/repository.py:79-121`:

```python
def create_source_reference(
    session: Session,
    *,
    source_type: str,
    stable_locator: str,
    actor_id: str,
    passage_range: str | None = None,
    content: str | bytes | None = None,
    content_hash: str | None = None,
    hash_algorithm: str = DEFAULT_HASH_ALGORITHM,
    source_visibility: str = "public",
    multi_source_role: str | None = None,
    source_subsystem: str = "api",
) -> SourceReference:
    """Create a source reference and record the authoring audit event."""
    resolved_hash = content_hash or compute_source_hash_for_reference(
        source_type=source_type,
        stable_locator=stable_locator,
        passage_range=passage_range,
        content=content,
        hash_algorithm=hash_algorithm,
    )
    reference = SourceReference(
        source_type=source_type,
        stable_locator=stable_locator,
        passage_range=passage_range,
        content_hash=resolved_hash,
        hash_algorithm=hash_algorithm,
        source_visibility=source_visibility,
        multi_source_role=multi_source_role,
    )
    session.add(reference)
    session.flush()
```

In `src/lms/sources/models.py:38-55`:

```python
    __table_args__ = (
        CheckConstraint(f"source_type IN ({_sql_values(SOURCE_TYPES)})", name="source_type_valid"),
        CheckConstraint(f"source_visibility IN ({_sql_values(SOURCE_VISIBILITIES)})", name="source_visibility_valid"),
        CheckConstraint(f"drift_status IN ({_sql_values(DRIFT_STATUSES)})", name="drift_status_valid"),
        CheckConstraint(f"multi_source_role IS NULL OR multi_source_role IN ({_sql_values(MULTI_SOURCE_ROLES)})", name="multi_source_role_valid"),
    )
```

## Implementation Notes

1. In `src/lms/sources/repository.py`, import `SOURCE_TYPES`, `SOURCE_VISIBILITIES`, `DRIFT_STATUSES`, and `MULTI_SOURCE_ROLES` from `lms.sources.models`.
2. In `create_source_reference`, validate `source_type in SOURCE_TYPES`, `source_visibility in SOURCE_VISIBILITIES`, and `multi_source_role is None or multi_source_role in MULTI_SOURCE_ROLES` (raising `ValueError` with informative messages).
3. In `update_source_reference`, validate any modified fields in `changes` (`source_type`, `source_visibility`, `drift_status`, `multi_source_role`) against their respective domain tuples before assigning them to the ORM instance and flushing.
4. In `tests/sources/test_source_references.py`, add unit test cases verifying `create_source_reference` and `update_source_reference` raise `ValueError` on invalid enum arguments.

## Tasks

- [ ] In `src/lms/sources/repository.py`, add enum validation for `source_type`, `source_visibility`, `multi_source_role`, and `drift_status` in `create_source_reference` and `update_source_reference`.
- [ ] In `tests/sources/test_source_references.py`, add test cases asserting `ValueError` on invalid source enum values.

## Acceptance Criteria

- [ ] Running `pytest tests/sources/test_source_references.py` passes cleanly.
- [ ] Calling `create_source_reference(session, source_type="invalid", ...)` raises `ValueError` with allowed `SOURCE_TYPES`.
- [ ] Calling `create_source_reference(session, ..., source_visibility="hidden")` raises `ValueError` with allowed `SOURCE_VISIBILITIES`.
- [ ] Calling `update_source_reference(session, reference, ..., drift_status="unknown")` raises `ValueError` with allowed `DRIFT_STATUSES`.
- [ ] Deliberately breaking the validation logic causes the targeted tests to fail.

## Non-Goals

- Changing hashing algorithms or adding new source types in `src/lms/sources/models.py`.
- Scaffold-only completion does NOT count: adding placeholder functions without wiring validation into `create_source_reference` and `update_source_reference` is a failure of this issue.

