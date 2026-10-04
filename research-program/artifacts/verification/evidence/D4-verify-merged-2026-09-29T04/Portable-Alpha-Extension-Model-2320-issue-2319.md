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
number:	2319
--
## Why

`stranske/Workflows#3399` tracks a fleet defect in repository-owned Gate copies. In current `main`, `.github/workflows/pr-00-gate.yml:283-309` calls `github.rest.repos.createCommitStatus` without a `try`/`catch`. A pull request from a fork receives a read-only token, so a successful computed Gate verdict is replaced by `403 Resource not accessible by integration` and never appears in the job summary. This is a verified current break, not latent cleanup.

## Scope

Add the narrow fork/read-only-token fallback to Portable-Alpha-Extension-Model's repository-owned Gate and add a focused test that executes the real embedded GitHub Script under Node.

## Non-Goals

- Do not change workflow permissions, switch to `pull_request_target`, expose a write credential to fork code, or claim this makes a protected required context satisfiable; `stranske/Workflows#3605` owns trusted exact-head publication.
- Do not suppress same-repository 403s, non-403 errors, or the existing rate-limit failure path.
- Do not change the create-only ownership policy for `.github/workflows/pr-00-gate.yml`.
- Scaffold-only completion does not count: adding a test file that does not execute the extracted `Report Gate commit status` script, or adding a catch without the deliberate-break proof, fails this issue.

## Tasks

- [ ] In `.github/workflows/pr-00-gate.yml`, wrap the `Report Gate commit status` call in a narrow `try`/`catch` that identifies `pull_request.head.repo.full_name != pull_request.base.repo.full_name`, tolerates only a non-rate-limit 403 for that fork, warns with the computed verdict, and writes the verdict to `core.summary`.
- [ ] Create `tests/workflows/test_gate_commit_status_fork_tolerance.py` to extract the real `Report Gate commit status` script from `.github/workflows/pr-00-gate.yml`, execute it under Node, and cover fork 403, same-repo 403, rate-limit 403, non-403, and successful-write cases.
- [ ] Deliberately remove only the fork-token fallback from `.github/workflows/pr-00-gate.yml`, run `python3 -m pytest tests/workflows/test_gate_commit_status_fork_tolerance.py -q`, capture the expected failure, restore the workflow exactly, and record the RED/GREEN output in the pull request.

## Acceptance Criteria

- [ ] `python3 -m pytest tests/workflows/test_gate_commit_status_fork_tolerance.py -q` passes and proves that a fork's non-rate-limit 403 does not fail the Gate while same-repo 403s and non-403 errors still raise, the rate-limit branch remains distinct, and a successful status write stays silent.
- [ ] With only the fork-token fallback removed from `.github/workflows/pr-00-gate.yml`, the named pytest command fails at the fork-read-only assertion; after exact restoration, the same command passes, with both literal outputs captured in the pull request.
- [ ] The restored workflow's warning and job summary include the computed `state`, `description`, and head SHA when the fork token is read-only; evidence is captured by the focused test and the pull-request validation block.

## Implementation Notes

- Parent campaign: `stranske/Workflows#3399`.
- Reference behavior: `stranske/Workflows#3398` and `tests/workflows/test_gate_commit_status_fork_tolerance.py` in Workflows.
- This repo has the older/simpler Gate shape: there is no preceding consolidated-summary comment write to patch, and the commit-status call currently has no catch at all.

