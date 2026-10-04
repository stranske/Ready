title:	Allow fork Gate to report verdict when status token is read-only
state:	CLOSED
author:	stranske
labels:	priority:normal
comments:	4
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	731
--
## Why

This is a verified current break in `.github/workflows/pr-00-gate.yml:220-257`: the `Report Gate commit status` step rethrows every non-rate-limit 403 from `createCommitStatus`. A pull request from a fork receives a read-only workflow token, so Gate can compute a verdict and then fail while trying to publish the `Gate / gate` status. The existing rate-limit classifier also checks only `error.message`, allowing response-message or header-only GitHub rate-limit signals to fall through to any fork-specific fallback.

This child belongs to the fleet campaign in stranske/Workflows#3399 and must preserve repo-local test evidence rather than relying on the source template alone.

## Scope

Teach the repository-owned Gate status-report step to preserve a computed verdict when a fork or deleted-fork token receives a non-rate-limit 403, keep every non-success verdict fail-closed, and distinguish message- and header-based rate limits before applying that fallback.

## Non-Goals

- Do not change branch protection, required-check policy, reusable workflows, or unrelated LMS product behavior.
- Do not treat same-repository permission errors, non-403 errors, or rate limits as fork-token failures.
- Scaffold-only or partial completion does NOT count: a test file that does not execute the embedded script from `.github/workflows/pr-00-gate.yml`, or a fallback that reports success while the computed verdict is `failure`, `error`, or `pending`, fails this issue.

## Tasks

- [ ] Update `.github/workflows/pr-00-gate.yml` in the `Report Gate commit status` step to classify message-, response-message-, `x-ratelimit-remaining`, and `retry-after` rate-limit signals before a fork/deleted-fork read-only-token fallback.
- [ ] Preserve the computed Gate verdict in a warning and job summary for fork/deleted-fork non-rate-limit 403s, and call `core.setFailed` for `failure`, `error`, and `pending` verdicts.
- [ ] Create `tests/test_gate_commit_status_fork_tolerance.py` to extract and execute the production embedded GitHub Script under Node across fork, deleted-fork, same-repository, rate-limit, non-403, non-success, and happy-path cases.

## Acceptance Criteria

- [ ] `uv run pytest tests/test_gate_commit_status_fork_tolerance.py -q --no-cov` executes the workflow's embedded script and passes all focused cases, proving fork/deleted-fork read-only 403s retain verdict evidence while same-repository, rate-limit, and unrelated failures keep their distinct behavior.
- [ ] As deliberate-break evidence, temporarily change only the `readOnlyForkToken` expression in `.github/workflows/pr-00-gate.yml` to `false`; the named focused pytest command with `--no-cov` must fail the fork-specific assertions, with the failing output captured in the PR, then the change must be reverted and the same command must pass.
- [ ] `uv run ruff check tests/test_gate_commit_status_fork_tolerance.py` and `uv run ruff format --check tests/test_gate_commit_status_fork_tolerance.py` both pass, and `python -c "import yaml; yaml.safe_load(open('.github/workflows/pr-00-gate.yml'))"` exits 0.

## Implementation Notes

- Current exact `main` is `2553cbdd585b3984ff5925de1097a660642c0e57`.
- The repository uses the older Gate shape: there is no consolidated-summary comment write before `Report Gate commit status`, so only the commit-status write needs the repo-local guard.
- Preserve the existing rate-limit warning path, but fail closed there when the computed verdict is not `success`.
- Reference implementation/evidence: stranske/trip-planner#1871 and parent campaign stranske/Workflows#3399.

