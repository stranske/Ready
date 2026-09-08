# Follow-up: Implement Release Workflow, Harden Platform Detection, and Add VBA Signature Tests

<!-- follow-up-depth: 2 -->

## Why
PR #100 addressed issue #99, but verification identified remaining gaps (verdict: **FAIL**). This follow-up issue focuses on implementing the missing executable release workflow, hardening/standardizing `validate_release_bundle.sh` platform detection and messaging, and adding targeted automated tests (including VBA source signature checks) so the requirements are enforced without manual inspection.

## Source
- Original PR: #100
- Parent issue: #99

## Scope
Implement an executable GitHub Actions release workflow that runs on `workflow_dispatch`, builds and validates a `release/` bundle, and uploads it as an artifact. Refactor `validate_release_bundle.sh` to centralize OS/Windows detection and standardize the missing-`gh` error message, and add/adjust automated tests including shell tests for platform detection and Python tests for `assets/vba/RunnerLaunch.bas` `BuildCommand` signature/date-handling checks.

## Non-Goals
- Changing the requirement that `scripts/validate_release_bundle.sh` hard-requires `gh`
- Adding manual verification steps or automation to validate consistency between VBA source and binary asset
- Background context and advisory items are documented in the Notes section below

## Tasks

### Platform Detection Refactoring
- [ ] Create a new platform detection function named `detect_platform` or `is_windows_like` in `validate_release_bundle.sh` with a clear function signature that returns a platform identifier string or boolean
- [ ] Implement platform detection logic in the new function using `uname` command output to check for platform strings
- [ ] Add environment variable checks to the platform detection function for `OS`, `MSYSTEM`, and `OSTYPE` variables
- [ ] Add pattern matching in the platform detection function to handle `CYGWIN*`, `MINGW*`, and `MSYS*` patterns in environment variables or uname output
- [ ] Refactor all existing platform-specific code branches in `validate_release_bundle.sh` to call the new detection function instead of inline checks

### Error Message Standardization
- [ ] Update `validate_release_bundle.sh` to define a single standardized error message variable for missing `gh` executable containing the keywords `gh`, `not found`, `required`, and `install`
- [ ] Update all code paths in `validate_release_bundle.sh` that check for `gh` availability to print the standardized error message and exit with non-zero status
- [ ] Update the corresponding test in `tests/test_validate_release_bundle.sh` to assert the exact standardized error message string using string equality comparison

### Platform Detection Tests
- [ ] Create test infrastructure in `tests/test_validate_release_bundle.sh` for stubbing the `uname` command by creating a temporary directory and fake `uname` script prepended to PATH
- [ ] Add test case in `tests/test_validate_release_bundle.sh` that simulates Linux environment by stubbing `uname` to return `Linux` and asserting Unix-like branch selection
- [ ] Add test case in `tests/test_validate_release_bundle.sh` that simulates macOS environment by stubbing `uname` to return `Darwin` and asserting Unix-like branch selection
- [ ] Add test case in `tests/test_validate_release_bundle.sh` that simulates Cygwin environment by setting `OSTYPE=cygwin` and asserting Windows-like branch selection
- [ ] Add test case in `tests/test_validate_release_bundle.sh` that simulates MinGW environment by setting `MSYSTEM=MINGW64` and asserting Windows-like branch selection
- [ ] Add test case in `tests/test_validate_release_bundle.sh` that simulates MSYS environment by stubbing `uname` to return `MSYS_NT-10.0` and asserting Windows-like branch selection

### VBA Source Signature Tests
- [ ] Implement text file reading and parsing logic in `tests/test_vba_runnerlaunch_signature.py` to load and parse `assets/vba/RunnerLaunch.bas` as plain text
- [ ] Add test function in `tests/test_vba_runnerlaunch_signature.py` that asserts `BuildCommand` function signature matches regex `Sub\s+BuildCommand\s*\([^,]+,[^,]+,[^,]+\)` to verify exactly three parameters
- [ ] Add test function in `tests/test_vba_runnerlaunch_signature.py` that asserts the `BuildCommand` function body contains at least one line matching regex `(CDate|DateValue|DateSerial)\s*\(` to verify date parsing logic is present

## Deferred Tasks (Requires Human)

The following tasks require manual intervention by a maintainer with repository permissions, as agents cannot modify files under `.github/workflows/` directory per AGENT_LIMITATIONS:

- [ ] **Create `.github/workflows/release.yml`**: Create the basic workflow file structure with `workflow_dispatch` trigger and job definition
- [ ] **Add checkout and Python setup steps**: Add `actions/checkout@v3` or later and `actions/setup-python@v4` or later with Python 3.8+ specified
- [ ] **Add dependency installation step**: Add step that installs required Python packages from `requirements.txt` using `pip install -r requirements.txt`
- [ ] **Add test execution step**: Add step that runs the repository test suite using `pytest` or equivalent with exit code 0 required before proceeding
- [ ] **Add PyInstaller build step**: Add step that executes `pyinstaller` with spec file producing executable artifacts in `dist/` directory
- [ ] **Add release directory population step**: Add step to copy all required files from `dist/` and other locations into a top-level `release/` directory with correct structure
- [ ] **Add validation step**: Add step that runs `validate_release_bundle.sh release/` with exit code 0 required to verify bundle integrity
- [ ] **Add artifact upload step**: Add step using `actions/upload-artifact@v3` or later to upload the `release/` directory with retention-days configured
- [ ] **Configure workflow_dispatch input**: Ensure the `workflow_dispatch` trigger includes a `version` input with `required: false` or omit the `required` field entirely

**Suggested Approach**: Create a draft workflow specification at `docs/workflows/release.yml.spec` documenting all required steps, action versions, and configurations. This specification can be used by maintainers to manually create or update `.github/workflows/release.yml`.

## Acceptance Criteria
- [ ] `validate_release_bundle.sh` contains a function named `detect_platform` or `is_windows_like` that is called at least once before any platform-specific code paths
- [ ] `tests/test_validate_release_bundle.sh` includes at least 5 test cases covering: (1) Linux via uname, (2) macOS via uname, (3) Cygwin via OSTYPE, (4) MinGW via MSYSTEM, (5) MSYS via uname pattern, with each test asserting the expected platform string or boolean return value
- [ ] When `gh` executable is not found, `validate_release_bundle.sh` exits with non-zero status and prints the exact standardized error message
- [ ] The test in `tests/test_validate_release_bundle.sh` for missing `gh` asserts the exact standardized error message string using string equality comparison (not substring matching)
- [ ] `tests/test_vba_runnerlaunch_signature.py` contains a test that parses `assets/vba/RunnerLaunch.bas` and asserts: (1) `BuildCommand` function signature matches regex `Sub\s+BuildCommand\s*\([^,]+,[^,]+,[^,]+\)` (exactly 3 parameters), and (2) the function body contains at least one line matching regex `(CDate|DateValue|DateSerial)\s*\(` indicating date parsing logic is present
- [ ] All new tests in `tests/test_validate_release_bundle.sh` and `tests/test_vba_runnerlaunch_signature.py` pass when executed
- [ ] `.github/workflows/release.yml` exists on the default branch and triggers via `workflow_dispatch` (deferred, requires human)
- [ ] The release workflow uses `actions/checkout@v3` or later, `actions/setup-python@v4` or later with Python 3.8+, installs dependencies from `requirements.txt`, runs `pytest` or equivalent test command with exit code 0 required, executes `pyinstaller` with spec file producing executable in `dist/`, copies all required files to `release/` directory, executes `validate_release_bundle.sh release/` with exit code 0 required, and uploads `release/` directory using `actions/upload-artifact@v3` with retention-days set (deferred, requires human)
- [ ] The `workflow_dispatch` input `version` (if present) has `required: false` or the `required` field is omitted, allowing the workflow to be started without providing it (deferred, requires human)

## Implementation Notes

### Platform Detection Function
Introduce a function (e.g., `detect_platform()` / `is_windows_like()`) that centralizes detection based on `uname` plus environment variables (`OS`, `MSYSTEM`, `OSTYPE`) and common Windows-like `uname` patterns (`CYGWIN*`, `MINGW*`, `MSYS*`). Avoid deeply nested conditionals; prefer a linear, readable decision structure. The function should:
- First check `uname` output for explicit platform strings
- Then check environment variables in order of specificity
- Use pattern matching (e.g., `case` statements) for Windows-like patterns
- Return a consistent value (string or boolean) that calling code can use for branching

### Error Message Standardization
Define the missing-`gh` error message as a single variable at the top of `validate_release_bundle.sh`, for example:
```bash
MISSING_GH_ERROR="Error: gh executable not found. The gh CLI is required for release validation. Please install it from https://cli.github.com/"
```
Update all code paths that check for `gh` to use this variable and update tests to match exactly (not substring/keyword matching).

### Test Infrastructure for Platform Detection
In `tests/test_validate_release_bundle.sh`, simulate OS environments by:
- Creating a temporary directory for test fixtures
- Writing a fake `uname` script to the temporary directory that echoes the desired platform string
- Prepending the temporary directory to `PATH` so the fake `uname` is found first
- Exporting/unsetting `OS`, `MSYSTEM`, `OSTYPE` as needed for each test case
- Sourcing or executing `validate_release_bundle.sh` in a subshell to test the detection function
- Asserting the selected branch deterministically via output markers, exit codes, or function return values
- Cleaning up the temporary directory after each test

### VBA Source Validation
Implement/adjust `tests/test_vba_runnerlaunch_signature.py` to:
- Open and read `assets/vba/RunnerLaunch.bas` as a text file
- Use regex to locate the `BuildCommand` function signature
- Assert the signature matches the expected pattern with exactly three parameters
- Search the function body for date parsing function calls
- Use whitespace-resilient regex patterns that allow for variations in formatting but are strict about the presence of required elements

### Release Workflow (Deferred)
When creating `.github/workflows/release.yml` (requires human intervention):
- Use `workflow_dispatch` with an optional `version` input (`required: false` or omitted)
- Keep paths and artifacts deterministic: build outputs should be copied into a top-level `release/` directory before validation and upload
- Ensure the workflow runs the repository's test suite before building
- Validate the resulting `release/` bundle by invoking `validate_release_bundle.sh release/`
- Use specific action versions (e.g., `actions/checkout@v3`, `actions/setup-python@v4`, `actions/upload-artifact@v3`)
- Configure artifact retention appropriately (e.g., `retention-days: 90`)

## Notes

### Advisory Items (Non-blocking)
- **Minor risk**: `scripts/validate_release_bundle.sh` now hard-requires `gh` even though the script's shown logic does not use `gh` for bundle validation; this may be intentional per requirements but increases coupling and can break local validation unless users install/stub `gh`

### Background (Previous Attempt Context)
- **What failed**: Relying solely on `docs/release.yml.draft` and helper scripts for validating the release workflow  
  **Why it failed**: The absence of an active `.github/workflows/release.yml` file means validation tests only work on a draft and do not reflect the live release process  
  **What to try instead**: Ensure that the actual workflow file exists on the default branch and is referenced directly during testing rather than relying on drafts

- **What failed**: Assuming that updates to the VBA binary asset can be validated through diff alone  
  **Why it failed**: The diff does not confirm that the regenerated binary is in sync with the VBA source, leading to potential inaccuracies  
  **What to try instead**: Include a manual verification step or add automated tests that can validate the consistency between the VBA source and the binary if possible