# [P1] Stabilize local vector preview and graphic export readiness

Staged issue body only; not filed. No duplicate found among the 15 open issues and zero open PRs at this sweep's observation time. Recheck before filing.

## Why

Default-branch CI fails in `Static SPA browser E2E`: https://github.com/stranske/Inv-Man-Intake/actions/runs/33966207743 at `b3211e3535ee5dc0c5b217ecd93354b47565136b`.

Two observed failures in `tests/app/test_static_spa_browser_e2e.py`:

1. `test_vector_figure_export_renders_a_local_pdf_region_without_egress` finds the rendered row and preview image, then times out at line 222 reading that row's text after the click. The log establishes a later locator timeout, not a failure to render the initial PNG.
2. `test_export_panel_produces_artifacts_and_manifest` fails at line 282: export rows contain `return-series.xlsx` and a generated one-pager, but no PNG/graphic entry.

These require investigation of asynchronous packet rendering, DOM replacement, and test readiness. The sweep does not establish that artifact registration itself is broken; changing selectors or weakening expected output without a reproduction would be premature.

## Scope

`app/static_operator_app.js`, its `app/vector_figure_renderer.js` dependency, and the two failing browser paths in `tests/app/test_static_spa_browser_e2e.py`.

## Non-Goals

Network rendering, relaxed no-egress guarantees, removing PNG-content assertions, or shared workflow changes.

## Tasks

- [ ] Reproduce both failures with `STATIC_SPA_E2E=true CI=true pytest -q tests/app/test_static_spa_browser_e2e.py -p no:cacheprovider -o addopts=""`; use the Chromium installation and dependencies from `.github/workflows/ci.yml`.
- [ ] Trace packet upload and the update of `state.vectorArtifacts` and `state.exportArtifacts` in `app/static_operator_app.js`; capture when the graphics row is replaced relative to preview clicks and when the export catalog becomes ready.
- [ ] Fix the demonstrated cause in `app/static_operator_app.js`, `app/vector_figure_renderer.js`, or an explicit readiness assertion in `tests/app/test_static_spa_browser_e2e.py`, preserving real image and no-egress verification.

## Acceptance Criteria

- [ ] The full command above passes with zero skipped browser tests in the same Chromium CI environment.
- [ ] The vector test verifies PNG magic, nonzero dimensions, multiple pixel colors, and zero external requests after selecting a local PDF region.
- [ ] The export test verifies a graphic or PNG row and thumbnail alongside `return-series.xlsx`, manifest skip reasons, and a one-pager.
- [ ] Existing deliberately disabled-handler tests still catch the missing behavior.
- [ ] Default-branch-equivalent `Static SPA browser E2E` is green after the repair.

## Implementation Notes

All cited files were opened or verified in a refreshed clone at the failing main SHA. CI logs are the reproduction evidence for this sweep; no local browser rerun or code edit was performed. Preserve the distinction between a product defect and an asynchronous test synchronization defect until reproduced.
