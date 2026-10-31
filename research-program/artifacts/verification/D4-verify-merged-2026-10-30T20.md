# D4 verify merged — 2026-10-30T20

**Window:** merges since `2026-10-29T08:53:48Z` (36 h before run). **Fleet:** `SUPPORTED_REPOS` from `handoff.sh`, excluding Orchestrator. **Cap:** 20 PRs (oldest issue-linked first). **Offload:** GitHub writes (issues, comments, reopen, follow-up filing) not performed; follow-up column records intent only.

**Discovery:** 12 non-chore merges in the window close or reference an issue via `closingIssuesReferences`, `Closes`/`Refs #N`, or autopilot source `#N` in PR metadata; all 12 verified this run (under cap). **Additional merges** in window were template-sync, release chores, or maint/verifier work without an issue link (skipped per scope).

**Skipped without verification (chore / no issue link):** `chore: sync workflow templates` (fleet batch 2026-10-30T05:33–05:35Z), `chore(main): release` on Workflows, Counter_Risk `#1213` (Python 3.13 validator — no `#issue` in metadata), Workflows `#4328–4333`, `#4341–4342`, `#4345–4347`, `#4351`, `#4353`, `#4356`, trip-planner `#1955`, learning-management-system `#815`, and similar unlinked product merges.

**Confidence:** High on squash-diff reads for all 12 rows. Medium on Counter_Risk coverage autopilot AC2 (relies on PR-body shortfall disclosures where hosted Gate deltas were not re-measured locally). High that skipped unlinked PRs correctly excluded.

## Results

| Repo | PR | Issue | Verdict | Unmet / deferred criteria | Follow-up filed |
|------|-----|-------|---------|---------------------------|-----------------|
| Counter_Risk | [#1221](https://github.com/stranske/Counter_Risk/pull/1221) | [#1219](https://github.com/stranske/Counter_Risk/issues/1219) | PARTIAL | Squash `eb0ce674`: substantive tests + explained `web_demo.py` fix. **Unmet / open:** ~180-unit uncovered reduction not shown on hosted Gate; body cites ~175 short; issue **OPEN**. | No (intent: monitor #1219 post-merge coverage; offload) |
| Counter_Risk | [#1216](https://github.com/stranske/Counter_Risk/pull/1216) | [#1215](https://github.com/stranske/Counter_Risk/issues/1215) | PARTIAL | Squash `e463bd79`: manifest/reconciliation tests + targeted prod fixes in diff. Post-merge coverage disposition still open; issue **OPEN**. | No (offload) |
| Counter_Risk | [#1220](https://github.com/stranske/Counter_Risk/pull/1220) | [#1218](https://github.com/stranske/Counter_Risk/issues/1218) | PARTIAL | Squash `856704af`: NISA/rollup coverage tests in diff; PR keeps hosted comparison open; issue **OPEN**. | No (offload) |
| Workflows | [#4327](https://github.com/stranske/Workflows/pull/4327) | [#4326](https://github.com/stranske/Workflows/issues/4326) | VERIFIED | Templates pass only `secrets.ACTIONS_BOT_PAT`; gate tests in `tests/workflows/test_integration_template_secrets_in_if.py` assert no whole-secrets `toJSON`. | — |
| Counter_Risk | [#1217](https://github.com/stranske/Counter_Risk/pull/1217) | [#1214](https://github.com/stranske/Counter_Risk/issues/1214) | VERIFIED | Squash `cfc949a3`: pipeline/CLI tests + documented prod fix in `src/counter_risk/pipeline/run.py`; closes #1214. | — |
| Workflows | [#4336](https://github.com/stranske/Workflows/pull/4336) | [#4326](https://github.com/stranske/Workflows/issues/4326) | VERIFIED | Sparse-checkout includes retry-helper siblings; `test_integration_template_script_closure.py` guards module closure. | — |
| Workflows | [#4340](https://github.com/stranske/Workflows/pull/4340) | [#4338](https://github.com/stranske/Workflows/issues/4338) | VERIFIED | `sync_integration_coverage_omit.py` + regression tests per issue #4338 AC; closes integration coverage omit failure class. | — |
| Manager-Database | [#1873](https://github.com/stranske/Manager-Database/pull/1873) | [#1872](https://github.com/stranske/Manager-Database/issues/1872) | VERIFIED | Test-only diff: `tests/test_resolve_mypy_pin.py` aligns with synced tool default (unblocks #1872 sync). | — |
| Trend_Model_Project | [#6182](https://github.com/stranske/Trend_Model_Project/pull/6182) | [#6180](https://github.com/stranske/Trend_Model_Project/issues/6180) | VERIFIED | Tests read synced runtime pins instead of hard-coded 3.12 (unblocks #6180 sync). | — |
| Counter_Risk | [#1223](https://github.com/stranske/Counter_Risk/pull/1223) | [#1189](https://github.com/stranske/Counter_Risk/issues/1189) | PARTIAL | Squash `193e3346`: provenance test uses minimal fixtures + mutation evidence under `docs/evidence/issue-1189/`. **Unmet:** Health 85 seven-day Gate p50 ≤10 min (#1189 **OPEN**). | No (monitoring; offload) |
| Trend_Model_Project | [#6181](https://github.com/stranske/Trend_Model_Project/pull/6181) | [#6124](https://github.com/stranske/Trend_Model_Project/issues/6124) | PARTIAL | Squash `d3284e5a`: legacy-surface/cli gate tests preserved with reduced scan/install work. **Unmet:** seven-day Health 85 p50 (#6124 **OPEN**). | No (monitoring; offload) |
| Manager-Database | [#1874](https://github.com/stranske/Manager-Database/pull/1874) | [#1830](https://github.com/stranske/Manager-Database/issues/1830) | PARTIAL | Squash `6f728a47`: ranked activism/EDGAR tests land with real asserts. **Unmet:** ~180-unit coverage chunk target; body states shortfall though issue closed. | No (offload) |

**Summary:** 12 PRs verified. **VERIFIED:** 7. **PARTIAL:** 5. **NOT IMPLEMENTED:** 0. **Belt ledger-only merges:** none. **Workflows#3391 belt defect:** none observed. **Reproduction blocks:** none on linked issues. **Follow-ups filed:** 0 (offload prohibits GitHub writes).

## Notes

- **Deferred from prior run (`D4-verify-merged-2026-10-29T20`):** `Counter_Risk#1221`, `#1216`, `#1220`, `#1217` were verified this run (ledger cleared for those four).
- **Workflows #4326** had two follow-up merges (`#4327`, `#4336`); both extend the integration-template fix with distinct, tested regressions — not belt-only bookkeeping.
- **Perf issues #1189 / #6124:** squash diffs deliver the named pytest optimizations and non-vacuous guards; trailing-seven-day p50 remains the honest deferral (same pattern as `#1207` on the prior D4 run).
- **Issue linkage rule:** PRs that only reference other PR numbers (e.g. sync fixes citing `#4341`) were excluded — they do not reference an issue in the sense of this unit.

## Ledger

Next run: include merges after `2026-10-30T20:09:01Z` (`Manager-Database#1874`). Re-evaluate unlinked Workflows verifier/sync merges if issue links appear in body or `closingIssuesReferences`.
