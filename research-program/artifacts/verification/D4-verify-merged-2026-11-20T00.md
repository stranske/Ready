# D4 — merged PR verification

Checked 2026-11-20 (UTC), for PRs merged from 2026-11-18T00:35:14Z onward. I enumerated all supported fleet repositories except Orchestrator and excluded template-sync, dependency, and release chores. Eight implementation-linked PRs were reviewed, oldest first; this is below the 20-PR cap. No GitHub secondary-rate-limit response occurred.

The strongest finding is that a green required check did not establish completion in three cases. Two merged PRs leave a literal acceptance criterion unmet, and the Codex subscription work merged without the required hosted Codex execution evidence.

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
| --- | --- | --- | --- | --- | --- |
| Inv-Man-Intake | [#1092](https://github.com/stranske/Inv-Man-Intake/pull/1092) | [#1091](https://github.com/stranske/Inv-Man-Intake/issues/1091) | VERIFIED | — | — |
| Workflows | [#4740](https://github.com/stranske/Workflows/pull/4740) | [#4739](https://github.com/stranske/Workflows/issues/4739) | PARTIAL | The issue requires `Enforce explicit Gate success` to conclude `success`; the cited successful Gate run has it `skipped`, which is its normal guarded success path. The criterion is literally unmet/impossible as written. | No — this offload expressly forbids opening GitHub issues. |
| Pension-Data | [#1050](https://github.com/stranske/Pension-Data/pull/1050) | [#1049](https://github.com/stranske/Pension-Data/issues/1049) | PARTIAL | Evidence shows 221→80 uncovered units (141), not approximately 180; it supplies neither Gate coverage evidence nor the required explicit shortfall explanation. | No — offload restriction. |
| Pension-Data | [#1047](https://github.com/stranske/Pension-Data/pull/1047) | [#1044](https://github.com/stranske/Pension-Data/issues/1044) | VERIFIED | — | — |
| Pension-Data | [#1046](https://github.com/stranske/Pension-Data/pull/1046) | [#1045](https://github.com/stranske/Pension-Data/issues/1045) | VERIFIED | — | — |
| Pension-Data | [#1051](https://github.com/stranske/Pension-Data/pull/1051) | [#1045](https://github.com/stranske/Pension-Data/issues/1045) | VERIFIED | — | — |
| Workflows | [#4711](https://github.com/stranske/Workflows/pull/4711) | [#4432](https://github.com/stranske/Workflows/issues/4432) | PARTIAL | No post-merge hosted Codex run establishes `llm-analysis-run=true`, Codex provider/model, JSON-derived summary outputs, subscription authentication, and absent OpenAI/Anthropic API keys. Merged-tip keepalive run 44427473656 skipped its Codex job. The delivered-SHA actual-workflow mutation/restoration proof is also absent. | No — offload restriction. |
| Workflows | [#4757](https://github.com/stranske/Workflows/pull/4757) | [#4501](https://github.com/stranske/Workflows/issues/4501) | VERIFIED | — | — |

Evidence summary:

- #1092 adds concrete PPTX corruption/relationship handling, persisted comparison details, and behavior-specific CRC/conflict tests; required Gate passed.
- #1047 adds 95 discriminating cases across all 11 ranked targets, records 219 covered statements/arcs and real break/revert evidence; required Gate passed.
- #1046/#1051 provide path-specific explanations for the remaining five unreachable coverage paths and a non-vacuous leap-day ordering regression; their required Gates passed.
- #4757 provides seven dated Health 85 observations at 409–563 seconds with traceable run/artifact references, plus reconciliation tests. The 11/18 overall Health 85 failure was an unrelated Orchestrator HTTP 502; its Workflows measurement remained recorded.

Excluded apparent references:

- Workflows #4774 references `trip-planner #2052`, which is a pull request, not an issue.
- Workflows #4778 uses #4501 as a diagnostic fixture rather than claiming to implement it. Treating it as a delivery PR would produce a false NOT IMPLEMENTED finding.

Confidence: high for diff/criterion verdicts; medium for #4757's historical measurement provenance because the retained run/artifact references were checked through the merged evidence rather than re-downloading every historical artifact in this capped pass.
