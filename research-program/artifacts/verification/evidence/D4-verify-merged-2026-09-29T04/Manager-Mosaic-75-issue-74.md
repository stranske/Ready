title:	Allow fork Gate to report verdict when status token is read-only
state:	CLOSED
author:	stranske
labels:	priority:normal
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
number:	74
--
## Why

This is a verified current break in the fork-contribution path. In
`.github/workflows/pr-00-gate.yml:1099-1180`, the `Report Gate commit status`
step computes the Gate verdict but its catch block treats only an exception
message containing `rate limit` as recoverable. A fork pull request runs with a
read-only token, so `createCommitStatus` can return `403 Resource not accessible
by integration`; the step rethrows after the verdict is computed and the Gate
appears red without preserving that verdict. Header-only primary/secondary rate
limits are also not distinguished from the fork-token permission failure. The
fleet parent is `stranske/Workflows#3399`, and this create-only consumer copy
must be repaired locally.

## Scope

Update Manager-Mosaic's create-only Gate status-reporting script so fork and
deleted-fork read-only-token 403s preserve the exact computed verdict, while
rate limits remain on their existing best-effort path and unrelated failures
remain loud. Add a focused test that executes the production embedded script.

## Non-Goals

- Do not change reusable keepalive, verifier, autofix, or agent-routing logic.
- Do not weaken same-repository permission failures, non-403 errors, or any
  computed `failure`, `error`, or `pending` verdict.
- Do not treat a rate-limit response as a fork-token permission failure.
- Scaffold-only completion does NOT count: adding a helper or test file without
  executing the real `.github/workflows/pr-00-gate.yml` script and proving the
  deliberate break below is a failure of this issue.

## Tasks

- [ ] In `.github/workflows/pr-00-gate.yml`, classify error-message,
  response-message, `x-ratelimit-remaining`, and `retry-after` rate-limit
  signals before applying the fork read-only-token fallback.
- [ ] In `.github/workflows/pr-00-gate.yml`, warn and append the exact computed
  verdict to `core.summary` for fork and deleted-fork read-only 403s, while
  throwing for same-repository permission errors and all unrelated failures.
- [ ] Create `tests/test_gate_commit_status_fork_tolerance.py` to extract and
  execute the production GitHub Script under Node for success, failure, error,
  pending, deleted-fork, same-repository, rate-limit, non-403, and successful
  status-write cases.
- [ ] Run `uv run pytest -q tests/test_gate_commit_status_fork_tolerance.py --no-cov`,
  focused Ruff checks, YAML safe-load, and the deliberate-break gate below;
  capture the observable results in the PR body.

## Acceptance Criteria

- [ ] `uv run pytest -q tests/test_gate_commit_status_fork_tolerance.py --no-cov`
  passes with the production workflow restored and proves fork/deleted-fork
  read-only 403s preserve the exact computed verdict while same-repository and
  unrelated failures throw.
- [ ] Rate-limit cases detected through the exception message, response message,
  `x-ratelimit-remaining`, and `retry-after` retain the best-effort rate-limit
  path and fail closed when the computed verdict is not `success`.
- [ ] Deliberate-break gate: in `.github/workflows/pr-00-gate.yml`, replace only
  the `readOnlyForkToken` condition with `false`; the named focused pytest must
  fail its fork/deleted-fork cases. Restore the exact file and capture the fail
  and restored-pass outputs in the PR.

## Implementation Notes

- Work only in `.github/workflows/pr-00-gate.yml` and the new focused test.
- Use the existing retry wrapper boundary in the production script; do not
  replace it with a test-only implementation.
- Run the focused pytest with `--no-cov` because the repository's global
  coverage floor is unrelated to this extracted workflow-script regression.

