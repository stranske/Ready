# Manager-Database audit — 2026-09-14

Unit: D-audit-Manager-Database--2026-09-14T06-49-50Z  
Completed research: 2026-09-14T08:36:27.770705+00:00  
Baseline: stranske/Manager-Database main at `4523cf50dac3f3fe2ba338b8243e630940c54fd0`, rechecked against remote main at close.

Nine verified findings are staged: four P1 data-integrity or access defects and five P2 correctness, navigation, or operations defects. No issues were filed and no repository source was changed. The Research Program's explicit research-only rule overrides the brief's filing instruction; this run therefore does **not** replenish the live GitHub implementation queue.

| Finding | Priority | Staged implementation body |
|---|---|---|
| F01 | P1 | [Restore configured login with the pinned authenticator API]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/01-restore-configured-login-with-the-pinned-authenticator-api.md) |
| F02 | P1 | [Align point-in-time same-day amendment authority with holdings diffs]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/02-align-point-in-time-same-day-amendment-authority-with-holdings-diffs.md) |
| F03 | P1 | [Preserve manager associations when document content is deduplicated]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/03-preserve-manager-associations-when-document-content-is-deduplicated.md) |
| F04 | P1 | [Make scheduled EDGAR indexing atomic with filing writes]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/04-make-scheduled-edgar-indexing-atomic-with-filing-writes.md) |
| F05 | P2 | [Resolve SQLite manager keys across dashboard and daily report queries]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/05-resolve-sqlite-manager-keys-across-dashboard-and-daily-report-queries.md) |
| F06 | P2 | [Resolve SQLite manager identity in RAG context extraction]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/06-resolve-sqlite-manager-identity-in-rag-context-extraction.md) |
| F07 | P2 | [Expose existing Alerts management through the full UI shell]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/07-expose-existing-alerts-management-through-the-full-ui-shell.md) |
| F08 | P2 | [Count only persisted news identities in spike alerts]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/08-count-only-persisted-news-identities-in-spike-alerts.md) |
| F09 | P2 | [Repair AWS CLI installation in the scheduled snapshot job]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-issue-bodies/09-repair-aws-cli-installation-in-the-scheduled-snapshot-job.md) |

## Evidence and priorities

Fix configured login and the three integrity boundaries first. With locked Streamlit 1.60.0 and authenticator 0.4.2, actual AppTest execution fails before the login form with Hasher TypeError. Offline fault injections demonstrate: a same-day original wins in point-in-time history while the diff selector chooses its amendment; deduplicated text assigned to two managers retains only the first association; and scheduled EDGAR filing-write failure leaves one indexed document with zero filings.

Matched SQLite fixtures differing only in managers.id versus managers.manager_id show empty dashboard/QC/news results, a daily-report JOIN error, and lost RAG entity context. Two duplicate news candidates yield one stored row but an alert count of two. The full UI renders five navigation entries while its implemented Alerts management page is absent. The [scheduled Database Snapshot run](https://github.com/stranske/Manager-Database/actions/runs/34809590737) fails before dry-run validation because apt cannot install awscli, despite [successful same-head CI](https://github.com/stranske/Manager-Database/actions/runs/34796000355).

## Validation and limits

- 1,651 tests collected. Focused existing tests under pinned Streamlit: **133 passed, 1 skipped**, exit 0. This is a targeted suite, not a claim of full local-suite success.
- Nine issue bodies pass the source-owned AGENT_ISSUE_FORMAT validator without advisories; all 37 cited lines were opened and checked. Deliberate-break gates are implementation requirements, not tests claimed to have been written during this audit.
- Synthetic browser journeys covered Dashboard, portfolio/history, Daily Report, Search, Upload rendering, Research gating, and configured-login failure. Screenshots used local Streamlit 1.63; the decisive login reproduction and focused tests were independently repeated on the 1.60 pin. The initial 1.63 navigation-test failure was excluded as environment skew.
- No live production Postgres, authenticated provider, production backup/restore, upload persistence, or Research submission was exercised. Panel suggestions about these unperformed flows were rejected as evidence of defects.

## Eight-dimension coverage

| Dimension | Result |
|---|---|
| Code quality | F01–F04 and F08: concrete API and data-boundary failures. |
| Duplication | Shared manager-key helper is bypassed in UI/RAG (F05/F06); scheduled ingestion forks from generic atomic ingestion (F04). |
| Functionality and wiring | F07 missing navigation; F05/F06 query contracts. |
| Observed UX | Browser captures plus four-model panel; configured auth and Alerts reachability verified. Product readiness gate remains failed. |
| Public field | Six primary-source references; existing pgvector/RAG capability is acknowledged rather than proposed again. |
| Opportunities | Local OCR with page provenance and a linked static manager-review packet; separate roadmap, not claimed completed. |
| Tooling | Actual-dependency auth gate, paired SQLite fixture matrix, and isolated restore drill proposed. |
| Automation | Current remote checks and local configurations inventoried; F09 belongs to this repo, shared sync workflows remain Workflows-owned. |

## Reconciliation and next action

Fresh open inventory contains #1653 (Postgres similarity bootstrap), #1664 (dashboard news coverage), and two informational trackers, with no open PRs at capture. F05 excludes #1664's already-covered news-stream branch; fixed upload, alert-selector, and activism-API cases from September 10 were not refiled. Older closed delivery contracts are context for the newly reproduced residual cases, not evidence of unfinished prior work by themselves.

An authorized publication lane can review the nine bodies, refresh dedup against current GitHub state, then file them. No intake-log URLs or format-guard run is claimed because publication did not occur. See the canonical [verification log]([LOCAL_HOME]/Library/CloudStorage/Dropbox/Learning/Code/Audits/Manager-Database/2026-09-14-verification-log.md), [UX review]([LOCAL_HOME]/Library/CloudStorage/Dropbox/Learning/Code/Audits/Manager-Database/2026-09-14-UX_REVIEW.md), and [platform/roadmap brief]([LOCAL_HOME]/Library/CloudStorage/Dropbox/Learning/Code/Audits/Manager-Database/2026-09-14-PLATFORM_TEST_BRIEF.md). Evidence and reproducers are in [audit assets]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-assets); durable records are also stored under Code/Audits/Manager-Database.
