title:	Validate finite bounds and relative ordering for feedback and remediation thresholds in rubric scoring
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
number:	673
--
## Why

In `score_attempt_with_rubric` (`src/lms/feedback/scoring.py:77-165`), `feedback_threshold: float = 0.85` and `remediation_threshold: float = 0.5` are consumed in boolean checks (`normalized_score >= feedback_threshold`, `normalized_score < feedback_threshold`, `normalized_score < remediation_threshold`) without validating that they are finite numbers in `[0.0, 1.0]` and that `remediation_threshold <= feedback_threshold`. Passing `float('nan')` causes `normalized_score >= nan` and `normalized_score < nan` to both evaluate to `False`, falsely marking a 100% attempt as failed (`correctness=False`) while simultaneously suppressing feedback creation.

## Scope

In `src/lms/feedback/scoring.py:77-165`:

```python
def score_attempt_with_rubric(
    session: Session,
    *,
    attempt_id: str,
    rubric_id: str,
    criterion_scores: list[dict[str, Any]],
    scorer_type: str,
    scorer_id: str | None = None,
    scorer_version: str | None = None,
    score_metadata: dict[str, Any] | None = None,
    feedback_threshold: float = 0.85,
    remediation_threshold: float = 0.5,
) -> RubricScore:
```

```python
    evidence = create_evidence_record(
        session,
        learner_id=attempt.learner_id,
        knowledge_node_id=knowledge_node_id,
        attempt_id=attempt.id,
        prompt_id=attempt.prompt_id,
        correctness=normalized_score >= feedback_threshold,
        raw_score=raw_score,
        normalized_score=normalized_score,
        max_score=max_score,
```

```python
    feedback_record_id: str | None = None
    if normalized_score < feedback_threshold:
        feedback_record = create_feedback_record(
            session,
            learner_id=attempt.learner_id,
            attempt_id=attempt.id,
            prompt_id=attempt.prompt_id,
            evidence_record_id=evidence.id,
            feedback_level="remediation" if normalized_score < remediation_threshold else "review",
```

## Implementation Notes

1. In `src/lms/feedback/scoring.py`, validate in `score_attempt_with_rubric` that `math.isfinite(feedback_threshold)` and `0.0 <= feedback_threshold <= 1.0` (raising `InvalidRubricScoringError("feedback_threshold must be a finite number between 0.0 and 1.0")`).
2. Validate that `math.isfinite(remediation_threshold)` and `0.0 <= remediation_threshold <= 1.0` (raising `InvalidRubricScoringError("remediation_threshold must be a finite number between 0.0 and 1.0")`).
3. Validate that `remediation_threshold <= feedback_threshold` (raising `InvalidRubricScoringError("remediation_threshold cannot exceed feedback_threshold")`).
4. In `tests/feedback/test_rubric_scoring.py`, add test cases asserting `InvalidRubricScoringError` when non-finite, out-of-range, or inverted thresholds are supplied to `score_attempt_with_rubric`.

## Tasks

- [ ] In `src/lms/feedback/scoring.py`, add finite range and threshold ordering validation for `feedback_threshold` and `remediation_threshold` in `score_attempt_with_rubric`.
- [ ] In `tests/feedback/test_rubric_scoring.py`, add test cases asserting `InvalidRubricScoringError` on invalid or out-of-order scoring thresholds.

## Acceptance Criteria

- [ ] Running `pytest tests/feedback/test_rubric_scoring.py` passes cleanly.
- [ ] Calling `score_attempt_with_rubric(session, ..., feedback_threshold=float('nan'))` raises `InvalidRubricScoringError("feedback_threshold must be a finite number between 0.0 and 1.0")`.
- [ ] Calling `score_attempt_with_rubric(session, ..., feedback_threshold=0.4, remediation_threshold=0.8)` raises `InvalidRubricScoringError("remediation_threshold cannot exceed feedback_threshold")`.
- [ ] Deliberately breaking the validation logic causes the targeted tests to fail.

## Non-Goals

- Altering the default 0.85 and 0.5 threshold values or modifying rubric criterion score normalization rules.
- Scaffold-only completion does NOT count: adding placeholder validation without enforcing threshold bounds in `score_attempt_with_rubric` is a failure of this issue.

