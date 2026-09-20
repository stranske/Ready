# D4-verify-merged-2026-09-17T02

**Window:** merged ≥ 2026-09-15T14:56:28Z (36h before run start)  
**Repos:** 15 lane fleet (`SUPPORTED_REPOS`, excluding Orchestrator)  
**Cap:** 20 PRs (9 verified this run; 8 template-sync chores skipped; 2 in-window PRs already adjudicated in D4-verify-merged-2026-09-16T02)

## Summary

| Metric | Count |
|--------|------:|
| PRs verified | 9 |
| VERIFIED | 7 |
| PARTIAL | 2 |
| NOT IMPLEMENTED | 0 |
| Follow-ups filed | 2 |
| Rate-limit stop | No |

## Results

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| Manager-Mosaic | [#25](https://github.com/stranske/Manager-Mosaic/pull/25) | [#3](https://github.com/stranske/Manager-Mosaic/issues/3) | PARTIAL | Deliberate-break gate performed via test-local `_forbidden_infer_exit_on_gap` helper; no RED/GREEN evidence from mutating `derive_gaps` in `src/manager_mosaic/model.py` as issue requires | [#31](https://github.com/stranske/Manager-Mosaic/issues/31) |
| Manager-Mosaic | [#27](https://github.com/stranske/Manager-Mosaic/pull/27) | [#9](https://github.com/stranske/Manager-Mosaic/issues/9) | VERIFIED | — | — |
| Fine-Art-Archive | [#723](https://github.com/stranske/Fine-Art-Archive/pull/723) | [#722](https://github.com/stranske/Fine-Art-Archive/issues/722) | VERIFIED | — | — |
| Manager-Mosaic | [#28](https://github.com/stranske/Manager-Mosaic/pull/28) | [#11](https://github.com/stranske/Manager-Mosaic/issues/11) | VERIFIED | — | — |
| Workflows | [#3458](https://github.com/stranske/Workflows/pull/3458) | [#3364](https://github.com/stranske/Workflows/issues/3364) | VERIFIED | — | — |
| Workflows | [#3460](https://github.com/stranske/Workflows/pull/3460) | [Ready#560](https://github.com/stranske/Ready/issues/560) | VERIFIED | — | — |
| Manager-Mosaic | [#29](https://github.com/stranske/Manager-Mosaic/pull/29) | [#12](https://github.com/stranske/Manager-Mosaic/issues/12) | VERIFIED | — | — |
| Workflows | [#3452](https://github.com/stranske/Workflows/pull/3452) | [#1836](https://github.com/stranske/Workflows/issues/1836) | VERIFIED | — | — |
| Manager-Mosaic | [#30](https://github.com/stranske/Manager-Mosaic/pull/30) | [#13](https://github.com/stranske/Manager-Mosaic/issues/13) | PARTIAL | Deliberate-break demonstration for named thesis gate absent from diff and PR body | [#32](https://github.com/stranske/Manager-Mosaic/issues/32) |

## Skipped (not verified)

| Reason | Count | Examples |
|--------|------:|----------|
| Already verified in D4-verify-merged-2026-09-16T02 | 2 | Doc-Lineage #25/#29 |
| Template-sync chore | 8 | Trend_Model_Project #6035, Manager-Database #1680, Inv-Man-Intake #971, Pension-Data #900, learning-management-system #676, Doc-Lineage #27, Deliverable-Render #17, Manager-Mosaic #24 |

## Notable findings

1. **Manager-Mosaic #25–#30** — first substantive delivery burst for the new mosaic repo; six of six issue-linked PRs land real modules with non-vacuous tests. Only gap is deliberate-break transcript hygiene on #25 and #30.
2. **Workflows #3458** — strongest gate hygiene this window: YAML static assertions plus pasted RED/GREEN blocks for the 403/404 swallow branch.
3. **Workflows #3460** — upstream half of Ready#560; `_self_smoke` now glob-discoveries every bundled schema and maps `capability-bundle/v1`; tests live in `tests/contracts/` (appropriate for this script, though Ready#560 text names `tests/test_main.py`).
4. **Workflows #3452** — references campaign tracker #1836 (no issue AC); diff delivers stale-attempt fencing and authoritative-storage completion with 300+ lines of new `test_runner_lib` coverage. Verdict based on diff evidence.

## Evidence

Squash diffs, issue JSON, and follow-up bodies: `artifacts/verification/evidence/D4-verify-merged-2026-09-17T02/`

Local gate runs (merge SHAs on `[LOCAL_WORKSPACE]/*/main`):
- Manager-Mosaic: `pytest tests/test_model_validation.py tests/test_backplane_registry.py tests/test_evidence_validation.py tests/test_discrepancy_detection.py tests/test_thesis_monitoring.py -q` → **37 passed**
- Workflows: `pytest tests/workflows/test_generated_delivery_wakeup.py tests/contracts/test_validate_run_contract.py::test_self_smoke_loads_every_bundled_schema tests/contracts/test_validate_run_contract.py::test_capability_bundle_is_a_schema_validated_ingest_token tests/scripts/test_runner_lib.py::test_stale_workflow_completion_cannot_replace_new_reservation -q` → **10 passed**
