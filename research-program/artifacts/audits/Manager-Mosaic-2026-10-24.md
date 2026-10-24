Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes (validate_payload → derive_gaps → fact keys opt-in → discrepancy → thesis → evidence → backplane CLI); surfaces unscored 0; closed-still-broken 0.

Issues filed: 0.

# Manager-Mosaic Track D audit — 2026-10-24

**Tip:** `f5c5c453561179011fd331cc72442ba5c303470e`  
**Unit:** `D-audit-Manager-Mosaic--2026-10-24T20-01-15Z`

## Run report

Refill trigger (`artifacts/audit-refill.md`): the 2026-10-24 morning scorecard cleared all seven contracted core functions but left **two interior inventory rows unscored** (`design-system/ds_streamlit.py`, `.github/workflows/*`), unchanged since 2026-09-23 — so coverage debt stayed at 2. This unit scores those rows as **interior (non–core-function)** with live checks, bringing `surfaces unscored` to **0**. `main` is unchanged at `f5c5c45` (deps sync #120).

Interior scoring evidence:

| Surface | Classification | Probe | Result |
| --- | --- | --- | --- |
| `design-system/ds_streamlit.py` | Interior — synced design-system helpers; no Streamlit app entry in this repo (`streamlit_app/` absent; README documents shared patterns only) | `python3 -m py_compile design-system/ds_streamlit.py` | Syntax OK; lazy `import_module("streamlit")` — product contract does not claim a UI |
| `.github/workflows/*` | Interior — fleet CI/agents workflows synced with consumer template; not a user-facing mosaic capability | `yaml.safe_load` on 35 `*.yml` under `.github/workflows/` | 0 parse errors; `ci.yml` and `backplane-conformance.yml` present; recent `gh run list` green on keepalive/PR-health |

Core functions CF-1–CF-7 were re-exercised on the tip: CF-3 alias grouping `alias 1` with identical-value control `0`; CF-4 IRR 12.0 → `supported`, 8.0 → `contradicted`; CF-7 strict typo → `UnregisteredFactKeyError`. Full suite `pytest -q --no-cov` → 245 passed; contract slice → 149 passed.

Eight-dimension reconciliation found no new verified defect outside open repo-review **#96** (payload validation / `Store.from_dict`), **#99** (contract enforcement remediation), and **#101** (fact provenance — behaviour covered on tip per `tests/test_model_validation.py` and `docs/evidence/issue-101/README.md` while the tracking issue remains open). Closed core-function issues **#53**, **#97**, **#98**, and **#100** were re-run; no regressions.

## Dedup / continuity

- #52 (PRODUCT_CONTRACT adoption) closed; contract on tip with CF-7.
- Interior template paths remain out of product defect scope; now **scored**, not unscored.
- No `REFUTED:` lines.

## Verification

| Check | Result |
| --- | --- |
| `pytest -q --no-cov` | 245 passed |
| `ruff check src tests` | passed |
| Contract probe slice | 149 passed |
| CF-3 alias / control | `alias 1` / `control 0` |
| CF-4 thesis varying IRR | supported → contradicted |
| Interior: ds_streamlit compile | OK |
| Interior: workflow YAML parse | 35 files, 0 errors |
| `gh issue list` open product backlog | #96, #99, #101 |
| Issues filed this unit | 0 |

## Artifacts

- OUT (this file): `artifacts/audits/Manager-Mosaic-2026-10-24.md`
- Checkpoint: `artifacts/audits/D-audit-Manager-Mosaic--2026-10-24T20-01-15Z.CHECKPOINT.md`
- Prior canonical (morning unit): `Code/Audits/Manager-Mosaic/2026-10-24-*` (headline there still shows unscored 2 until owner mirrors this unit)

## Confidence

**High** that all seven core functions work on `f5c5c45` and that interior surfaces are correctly classified (not product entry points). **High** that coverage debt is now 0 for unscored surfaces. **High** that filing zero issues remains correct given open #96/#99/#101. **Medium** on latent interior bugs inside synced template trees — would change mind with a reproducible product-path defect on a fresher tip.
