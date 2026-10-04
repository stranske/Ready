# D4 implementation verification — 2026-10-01T04

**Window:** merged ≥ 2026-09-29T16:14:00Z (36h before run start)  
**Scope:** Issue-linked merges not already ledgered in `D4-verify-merged-2026-09-30T04`. Excluded `stranske/Orchestrator`, template-sync / release / fleet LLM pin chores (see below). Verdicts from squash diffs (`gh pr diff` via `with-gh-auth.sh`) and linked issue acceptance criteria. No linked issue carried a `Reproduction:` block in this batch.

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| Workflows | 3625 | 3620 | PARTIAL | Reporter delayed-recovery path in `keepalive_reporter_applicability.js` + expanded JS tests (`efcae8e`). **Unmet:** #3620 tri-suite `node --test` deliberate-break evidence; authority-state / loop tasks not in this squash diff. | [#3656](https://github.com/stranske/Workflows/issues/3656) |
| Manager-Database | 1737 | 1736 | VERIFIED | Replaced `quay.io/minio/minio` with digest-pinned `docker.io/shuomura/minio` in `ci.yml`, `docker-compose.yml`, `Manager-Intel-Platform.md` + explanatory CI comment (`9ae40b10`). | — |
| Workflows | 3628 | 3612 | PARTIAL | `keepalive_authority_state.js` + authority-state unit tests (`89bc39dc`). **Unmet:** #3612 AC consumer sync PR URL / thread disposition. | [#3657](https://github.com/stranske/Workflows/issues/3657) |
| Workflows | 3635 | 3630 | PARTIAL | `running_owner_attempt`, ledger revalidation, `superseded` reporter path + adversarial JS tests (`ff1fc18c`). **Unmet:** deliberate-break transcript for named `same-generation recovery` regression. | [#3658](https://github.com/stranske/Workflows/issues/3658) |
| Workflows | 3638 | 3631 | VERIFIED | `reconcileFailedAuthorityAttempt` refresh/lineage + extensive `keepalive-authority-state` tests (`1d2fd28b`). | — |
| Workflows | 3636 | 3632 | VERIFIED | `scripts/state_fingerprint.py` in authority-release sparse checkout for keepalive + `agents-81-gate-followups` template; `test_gate_followups_authority_sparse_checkout.py` (`029058f0`). | — |
| Workflows | 3639 | 3634 | VERIFIED | `keepalive_loop.js` recovery-owner guard + `test_keepalive_loop_rate_limit.py` attempt-not-current case (`e2923c81`). | — |
| trip-planner | 1876 | 1837 | PARTIAL | Stops inventing `compliance_score`; null-safe TPP client + packet/tests (`9041478b`). **Unmet:** budget cap, vendor cost lines, print blank pages, traveller/itinerary fields (#1837). | [#1877](https://github.com/stranske/trip-planner/issues/1877) |
| Workflows | 3642 | 3637 | PARTIAL | `run-contract-v1.md` Pension-Data section + `tests/docs/test_run_contract_doc_pension_data.py` + belt ledger (`d4bae1de`). **Unmet:** Pension-Data `test_contract_doc_drift` gate run not in squash diff. | [#3659](https://github.com/stranske/Workflows/issues/3659) |
| Workflows | 3644 | 3643 | PARTIAL | Challenge-pending preservation in `keepalive_loop.js` + named Node regression (`6eaf64bc`). **Unmet:** deliberate-break transcript per #3643 AC. | [#3661](https://github.com/stranske/Workflows/issues/3661) |
| Workflows | 3647 | 3645 | PARTIAL | `keepalive-dispatch/v2 ordinary pr=` binding, reporter plumbing, expanded Node/Python delivery tests (`4df2e27f`). **Unmet:** deliberate-break skip/continue transcript. | [#3662](https://github.com/stranske/Workflows/issues/3662) |
| Workflows | 3648 | 3646 | VERIFIED | Three `gate-fork-status-publication.js` trust-boundary fixes mirrored to template + expanded `test_gate_fork_status_publication.py` (`6e33605f`). | — |
| Manager-Database | 1741 | 1739 | VERIFIED | `readProxyProperty` in synced wrapper + matching `tests/fixtures/github-rate-limited-wrapper.js` (`5af310dd`). | — |
| Inv-Man-Intake | 998 | 997 | VERIFIED | URI-scheme + repeated-separator rejection in `report_spec.py` + parametrized tests (`c202bf01`). | — |

**Result:** 7 VERIFIED, 7 PARTIAL, 0 NOT IMPLEMENTED, 0 belt-only ledger merges ( #3642 includes ledger bookkeeping plus substantive doc/test changes).  
**Follow-ups filed:** 7 (see table).  
**Out of scope (not tabled):** `Counter_Risk` #1132 — D3 red-main black format fix with no closing issue reference; fleet LLM pin chores (`Counter_Risk` #1134, `Manager-Database` #1740, `Portable-Alpha-Extension-Model` #2326, `Trend_Model_Project` #6071, and similar) skipped as dependency chores; `Workflows` #3629 release chore.

Evidence: `artifacts/verification/evidence/D4-verify-merged-2026-10-01T04/`

**Confidence:** High on VERIFIED rows — squash diffs contain production changes and regression tests that directly map to issue tasks (gate fork #3646, recovery owner #3634, MinIO pin #1736, report-spec #997, wrapper fixture #1739). High on PARTIAL rows — real code landed; gaps are deliberate-break transcripts, cross-repo pytest gates, consumer-sync URLs, or (#1837) a narrow slice of a multi-symptom audit. **What would change my mind:** deliberate-break or Pension-Data pytest transcripts only in PR comments (not squash) would upgrade affected PARTIAL rows; live CI green on #1736 without `test_readiness_smoke` in diff would not by itself upgrade if that test were still failing on tip (not re-run here).
