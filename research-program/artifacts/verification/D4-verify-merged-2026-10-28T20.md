# D4 verify merged — 2026-10-28T20

**Window:** merges since `2026-10-27T08:30:00Z` (36 h before run). **Fleet:** `SUPPORTED_REPOS` from `handoff.sh`, excluding Orchestrator. **Cap:** 20 PRs (oldest issue-linked first). **Offload:** GitHub writes (issues, comments, reopen, follow-up filing) not performed; follow-up column records intent only.

**Discovery:** 19 non–template-sync/deps-title merges in the window across the fleet; **2** close or `Refs #` an issue (see table). **17** `Workflows` product merges (4285–4308) carry no `Fixes`/`Closes`/`Refs` line and no `closingIssuesReferences` — out of scope for this track (belt/local_request work without issue binding).

**Skipped without verification (chore class):** all `chore: sync workflow templates`, `deps:`, and `chore(main): release` merges in the window (~90+).

**Confidence:** High on squash-diff reads for the two verified rows. High that the Workflows batch is correctly excluded (no issue link in GitHub metadata or standard ref lines). Medium on whether narrative-only `#NNNN` mentions (e.g. PR bodies citing Orchestrator #982 or frozen case ids #3850/#4265) should ever count as “reference”; this run treats them as **not** in scope because they do not close nor use `Refs`/`Fixes`/`Closes`.

## Results

| Repo | PR | Issue | Verdict | Unmet / deferred criteria | Follow-up filed |
|------|-----|-------|---------|---------------------------|-----------------|
| Ready | [#652](https://github.com/stranske/Ready/pull/652) | [#640](https://github.com/stranske/Ready/issues/640) | NOT IMPLEMENTED | Squash diff (`ef954455`) touches only `.github/workflows/ci.yml` header comment (3.12→3.13/3.14 wording). Issue tasks require matrix pins in `ci.yml` and `pr-00-gate.yml`, `publication-guard.yml` 3.14, `tests/test_ci_python_standard.py`, and Gate legs on 3.13/3.14 — none in diff. Named gate `test_workflow_python_pins_follow_standard` absent. Issue remains **OPEN**. | No (intent: file follow-up naming unmet tasks + merge `ef954455`; offload) |
| Counter_Risk | [#1201](https://github.com/stranske/Counter_Risk/pull/1201) | [#1200](https://github.com/stranske/Counter_Risk/issues/1200) | PARTIAL | Squash diff adds `coverage-python-version: '3.14'` in `.github/workflows/ci.yml` and `tests/test_ci_gate_budget.py::test_main_ci_measures_coverage_on_primary_runtime_only` asserting it equals `primary-python-version` (non-vacuous). Deliberate-break evidence in PR body. **Deferred:** pass number (2026-11-07) — no job duration ≤600 s proof on main yet. | No (monitoring; offload) |

**Summary:** 2 issue-linked PRs verified (under 20 cap). **VERIFIED:** 0. **PARTIAL:** 1. **NOT IMPLEMENTED:** 1. **Belt ledger-only merges:** none observed. **Reproduction blocks:** none on linked issues. **Workflows#3391 belt defect:** none observed. **Follow-ups filed:** 0 (offload prohibits GitHub writes).

## Notes

- **Ready #652** is a comment-only partial toward #640; it explicitly `Refs #640` but does not close it. Treat as scaffold-relative-to-issue, not a delivered matrix migration.
- **Counter_Risk #1201** closes #1200 with real CI wiring + regression test; timing pass number is the only outstanding acceptance line (same class as prior D4 timing deferrals).
- **Workflows** merges in-window are substantial verifier/sync work but lack issue linkage in GitHub; a future run could extend discovery rules if the owner wants belt PRs verified against ledger tasks instead of issue AC.

## Ledger

Next run: resume after `Counter_Risk#1201`. Re-check new merges after `2026-10-28T12:31:38Z` and any PRs that gain `Fixes`/`Refs`/`closingIssuesReferences`.
