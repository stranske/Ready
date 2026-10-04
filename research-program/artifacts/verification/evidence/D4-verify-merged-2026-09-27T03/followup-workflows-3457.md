## Why (verified evidence)

D4-verify-merged-2026-09-27T03 read squash diff for stranske/Workflows#3584 (merge `b4c0862874de…`) against #3457. Auto-dispatch wiring is present: `maint-77-model-registry-freshness.yml` adds `dispatch-evaluation-pilot`, `tools/refresh_model_eval_candidates.py` merges catalog discovery, and `tests/workflows/test_model_eval_pilot_workflow.py::test_auto_dispatch_maint77_chains_to_maint78_on_catalog_drift` passes locally.

Issue #3457 also requires deliberate-break evidence: remove the maint-77 dispatch step → `pytest tests/workflows/test_model_eval_pilot_workflow.py -k auto_dispatch` FAILS → restore → passes. The squash diff and PR #3584 body contain **no executed FAIL/PASS transcript** for that mutation.

## Tasks

- [ ] On a branch off `main`, temporarily remove or neuter the `Dispatch evaluation pilot on catalog drift` step in `.github/workflows/maint-77-model-registry-freshness.yml`, run `pytest tests/workflows/test_model_eval_pilot_workflow.py -k auto_dispatch -q`, capture failing output.
- [ ] Restore the dispatch step, re-run the same pytest command, capture passing output, and record RED/GREEN blocks in a comment on #3457 or `docs/evidence/issue-3457-auto-dispatch-deliberate-break.md`.

## Acceptance Criteria

- Named test: `pytest tests/workflows/test_model_eval_pilot_workflow.py -k auto_dispatch -q` exits 0 on `main` (already satisfied).
- Deliberate-break → revert: with dispatch step removed, the named test FAILS; after restore it passes; both runs recorded with literal pytest output.

## Non-Goals

- Do NOT remove maint-77→maint-78 auto-dispatch behavior from #3584.
- Do NOT weaken `config/model_selection_policy.json` gates.

_Surfaced by D4-verify-merged-2026-09-27T03; verified against `Workflows-3584.diff` and issue #3457. Related: #3457, merged PR #3584._
