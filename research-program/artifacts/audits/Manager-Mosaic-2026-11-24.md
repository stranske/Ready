Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes (validate_payload → derive_gaps → fact keys opt-in → discrepancy → thesis → evidence → backplane CLI); surfaces unscored 0; closed-still-broken 0.

Issues filed: 0.

# Manager-Mosaic Track D audit — 2026-11-24

**Tip:** `6eb1c5e0c063792e2a331632608b7581081dc223`  
**Unit:** `D-audit-Manager-Mosaic--2026-11-24T04-25-42Z`  
**Prior scorecard:** 2026-10-24 @ `f5c5c45` (same seven CF rows; open backlog then #96/#99/#101)

## Run report

Refill trigger (`artifacts/audit-refill.md`): scorecard age >30d and open agent-ready supply collapsed after #96, #99, and #101 closed (only tracker issues #1 and #17 remain open). Tip moved from `f5c5c45` to `6eb1c5e` (workflow template sync); product paths unchanged.

### Phase 1.5 — scorecard

| ID | Score | Varying-input / probe |
| --- | --- | --- |
| CF-1 | WORKS | `validate_payload` tamper increases violations; `Store.from_dict` raises on structural damage (`tests/test_payload_collects_structural_and_independent_semantic_defects`) |
| CF-2 | WORKS | `derive_gaps` leaves entry status unchanged (`tests/test_derive_gaps_leaves_status_unchanged`) |
| CF-3 | WORKS | Live: `2024Q4`/`Q4 2024` alias → 1 group; identical values → 0 |
| CF-4 | WORKS | IRR 12.0 → `supported`, 8.0 → `contradicted` |
| CF-5 | WORKS | Document-identity combined defects (`tests/test_document_identity_combined_defects_returns_all_three_violations`) |
| CF-6 | WORKS | `validate_run_contract.py` valid fixture exit 0 / invalid exit 1 |
| CF-7 | WORKS | `strict_fact_keys=True` typo → `UnregisteredFactKeyError` |

Primary journey driven via library entry points (no UI). Full suite: `pytest -q --no-cov` → **285 passed**; contract slice → **196 passed**.

### Closed-issue reproduction (tip)

| Issue | Concern | Tip result |
| --- | --- | --- |
| #53 | Quarter alias grouping | PASS (`test_detect_numeric_discrepancies_groups_equivalent_period_labels`) |
| #96 | Payload validation before construction | PASS (payload tests) |
| #97 | Evidence document-identity in package | PASS |
| #98 | Canonical discrepancy IDs | PASS (`test_discrepancy_id_and_display_are_permutation_stable`) |
| #100 | Fact-key registry opt-in | PASS (`tests/test_fact_key_registry.py`) |
| #101 | Fact provenance through results | PASS (model/discrepancy/thesis tests) |

### Surface inventory

Product entry points unchanged from `2026-10-24-surface-inventory.txt`. Interior rows re-scored: `design-system/ds_streamlit.py` (py_compile); `.github/workflows/*` (35 YAML, 0 parse errors); fleet `scripts/*.py` + `tools/*.py` (45 files, py_compile 0 errors) — not core-function surfaces.

### Eight dimensions — reconciliation

No new verified defect with `file:line` evidence outside delivered work. Candidate “stale `contract-enforcement-audit.md` confirmed-bug rows” **withdrawn**: lines 1–8 document historical snapshot preservation; `tests/test_repo_hygiene.py:161` requires `"Pending delivery"` in the report by design.

## Dedup / continuity

- Open product backlog: none (trackers #1, #17 only).
- No `REFUTED:` lines.

## Verification

| Check | Result |
| --- | --- |
| `pytest -q --no-cov` | 285 passed |
| `ruff check src tests` | passed |
| Contract probe slice | 196 passed |
| `gh run list` ci.yml | success @ 6eb1c5e |
| Issues filed | 0 |

## Artifacts

- OUT: `artifacts/audits/Manager-Mosaic-2026-11-24.md`
- Checkpoint: `artifacts/audits/D-audit-Manager-Mosaic--2026-11-24T04-25-42Z.CHECKPOINT.md`
- Canonical: `Code/Audits/Manager-Mosaic/2026-11-24-*`

## Confidence

**High** that all seven contracted core functions work on `6eb1c5e` and that closed remediation issues remain fixed. **High** that zero filings is correct — the refill depleted open agent-ready supply by closing backlog, not by hiding defects. **Medium** on latent bugs in synced fleet trees; would change mind with a reproducible defect on a product entry point after a non-sync commit.