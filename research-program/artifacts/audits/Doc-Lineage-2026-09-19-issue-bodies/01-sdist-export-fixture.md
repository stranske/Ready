## Why

`MANIFEST.in:1` includes the `tests/export/` Python files in source distributions, and `README.md:28-29` says that source distributions include export tests so their acceptance checks can run. But `tests/export/test_fact_key_map.py:11-15` and `tests/export/test_fact_key_map_cli.py:13-18` require `tests/fixtures/fact_key_map/tracked_variables.json`, which the manifest does not include. This is a current packaging break: building the current sdist, installing its `dev` extra, extracting it, and running `pytest tests/export/test_fact_key_map.py tests/export/test_fact_key_map_cli.py` produces 20 failures from that missing fixture.

## Scope

Make the source distribution self-contained for every exported test check, and add a package-artifact regression test for the fact-key-map fixture.

## Non-Goals

- Do not broaden the source distribution to all repository fixtures or binary corpus files without a test dependency that requires them.
- Do not remove the fact-key-map export tests from the sdist to hide the missing input.
- Scaffold-only completion does NOT count: adding a manifest rule without proving the extracted source distribution contains `tests/fixtures/fact_key_map/tracked_variables.json` and runs the named tests is a failure of this issue.

## Tasks

- [ ] Update `MANIFEST.in:1` with an explicit include rule for `tests/fixtures/fact_key_map/tracked_variables.json`, alongside the existing exported test include.
- [ ] Add a packaging regression test in `tests/test_package_identity.py` that builds or inspects the source distribution and asserts `tests/fixtures/fact_key_map/tracked_variables.json` is present when `tests/export/test_fact_key_map.py` is present.
- [ ] Update `README.md:28-29` only if the exact exported test fixture packaging contract needs clarification after the implementation.

## Acceptance Criteria

- [ ] `python -m build --sdist` followed by extracting the archive and running `pytest tests/export/test_fact_key_map.py tests/export/test_fact_key_map_cli.py` passes with all 27 selected tests collected and no fixture `FileNotFoundError`.
- [ ] Deliberate-break gate: temporarily remove the `tests/fixtures/fact_key_map/tracked_variables.json` inclusion from `MANIFEST.in:1`; the new `tests/test_package_identity.py` packaging assertion and the extracted-sdist fact-key-map pytest command must fail. Restore the inclusion before requesting review.

## Implementation Notes

- Verified current source evidence at `MANIFEST.in:1`, `README.md:28-29`, `tests/export/test_fact_key_map.py:11-15`, and `tests/export/test_fact_key_map_cli.py:13-18`.
- Confirmed current reproduction: an isolated current sdist has the export test files but not `tests/fixtures/fact_key_map/tracked_variables.json`; the named pytest command fails 20 times.
