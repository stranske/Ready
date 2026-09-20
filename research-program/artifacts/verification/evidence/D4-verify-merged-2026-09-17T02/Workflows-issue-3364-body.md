## Summary

The consumer template's `generated-delivery-wakeup` job fires a cross-repo
`repository_dispatch` into `stranske/Workflows` using `WRITE_TOKEN`. That token is not
authorized for the target repo, so the step throws a non-retryable `HttpError` and the whole
`Agents Gate Followups` run is marked `failure` — in every consumer repo, on every Gate
completion for a `sync/workflows-*` or `deps/sync-dev-versions-*` branch.

Observed today (2026-09-04), same failing job and step in three repos:

| Repo | Run | Job | Failing step |
|---|---|---|---|
| `stranske/Travel-Plan-Permission` | [33884908164](https://github.com/stranske/Travel-Plan-Permission/actions/runs/33884908164) | `Wake generated delivery reconciler` | `Dispatch exact generated lane to Workflows` |
| `stranske/Portable-Alpha-Extension-Model` | [33884930515](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/33884930515) (also 33868050096) | same | same |
| `stranske/learning-management-system` | [33872494459](https://github.com/stranske/learning-management-system/actions/runs/33872494459) | same | same |

Annotation on the TPP run:

```
Unhandled error: HttpError: Resource not accessible by personal access token
 - https://docs.github.com/rest/repos/repos#create-a-repository-dispatch-event
```

`Resource not accessible by **personal access token**` (not `by integration`) means the fallback
chain at `templates/consumer-repo/.github/workflows/agents-81-gate-followups.yml:56-60`
(`AGENTS_AUTOMATION_PAT || ACTIONS_BOT_PAT || SERVICE_BOT_PAT || github.token`) resolved a PAT
whose resource scope does not include `stranske/Workflows`.

## What is NOT broken (checked, so this is not filed as a starvation)

`Merge Sync PRs` (`maint-71-merge-sync-prs.yml`) is running fine — 12 successful runs in
`stranske/Workflows` today between 10:59Z and 14:55Z, all via `workflow_dispatch`, none via
`repository_dispatch`. The reconciler is being woken by another route, so sync PRs are **not**
starved. This dispatch path is a redundant wakeup that is dead, and its only current effect is
noise.

That noise is the actual cost: `Agents Gate Followups` goes red in consumer repos for a reason
that has nothing to do with the PR under test, which is exactly the condition that trains readers
(and closer lanes) to discount a red Gate Followups run. This surfaced while auditing why
Fine-Art-Archive #680 looked unhealthy.

## Tasks

- [ ] In `templates/consumer-repo/.github/workflows/agents-81-gate-followups.yml`, stop letting a
  cross-repo authorization failure fail the run. The wakeup is best-effort and provably redundant:
  catch the non-retryable authorization error (403/404 from `createDispatchEvent`), emit
  `core.notice`/`core.warning` naming the token that was tried and the target, and exit the step
  successfully. Keep the existing `withRetry` behaviour for 429/5xx.
- [ ] Do not broaden the failure swallow: a 5xx after retries, or any other status, must still fail
  so a genuinely broken dispatch is still visible.
- [ ] Mirror the change into any other cross-repo `createDispatchEvent` call in the same template
  that has the same best-effort character (audit `env.WRITE_TOKEN` uses at lines 1381, 1442, 1812,
  1889, 2090, 2164 and change only the ones that are genuinely best-effort).
- [ ] Add a test in `tests/workflows/` asserting the step yaml handles the authorization error
  branch, so the swallow cannot silently widen later.

## Test gate

Named gate: the new `tests/workflows/` case for the `generated-delivery-wakeup` error handling,
plus the existing consumer-template parity tests.

Deliberate-break demonstration required in the PR: with the fix in place, revert only the
error-handling branch (let the 403 propagate) and show the new test going RED, then restore it and
show it GREEN. Paste both blocks.

## Non-goals

- Do not rotate, mint, or re-scope any PAT in this issue, and do not add a new secret name to the
  fallback chain. If the owner later widens `AGENTS_AUTOMATION_PAT` to include `stranske/Workflows`,
  the dispatch starts working again and this change stays correct either way.
- Do not remove the `generated-delivery-wakeup` job. It is the intended fast path; only its failure
  mode is wrong.
- Do not touch `maint-71-merge-sync-prs.yml` or the sync-PR lifecycle.
- No scaffolding: no new workflow, no new script, no config toggle.

<!-- workflow-source:local_request -->
_Filed by the Claude closer lane, 2026-09-04._

