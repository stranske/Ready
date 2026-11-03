# D4 merged-PR verification — 2026-11-03T21

**Outcome:** 20 eligible PRs inspected (cap: 20): **6 VERIFIED**, **12 PARTIAL**, **2 NOT IMPLEMENTED**. Squash diffs and issue acceptance criteria were read; no GitHub secondary rate limit was hit.

**Window:** merges on `SUPPORTED_REPOS` (excluding Orchestrator) with `mergedAt >= 2026-11-02T09:22:00Z` through run time, skipping template-sync / dependency / release / bootstrap chores. Oldest eligible first; ledger in `D4-verify-merged-2026-11-03T21.CHECKPOINT.md`.

**Offload constraint:** this synchronous offload forbids issue comments, reopen, and follow-up filing. Rows below note what a writer-enabled run should file.

| Repo | PR | Issue | Verdict | Unmet criteria / evidence | Follow-up filed |
|---|---:|---:|---|---|---|
| Travel-Plan-Permission | [#1722](https://github.com/stranske/Travel-Plan-Permission/pull/1722) | [#1720](https://github.com/stranske/Travel-Plan-Permission/issues/1720) | **VERIFIED** | Squash diff updates `README.md`, `docs/local-testing-plan.md`, and adds `test_operator_docs_do_not_reference_legacy_portal_requests_paths` with `/portal/requests` assertions. Named gate passed on main tip (`pytest …::test_operator_docs_do_not_reference_legacy_portal_requests_paths`, 1 passed). | — |
| Inv-Man-Intake | [#1062](https://github.com/stranske/Inv-Man-Intake/pull/1062) | [#1061](https://github.com/stranske/Inv-Man-Intake/issues/1061) | **VERIFIED** | Diff replaces runbook quickstart with staging + `inv-man-ingest` and adds `tests/docs/test_headless_ingest_runbook.py`, which executes the documented bash fence and asserts exit 0 and `run.json`. **`pytest tests/docs/test_headless_ingest_runbook.py` passed on merged tip** (prior D4 used wrong module invocation, not the runbook command). | — |
| trip-planner | [#1963](https://github.com/stranske/trip-planner/pull/1963) | [#1962](https://github.com/stranske/trip-planner/issues/1962) | **VERIFIED** | Diff adds `"origin": "Seattle"` in `_create_trip`, contract doc note, deliberate-break evidence doc, and regression tests asserting TP3 is not `FABRICATED` without monkeypatching scenario search. | — |
| Travel-Plan-Permission | [#1723](https://github.com/stranske/Travel-Plan-Permission/pull/1723) | [#1721](https://github.com/stranske/Travel-Plan-Permission/issues/1721) | **VERIFIED** | Diff adds PP8 row, updates PP4 status, extends `tests/python/test_product_contract.py` for PP1–PP8 presence and non–`NOT-EXERCISED` PP4/PP8. Deliberate-break steps not re-run here; behavior is asserted in new tests, not no-raise stubs. | — |
| Workflows | [#4395](https://github.com/stranske/Workflows/pull/4395) | [#4165](https://github.com/stranske/Workflows/issues/4165) | **PARTIAL** | Squash diff only touches `scripts/analyze_api_rate_limits.py` (`_clean_repo` branches) and extends `tests/scripts/test_repo_review_scorecard.py`. Issue also requires new coverage for `analyze_api_rate_limits.py` in this round; no new/changed `test_analyze_api_rate_limits.py` hunk in this merge. Break-and-revert and per-target `--cov` deltas not independently replayed. | No — offload prohibits writes; cite merge + missing analyze-api test delta. |
| Workflows | [#4399](https://github.com/stranske/Workflows/pull/4399) | [#3964](https://github.com/stranske/Workflows/issues/3964) | **PARTIAL** | Diff adds `test_sync_test_dependencies.py` and `test_issue_pr_context.py` only. Issue lists `tools/embedding_provider.py` as a target; no test file for it in squash diff. Coverage/break-revert proof not independently run. | No — offload. |
| Portable-Alpha-Extension-Model | [#2457](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2457) | [#2421](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2421) | **PARTIAL** | Large test-only diff (~60k bytes) aligned with a coverage round; named targets not mapped line-by-line in this run; PR-body coverage before/after and deliberate-break transcripts not independently reproduced. | No — offload. |
| Workflows | [#4409](https://github.com/stranske/Workflows/pull/4409) | [#4239](https://github.com/stranske/Workflows/issues/4239) | **NOT IMPLEMENTED** | Issue requires production changes in `.github/scripts/verification_event.js`, verifier workflow publication, and `tools/verifier_event_recovery.py`. Squash diff is **fixtures + `tests/scripts/test_verification_input_repair.js` only** — no production admission path in merge evidence. | No — offload; writer should file against #4239 citing missing JS/workflow hunks. |
| Portable-Alpha-Extension-Model | [#2458](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2458) | [#2403](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2403) | **PARTIAL** | Test additions for listed modules; full target list and break-revert proof not independently verified in this run. | No — offload. |
| Workflows | [#4408](https://github.com/stranske/Workflows/pull/4408) | [#4137](https://github.com/stranske/Workflows/issues/4137) | **NOT IMPLEMENTED** | **`gh pr diff` is empty** (`additions: 0`, `changedFiles: 0`, merge `9590d248…`). No coverage tests or script changes landed; closer repair merged a no-op. | No — offload; reopen or replace merge for #4137. |
| Portable-Alpha-Extension-Model | [#2459](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2459) | [#2382](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2382) | **PARTIAL** | Very large diff; treated as coverage round — AC mapping and cov deltas not completed within cap. | No — offload. |
| Manager-Database | [#1878](https://github.com/stranske/Manager-Database/pull/1878) | [#1833](https://github.com/stranske/Manager-Database/issues/1833) | **PARTIAL** | Single-file test diff; issue lists four adapter/API targets — not all mappable from file list alone; break-revert not replayed. | No — offload. |
| trip-planner | [#1965](https://github.com/stranske/trip-planner/pull/1965) | [#1964](https://github.com/stranske/trip-planner/issues/1964) | **VERIFIED** | Diff refreshes TP3–TP7 status cells and gap bullets from probe semantics and adds `tests/docs/test_product_contract_probe_drift.py` CI guard — directly addresses all three issue tasks. | — |
| Portable-Alpha-Extension-Model | [#2461](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2461) | [#2360](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2360) | **PARTIAL** | Tests for `Scenario_Wizard.py`; whole-issue coverage AC and deliberate-break proof not independently run. | No — offload. |
| Manager-Database | [#1879](https://github.com/stranske/Manager-Database/pull/1879) | [#1794](https://github.com/stranske/Manager-Database/issues/1794) | **PARTIAL** | Squash diff adds only a few lines to existing `tests/test_chat_coverage_gap.py` (timeout edge cases). Issue scopes 117 missing units on `api/chat.py`; merge evidence is a minimal increment, not demonstrated full coverage closure. | No — offload. |
| Manager-Database | [#1880](https://github.com/stranske/Manager-Database/pull/1880) | [#1830](https://github.com/stranske/Manager-Database/issues/1830) | **PARTIAL** | Multi-file test diff (~1.7M bytes); coverage-round AC and break-revert not independently replayed. | No — offload. |
| Fine-Art-Archive | [#866](https://github.com/stranske/Fine-Art-Archive/pull/866) | [#816](https://github.com/stranske/Fine-Art-Archive/issues/816) | **PARTIAL** | Test additions for listed `src/fine_art_archive/*` modules; per-target cov and break-revert not verified here. | No — offload. |
| Workflows | [#4403](https://github.com/stranske/Workflows/pull/4403) | [#4005](https://github.com/stranske/Workflows/issues/4005) | **PARTIAL** | Diff adds `test_reference_packs.py` and `test_issue_formatter.py` only; issue also names `scripts/api_client.py` and `scripts/langchain/trace_utils.py` without corresponding new tests in squash diff. | No — offload. |
| Portable-Alpha-Extension-Model | [#2462](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2462) | [#2415](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2415) | **PARTIAL** | Five test files for listed modules; coverage-round proof not independently replayed. | No — offload. |
| Workflows | [#4412](https://github.com/stranske/Workflows/pull/4412) | [#4107](https://github.com/stranske/Workflows/issues/4107) | **VERIFIED** | Diff updates `tools/run_judge_backend_screen.py` and adds contributor-tier regression tests (repo mismatch before manifest lookup, bounded refusal text). Matches issue AC on binding eligibility to prompt/snapshot repo identity. | — |

## Excluded merged chores (not scored)

- `Ready#663` (Codex bootstrap), `Travel-Plan-Permission#1725` (bootstrap), `Portable-Alpha-Extension-Model#2456` (labeled Gate CI campaign), `Workflows#4410` (synced mypy consumer fix without issue link in title), release/template/dependency merges called out in search but filtered by title heuristics.
- `trip-planner#1959` merged before window start (`2026-11-02T00:58:04Z`).

## Belt ledger / Workflows#3391

No PR in this batch was **ledger-only**. No false `status: done` belt tasks observed in sampled ledger files.

## Reproduction receipts

| Issue | Command / gate | Result |
|---|---|---|
| #1720 | `pytest tests/python/test_http_service.py::test_operator_docs_do_not_reference_legacy_portal_requests_paths` on main | pass |
| #1061 | `pytest tests/docs/test_headless_ingest_runbook.py` on main | pass (executes runbook bash quickstart) |
| #1720 `Reproduction:` block | Not re-run (issue reproduction is doc URL walkthrough; named pytest gate is decisive) | — |

## Confidence

- **High:** #1720, #1061, #1962, #1964, #4408 (empty merge), #4409 (missing prod hunks), #4412.
- **Medium:** #1721 (deliberate-break not re-run), coverage-round PARTIAL rows (conservative — diff shows real tests but not full AC mapping).
- **Would change mind:** fresh `pytest --cov` + break-revert replay on any PARTIAL coverage PR; full `gh pr diff` for #4409 if GitHub omitted binary/large paths (unlikely — JS/workflow paths absent from `diff --git` list).

## Remaining queue

16 eligible merges in window were not verified this run (cap 20). Next run should resume from checkpoint ledger and continue oldest-first among unlisted PRs (e.g. `Counter_Risk#1228`, `Manager-Database#1881`, newer Workflows/PAEM closer repairs).
