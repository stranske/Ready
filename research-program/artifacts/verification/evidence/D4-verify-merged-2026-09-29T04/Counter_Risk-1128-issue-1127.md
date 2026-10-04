title:	Gate: tolerate fork read-only 403 on commit status (Workflows#3399 fleet sweep)
state:	CLOSED
author:	stranske
labels:	priority:normal
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
number:	1127
--
## Why

Fork pull requests run `pr-00-gate.yml` with a read-only `GITHUB_TOKEN`, so `Report Gate commit status` cannot write `Gate / gate` and the job fails after computing a passing verdict. Parent fleet tracker: stranske/Workflows#3399.

## Scope

Port the fork read-only 403 tolerance into `.github/workflows/pr-00-gate.yml` for `stranske/Counter_Risk` and add a workflow-script-bound regression test.

## Non-Goals

- No `pull_request_target`, permission, or token-scope changes.
- No widening tolerance beyond fork heads (same-repo 403 must still fail).

## Tasks

- [ ] Add `isForkPullRequest` handling to the `Report Gate commit status` catch block.
- [ ] Add `tests/test_gate_commit_status_fork_tolerance.py` executing the extracted step script under Node.

## Acceptance Criteria

- [ ] `python3 -m pytest tests/test_gate_commit_status_fork_tolerance.py -q` passes on the PR branch (7 tests: fork 403 tolerated, same-repo 403 fails, rate-limit path unchanged, non-403 fails, happy path silent).
- [ ] Reverting only `.github/workflows/pr-00-gate.yml` to pre-fix content makes the same pytest command fail on `test_fork_read_only_403_does_not_fail_the_gate` (and related fork cases); restoring the fix makes all 7 pass again.
- [ ] Remote scan: `gh api repos/stranske/Counter_Risk/contents/.github/workflows/pr-00-gate.yml` decoded content contains `isForkPullRequest`.

## Implementation Notes

Reference: stranske/Travel-Plan-Permission merged gate fix and stranske/Workflows#3398.

