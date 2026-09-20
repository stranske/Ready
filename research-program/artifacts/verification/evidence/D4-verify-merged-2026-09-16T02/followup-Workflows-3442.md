## Why (verified evidence)

Post-merge verification (D4-verify-merged-2026-09-16T02) of stranske/Workflows#3442 (merge `9a16cbf4f93a9366cdc2a0ab30fa2d01c977abbc`) against #2819 found corpus-evidence and promotion-prepare slices landed with 87 passing tests, but the self-triggering pilot move is absent from the squash diff.

- `tools/harvest_verifier_corpus.py`, `tools/verifier_corpus_evidence.py`, and `tools/prepare_model_promotion.py` substantially updated; `reusable-agents-verifier.yml` publishes replayable decisions.
- Issue task 1 requires `maint-77-model-registry-freshness.yml` to dispatch `maint-78-model-evaluation-pilot.yml` when a new catalog candidate passes freshness — **no workflow changes** to maint-77 or maint-78 in the diff.
- Docs still describe maint-78 as `workflow_dispatch`-only; acceptance criterion "new catalogued model results in auto-dispatched pilot" is therefore NOT MET.

## Tasks

- [ ] Update `.github/workflows/maint-77-model-registry-freshness.yml` to dispatch `.github/workflows/maint-78-model-evaluation-pilot.yml` when freshness screening finds a new catalog candidate.
- [ ] Auto-populate `config/model_eval_candidates.json` from catalog discovery (incumbent + same-provider successors) per #2819 design.
- [ ] Add workflow regression in `tests/workflows/test_model_eval_pilot_workflow.py` proving catalog-change triggers pilot dispatch without manual `workflow_dispatch`.

## Acceptance Criteria

- Named test: `pytest tests/workflows/test_model_eval_pilot_workflow.py -k auto_dispatch` exits 0 proving maint-77 chains to maint-78 on new candidate.
- Deliberate-break → revert: remove dispatch step from maint-77 → named test FAILS → restore → passes.

## Non-Goals

- Do NOT weaken `config/model_selection_policy.json` gates or remove human approval for risky swaps.
- Do NOT revert corpus-evidence hardening from #3442.

_Surfaced by D4-verify-merged-2026-09-16T02; verified against squash diff `Workflows-3442.diff`, local gate 87/87 pass, and issue #2819. Related: #2819, merged PR #3442._
