title:	Gate: tolerate fork read-only 403 on commit status (Workflows#3399 fleet sweep)
state:	CLOSED
author:	stranske
labels:	priority:normal
comments:	8
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	601
--
## Why

Ready's repository-owned Gate catches commit-status failures in `.github/workflows/pr-00-gate.yml`, but a fork or deleted-fork pull request receives a read-only token and cannot call `repos.createCommitStatus`. PR #600 attempted the fleet repair tracked by `stranske/Workflows#3399`, but its empty issue body stopped keepalive, its non-registry branch bypasses the numbered agent contract, and exact-head review/CI found that non-success fork verdicts could leave a passing job and that the new YAML-parsing test dependency was undeclared.

## Scope

Deliver the Ready child of `stranske/Workflows#3399` on a numbered registry branch. Preserve computed success/failure verdicts for fork read-only 403s, fail closed for every non-success verdict when no status can be published, preserve all rate-limit and unrelated-error behavior, declare the test dependency, and exercise the production embedded script.

## Non-Goals

- Do not change workflow permissions, use `pull_request_target`, or claim that a missing protected `Gate / gate` context is solved; trusted exact-head publication remains `stranske/Workflows#3605`.
- Do not swallow same-repository permission failures, primary/secondary rate limits, abuse limits, or non-403 errors.
- Do not alter shared agent, keepalive, or verifier workflows.
- Scaffold-only completion does NOT count: a test that does not execute the real `.github/workflows/pr-00-gate.yml` script, omits rate-limit response signals, or permits a non-success verdict to leave a passing job fails this issue.

## Tasks

- [ ] Update `.github/workflows/pr-00-gate.yml` so fork/deleted-fork non-rate-limit 403s preserve the computed verdict while every non-success verdict still fails the Gate job.
- [ ] Update `tests/test_gate_commit_status_fork_tolerance.py` to execute the production embedded script and independently cover response-message, `x-ratelimit-remaining`, and `retry-after` rate-limit signals.
- [ ] Add PyYAML to `pyproject.toml` test/development dependencies and regenerate `requirements.lock` with the repository's dependency tooling.
- [ ] Rehome PR #600 to `codex/issue-601-fork-gate-readonly-token`, open a ready replacement PR with `Closes #601` and `Supersedes #600`, then close #600 with durable linkage.

## Acceptance Criteria

- [ ] `python -m pytest --no-cov tests/test_gate_commit_status_fork_tolerance.py -q` executes the actual workflow script and passes focused fork, deleted-fork, same-repository, rate-limit, non-403, success, and non-success-verdict cases.
- [ ] Disabling only the fork read-only fallback makes the named pytest gate fail; restoration passes, with the red/green counts captured in the replacement PR.
- [ ] A fork-token 403 with Gate state `error`, `failure`, or `pending` preserves the verdict evidence and leaves a failing job, while state `success` completes without failing the job.
- [ ] The repository's exact dependency consistency command exits 0 after `pyproject.toml` and `requirements.lock` include PyYAML, and YAML parsing plus `git diff --check origin/main...HEAD` pass.

## Implementation Notes

- Parent campaign: `stranske/Workflows#3399`.
- Review evidence: `stranske/Ready#600` active threads `discussion_r4117750387`, `discussion_r4117750390`, and `discussion_r4117750396`.
- This repository has the older status-only Gate shape; no earlier consolidated-summary comment write needs adjustment.

