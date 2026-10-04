title:	[P1] Fork PR Gate should preserve verdict when commit-status token is read-only
state:	CLOSED
author:	stranske
labels:	priority:normal, repo-review-approved
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
number:	6067
--
## Why

This is the Trend_Model_Project child of the fleet campaign in
`stranske/Workflows#3399`. The repository-owned Gate calls
`github.rest.repos.createCommitStatus` in
`.github/workflows/pr-00-gate.yml:382-391`. Its catch at
`.github/workflows/pr-00-gate.yml:393-401` tolerates only a rate-limit 403 via
`isRateLimitError` and rethrows every other 403. A pull request opened from a
fork receives a read-only `GITHUB_TOKEN`, so `Resource not accessible by
integration` currently fails the summary job after the Gate has already
computed its verdict. This is a verified current break: the 2026-09-27 remote
fleet scan found that Trend_Model_Project still lacks `isForkPullRequest`, while
the source guard is already merged in `stranske/Workflows#3398`.

## Scope

Align this repository-owned, `create_only` Gate copy with the merged Workflows
fork-token guard while preserving Trend_Model_Project's existing
`isRateLimitError` name and its repo-specific jobs. This Gate shape has the
commit-status write but no preceding consolidated-summary-comment write, so the
child changes only the status step and adds one focused executable regression
test.

## Non-Goals

- Do NOT change `pull_request_target`, workflow permissions, token loading,
  branch protection, reusable CI wiring, or Trend_Model_Project's Gate policy.
- Do NOT rename `isRateLimitError` or broaden tolerance to every 403; a
  same-repository 403 must remain a hard failure.
- Do NOT alter the existing rate-limit path or claim that a missing
  `Gate / gate` status becomes satisfiable under branch protection.
- Do NOT edit Workflows or another consumer in this child; Workflows #3399
  retains the remaining fleet campaign.
- Scaffold-only completion does NOT count: adding a predicate without executing
  the actual extracted GitHub Script, or adding a test that does not prove both
  fork and same-repository behavior, fails this issue.

## Tasks

- [ ] In `.github/workflows/pr-00-gate.yml:369-401`, add `isForkPullRequest`
  from the pull request head/base repository names and
  tolerate only a non-rate-limit 403 on that fork by logging the computed Gate
  verdict and appending it to `core.summary`.
- [ ] Create `tests/workflows/test_gate_commit_status_fork_tolerance.py` to extract the
  real `Report Gate commit status` JavaScript from
  `.github/workflows/pr-00-gate.yml` and execute it under Node with stubbed
  `github`, `context`, and `core` objects.
- [ ] In `tests/workflows/test_gate_commit_status_fork_tolerance.py`, cover fork
  read-only 403, same-repository 403, rate-limit 403, non-403 failure, and
  successful status-write behavior, including warning and job-summary verdict
  evidence.
- [ ] Run `pytest tests/workflows/test_gate_commit_status_fork_tolerance.py -q`
  through the deliberate-break loop in the Acceptance Criteria, capture literal
  failing and passing output in the PR body, and restore the exact Gate
  implementation before requesting review.

## Acceptance Criteria

- [ ] `pytest tests/workflows/test_gate_commit_status_fork_tolerance.py -q`
  exits 0 and executes the workflow step's extracted JavaScript under Node; the
  literal output is captured in the PR body.
- [ ] The named test file proves a fork 403 does not throw and writes the
  computed `success` verdict, description, and head SHA to `core.summary`, while
  a same-repository 403 and a non-403 error still throw.
- [ ] The named test file proves the existing rate-limit 403 remains tolerated
  through its own warning path and a successful status write remains silent.
- [ ] **Deliberate-break gate:** temporarily remove only the
  `readOnlyForkToken` branch from `.github/workflows/pr-00-gate.yml`; then
  `pytest tests/workflows/test_gate_commit_status_fork_tolerance.py::test_fork_read_only_403_does_not_fail_the_gate -q`
  must fail because the 403 is rethrown. Restore that branch, rerun the same
  test, and capture both literal outputs in the PR body.
- [ ] A post-change remote read of
  `.github/workflows/pr-00-gate.yml` on the PR head contains
  `isForkPullRequest`; the PR body records base SHA
  `6c972f3c14539fca314dfe5eb2ba91fc30a948d0` and the exact pushed head SHA.

## Implementation Notes

- Parent campaign: `stranske/Workflows#3399`; merged source reference:
  `stranske/Workflows#3398` and
  `tests/workflows/test_gate_commit_status_fork_tolerance.py` on Workflows
  `main`.
- Verified base: Trend_Model_Project `origin/main` at
  `6c972f3c14539fca314dfe5eb2ba91fc30a948d0`; the affected step is
  `.github/workflows/pr-00-gate.yml:358-402`.
- Confirmed reproduction command from the repo root after implementation:
  `python3 -m pytest tests/workflows/test_gate_commit_status_fork_tolerance.py -q`.
- Keep the branch and PR limited to this repository. The PR closes only this
  child issue and references Workflows #3399 without closing it.

