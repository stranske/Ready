title:	fix(runner): prevent fallback-only dispatch reservations
state:	CLOSED
author:	stranske
labels:	agents:formatted
comments:	10
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	3470
--
## Why

Consumer sync campaign review threads (Doc-Lineage#33, Manager-Database#1684, learning-management-system#678) identified that automatic runner dispatch could reserve only in fallback storage during a primary outage while `record_completion` requires an authoritative primary reservation. Such runs cannot reach a recorded terminal state.

## Scope

Verify the merged `scripts/runner_lib` repair on `main` (PR #3471, head `190eafed`). Do not edit generated consumer PRs.

## Non-Goals

- Re-implementing the runner fix (already merged).
- Patching consumer sync PRs directly.

## Tasks

- [ ] In `scripts/runner_lib/core.py`, confirm `should_dispatch` and `FallbackRunnerStorage.write_record` refuse to start a dispatch when primary reservation read/write fails (no fallback-only pending record).
- [ ] In `tests/scripts/test_runner_lib.py`, confirm `test_auto_dispatch_requires_primary_storage`, `test_auto_dispatch_checks_real_legacy_backend_access`, and `test_auto_completion_requires_authoritative_reservation` cover outage/recovery and reused-adapter paths.
- [ ] In `docs/keepalive/GoalsAndPlumbing.md`, confirm the authoritative-reservation contract paragraph documents primary-required dispatch and completion behavior.

## Acceptance Criteria

- [ ] `pytest tests/scripts/test_runner_lib.py -q -k "auto_dispatch_requires_primary or auto_dispatch_checks_real_legacy or auto_completion_requires_authoritative"` passes on current `main`.
- [ ] **Deliberate-break gate:** revert the primary-storage refusal in `should_dispatch` → `test_auto_dispatch_requires_primary_storage` **must FAIL** → restore.

## Implementation Notes

Merged via PR #3471 at 2026-09-19T15:44:22Z. Source paths verified in clone at `scripts/runner_lib/core.py`, `tests/scripts/test_runner_lib.py`, `docs/keepalive/GoalsAndPlumbing.md`.
