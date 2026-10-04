title:	Allow fork Gate to report verdict when status token is read-only
state:	CLOSED
author:	stranske
labels:	agents:formatted, priority:normal
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
number:	62
--
## Why

`main` still has a fork-unsafe Gate status publisher. In `.github/workflows/pr-00-gate.yml:1099-1179`, the `Report Gate commit status` step catches rate-limit 403s but rethrows every other 403. For a pull request from a fork (including a deleted fork), GitHub can allow the Gate to compute its verdict while denying `createCommitStatus`; the current handler turns that expected read-only-token condition into a failed workflow and loses the computed `success`, `failure`, `error`, or `pending` verdict. This is a verified current defect in the create-only consumer Gate, not hypothetical cleanup.

## Scope

Make the repository-owned Gate preserve the exact computed verdict for fork/deleted-fork read-only-token 403s, keep rate limits on their existing path, and keep same-repository permission failures and unrelated errors loud. Add a focused test that extracts and executes the production GitHub Script under Node.

## Non-Goals

- Do not change workflow permissions, `pull_request_target`, token selection, branch protection, or the create-only ownership of `pr-00-gate.yml`.
- Do not tolerate arbitrary 403 responses; same-repository permission failures must still throw.
- Do not claim this creates a protected-branch status when GitHub rejects the write; it preserves visible verdict evidence in warnings and the job summary.
- Scaffold-only or partial completion does not count: a copied test that does not execute the real script, or a handler that covers only `success`, is not completion.

## Tasks

- [ ] In `.github/workflows/pr-00-gate.yml`, extend `Report Gate commit status` to classify message-, response-message-, `x-ratelimit-remaining`-, and `retry-after`-based rate limits before a fork/deleted-fork read-only-token fallback.
- [ ] In `.github/workflows/pr-00-gate.yml`, preserve the exact computed Gate state and description in `core.warning` and `core.summary`, and call `core.setFailed` for non-success verdicts when the commit-status write is unavailable.
- [ ] Create `tests/test_gate_commit_status_fork_tolerance.py` to extract and execute the production step script under Node across fork/deleted-fork, same-repository, unrelated-error, rate-limit, and all four verdict cases.
- [ ] Run `uv run pytest -q tests/test_gate_commit_status_fork_tolerance.py --no-cov` for the deliberate break and exact restoration, and capture both outputs in the pull request body.

## Acceptance Criteria

- [ ] `uv run pytest -q tests/test_gate_commit_status_fork_tolerance.py --no-cov` exits 0 and reports every focused case passing; the test executes the script extracted from `.github/workflows/pr-00-gate.yml`, not a duplicate implementation.
- [ ] Deliberately changing only the production `readOnlyForkToken` predicate to `false` makes the named pytest command fail in the fork/deleted-fork cases; restoring the exact file makes the same command pass, with both outputs captured in the PR.
- [ ] The focused test observes that fork/deleted-fork read-only 403s preserve `success`, `failure`, `error`, and `pending`; non-success states call `core.setFailed`, while same-repository 403s and non-403 errors still throw.
- [ ] `python -c "import yaml, pathlib; yaml.safe_load(pathlib.Path('.github/workflows/pr-00-gate.yml').read_text())"` exits 0, proving the edited workflow remains valid YAML.

## Implementation Notes

Follow the already-merged Workflows campaign contract in `stranske/Workflows#3399`, while adapting the harness to this repository's current Gate shape. Keep the change limited to the create-only Gate and its focused regression test.

