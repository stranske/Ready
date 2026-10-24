Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes (validate_payload → derive_gaps → fact keys opt-in → discrepancy → thesis → evidence → backplane CLI); surfaces unscored 2; closed-still-broken 0.

Issues filed: 0.

# Manager-Mosaic Track D audit — 2026-10-24

**Tip:** `f5c5c453561179011fd331cc72442ba5c303470e`  
**Unit:** `D-audit-Manager-Mosaic--2026-10-24T04-03-25Z`

## Run report

Refill trigger: prior scorecard dated 2026-09-23 (>30 days per `artifacts/audit-refill.md`). `main` advanced one commit since the 2026-09-23 tip (`52b7f4b` → `f5c5c45`, deps sync #120). The in-repo `docs/PRODUCT_CONTRACT.md` now defines **seven** core functions (CF-7 fact-key registry validation); this round scored all seven live with varying-input probes and drove the primary journey through API/CLI equivalents.

Eight-dimension reconciliation found no new verified defect outside the existing open repo-review backlog **#96** (`Store.from_dict` / payload validation), **#99** (contract-enforcement remediation), and **#101** (fact provenance — behavior present on tip per `tests/test_model_validation.py` and README delivery evidence while the issue remains open). Closed core-function issues **#53**, **#97**, **#98**, and **#100** were re-run on the current tip; reproductions do not show regressions.

## Dedup / continuity

- #52 (PRODUCT_CONTRACT adoption) closed; contract file is on tip.
- Interior template `.github/` and `design-system/` remain out of scope.
- No `REFUTED:` lines (no closed-issue claim contradicted on tip).

## Verification

| Check | Result |
| --- | --- |
| `pytest -q --no-cov` | 245 passed |
| `ruff check src tests` | passed |
| Contract probe slice (CF-1–CF-7) | 172 passed |
| CF-3 alias probe | `alias 1` / `same 0` |
| CF-7 strict typo claim | `UnregisteredFactKeyError` |
| `gh issue list` open product backlog | #96, #99, #101 (+ tracker #17, #1) |
| Issues filed this unit | 0 |

## Artifacts

- OUT (this file): `artifacts/audits/Manager-Mosaic-2026-10-24.md`
- Canonical: `Code/Audits/Manager-Mosaic/2026-10-24-{SCORECARD,AUDIT_REPORT,audit-run,00-repo-map,surface-inventory}.*`
- Checkpoint: `artifacts/audits/D-audit-Manager-Mosaic--2026-10-24T04-03-25Z.CHECKPOINT.md`

## Confidence

**High** that all seven contracted core functions work on `f5c5c45` (live probes + full test suite). **High** that filing zero issues is correct given open #96/#99/#101 cover the only confirmed-bug class left from `contract-enforcement-audit.md`. **Medium** that no latent interior defect escaped a focused pass — would change mind if a reproducible `file:line` defect appears outside those issues on a fresher tip.
