# D4 implementation verification — 2026-09-20T20

**Window:** merged ≥ 2026-09-19T09:14:47Z (36h before run start)  
**Scope:** 20 oldest eligible issue-linked PRs not verified in D4-2026-09-20T03 (that run consumed the prior 20). Template-sync, dependency/release chores, and `stranske/Orchestrator` excluded from discovery; one dependency refresh (#3479) reached the batch via title filter and is marked EXCLUDED below. Verdicts are based on squash diffs and linked issue acceptance criteria; Gate CI conclusions confirm named tests ran.

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| Workflows | #3471 | #3470 | PARTIAL | `scripts/runner_lib/core.py` refuses fallback-only dispatch reservations; `tests/scripts/test_runner_lib.py` adds `test_auto_dispatch_requires_primary_storage` and related coverage; docs updated. Gate succeeded. No executed deliberate-break fail→restore evidence for #3470's named gate. | #3494 |
| Manager-Database | #1687 | #1653 | VERIFIED | PostgreSQL DDL branch in `etl/manager_similarity_flow.py`; discriminating mock-connection tests in `tests/test_manager_similarity_flow.py`; deliberate-break marker and executed evidence in PR body. | — |
| Manager-Database | #1688 | #1685 | VERIFIED | Per-case `pg_conn` fixture isolation in `tests/test_alert_postgres_integration.py` fixes cross-test delivery leakage causing `test_scheduled_edgar_alert_transaction[success]` failure; PR documents parent/main CI failure and hosted postgres acceptance. No production code change (test harness repair only). | — |
| learning-management-system | #679 | #667 | VERIFIED | `create_attempt` validation in `src/lms/evidence/repository.py`; parametrized rejection tests; deliberate-break tested and reverted per PR body. | — |
| learning-management-system | #680 | #668 | PARTIAL | `create_evidence_record` domain validation and substantive session-poisoning tests in diff. Gate succeeded. No executed deliberate-break evidence despite #668 requiring it. | #700 |
| learning-management-system | #681 | #669 | VERIFIED | Enum validation in `src/lms/sources/repository.py`; tests assert allowed sets; PR records deliberate disable→fail→restore. | — |
| learning-management-system | #682 | #670 | VERIFIED | `set_item_tier` retention-tier guard in `src/lms/maintenance/service.py`; tests cover invalid tiers; PR records guard removal failure. | — |
| learning-management-system | #683 | #671 | VERIFIED | Finite `[0,1]` mastery threshold guard in `src/lms/learners/repository.py`; 12-case regression suite; deliberate-break evidence in PR body. | — |
| learning-management-system | #684 | #672 | VERIFIED | Non-negative capacity guards in `src/lms/maintenance/budget.py`; targeted tests; deliberate-break evidence in PR body. | — |
| learning-management-system | #685 | #673 | VERIFIED | Rubric threshold ordering validation in `src/lms/feedback/scoring.py`; 13 invalid-input cases; deliberate-break evidence in PR body. | — |
| Workflows | #3476 | #1836 | VERIFIED | `RepoVariableRunnerStorage.write_record` propagates HTTP 401/403 instead of silent skip; `test_repo_variable_denied_write_cannot_report_success` discriminates reserve/complete paths. Campaign reference only; substantive infra fix with tests. | — |
| Manager-Database | #1689 | #1672 | VERIFIED | `resolve_manager_id_column` wired through `chains/rag_search.py`; id-schema matrix tests in `tests/test_rag_search_chain.py`; deliberate-break gate recorded in PR body. | — |
| Fine-Art-Archive | #730 | — | VERIFIED | Test-only: `monkeypatch` isolates `MASTER_FACTS_CACHE` / `_MASTER_FACTS_*` in `tests/test_judgement_surfaces.py` to fix order-dependent cache pollution (sync-campaign unblock for #729). No production change; PR documents reproduction. References Workflows#1836, not a fleet issue. | — |
| Workflows | #3477 | #1836 | VERIFIED | Keepalive signed-challenge reservation before dispatch in `scripts/keepalive_lib/`; new tests `test_signed_challenge_reserves_own_attempt_and_records_completion`, invalid-authority and storage-failure cases. Gate succeeded. | — |
| Counter_Risk | #1074 | #1063 | VERIFIED | Malformed maturity totals raise in `src/counter_risk/parsers/exposure_maturity_schedule.py`; `test_invalid_nonblank_total_raises` with workbook fixtures; deliberate-break evidence in PR body. | — |
| Counter_Risk | #1075 | #1064 | VERIFIED | Delta facts serialized into guarded provider messages in `src/counter_risk/chat/session.py`; `test_delta_facts_reach_langchain_invoke` intercepts real transport; deliberate-break evidence in PR body. | — |
| Workflows | #3479 | #1836 | EXCLUDED | Dependency chore: vendored `glob` security refresh across consumer template trees (82 files, no tests). Out of D4 scope per template-sync/dependency skip rule; not scored as NOT IMPLEMENTED. | — |
| Workflows | #3480 | #1836 | VERIFIED | Gate install step identifies project from pip install report (`consumer-template-gate` / `gate` workflows); `test_gate_removes_reported_project_or_fails_closed` added. Fixes Deliverable-Render#20 class of missing-deps collection failures. | — |
| Counter_Risk | #1076 | #1065 | VERIFIED | `src/counter_risk/pipeline/data_quality.py` distinguishes skipped link refresh from generated distribution; `test_skipped_refresh_reports_existing_distribution` with real decks; deliberate-break evidence in PR body. | — |
| Deliverable-Render | #19 | #4 | VERIFIED | `src/deliverable_render/probe/build_probe.py` emits self-contained offline capability probe; `tests/test_probe_offline_and_minimal.py` asserts no external network on load, privacy-safe summary, WASM-fail path; deliberate remote-script break/revert recorded. | — |

**Result:** 17 VERIFIED, 2 PARTIAL, 0 NOT IMPLEMENTED, 1 EXCLUDED (dependency chore).  
**Follow-ups filed:** Workflows #3494, learning-management-system #700.  
**Deferred:** 26 additional eligible PRs remain in the 36h window for the next D4 pass (oldest unverified after this batch).
