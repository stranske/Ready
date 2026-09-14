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

The required external `Code/Audits` index/ledger reconciliation was attempted and rejected by the workspace policy because that Dropbox path is outside the allowed writable roots. The existing canonical research report remains intact; this required OUT report and the unit checkpoint retain the publication record. This is the only incomplete administrative sink.
