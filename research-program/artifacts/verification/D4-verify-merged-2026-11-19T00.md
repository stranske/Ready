# D4 verify merged — 2026-11-19T00 (attempt 1)

**Window:** merges on/after `2026-11-17T12:21:30Z` (~36h before run). **Repos:** `SUPPORTED_REPOS` minus Orchestrator. **Cap:** 20 PRs; **verified this run:** 12 (all eligible in-window merges not already covered by `D4-verify-merged-2026-11-18T00` ledger, after chore/bootstrap/template-sync exclusion). **GitHub writes:** none (offload read-only); follow-ups not filed.

**Rate limit:** none.

**Ledger:** 12/12 eligible in window; **0** additional eligible merges remain for this window under the same filters.

## Summary

| Verdict | Count |
|---------|------:|
| VERIFIED | 8 |
| PARTIAL | 2 |
| NOT IMPLEMENTED | 0 |
| DOC / no issue AC | 2 |

## Results

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| trip-planner | [2046](https://github.com/stranske/trip-planner/pull/2046) | [#2043](https://github.com/stranske/trip-planner/issues/2043) | VERIFIED | — | no (offload) |
| Portable-Alpha-Extension-Model | [2519](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2519) | [#2515](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2515) | VERIFIED | `_comparison_identity` + `test_same_path_rerun_invalidates_comparison`; deliberate-break transcript in PR body. | no (offload) |
| Portable-Alpha-Extension-Model | [2521](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2521) | [#2515](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2515) (closer) | VERIFIED | Lint-format closer on #2519; no new functional claim. | no (offload) |
| Workflows | [4735](https://github.com/stranske/Workflows/pull/4735) | — (cites Inv-Man-Intake#1083, Orchestrator#1439 in body) | DOC | Operational docs only (`docs/ops/LOCAL_LANES.md` reopen route). | no (offload) |
| Workflows | [4736](https://github.com/stranske/Workflows/pull/4736) | — (PR-owned) | VERIFIED | `test_keepalive_prompt_delivery_rules.py` + deliberate-break note in body. | no (offload) |
| Workflows | [4740](https://github.com/stranske/Workflows/pull/4740) | [#4739](https://github.com/stranske/Workflows/issues/4739) | VERIFIED | Black/format repair for `test_maint76_claude_review_dispatch`; dispatch `pr_number` wiring in template. | no (offload) |
| Pension-Data | [1050](https://github.com/stranske/Pension-Data/pull/1050) | [#1049](https://github.com/stranske/Pension-Data/issues/1049) | PARTIAL | Break-and-revert + substantive tests for all six lane-E targets in diff; PR does not report whole-Gate CI uncovered statement+branch delta (~180 or documented shortfall on CI artifacts). | no (offload) |
| Pension-Data | [1047](https://github.com/stranske/Pension-Data/pull/1047) | [#1044](https://github.com/stranske/Pension-Data/issues/1044) | VERIFIED | `tests/coverage/test_issue_1044_lane_b.py`; 219-unit reduction and break/revert table in body. | no (offload) |
| Pension-Data | [1046](https://github.com/stranske/Pension-Data/pull/1046) | [#1045](https://github.com/stranske/Pension-Data/issues/1045) | VERIFIED | Ranked targets + production fixes; body documents 176-unit CI reduction (4 short of 180, allowed). | no (offload) |
| Pension-Data | [1051](https://github.com/stranske/Pension-Data/pull/1051) | [#1045](https://github.com/stranske/Pension-Data/issues/1045) (closer) | VERIFIED | Leap-day UTC ordering regression + mutation table in `tests/quality/test_anomaly_rules.py`. | no (offload) |
| Workflows | [4714](https://github.com/stranske/Workflows/pull/4714) | — (maint-79 corpus harvest; design #2819) | DOC | Staging-only `config/model_eval_corpus_staging.json` growth; no product AC. | no (offload) |
| Workflows | [4711](https://github.com/stranske/Workflows/pull/4711) | [#4432](https://github.com/stranske/Workflows/issues/4432) (Refs) | PARTIAL | Diff lands confinement canaries, `validate_subscription_analysis_evidence.py`, and API-key regression tests; issue task 6 and PR body still require hosted post-merge Actions evidence on the delivered merge SHA (`876baff4`). | no (offload) |

## Notes

- **Continuity:** Prior run `D4-verify-merged-2026-11-18T00` ledger excluded 20 PRs still inside an overlapping window; this run consumed the remaining **12** before the 36h window slid forward (e.g. lane-C/E coverage on #842 / #690 are now out of window).
- **Reproduction blocks:** none on linked issues in this batch.
- **Belt (#Workflows#3391):** none among these 12.
- **Confidence:** high on named-test vs diff alignment for product fixes; medium on #1050 / #4432 where closure/issue checkboxes outpace evidenced hosted or whole-Gate coverage numbers.

**Stopped:** window exhausted (12/12). **Next run:** new 36h window; no resume ledger entries for this unit until attempt 2.