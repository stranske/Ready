title:	Enforce finite unit interval bounds for mastery threshold in goal progress calculation
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
number:	671
--
## Why

In `goal_progress_for_learner` (`src/lms/learners/repository.py:308-349`), the `mastery_threshold: float` parameter is used in comparisons (`estimate_by_node.get(node_id, 0.0) >= mastery_threshold`) without validating that it is a finite float in `[0.0, 1.0]`. If `float('nan')` is passed, the comparison `x >= nan` evaluates to `False` for all nodes, silently reporting `mastered_count: 0` and `progress: 0.0` even for fully mastered goals. If non-finite (`inf`, `-inf`) or out-of-range (`-0.5`, `1.5`) values are passed, calculations produce distorted domain metrics without raising an error.

## Scope

In `src/lms/learners/repository.py:308-349`:

```python
def goal_progress_for_learner(
    session: Session,
    *,
    learner_id: str,
    goal_id: str,
    mastery_threshold: float = MASTERY_THRESHOLD,
) -> dict[str, object]:
    """Return goal-relative progress: target nodes covered vs. mastered.

    ``covered`` counts target nodes with any mastery evidence; ``mastered``
    counts target nodes whose current estimate reaches ``mastery_threshold``.
    ``progress`` is the mastered/target ratio (0.0 when the goal has no targets).
    """
    goal = get_learning_goal(session, learner_id=learner_id, goal_id=goal_id)
    if goal is None:
        raise ValueError("learning goal not found for this learner")

    target_node_ids = [node.id for node in goal.target_nodes]
    target_count = len(target_node_ids)

    estimates = mastery_estimates_for_learner(session, learner_id)
    estimate_by_node = {
        str(estimate["knowledge_node_id"]): float(estimate["current_estimate"])
        for estimate in estimates
    }

    covered = sum(1 for node_id in target_node_ids if node_id in estimate_by_node)
    mastered = sum(
        1 for node_id in target_node_ids if estimate_by_node.get(node_id, 0.0) >= mastery_threshold
    )
    progress = mastered / target_count if target_count else 0.0
```

## Implementation Notes

1. In `src/lms/learners/repository.py`, check `if not math.isfinite(mastery_threshold) or not (0.0 <= mastery_threshold <= 1.0): raise ValueError("mastery_threshold must be a finite float between 0.0 and 1.0 (inclusive)")` at the beginning of `goal_progress_for_learner`.
2. In `tests/learners/test_learners.py`, add unit test cases checking `goal_progress_for_learner` with `float('nan')`, `float('inf')`, `float('-inf')`, `-0.1`, and `1.1`, verifying `ValueError` is raised.

## Tasks

- [ ] In `src/lms/learners/repository.py`, add finite unit interval validation for `mastery_threshold` in `goal_progress_for_learner`.
- [ ] In `tests/learners/test_learners.py`, add test cases asserting `ValueError` when `mastery_threshold` is non-finite or outside `[0.0, 1.0]`.

## Acceptance Criteria

- [ ] Running `pytest tests/learners/test_learners.py` passes cleanly.
- [ ] Calling `goal_progress_for_learner(session, learner_id=..., goal_id=..., mastery_threshold=float('nan'))` raises `ValueError("mastery_threshold must be a finite float between 0.0 and 1.0 (inclusive)")`.
- [ ] Calling `goal_progress_for_learner(session, learner_id=..., goal_id=..., mastery_threshold=1.5)` raises `ValueError("mastery_threshold must be a finite float between 0.0 and 1.0 (inclusive)")`.
- [ ] Calling `goal_progress_for_learner(session, learner_id=..., goal_id=..., mastery_threshold=-0.1)` raises `ValueError("mastery_threshold must be a finite float between 0.0 and 1.0 (inclusive)")`.
- [ ] Deliberately breaking the validation logic causes the targeted tests to fail.

## Non-Goals

- Modifying the default `MASTERY_THRESHOLD` constant or changing how knowledge profile estimates are generated.
- Scaffold-only completion does NOT count: adding placeholder checks without validating `mastery_threshold` in `goal_progress_for_learner` is a failure of this issue.

