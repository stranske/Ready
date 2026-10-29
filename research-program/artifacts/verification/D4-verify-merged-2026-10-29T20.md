# D4 verify merged — 2026-10-29T20

**Window:** merges since `2026-10-28T08:47:00Z` (36 h before run). **Fleet:** `SUPPORTED_REPOS` from `handoff.sh`, excluding Orchestrator. **Cap:** 20 PRs (oldest issue-linked first). **Offload:** GitHub writes (issues, comments, reopen, follow-up filing) not performed; follow-up column records intent only.

**Discovery:** 22 non-chore merges in the window close or `Refs`/`Fixes`/`Closes` an issue; **20** verified this run (oldest first). **4** deferred (next ledger): `Counter_Risk#1221`, `#1216`, `#1220`, `#1217`.

**Skipped without verification (chore class):** `chore: sync workflow templates`, `deps:`, `chore(main): release`, and issue-unlinked product merges (e.g. Workflows verifier-shadow batch without `closingIssuesReferences` / ref lines).

**Confidence:** High on squash-diff reads for all 20 rows. High that the four deferred PRs are correctly queued. Medium on deliberate-break evidence for the fleet Python-floor batch (taken from PR bodies where cited, not re-run locally).

## Results

| Repo | PR | Issue | Verdict | Unmet / deferred criteria | Follow-up filed |
|------|-----|-------|---------|---------------------------|-----------------|
| Ready | [#652](https://github.com/stranske/Ready/pull/652) | [#640](https://github.com/stranske/Ready/issues/640) | NOT IMPLEMENTED | Squash diff (`ef954455`) only updates the `ci.yml` header comment (3.12→3.13/3.14 wording). No matrix pins, `publication-guard.yml`, or `tests/test_ci_python_standard.py::test_workflow_python_pins_follow_standard`. | No (intent: follow-up for #640 citing `ef954455`; offload) |
| Counter_Risk | [#1201](https://github.com/stranske/Counter_Risk/pull/1201) | [#1200](https://github.com/stranske/Counter_Risk/issues/1200) | PARTIAL | Diff delivers `coverage-python-version: '3.14'`, slow-job split, metrics, and `test_main_ci_measures_coverage_on_primary_runtime_only` (non-vacuous YAML parse). **Deferred:** pass number (2026-11-07) — no proof yet that every push-to-main job is ≤600 s. | No (monitoring; offload) |
| Counter_Risk | [#1207](https://github.com/stranske/Counter_Risk/pull/1207) | [#1189](https://github.com/stranske/Counter_Risk/issues/1189) | PARTIAL | Squash diff (`f3ab6c14`) shrinks `test_optional_input_provenance_hashes` inputs and documents before/after Gate timings; named test path is real. **Unmet:** Health 85 trailing-seven-day Gate p50 ≤10 min for seven consecutive days (#1189 still **OPEN**). | No (monitoring; offload) |
| Counter_Risk | [#1210](https://github.com/stranske/Counter_Risk/pull/1210) | [#1209](https://github.com/stranske/Counter_Risk/issues/1209) | VERIFIED | — | — |
| Doc-Lineage | [#162](https://github.com/stranske/Doc-Lineage/pull/162) | [#161](https://github.com/stranske/Doc-Lineage/issues/161) | VERIFIED | — | — |
| Inv-Man-Intake | [#1056](https://github.com/stranske/Inv-Man-Intake/pull/1056) | [#1055](https://github.com/stranske/Inv-Man-Intake/issues/1055) | VERIFIED | — | — |
| Travel-Plan-Permission | [#1710](https://github.com/stranske/Travel-Plan-Permission/pull/1710) | [#1709](https://github.com/stranske/Travel-Plan-Permission/issues/1709) | VERIFIED | — | — |
| Deliverable-Render | [#122](https://github.com/stranske/Deliverable-Render/pull/122) | [#120](https://github.com/stranske/Deliverable-Render/issues/120) | VERIFIED | — | — |
| Fine-Art-Archive | [#862](https://github.com/stranske/Fine-Art-Archive/pull/862) | [#861](https://github.com/stranske/Fine-Art-Archive/issues/861) | VERIFIED | — | — |
| Manager-Mosaic | [#138](https://github.com/stranske/Manager-Mosaic/pull/138) | [#137](https://github.com/stranske/Manager-Mosaic/issues/137) | VERIFIED | — | — |
| Pension-Data | [#1004](https://github.com/stranske/Pension-Data/pull/1004) | [#1003](https://github.com/stranske/Pension-Data/issues/1003) | VERIFIED | — | — |
| Portable-Alpha-Extension-Model | [#2448](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2448) | [#2447](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2447) | VERIFIED | — | — |
| Trend_Model_Project | [#6176](https://github.com/stranske/Trend_Model_Project/pull/6176) | [#6175](https://github.com/stranske/Trend_Model_Project/issues/6175) | VERIFIED | — | — |
| learning-management-system | [#810](https://github.com/stranske/learning-management-system/pull/810) | [#809](https://github.com/stranske/learning-management-system/issues/809) | VERIFIED | — | — |
| trip-planner | [#1952](https://github.com/stranske/trip-planner/pull/1952) | [#1951](https://github.com/stranske/trip-planner/issues/1951) | VERIFIED | — | — |
| Manager-Database | [#1871](https://github.com/stranske/Manager-Database/pull/1871) | [#1868](https://github.com/stranske/Manager-Database/issues/1868) | VERIFIED | Evidence-successor chain + `tests/test_python_floor.py::test_python_floor_is_3_13` and pyproject tool pins in diff (`9fe0ab4d`). | — |
| Ready | [#658](https://github.com/stranske/Ready/pull/658) | [#657](https://github.com/stranske/Ready/issues/657) | VERIFIED | Fleet-wide floor test (parametrized pyprojects) + pyproject pins (`8a371a3d`). | — |
| Workflows | [#4321](https://github.com/stranske/Workflows/pull/4321) | [#4319](https://github.com/stranske/Workflows/issues/4319) | VERIFIED | Root + `packages/stranske_pdf_extract` floors, lock header/regen, floor test (`3edf6a63`). | — |

**Summary:** 20 PRs verified (cap). **VERIFIED:** 17. **PARTIAL:** 2. **NOT IMPLEMENTED:** 1. **Belt ledger-only merges:** none. **Reproduction blocks:** none on linked issues. **Workflows#3391 belt defect:** none. **Follow-ups filed:** 0 (offload prohibits GitHub writes).

## Notes

- **Ready #652** `Refs #640` but does not implement the CI matrix migration; **Ready #658** closes the separate Python-floor issue **#657**. Do not conflate the two.
- **Counter_Risk #1201** now includes post-merge slow sharding in the squash diff (broader than the coverage-only slice seen on earlier D4 runs); pass-number timing remains the only deferred AC.
- **Fleet Python-floor closes** (rows marked VERIFIED without detail) each land `requires-python >=3.13`, ruff/black/mypy `py313`/`3.13`, and `tests/test_python_floor.py::test_python_floor_is_3_13` with substantive assertions (not vacuous).

## Ledger

Next run: resume with `Counter_Risk#1221`, `#1216`, `#1220`, `#1217` (merged after `Workflows#4321`). Re-check new merges after `2026-10-29T14:17:36Z`.
