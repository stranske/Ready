# Astra migration and unattended readiness review

Updated 2026-09-05 02:38 UTC. **Astra is installed locally and verified in GitHub Actions. Remote consumer delivery is still in progress.**

## Current state

The previous migration was incomplete. I finished the local model settings, merged the source repairs, and verified Astra/high with both a local CLI call and a remote Actions run. Sixteen canonical checkouts now carry the active Astra settings. Their existing branches and unrelated edits were preserved; installations on older branches are recorded working-tree patches, not claims that those branches have fast-forwarded.

The research engine is running, unpaused, with no phase stops. **All 45 current units are done** as of 01:26 UTC, including a newly enqueued merged-PR verification that completed after the initial 44-unit batch. Four earlier false completions were repaired and successfully rerun. The corrected dossiers, dependent summaries, and seven Word destinations are refreshed; all 29 rendered pages passed visual review. The next demand-driven audit refill check is due September 5 at 03:47 UTC (September 4, 22:47 Central), then every twelve hours.

**The requested 80% aggregate spending allowance is not measured or enforced across providers.** Per-provider capacity checks and Claude conservation are active, but the mixed subscription windows have no trustworthy aggregate spending denominator. This remains a limitation, not a certified budget control.

## Astra coverage

- Codex default and isolated repo-review home: `gpt-6-astra`, high reasoning; CLI 0.153.2.
- Seven remaining high-reasoning automations migrated: opener, closer, reviewed-repo controller, monthly campaign controller, orphan PR steward, auth refresh, and research program. Schedules, directories and active/paused states were preserved. Existing Astra/xhigh seats and cheaper tiers remain as configured.
- Orchestrator full tier: Astra/high; mid Terra and cheap Luna. Current routing retires Sol while the immutable historical profile registry still validates old database rows and trial manifests. The installed runtime mirror was refreshed.
- Workflows source/templates: Astra agent defaults, model catalog and derived candidates, Responses/high client settings, CLI lockfile, and a reachable immutable trial runner. New trials use Astra/Terra/Luna; historical Sol trials remain interpretable.
- All sixteen local agent registries select Astra. Exact patches, source hashes, preserved heads and backups are recorded in [local installation evidence](https://github.com/stranske/Ready/blob/main/research-program/artifacts/readiness/local-astra-installation.json).
- The local read-only invocation returned `ASTRA_HIGH_CANARY_OK`. [Remote canary 33931099913](https://github.com/stranske/Workflows/actions/runs/33931099913) requested, selected and reported Astra/high, exited zero, recorded no fallback, and left its source manifest unchanged. The artifact does not expose provider-resolved model identity.

The model contract was checked against the [official latest-model guide](https://developers.openai.com/api/docs/guides/latest-model). Historical records and explicit cheaper tiers were not globally rewritten.

## Source delivery and consumer rollout

| Source repair | Merged commit |
|---|---|
| [Workflows #3379: Astra defaults and trial support](https://github.com/stranske/Workflows/pull/3379) | `b06c6d16c3162a624c179a4c4f2080ec3c14876e` |
| [Orchestrator #233: routing and historical compatibility](https://github.com/stranske/Orchestrator/pull/233) | `ebe1ca514eca08d3489536f899072f1b8e1fc24c` |
| [Workflows #3382: preserve deliveries owned by another plan](https://github.com/stranske/Workflows/pull/3382) | `72be6db44dd81a7eb8bdaeaf5437a00d1bd5f221` |
| [Workflows #3386: reachable immutable runner](https://github.com/stranske/Workflows/pull/3386) | `913e2625bdc471de84addea5b4cc8dfefca1c78a` |
| [Workflows #3388: fresh sealing event](https://github.com/stranske/Workflows/pull/3388) | `f88d7fc5f6ce6f78c64d0341eaea7dbe9aa78c19` |

Every merged source head passed its checks, had zero active, non-outdated unresolved review threads, was directly mergeable, and exceeded the seven-minute review window. CodeRabbit capacity was unavailable; independent Orchestrator/Cursor advisory reviews were completed and substantive findings fixed. Required statuses were not bypassed.

The consumer migration uses source range `0b65b95a362ae4643aaa0326bdc06b1b47f814b7..913e2625bdc471de84addea5b4cc8dfefca1c78a`, plan `sha256:695d947ab30a1bbeb81d5fe2006db08c375126d10ce8f442df3c63997485c681`, and [Maint 68 run 33931101622](https://github.com/stranske/Workflows/actions/runs/33931101622). Only the three Astra manifest paths are in this delivery.

All three canaries are sealed and have passing required Gates. trip-planner required a verified label refresh because a stale `sync:delivery-ready` label prevented sealing from emitting a fresh event. Its old run retained the unsealed payload when rerun. The fresh [required Gate 33933089879](https://github.com/stranske/trip-planner/actions/runs/33933089879) passed on attempt 2 after exposing a separate parallel-test race. The green `gate` job in run 33933089597 was an automation eligibility job, not the required CI Gate; evidence was corrected accordingly.

[Workflows #3388](https://github.com/stranske/Workflows/pull/3388) merged and was installed into both local Workflows checkouts. It clears stale ready labels before advancing review state. [trip-planner #1792](https://github.com/stranske/trip-planner/pull/1792) isolates a negative packaging test that had rewritten real production code concurrently with positive checks; serial and xdist checks and all remote checks passed; its merge is held until the Astra fleet transition finishes. After one safely deferred quota-exhausted run, reconciliation resumed when the actual primary quota reset. Promotion [33934143121](https://github.com/stranske/Workflows/actions/runs/33934143121) created/refreshed all fourteen deliveries. Ready alone needed an exact-plan base refresh [33935024740](https://github.com/stranske/Workflows/actions/runs/33935024740) after a status-mirror push. Owner reconciliation has merged thirteen consumer deliveries, including Ready #552 and the separately owned Collab-Admin exception. Exact default-branch inspection verifies Astra in **14 of 18 applicable repositories** (including Workflows); four remain pending: Travel-Plan-Permission, trip-planner, Portable-Alpha-Extension-Model and Trend_Model_Project. Workflows-Integration-Tests has no model registry and is not applicable.

Existing [Trend #6027](https://github.com/stranske/Trend_Model_Project/pull/6027) merged as `50d91ce9eadf863d4336ae60523911dc86c37ef4` after its policy and browser repairs passed. [Gate 33938312322](https://github.com/stranske/Trend_Model_Project/actions/runs/33938312322) passed on attempt 2; the retry addressed a dependency-download connection reset. [Browser run 33938311896](https://github.com/stranske/Trend_Model_Project/actions/runs/33938311896) passed. The browser failure was reproduced as a native Arrow 25 mimalloc crash under Python 3.14; the smoke process now uses Arrow's documented system pool and verifies full 20→0→20 transitions. This allocator setting is confined to the smoke process, not a production-wide allocator migration. The two reviewed test files were also installed into the canonical Trend checkout after exact preimage and clean-path checks, preserving its branch head.

[Trend refresh 33939464310](https://github.com/stranske/Workflows/actions/runs/33939464310) succeeded on the same Astra plan and staged head `41c67230d66fe3669ddd36ab92c917f367f42167` on the repaired default branch. Its owner review/seal and required Gate remain pending. The three canaries await campaign completion. Ready merged at 02:32 UTC and the mirror guard released normally. Green owner runs alone are not completion evidence.

Generated candidates remain Maint 68/71-owned. The narrowly verified trigger repair changed only the ready label; no generated head, seal, merge authorization or staging hold was bypassed.

## Unattended engine repairs

1. Corrected invalid launchd XML, loaded the job, and set the actual driver to one unit per fifteen-minute tick.
2. Replaced temporary-session clone symlinks with durable local clones and moved runtime lookups to the installed Orchestrator mirror.
3. Enforced phase stops and fail-closed capacity. A capacity refusal no longer falls through to a permissive routing fallback.
4. Preserved parked questions on the original unit with nonblocking defaults; paginated inbox reads retain late answers. Worker roles still enforce their original research-only boundaries.
5. Required successful execution, no explicit error envelope, a fresh substantive artifact and the dossier verification table before completion. Timeouts, command failures and stale outputs cannot impersonate success.
6. Recovered four false completions, then ran a bounded consistency pass. Corrected the three dossier exports and downstream summaries; [export evidence](https://github.com/stranske/Ready/blob/main/research-program/artifacts/readiness/export-refresh-20260904.md) records packaging checks.
7. Serialized GitHub mirroring and made pending pushes retry even on empty ticks. Added atomic state writes, field-specific updates and inbox serialization so concurrent maintenance cannot overwrite a pause.
8. Made refill IDs unique, made recurring sweep enqueue idempotent within each hour (including completed units), preserved concurrent queue completions, and calculated audit refill thresholds from each last completed filing set. Deliverable-Render and Manager-Mosaic join Doc-Lineage in the durable audit population.
9. Added a nonblocking mirror publication guard for recent, valid Ready sync reviews. It preserves the strict-review base for at most two hours from the observed head, covering a quota reset plus review and long CI, resumes earlier after merge, and retains artifacts locally when the live review lookup is unavailable. A temporary manual hold was released after the guard was installed; local worker progress was preserved.
10. Corrected the travel handout’s stale Trend_Model_Project `phase-3` instruction. GitHub reports `main`; the handout now requires live default-branch discovery. Both Markdown and Word were updated, and all six Word pages were rendered and checked. Active automation prompts contained no stale `phase-3` pin.
11. Preserved Claude conservation until September 6 at 12:00 UTC with automatic expiry. Verified sleep disabled and local executor applications available.

## Validation and operating limits

- Research engine: 22 regression tests passed, including concurrent state writers, pause preservation, capacity refusal, phase stops, stale outputs, refill accounting, exact-head mirror deferral, expiry, and lookup failure before any Git publication.
- Orchestrator: 105 focused tests plus historical migration checks; dispatcher/adapter selftests passed. A copy of the installed database upgraded without rewriting historical profile definitions.
- Workflows: 130 focused Python tests passed, two existing permission-gated cases skipped; template completeness and registry checks passed. Coordination fixes passed 81 contract tests; the ready-label follow-up passes 82, including 404 cleanup and fail-closed 403 behavior.
- Citation-check failures include quoted old links in correction logs, placeholders and access-restricted sources; the count is not a count of uncorrected fabricated claims. Verification tables retain corrections and explicit uncertainty.
- Local inbox polling is verified. Daily cloud backstop existence is verified, but issue-comment webhook delivery was not independently proven.
- Local workers require the machine to remain powered and its desktop sessions available. No new owner approval queue was added.

Backups are under `~/.codex/automations/research-program/maintenance-backups/20260904-astra/`; isolated source worktrees are under `~/.codex/worktrees/astra-rollout/`. The structured [migration evidence index](https://github.com/stranske/Ready/blob/main/research-program/artifacts/readiness/astra-migration-evidence-index.json) records exact run and commit identifiers.

Owner-facing [live status](https://github.com/stranske/Ready/blob/main/research-program/STATUS.md) and existing [Ready #553 inbox](https://github.com/stranske/Ready/issues/553) remain the portable review interface.
