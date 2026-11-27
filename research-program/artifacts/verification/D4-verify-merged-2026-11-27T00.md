# D4 verify merged — 2026-11-27T00

**Window:** merges after `2026-11-25T12:54:00Z` (36h), lane fleet per `handoff.sh` `SUPPORTED_REPOS` (excluding Orchestrator).

**Run limits:** 20 PRs verified (issue-linked, non-chore), oldest merged first; API pacing observed; no secondary rate limit.

**Reproduction / offload:** Where issues carry `Reproduction:` blocks, re-run is noted per PR below. This invocation is an **offload** — GitHub follow-up issues, comments, and reopens were **not** performed (unit brief authorizes filing; offload rules block writes).

## Summary

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| Counter_Risk | [#1273](https://github.com/stranske/Counter_Risk/pull/1273) | [#1272](https://github.com/stranske/Counter_Risk/issues/1272) | VERIFIED | — | No (offload) |
| Travel-Plan-Permission | [#1770](https://github.com/stranske/Travel-Plan-Permission/pull/1770) | [#1769](https://github.com/stranske/Travel-Plan-Permission/issues/1769) | VERIFIED | — | No (offload) |
| Travel-Plan-Permission | [#1771](https://github.com/stranske/Travel-Plan-Permission/pull/1771) | [#1768](https://github.com/stranske/Travel-Plan-Permission/issues/1768) | VERIFIED | — | No (offload) |
| Counter_Risk | [#1275](https://github.com/stranske/Counter_Risk/pull/1275) | [#1274](https://github.com/stranske/Counter_Risk/issues/1274) | VERIFIED | — | No (offload) |
| Travel-Plan-Permission | [#1773](https://github.com/stranske/Travel-Plan-Permission/pull/1773) | [#1772](https://github.com/stranske/Travel-Plan-Permission/issues/1772) | VERIFIED | — | No (offload) |
| Workflows | [#5249](https://github.com/stranske/Workflows/pull/5249) | [#5245](https://github.com/stranske/Workflows/issues/5245) | VERIFIED | — | No (offload) |
| Workflows | [#5250](https://github.com/stranske/Workflows/pull/5250) | [#5235](https://github.com/stranske/Workflows/issues/5235) | VERIFIED | — | No (offload) |
| Workflows | [#5251](https://github.com/stranske/Workflows/pull/5251) | [#2298](https://github.com/stranske/Workflows/issues/2298) | VERIFIED | — | No (offload) |
| Workflows | [#5254](https://github.com/stranske/Workflows/pull/5254) | [#5252](https://github.com/stranske/Workflows/pull/5252) | VERIFIED | — | No (offload) |
| Workflows | [#5256](https://github.com/stranske/Workflows/pull/5256) | [#5255](https://github.com/stranske/Workflows/issues/5255) | VERIFIED | — | No (offload) |
| Workflows | [#5258](https://github.com/stranske/Workflows/pull/5258) | [#4784](https://github.com/stranske/Workflows/issues/4784) | VERIFIED | — | No (offload) |
| Workflows | [#5260](https://github.com/stranske/Workflows/pull/5260) | [#5232](https://github.com/stranske/Workflows/pull/5232) | VERIFIED | — | No (offload) |
| Workflows | [#5261](https://github.com/stranske/Workflows/pull/5261) | [#5233](https://github.com/stranske/Workflows/pull/5233) | VERIFIED | — | No (offload) |
| Workflows | [#5265](https://github.com/stranske/Workflows/pull/5265) | [#3988](https://github.com/stranske/Workflows/issues/3988) | VERIFIED | — | No (offload) |
| Workflows | [#5269](https://github.com/stranske/Workflows/pull/5269) | [#4747](https://github.com/stranske/Workflows/issues/4747) | VERIFIED | — | No (offload) |
| Workflows | [#5268](https://github.com/stranske/Workflows/pull/5268) | [#5265](https://github.com/stranske/Workflows/pull/5265) | VERIFIED | — | No (offload) |
| Trend_Model_Project | [#6251](https://github.com/stranske/Trend_Model_Project/pull/6251) | [#6250](https://github.com/stranske/Trend_Model_Project/pull/6250) | VERIFIED | — | No (offload) |
| Workflows | [#5270](https://github.com/stranske/Workflows/pull/5270) | [#6250](https://github.com/stranske/Trend_Model_Project/pull/6250) | VERIFIED | — | No (offload) |
| Workflows | [#5274](https://github.com/stranske/Workflows/pull/5274) | [#6250](https://github.com/stranske/Trend_Model_Project/pull/6250) | VERIFIED | — | No (offload) |
| Workflows | [#5277](https://github.com/stranske/Workflows/pull/5277) | [#6250](https://github.com/stranske/Trend_Model_Project/pull/6250) | VERIFIED | — | No (offload) |

**Skipped (not verified this run):** All `chore: sync workflow templates`, `chore(main): release *`, and `deps: sync` merges in window; Workflows [#5252](https://github.com/stranske/Workflows/pull/5252) and [#5257](https://github.com/stranske/Workflows/pull/5257) (no issue reference in body); remaining issue-linked merges in window deferred to the next run (cap 20).

## Per-PR notes

### Counter_Risk #1273 → #1272

- **Diff:** `src/counter_risk/cli/__init__.py` prints `result.error_message` and routes exceptions through `format_gui_run_failure`; gate tests in `tests/test_cli_coverage_round.py` and `tests/test_counter_risk_cli.py` assert operator guidance.
- **AC:** Named test `test_gui_headless_preserves_unsuccessful_exit_code` updated to expect `Operator action:` — met.
- **Reproduction:** Not in issue body. Deliberate-break from AC not re-run (offload).

### Travel-Plan-Permission #1770 → #1769 / #1771 → #1768

- **Diff:** Belt ledger + substantive edits to `tests/python/test_cross_repo_smoke.py` (date isolation / static travel date expiry).
- **AC:** Source-side regression tests landed; sync-core / Gate success on consumer #1767 is operational evidence recorded in ledger and #1773 — not re-driven end-to-end this run.

### Counter_Risk #1275 → #1274

- **Diff:** Audit doc lines dropped in `docs/audit/*`; `test_audit_progress_docs_drop_resolved_gaps` added to `tests/docs/test_audit_log_historical.py`.
- **AC:** Named module gate present; deliberate-break not re-run.

### Travel-Plan-Permission #1773 → #1772

- **Diff:** Only `docs/evidence/issue-1772/README.md` — post-merge CI, pytest, and sync-core classification evidence per backlog AC (issue checkboxes already marked done).

### Workflows #5249 → #5245

- **Diff:** `workflow-decisions.md` / `workflows-cleanup-tracker.md` move Health 68 from in-review to verified with artifact links — matches Health 68 alert coverage correction.

### Workflows #5250 → #5235 (scenario)

- **Diff:** `keepalive_loop.js` returns `skip/pr-not-open` when `pr.state !== 'open'`; Node regression `evaluateKeepaliveLoop skips a closed pull request before Gate even with force retry`.
- **AC:** Matches PR narrative (post-merge #5235 loop); belt issue #5235 still describes unrelated Gate fixture work — implementation evidence is PR-scoped, not belt-ledger-only.

### Workflows #5251 → #2298 (context)

- **Diff:** `scripts/validate_sync_target_dispositions.py`, Health 70 workflow step, Python tests — requires explicit disposition when manifest targets drop.
- **AC:** PR verification block cites failing/broken comparisons and 64 passing focused tests; not re-run locally.

### Workflows #5254 → #5252 (placement)

- **Diff:** `docs/reports/workflow-decisions.md` placement row for vendored matcher — doc-only decision record.

### Workflows #5256 → #5255

- **Diff:** `health85_followup.py` short-circuits closed delivery issues; `test_closed_delivery_issue_preserves_observations_without_publication` added.

### Workflows #5258 → #4784 (tracker)

- **Diff:** Publisher/PR context placement outcomes in `docs/reports/*` — doc evidence for structure-review track.

### Workflows #5260 → #5232

- **Diff:** Keepalive publisher skips Git push when PR closed; shell tests for `closed` state in publisher paths.

### Workflows #5261 → #5233

- **Diff:** `Setup API client` moved before `Resolve Workflows ref` in belt dispatcher workflow + template + drift allowlist hashes.

### Workflows #5265 → #3988

- **Diff:** Retires 46-file routing packet per #3988; archive map and `.gitignore` comment fix; large deletion set with recovery pointers.

### Workflows #5269 → #4747

- **Diff:** Retires unused archive forwarding pages; tests guard remaining routes.

### Workflows #5268 → #5265

- **Diff:** Tracker markdown recording verified root pruning — companion evidence to #5265 merge.

### Trend_Model_Project #6251 → #6250 (rollout context)

- **Diff:** `tests/test_post_ci_summary.py` accepts either footer string while managed publisher rolls out — matches PR verification (10/10 module tests cited in body); local pytest not re-run.

### Workflows #5270 / #5274 / #5277 → #6250 (fleet context)

- **Context:** Maint 71 campaign held on Trend #6250 review; fixes are in `maint-82` campaign refresh/continuation and Maint 71 receipt/head reporting.
- **Diff:** Substantive JS tests for review recovery dispatch, marked Codex receipt handling, and prepared/drainable head summaries — met PR verification narratives; fleet issues live in Trend, not Workflows.

## Confidence

**Outcome:** 20/20 verdicts VERIFIED on squash-diff vs stated acceptance (high confidence on code+test PRs; doc/evidence PRs verified against issue/PR text, not re-run gates locally).

**Would change verdicts:** A mandatory `Reproduction:` re-run that still fails on current `main`, or a belt ledger marking tasks `done` with ledger-only commits (none observed this run; Workflows#3391 not triggered).