# [P1] Reject infinite exposure limits before evaluation

## Why

`src/counter_risk/limits_config.py:23` checks only that the limit is positive. YAML positive infinity therefore passes `load_limits_config`, and `src/counter_risk/compute/limits.py:277` subtracts it and drops the negative result as not breached. The normal pipeline consumes this model at `src/counter_risk/pipeline/run.py:2396`. Lead-seat matched controls loaded real temporary YAML: a 100 exposure against 50 produced one fail-severity breach; the same exposure against YAML infinity was accepted and produced zero. This is an invalid-config acceptance defect; no actual owner policy using infinity was observed. Existing enabled=false already represents a staged limit.

## Scope

Finite validation of LimitEntry.limit_value for all limit kinds, without changing finite threshold semantics.

## Non-Goals

No new financial model, source-format rewrite or upstream workflow change. Scaffold-only or partial completion does NOT count as done; the behavior and test gates must be delivered.

## Tasks

- [ ] In `src/counter_risk/limits_config.py`, require finite positive `limit_value` and retain the explicit enabled flag for disabled policy entries.
- [ ] Extend `tests/test_limits_config.py` to reject YAML and direct-model positive infinity, negative infinity and NaN with an actionable validation error.
- [ ] Extend `tests/compute/test_limits.py` to preserve a finite breached-limit control and prove non-finite policy cannot reach evaluation.

## Acceptance Criteria

- [ ] `python -m pytest tests/test_limits_config.py tests/compute/test_limits.py -q` passes; the new YAML regression rejects positive infinity before check_limits runs.
- [ ] A finite 50 absolute limit against 100 still produces one breach, while explicitly disabled finite limits retain their existing behavior.
- [ ] Deliberate-break gate: remove finite validation from `LimitEntry` in `src/counter_risk/limits_config.py`; the new positive-infinity YAML test must fail; restore the validator and rerun.

## Implementation Notes

Closed #1004 hardens WorkflowConfig cash bounds, not LimitEntry policy values. This is a distinct consumer with a separately reproduced trigger.
