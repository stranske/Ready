title:	Allow fork Gate to report verdict when token is read-only
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
number:	72
--
## Why

`stranske/Workflows#3399` tracks a fleet break in repository-owned, create-only Gate copies. On current `main` (`77105c5221e87ab8764d093d8d3401090b810331`), `.github/workflows/pr-00-gate.yml:1030-1054` runs `Ensure consolidated summary comment` with the pull-request workflow token and does not tolerate a fork token's `403 Resource not accessible by integration`. The later `Report Gate commit status` catch at `.github/workflows/pr-00-gate.yml:1125-1136` treats only message-based rate limits as recoverable and rethrows the same fork read-only 403. A fork contribution can therefore finish product CI with a computed Gate verdict but still report a failed summary job before either write can publish readable evidence.

## Scope

Update Doc-Lineage's repository-owned Gate so a pull request whose head repository differs from the base repository preserves the computed Gate summary and verdict when the workflow token cannot write comments or statuses. Keep rate-limit handling separate and keep same-repository permission failures loud. This is the Doc-Lineage child of `stranske/Workflows#3399`.

## Non-Goals

- Do not change workflow permissions, `pull_request_target`, branch protection, or token-loading policy.
- Do not treat every 403 as a fork-token failure; same-repository permission errors and unrelated failures must still fail.
- Do not claim this creates the protected `Gate / gate` status when GitHub refuses the write; it preserves the exact computed verdict in warnings and the job summary.
- Scaffold-only or partial completion does not count: fixing only the later status write while the earlier summary-comment write can still fail the job is incomplete, and a test that does not execute both production embedded scripts is insufficient.

## Tasks

- [ ] In `.github/workflows/pr-00-gate.yml`, wrap the `Ensure consolidated summary comment` call so a non-rate-limit fork-only read-only-token 403 emits a warning and writes the existing `gate-summary.md` body to `core.summary`, while same-repository and unrelated failures rethrow.
- [ ] In `.github/workflows/pr-00-gate.yml`, update `Report Gate commit status` to classify message-, response-message-, `x-ratelimit-remaining`-, and `retry-after`-based rate limits before the fork fallback, preserve the exact success/failure/error/pending verdict for fork/deleted-fork read-only-token 403s, and fail closed for non-success verdicts.
- [ ] Create `tests/test_gate_commit_status_fork_tolerance.py` to extract and execute both real GitHub Script steps under Node across fork, deleted-fork, same-repository, rate-limit, non-403, successful-write, and non-success-verdict cases.
- [ ] Run focused pytest, Ruff, YAML safe-load, and diff-hygiene validation, and capture deliberate-break and restored-pass evidence in the pull request.

## Acceptance Criteria

- [ ] `python -m pytest tests/test_gate_commit_status_fork_tolerance.py -q` passes and proves both production embedded scripts tolerate only fork/deleted-fork read-only-token 403s, preserve readable verdict evidence, keep rate-limit handling separate, and leave same-repository and unrelated failures loud.
- [ ] The extracted status-step cases prove `failure`, `error`, and `pending` verdicts still call `core.setFailed`, while successful fork read-only and rate-limit cases record no failure.
- [ ] Deliberate-break gate: replace only the fork read-only predicate in both `.github/workflows/pr-00-gate.yml` handlers with `false`; the exact focused pytest command must fail the named fork/deleted-fork cases, then restore the exact file and capture both failing and passing outputs in the pull request.
- [ ] `python -c "import yaml; yaml.safe_load(open('.github/workflows/pr-00-gate.yml'))"`, focused Ruff checks, and `git diff --check origin/main...HEAD` all succeed; the pull request records the observable command results.

## Implementation Notes

Reference the two-step guard and production-script harness in `stranske/Workflows#3398`, but adapt it to Doc-Lineage's pinned-action and retry-helper shape. The source parent remains open until every affected consumer is merged and the final remote scan reports the fork guard everywhere.

