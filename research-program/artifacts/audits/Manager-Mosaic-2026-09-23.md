Scorecard: 6 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 6; journey: passes (validate → derive_gaps → discrepancy → thesis → evidence via API/CLI); surfaces unscored 2; closed-still-broken 0.

Issues filed: 2 — https://github.com/stranske/Manager-Mosaic/issues/53 (P1 core-function defect), https://github.com/stranske/Manager-Mosaic/issues/52 (PRODUCT_CONTRACT adoption).

# Manager-Mosaic Track D audit — 2026-09-23

**Tip:** `52b7f4b891d31beb8a2331667c857e59bab99666`  
**Unit:** `D-audit-Manager-Mosaic--2026-09-23T22-11-13Z` (continuation: scorecard-headline repair and live-tip re-verification)

## Run report

The original same-day audit was substantive, but the canonical scorecard omitted the mandatory parseable `Scorecard:` headline. In this continuation `git pull --ff-only` advanced `main` from `e0fe240` to `52b7f4b`. The period-alias discrepancy is now fixed: `src/manager_mosaic/discrepancy.py:63-89` groups parseable aliases through `period_chronology_key`, and `tests/test_discrepancy_detection.py:45-56` proves `2024Q4` and `Q4 2024` surface the same `numeric_delta`. Direct current-tip probe reports `alias 1` and `same 1`, so CF-3 changes from PARTIAL to WORKS and the scorecard is 6/6 WORKS.

**Prior primary finding (#53):** resolved in the checked-out source tree by commit `52b7f4b` (subject: `Fix quarter alias discrepancy grouping (#54)`). This confirms source behavior, not remote #53/#54 lifecycle status; `gh` is unauthenticated here.

**Documentation gap (filed #52):** No in-repo `docs/PRODUCT_CONTRACT.md`; audit draft written to `Code/Audits/Manager-Mosaic/2026-09-23-product-contract.md`.

## Dedup / continuity

- 2026-09-19 staged bodies (inverted entry range, thesis same-period ID order, unparsed period labels) **not re-filed** — fixed on tip (#41–#43 merged); adversarial re-probe confirms violations now reported / `ValueError` raised as intended.
- Open follow-ups #31–#32 (deliberate-break evidence) left untouched — not duplicate defects.
- Synced `.github` / `tools` / design-system template excluded per prior scope.

## Verification

| Check | Result |
| --- | --- |
| `pytest -q --no-cov` | 78 passed; 2 failed only because this sandbox forbids a workflow fixture's hard-coded macOS temporary path, not due to a repository assertion failure |
| `ruff check src tests` | passed |
| Targeted product regressions | 29 passed (`tests/test_discrepancy_detection.py`, `tests/test_thesis_monitoring.py`) |
| Prior #53 reproduction on tip | `alias 1` / `same 1`; fixed in source |
| Canonical scorecard headline | Missing; attempted backfill was sandbox-denied because `Code/Audits` is outside writable roots |
| `gh issue list` / `gh run list` | unknown — CLI requires authentication; no format-guard verdict claimed |
| Additional dimension sweep | No new verified defect at current tip; 0 new issues filed |

## Artifacts

- OUT (this file): `artifacts/audits/Manager-Mosaic-2026-09-23.md`
- Canonical: `Code/Audits/Manager-Mosaic/2026-09-23-{SCORECARD,audit-run,AUDIT_REPORT,surface-inventory,product-contract}.md`
- Issue bodies: `artifacts/audits/Manager-Mosaic-2026-09-23-issue-bodies/`

## Confidence

**High** that the former CF-3 defect is fixed in the current tip: the direct alias probe and the new regression test agree. **High** that the canonical scorecard headline is absent. **Low** confidence in any GitHub lifecycle assertion because `gh` is unauthenticated. The remaining operational blocker is authority to write the canonical `Code/Audits` scorecard.
