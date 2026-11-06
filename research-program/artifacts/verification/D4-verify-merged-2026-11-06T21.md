# D4 merged-PR acceptance verification — 2026-11-06

Window sampled: 2026-11-05T09:46:58Z through 2026-11-06T21:33:57Z.  The 20 oldest eligible, non-chore merges were checked in merge order; the next candidate is `trip-planner#1991`.  GitHub did not return a secondary-rate-limit response.

| Repo | PR (merge) | Linked issue | Verdict | Unmet criteria / evidence | Follow-up filed |
|---|---|---|---|---|---|
| trip-planner | #1980 (`457f457`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; no product-probe implementation, named tests, CI job, artifact, or deliberate-break evidence. | No — offload prohibits GitHub writes. |
| Portable-Alpha-Extension-Model | #2483 (`524a505`) | #2480 | NOT IMPLEMENTED | Only `agents/cursor-2480.md`; none of the required artifact-integrity regressions, mutations, coverage evidence, or CI work is in the diff. | No — offload prohibits GitHub writes. |
| trip-planner | #1981 (`66553a8`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |
| Travel-Plan-Permission | #1731 (`87aaeb6`) | #1728 | NOT IMPLEMENTED | Only `agents/claude-1728.md`; no `Issues.txt` correction or named regression test. | No — offload prohibits GitHub writes. |
| trip-planner | #1982 (`a6ad438`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |
| Workflows | #4448 (`7b92760`) | #4370 | PARTIAL | Source and template fix plus discriminating backup tests landed and merge CI passed. The required live maint-71/consumer-thread outcome remains deferred and unobserved; no durable deliberate-break transcript is in the diff. The ledger is not a ledger-only PR and does not show the belt false-`done` defect. | No — offload prohibits GitHub writes. |
| trip-planner | #1983 (`181aa6f`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |
| Fine-Art-Archive | #872 (`a0e9ee6`) | #827 | NOT IMPLEMENTED | Only `agents/cursor-827.md`; none of the count-contract behavior or tests landed in this merge. | No — offload prohibits GitHub writes. |
| trip-planner | #1984 (`bbe27e2`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |
| Fine-Art-Archive | #870 (`f59996c`) | #825 | VERIFIED | Diff documents preview-only caller evidence, keeps saved/feed/export on server-owned evidence, and adds discriminating endpoint/OpenAPI tests. Required CI checks passed. | — |
| trip-planner | #1985 (`f250ed6`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |
| Fine-Art-Archive | #871 (`348abf6`) | #826 | VERIFIED | Implements target validation/disclosure and UI output; tests cover equal target-independent evidence and unknown target (including `sample=0`); retained red/green receipt and passing CI are present. | — |
| trip-planner | #1986 (`d267aeb`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |
| Travel-Plan-Permission | #1730 (`34253f5`) | #1727 | VERIFIED | Diff separates registered and planned routes, updates permission maps, and adds route/document assertions. On exact merge commit, the issue reproduction returned `GET /api/itineraries -> 404`; named test `test_security_model_doc_lists_only_registered_api_routes` passed (1 passed, 3.23s). Merge CI passed. | — |
| Workflows | #4456 (`2d47d97`) | #3904 | PARTIAL | It reduces and audits a subset of body-clause/floor witnesses, with passing CI. It does not deliver the issue's full three-file collection/coverage comparison, production-path deliberate-break receipts, workflow timing/budget instrumentation, or required hosted before/after evidence. | No — offload prohibits GitHub writes. Existing #4462 is cited as unfinished work. |
| Travel-Plan-Permission | #1732 (`b56d92b`) | #1727 | NOT IMPLEMENTED | Only `agents/cursor-1727.md`; no product or test change in this PR. #1730 independently delivered the issue, but that does not make this merge an implementation. | No — offload prohibits GitHub writes. |
| Fine-Art-Archive | #874 (`6282d59`) | #827 | VERIFIED | Implements distinct selected/available/written/omission counts across preview, feed, export and UI; focused tests cover mixed, all-master, all-missing and empty cases. Diff retains the requested ambiguous-rendering red/green receipts; merge CI passed. | — |
| trip-planner | #1987 (`c5b7435`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |
| trip-planner | #1988 (`5fd18a7`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |
| trip-planner | #1989 (`ef2d130`) | #1910 | NOT IMPLEMENTED | Only `agents/claude-1910.md`; same unmet #1910 product-probe criteria. | No — offload prohibits GitHub writes. |

## Critical judgment

The strongest problem is repeated merging of generic agent-bootstrap files as PRs that reference substantive issues. These are not the special `.agents/issue-<n>-ledger.yml` bookkeeping commits covered by the belt exception, and their squash diffs contain none of the issue's requested product or test changes. They are therefore NOT IMPLEMENTED, even where a later PR eventually delivered the same issue.

Confidence is high for the file-only findings and the three VERIFIED rows. Confidence is moderate for the two PARTIAL rows: their concrete omissions are direct diff evidence, while their unobserved external/live criteria cannot be resolved by a read-only offload.

No issue carried a runnable `Reproduction:` block except Travel-Plan-Permission#1727. Its reproduction was re-run successfully as recorded above. No issue was commented on, reopened, or followed up because the offload rules forbid all GitHub writes despite the unit brief otherwise authorizing them.

