# D4 verify merged — 2026-11-01T21

**Window:** merges since `2026-10-31T09:06:50Z` (36 h before run) and after prior fleet ledger `2026-10-31T22:13:10Z` (`Manager-Database#1875`, `D4-verify-merged-2026-10-31T21`). **Fleet:** `SUPPORTED_REPOS` from `handoff.sh`, excluding Orchestrator. **Cap:** 20 PRs (oldest issue-linked first). **Offload:** GitHub writes (issues, comments, reopen, follow-up filing) not performed; follow-up column records intent only.

**Discovery:** 2 new issue-linked, non-chore merges after the ledger (5 candidates in window after ledger; 3 skipped as dependency chore). **Additional merges** in the full 36 h window were already adjudicated on `D4-verify-merged-2026-10-31T21`, template-sync batches, release/verifier maint without issue links, or deps-only sync.

**Skipped without verification:** `Travel-Plan-Permission#1717`, `Counter_Risk#1226`, `Portable-Alpha-Extension-Model#2455` (`deps: sync dev tool versions`, dependency chore); prior-run ledger for `Workflows#4355`, `Doc-Lineage#167`, `Manager-Database#1875`; chore/template/release/verifier merges as in prior D4 notes.

**Confidence:** High on squash-diff reads and local `pytest tests/test_coverage_round_1842_followup.py` (5 passed on merge tip `e5830db4`). High on `Ready#638`: post-run local `pytest -q -n 2` on merge tip → **1056 passed**, aggregate cov **95.75%**, both publication scripts in report with per-script line/branch counts; publication floor hook exited 0 (no `PUBLICATION COVERAGE` failures).

## Results

| Repo | PR | Issue | Verdict | Unmet / deferred criteria | Follow-up filed |
|------|-----|-------|---------|---------------------------|-----------------|
| Manager-Database | [#1876](https://github.com/stranske/Manager-Database/pull/1876) | [#1842](https://github.com/stranske/Manager-Database/issues/1842) | PARTIAL | Squash `e5830db4`: test-only `tests/test_coverage_round_1842_followup.py` (5 discriminating tests; offline badge asserts `httpx.Client` never constructed). **Unmet:** issue AC1 requires break-and-revert runs shown in the PR body for each new test — body defers to hosted Gate / `#1843` without transcripts for these five. AC2 ~180-unit Gate chunk: body documents continued shortfall vs fleet target (same honest partial pattern as `#1875`). | No (offload) |
| Ready | [#638](https://github.com/stranske/Ready/pull/638) | [#623](https://github.com/stranske/Ready/issues/623) | VERIFIED | Squash `4d9a07cf`: extends `pyproject.toml` / `[tool.coverage.run].include` to both publication scripts; `config/coverage-baseline.json` `publication_scripts` floors; `scripts/publication_coverage_gate.py` + `tests/conftest.py` session hook fail closed on line/branch regressions; `tests/test_coverage_baseline.py` pins measured set and exercises gate/subprocess/branch-removal paths; deliberate-break evidence in `docs/evidence/issue-623-publication-coverage.md` + JSON (`branch_removal_control`). | — |

**Summary:** 2 PRs verified in this run. **VERIFIED:** 1. **PARTIAL:** 1. **NOT IMPLEMENTED:** 0. **Belt ledger-only merges:** none. **Workflows#3391 belt defect:** none observed. **Reproduction blocks:** none on linked issues. **Follow-ups filed:** 0 (offload prohibits GitHub writes).

## Notes

- **Manager-Database #1842:** Closing merge is a follow-up slice after `#1843`; tests are not vacuous, but issue contract still wants explicit break-and-revert reporting in the PR body for each new test.
- **Ready #623:** PR body notes hosted pinned CI / current-head review as separate boundaries; local Gate-shaped pytest on tip (~14 min) confirms AC1 measurement + floors. Implementation in diff matches all three acceptance criteria and named test refs.
- **Dependency chores:** `#1717`, `#1226`, `#2455` reference issues in titles but are fleet dev-tool version sync only — out of scope per unit skip rules.

## Ledger

Next run: include merges after `2026-11-01T15:55:41Z` (`Ready#638`). Do not re-verify `#1876` or `#638`.
