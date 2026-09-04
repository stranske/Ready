# Astra migration and unattended readiness review

Reviewed 2026-09-04. Source delivery remains in progress; this report distinguishes installed local behavior from remote delivery.

## Current disposition

The previous migration was incomplete: important Orchestrator changes were uncommitted, shared Workflows/consumer defaults remained Terra, seven relevant high-reasoning automations remained Terra, and the isolated repo-review Codex home remained Sol. Those local settings are now Astra/high. Source fixes are in [Workflows #3379](https://github.com/stranske/Workflows/pull/3379) and [Orchestrator #233](https://github.com/stranske/Orchestrator/pull/233); final remote state is recorded below after delivery checks.

The unattended engine is running and has completed a recovered unit with the repaired driver. At the 22:55 UTC checkpoint it reported 40 done / 3 queued, unpaused, no phase stops. Three previously failed dossier-verification outputs remain queued for actual validation; the earlier claim of 43 complete was not reliable.

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
6. Audited claimed completions: three failed Gemini verification runs and one timed-out Cursor unblock sweep had been marked done. Requeued them with checkpoints and retained artifacts. The repaired driver subsequently completed the unblock sweep successfully (656-word artifact); the three dossier verifications await their queue turns.
7. Serialized GitHub mirroring, checked git command outcomes and made pending pushes retry even during empty ticks. The repaired queue status was read back from GitHub.
8. Made audit round IDs unique and merged refill additions into the fresh queue, preserving concurrent completions. Future completed audits replace the last-filed-set denominator using unique intake URLs added since their first claim; the denominator no longer grows cumulatively across completed rounds. Added Deliverable-Render and Manager-Mosaic to the research refill population from the current plan; lane fleet arrays were preserved.
9. Preserved Claude conservation through 2026-09-06 12:00 UTC with its existing automatic expiry. Verified macOS sleep disabled and local executor apps running.

## Validation

- Research engine: 13 focused regression tests passed, including capacity, phase stops, nonblocking questions, pagination, concurrent refill, per-round denominators, process failures and stale outputs.
- Orchestrator: 105 focused tests passed; dispatcher/adapter selftests passed. A copy of the installed feedback database upgraded without altering old profile definitions. Frozen historical trial ingestion has regression coverage.
- Workflows: 130 focused Python tests passed, 2 existing permission-gated cases skipped; template completeness passed; registry JavaScript tests passed earlier in the review. GitHub CI is checked separately on the exact final heads.
- CodeRabbit reported a spending cap. An independent Orchestrator/Cursor advisory review found candidate-list drift and a database compatibility regression; both were fixed with regression checks. All substantive inline findings on the source PRs were addressed.

## Limits and recovery

The plan's 80% aggregate allowance is not a measured, enforced cross-provider spending cap. Orchestrator capacity controls are active, but mixed subscription windows do not supply a trustworthy aggregate dollar denominator. This review does not certify that budget target as enforced.

The machine must stay powered with its desktop sessions available for local workers. The daily cloud routine is a backstop; issue-comment webhook delivery was not independently demonstrated by this review. Local inbox polling remains the primary verified path. No additional owner approval queue was introduced.

Backups: ~/.codex/automations/research-program/maintenance-backups/20260904-astra/. Existing research artifacts and unrelated dirty repository files were preserved. Worktrees for the source PRs are under ~/.codex/worktrees/astra-rollout/, outside the neutral Dropbox Code root.

Owner-facing status: [research-program/STATUS.md](https://github.com/stranske/Ready/blob/main/research-program/STATUS.md). Existing inbox: [Ready #553](https://github.com/stranske/Ready/issues/553).

## Final remote delivery evidence

Pending source CI and controlled consumer distribution at report creation. Updated below as verified.
