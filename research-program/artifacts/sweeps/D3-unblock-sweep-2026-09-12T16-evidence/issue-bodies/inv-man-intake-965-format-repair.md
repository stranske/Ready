<!-- follow-up-depth: 1 -->
## Why
PR #955 addressed issue #942, but verification identified remaining concerns (verdict: **CONCERNS**). This follow-up closes the remaining gaps by separating production ingestion from fixture/smoke-only behavior, ensuring performance data is derived from the submitted workbook in non-smoke mode, and adding regression coverage to prevent fixture-path or fixture-data fallback from reappearing in production flows.

## Source
- Original PR: #955
- Parent issue: #942

## Scope

Production workbook performance and content resolution, plus smoke regression coverage.

## Non-Goals

Do not change smoke fixture values or unrelated ingestion behavior.

## Tasks
- [ ] Refactor the conditional logic in `_resolve_performance_series` to create separate code paths for smoke mode versus production mode
- [ ] Implement workbook-derived performance extraction logic that reads performance data directly from the submitted workbook in production mode in `src/inv_man_intake/v1_smoke.py`.
- [ ] Add explicit unavailable or no-data result handling when performance rows cannot be parsed from the workbook in `src/inv_man_intake/v1_smoke.py`.
- [ ] Remove all calls to `_fixture_performance_series()` from the production code path in `_resolve_performance_series`
- [ ] Update the content resolution flow in production mode to use only the `content_root` parameter passed from `run.py`
- [ ] Remove any fallback logic that references fixture directories when resolving workbook paths in production mode in `src/inv_man_intake/v1_smoke.py`.
- [ ] Remove any hardcoded fixture filenames such as `summit_arc_track_record.xlsx` from the production workbook resolution path
- [ ] Eliminate repository-relative path assumptions from the production content resolution logic in `src/inv_man_intake/v1_smoke.py`.
- [ ] Create a test bundle with performance values distinct from the XLSX fixture series, located outside the repository fixture layout with valid workbook performance data for regression testing in `tests/cli/test_ingest_entrypoint.py`.
- [ ] Write a regression test in `tests/cli/test_ingest_entrypoint.py` that runs ingestion on the non-fixture production bundle
- [ ] Add assertions to verify that generated artifacts contain workbook-extracted performance values matching the test bundle data in `tests/cli/test_ingest_entrypoint.py`.
- [ ] Add assertions to verify that artifacts do not contain any hard-coded fixture performance values from `_fixture_performance_series()`
- [ ] Add test coverage for the scenario where performance data is explicitly marked as unavailable when workbook parsing fails in `tests/cli/test_ingest_entrypoint.py`.
- [ ] Add or update tests in `tests/cli/test_ingest_entrypoint.py` covering smoke-mode ingestion to verify that smoke bundles still use the fixture performance series behavior unchanged after the production-path refactor.

## Acceptance Criteria
- [ ] In non-smoke ingestion, `_resolve_performance_series` in `src/inv_man_intake/v1_smoke.py` does not call `_fixture_performance_series()` on the production path and instead returns performance data derived from the submitted workbook, or returns `None` when workbook performance rows cannot be parsed.
- [ ] For a valid non-smoke bundle located outside the repository fixture layout, the generated ingest artifacts do not contain performance values matching [0.021, -0.012, 0.018, 0.006, -0.004, 0.014] which are the known XLSX fixture values produced by `_fixture_performance_series()`.
- [ ] The production content and file resolution flow resolves workbook inputs only from the `content_root` passed by `run.py` and does not reference fixture directories, fixed fixture filenames, or repository-relative fallback paths in non-smoke mode.
- [ ] A regression test exists in `tests/cli/test_ingest_entrypoint.py` that uses a production (non-smoke) bundle outside the repository fixture layout and asserts one of the following outcomes only: (a) artifact performance fields equal workbook-extracted values expected from that bundle, or (b) artifact performance fields are set to `None`.
- [ ] A smoke-mode test verifies that output artifacts contain the expected XLSX fixture performance values [0.021, -0.012, 0.018, 0.006, -0.004, 0.014] when run in smoke mode.
- [ ] The manual verification safeguard is enforceable by the test suite: if a developer reintroduces a fixed workbook lookup or fixture-path fallback in the non-smoke production path, `tests/cli/test_ingest_entrypoint.py::test_ingest_entrypoint_runs_valid_bundle_outside_repository_fixture_layout` fails.

## Implementation Notes

### Files to Modify
- `src/inv_man_intake/v1_smoke.py`
- `src/inv_man_intake/run.py`
- `tests/cli/test_ingest_entrypoint.py`

### Design Constraints
- In non-smoke mode, keep fixture-only helpers and fixture-only path assumptions fully out of the production performance resolution path.
- Production workbook lookup should be driven exclusively by the `content_root` supplied from `run.py`.
- Avoid any non-smoke dependency on:
  - fixture directories
  - repository-relative fallback paths
  - fixed workbook filenames such as `summit_arc_track_record.xlsx`
- When workbook performance rows cannot be parsed in production, return the explicit unavailable or no-data representation used by the ingest artifacts rather than substituting fixture values.
- Add regression coverage that exercises a bundle located outside the repository fixture layout.

### Verification
Useful verification commands while implementing:
- `pytest tests/cli/test_ingest_entrypoint.py::test_ingest_entrypoint_runs_valid_bundle_outside_repository_fixture_layout -q`
- `pytest tests/cli/test_ingest_entrypoint.py -k 'performance and unavailable'`
- `pytest tests/cli/test_ingest_entrypoint.py -k smoke -q`

## Notes
<details>
<summary>Background (previous attempt context)</summary>

- Previous failure to avoid: in the current `_resolve_performance_series`, the non-smoke branch calls `_fixture_performance_series`, leading to hard-coded performance values in production.
- Why it failed: the condition distinguishing smoke mode from production only gated fixed file name usage, but did not also separate performance extraction behavior, so production ingestion still reused fixture-only performance data.
- What to do instead: ensure that in production mode, the function fully executes canonical workbook-derived performance extraction and never calls fixture-only helpers on that path.

</details>

