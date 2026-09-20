## Why

`src/doc_lineage/harvest/edgar_ex10.py:290-299` creates the final output directory and writes each EX-10 artifact before `src/doc_lineage/harvest/edgar_ex10.py:301-305` validates and writes the manifest. This is a current publication break: with a fixture containing two EX-10 records where the first payload exists and the second is missing, `harvest_edgar_ex10` raises after the first file is already published in the final tree, while no manifest exists. A failed run therefore leaves a partial final mirror that later operators cannot distinguish from an interrupted valid harvest by inspecting the artifact tree alone.

## Scope

Publish EDGAR harvest output atomically: a failed multi-exhibit run must leave no newly published final artifacts or final manifest.

## Non-Goals

- Do not change EX-10 parsing criteria or the SEC rate-limit policy.
- Do not delete a pre-existing successful harvest directory as part of failure cleanup without an explicit replacement policy.
- Scaffold-only completion does NOT count: writing a temporary manifest while still exposing the first downloaded artifact at a final output path after a later fetch failure is a failure of this issue.

## Tasks

- [ ] Rework `src/doc_lineage/harvest/edgar_ex10.py:290` to stage exhibit bytes and the validated manifest outside the final publication paths, then promote them only after every exhibit is available and the artifact manifest version 1 validation succeeds.
- [ ] Add a failure-atomicity test in `tests/harvest/test_edgar_ex10_offline.py` with two EX-10 fixture records where the second payload is absent, asserting no new final artifact and no final manifest remain in the output directory.
- [ ] Preserve the existing successful offline-manifest behavior in `tests/harvest/test_edgar_ex10_offline.py:37-57`.

## Acceptance Criteria

- [ ] `pytest tests/harvest/test_edgar_ex10_offline.py` passes, including the new two-exhibit failure case and the existing successful mirror-compatible manifest assertions.
- [ ] Deliberate-break gate: temporarily restore direct final-path writing in `src/doc_lineage/harvest/edgar_ex10.py:290`; the new failure-atomicity test must fail after the first fixture artifact appears despite the missing second payload. Restore staged publication before requesting review.

## Implementation Notes

- Verified current evidence at `src/doc_lineage/harvest/edgar_ex10.py:190` and `src/doc_lineage/harvest/edgar_ex10.py:290`.
- Current offline reproduction left the first artifact after the second fixture failed, and did not write the final manifest.
