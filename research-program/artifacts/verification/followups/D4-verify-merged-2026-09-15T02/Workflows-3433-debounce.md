# Complete debounce productivity and workflow acceptance for issue #3433

Status: research-only draft, not filed. Original https://github.com/stranske/Workflows/issues/3433 is open; reconcile there before creating a duplicate. The prior #3435 PR is closed unmerged. Scope is the remaining original requirements, not reversing the successful cooldown fix.

## Why

Merged #3436 and #3440 provide same-head retries and a time-drained cooldown, but do not complete source #3433. At merge `a5908e2` (full SHA in the verification report), productivity remains a boolean head comparison, not commit-or-task-delta measurement. Refusals do not report the requested prior commit and task counts. The named workflow-level acceptance test is absent. A task-only completion can therefore be treated as zero work and retried, and operators cannot see both measures explaining the refusal.

## Scope

`.github/workflows/agents-keepalive-loop.yml`, its consumer `templates/consumer-repo/.github/workflows/agents-81-gate-followups.yml`, `scripts/runner_lib/core.py`, and `tests/workflows/test_keepalive_dispatch_debounce.py`.

## Tasks

- Measure commits and completed-task delta, preserve both values, and define productive as the original issue's commit-or-task-delta rule.
- Include both numeric quantities and the concrete drain condition in refusal output.
- Keep the already-merged time-based cooldown; do not restore the head-commit-only exhaustion refusal.
- Add the named workflow-derived test and retain literal execution/break/restoration evidence.

## Acceptance Criteria

- A completed record with zero commits and zero task delta permits the next same-head dispatch within the allowance.
- A task-only productive completion and a commit-producing completion follow the intended duplicate suppression rule; refusals expose both numbers.
- Exhausted zero-output retries resume after the cooldown without a new commit.
- `python -m pytest tests/workflows/test_keepalive_dispatch_debounce.py -q` passes. Temporarily making all completed records terminal must fail the zero-output regression; restore and pass.

## Evidence

- https://github.com/stranske/Workflows/pull/3436
- https://github.com/stranske/Workflows/pull/3440
- Exact merge-linked line references and 60 passing existing runner tests are in the parent verification report.

Full relevant merge SHA: `a5908e2624eefd374d7582bbd600186a51ab54fe`.
