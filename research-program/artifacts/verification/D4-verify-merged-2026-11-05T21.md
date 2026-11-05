# D4 merged-PR implementation verification — 2026-11-05

Checked 2026-11-05T21:41Z UTC. Window: merged at or after `2026-11-04T09:41:22Z` through this run. Inspected the first **20** non–dependency-sync PRs in merge order (of **41** non-chore candidates in window). `Orchestrator` and `stranske/Collab-Admin` excluded.

Method: squash diff via `gh pr diff`, linked issue bodies, PR bodies for issue refs. No linked issue in this batch contained a `Reproduction:` block or a core-function scorecard contract requiring a product-scorecard re-drive.

| Repo | PR | Issue | Verdict | Unmet criteria / diff evidence | Follow-up |
| --- | --- | --- | --- | --- | --- |
| Workflows | #4441 `cb380fbe` | #4389 | PARTIAL | Diff implements option (a): `agents-81-gate-followups.yml` counts only PR-body tasks; adds `guarded-merge-tasks.test.js`, refusal comment marker, and `GoalsAndPlumbing` direction. Unmet: post-deploy AC (“Runtime AC merge guard passed” on a real consumer PR) not observable here; issue #4389 remains open for that. | Not filed: offload read-only on GitHub. |
| trip-planner | #1968 `b64a8d7a` | #1910 | NOT IMPLEMENTED | Diff adds only `agents/claude-1910.md`. No changes to `check_full_product_verification.py`, CI `product-probe` job, contract tests, or `PRODUCT_CONTRACT.md`. | Not filed: offload restriction. |
| Workflows | #4453 `0eb17f69` | #4427 | NOT IMPLEMENTED | Diff is `.agents/issue-4427-ledger.yml` plus handoff markdown only; no `pyproject.toml`, `sync_dev_dependencies.py`, or regression tests for the pytest pin mismatch. | Not filed: offload restriction. |
| Manager-Database | #1890 `bbefced1` | #1750 | NOT IMPLEMENTED | Diff adds only `agents/cursor-1750.md`. No `tests/test_chat_chain_lifecycle.py`, evidence replay, or coverage work. | Not filed: offload restriction. |
| trip-planner | #1969 `bcc6f144` | #1910 | NOT IMPLEMENTED | Same as #1968: single agent bootstrap file only. | Not filed: offload restriction. |
| trip-planner | #1970 `6013fca0` | #1910 | NOT IMPLEMENTED | Same scaffold-only pattern. | Not filed: offload restriction. |
| Workflows | #4450 `f2849e4a` | #4366 | PARTIAL | Substantive `agents-auto-pilot.yml` dispatch-before-marker and page-at-a-time merged-PR search; Python tests in diff. PR body admits full `pytest -q tests/` gate and deliberate-break receipts still pending; live Maint-71 thread resolution unverified. | Not filed: offload restriction. |
| trip-planner | #1971 `8d904d94` | #1910 | NOT IMPLEMENTED | Bootstrap-only. | Not filed: offload restriction. |
| Workflows | #4443 `81e575a0` | #4364 | VERIFIED | `SubscriptionClientAdapter` / scoped auxiliary routing in `_llm_client.py`; discriminating tests in `tests/scripts/test_llm_client_shared.py`; template consumer copy updated. | — |
| Workflows | #4439 `7862c733` | #4435 | PARTIAL | `maint71_merge_sync_prs.js` and `sync_pr_merge_contract.js` changes match named full-scope identity tests in diff; PR cites deliberate-break on bare `dispatchCanaryRefresh`. Unmet: live Maint-71 “refresh_dispatched >= 1” acceptance still open on issue. | Not filed: offload restriction. |
| Workflows | #4446 `fac332ae` | #4427 | PARTIAL | Delivers Maint-52 `sync_dev_dependencies.py` rewrite for consumer `pages-wasm-demo.yml`, new pytest alignment tests, and ledger updates. Unmet: issue’s live Maint-71/sync-thread AC; ledger marks several tasks `done` citing this merge while some agent-owned AC items (full-suite gate receipts) remain claim-only in notes. | Belt false-done pattern → report under Workflows#3391 (repo Workflows, file `.agents/issue-4427-ledger.yml`, tasks marked done with handoff-only commits on #4453/#4457). Follow-up issue not filed (offload). |
| trip-planner | #1974 `5f39a36c` | #1910 | NOT IMPLEMENTED | Bootstrap-only. | Not filed: offload restriction. |
| Workflows | #4445 `f4992eff` | #4368 | VERIFIED | `config/model_registry.json` documents no Muse backup without consumer `capacity_backup`; `tests/test_model_registry_retirement.py` fails on mis-stated backup text. Live sync-thread AC deferred per issue. | — |
| Workflows | #4457 `17d9913e` | #4427 | NOT IMPLEMENTED | Ledger + handoff doc only (duplicate closer pass); no executable fix beyond #4446. | Not filed: offload restriction. |
| trip-planner | #1975 `5e5bdd03` | #1910 | NOT IMPLEMENTED | Bootstrap-only. | Not filed: offload restriction. |
| Workflows | #4444 `d77a8e3a` | #4369 | VERIFIED | `tools/subscription_llm.py` resolves credentials under `CLAUDE_CONFIG_DIR`; new tests in `tests/test_subscription_llm.py` with deliberate-break notes in ledger portion of PR. | — |
| trip-planner | #1976 `28c8b77c` | #1910 | NOT IMPLEMENTED | Bootstrap-only. | Not filed: offload restriction. |
| trip-planner | #1977 `76bc591a` | #1910 | NOT IMPLEMENTED | Bootstrap-only. | Not filed: offload restriction. |
| Workflows | #4459 `ece97ee3` | #3898 | PARTIAL | Extends `test_agents_guard_publication.py` with fork read-only boundary cases; evidence doc records falsifying run (existing publishers already skip ineligible fork writes). Unmet: issue checklist items for sync-manifest audit, Maint68/71 campaign delivery, and independent CI/review evidence not in squash diff. | Not filed: offload restriction. |
| trip-planner | #1978 `bec440b6` | #1910 | NOT IMPLEMENTED | Bootstrap-only. | Not filed: offload restriction. |

## Summary counts (this run)

| Verdict | Count |
| --- | ---: |
| VERIFIED | 3 |
| PARTIAL | 5 |
| NOT IMPLEMENTED | 12 |

## Critical judgment and limits

**Bootstrap PRs:** Nine trip-planner merges for #1910 and one Manager-Database bootstrap are agent lane openers, not implementation. Treating them as NOT IMPLEMENTED is high-confidence; the fleet should stop re-merging identical bootstrap files for the same open issue.

**Repair vs evidence:** Workflows #4453 and #4457 are closer bookkeeping on #4427 while #4446 carries the real Maint-52 repair. Verifying the bookkeeping merges as NOT IMPLEMENTED is correct; the belt ledger on #4446 still marks tasks `done` tied to commits that are mostly operational narrative — that matches the #3391 root cause class.

**Offload vs unit auth:** This invocation’s offload rule forbids GitHub writes (issues, comments, reopen). The unit brief authorizes filing; no follow-ups were opened. Each “Not filed” row is actionable text for a non-offload closer.

**Rate limit:** No secondary rate limit encountered. Remaining in-window non-chore candidates after the 20-PR cap include (merge order): Workflows #4448, Counter_Risk #1232, Portable-Alpha-Extension-Model #2482–#2483, Travel-Plan-Permission #1730–#1732, Fine-Art-Archive #870–#874, trip-planner #1979–#1988, and others merged after #1978.
