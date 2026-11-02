## Why (verified evidence)

Owner decision #4362 (2026-10-31) retired GitHub Models from `config/llm_slots.json` and moved the selection to `selection_history`, so `GitHubModelsProvider.is_available()` now requires a configured slot model (`tools/llm_provider.py:338-342`) and returns false when only `GITHUB_TOKEN` is set. Despite that, **Maint 39 Test LLM Providers** still exposes `github-models` as a `workflow_dispatch` choice (`.github/workflows/maint-39-test-llm-providers.yml:12-15`) and runs a **Test GitHub Models** step (lines 66-81) that calls `get_llm_provider(force_provider='github-models')`, which raises `RuntimeError: Forced provider 'github-models' is not available` on the current tip (reproduced locally with `GITHUB_TOKEN=test-token`). Default dispatch `provider=all` always hits this step, so the maintenance smoke workflow is broken for its primary use case.

## Tasks
- [ ] Remove the `github-models` option from `workflow_dispatch.inputs.provider.options` in `.github/workflows/maint-39-test-llm-providers.yml:12-15` and delete the **Test GitHub Models** job step at `:66-81`.
- [ ] Drop the unused `models: read` permission if no step requires it after the removal (`.github/workflows/maint-39-test-llm-providers.yml:17-19`).
- [ ] Update operator docs that still tell maintainers to smoke-test GitHub Models via Maint 39 (`docs/WORKFLOW_GUIDE.md:74`, `docs/ci/WORKFLOWS.md:191`) to list only OpenAI/Anthropic (and regex fallback via `check_providers()`).
- [ ] Add `tests/workflows/test_maint39_llm_provider_workflow.py` asserting the workflow YAML has no `github-models` dispatch option and no step named `Test GitHub Models`.

## Acceptance Criteria
- Named test: `tests/workflows/test_maint39_llm_provider_workflow.py::test_maint39_does_not_reference_retired_github_models_provider` — loads `.github/workflows/maint-39-test-llm-providers.yml` and asserts `github-models` is absent from dispatch options and step names.
- Deliberate-break → revert: re-add the `github-models` option and **Test GitHub Models** step → named test FAILS → revert.

## Non-Goals
- Do NOT re-enable GitHub Models in `config/llm_slots.json` or the fallback chain; owner decision #4362 stands.
- Do NOT bulk-rewrite historical plan docs under `docs/plans/` in this change.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by Track D audit 2026-11-02; verified on tip `c4633a95` by local `get_llm_provider(force_provider='github-models')` failure and workflow YAML inspection._
