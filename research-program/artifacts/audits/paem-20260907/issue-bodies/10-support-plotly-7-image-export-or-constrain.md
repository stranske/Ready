## Why

`pyproject.toml:119` permits Plotly 7, but `pa_core/viz/export_backend.py:88` passes the removed engine keyword to to_image and line 100 passes it to write_image. A clean dependency solve installed Plotly 7.0.0; a real CLI sweep crashed with TypeError before manifest completion. The repository lock pins Plotly 6.9.0, and the same command succeeds under that pin. `pa_core/reporting/sweep_excel.py:96` skips the affected chart branch in CI, explaining why green CI does not refute this supported-install failure. Plotly documents this removal: https://plotly.com/python/static-image-generation-changes/ . This overturns the delegated environmental-only dismissal.

## Scope

Support Plotly 7 image export or constrain installation. First-party infra behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] Remove deprecated explicit engine arguments in `pa_core/viz/export_backend.py` with compatibility coverage, or add an explicit temporary supported-version constraint in `pyproject.toml` until migration is delivered.
- [ ] Extend `tests/test_export_backend.py` to exercise actual supported Plotly signatures and add a real CLI export smoke outside the CI or PYTEST_CURRENT_TEST bypass in `pa_core/reporting/sweep_excel.py`.

## Acceptance Criteria

- [ ] A fresh installation cannot resolve an unsupported Plotly version, or a real PNG and CLI sweep export succeeds with Plotly7; the supported lock-version export still succeeds.
- [ ] Run `pytest tests/test_export_backend.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Restore engine="kaleido" without a dependency constraint; the real Plotly7 signature and export regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
