# D4 Verification Report — 2026-11-10T22

**Unit:** D4-verify-merged-2026-11-10T22 (attempt 1)  
**Window:** 2026-11-09T11:00:23Z to 2026-11-10T23:00:23Z  
**Scope result:** 1 issue-linked, non-chore PR completed before evidence collection was interrupted. Template-sync chores and PRs with no linked issue were excluded. No GitHub writes were performed: the offload rules prohibit comments, reopening issues, and follow-up filing.

## Verification ledger

| Repo | PR | Issue | Merged | Verdict | Unmet criteria | Follow-up filed |
|---|---|---|---|---|---|---|
| stranske/Workflows | [#4578](https://github.com/stranske/Workflows/pull/4578) | [#4515](https://github.com/stranske/Workflows/issues/4515) | 2026-11-09T11:15:22Z | PARTIAL | Required real post-merge intake run showing a non-Codex `DEFAULT_AGENT` under the specified posterior/capacity condition is explicitly unchecked. | No — offload rule prohibits GitHub writes. |

## Finding: Workflows #4578 / #4515 — PARTIAL

Merged commit: `e1b5c5284108b94eacaab658cfcc60196c2dd0ce`.

The issue’s first, second, and fourth acceptance criteria are checked. The required A3 production observation is not: the issue explicitly leaves unchecked the criterion requiring a qualifying post-merge intake summary with a non-Codex `DEFAULT_AGENT`. The PR body likewise says “overall acceptance is NOT ESTABLISHED” and “A3 remains unchecked.”

The squash diff contains collected fleet-history evidence and acceptance artifacts, but no diff line can substitute for the missing live run. The named node test and deliberate-break evidence are represented by retained evidence; they do not satisfy A3. This is a genuine operational acceptance gap, not a test failure.

**Required external follow-up (not filed):** create or continue a follow-up against #4515 that names the missing production run URL and records the requested summary condition. Cite `artifacts/issue-3988/acceptance.md` and the merged commit above.

## Limits and unknowns

Discovery identified additional issue-linked candidates in merge order, including Workflows #4586, #4588, #4600, #4582, #4585, #4598, #4599, #4602, #4596, and #4605. They were not assigned verdicts: the combined diff/issue retrieval response was truncated before each issue’s criteria and its corresponding diff could be independently retained and compared. No secondary-rate-limit response was observed.

Confidence: high for #4578’s PARTIAL verdict because the source issue and the PR body explicitly retain the failed A3 condition. A qualifying live run with the specified summary would change that criterion’s status.
