title:	Allow fork Gate to report verdict when status token is read-only
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
number:	1733
--
## Why

`Manager-Database` owns a create-only Gate workflow. Its current `Report Gate commit status` catch at `.github/workflows/pr-00-gate.yml:190` recognizes only message-based API rate limits; `.github/workflows/pr-00-gate.yml:194-196` rethrows every other 403. This is a verified current break for pull requests from forks: GitHub gives fork workflows a read-only token, `createCommitStatus` returns `403 Resource not accessible by integration`, and the Gate job fails after computing its verdict instead of reporting it. Parent fleet campaign: stranske/Workflows#3399.

## Scope

Update this repository's older, status-only Gate shape so a non-rate-limit 403 from a fork or deleted-fork status write preserves the computed verdict in a warning and job summary. Add a focused test that extracts and executes the actual embedded GitHub Script under Node.

## Non-Goals

- Do not change workflow permissions, use `pull_request_target`, alter branch protection, or claim that a missing `Gate / gate` status becomes satisfiable for fork PRs.
- Do not swallow same-repository permission failures or non-403 errors, and do not route message-, primary-header-, or secondary-header-based rate-limit 403s through the fork fallback.
- Do not change the separate upstream trusted-status design tracked by stranske/Workflows#3605.
- Scaffold-only or partial completion does not count: a test file that does not execute the real `.github/workflows/pr-00-gate.yml` script, or a handler that accepts every 403, fails this issue.

## Tasks

- [ ] In `.github/workflows/pr-00-gate.yml`, distinguish fork/deleted-fork read-only 403 failures from same-repository permission failures after preserving the existing rate-limit path.
- [ ] In `.github/workflows/pr-00-gate.yml`, write the computed head SHA, Gate state, and description to `core.summary` when the fork token cannot create the status.
- [ ] Create `tests/test_gate_commit_status_fork_tolerance.py` to extract `Report Gate commit status` from the workflow and execute fork, deleted-fork, same-repository, rate-limit, non-403, and successful-write cases under Node.

## Acceptance Criteria

- [ ] `pytest -q tests/test_gate_commit_status_fork_tolerance.py` exits 0 with eight passing cases and proves fork/deleted-fork read-only 403s preserve both success and failure verdicts while same-repository 403 and non-403 failures remain loud.
- [ ] Deliberately remove only the fork/deleted-fork fallback from `.github/workflows/pr-00-gate.yml`; the named pytest command must fail its fork-verdict assertions. Restore the exact implementation and capture both red and green outputs in the PR body.
- [ ] `python -c "import yaml; yaml.safe_load(open('.github/workflows/pr-00-gate.yml'))"` exits 0, and `git diff --check` reports no whitespace errors.

## Implementation Notes

This repo has the older Gate shape: there is no pre-status comment-upsert step in the `summary` job, so only `Report Gate commit status` needs the narrow fallback. Use the merged consumer implementation in `stranske/Travel-Plan-Permission#1636` as the behavioral reference, while keeping `context.repo.repo` and local test paths specific to `Manager-Database`.

