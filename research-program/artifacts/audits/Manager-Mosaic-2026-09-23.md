Scorecard: 5 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 6; journey: passes (validate → derive_gaps → discrepancy → thesis → evidence via API/CLI); surfaces unscored 2; closed-still-broken 0.

Issues filed: 2 — https://github.com/stranske/Manager-Mosaic/issues/53 (P1 core-function defect), https://github.com/stranske/Manager-Mosaic/issues/52 (PRODUCT_CONTRACT adoption).

# Manager-Mosaic Track D audit — 2026-09-23

**Tip:** `e0fe2405d34ed61c47d238ffd57cf16dcff05ee3`  
**Unit:** `D-audit-Manager-Mosaic--2026-09-23T09-11-14Z`

## Run report

Shallow-cloned `main` and ran Phase 0 scope from README, mosaic-core contract, prior `Code/Audits/Manager-Mosaic/` records, and refill table (3/4 open agent-ready ≤ threshold). Phase 1 bash: 78 tests passed (`pytest -q --no-cov`), `ruff` clean on prior CI pattern. Phase 1.5 scorecard exercised all six core functions via tests plus live varying-input probes (evidence in `Code/Audits/Manager-Mosaic/2026-09-23-SCORECARD.md`).

**Primary finding (filed #53):** `detect_numeric_discrepancies()` groups on raw `period` strings (`src/manager_mosaic/discrepancy.py:70-72`) while mosaic-core requires normalized period joins (`docs/contracts/mosaic-core-v1.md:59-60`) and thesis evaluation already normalizes quarters (`src/manager_mosaic/thesis.py:25-32`). Equivalent labels (`2024Q4` vs `Q4 2024`) with 12.0 vs 18.0 IRR return **no** discrepancy on the live tip; same values under one label flag correctly.

**Documentation gap (filed #52):** No in-repo `docs/PRODUCT_CONTRACT.md`; audit draft written to `Code/Audits/Manager-Mosaic/2026-09-23-product-contract.md`.

## Dedup / continuity

- 2026-09-19 staged bodies (inverted entry range, thesis same-period ID order, unparsed period labels) **not re-filed** — fixed on tip (#41–#43 merged); adversarial re-probe confirms violations now reported / `ValueError` raised as intended.
- Open follow-ups #31–#32 (deliberate-break evidence) left untouched — not duplicate defects.
- Synced `.github` / `tools` / design-system template excluded per prior scope.

## Verification

| Check | Result |
| --- | --- |
| `pytest -q --no-cov` | 78 passed |
| `issue_format.py` pre-flight | Both bodies agent-processable |
| `agents:formatted` on #52–#53 | Present after `agents:format` trigger |
| Agents Issue Intake workflow | success on both issues |

## Artifacts

- OUT (this file): `artifacts/audits/Manager-Mosaic-2026-09-23.md`
- Canonical: `Code/Audits/Manager-Mosaic/2026-09-23-{SCORECARD,audit-run,AUDIT_REPORT,surface-inventory,product-contract}.md`
- Issue bodies: `artifacts/audits/Manager-Mosaic-2026-09-23-issue-bodies/`

## Confidence

**High** on #53 (direct live repro, contract alignment). **High** on #52 (file absence). Would revise #53 if product policy intentionally requires callers to pre-canonicalize period strings before discrepancy detection (no such policy found in-repo; thesis module already canonicalizes internally).
