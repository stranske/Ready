# Astra migration and unattended readiness review

Reviewed 2026-09-04; updated 23:42 UTC. Astra source changes are merged and installed locally. Consumer delivery remains in progress through Maint 68/71.

## Current disposition

The previous migration was incomplete: important Orchestrator changes were uncommitted, shared Workflows/consumer defaults remained Terra, seven relevant high-reasoning automations remained Terra, and the isolated repo-review Codex home remained Sol. Those local settings are now Astra/high. Source fixes are in [Workflows #3379](https://github.com/stranske/Workflows/pull/3379) and [Orchestrator #233](https://github.com/stranske/Orchestrator/pull/233); final remote state is recorded below after delivery checks.

The unattended engine is running. At 23:38:58 UTC it reported 44 of 44 units done, unpaused, with no phase stops. All four falsely completed jobs were recovered and actually completed, followed by a downstream consistency pass. The corrected dossiers, summaries and seven Word export destinations are refreshed. Future work remains demand-driven through the scheduled refill mechanism; an empty queue is an intentional stop state. The next refill is due 2026-09-05 03:47 UTC (22:47 Central on September 4), then every twelve hours, and includes all three new product repositories.

## Astra scope and evidence

- Local Codex default: gpt-6-astra with high reasoning, CLI 0.153.2. A live read-only CLI invocation returned exactly ASTRA_HIGH_CANARY_OK and turn.completed.
- Migrated relevant high-reasoning automations: imi-merge-verify-closer, reviewed-repo-automation-controller, workflows-campaign-monthly-controller, pd-workloop-resume, reviewed-repo-orphan-pr-steward, refresh-codex-auth-json, and research-program. Schedules, working directories, and enabled/paused states were preserved and read back. Existing Astra xhigh workers were already migrated. Medium/low cost tiers and the unrelated paused allocator intake were preserved.
- Isolated review home: ~/.codex/automations/repo-review-codex-home/config.toml now selects Astra/high.
- Orchestrator full tier: Astra/high; mid Terra and cheap Luna unchanged. Sol is excluded by active routing retirement policy while immutable historical database rows remain valid. The installed runtime mirror and canonical source carry the compatible implementation.
- Workflows source and consumer templates: Astra worker/checkbox defaults, model catalog, derived candidate list, Responses/high client settings without temperature, CLI 0.153.2 lockfile, and updated canonical documentation. Read-only trials use an immutable runner commit and reviewed npm lockfile.
- New trials compare Astra/Terra/Luna. Existing frozen Sol/Terra/Luna manifests remain interpretable and ingestible.
- Initial live inventory found no per-repository model variable overrides in the 16 distinct canonical remote repositories. Registered consumer distribution is managed by Maint 68/71; a source merge is not by itself proof of consumer delivery.

OpenAI contract checked against [the official latest-model guide](https://developers.openai.com/api/docs/guides/latest-model). Historical evidence, explicit cheaper tiers, and prior evaluation fixtures were not globally rewritten.

## Unattended plan repairs

Reviewed the Projects plan v2, the Astra behavioral contract, the engine's B7 plan v3 and OWNER_NOTES, live queue/state, automation files, launchd job, capacity policy and GitHub status mirror.

1. Fixed invalid launchd plist XML and changed the actual driver from three units per tick to one. Reloaded the idle job and verified its successful invocation. The 15-minute cadence remains.
2. Replaced the research clone directory's temporary-session symlink with a durable local directory. Updated dossier lookup and automation dispatcher paths to local disk; launchd no longer depends on Dropbox for these reads.
3. Enforced phase stops before claims. Missing capacity now blocks that seat instead of granting permission. Router fallback only applies when the router is unavailable, not when it declines capacity.
4. Made parked questions nonblocking defaults on the original unit, preserving dependency identity and preventing duplicate writers. Paginated inbox reads and late answers are retained in OWNER_NOTES even after a unit finishes.
5. Completion now requires a successful subprocess, no explicit dispatcher error envelope, a fresh output file, and the artifact floor; dossier verification also requires its verification table. A successful dispatcher can return plain text, which is accepted. Failed engine commands raise errors rather than impersonating NO_UNIT.
6. Audited claimed completions: three failed Gemini verification runs and one timed-out Cursor unblock sweep had been marked done. Requeued them with checkpoints and retained artifacts. The repaired driver subsequently completed the unblock sweep successfully (656-word artifact); all three dossier verifications subsequently completed successfully.
7. Serialized GitHub mirroring, checked git command outcomes and made pending pushes retry even during empty ticks. The repaired queue status was read back from GitHub.
8. Made audit round IDs unique and merged refill additions into the fresh queue, preserving concurrent completions. Future completed audits replace the last-filed-set denominator using unique intake URLs added since their first claim; the denominator no longer grows cumulatively across completed rounds. Added Deliverable-Render and Manager-Mosaic to the research refill population from the current plan; lane fleet arrays were preserved.
9. Preserved Claude conservation through 2026-09-06 12:00 UTC with its existing automatic expiry. Verified macOS sleep disabled and local executor apps running.

## Validation

- Research engine: 16 focused regression tests passed, including capacity, phase stops, nonblocking questions, pagination, concurrent refill, per-round denominators, process failures and stale outputs.
- Orchestrator: 105 focused tests passed; dispatcher/adapter selftests passed. A copy of the installed feedback database upgraded without altering old profile definitions. Frozen historical trial ingestion has regression coverage.
- Workflows: 130 focused Python tests passed, 2 existing permission-gated cases skipped; template completeness passed; registry JavaScript tests passed earlier in the review. GitHub CI is checked separately on the exact final heads.
- CodeRabbit reported a spending cap. An independent Orchestrator/Cursor advisory review found candidate-list drift and a database compatibility regression; both were fixed with regression checks. All substantive inline findings on the source PRs were addressed.

## Limits and recovery

The plan's 80% aggregate allowance is not a measured, enforced cross-provider spending cap. Orchestrator capacity controls are active, but mixed subscription windows do not supply a trustworthy aggregate dollar denominator. This review does not certify that budget target as enforced.

The machine must stay powered with its desktop sessions available for local workers. The daily cloud routine is a backstop; issue-comment webhook delivery was not independently demonstrated by this review. Local inbox polling remains the primary verified path. No additional owner approval queue was introduced.

Backups: ~/.codex/automations/research-program/maintenance-backups/20260904-astra/. Existing research artifacts and unrelated dirty repository files were preserved. Worktrees for the source PRs are under ~/.codex/worktrees/astra-rollout/, outside the neutral Dropbox Code root.

Owner-facing status: [research-program/STATUS.md](https://github.com/stranske/Ready/blob/main/research-program/STATUS.md). Existing inbox: [Ready #553](https://github.com/stranske/Ready/issues/553).

## Final remote delivery evidence

- Workflows #3379 merged at 23:02:15 UTC as `b06c6d16c3162a624c179a4c4f2080ec3c14876e`.
- Orchestrator #233 merged at 23:02:19 UTC as `ebe1ca514eca08d3489536f899072f1b8e1fc24c`.
- Both exact source heads passed every reported check, had zero unresolved review threads, were directly mergeable, and exceeded the seven-minute review window before merging.
- [Maint 68 source-delta canary run](https://github.com/stranske/Workflows/actions/runs/33927956548) uses exact range `0b65b95a362ae4643aaa0326bdc06b1b47f814b7..b06c6d16c3162a624c179a4c4f2080ec3c14876e`. Consumer delivery is still in progress.
- Canonical local Workflows fast-forwarded to the merged source while preserving its unrelated untracked test.
- The report itself was read back from the Ready GitHub mirror.


## Later unattended execution evidence

The repaired scheduled driver completed Pension-Data verification at 23:05:50 UTC (1,648 words; 63 checked claims). Codex completed Portable-Alpha verification at 23:19:04 (54 claim groups; 13 corrected). The driver completed Travel-Plan-Permission at 23:24:08 (2,064 words; 54 claims, 9 corrected, 1 explicitly unverified). The bounded downstream consistency unit then corrected the index, R5, B2 and curriculum summaries, including the mistaken assertion that PAEM rejected browser delivery.

The three redacted Work-bundle Markdown files and seven Word destinations were regenerated from corrected evidence. All four unique documents passed structural verification and all 29 rendered pages were visually inspected. See [export refresh evidence](https://github.com/stranske/Ready/blob/main/research-program/artifacts/readiness/export-refresh-20260904.md). Prior exports were backed up.

## Consumer coordination defect found during rollout

The first Astra source-delta candidates were closed, not merged, by an older Maint 71 campaign at 23:09 UTC. Its `plan_mismatch` handling incorrectly treated another plan's delivery as superseded. The subsequent `stable_base_refresh_required` result was a downstream missing-candidate symptom, not evidence of a changed base. [Workflows #3382](https://github.com/stranske/Workflows/pull/3382) makes plan-bound retries preserve other plans and limits stale cleanup to the selected plan. Its regression test runs the real reconciliation with mutations enabled and asserts no close/comment/delete calls for a foreign plan.

The automatic recovery generated a full template plan, bringing unrelated review findings back into scope. After the ownership fix, the intended recovery is the original immutable Astra source delta. Source migrations remain merged; consumer completion is not yet certified.

Live branch verification: Trend_Model_Project now has `refs/heads/main` at `18616a82837411b35d1581e86daf726737cf2142`; direct `refs/heads/phase-3` lookup returns 404. The old branch endpoint reports the renamed main branch. This review did not recreate an obsolete branch or alter lane arrays.


## Coordination recovery verification

Workflows #3382 merged at 23:29:30 UTC as `72be6db44dd81a7eb8bdaeaf5437a00d1bd5f221`, after 81 JavaScript tests, independent review, all remote checks and the review window. The older campaign retry at 23:32 closed zero newer candidates; its remaining failures were missing targets for its old plan. The current Astra candidate pass at 23:38 started an explicit review window on all three unchanged candidate heads, eligible after 23:45:28 UTC. No generated PR was directly merged or closed by this review.


## Remote runner canary follow-up

The local Astra invocation succeeded, but the first GitHub Actions canary [33930520106](https://github.com/stranske/Workflows/actions/runs/33930520106) failed before creating any job: its reusable workflow was not found at the orphaned pre-squash commit. This is workflow resolution evidence, not an Astra capacity/authentication failure. [Workflows #3386](https://github.com/stranske/Workflows/pull/3386) pins the caller and both registries to reachable merged commit `b06c6d16c3162a624c179a4c4f2080ec3c14876e`; the runner, helper and CLI lockfile are byte-identical. Fourteen focused tests and independent review passed. Remote execution and final consumer delivery still require verification after this repair merges.


## Remote Astra execution verified

Workflows #3386 merged at 23:52:24 UTC as `913e2625bdc471de84addea5b4cc8dfefca1c78a` after all checks and zero unresolved threads on exact head `90935a8129081c2c31d7ec1ed4f663b4ebacce67`. The repaired [GitHub canary 33931099913](https://github.com/stranske/Workflows/actions/runs/33931099913) passed: Codex CLI 0.153.2 requested, selected and reported `gpt-6-astra` / `high`, exited zero, recorded no fallback and preserved identical before/after source manifests. Provider-resolved model identity is not exposed by this artifact; no stronger claim is made. Consumer sync [33931101622](https://github.com/stranske/Workflows/actions/runs/33931101622) now uses the corrected source commit and original Astra source-delta base.


## Concurrent state safety

State writes now use atomic replacement and a dedicated read/modify/write lock. Maintenance and digest updates merge only their own fields, so a concurrent inbox pause or phase stop is retained. Inbox consumers are serialized to avoid duplicate comment application. Regression tests reproduce a pause arriving during digest posting, concurrent independent writers, and readers during a partial temporary write. All 16 readiness tests pass.
