# D4 verification — 2026-11-15T23

Checked 2026-11-15 (UTC run ~2026-11-16T00:00Z). Discovery covered the 36-hour
window beginning **2026-11-14T11:52:00Z** across `SUPPORTED_REPOS` in
`handoff.sh`, excluding Orchestrator and owner-excluded `stranske/Collab-Admin`.
**23** merged PRs were found; **14** release/template/dependency chores and **2**
issue-unlinked merges were skipped. **9** issue-linked merges were verified
(oldest first). No GitHub secondary-rate-limit response occurred. This offload
did not post GitHub comments, reopen issues, or file new follow-ups (read-only).

| Repo | PR | Issue / relationship | Verdict | Unmet criteria / evidence | Follow-up |
|---|---:|---|---|---|---|
| Workflows | [#4683](https://github.com/stranske/Workflows/pull/4683) | (none) | **SKIPPED** | Weekly maint-83 consumer bootstrap **verify** job + regression tests; no linked issue in body/metadata. | — |
| Portable-Alpha-Extension-Model | [#2509](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2509) | [#2496](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2496) | **VERIFIED** | Squash diff (not body): major `tests/test_coverage_round_2375.py` reconciliation, `docs/evidence/issue-2496/mutations.json` with named mutation/restoration transcripts, `tests/test_tracing.py` formatting. Meets integrity/mutation acceptance rows at evidence level. Hosted CI timing (<120s) and full Gate delta not re-executed in this unit. | — |
| Workflows | [#4685](https://github.com/stranske/Workflows/pull/4685) | [#4684](https://github.com/stranske/Workflows/issues/4684) | **BELT** | Ledger-only (`.agents/issue-4684-ledger.yml`); belt still owns #4684 (`status:in-progress`). No task marked `done` without implementation (#3391 check clean). | — |
| Portable-Alpha-Extension-Model | [#2508](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2508) | [#2507](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2507) | **VERIFIED** | Diff: `pa_core/schema.py` type-string normalization for cross-interpreter dict generation; `tests/test_schema_export.py` adds `test_parameter_dictionary_byte_identical_across_313_and_314`; evidence README documents 3.13/3.14 pytest + `cmp`/SHA parity for `PARAMETER_DICTIONARY.md`. | — |
| Workflows | [#4687](https://github.com/stranske/Workflows/pull/4687) | [#4686](https://github.com/stranske/Workflows/issues/4686) | **PARTIAL** | Diff implements `criterionNamesGate` / `textNamesCommand` in `.github/scripts/keepalive_loop.js` (+ template) and adds pinned-vs-bare regression in `keepalive-loop.test.js` — meets source regression and named `node --test` gate. **Not met:** live row — `Trend_Model_Project#6223` merged 2026-11-15T19:06Z but **1** review thread remains **unresolved** (GraphQL 2026-11-16; finding from #4684 lineage). | Would file (offload read-only) |
| Workflows | [#4688](https://github.com/stranske/Workflows/pull/4688) | [Orchestrator#1354](https://github.com/stranske/Orchestrator/issues/1354) / [#1382](https://github.com/stranske/Orchestrator/issues/1382) | **VERIFIED** | Diff moves deliberate-break labelling to `acceptance-criteria-label` job with `pull-requests: write`; `tests/workflows/test_gate_label_permission.py` parametrizes both root and consumer `pr-00-gate.yml`. | — |
| Workflows | [#4692](https://github.com/stranske/Workflows/pull/4692) | [Orchestrator#1379](https://github.com/stranske/Orchestrator/issues/1379) | **VERIFIED** | Diff adds `keepalive-gate-citation` regression in `agents-pr-meta-update-body.test.js` and keeps gate report on plan/head-bound refresh in keepalive/PR-meta scripts (+ consumer templates). Named test cited in PR acceptance. Not re-run locally. | — |
| Workflows | [#4693](https://github.com/stranske/Workflows/pull/4693) | (none) | **SKIPPED** | Runner completion receipt `requested_model` / `reported_model` wiring + `tests/scripts/test_receipt_model_fields.py` (35 cases, deliberate-break noted in PR body). No issue reference — out of scoped verify set. | — |
| Workflows | [#4694](https://github.com/stranske/Workflows/pull/4694) | (cites [Orchestrator#1387](https://github.com/stranske/Orchestrator/issues/1387)) | **VERIFIED** | Diff replaces Gemini 3.8 Flash with Gemini 4 Hydrogen in `.github/agents/model-table.json` and `config/verifier_shadow.json`; documents pilot in `docs/guides/agent-readiness/agy.md`. | — |

## Skipped merges (scope)

Template-sync / dependency chores (not verified): `Travel-Plan-Permission#1745–1746`, `Trend_Model_Project#6223` (sync title), `Portable-Alpha-Extension-Model#2506`, and matching `chore: sync workflow templates` merges on Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data, Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic (~2026-11-15T19:05–19:07Z).

## Critical findings

- **Outcome count:** 6 **VERIFIED**, 1 **PARTIAL**, 1 **BELT**, 2 **SKIPPED** (no issue), 14 **SKIPPED** (chores), among 23 window merges.
- **#4685 → #4684** is textbook belt bookkeeping; implementation landed in **#4687** (`#4686`), not the belt PR.
- **#4687** source fix looks real (not scaffold), but **live sync proof is still open** while `TMP#6223` carries an unresolved review thread — same failure class as prior D4 on consumer sync PRs.
- **#2509** is the opposite pattern: large test/evidence delivery for a backlog acceptance issue; confidence on diff is high; wall-clock/CI rows depend on merged evidence artifacts, not a local re-run here.
- **#4693** is substantive but **untracked to an issue** — worth an intake issue if the fleet wants it in the verify ledger next run.
- Offload constraint: no GitHub writes; no `Reproduction:` blocks required on linked issues this pass.

## Confidence

**High** on diff-read verdicts for Workflows keepalive/gate/receipt PRs and PAEM #2508. **High** that #4687’s live criterion is still unmet given unresolved `TMP#6223` thread. **Medium** on #2509 hosted CI / 120s timing without re-execution. Resolved `TMP#6223` review thread + quiet sync-core on #4684 would move #4687 to **VERIFIED**.