# D4-verify-merged-2026-09-16T02

**Window:** merged ≥ 2026-09-14T14:28:38Z (36h before run start)  
**Repos:** 15 lane fleet (`SUPPORTED_REPOS`, excluding Orchestrator)  
**Cap:** 20 PRs (13 verified this run; 17 template-sync/dependency/release chores skipped; 18 PRs from prior unit D4-verify-merged-2026-09-15T02 already adjudicated in-window)

## Summary

| Metric | Count |
|--------|------:|
| PRs verified | 13 |
| VERIFIED | 7 |
| PARTIAL | 5 |
| NOT IMPLEMENTED | 1 |
| Follow-ups filed | 5 |
| Rate-limit stop | No |

## Results

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| Workflows | [#3442](https://github.com/stranske/Workflows/pull/3442) | [#2819](https://github.com/stranske/Workflows/issues/2819) | PARTIAL | maint-77→maint-78 auto-dispatch absent; catalog auto-candidate refresh not in diff; AC "new model auto-dispatches pilot" unmet | [#3457](https://github.com/stranske/Workflows/issues/3457) |
| Ready | [#570](https://github.com/stranske/Ready/pull/570) | [#557](https://github.com/stranske/Ready/issues/557) | PARTIAL | No deliberate-break removing `force-exclude` on explicit-path Black invocation | [#575](https://github.com/stranske/Ready/issues/575) |
| Ready | [#574](https://github.com/stranske/Ready/pull/574) | [#554](https://github.com/stranske/Ready/issues/554) | PARTIAL | PKCS#8/ENCRYPTED key headers, shared scanner/exporter header set, `prepare_publication.py` CI wiring | [#576](https://github.com/stranske/Ready/issues/576) |
| Counter_Risk | [#1060](https://github.com/stranske/Counter_Risk/pull/1060) | [#1058](https://github.com/stranske/Counter_Risk/issues/1058) | NOT IMPLEMENTED | Regression in `test_cprs_ch_workbook_total.py` not `test_reconciliation.py`; named cov gate + deliberate-break evidence absent | [#1073](https://github.com/stranske/Counter_Risk/issues/1073) |
| Manager-Database | [#1679](https://github.com/stranske/Manager-Database/pull/1679) | [#1670](https://github.com/stranske/Manager-Database/issues/1670) | VERIFIED | — | — |
| Manager-Database | [#1676](https://github.com/stranske/Manager-Database/pull/1676) | [#1667](https://github.com/stranske/Manager-Database/issues/1667) | VERIFIED | — | — |
| Manager-Database | [#1678](https://github.com/stranske/Manager-Database/pull/1678) | [#1669](https://github.com/stranske/Manager-Database/issues/1669) | PARTIAL | Postgres acceptance leg skipped unless `DOCUMENT_TEST_POSTGRES_URL` set | [#1682](https://github.com/stranske/Manager-Database/issues/1682) |
| Deliverable-Render | [#18](https://github.com/stranske/Deliverable-Render/pull/18) | [#3](https://github.com/stranske/Deliverable-Render/issues/3) | VERIFIED | — | — |
| Workflows | [#3454](https://github.com/stranske/Workflows/pull/3454) | [#3453](https://github.com/stranske/Workflows/issues/3453) | VERIFIED | — | — |
| Manager-Database | [#1681](https://github.com/stranske/Manager-Database/pull/1681) | [#1671](https://github.com/stranske/Manager-Database/issues/1671) | VERIFIED | — | — |
| Workflows | [#3456](https://github.com/stranske/Workflows/pull/3456) | [#3346](https://github.com/stranske/Workflows/issues/3346) | VERIFIED | — | — |
| Doc-Lineage | [#25](https://github.com/stranske/Doc-Lineage/pull/25) | [#2](https://github.com/stranske/Doc-Lineage/issues/2) | VERIFIED | — | — |
| Doc-Lineage | [#29](https://github.com/stranske/Doc-Lineage/pull/29) | [#4](https://github.com/stranske/Doc-Lineage/issues/4) | VERIFIED | — | — |

## Skipped (not verified)

| Reason | Count | Examples |
|--------|------:|----------|
| Already verified in D4-verify-merged-2026-09-15T02 | 18 | Workflows #3432–#3451, Ready #569/#571, Counter_Risk #1069/#1071, … |
| Template-sync chore | 8 | Pension-Data #899, Inv-Man-Intake #970, Doc-Lineage #26, … |
| Release/dependency chore | 0 | — |

## Notable findings

1. **Counter_Risk #1060** — behavioral fix in `src/counter_risk/pipeline/run.py` is real, but the issue's **named gate file** (`tests/pipeline/test_reconciliation.py`) was never touched. Classic scaffold-adjacent completion: tests exist, wrong contract.
2. **Workflows #3442** — corpus-evidence hardening is substantive (87/87 local gate pass at merge SHA `9a16cbf4`); closing #2819 overstates delivery because maint-77/78 auto-dispatch (design move 1) is still manual-only.
3. **Ready #574** — repairs the allowlist-location gap flagged as PARTIAL for #569, but adversarial PKCS#8 and preparation-workflow items from #554 remain open.
4. **Doc-Lineage #25/#29** — both include deliberate-break gates and non-vacuous behavioral tests; strongest deliveries this window.

## Evidence

Squash diffs, issue JSON, and follow-up bodies: `artifacts/verification/evidence/D4-verify-merged-2026-09-16T02/`

Local gate run: Workflows #3442 merge SHA — `pytest tests/tools/test_harvest_verifier_corpus.py tests/tools/test_prepare_model_promotion.py tests/workflows/test_model_eval_pilot_workflow.py -q` → **87 passed**.
