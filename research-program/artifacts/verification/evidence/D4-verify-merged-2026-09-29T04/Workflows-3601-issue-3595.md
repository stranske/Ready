title:	[sync-review] Fix upstream manifest-synced paths blocking stranske/Portable-Alpha-Extension-Model#2318
state:	CLOSED
author:	stranske
labels:	automation, consumer-sync
comments:	44
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	3595
--
## Why

The current Workflows-source keepalive authority protocol can strand a prepared or consumed receipt for up to 24 hours after a failed/cancelled preflight or mark-running attempt. Conversely, the failure reporter currently assumes no agent executed, which could replay a single-use authority generation if liveness recovery is broadened without an execution-evidence guard. The active generated canary stranske/Portable-Alpha-Extension-Model#2318 has two unresolved P1 threads on exact head `09b3ae8f4b98dc1530636b091d51e7c2afaa5fc0`. Related findings on stranske/trip-planner#1869 and stranske/Travel-Plan-Permission#1638 concern the same Workflows source.

## Scope

Repair attempt-bound authority receipt preparation, finalization, release, recovery, and execution-start detection in Workflows source, then regenerate consumer deliveries through Maint 68/71. Preserve single-use semantics: uncertainty about worker execution must never refund authority.

## Non-Goals

- Do not edit, merge, close, or resolve threads on generated consumer PRs directly.
- Do not infer a safe refund from `state.running=false`, absent worker outputs, a generic failed run, or a 24-hour expiry alone.

## Tasks

- [ ] In `scripts/runner_lib/core.py`, make `release_authority_challenge` retryable for the same exact receipt, reservation and owner attempt when the first ledger release failed after completion was recorded; reject stale or replacement receipts.
- [ ] In `templates/consumer-repo/.github/workflows/agents-81-gate-followups.yml` and `.github/workflows/agents-keepalive-loop.yml`, cover cancellation and failure between preparation and finalization, and move finalization after failure-prone mark-running setup while keeping worker execution gated on successful finalization.
- [ ] In `templates/consumer-repo/.github/workflows/agents-keepalive-loop-reporter.yml` and `.github/workflows/agents-keepalive-loop-reporter.yml`, derive `agent_execution_started` from exact originating worker-job evidence with started, definitely-not-started, and unknown states; make absent PR association and API errors retryable rather than asserting false.
- [ ] In `.github/scripts/keepalive_loop.js` and `.github/scripts/keepalive_authority_state.js`, reconcile the exact receipt and owner attempt independently of fresh authority-failure classification and presentation `state.running`, and never reopen a consumed or confirmed receipt when worker execution is started or unknown.
- [ ] Keep `templates/consumer-repo/.github/scripts/` copies byte-aligned, update `.github/sync-manifest.yml` descriptions or entries as appropriate, document recovery ownership in `docs/keepalive/Agents.md` and `docs/keepalive/GoalsAndPlumbing.md`, and add focused regression tests.

## Acceptance Criteria

- [ ] Targeted authority helper, runner-lib, keepalive-loop, and workflow delivery tests pass, including `pytest -q tests/workflows/test_keepalive_authority_delivery.py` and the applicable authority and runner suites.
- [ ] A deliberate regression test fails when execution-start protection is removed and passes restored; tests cover preflight cancellation, mark-running setup failure, release-write failure followed by same-attempt retry, response-lost idempotence, generic reporter failure, worker-started summary failure, and unknown execution evidence.
- [ ] Exact-head source PR review threads and required checks are clear before source merge; Maint 68 canary and Maint 71 reconciliation create current, review-clear, green delivery evidence before promotion.

## Implementation Notes

Originating review evidence: [Portable Alpha release retry](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2318#discussion_r4114202034), [Portable Alpha cancellation](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2318#discussion_r4114202037), [trip-planner mark-running](https://github.com/stranske/trip-planner/pull/1869#discussion_r4114202516), [trip-planner recovery classification](https://github.com/stranske/trip-planner/pull/1869#discussion_r4114202521), [Travel Plan prepared gap](https://github.com/stranske/Travel-Plan-Permission/pull/1638#discussion_r4114199540), [Travel Plan false execution](https://github.com/stranske/Travel-Plan-Permission/pull/1638#discussion_r4114199542). The latter four generated threads were resolved by Maint 71 but their source defects remain. Source owner should use a Workflows PR and normal promotion gates.

