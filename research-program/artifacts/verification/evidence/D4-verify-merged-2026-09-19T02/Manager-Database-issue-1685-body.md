## Why

Portable Alpha records prior-run information, but users still need a clear explanation of what changed between runs. A comparison LLM panel should summarize config differences, metric movement, risk constraint changes, and traceable reasoning.

## Scope

- Finish `pa_core/llm/compare_runs.py` for prior-run loading, diff formatting, prompt construction, and chain invocation.
- Finish `dashboard/components/comparison_llm.py` for the Streamlit UI and exports.
- Wire the comparison panel into `dashboard/pages/4_Results.py` using `manifest_data["previous_run"]` or existing prior-run discovery.

## Non-Goals

- Do not build Config Chat patching in this issue.
- Do not require a previous run for the Results page to load.
- Do not call real LLM endpoints in required tests.

## Tasks

- [ ] Verify or implement prior manifest and prior summary loading when `previous_run` exists and is readable.
- [ ] Verify or implement a human-readable config diff covering seed, capital, weights, distribution choices, and wizard fields stored in manifests.
- [ ] Verify or implement current-versus-prior metric catalogs using the same metric definitions as Explain Results.
- [ ] Invoke the LLM through the shared provider helper and return explanation text plus trace URL when available.
- [ ] Verify or implement `dashboard/components/comparison_llm.py` with current/previous selection, question input, provider settings, spinner, and TXT/JSON downloads.
- [ ] Wire the panel into `dashboard/pages/4_Results.py` with a clear missing-previous-run state.
- [ ] Add tests for readable prior run, missing prior run, malformed prior summary, diff formatting, export payloads, and no-secret leakage.

## Acceptance Criteria

- [ ] When a previous run exists, the comparison panel produces a coherent explanation and displays a trace URL when LangSmith is enabled.
- [ ] When the previous run is missing or unreadable, the Results page still loads and explains what input is missing.
- [ ] Export payloads include current/prior identifiers, config diff, metric diff, provider/model metadata, and trace URL when available.
- [ ] Tests cover diff construction and missing-data behavior without real provider calls.
- [ ] No secrets appear in UI output, downloads, logs, or exceptions.

## Implementation Notes

Relevant files: `pa_core/llm/compare_runs.py`, `pa_core/llm/prompts.py`, `dashboard/components/comparison_llm.py`, `dashboard/components/llm_settings.py`, `dashboard/pages/4_Results.py`, `tests/test_compare_runs.py`, `tests/test_llm_compare_runs.py`, `tests/test_dashboard_comparison_llm.py`, `tests/test_reporting_run_diff.py`, `tests/test_dashboard_results_previous_run.py`.
