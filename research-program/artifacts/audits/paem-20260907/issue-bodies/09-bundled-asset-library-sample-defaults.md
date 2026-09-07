## Why

`templates/asset_timeseries_wide_returns.csv:2` begins a 24-observation sample, but `dashboard/pages/1_Asset_Library.py:116` sets minimum observations to 36. Selecting the bundled sample in a clean browser triggers the uncaught importer error at `dashboard/pages/1_Asset_Library.py:204`: insufficient data for FUND_A, FUND_B, SP500_TR. The initial page loads, but the advertised no-upload path fails. This is a residual behavior failure after closed #2026, distinct from the installed-resource omission.

## Scope

Make the bundled Asset Library sample load with defaults. First-party ui behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] Align `templates/asset_timeseries_wide_returns.csv` and the bundled-sample behavior in `dashboard/pages/1_Asset_Library.py` so the supplied fixture meets the retained data-quality minimum without silently weakening validation for uploaded user data.
- [ ] In `dashboard/pages/1_Asset_Library.py`, present actionable guidance for insufficient-data imports instead of propagating the raw exception.
- [ ] Extend `tests/test_dashboard_asset_library.py` to run the real sample at the actual default minimum using AppTest, and exercise an insufficient uploaded series.

## Acceptance Criteria

- [ ] A fresh Asset Library session can select the bundled sample and reach Data loaded successfully with no exception and no manual parameter edits; undersized user uploads receive explicit guidance.
- [ ] Run `pytest tests/test_dashboard_asset_library.py tests/test_asset_library_exception_handling.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Restore the 24-row fixture with an unchanged minimum36; the real-default sample regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
