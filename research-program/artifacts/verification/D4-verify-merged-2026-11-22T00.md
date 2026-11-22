# D4 verification — 2026-11-22T00

**Outcome:** 8 **VERIFIED**, 2 **PARTIAL**, 10 **EXCLUDED** (of 20 PRs processed). **13** qualifying merges remain for the next run (API cap).

**Window:** `2026-11-20T12:41:00Z` through `2026-11-22T00:41:00Z` (36 hours).  
**Fleet:** 15 lane repos from `SUPPORTED_REPOS` (`stranske/Orchestrator` and `stranske/Collab-Admin` excluded). **57** merges in window; **14** template-sync-style titles skipped at enumeration; **33** merges referenced or closed at least one issue.

**Method:** Squash diffs via `gh pr diff`; acceptance criteria from `gh issue view`; belt-ledger rule applied (no ledger-only PRs in this batch). **Offload bound:** no `gh issue create`, comments, reopen, or label edits — follow-up filing deferred with draft text below.

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|---|---:|---|---|---|---|
| Workflows | [#4844](https://github.com/stranske/Workflows/pull/4844) | [#4784](https://github.com/stranske/Workflows/issues/4784) (tracker) | Excluded | N/A — tracker/checkpoint markdown only | No |
| Workflows | [#4846](https://github.com/stranske/Workflows/pull/4846) | historical evidence refs | Excluded | N/A — verifier evidence archive | No |
| Workflows | [#4852](https://github.com/stranske/Workflows/pull/4852) | [#4784](https://github.com/stranske/Workflows/issues/4784) (tracker) | Excluded | N/A — tracker/checkpoint | No |
| Workflows | [#4855](https://github.com/stranske/Workflows/pull/4855) | (peer PR refs) | Excluded | N/A — Gate wiring chore | No |
| Workflows | [#4867](https://github.com/stranske/Workflows/pull/4867) | [#3841](https://github.com/stranske/Workflows/issues/3841) (context) | Excluded | N/A — log archival, not issue delivery | No |
| trip-planner | [#2055](https://github.com/stranske/trip-planner/pull/2055) | [#960](https://github.com/stranske/trip-planner/issues/960) | **PARTIAL** | Open epic: map full canonical state model; quarantine non-canonical shortcuts; broader orchestration wiring beyond typed in-trip slice (issue still open; PR `Refs` only) | No (offload) |
| Trend_Model_Project | [#6240](https://github.com/stranske/Trend_Model_Project/pull/6240) | [#6239](https://github.com/stranske/Trend_Model_Project/issues/6239) | **VERIFIED** | — | No |
| Manager-Database | [#1943](https://github.com/stranske/Manager-Database/pull/1943) | [#1940](https://github.com/stranske/Manager-Database/issues/1940) | **VERIFIED** | — | No |
| learning-management-system | [#853](https://github.com/stranske/learning-management-system/pull/853) | [#851](https://github.com/stranske/learning-management-system/issues/851) | **VERIFIED** | — | No |
| Workflows | [#4880](https://github.com/stranske/Workflows/pull/4880) | [#296](https://github.com/stranske/Workflows/issues/296) (incidental) | Excluded | N/A — fixture archive under embedded Trend tree | No |
| Doc-Lineage | [#194](https://github.com/stranske/Doc-Lineage/pull/194) | [#193](https://github.com/stranske/Doc-Lineage/issues/193) | **VERIFIED** | — | No |
| Workflows | [#4883](https://github.com/stranske/Workflows/pull/4883) | [#4338](https://github.com/stranske/Workflows/issues/4338) (replay) | Excluded | N/A — maint-71 run-id routing; does not deliver #4338 omit-sync scope | No |
| Workflows | [#4886](https://github.com/stranske/Workflows/pull/4886) | peer PR refs | Excluded | N/A — cleanup tracker | No |
| Manager-Database | [#1944](https://github.com/stranske/Manager-Database/pull/1944) | [#1941](https://github.com/stranske/Manager-Database/issues/1941) | **VERIFIED** | — | No |
| trip-planner | [#2057](https://github.com/stranske/trip-planner/pull/2057) | [#2054](https://github.com/stranske/trip-planner/issues/2054) | **VERIFIED** | — | No |
| Workflows | [#4887](https://github.com/stranske/Workflows/pull/4887) | [#4551](https://github.com/stranske/Workflows/issues/4551) (evidence) | Excluded | N/A — Git fixture indexing | No |
| Portable-Alpha-Extension-Model | [#2529](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2529) | [#2526](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2526) | **PARTIAL** | Issue AC “clean developer install collection gate” in a **fresh** environment: diff adds `test_install_dev_selects_baseline_kit_extra` (Make dry-run + TOML parse) but no automated collect-only run proving nonzero baseline count without import errors | No (offload) |
| Inv-Man-Intake | [#1098](https://github.com/stranske/Inv-Man-Intake/pull/1098) | [#1097](https://github.com/stranske/Inv-Man-Intake/issues/1097) | **VERIFIED** | — | No |
| learning-management-system | [#852](https://github.com/stranske/learning-management-system/pull/852) | [#850](https://github.com/stranske/learning-management-system/issues/850) | **VERIFIED** | — | No |
| Workflows | [#4890](https://github.com/stranske/Workflows/pull/4890) | historical issue refs in tests | Excluded | N/A — optimizer workflow guard | No |

## Evidence notes (VERIFIED)

- **Trend_Model_Project#6240 / #6239:** Diff updates `validation.py` normalization for shipped HF Macro pack; `test_cli_validates_shipped_hf_macro_pack` asserts legacy `strategy_pack.curated is required` failure path and CLI exit 0/1 with field identification. Deliberate-break narrative recorded in PR cursor output.
- **Manager-Database#1943 / #1940:** `ui/dashboard.py` renders similar-manager panel via canonical `/managers/1/similar`; `test_dashboard_shows_peer_similarity_in_both_layouts` parametrizes `tabs`/`tabless`, asserts basis/counts, stale and empty states — not vacuous.
- **Manager-Database#1944 / #1941:** Baseline golden fixtures + `test_manager_search_baseline_records_observed_filter_reads`; `docs/PRODUCT_CONTRACT.md` MDB-2 evidence dated 2026-11-21 (core-function named; no `Reproduction:` block in issue).
- **LMS#853 / #851:** `src/lms/llm/api.py`, budgets/client changes; `test_daily_usage_reconciles_citation_fallback` asserts single provider call and receipt reconciliation.
- **LMS#852 / #850:** `export_import.py` redaction; `test_generated_source_visibility_export` asserts local-only generated sentinel absent from JSONL modes.
- **Doc-Lineage#194 / #193:** `edgar_ex10.py` provenance schema marker + CLI; `test_edgar_manifest_has_accurate_filing_provenance` and CLI help/validation tests.
- **Inv-Man-Intake#1098 / #1097:** `throughput.py` production batch path; `test_throughput_measures_production_real_byte_batch` plus production-mode regressions separate from smoke metrics.
- **trip-planner#2057 / #2054:** Large baseline adapter/coverage change; `test_non_transport_roundtrips_use_canonical_models` in squash diff with golden fixtures replacing unconditional success.

## PARTIAL — recommended follow-ups (not filed; offload)

1. **trip-planner#2055** (merge `d2ae8923e7a4`): Link to #960. Land remaining #960 tasks (canonical model map, shortcut quarantine, broader orchestration) or split a child issue so closure criteria match the merged slice (`tests/integrations/test_in_trip_planner_persistence.py`, `docs/contracts/canonical-state-seam.md`).
2. **Portable-Alpha-Extension-Model#2529** (merge `4a5eeb4a46bf`): Link to #2526. Add gate test that runs documented `python -m pytest --collect-only -q tests/baseline/` in a clean venv after `pip install -e '.[dev]'`, or amend #2526 AC to match the Make-recipe regression if that is the intended gate.

## Exclusions (classification)

Checkpoint and evidence PRs in Workflows mirror the 2026-11-21 run: textual `#N` mentions and open tracker #4784 are not treated as “merged == implemented.” **#4883** is the same pattern as **#4778** (replay/context citation). No belt ledger defect (no `status: done` on ledger-only commits) observed in this batch.

## Reproduction re-runs

No linked issue among the **VERIFIED** set contained a `Reproduction:` block requiring re-execution on this slice.

## Deferred queue (next run, oldest first among unprocessed)

`Workflows#4891`, `#4893`, `#4894`, `#4898`, `Portable-Alpha-Extension-Model#2530`, `Manager-Mosaic#163`, `Manager-Database#1942`, `Deliverable-Render#151`, `#150`, `trip-planner#2056`, `learning-management-system#854`, `Portable-Alpha-Extension-Model#2528`, `Travel-Plan-Permission#1759`, `Inv-Man-Intake#1099`, `Trend_Model_Project#6241` (13 PRs).

**Confidence:** high on VERIFIED/EXCLUDED rows grounded in squash diff + issue text; medium on **PARTIAL** portable-alpha gate interpretation (would upgrade to VERIFIED if CI or PR evidence shows a fresh-env collect-only run not captured in the diff). **Would change if:** GitHub `closingIssuesReferences` omitted a formal link, or merges landed after window end.