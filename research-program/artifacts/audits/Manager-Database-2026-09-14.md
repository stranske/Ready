# Manager-Database Track D audit publication — 2026-09-14

Unit: `D-audit-Manager-Database--2026-09-14T19-00-22Z`  
Repository: `stranske/Manager-Database`  
Base: `main` / `4523cf50dac3f3fe2ba338b8243e630940c54fd0`

## Result

Published nine verified, deduplicated, agent-ready implementation issues, replenishing the supply that had fallen to two. The source clone was refreshed with `git pull --ff-only`; its pre-existing untracked `uv.lock` was not changed. This publication reused the completed same-day research audit because the current remote SHA was unchanged, then independently re-opened every cited target-repository line and refreshed the open/recently-closed issue and open-PR inventory.

| Issue | Priority | Verified defect |
| --- | --- | --- |
| [#1667](https://github.com/stranske/Manager-Database/issues/1667) | P1 | Configured Streamlit login uses an obsolete pinned authenticator API. |
| [#1668](https://github.com/stranske/Manager-Database/issues/1668) | P1 | Point-in-time history and holdings diffs select different same-day amendment authorities. |
| [#1669](https://github.com/stranske/Manager-Database/issues/1669) | P1 | Content deduplication drops an explicitly supplied second manager association. |
| [#1670](https://github.com/stranske/Manager-Database/issues/1670) | P1 | Scheduled EDGAR indexing can commit a document before a later filing write fails. |
| [#1671](https://github.com/stranske/Manager-Database/issues/1671) | P2 | Dashboard and daily-report SQLite queries hard-code an unsupported manager key. |
| [#1672](https://github.com/stranske/Manager-Database/issues/1672) | P2 | RAG catalog/context extraction silently loses data on the supported SQLite key spelling. |
| [#1673](https://github.com/stranske/Manager-Database/issues/1673) | P2 | The implemented Alerts page is absent from the supported full UI shell. |
| [#1674](https://github.com/stranske/Manager-Database/issues/1674) | P2 | News-spike alerts count duplicate identities that persistence suppresses. |
| [#1675](https://github.com/stranske/Manager-Database/issues/1675) | P2 | The scheduled snapshot job cannot install AWS CLI before its dry-run contract. |

## Verification

- All nine bodies passed the target repository's `.github/scripts/issue_format.py` locally with no advisories.
- GitHub readback confirmed each issue is open with only `bug`, `priority:high|normal`, and `testing`; no auto-dispatch label was applied.
- The format guard explicitly succeeded for #1667–#1673 and #1675. #1674's opened-event check was canceled in its label-event burst, so the supported manual guard check was dispatched and succeeded: [run 34884950733](https://github.com/stranske/Manager-Database/actions/runs/34884950733).
- The live scheduled snapshot failure remains reproduced at the audited SHA: [run 34809590737](https://github.com/stranske/Manager-Database/actions/runs/34809590737).
- The required intake log received nine `repo|body-file|url` entries.

## Risks and non-actions

The audit does not claim a full local-suite run or any production-provider/Postgres execution. Its focused prior evidence at the unchanged SHA remains the basis for the nine issue-specific reproduction and deliberate-break gates. No repository source, branches, PRs, or labels that dispatch implementation work were changed.

The prior attempt could not write the external audit records. Attempt 2 completed that reconciliation at 2026-09-14T19:14:45.381778+00:00; the canonical report, verification log, repository index, root ledger, and body status index now record all nine published issues. Administrative sinks are complete; implementation remains pending.


## 2026-09-14T19:14:45.381778+00:00 — Publication reconciliation, attempt 2

Unit `D-audit-Manager-Database--2026-09-14T19-00-22Z` resumed Phase 5 from its completed publication checkpoint. Current clone and remote main remain `4523cf50dac3f3fe2ba338b8243e630940c54fd0`. All nine existing issues are open, their bodies match the staged files, local and remote-body format validation passes without advisories, and all 37 retained citation contexts match the current source. Each issue has exactly one intake row. All nine remote format guards are successful, including the supported manual replacement for #1674. No duplicate issue or intake row was created.

The prior executor's external-write limitation is resolved in this run: canonical report, verification log, repository index, root audit ledger, and body status index now record publication. This completes the administrative sink; the nine implementation defects remain open. The earlier research-only statuses below are historical and are superseded by this publication record. Runtime evidence is retained from the earlier same-SHA audit; this reconciliation did not rerun the suite or claim production readiness.

| Finding | Issue | Status | Format guard |
| --- | --- | --- | --- |
| F01 | [#1667](https://github.com/stranske/Manager-Database/issues/1667) — Restore configured login with the pinned authenticator API | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884639893) |
| F02 | [#1668](https://github.com/stranske/Manager-Database/issues/1668) — Align point-in-time same-day amendment authority with holdings diffs | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884642152) |
| F03 | [#1669](https://github.com/stranske/Manager-Database/issues/1669) — Preserve manager associations when document content is deduplicated | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884644119) |
| F04 | [#1670](https://github.com/stranske/Manager-Database/issues/1670) — Make scheduled EDGAR indexing atomic with filing writes | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884646787) |
| F05 | [#1671](https://github.com/stranske/Manager-Database/issues/1671) — Resolve SQLite manager keys across dashboard and daily report queries | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884648869) |
| F06 | [#1672](https://github.com/stranske/Manager-Database/issues/1672) — Resolve SQLite manager identity in RAG context extraction | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884651189) |
| F07 | [#1673](https://github.com/stranske/Manager-Database/issues/1673) — Expose existing Alerts management through the full UI shell | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884653399) |
| F08 | [#1674](https://github.com/stranske/Manager-Database/issues/1674) — Count only persisted news identities in spike alerts | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884950733) |
| F09 | [#1675](https://github.com/stranske/Manager-Database/issues/1675) — Repair AWS CLI installation in the scheduled snapshot job | Filed; implementation pending | [success](https://github.com/stranske/Manager-Database/actions/runs/34884656369) |

Evidence: [LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Manager-Database-2026-09-14-assets/resume-verification.json, resume-guards.json, resume-issues.json, and resume-format-runs.json. Next ledger action: record implementation PRs, merges, and acceptance-gate verification.
