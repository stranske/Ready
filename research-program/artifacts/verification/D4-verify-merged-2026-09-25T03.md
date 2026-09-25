# D4 implementation verification — 2026-09-25T03

**Window:** merged ≥ 2026-09-23T15:34:16Z (36h before run start)  
**Scope:** 20 oldest eligible issue-linked PRs not verified in prior D4 checkpoints (`D4-verify-merged-2026-09-24T03` and earlier). Template-sync, dependency/release chores, and `stranske/Orchestrator` excluded. Verdicts from squash diffs (`gh pr diff`) and linked issue acceptance criteria; PR bodies used for deliberate-break transcripts and gate tables.

**Method note:** `gh` used with token from git credential helper. trip-planner #1860 `Reproduction:` curl requires an authenticated session; local `TestClient` returned 401 without cookies — reproduction not re-run verbatim; named API/UI gates in the squash diff and PR gate table were used instead.

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| Travel-Plan-Permission | #1623 | #1593 | VERIFIED | `canonical_intake.py` collision guard + `tests/python/test_canonical_intake.py`; PR documents deliberate-break on shared `trip_id` seed. | — |
| Travel-Plan-Permission | #1624 | #1595 | VERIFIED | `approval_packet.py` reconciliation; `test_build_packet_rejects_cost_breakdown_that_disagrees_with_trip_total` in diff; PR states gate failed on `origin/main` before fix. | — |
| Travel-Plan-Permission | #1625 | #1596 | VERIFIED | `policy_snapshot.py` evaluates contracts at departure; `tests/python/test_policy_snapshot_contracts.py` + deliberate-break note in PR. | — |
| Trend_Model_Project | #6056 | #6053 | VERIFIED | `src/trend_analysis/api.py` exports regime table for multi-period runs; `tests/test_multi_period_regime_exports.py` added; PR includes fail→restore transcript. | — |
| Pension-Data | #917 | #885 | VERIFIED | `pension_data/staging/doc_lineage_vars.py`, JSON schema package data, `tests/staging/test_doc_lineage_vars.py`; deliberate-break transcript in PR. | — |
| trip-planner | #1857 | #1783 | VERIFIED | `amtrak_gtfs.py`, GTFS fixture, `tests/sources/test_amtrak_gtfs_adapter.py::test_parses_fixture_trips`; deliberate-break on corrupted `stop_times.txt` in PR. | — |
| trip-planner | #1858 | #1785 | VERIFIED | `duffel_flight.py`, `tests/sources/test_duffel_adapter_offline.py::test_emits_raw_snapshot`; deliberate-break on empty records in PR. | — |
| Workflows | #3527 | #3391 | VERIFIED | Belt completion evidence in worker + `belt_ledger_completion.py`, `audit_belt_ledger_completion.py`, `tests/workflows/test_belt_ledger_completion.py` (ledger-only reject, blocked artifact, four counts, issue-3371 audit). | — |
| Fine-Art-Archive | #742 | #708 | VERIFIED | `selection/lenses.py` guards; `tests/test_selection_lenses.py` new cases; deliberate-break transcript in PR. | — |
| trip-planner | #1859 | #1827, #1839 | VERIFIED | Removes Kyoto fallback fixtures from `workspace.py`; compare shows measured routes only; tests `test_uncovered_destination_yields_no_substituted_scenarios`, connection-count honesty, multi-modal trip. | — |
| trip-planner | #1860 | #1841 | VERIFIED | `PATCH /api/trips`, `extra="forbid"` on create, edit UI; gate table with break rows for `extra="ignore"` and verdict clearing. Reproduction curl not run (401 without session). | — |
| trip-planner | #1861 | #1845 | VERIFIED | Geo-resolved destinations, verdict-aware chat copy, offline-first messaging; planner turn tests in diff; deliberate-break in PR. | — |
| Fine-Art-Archive | #743 | #709 | VERIFIED | `rocchio.py` filters non-finite ratings; `tests/test_rocchio_preference.py`; deliberate-break transcript. | — |
| Fine-Art-Archive | #744 | #710 | VERIFIED | `variants.py` `deepcopy` on inherit; `tests/test_variants.py`; deliberate-break transcript. | — |
| Fine-Art-Archive | #745 | #711 | VERIFIED | `dimension_utils.py` tolerance validation; `tests/test_dimension_utils.py`; deliberate-break transcript. | — |
| Workflows | #3537 | #1836 | VERIFIED | Campaign tracker only on issue; PR implements keepalive consumed-receipt retry in `.github/scripts/keepalive-loop.js` + `keepalive-loop.test.js`. | — |
| Fine-Art-Archive | #746 | #712 | VERIFIED | `eink/palette.py` finite guards on `acuity_blur_radius`; `tests/test_dither_metric_discriminates.py`; deliberate-break transcript. | — |
| Workflows | #3536 | #1836 | VERIFIED | Campaign tracker on issue; PR fixes full-width GraphQL comment IDs in `runner_lib` storage + `test_pr_comment_storage.py`. | — |
| Workflows | #3540 | #36 | NOT IMPLEMENTED | Diff retires `APPROVED_ASSERTION_REPLACEMENTS` in `check_deliberate_break.py` (+ consumer template) with new tests. **Unmet:** issue #36 acceptance criteria still describe conditional mypy/black/coverage installation and timing — none of that appears in the squash diff. Wrong issue close. | [#3575](https://github.com/stranske/Workflows/issues/3575) |
| Workflows | #3535 | #1836 | VERIFIED | Campaign tracker on issue; PR requires reviewer request for legacy sealed canaries in `maint71_merge_sync_prs.js` + JS contract tests. | — |

**Result:** 19 VERIFIED, 0 PARTIAL, 1 NOT IMPLEMENTED, 0 EXCLUDED (belt-only bookkeeping merges none in batch).  
**Follow-ups filed:** 1 (issue/AC mismatch on Workflows #3540 → #36).  
**Deferred:** 25 additional eligible PRs remain in the rolling 36h window for the next D4 pass.

Evidence: `artifacts/verification/evidence/D4-verify-merged-2026-09-25T03/`

**Confidence:** High on VERIFIED rows (squash diff + named tests; deliberate-break or gate tables where required). High that Workflows #3540 delivered real gate hardening; high that it does **not** satisfy issue #36’s written acceptance criteria — would change verdict only if #36’s body is shown to have been intentionally repurposed without updating AC text. Medium on trip-planner #1860 reproduction (auth-blocked curl; pytest gates substituted).
