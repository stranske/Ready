# D4 merged-PR implementation verification — 2026-11-04

Checked 2026-11-04 UTC. Window: merged 2026-11-03T09:31:37Z through the check. I inspected the first 20 non-chore PRs in merge order (of 25 candidates) and stopped at the mandated cap. `Orchestrator` and `stranske/Collab-Admin` were excluded.

Method: read each squash diff, linked issue and issue comments, plus check-run readback. No linked issue contained a `Reproduction:` block or named a core-function scorecard contract, so no reproduction or product-scorecard rerun applied. A green/unrelated check-run was not accepted as implementation proof.

| Repo | PR | Issue | Verdict | Unmet criteria / diff evidence | Follow-up |
| --- | --- | --- | --- | --- | --- |
| Fine-Art-Archive | #866 `ceeea842` | #816 | PARTIAL | Added tests and measurement evidence, but target reduction is 71 units, not about 180; no adequate target-by-target explanation for the shortfall. | Not filed: offload is read-only on GitHub. |
| Workflows | #4403 `8e25712f` | #4005 | PARTIAL | Two small test edits; diff contains neither Gate coverage result nor break-and-revert evidence for the ~180-unit contract. | Not filed: offload restriction. |
| Portable-Alpha-Extension-Model | #2462 `ec9a0127` | #2415 | NOT IMPLEMENTED | Five evidence files only; no tests or product changes. The added README expressly says hosted pytest remains unestablished and preserves an earlier partial PR. | Not filed: offload restriction. |
| Workflows | #4412 `6cf49cb2` | #4107 | PARTIAL | Direct screen logic and non-vacuous refusal tests landed, but merge check readback has failures and does not establish the named gate passing on this merge. | Not filed: offload restriction. |
| Counter_Risk | #1228 `941638d8` | #1209 | PARTIAL | Added `tests/test_python_floor.py`, but the diff does not change the cited configuration nor contain the required deliberate-break/revert evidence. | Not filed: offload restriction. |
| Manager-Database | #1881 `5848aa01` | #1842 | PARTIAL | Test/evidence landed, but its own evidence records 0 covered units against the 180-unit objective. | Not filed: offload restriction. |
| Portable-Alpha-Extension-Model | #2466 `5cd8c88e` | #2417 | VERIFIED | Test plus evidence deliver the issue-permitted disclosed partial result; mutations name failing assertions and restoration, with successful check readback. | — |
| Workflows | #4420 `c3f3fc5d` | #4161 | NOT IMPLEMENTED | Only README and proof archive changed; no target tests or product changes landed in this PR. | Not filed: offload restriction. |
| Portable-Alpha-Extension-Model | #2464 `6abacb50` | #2413 | PARTIAL | One assertion-only test edit; no Gate coverage or break/revert evidence for the coverage-round contract. | Not filed: offload restriction. |
| Trend_Model_Project | #6185 `1eb64d9b` | #6094 | NOT IMPLEMENTED | Tests/evidence demonstrate a disconnected-runner failure, but the diff has no change to the required Monte Carlo strategy-evaluation path. | Not filed: offload restriction. |
| Manager-Database | #1882 `e6405b61` | #1835 | NOT IMPLEMENTED | Evidence artifacts only; no test or production implementation is in this squash diff. It reports only 45 of about 180 units. | Not filed: offload restriction. |
| Portable-Alpha-Extension-Model | #2467 `bb8dd930` | #2360 | NOT IMPLEMENTED | Documentation/evidence only; no tests or product changes to satisfy the coverage issue. | Not filed: offload restriction. |
| Workflows | #4424 `4cbdbac8` | #4018 | NOT IMPLEMENTED | Documentation/evidence only; no implementation or test change is in the diff. | Not filed: offload restriction. |
| Travel-Plan-Permission | #1725 `0ccee0fa` | #1724 | PARTIAL | Contract tests and evidence changed, but neither `docs/PRODUCT_CONTRACT.md` nor the named expense-service behavior changed in this PR. | Not filed: offload restriction. |
| Portable-Alpha-Extension-Model | #2469 `0d57fb38` | #2418 | NOT IMPLEMENTED | Single evidence document; it explicitly records an accepted partial result but adds no missing test/product implementation. | Not filed: offload restriction. |
| Workflows | #4425 `e253f900` | #3995 | NOT IMPLEMENTED | Documentation/evidence only, including an acknowledged 61-unit shortfall before a different PR; this diff adds no implementation. | Not filed: offload restriction. |
| Workflows | #4406 `2bd1aa09` | #4019 | VERIFIED | Added discriminating tests, provider behavior, regenerated pins, and red/green mutation receipts; coverage evidence identifies the remaining narrow branch gap rather than omitting it. | — |
| Portable-Alpha-Extension-Model | #2470 `cec2fe3c` | #2415 | NOT IMPLEMENTED | One README correction only; it explicitly preserves the earlier partial-coverage disclosures and adds no implementation. | Not filed: offload restriction. |
| Portable-Alpha-Extension-Model | #2473 `7613ffd9` | #2381 | VERIFIED | Adds two target test modules plus measured Gate/mutation/ranking evidence. Assertions cover output, error, isolation and UI paths rather than merely no-raise behavior. | — |
| Manager-Database | #1887 `a7f4e626` | #1835 | NOT IMPLEMENTED | Twenty-seven evidence/receipt files only; no test or product change. It preserves the documented 45-unit partial result. | Not filed: offload restriction. |

## Critical judgment and limits

The repair-evidence-only PR pattern is not an implementation. It can substantiate an earlier change, but it cannot close an acceptance criterion that requires this PR to add a test or behavior. I used that distinction for the NOT IMPLEMENTED findings above. Confidence is high for evidence-only findings and moderate for PARTIAL findings, because the GitHub check-run readback does not always expose a uniquely named issue gate on the merge commit.

The unit instructions authorize filing/reopening issues, but the higher-priority offload rule prohibits GitHub writes (issues, comments, and PR state changes). Therefore no follow-up issues or reopen/comments were made. Each listed follow-up is actionable but unfiled.

Remaining in-window non-chore candidates after the 20-PR cap: Workflows #4390, #4440, #4438 and #4442; Doc-Lineage #169. Dependency-sync PRs were skipped as instructed.
