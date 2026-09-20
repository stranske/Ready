title:	Validate scores, difficulty estimates, durations, and categorical enums before evidence record persistence
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
number:	668
--
## Why

In `create_evidence_record` (`src/lms/evidence/repository.py:146-224`), input values for `evidence_kind`, `demand_level`, `knowledge_type`, `scorer_type`, `scoring_method`, `confidence_rating`, `support_level`, `raw_score`, `max_score`, `item_difficulty_estimate`, `time_since_last_attempt_seconds`, and `response_time_seconds` are passed directly into `EvidenceRecord` without Python domain validation. The `EvidenceRecord` model (`src/lms/evidence/models.py:95-149`) defines database CHECK constraints for each of these fields (`evidence_kind_valid`, `demand_level_valid`, `knowledge_type_valid`, `scorer_type_valid`, `scoring_method_valid`, `confidence_rating_valid`, `support_level_valid`, `raw_score_non_negative`, `max_score_positive`, `item_difficulty_unit_interval`, `time_since_last_attempt_non_negative`, and `response_time_non_negative`). Invalid inputs crash at `session.flush()` with unhandled `IntegrityError` exceptions instead of raising `ValueError`.

## Scope

In `src/lms/evidence/repository.py:146-224`:

```python
def create_evidence_record(
    session: Session,
    *,
    learner_id: str,
    knowledge_node_id: str,
    attempt_id: str | None = None,
    prompt_id: str | None = None,
    prompt_version_id: str | None = None,
    timestamp: datetime | None = None,
    evidence_kind: str = "observed",
    demand_level: str | None = None,
    knowledge_type: str | None = None,
    time_since_last_attempt_seconds: int | None = None,
    response_time_seconds: int | None = None,
    correctness: bool | None = None,
    confidence_rating: int | None = None,
    reference_accessed: bool = False,
    hint_used: bool = False,
    support_level: str = "none",
    retrieval_demand: str | None = None,
    transfer_distance: str | None = None,
    source_match_quality: str | None = None,
    scorer_type: str | None = None,
    scorer_id: str | None = None,
    scorer_version: str | None = None,
    scoring_method: str | None = None,
    scorer_metadata: dict[str, Any] | None = None,
    raw_score: float | None = None,
    normalized_score: float | None = None,
    max_score: float | None = None,
    partial_credit_dimensions: dict[str, Any] | None = None,
    item_difficulty_estimate: float | None = None,
    attempt_context: dict[str, Any] | None = None,
    validity_scope: str | None = None,
    answer_artifact_ref: str | None = None,
) -> EvidenceRecord:
```

In `src/lms/evidence/models.py:95-149`:

```python
    __table_args__ = (
        CheckConstraint(f"evidence_kind IN ({_sql_values(EVIDENCE_KINDS)})", name="evidence_kind_valid"),
        CheckConstraint(f"demand_level IS NULL OR demand_level IN ({_sql_values(DEMAND_LEVELS)})", name="demand_level_valid"),
        CheckConstraint(f"knowledge_type IS NULL OR knowledge_type IN ({_sql_values(KNOWLEDGE_TYPES)})", name="knowledge_type_valid"),
        CheckConstraint("time_since_last_attempt_seconds IS NULL OR time_since_last_attempt_seconds >= 0", name="time_since_last_attempt_non_negative"),
        CheckConstraint("response_time_seconds IS NULL OR response_time_seconds >= 0", name="response_time_non_negative"),
        CheckConstraint("confidence_rating IS NULL OR (confidence_rating >= 1 AND confidence_rating <= 5)", name="confidence_rating_valid"),
        CheckConstraint(f"support_level IN ({_sql_values(SUPPORT_LEVELS)})", name="support_level_valid"),
        CheckConstraint("raw_score IS NULL OR raw_score >= 0", name="raw_score_non_negative"),
        CheckConstraint("max_score IS NULL OR max_score > 0", name="max_score_positive"),
        CheckConstraint("item_difficulty_estimate IS NULL OR (item_difficulty_estimate >= 0.0 AND item_difficulty_estimate <= 1.0)", name="item_difficulty_unit_interval"),
        CheckConstraint(f"scorer_type IS NULL OR scorer_type IN ({_sql_values(SCORER_TYPES)})", name="scorer_type_valid"),
        CheckConstraint(f"scoring_method IS NULL OR scoring_method IN ({_sql_values(SCORING_METHODS)})", name="scoring_method_valid"),
    )
```

## Implementation Notes

1. In `src/lms/evidence/repository.py`, import `DEMAND_LEVELS`, `EVIDENCE_KINDS`, `SCORER_TYPES`, `SCORING_METHODS`, and `SUPPORT_LEVELS` from `lms.evidence.models`, and `KNOWLEDGE_TYPES` from `lms.graphs.models`.
2. In `create_evidence_record`, validate:
   - `evidence_kind in EVIDENCE_KINDS` (raise `ValueError`)
   - `demand_level is None or demand_level in DEMAND_LEVELS` (raise `ValueError`)
   - `knowledge_type is None or knowledge_type in KNOWLEDGE_TYPES` (raise `ValueError`)
   - `scorer_type is None or scorer_type in SCORER_TYPES` (raise `ValueError`)
   - `scoring_method is None or scoring_method in SCORING_METHODS` (raise `ValueError`)
   - `support_level in SUPPORT_LEVELS` (raise `ValueError`)
   - `confidence_rating is None or (1 <= confidence_rating <= 5)` (raise `ValueError`)
   - `raw_score is None or (math.isfinite(raw_score) and raw_score >= 0)` (raise `ValueError`)
   - `max_score is None or (math.isfinite(max_score) and max_score > 0)` (raise `ValueError`)
   - `item_difficulty_estimate is None or (math.isfinite(item_difficulty_estimate) and 0.0 <= item_difficulty_estimate <= 1.0)` (raise `ValueError`)
   - `time_since_last_attempt_seconds is None or time_since_last_attempt_seconds >= 0` (raise `ValueError`)
   - `response_time_seconds is None or response_time_seconds >= 0` (raise `ValueError`)
3. In `tests/evidence/test_evidence_records.py`, add unit tests asserting `ValueError` for out-of-range bounds, non-finite floats, and invalid categorical strings.

## Tasks

- [ ] In `src/lms/evidence/repository.py`, add domain validation for enums, scores, difficulty estimates, and duration fields in `create_evidence_record`.
- [ ] In `tests/evidence/test_evidence_records.py`, add test cases verifying `create_evidence_record` raises `ValueError` for invalid parameters.

## Acceptance Criteria

- [ ] Running `pytest tests/evidence/test_evidence_records.py` passes cleanly.
- [ ] Calling `create_evidence_record(session, ..., raw_score=-1.0)` raises `ValueError("raw_score must be non-negative")`.
- [ ] Calling `create_evidence_record(session, ..., max_score=0.0)` raises `ValueError("max_score must be a positive number")`.
- [ ] Calling `create_evidence_record(session, ..., evidence_kind="invalid")` raises `ValueError` indicating valid choices from `EVIDENCE_KINDS`.
- [ ] Calling `create_evidence_record(session, ..., item_difficulty_estimate=1.5)` raises `ValueError("item_difficulty_estimate must be between 0.0 and 1.0")`.
- [ ] Deliberately breaking the validation logic causes the targeted tests to fail.

## Non-Goals

- Modifying the underlying database migration or table schema in `src/lms/evidence/models.py`.
- Scaffold-only completion does NOT count: adding placeholder checks without enforcing validation in `create_evidence_record` and adding tests is a failure of this issue.

