# D4 — verify merged PRs against issue acceptance criteria

Run: 2026-10-21 (36-hour window from **2026-10-20T06:53:51Z**; **16 PRs** verified — all in-window issue-linked non-chore merges in the lane fleet, oldest merged first; none were in a prior ledger for this unit id)

## Result

**16** non-chore merges with closing issue references in the window (excluding Orchestrator). No other supported repos had merges in the window. No ledger-only belt bookkeeping PRs. **No `Reproduction:` blocks** on linked issues; re-run/reopen not required.

| Repo | PR | Issue | Verdict | Unmet criteria / diff evidence | Follow-up filed |
|---|---:|---:|---|---|---|
| Workflows | [#4152](https://github.com/stranske/Workflows/pull/4152) | [#4150](https://github.com/stranske/Workflows/issues/4150) | VERIFIED | Squash diff: `tests/scripts/test_langsmith_fleet.py`, `tests/scripts/test_validate_template_sync.py` only; discriminating asserts/`pytest.raises` (no vacuous “does not raise”). PR documents break-and-revert and **170** focused units vs ~180 goal with unreachable-branch rationale for `repo_review_state` / `repo_review_docs_drift_scan` (issue AC accepts documented shortfall). Merge `2e1b77e50abb`. | N/A (offload: no GitHub writes) |
| Workflows | [#4154](https://github.com/stranske/Workflows/pull/4154) | [#4153](https://github.com/stranske/Workflows/issues/4153) | VERIFIED | Four test modules (`test_langchain_context_extractor`, `test_langchain_progress_reviewer`, `test_orchestrator_skill`, `test_ndjson_parser`); test-only diff; break-and-revert recorded in body. | N/A |
| Workflows | [#4155](https://github.com/stranske/Workflows/pull/4155) | [#3977](https://github.com/stranske/Workflows/issues/3977) | VERIFIED | Diff: `docs/ci/WORKFLOWS.md` + tightened `tests/workflows/test_gate_trigger_contract.py` (exact `pull_request.types` allowlist, `unlabeled` regression). YAML trigger fix cited as already landed in **#3983**; deliberate-break transcript in PR body. **48 h &lt;5% cancelled Gate runs** campaign AC not yet observable (~27 h post-merge). Merge `8e18fe9e911d`. | N/A |
| Workflows | [#4158](https://github.com/stranske/Workflows/pull/4158) | [#4156](https://github.com/stranske/Workflows/issues/4156) | VERIFIED | Six-target coverage round: tests across validator/run-contract/langchain/api/ledger/docs-drift; `docs/evidence/issue-4156/verification.json` evidence only. PR states focused aggregate short of ~180 CI units with rationale (issue partial-OK). Break-and-revert per target in body. | N/A |
| Workflows | [#4160](https://github.com/stranske/Workflows/pull/4160) | [#4159](https://github.com/stranske/Workflows/issues/4159) | VERIFIED | Test-only expansion (four modules); asserts + `pytest.raises`; break-and-revert in body. Merge `df108f233ea9`. | N/A |
| Portable-Alpha-Extension-Model | [#2414](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2414) | [#2413](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2413) | VERIFIED | `tests/…` Scenario Wizard navigation with Streamlit stubs (`pass` only in mock UI methods, not vacuous tests); asserts + `pytest.raises`. Break-and-revert in body. | N/A |
| Portable-Alpha-Extension-Model | [#2416](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2416) | [#2415](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2415) | VERIFIED | Three test files (reporting/paths/scenario comparison); strong assert/`raises` density; break-and-revert in body. | N/A |
| Portable-Alpha-Extension-Model | [#2419](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2419) | [#2417](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2417) | VERIFIED | `tests/test_coverage_round_2417.py`: nine ranked targets, **168** new-module missed-statement reduction documented (short of ~180; issue accepts partial). Break/revert proof for all nine mutations in body. | N/A |
| Workflows | [#4163](https://github.com/stranske/Workflows/pull/4163) | [#4161](https://github.com/stranske/Workflows/issues/4161) | VERIFIED | Four test modules; large assert surface (214+ new asserts); test-only; break-and-revert in body. | N/A |
| Portable-Alpha-Extension-Model | [#2420](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2420) | [#2418](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2418) | VERIFIED | Tests for PDF/reporting export branches; minimal `pyproject.toml` dev dependency line for test tooling; break-and-revert in body. | N/A |
| Portable-Alpha-Extension-Model | [#2422](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2422) | [#2421](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2421) | VERIFIED | Single new coverage test module; asserts + `pytest.raises`; break-and-revert in body. | N/A |
| Workflows | [#4168](https://github.com/stranske/Workflows/pull/4168) | [#4165](https://github.com/stranske/Workflows/issues/4165) | VERIFIED | Tests + **minimal prod fixes** in `scripts/analyze_api_rate_limits.py` and `scripts/repo_review_scorecard.py` (HTTPError close, `OverflowError` on reset time, `_clean_repo` dead-branch removal) each tied to failing tests in body. Focused 100% on both targets. Merge `ca04a9c2d096`. | N/A |
| Workflows | [#4169](https://github.com/stranske/Workflows/pull/4169) | [#4164](https://github.com/stranske/Workflows/issues/4164) | VERIFIED | Four test modules; test-only; break-and-revert in body. | N/A |
| Workflows | [#4172](https://github.com/stranske/Workflows/pull/4172) | [#4170](https://github.com/stranske/Workflows/issues/4170) | VERIFIED | Three test modules (docs/keepalive diagnostics); test-only; break-and-revert in body. | N/A |
| Workflows | [#4175](https://github.com/stranske/Workflows/pull/4175) | [#4173](https://github.com/stranske/Workflows/issues/4173) | VERIFIED | Five test modules; test-only; break-and-revert in body. | N/A |
| Workflows | [#4178](https://github.com/stranske/Workflows/pull/4178) | [#4176](https://github.com/stranske/Workflows/issues/4176) | VERIFIED | Eight test modules (fleet utility coverage); test-only; break-and-revert in body. Merge `e6c2d49fe44e`. | N/A |

## Test-gate, belt-ledger, reproduction, and campaign disposition

- **Belt ledger:** None of the sixteen PRs were ledger-only; rule 3b not triggered.
- **Reproduction:** No linked issue contained a runnable `Reproduction:` block.
- **Coverage rounds:** Squash diffs are discriminating tests (plus documented minimal prod fixes in #4168 and dev-deps in #2420). Issue contracts explicitly accept documented shortfall vs ~180 CI units (#4150, #4156, #2417, etc.); treated as **VERIFIED**, not scaffold-only.
- **#3977 campaign metric:** 48 h post-merge Gate cancellation rate not evaluated this run (merge 2026-10-20T10:57:30Z).
- **GitHub writes:** Unit instructions authorize follow-ups/reopens; **OFFLOAD WORKSPACE RULES** forbid them this run. No issues filed, commented, or reopened.

## Resume pointer

All issue-linked non-chore merges in **2026-10-20T06:53:51Z … run time** are in the checkpoint ledger below. Next run: advance the 36 h window; skip ledger keys already recorded under `D4-verify-merged-2026-10-21T18`.

**Confidence:** High for diff-evidenced tests and documented break-and-revert in PR bodies. Moderate on whole-repo Gate coverage deltas for coverage chunks—CI conclusions were not re-fetched; reliance on squash diff + issue partial-OK contract matches prior D4 passes.
