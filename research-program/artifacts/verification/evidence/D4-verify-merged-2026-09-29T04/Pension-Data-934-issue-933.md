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
number:	933
--
## Why

The repository-owned Gate computes its verdict, then publishes the required `Gate / gate` status from `.github/workflows/pr-00-gate.yml:152-189`. Its error handler recognizes only message-based rate limits and rethrows every other 403. On a pull request from a fork or deleted fork, GitHub gives the workflow a read-only token, so `github.rest.repos.createCommitStatus` is rejected and the `gate-summary` job loses the already-computed verdict. This is a verified latent fleet defect tracked by `stranske/Workflows#3399`; the current workflow contains no `isForkPullRequest` guard or read-only-token fallback.

## Scope

Update Pension-Data's create-only `.github/workflows/pr-00-gate.yml` status-publication step and add a repository-local regression test that executes the actual embedded GitHub Script. Preserve the existing Gate calculation and `Enforce Gate success` behavior.

## Non-Goals

- Do not solve trusted required-context publication for fork PRs; that separate architecture/security concern is tracked by `stranske/Workflows#3605`.
- Do not change reusable Workflows-owned CI, keepalive, verifier, or sync files.
- Do not weaken rate-limit handling or swallow same-repository permission errors and unrelated failures.
- Scaffold-only completion does not count: adding a helper or test fixture without executing the production script and demonstrating the deliberate-break failure is not completion.

## Tasks

- [ ] In `.github/workflows/pr-00-gate.yml`, harden the `Report Gate commit status` script so message-, response-message-, primary-header-, and secondary-header-based rate-limit 403s keep their existing warning path before any fork fallback is considered.
- [ ] In `.github/workflows/pr-00-gate.yml`, detect fork and deleted-fork pull requests and preserve the computed Gate verdict in a warning and job summary when `createCommitStatus` receives a non-rate-limit read-only-token 403; fail closed for every non-success verdict.
- [ ] Create `tests/test_gate_commit_status_fork_tolerance.py` to extract and execute the production `actions/github-script` body under Node for success, failure, error, pending, deleted-fork, same-repository, independent rate-limit-signal, and unrelated-error cases.
- [ ] Temporarily disable only the `readOnlyForkToken` expression in `.github/workflows/pr-00-gate.yml`, run the named focused pytest gate to a real failure, capture the failing output, restore the exact workflow, and rerun the same command to green.

## Acceptance Criteria

- [ ] `python -m pytest --no-cov tests/test_gate_commit_status_fork_tolerance.py -q` executes the actual script from `.github/workflows/pr-00-gate.yml` and passes every focused case after restoration; record the command and count in the PR.
- [ ] Deliberate-break gate: with only the `readOnlyForkToken` expression changed to `false`, `python -m pytest --no-cov tests/test_gate_commit_status_fork_tolerance.py -q` fails named fork/deleted-fork cases; after reverting that mutation, the same command passes, and both outputs are captured in the PR.
- [ ] Fork/deleted-fork non-rate-limit 403s emit the exact success/failure/error/pending verdict without turning a successful Gate red; non-success verdicts still call `core.setFailed`, while same-repository 403s and unrelated errors still throw.
- [ ] Rate-limit detection independently covers error message, response message, `x-ratelimit-remaining: 0`, and `retry-after`; none of those signals enters the fork read-only fallback.
- [ ] `python -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('.github/workflows/pr-00-gate.yml').read_text())"` exits 0 and `git diff --check origin/main...HEAD` prints no errors; capture both results in the PR.

## Implementation Notes

- This repository has the older Gate shape: the status-write step is the only write in `gate-summary`; there is no preceding consolidated-summary comment upsert to guard.
- Preserve the existing `Gate / gate` context, description truncation, target URL, and `Enforce Gate success` step.
- The fixed sibling implementations under `stranske/Inv-Man-Intake#993` and `stranske/Ready#602` cover the hardened rate-limit classifier and fail-closed non-success behavior expected here.

