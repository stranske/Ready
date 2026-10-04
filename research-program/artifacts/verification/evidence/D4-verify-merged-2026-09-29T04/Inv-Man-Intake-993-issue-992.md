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
number:	992
--
## Why

The repository-owned Gate currently catches commit-status failures in `.github/workflows/pr-00-gate.yml:177-194`, but it recognizes only message-based rate limits and rethrows every other 403. On a pull request from a fork or deleted fork, the read-only `GITHUB_TOKEN` cannot call `repos.createCommitStatus`, so the `gate-summary` job fails while trying to publish the verdict instead of preserving the computed success or failure result. This is a verified latent fleet defect tracked by `stranske/Workflows#3399`; the current workflow has no `isForkPullRequest` or read-only-token fallback.

## Scope

Update Inv-Man-Intake's create-only `.github/workflows/pr-00-gate.yml` copy so only fork/deleted-fork, non-rate-limit 403 status-write failures are tolerated and the computed Gate verdict remains visible in the warning/job summary. Add a focused executable regression test for the embedded GitHub Script.

## Non-Goals

- Do not change the protected required-context architecture tracked separately by `stranske/Workflows#3605`.
- Do not swallow primary, secondary, or abuse rate limits, non-403 failures, or same-repository permission failures.
- Do not modify shared agent/keepalive/verifier workflows.
- Scaffold-only completion does NOT count: adding a test file or warning text without executing the production embedded script across fork and non-fork failure cases is not done.

## Tasks

- [ ] Update the `Report Gate commit status` step in `.github/workflows/pr-00-gate.yml` to distinguish rate-limit 403s from fork/deleted-fork read-only-token 403s and to preserve the computed Gate verdict in observable output.
- [ ] Create `tests/test_gate_commit_status_fork_tolerance.py` that extracts and executes the production `actions/github-script` body under Node for success, failure, fork, rate-limit, same-repository, and unrelated-error cases.
- [ ] Record deliberate-break evidence by temporarily disabling only the fork read-only fallback, running the named pytest gate to a real failure, reverting the break, and rerunning it to green; capture the commands and counts in the PR body.

## Acceptance Criteria

- [ ] `python -m pytest --no-cov tests/test_gate_commit_status_fork_tolerance.py -q` executes the actual script from `.github/workflows/pr-00-gate.yml` and passes every focused case after restoration.
- [ ] With only the fork read-only fallback deliberately disabled, `python -m pytest --no-cov tests/test_gate_commit_status_fork_tolerance.py -q` fails at least one named fork/deleted-fork case; after reverting that mutation, the same command passes, with both outputs captured in the PR.
- [ ] Fork/deleted-fork non-rate-limit 403s emit a warning/job-summary verdict without failing the status-publication step, while same-repository 403s, rate-limit 403s, and non-403 errors retain their intended fail-closed or rate-limit behavior.
- [ ] `python -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('.github/workflows/pr-00-gate.yml').read_text())"` exits 0 and `git diff --check origin/main...HEAD` prints no errors.

## Implementation Notes

- Parent fleet campaign: `stranske/Workflows#3399`.
- This repo has the older Gate shape: only the `Report Gate commit status` write needs the fork-token guard; there is no earlier consolidated-summary comment write.
- Preserve existing message-based rate-limit behavior while adding header-aware primary/secondary rate-limit detection before the fork fallback, matching the hardened consumer children already delivered in this campaign.

