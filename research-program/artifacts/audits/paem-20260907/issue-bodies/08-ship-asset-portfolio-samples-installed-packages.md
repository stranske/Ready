## Why

`dashboard/utils.py:146` resolves templates relative to site-packages, while `pyproject.toml:89` includes only data CSV package resources. In an actual non-editable installation, bundled_asset_timeseries_path points to a nonexistent templates file; bundled_sample_index_path exists. The same template resolver feeds the portfolio starter at `dashboard/utils.py:177`. Closed #2026 added checkout samples; the installed layout still lacks their files.

## Scope

Ship asset and portfolio samples in installed packages. First-party ui behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] Update package resources in `pyproject.toml` and the sample resolvers in `dashboard/utils.py` so asset CSV and portfolio YAML ship and resolve in a wheel install outside the source checkout.
- [ ] Extend `tests/test_dashboard_sample_data.py` or add a packaging smoke helper wired into the existing package-validation test command to build and install a wheel and open all three samples.

## Acceptance Criteria

- [ ] A built non-editable wheel installed into an isolated environment outside the checkout exposes readable asset CSV, portfolio YAML and index CSV without relying on repository-relative templates.
- [ ] Run `pytest tests/test_dashboard_sample_data.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Omit the asset and portfolio resources from package data; the named wheel-install smoke must fail; revert.

## Implementation Notes

Severity P2. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
