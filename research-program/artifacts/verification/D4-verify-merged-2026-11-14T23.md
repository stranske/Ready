# D4 verification — 2026-11-14

Checked 2026-11-14 (UTC run ~2026-11-15T00:12Z). Discovery covered the 36-hour
window beginning **2026-11-13T11:45:00Z** across `SUPPORTED_REPOS` in
`handoff.sh`, excluding Orchestrator and owner-excluded `stranske/Collab-Admin`.
**Two** merged PRs were found in the window; one release chore was skipped. No
GitHub secondary-rate-limit response occurred. This offload did not post GitHub
comments, reopen issues, or file new follow-ups (read-only); gaps reference
existing tracking where noted.

| Repo | PR | Issue / relationship | Verdict | Unmet criteria / evidence | Follow-up |
|---|---:|---|---|---|---|
| Workflows | [#4627](https://github.com/stranske/Workflows/pull/4627) | Release manifest/changelog | **SKIPPED** | `chore(main): release 1.51.1` — excluded by scope (release chore). | — |
| Workflows | [#4680](https://github.com/stranske/Workflows/pull/4680) | [#4679](https://github.com/stranske/Workflows/issues/4679) | **PARTIAL** | Squash diff (not body) adds `original_command` through Python extraction/results and both JS renderers; `tests/workflows/test_acceptance_gate.py` and keepalive JS tests assert pinned-interpreter uncollapse, companion gates, setup failures, and colliding normalized commands. `docs/evidence/issue-4679/task-reconciliation.md` documents deliberate-break mutation checks. **Not met:** acceptance “Live” row — `stranske/Portable-Alpha-Extension-Model#2506` remains **open** (head `f5671cc…`, checked 2026-11-15); review thread from discussion r4559852804 is **not resolved**; sync-core stop-bumping not demonstrated. Issue state is CLOSED with `status:in-progress` labels (belt still owns post-merge proof). | Existing [#4681](https://github.com/stranske/Workflows/issues/4681) (not re-filed; offload read-only). |

## Acceptance criteria map (#4679 / #4680)

| Criterion | Evidence in squash diff | Result |
|---|---|---|
| Source-fix gates (`node --test` JS, `pytest -q tests/` Python) pass on the fix | Focused suites expanded in diff; PR merge validation narrative and evidence doc cite passing focused runs; full-repo gates not re-run locally this unit | **Met for stated regression scope** (CI/readme-backed; full fleet pytest not re-executed here) |
| Deliberate-break → revert makes named test fail then pass | `task-reconciliation.md` + isolated renderer mutation steps in diff | **Met** (documented in merged artifact, not re-run locally) |
| Next maint-71 run clears #2506 thread; sync-core stops bumping | #2506 still open/unmerged; at least one review thread unresolved | **NOT MET** |

## Critical findings

- The 36-hour window contained **no new merges** beyond the two Workflows PRs
  already on `main` from 2026-11-13 afternoon UTC; fleet-wide `gh pr list
  --search 'merged:>=2026-11-14'` returned empty for all lane repos.
- #4680 is **not** belt-only bookkeeping: the diff touches product code and
  tests, not solely `.agents/issue-*-ledger.yml`.
- Downstream live proof regressed **not** since the prior D4 run: consumer sync
  PR #2506 is still open, so a VERIFIED verdict would mis-state delivery.
- Offload constraint: reproduction re-run did not apply (`Reproduction:` block
  absent on #4679). No GitHub write actions performed.

## Test and CI evidence

- Merge commit: `1061fa7bff0960256c645cca425baae770d0569c` on `stranske/Workflows`.
- `gh pr checks 4680` shows many skipped jobs; post-merge verifier job failed on
  an older run id — treated as orthogonal to the acceptance-gate source fix.
- Recent `maint-71-merge-sync-prs.yml` runs (e.g. 43653757200, 2026-11-14T23:32Z)
  completed **success** but do not substitute for merged consumer PR #2506.

Confidence: **high** on diff-level source implementation; **high** that the live
criterion is still unmet given #2506 state; **medium** on whether latest maint-68
regenerated #2506 head since last sync-core round without merging. Merged #2506
with resolved review thread and closed sync-core bump loop would move #4680 to
**VERIFIED** for the remaining acceptance row.