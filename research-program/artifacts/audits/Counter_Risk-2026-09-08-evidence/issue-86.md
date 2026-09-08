## Why

PR #79 addressed issue #78, but verification identified concerns (verdict: **CONCERNS**). This follow-up issue closes the remaining gaps by adding a CI release workflow, true end-to-end packaged-executable tests (including Windows `.cmd` execution), stronger validation around bundled templates and runtime path resolution, more stable numeric fixture assertions, and better build/error logging for PyInstaller and COM-related failures.

## Scope

Add the following across CI, integration tests, unit tests, and runtime/build code:
A CI release workflow, end-to-end packaged executable tests (including Windows `.cmd` runner behavior), template bundling duplicate detection tests, numeric fixture assertion stabilization via a shared helper, improved PyInstaller build logging, tightened runtime path resolution behavior with tests, and surfaced COM-related failures in `pipeline/run.py` with tests.

## Non-Goals

_Not provided._

## Tasks

- [ ] Create `.github/workflows/release.yml` to: checkout → `actions/setup-python` → install deps → run full test suite → run `pyinstaller -y release.spec` → assemble a versioned release bundle → validate required artifacts (`VERSION`, `manifest.json`, `templates/`, default config file, `run_counter_risk.cmd`, `README` containing `How to run`, and the built executable) → upload the bundle as a workflow artifact (fail non-zero on any missing artifact).
  - [ ] Create the basic workflow file structure with checkout (verify: confirm completion in repo)
  - [ ] Create the basic workflow file structure with Python setup steps (verify: confirm completion in repo)
  - [ ] Add dependency installation (verify: dependencies updated)
  - [ ] test suite execution steps to the workflow (verify: confirm completion in repo)
  - [ ] Add the PyInstaller build step that runs release.spec to the workflow (verify: confirm completion in repo)
  - [ ] Implement the versioned bundle assembly logic in the workflow (verify: confirm completion in repo)
  - [ ] Add validation steps that check for all required artifacts in the bundle (verify: confirm completion in repo)
  - [ ] Configure artifact upload with failure handling for missing artifacts (verify: config validated)
- [ ] Implement `tests/integration/test_packaged_executable_assets.py` to run `pyinstaller -y release.spec` via `subprocess.run(..., check=True)`, copy/move only the packaged output into a temporary isolated directory (no repo paths), execute the produced binary from that directory, and assert it locates/loads the bundled default configuration and at least one template asset.
  - [ ] Create the test file with PyInstaller subprocess execution (verify: confirm completion in repo)
  - [ ] Create the test file with error handling (verify: confirm completion in repo)
  - [ ] Implement the isolated directory setup that copies only packaged output (verify: confirm completion in repo)
  - [ ] Add test logic to execute the binary from the isolated directory (verify: tests pass)
  - [ ] Define scope for: Assert that the executable successfully loads the bundled default configuration (verify: config validated)
  - [ ] Implement focused slice for: Assert that the executable successfully loads the bundled default configuration (verify: config validated)
  - [ ] Validate focused slice for: Assert that the executable successfully loads the bundled default configuration (verify: config validated)
  - [ ] Define scope for: Assert that the executable successfully loads at least one template asset (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Assert that the executable successfully loads at least one template asset (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Assert that the executable successfully loads at least one template asset (verify: confirm completion in repo)
- [ ] Implement `tests/integration/test_windows_runner_cmd.py` to be skipped on non-Windows, copy `run_counter_risk.cmd` and the packaged executable into a temp directory, execute the `.cmd` with `cwd` set to the temp directory, and assert (a) executable path is resolved relative to the `.cmd` location, (b) the `.cmd` does not invoke `python`/`py`/a `.py` entrypoint, and (c) CLI args (including at least one `--flag value`) are forwarded unchanged.
  - [ ] Create the Windows-specific test file with platform skip decorator (verify: confirm completion in repo)
  - [ ] Implement temporary directory setup with cmd (verify: confirm completion in repo)
  - [ ] Implement temporary directory setup with executable files (verify: confirm completion in repo)
  - [ ] Define scope for: Add test execution logic that runs the cmd file from the temp directory (verify: tests pass)
  - [ ] Implement focused slice for: Add test execution logic that runs the cmd file from the temp directory (verify: tests pass)
  - [ ] Validate focused slice for: Add test execution logic that runs the cmd file from the temp directory (verify: tests pass)
  - [ ] Assert that the executable path is resolved relative to cmd location (verify: confirm completion in repo)
  - [ ] Define scope for: Verify that the cmd file does not invoke Python interpreters or py files
  - [ ] Implement focused slice for: Verify that the cmd file does not invoke Python interpreters or py files
  - [ ] Validate focused slice for: Verify that the cmd file does not invoke Python interpreters or py files
  - [ ] Assert that CLI arguments including flags (verify: confirm completion in repo)
  - [ ] Assert that CLI arguments including values are forwarded correctly (verify: confirm completion in repo)
- [ ] Write `tests/unit/test_template_bundling_duplicates.py` to create at least two template source directories with a colliding template filename, invoke the template bundling logic, and assert either a raised error listing all conflicting filenames and source paths or a deterministic precedence rule documented in code and validated by the test.
- [ ] Add or update `tests/utils/assertions.py` to include a shared numeric comparison helper (e.g., `assert_numeric_outputs_close`) that accepts explicit `abs_tol` and `rel_tol` (or provides clearly defined defaults).
- [ ] Update fixture-based transformation tests asserting numeric outputs (CSV/TSV/JSON/parquet/etc.) to use `tests/utils/assertions.py` numeric helper instead of byte-for-byte equality for numeric fields, and ensure at least one updated test passes explicit `abs_tol` and `rel_tol`.
  - [ ] Identify all fixture-based transformation tests that assert numeric outputs (verify: tests pass)
  - [ ] Update CSV transformation tests to use the numeric comparison helper (verify: tests pass)
  - [ ] Update TSV transformation tests to use the numeric comparison helper (verify: tests pass)
  - [ ] Update JSON transformation tests to use the numeric comparison helper (verify: tests pass)
  - [ ] Update parquet transformation tests to use the numeric comparison helper (verify: tests pass)
  - [ ] Ensure at least one test explicitly passes abs_tol (verify: confirm completion in repo)
  - [ ] rel_tol parameters (verify: confirm completion in repo)
- [ ] Update `src/counter_risk/build/release.py` `_run_pyinstaller` to always capture and log PyInstaller stdout and stderr on both success and failure paths.
- [ ] Update `resolve_runtime_path` in `src/counter_risk/**/runtime_paths.py` to explicitly raise a clear exception or emit a warning when an asset cannot be found in any bundle root, and write/extend `tests/unit/test_runtime_paths.py` to cover the missing-asset and misconfiguration scenarios (asserting message contents include the asset name and at least one searched location/root).
  - [ ] Define scope for: Update resolve_runtime_path to raise an exception or emit a warning for missing assets (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Update resolve_runtime_path to raise an exception or emit a warning for missing assets (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Update resolve_runtime_path to raise an exception or emit a warning for missing assets (verify: confirm completion in repo)
  - [ ] Ensure the error message includes the asset name (verify: confirm completion in repo)
  - [ ] searched locations (verify: confirm completion in repo)
  - [ ] Add unit test for the missing-asset scenario with message validation (verify: confirm completion in repo)
  - [ ] Add unit test for misconfiguration scenarios like incorrect MEIPASS (verify: config validated)
  - [ ] Verify that tests assert message contents include asset name
  - [ ] searched roots (verify: confirm completion in repo)
- [ ] Fix `src/counter_risk/pipeline/run.py` `_refresh_ppt_links` to no longer silently swallow COM failures (re-raise with context or return a structured explicit error), and add `tests/unit/test_refresh_ppt_links_errors.py` using mocking plus `caplog` and/or exception assertions to verify the failure is surfaced.
  - [ ] Update _refresh_ppt_links to re-raise COM failures with added context (verify: confirm completion in repo)
  - [ ] Define scope for: Create the test file test_refresh_ppt_links_errors.py with basic structure (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Create the test file test_refresh_ppt_links_errors.py with basic structure (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Create the test file test_refresh_ppt_links_errors.py with basic structure (verify: confirm completion in repo)
  - [ ] Add test that uses mocking to force a COM operation failure (verify: tests pass)
  - [ ] Add assertions that verify the failure is surfaced via exception or logging
  - [ ] Verify that error messages contain contextual information about the failure

## Acceptance Criteria

- [ ] `.github/workflows/release.yml` exists on the default branch.
- [ ] The `release` workflow uses `actions/setup-python` and installs project dependencies before running tests/build steps.
- [ ] The `release` workflow runs the full Python test suite before building the release bundle.
- [ ] The `release` workflow runs `pyinstaller -y release.spec`.
- [ ] The `release` workflow assembles and uploads a versioned release bundle directory whose name includes the version value.
- [ ] The `release` workflow validates the bundle contains: `VERSION`, `manifest.json`, `templates/` directory, default configuration file, `run_counter_risk.cmd`, `README` containing a line with substring `How to run`, and the built executable.
- [ ] The `release` workflow exits non-zero if any required artifact is missing from the assembled bundle.
- [ ] `tests/integration/test_packaged_executable_assets.py` exists and is collected by pytest.
- [ ] The packaged-executable integration test runs `pyinstaller -y release.spec` and fails if the command exits non-zero.
- [ ] The packaged-executable integration test executes the produced binary from a temporary isolated directory containing only the packaged output (not the repository).
- [ ] The packaged-executable integration test asserts the executable successfully locates and loads the bundled default configuration when run from the isolated directory.
- [ ] The packaged-executable integration test asserts the executable successfully locates and loads at least one bundled template asset when run from the isolated directory.
- [ ] `tests/integration/test_windows_runner_cmd.py` exists and is skipped automatically on non-Windows platforms.
- [ ] The Windows integration test executes `run_counter_risk.cmd` from a temporary directory (separate from repo root) and verifies it launches the packaged executable using a path resolved relative to the `.cmd` file location.
- [ ] `run_counter_risk.cmd` does not invoke `python`, `py`, or a `.py` entrypoint; it directly invokes the built executable.
- [ ] The Windows integration test verifies CLI args passed to `run_counter_risk.cmd` are forwarded unchanged to the packaged executable, including at least one flag and one value.
- [ ] `tests/unit/test_template_bundling_duplicates.py` exists and includes a test that creates at least two different template source directories containing a colliding template filename.
- [ ] When duplicate template filenames are present, bundling logic either (A) raises an exception whose message includes every conflicting filename and all corresponding source paths, OR (B) applies a deterministic precedence rule documented in code and validated by unit tests.
- [ ] `tests/utils/assertions.py` contains a shared numeric comparison helper (e.g., `assert_numeric_outputs_close`) that accepts explicit absolute and relative tolerances (or exposes clearly defined defaults).
- [ ] All fixture-based transformation tests that assert numeric outputs (CSV/TSV/JSON/parquet/etc.) use the shared numeric comparison helper and do not do byte-for-byte equality checks for numeric fields.
- [ ] At least one updated fixture-based test calls the numeric helper with explicit `abs_tol` and `rel_tol`.
- [ ] `src/counter_risk/build/release.py` `_run_pyinstaller` captures and logs PyInstaller stdout and stderr on success.
- [ ] `src/counter_risk/build/release.py` `_run_pyinstaller` captures and logs PyInstaller stdout and stderr on failure before raising/returning a non-zero result.
- [ ] `resolve_runtime_path` emits an explicit failure signal on missing assets: either raises a specific exception with a clear message or emits a warning containing the asset name and attempted roots.
- [ ] `tests/unit/test_runtime_paths.py` covers the missing-asset scenario and asserts the chosen behavior (exception or warning) including message contents mentioning the requested asset and at least one searched location.
- [ ] `tests/unit/test_runtime_paths.py` includes a misconfiguration scenario (e.g., wrong bundle root / missing env var / incorrect `_MEIPASS`) and asserts failure is surfaced (exception or warning) rather than silently falling back to an unrelated path.
- [ ] `src/counter_risk/pipeline/run.py` `_refresh_ppt_links` does not silently swallow COM exceptions; it either re-raises with context or returns a structured explicit error value callers can check.
- [ ] `tests/unit/test_refresh_ppt_links_errors.py` exists and includes a test that forces a COM operation failure and asserts the failure is surfaced via (A) a raised exception containing contextual information, or (B) an explicit structured error plus an error log record.

## Implementation Notes

Workflow (`.github/workflows/release.yml`)
Ensure ordering is: checkout → setup-python → install deps → run tests → run `pyinstaller -y release.spec` → assemble versioned bundle → validate required artifacts → upload artifact.
Validation should explicitly check for:
Files: `VERSION`, `manifest.json`, default config file, `run_counter_risk.cmd`, built executable
Directories: `templates/`
README content: at least one line containing substring `How to run`
Validation must hard-fail (non-zero exit) on any missing/invalid requirement.

Integration packaged-binary test (`tests/integration/test_packaged_executable_assets.py`)
Build using subprocess with strict failure handling (e.g., `check=True`).
Execute the produced binary from a temp directory containing only the packaged output (avoid PYTHONPATH/PATH tricks that pick up the repo).
Assert behavior that demonstrates assets are loaded (e.g., program output, created output files, or an exit path that requires config/template availability).

Windows `.cmd` integration test (`tests/integration/test_windows_runner_cmd.py`)
Mark skip on non-Windows platforms.
Copy the `.cmd` and packaged executable into a temp directory; run the `.cmd` with `cwd` set to that temp directory.
Validate: relative path resolution, no python invocation, and argument forwarding (include at least one `--flag value` pair).

Template duplicate detection tests
Create at least two source directories with colliding template filenames; invoke the bundling logic.
Assert either a comprehensive error (filename + all source paths) or a deterministic precedence rule (and test it).

Numeric fixture comparisons
Centralize numeric comparisons in `tests/utils/assertions.py` with explicit `abs_tol` and `rel_tol`.
Replace byte-for-byte numeric comparisons across fixture-based tests with the helper; ensure at least one test demonstrates passing explicit tolerances.

PyInstaller logging (`src/counter_risk/build/release.py`)
Capture both stdout and stderr in success and failure paths and log them so CI provides actionable diagnostics.

Runtime path resolution (`src/counter_risk/**/runtime_paths.py`)
On missing assets: choose raise or warning, but make it explicit and message-rich (asset name + attempted roots).
Add unit tests for missing asset and a misconfiguration scenario (e.g., incorrect `_MEIPASS`).

COM error handling (`src/counter_risk/pipeline/run.py`)
Ensure `_refresh_ppt_links` does not silently swallow COM failures; re-raise with context or return a structured explicit error.
Test using mocking + `caplog` (or exception assertions) to guarantee failures surface.

<details>
<summary>Original Issue</summary>

```text
<!-- follow-up-depth: 2 -->
## Why
PR #79 addressed issue #78, but verification identified concerns (verdict: **CONCERNS**). This follow-up issue closes the remaining gaps by adding a CI release workflow, true end-to-end packaged-executable tests (including Windows `.cmd` execution), stronger validation around bundled templates and runtime path resolution, more stable numeric fixture assertions, and better build/error logging for PyInstaller and COM-related failures.

## Source
- Original PR: #79
- Parent issue: #78

## Tasks
- [ ] Add a GitHub Actions workflow at `.github/workflows/release.yml` that sets up Python, installs dependencies, runs the full test suite, runs `pyinstaller -y release.spec`, assembles the versioned release bundle, validates required artifacts exist (VERSION, manifest.json, templates/, default config, run_counter_risk.cmd, README containing a title line with 'How to run', and the built executable), fails on any missing artifact, and uploads the bundle as a workflow artifact.
- [ ] Implement an end-to-end integration test that builds via `pyinstaller -y release.spec`, then executes the produced binary from a temporary, isolated directory (without repository paths available) and asserts it can locate and load the bundled default configuration and template assets.
- [ ] Add an automated Windows test that executes `run_counter_risk.cmd` from a temp directory and verifies it resolves the executable path relative to the `.cmd` location (not via python) and forwards CLI args to the bundled executable correctly.
- [ ] Add unit tests for template bundling duplicate detection by creating conflicting template filenames across multiple source directories and asserting either (A) a raised error includes all conflicting filenames and their source paths, or (B) a documented precedence rule is applied deterministically.
- [ ] Update all fixture-based transformation tests that assert numeric outputs (CSV/TSV/JSON/parquet/etc.) to use a shared helper (e.g., `assert_numeric_outputs_close`) with explicit abs/rel tolerances, replacing any byte-for-byte comparisons for numeric fields.
- [ ] Update `src/counter_risk/build/release.py` (`_run_pyinstaller`) to always capture and log PyInstaller stdout/stderr on both success and failure so CI logs contain actionable build output.
- [ ] Tighten and test runtime path resolution behavior: update `resolve_runtime_path` to either raise a clear exception or emit a warning when an asset cannot be found in any bundle root, and add unit tests covering the chosen behavior (including a misconfiguration scenario).
- [ ] Adjust `pipeline/run.py` (`_refresh_ppt_links`) error handling so COM operation failures are not silently swallowed (either re-raise with context or return a structured/explicit error), and add tests that assert failures are surfaced via logging or exceptions.

## Acceptance Criteria
- [ ] A GitHub Actions workflow file exists at `.github/workflows/release.yml` on the default branch.
- [ ] The `release` workflow provisions Python using `actions/setup-python` and installs project dependencies prior to running tests/build steps.
- [ ] The `release` workflow runs the full Python test suite before building the release bundle.
- [ ] The `release` workflow runs `pyinstaller -y release.spec` as part of the workflow execution.
- [ ] The `release` workflow assembles a versioned release bundle directory (name includes the version value) and uploads it as a workflow artifact.
- [ ] The `release` workflow validates the bundle contains all required artifacts: `VERSION`, `manifest.json`, `templates/` directory, default configuration file, `run_counter_risk.cmd`, `README` containing a line with the substring `How to run`, and the built executable.
- [ ] The `release` workflow fails the job with a non-zero exit code if any required artifact is missing from the assembled bundle.
- [ ] An integration test file exists at `tests/integration/test_packaged_executable_assets.py` and is collected by pytest.
- [ ] The integration test executes `pyinstaller -y release.spec` and fails if the PyInstaller command exits non-zero.
- [ ] The integration test copies/moves only the produced packaged output (not the repository) into a temporary isolated directory and executes the binary from that isolated directory.
- [ ] The integration test asserts the packaged executable successfully locates and loads the bundled default configuration asset when executed from the isolated directory.
- [ ] The integration test asserts the packaged executable successfully locates and loads at least one bundled template asset when executed from the isolated directory.
- [ ] A Windows-specific integration test file exists at `tests/integration/test_windows_runner_cmd.py` and is skipped automatically on non-Windows platforms.
- [ ] The Windows integration test executes `run_counter_risk.cmd` from a temporary directory (separate from repo root) and verifies it launches the packaged executable using a path resolved relative to the `.cmd` file location.
- [ ] `run_counter_risk.cmd` does not invoke `python`, `py`, or a `.py` entrypoint; it directly invokes the built executable.
- [ ] The Windows integration test verifies that CLI arguments passed to `run_counter_risk.cmd` are forwarded unchanged to the packaged executable (including at least one flag and one value).
- [ ] A unit test file exists at `tests/unit/test_template_bundling_duplicates.py` and includes a test case that creates at least two different template source directories containing a colliding template filename.
- [ ] When duplicate template filenames are present, the bundling logic either (A) raises an exception whose message includes every conflicting filename and all corresponding source paths, OR (B) applies a deterministic precedence rule documented in code and validated by unit tests.
- [ ] A shared numeric comparison helper exists (or is updated) at `tests/utils/assertions.py` (e.g., `assert_numeric_outputs_close`) and accepts explicit absolute and relative tolerances as parameters (or exposes clearly defined defaults).
- [ ] All fixture-based transformation tests that assert numeric outputs (CSV/TSV/JSON/parquet/etc.) use the shared numeric comparison helper and do not perform byte-for-byte equality checks for numeric fields.
- [ ] At least one updated fixture-based test asserts numeric results within both absolute and relative tolerance (i.e., the test calls the helper with explicit tolerances rather than relying on implicit float equality).
- [ ] `src/counter_risk/build/release.py` `_run_pyinstaller` captures PyInstaller stdout and stderr and logs them on success.
- [ ] `src/counter_risk/build/release.py` `_run_pyinstaller` captures PyInstaller stdout and stderr and logs them on failure before raising/returning a non-zero result.
- [ ] `resolve_runtime_path` behavior is tightened such that when an asset cannot be found in any bundle root it either raises a specific exception type with a clear message OR emits a warning containing the asset name and attempted roots.
- [ ] Unit tests in `tests/unit/test_runtime_paths.py` cover the missing-asset scenario and assert the chosen behavior (exception or warning) including message contents mentioning the requested asset and at least one searched location.
- [ ] Unit tests in `tests/unit/test_runtime_paths.py` include a misconfiguration scenario (e.g., wrong bundle root / missing env var / incorrect `_MEIPASS`) and assert that the failure is surfaced (exception or warning) rather than silently falling back to an unrelated path.
- [ ] `src/counter_risk/pipeline/run.py` `_refresh_ppt_links` no longer silently swallows COM exceptions; it either re-raises an exception with added context or returns a structured explicit error object/value that callers can check.
- [ ] A unit test file exists at `tests/unit/test_refresh_ppt_links_errors.py` and includes a test that forces a COM operation failure and asserts the failure is surfaced via (A) a raised exception containing contextual information, or (B) an explicit structured error plus an error log record.

## Implementation Notes
- Workflow (`.github/workflows/release.yml`)
  - Ensure ordering is: checkout → setup-python → install deps → run tests → run `pyinstaller -y release.spec` → assemble versioned bundle → validate required artifacts → upload artifact.
  - Validation should explicitly check for:
    - Files: `VERSION`, `manifest.json`, default config file, `run_counter_risk.cmd`, built executable
    - Directories: `templates/`
    - README content: at least one line containing substring `How to run`
  - Validation must hard-fail (non-zero exit) on any missing/invalid requirement.
- Integration packaged-binary test (`tests/integration/test_packaged_executable_assets.py`)
  - Build using subprocess with strict failure handling (e.g., `check=True`).
  - Execute the produced binary from a temp directory containing only the packaged output (avoid PYTHONPATH/PATH tricks that pick up the repo).
  - Assert behavior that demonstrates assets are *loaded* (e.g., program output, created output files, or an exit path that requires config/template availability).
- Windows `.cmd` integration test (`tests/integration/test_windows_runner_cmd.py`)
  - Mark skip on non-Windows platforms.
  - Copy the `.cmd` and packaged executable into a temp directory; run the `.cmd` with `cwd` set to that temp directory.
  - Validate: relative path resolution, no python invocation, and argument forwarding (include at least one `--flag value` pair).
- Template duplicate detection tests
  - Create at least two source directories with colliding template filenames; invoke the bundling logic.
  - Assert either a comprehensive error (filename + all source paths) or a deterministic precedence rule (and test it).
- Numeric fixture comparisons
  - Centralize numeric comparisons in `tests/utils/assertions.py` with explicit `abs_tol` and `rel_tol`.
  - Replace byte-for-byte numeric comparisons across fixture-based tests with the helper; ensure at least one test demonstrates passing explicit tolerances.
- PyInstaller logging (`src/counter_risk/build/release.py`)
  - Capture both stdout and stderr in success and failure paths and log them so CI provides actionable diagnostics.
- Runtime path resolution (`src/counter_risk/**/runtime_paths.py`)
  - On missing assets: choose raise or warning, but make it explicit and message-rich (asset name + attempted roots).
  - Add unit tests for missing asset and a misconfiguration scenario (e.g., incorrect `_MEIPASS`).
- COM error handling (`src/counter_risk/pipeline/run.py`)
  - Ensure `_refresh_ppt_links` does not silently swallow COM failures; re-raise with context or return a structured explicit error.
  - Test using mocking + `caplog` (or exception assertions) to guarantee failures surface.

## Notes
<details>
<summary>Background (previous attempt context)</summary>

- Existing tests merely verify file existence or simulate behavior using PYTHONPATH injection for the runner script. This does not test the executable's behavior in a realistic, isolated release environment or verify true relative path resolution. Develop tests that run the actual bundled executable (and the `.cmd` script) in an environment that mimics a production release (without repo checkout paths), ensuring that asset resolution and execution behave as expected.
- Relying solely on mocks for verifying config and template asset resolution does not validate runtime behavior. Implement an integration test that executes the packaged binary and observes its behavior when accessing bundled assets.

</details>
```
</details>

## Deferred Tasks (Requires Human)

- [ ] Create `.github/workflows/release.yml` to: checkout → `actions/setup-python` → install deps → run full test suite → run `pyinstaller -y release.spec` → assemble a versioned release bundle → validate required artifacts (`VERSION`, `manifest.json`, `templates/`, default config file, `run_counter_risk.cmd`, `README` containing `How to run`, and the built executable) → upload the bundle as a workflow artifact (fail non-zero on any missing artifact). (AGENT_LIMITATIONS: Cannot modify .github/workflows/*.yml (protected) | Request manual creation of the workflow file by a maintainer with repository write access, or provide the complete workflow YAML content for manual addition.)