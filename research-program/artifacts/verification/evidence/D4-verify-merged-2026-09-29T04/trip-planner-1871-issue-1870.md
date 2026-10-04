title:	Allow fork Gate to report verdict when status token is read-only
state:	CLOSED
author:	stranske
labels:	priority:normal
comments:	3
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1870
--
## Why

The repository-owned Gate computes its verdict and then publishes the required
`Gate / gate` status in `.github/workflows/pr-00-gate.yml:272-309`. The current
catch block recognizes only a message-based rate limit at lines 302-308. For a
pull request from a fork or deleted fork, GitHub gives this workflow a read-only
token, so `github.rest.repos.createCommitStatus` receives a non-rate-limit 403
after the Gate has already computed its verdict. The job rethrows that response,
loses the verdict evidence, and makes otherwise passing fork CI look broken.

This is verified latent fleet fragility tracked by
`stranske/Workflows#3399`, not a currently observed trip-planner product
regression. The missing behavior is a narrow fork/deleted-fork fallback that
preserves the computed Gate verdict without hiding same-repository permission
failures or genuine rate limits.

## Scope

Harden only trip-planner's consumer-owned `.github/workflows/pr-00-gate.yml`
status-publication step and add a focused repository test that extracts and
executes that production GitHub Script under Node.

## Non-Goals

- Do not change workflow permissions, switch to `pull_request_target`, modify
  the reusable CI matrix, or claim this makes a protected branch mergeable
  without a maintainer-written status.
- Do not tolerate every 403: same-repository permission failures and unrelated
  errors must still throw, and rate-limit handling must remain a separate path.
- Do not change the create-only ownership policy for `pr-00-gate.yml` or edit
  synced keepalive/routing workflows.
- Scaffold-only or partial completion does not count: a test file that does not
  execute the actual embedded workflow script, or omits failure/error/pending,
  same-repository, rate-limit, and unrelated-error cases, does not satisfy this
  issue.

## Tasks

- [ ] In `.github/workflows/pr-00-gate.yml`, classify message-, response-message-,
  `x-ratelimit-remaining`, and `retry-after` rate-limit signals before any fork
  fallback is considered.
- [ ] In `.github/workflows/pr-00-gate.yml`'s `Report Gate commit status` job, detect fork and
  deleted-fork pull requests and preserve the computed success/failure/error/
  pending verdict in a warning and `core.summary` when a non-rate-limit
  read-only-token 403 prevents status publication; keep non-success verdicts
  fail-closed.
- [ ] Create `tests/test_gate_commit_status_fork_tolerance.py` to extract and
  execute the actual `actions/github-script` body from
  `.github/workflows/pr-00-gate.yml` under Node for fork, deleted-fork,
  same-repository, independent rate-limit-signal, unrelated-error, and
  successful-write cases.
- [ ] Run `python -m pytest --no-cov tests/test_gate_commit_status_fork_tolerance.py -q` for the deliberate-break gate below, capture the red and green
  outputs in the pull request, and restore the exact production workflow before
  committing.

## Acceptance Criteria

- [ ] `python -m pytest --no-cov tests/test_gate_commit_status_fork_tolerance.py -q`
  exits 0 after executing the production embedded script and reports every
  focused case passed.
- [ ] Deliberate-break verification: temporarily change only the
  `readOnlyForkToken` expression in `.github/workflows/pr-00-gate.yml` to
  `false`; the exact focused pytest command must fail the named fork and
  deleted-fork verdict cases. Restore that expression exactly, rerun the same
  command to green, and capture both outputs in the pull request.
- [ ] Fork/deleted-fork non-rate-limit 403s preserve the exact
  success/failure/error/pending verdict; non-success states call
  `core.setFailed`, while same-repository 403s and unrelated errors still throw.
- [ ] Rate-limit detection independently covers error message, response
  message, `x-ratelimit-remaining: 0`, and `retry-after`; none enters the fork
  fallback.
- [ ] `python -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('.github/workflows/pr-00-gate.yml').read_text())"`
  exits 0, and `git diff --check origin/main...HEAD` prints no errors; record
  both observable results in the pull request.

## Implementation Notes

- Parent campaign: `stranske/Workflows#3399`.
- Use the already-delivered consumer children as behavioral references, but
  preserve trip-planner's local Gate shape and existing rate-limit behavior.
- `PyYAML` is already declared in the `dev` optional dependency group, so the
  focused test must not add a duplicate dependency.

