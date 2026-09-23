Scorecard: 6 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 6; journey: passes (validate → derive_gaps → discrepancy → thesis → evidence via API/CLI); surfaces unscored 2; closed-still-broken 0.

Issues filed: 0 (this unit). Same-day prior unit filed #52, #53; #53 closed via PR #54 on tip `52b7f4b`.

REFUTED: https://github.com/stranske/Manager-Mosaic/issues/53 — live reproduction on tip `52b7f4b` returns one discrepancy for `2024Q4` vs `Q4 2024` (`alias 1`), matching the same-label control (`same 1`).

# Manager-Mosaic Track D audit — 2026-09-23

**Tip:** `52b7f4b891d31beb8a2331667c857e59bab99666`  
**Unit:** `D-audit-Manager-Mosaic--2026-09-23T22-11-13Z` (attempt 2: canonical scorecard headline + live-tip re-verification)

## Run report

The refill trigger fired because `Code/Audits/Manager-Mosaic/2026-09-23-SCORECARD.md` lacked the mandatory parseable `Scorecard:` headline (fixed in attempt 2). `main` is unchanged since attempt 1 at `52b7f4b` (PR #54: quarter alias grouping via `src/manager_mosaic/periods.py` and `src/manager_mosaic/discrepancy.py:63-89`). CF-3 is **WORKS**: live probe `alias 1` / `same 1`; `tests/test_discrepancy_detection.py:45-56` asserts equivalent labels compete.

Eight-dimension reconciliation on the four files touched by #54 found no new verified, non-duplicate defect. Open product backlog from audits remains #52 (PRODUCT_CONTRACT adoption) and deliberate-break evidence follow-ups #31–#32; open issues #55–#64 are verify:compare / review-comment hygiene, not unreproduced core-function bugs.

## Dedup / continuity

- 2026-09-19 staged defects (inverted entry range, thesis ID order, unparsed period labels) remain fixed on tip; not re-filed.
- #53 filed 2026-09-23 morning; closed after #54 merge; reproduction refuted on current tip (see REFUTED line).
- Synced `.github` / `tools` / design-system template excluded per prior scope.

## Verification

| Check | Result |
| --- | --- |
| `pytest -q --no-cov` | 80 passed |
| `ruff check src tests` | passed |
| Core-function slice | 54 passed (validation, gaps, discrepancy, thesis, evidence, backplane CLI) |
| CF-3 alias probe | `alias 1` / `same 1` |
| Canonical scorecard headline | present in `Code/Audits/Manager-Mosaic/2026-09-23-SCORECARD.md` line 3 |
| `gh issue list` / format guard | #52 open (`agents:formatted`); #53 closed; intake format-guard runs success (`35854490072`, `35869131704`) |
| Issues filed this unit | 0 |

## Artifacts

- OUT (this file): `artifacts/audits/Manager-Mosaic-2026-09-23.md`
- Canonical: `Code/Audits/Manager-Mosaic/2026-09-23-{SCORECARD,AUDIT_REPORT,audit-run,product-contract,surface-inventory}.*`
- Issue bodies (prior unit): `artifacts/audits/Manager-Mosaic-2026-09-23-issue-bodies/`

## Confidence

**High** that all six core functions work on `52b7f4b` (live probes + 80 tests). **High** that the canonical scorecard now has a parseable headline for `newest_scorecard`. **High** that #53’s defect claim is obsolete on tip (would change mind if `alias` probe returned 0 again). **Medium** that no interior defect escaped a same-day second pass — the repo is small and recently heavily audited; a latent bug in unscored template surfaces remains possible but out of scope.
