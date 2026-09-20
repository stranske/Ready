title:	Enforce Python-level validation for confidence rating, support level, and elapsed duration in attempt creation
state:	CLOSED
author:	stranske
labels:	bug, priority:normal
comments:	0
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	667
--
## Why

In `create_attempt` (`src/lms/evidence/repository.py:50-81`), input arguments for `confidence_rating`, `support_level`, and `elapsed_seconds` are passed directly into `Attempt(...)` and flushed to the database without Python-level domain validation. The `Attempt` model (`src/lms/evidence/models.py:44-57`) specifies CHECK constraints enforcing `1 <= confidence_rating <= 5`, `support_level IN SUPPORT_LEVELS`, and `elapsed_seconds >= 0`. When invalid values (such as `confidence_rating=0`, `confidence_rating=6`, `support_level="invalid"`, or `elapsed_seconds=-10`) are passed, `session.flush()` fails with an unhandled database `IntegrityError` from SQLite/Postgres instead of raising a descriptive `ValueError`.

## Scope

In `src/lms/evidence/repository.py:50-81`:

```python
def create_attempt(
    session: Session,
    *,
    learner_id: str,
    prompt_id: str,
    response_text: str,
    feedback: dict[str, Any],
    response_metadata: dict[str, Any] | None = None,
    confidence_rating: int | None = None,
    reference_accessed: bool = False,
    hint_used: bool = False,
    support_level: str = "none",
    elapsed_seconds: int | None = None,
    llm_session_id: str | None = None,
    evidence: dict[str, Any] | None = None,
) -> Attempt:
    """Persist a learner attempt with structured feedback."""
    attempt = Attempt(
        learner_id=learner_id,
        prompt_id=prompt_id,
        response_text=response_text,
        response_metadata=response_metadata,
        confidence_rating=confidence_rating,
        reference_accessed=reference_accessed,
        hint_used=hint_used,
        support_level=support_level,
        elapsed_seconds=elapsed_seconds,
        feedback=feedback,
        llm_session_id=llm_session_id,
    )
    session.add(attempt)
    session.flush()
```

In `src/lms/evidence/models.py:44-57`:

```python
    __table_args__ = (
        CheckConstraint(
            "confidence_rating IS NULL OR (confidence_rating >= 1 AND confidence_rating <= 5)",
            name="confidence_rating_valid",
        ),
        CheckConstraint(
            f"support_level IN ({_sql_values(SUPPORT_LEVELS)})",
            name="support_level_valid",
        ),
        CheckConstraint(
            "elapsed_seconds IS NULL OR elapsed_seconds >= 0",
            name="elapsed_seconds_non_negative",
        ),
    )
```

## Implementation Notes

1. In `src/lms/evidence/repository.py`, import `SUPPORT_LEVELS` from `lms.evidence.models`.
2. In `create_attempt`, validate `confidence_rating` (`if confidence_rating is not None and (confidence_rating < 1 or confidence_rating > 5): raise ValueError("confidence_rating must be between 1 and 5")`).
3. In `create_attempt`, validate `support_level` (`if support_level not in SUPPORT_LEVELS: raise ValueError(f"unknown support_level {support_level!r}; expected one of {SUPPORT_LEVELS}")`).
4. In `create_attempt`, validate `elapsed_seconds` (`if elapsed_seconds is not None and elapsed_seconds < 0: raise ValueError("elapsed_seconds must be non-negative")`).
5. In `tests/evidence/test_attempts.py`, add unit test cases testing `create_attempt` with invalid confidence ratings (`0`, `6`), invalid support level strings, and negative elapsed durations.

## Tasks

- [ ] In `src/lms/evidence/repository.py`, add validation for `confidence_rating`, `support_level`, and `elapsed_seconds` in `create_attempt`.
- [ ] In `tests/evidence/test_attempts.py`, add test cases asserting `create_attempt` raises `ValueError` on invalid parameter inputs.

## Acceptance Criteria

- [ ] Running `pytest tests/evidence/test_attempts.py` passes with all validation test cases.
- [ ] Calling `create_attempt(session, ..., confidence_rating=6)` raises `ValueError("confidence_rating must be between 1 and 5")`.
- [ ] Calling `create_attempt(session, ..., support_level="invalid")` raises `ValueError` indicating valid choices from `SUPPORT_LEVELS`.
- [ ] Calling `create_attempt(session, ..., elapsed_seconds=-5)` raises `ValueError("elapsed_seconds must be non-negative")`.
- [ ] Deliberately breaking the validation logic causes the targeted tests to fail.

## Non-Goals

- Modifying the existing schema or constraint definitions of `Attempt` in `src/lms/evidence/models.py`.
- Scaffold-only completion does NOT count: adding placeholder validation or stubs without wiring parameter checks in `create_attempt` and adding unit test coverage is a failure of this issue.

