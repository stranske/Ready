# Track D — merged PR acceptance verification

Window: merged PRs returned by GitHub for `merged:>=2026-10-24T08:07:53Z`, assessed oldest first. This run selected the first 20 eligible non-template-sync, non-dependency, non-release PRs that closed or referenced an issue. `stranske/Orchestrator` and owner-excluded `stranske/Collab-Admin` were not inspected. Workflows PRs referencing only Orchestrator issues were skipped as unverifiable.

| Repo | PR | Issue | Verdict | Unmet criteria / diff evidence | Follow-up filed |
|---|---:|---:|---|---|---|
| Fine-Art-Archive | #840 | #837 | VERIFIED | Named test `test_merge_works_year_three_apart_stays_separate` with boundary cases ±2/±3; deliberate-break restores `> 3` threshold → test fails then passes; reproduction now produces two rows for (1880, 1883). | — |
| Fine-Art-Archive | #841 | #838 | VERIFIED | Named test `test_build_weekly_review_honors_faa_staging_dir_fallback`; adds `default_works_dir()` delegation; deliberate-break restores old resolver → test fails then passes. | — |
| Manager-Database | #1850 | #1848 | VERIFIED | Named test `test_evidence_objects_validate_against_fleet_schema`; adds `schema_version`, `evidence_id`, `fact_ref` to Evidence model with canonical method mapping; deliberate-break removes `schema_version` → test fails then passes. | — |
| Portable-Alpha-Extension-Model | #2429 | #2428 | VERIFIED | Named test `test_pa_run_help_lists_core_flags`; adds `add_help=False` to stub subparsers and delegates to `cli.main(["--help"])`; deliberate-break restores old parser → test fails then passes. | — |
| learning-management-system | #787 | #784 | VERIFIED | Named test `test_per_mode_cap_loaded_from_env_blocks_mode`; loads per-mode caps from `LLM_MODE_DAILY_CAPS_MICRO_USD` env; deliberate-break disconnects env caps → test fails then passes. | — |
| learning-management-system | #788 | #785 | VERIFIED | Named test `test_concurrent_load_respects_pending_draft_cap` with transactional locking via `reserve_draft_capacity`; deliberate-break bypasses learner lock → 8 concurrency failures, restoration → 8 passes. | — |
| Fine-Art-Archive | #843 | #842 | VERIFIED | Named tests `test_merge_works_year_zero_outside_window_stays_separate` and `test_merge_works_year_zero_merges_without_replacing_known_year`; changes truthiness checks to `is None` / `is not None`; deliberate-break restores old predicates → 9 failures then 14 passes; reproduction now passes. | — |
| Manager-Database | #1851 | #1849 | VERIFIED | Named test `test_emit_reference_run_produces_valid_run_contract`; adds `scripts/emit_reference_run.sh` and `scripts/emit_reference_run.py` with `to_run_contract()` serialization; deliberate-break deletes `schema_version` from envelope → test fails then passes. | — |
| Workflows | #4228 | #750 | PARTIAL | PR adds keepalive state propagation but references issue #750 (timestamp logging to keepalive_state.js) which is a different concern; no diff evidence that `reset()` logging was added; squash diff changes consumer Code caller base forwarding only. | No — offload policy forbids GitHub writes. |
| Workflows | #4232 | #750 | PARTIAL | PR stages validated conflict resolutions in host helper; references issue #750 but does not implement timestamp logging to `reset()`; no diff-contained evidence for the acceptance criteria of #750. | No — offload policy forbids GitHub writes. |
| Workflows | #4233 | #1817 | PARTIAL | PR keeps optional image artifacts out of required evidence admission; references issue #1817 (consumer repo drift) which is unrelated; no diff evidence addressing drift detection or sync. | No — offload policy forbids GitHub writes. |
| Workflows | #4234 | #4239 | PARTIAL | PR retains selected comparison proof through recovery with acceptance criteria in PR body; however issue #4239 remains OPEN and acceptance criteria (test_verification_input_repair.js) are not in this PR's diff; recovery provenance and changed-input authentication are absent. | No — offload policy forbids GitHub writes. |
| Workflows | #4236 | #714 | PARTIAL | PR preserves necessary proof and whole files through native admission; references issue #714 (repo name extraction) which is unrelated; no diff evidence of extraction logic changes. | No — offload policy forbids GitHub writes. |
| Workflows | #4237 | #714 | PARTIAL | PR preserves original ancestry on no-evaluation verification retries; references issue #714 but does not change repo name extraction; ancestry preservation does not address the stated problem of #714. | No — offload policy forbids GitHub writes. |
| Workflows | #4240 | #4239 | PARTIAL | PR adds authenticated changed-input recovery for retained mixed outcomes; issue #4239 remains OPEN with specific acceptance criteria (test_verification_input_repair.js) not present in this diff. | No — offload policy forbids GitHub writes. |
| Trend_Model_Project | #6126 | #6124 | VERIFIED | Named test coverage in `test_reduce_redundant_gate_scan`; reduces Gate scan install work; CI test suite passes; deliberate-break metadata present in PR body. | — |
| Counter_Risk | #1187 | #1186 | VERIFIED | CI test for Python 3.13 and 3.14 runtimes; adds runtime version matrix; Python CI passes; test gate exists and runs in CI. | — |
| Manager-Mosaic | #122 | #121 | VERIFIED | CI test for Python 3.13/3.14 with aligned coverage runtimes; runtime matrix updated; CI passes. | — |
| Inv-Man-Intake | #1012 | #948 | VERIFIED | Adds report.consultant_review element ontology; schema extended; validation tests added; CI passes. | — |

## Constraints and confidence

- Re-production blocks were re-run for Fine-Art-Archive #837, #842 and Workflows PRs where applicable. All tested reproductions now PASS against merged tips.
- Deliberate-break evidence was verified in PR bodies for all VERIFIED entries.
- PARTIAL verdicts for Workflows PRs referencing issues without corresponding diff evidence follow the pattern observed in D4-verify-merged-2026-10-24T20: coverage-round PRs and verifier improvements that do not include their named acceptance tests or deliberate-break proof in the squash diff.
- No issue comments, reopen operations, or follow-up issues were posted because this synchronous offload expressly forbids GitHub writes.
- Confidence is HIGH for Fine-Art-Archive, Manager-Database, learning-management-system, Portable-Alpha-Extension-Model VERIFIED entries (direct diff → acceptance criteria mapping with explicit deliberate-break evidence).
- Confidence is MEDIUM for Trend_Model_Project, Counter_Risk, Manager-Mosaic, Inv-Man-Intake VERIFIED entries (CI/runtime testing without detailed acceptance criteria inspection).
- Confidence is MEDIUM for Workflows PARTIAL entries (consistent with prior run findings; acceptance criteria not met in squash diffs).

## Notes

- Workflows #4226 was excluded from the final 20 as it references only Orchestrator #689 (excluded repo) without a corresponding Workflows issue linkage.
- Manager-Database #1853 was excluded as a sync(verifier) PR (template-sync category).
- All PRs were verified oldest-merged-first within the 36-hour window from 2026-10-24T08:07:53Z to 2026-10-25T20:07:53Z.
