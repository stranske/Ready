# Verification and complete disposition log — 2026-09-14

Unit D-audit-Manager-Database--2026-09-14T06-49-50Z; baseline 4523cf50dac3f3fe2ba338b8243e630940c54fd0; reconciled 2026-09-14T08:36:27.770705+00:00. All source changes forbidden in this research role. Status 'deferred with reason' below means a verified implementation task is staged awaiting a publication lane, not fixed.

- F01: deferred with reason — Restore configured login with the pinned authenticator API; verified body `01-restore-configured-login-with-the-pinned-authenticator-api.md`; publication prohibited in this worker. Labels verified: bug, priority:high, testing.
- F02: deferred with reason — Align point-in-time same-day amendment authority with holdings diffs; verified body `02-align-point-in-time-same-day-amendment-authority-with-holdings-diffs.md`; publication prohibited in this worker. Labels verified: bug, priority:high, testing.
- F03: deferred with reason — Preserve manager associations when document content is deduplicated; verified body `03-preserve-manager-associations-when-document-content-is-deduplicated.md`; publication prohibited in this worker. Labels verified: bug, priority:high, testing.
- F04: deferred with reason — Make scheduled EDGAR indexing atomic with filing writes; verified body `04-make-scheduled-edgar-indexing-atomic-with-filing-writes.md`; publication prohibited in this worker. Labels verified: bug, priority:high, testing.
- F05: deferred with reason — Resolve SQLite manager keys across dashboard and daily report queries; verified body `05-resolve-sqlite-manager-keys-across-dashboard-and-daily-report-queries.md`; publication prohibited in this worker. Labels verified: bug, priority:normal, testing.
- F06: deferred with reason — Resolve SQLite manager identity in RAG context extraction; verified body `06-resolve-sqlite-manager-identity-in-rag-context-extraction.md`; publication prohibited in this worker. Labels verified: bug, priority:normal, testing.
- F07: deferred with reason — Expose existing Alerts management through the full UI shell; verified body `07-expose-existing-alerts-management-through-the-full-ui-shell.md`; publication prohibited in this worker. Labels verified: bug, priority:normal, testing.
- F08: deferred with reason — Count only persisted news identities in spike alerts; verified body `08-count-only-persisted-news-identities-in-spike-alerts.md`; publication prohibited in this worker. Labels verified: bug, priority:normal, testing.
- F09: deferred with reason — Repair AWS CLI installation in the scheduled snapshot job; verified body `09-repair-aws-cli-installation-in-the-scheduled-snapshot-job.md`; publication prohibited in this worker. Labels verified: bug, priority:normal, testing.

## Raw review reconciliation

- ETL-1 → F02; ETL-2 → F03; ETL-3 → F04; ETL-4 → F08.
- ETL-5 OpenFIGI negative caching → explicitly optional roadmap: repeated misses may waste calls, but a durable negative-cache lifetime and present operational impact need measurement. Do not indefinitely suppress newly mapped identifiers.
- API/UI F1 → F07; F2, F3, F4, F5 → consolidated F05; F6 → F06. Daily Report activism join is also included in F05 by direct source inspection.
- Parent auth reproduction → F01; parent scheduled-run investigation → F09.
- Four-model UX suggestions → exact adjudications in UX_REVIEW; unsupported failures declined, polish optional. No panel-only claim became an issue.
- Existing #1653 → deferred to already-open owner. #1664 → its existing test-only news-stream branch excluded. Previous fixed #1647–1652 → declined as duplicates where fixed; the surviving consumers above have separate cited sites.
- Larger OCR, shared evidence identity/static packet, internal hosting, and restore drill → deferred roadmap with endpoint/IT evidence gates in PLATFORM_TEST_BRIEF. Existing vector search, portfolio view, and RAG are acknowledged present.

## Evidence retained

`verify-etl.json`: four independent real-function reproductions; `dialect-results.json`: identical-data manager-key comparison; `auth-repro.json` and `pinned-auth-repro.log`: real pinned dependency failure; `pinned-targeted-tests.log`: 133 pass/1 skip, exit 0; `format-validation.json`: 9 pass without advisory; `citation-audit.json`: 37 verified citations. Current CI successful; scheduled snapshot failure log retained. Test collection 1651, not full-suite execution.

Cursor API offload succeeded. Codex ETL wrapper returned exit 1/OFFLOAD_INCOMPLETE despite a nonempty report; its findings were used only after parent reproduction and direct source verification, never as a successful wrapper claim. Raw offload output and failure traces are not repo defects. Reproducers bypassed external network/Prefect scheduling with synthetic inputs and real target functions. No production services were altered.

All nine bodies use repository-relative evidence paths, concrete targets, measurable test gates, deliberate-break requirements, and issue-specific scaffold exclusions. Local source-owned validator executed with target clone path resolution. No GitHub issue, issue intake row, PR, or remote format-guard result was created or claimed.

Final main SHA equals audit SHA. No tracked changes; pre-existing untracked uv.lock preserved. Scope and all original candidate sequences reconciled. Next: authorized publication lane refreshes dedup, then implementation lanes run the acceptance gates.
