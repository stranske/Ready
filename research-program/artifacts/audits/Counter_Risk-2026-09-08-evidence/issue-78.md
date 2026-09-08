## Why

PR #76 addressed issue #24, but verification identified concerns (verdict: **CONCERNS**) around producing a truly portable release artifact, ensuring deterministic template bundling behavior, strengthening fixture validation to check transformation correctness (not just copying), and adding CI + documentation to standardize and verify releases. This follow-up closes those gaps with concrete build, packaging, test, and workflow tasks.

## Scope

Add PyInstaller-based executable builds, integrate them into the packaging flow, update the Windows runner to execute the bundled binary, enforce deterministic template conflict handling, strengthen fixture tests to validate numeric transformations within tolerances, add a release CI workflow to build/test/package/validate/upload the bundle, and document the release checklist and expected bundle contents.

## Non-Goals

_Not provided._

## Tasks

- [ ] Create a PyInstaller spec file `release.spec` at repo root that builds the pipeline CLI entrypoint into an executable named `counter-risk` (and `counter-risk.exe` on Windows), bundling required package data (templates + default config) and any runtime hooks needed for path resolution.
  - [ ] Create a PyInstaller spec file at repo root with Analysis (verify: confirm completion in repo)
  - [ ] Create a PyInstaller spec file at repo root with EXE (verify: confirm completion in repo)
  - [ ] Define scope for: Create a PyInstaller spec file at repo root with and COLLECT sections for the pipeline CLI entrypoint (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Create a PyInstaller spec file at repo root with and COLLECT sections for the pipeline CLI entrypoint (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Create a PyInstaller spec file at repo root with and COLLECT sections for the pipeline CLI entrypoint (verify: confirm completion in repo)
  - [ ] Define scope for: Configure the spec file to produce an executable named counter-risk with platform-specific extensions (verify: config validated)
  - [ ] Implement focused slice for: Configure the spec file to produce an executable named counter-risk with platform-specific extensions (verify: config validated)
  - [ ] Validate focused slice for: Configure the spec file to produce an executable named counter-risk with platform-specific extensions (verify: config validated)
  - [ ] Add datas configuration to bundle templates (verify: config validated)
  - [ ] default config files into the executable (verify: config validated)
  - [ ] Define scope for: Implement runtime hooks or path resolution helpers to locate bundled assets at runtime (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Implement runtime hooks or path resolution helpers to locate bundled assets at runtime (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Implement runtime hooks or path resolution helpers to locate bundled assets at runtime (verify: confirm completion in repo)
- [ ] Update `src/counter_risk/build/release.py` to invoke PyInstaller using `release.spec` during packaging, fail with non-zero exit code on PyInstaller failure, and fail fast with clear errors if `release.spec` or the expected `dist/...` executable output is missing.
  - [ ] Define scope for: Update release.py to invoke PyInstaller using release.spec via subprocess during the packaging flow (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Update release.py to invoke PyInstaller using release.spec via subprocess during the packaging flow (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Update release.py to invoke PyInstaller using release.spec via subprocess during the packaging flow (verify: confirm completion in repo)
  - [ ] Define scope for: Add error handling to exit with non-zero code when PyInstaller returns a failure status (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Add error handling to exit with non-zero code when PyInstaller returns a failure status (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Add error handling to exit with non-zero code when PyInstaller returns a failure status (verify: confirm completion in repo)
  - [ ] Define scope for: Add validation to fail fast with clear error messages if release.spec is missing before invoking PyInstaller (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Add validation to fail fast with clear error messages if release.spec is missing before invoking PyInstaller (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Add validation to fail fast with clear error messages if release.spec is missing before invoking PyInstaller (verify: confirm completion in repo)
  - [ ] Define scope for: Add validation to fail fast with clear error messages if the expected dist executable is missing after PyInstaller completes (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Add validation to fail fast with clear error messages if the expected dist executable is missing after PyInstaller completes (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Add validation to fail fast with clear error messages if the expected dist executable is missing after PyInstaller completes (verify: confirm completion in repo)
- [ ] Update `src/counter_risk/build/release.py` to copy the built executable from `dist/...` into a deterministic location under `release/<version>/` (e.g., `release/<version>/bin/counter-risk(.exe)`), and add/keep an automated check that `release/<version>/VERSION` equals the `manifest.json` version field.
- [ ] Update `run_counter_risk.cmd` to execute the bundled executable (not `python`/`py`), resolving the executable path relative to the `.cmd` location (e.g., via `%~dp0`) and passing through `%*` unchanged.
- [ ] Implement deterministic template conflict handling during bundle assembly by detecting duplicate template filenames across template source directories and either enforcing an explicit precedence rule in code or raising an error that lists each conflicting filename and all source paths.
- [ ] Add a numeric comparison test helper in `tests/utils/assertions.py` (or equivalent) that compares parsed numeric outputs with configurable `atol` and `rtol`.
- [ ] Update fixture-based transformation tests to parse numeric outputs (CSV/TSV/JSON/parquet as applicable to fixtures) and compare using the helper with explicitly specified `atol`/`rtol` values instead of byte-for-byte equality.
- [ ] Add a GitHub Actions workflow `.github/workflows/release.yml` that (1) sets up Python, (2) installs dependencies, (3) runs unit + fixture tests, (4) builds the PyInstaller executable with `release.spec`, (5) runs the packaging script to assemble `release/<version>/...`, (6) validates required bundle files exist, and (7) uploads the release bundle as an artifact.
  - [ ] Create the release.yml workflow file with Python setup (verify: confirm completion in repo)
  - [ ] Create the release.yml workflow file with dependency installation steps (verify: dependencies updated)
  - [ ] Add a workflow step to run unit (verify: confirm completion in repo)
  - [ ] fixture tests before building (verify: tests pass)
  - [ ] Add a workflow step to build the PyInstaller executable using release.spec (verify: confirm completion in repo)
  - [ ] Add a workflow step to run the packaging script (verify: confirm completion in repo)
  - [ ] assemble the versioned release directory (verify: confirm completion in repo)
  - [ ] Define scope for: Add a workflow step to validate that all required bundle files exist in the release directory (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Add a workflow step to validate that all required bundle files exist in the release directory (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Add a workflow step to validate that all required bundle files exist in the release directory (verify: confirm completion in repo)
  - [ ] Define scope for: Add a workflow step to upload the release bundle as a GitHub Actions artifact (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Add a workflow step to upload the release bundle as a GitHub Actions artifact (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Add a workflow step to upload the release bundle as a GitHub Actions artifact (verify: confirm completion in repo)
- [ ] Write `docs/RELEASE_CHECKLIST.md` documenting the commands to build via PyInstaller (`release.spec`), run packaging, validate bundle contents, and trigger/run the release workflow, plus an explicit list of expected bundle contents.

## Acceptance Criteria

- [ ] `release.spec` exists at repo root and defines an `Analysis`/`EXE`/`COLLECT` (one-folder) or `EXE` (one-file) build for the pipeline CLI entrypoint, producing an executable named `counter-risk` (or `counter-risk.exe` on Windows).
- [ ] Running `pyinstaller -y release.spec` on a clean workspace produces the executable artifact at `dist/counter-risk/counter-risk` (one-folder) or `dist/counter-risk` (one-file) on Linux/macOS, and `dist\counter-risk\counter-risk.exe` or `dist\counter-risk.exe` on Windows (depending on chosen mode).
- [ ] The PyInstaller build includes required package data such that, when run from `dist/...`, the executable can load the default configuration and template assets without referencing the repo checkout paths.
- [ ] `src/counter_risk/build/release.py` invokes PyInstaller using `release.spec` as part of the packaging flow and exits non-zero if PyInstaller fails.
- [ ] After packaging completes, the versioned release directory contains the bundled executable at a deterministic path (e.g., `release/<version>/bin/counter-risk(.exe)` or `release/<version>/counter-risk(.exe)`), and the packaging command fails if the executable is not present at the expected PyInstaller output location.
- [ ] `run_counter_risk.cmd` does not invoke `python` and instead executes the bundled executable using a path resolved relative to the location of the `.cmd` file, passing through all CLI args unchanged.
- [ ] Template bundle assembly detects duplicate template filenames across template source directories and applies one deterministic policy: either (A) raise an error that lists every conflicting filename and all source paths for each conflict, or (B) apply a documented precedence order that is enforced in code and covered by a unit test.
- [ ] Fixture-based transformation tests compare numeric outputs using absolute/relative tolerances rather than byte-for-byte file equality for supported numeric formats (CSV/TSV/JSON/parquet as applicable to the fixtures).
- [ ] `tests/utils/assertions.py` (or the chosen helper path) exists and provides a function that compares numeric outputs with configurable `atol` and `rtol`, and fixture tests call this helper with explicitly defined tolerance values (not implicit defaults).
- [ ] `.github/workflows/release.yml` exists and, on workflow execution, performs these steps in order: (1) sets up Python, (2) installs dependencies, (3) runs unit + fixture tests, (4) builds the PyInstaller executable using `release.spec`, (5) runs the packaging script to assemble the versioned release bundle, (6) validates required bundle files exist, and (7) uploads the release bundle as a workflow artifact.
- [ ] The release workflow includes an explicit validation step that fails the job if any required bundle artifact is missing: `VERSION`, `manifest.json`, templates directory, default config file, runner script, README ("How to run"), and the bundled executable.
- [ ] Packaging produces a versioned release directory where `VERSION` file content exactly matches the `manifest.json` version field value.
- [ ] The versioned release directory contains a README file whose title line includes the exact phrase `How to run`.
- [ ] `docs/RELEASE_CHECKLIST.md` exists and contains: (1) the exact command(s) to run the release workflow locally or in CI, (2) the packaging command(s), (3) the validation command(s) to confirm bundle contents, and (4) an explicit list of expected bundle contents including the executable, runner, templates, default config, `VERSION`, and `manifest.json`.
- [ ] A fixture-based run executed using the produced release bundle (calling the bundled executable or the updated runner) produces numeric outputs that match the expected fixture values within the tolerances defined in the fixture tests.

## Implementation Notes

**PyInstaller spec (`release.spec`)**
Place at repo root.
Ensure the chosen build mode (one-folder vs one-file) is reflected consistently in expected `dist/` output paths, the packaging script copy logic, and the runner script path resolution.
Include required package data (templates + default config) using `datas=` and/or PyInstaller hooks as appropriate.
If the app resolves asset paths at runtime, prefer a single helper that handles both source-tree execution and PyInstaller execution (e.g., checking `sys._MEIPASS`), and update `src/counter_risk/**` only where needed.

**Packaging flow (`src/counter_risk/build/release.py`)**
Invoke PyInstaller via subprocess (or module invocation) using `release.spec`.
Fail fast with clear errors for missing `release.spec`, PyInstaller non-zero exit, and missing expected `dist/...` executable path after a “successful” build.
Copy the executable into a deterministic location inside `release/<version>/...`.
Add/keep an automated check that `release/<version>/VERSION` equals `release/<version>/manifest.json`’s version field.

**Windows runner (`run_counter_risk.cmd`)**
Must not call `python`/`py`.
Resolve the executable path relative to the `.cmd` file directory (e.g., via `%~dp0`) and pass through `%*` unchanged.
Keep the executable location aligned with the packaging output (e.g., `bin\counter-risk.exe`).

**Template conflict handling**
Implement an explicit and deterministic policy: either raise on duplicates with a message listing each filename and all source paths, or enforce a documented precedence ordering and add a unit test that proves it.
Avoid filesystem traversal-order dependence; sort inputs and/or make precedence explicit.

**Fixture test improvements**
Replace byte-for-byte comparisons for numeric outputs with parsing + numeric comparison.
Add `tests/utils/assertions.py` (or equivalent) helper(s) that accept explicit `atol` and `rtol` values; fixture tests must pass explicit tolerances.
Keep expected fixture values stable; only normalize fixture formats if necessary to support parsing/typing.

**Release CI (`.github/workflows/release.yml`)**
Include steps: setup → install → tests → PyInstaller build → packaging → validate required bundle files → upload artifact.
Validation step should explicitly check for: `VERSION`, `manifest.json`, templates dir, default config, runner script, README with `# How to run`, and the bundled executable.

**Docs (`docs/RELEASE_CHECKLIST.md`)**
Include concrete commands for building via PyInstaller (`release.spec`), running packaging, validating bundle contents, and running/triggering the workflow in CI.
List expected bundle contents explicitly.

<details>
<summary>Original Issue</summary>

```text
<!-- follow-up-depth: 1 -->
## Why
PR #76 addressed issue #24, but verification identified concerns (verdict: **CONCERNS**) around producing a truly portable release artifact, ensuring deterministic template bundling behavior, strengthening fixture validation to check transformation correctness (not just copying), and adding CI + documentation to standardize and verify releases. This follow-up closes those gaps with concrete build, packaging, test, and workflow tasks.

## Source
- Original PR: #76
- Parent issue: #24

## Tasks
- [ ] Add a PyInstaller build definition (e.g., `release.spec`) that bundles the pipeline entrypoint into a single-folder or single-file executable, including required package data (templates/default config) and any runtime hooks needed for path resolution.
- [ ] Update the release bundling script to invoke PyInstaller as part of packaging and to copy the built executable into the versioned release directory; fail fast with clear errors if the executable is missing.
- [ ] Update the Windows runner script to call the bundled executable (and not `python ...`), resolving paths relative to the runner location and passing through CLI args.
- [ ] Implement deterministic template conflict handling during bundle assembly: detect duplicate template filenames across source directories and either (a) apply an explicit precedence rule in code or (b) raise an error listing conflicts.
- [ ] Enhance fixture-based tests to validate transformation outputs numerically within tolerances (e.g., parse outputs to numeric arrays/dataframes and compare with abs/rel tolerance) instead of byte-for-byte file equality.
- [ ] Add a release CI workflow that builds the executable via PyInstaller, runs unit/fixture tests, assembles the versioned release bundle, validates required files exist, and uploads the bundle as an artifact.
- [ ] Add release checklist documentation describing the automated release steps, validation commands, and bundle contents expectations.

## Acceptance Criteria
- [ ] A PyInstaller spec file named `release.spec` exists at repo root and defines an `Analysis`/`EXE`/`COLLECT` (one-folder) or `EXE` (one-file) build for the pipeline CLI entrypoint, producing an executable named `counter-risk` (or `counter-risk.exe` on Windows).
- [ ] Running `pyinstaller -y release.spec` on a clean workspace produces the executable artifact at `dist/counter-risk/counter-risk` (one-folder) or `dist/counter-risk` (one-file) on Linux/macOS, and `dist\counter-risk\counter-risk.exe` or `dist\counter-risk.exe` on Windows (depending on chosen mode).
- [ ] The PyInstaller build includes required package data such that, when run from `dist/...`, the executable can load the default configuration and template assets without referencing the repo checkout paths.
- [ ] The release bundling script `src/counter_risk/build/release.py` invokes PyInstaller using `release.spec` as part of the packaging flow and fails with a non-zero exit code if PyInstaller fails.
- [ ] After packaging completes, the versioned release directory contains the bundled executable at a deterministic path (e.g., `release/<version>/bin/counter-risk(.exe)` or `release/<version>/counter-risk(.exe)`), and the packaging command fails fast if the executable is not present at the expected PyInstaller output location.
- [ ] The Windows runner script `run_counter_risk.cmd` does not invoke `python` and instead executes the bundled executable using a path resolved relative to the location of the `.cmd` file, passing through all CLI args unchanged.
- [ ] Template bundle assembly detects duplicate template filenames across template source directories and applies one deterministic policy: either (A) raise an error that lists every conflicting filename and all source paths for each conflict, or (B) apply a documented precedence order that is enforced in code and covered by a unit test.
- [ ] Fixture-based transformation tests compare numeric outputs using absolute/relative tolerances rather than byte-for-byte file equality for supported numeric formats (CSV/TSV/JSON/parquet as applicable to the fixtures).
- [ ] A test helper exists (e.g., `tests/utils/assertions.py`) providing a function that compares numeric outputs with configurable `atol` and `rtol`, and the fixture tests call this helper with explicitly defined tolerance values (not implicit defaults).
- [ ] The repository contains `.github/workflows/release.yml` which, on workflow execution, performs these steps in order: (1) sets up Python, (2) installs dependencies, (3) runs unit + fixture tests, (4) builds the PyInstaller executable using `release.spec`, (5) runs the packaging script to assemble the versioned release bundle, (6) validates required bundle files exist, and (7) uploads the release bundle as a workflow artifact.
- [ ] The release workflow includes an explicit validation step that fails the job if any required bundle artifact is missing: `VERSION`, `manifest.json`, templates directory, default config file, runner script, README ("How to run"), and the bundled executable.
- [ ] Packaging produces a versioned release directory where `VERSION` file content exactly matches the `manifest.json` version field value.
- [ ] The versioned release directory contains a README file whose title line includes the exact phrase `How to run`.
- [ ] `docs/RELEASE_CHECKLIST.md` exists and contains: (1) the exact command(s) to run the release workflow locally or in CI, (2) the packaging command(s), (3) the validation command(s) to confirm bundle contents, and (4) an explicit list of expected bundle contents including the executable, runner, templates, default config, `VERSION`, and `manifest.json`.
- [ ] A fixture-based run executed using the produced release bundle (calling the bundled executable or the updated runner) produces numeric outputs that match the expected fixture values within the tolerances defined in the fixture tests.

## Implementation Notes
- **PyInstaller spec (`release.spec`)**
  - Place at repo root.
  - Ensure the chosen build mode (one-folder vs one-file) is reflected consistently in:
    - expected `dist/` output paths,
    - the packaging script copy logic,
    - the runner script path resolution.
  - Include required package data (templates + default config) using `datas=` and/or PyInstaller hooks as appropriate.
  - If the app resolves asset paths at runtime, prefer a single helper that handles both source-tree execution and PyInstaller execution (e.g., checking `sys._MEIPASS`), and update `src/counter_risk/**` only where needed.

- **Packaging flow (`src/counter_risk/build/release.py`)**
  - Invoke PyInstaller via subprocess (or module invocation) using `release.spec`.
  - Fail fast with clear errors for:
    - missing `release.spec`,
    - PyInstaller non-zero exit,
    - missing expected `dist/...` executable path after a “successful” build.
  - Copy the executable into a deterministic location inside `release/<version>/...`.
  - Add/keep an automated check that `release/<version>/VERSION` equals `release/<version>/manifest.json`’s version field.

- **Windows runner (`run_counter_risk.cmd`)**
  - Must not call `python`/`py`.
  - Resolve the executable path relative to the `.cmd` file directory (e.g., via `%~dp0`) and pass through `%*` unchanged.
  - Keep the executable location aligned with the packaging output (e.g., `bin\counter-risk.exe`).

- **Template conflict handling**
  - Implement an explicit and deterministic policy:
    - either raise on duplicates with a message listing each filename and all source paths,
    - or enforce a documented precedence ordering and add a unit test that proves it.
  - Avoid filesystem traversal-order dependence; sort inputs and/or make precedence explicit.

- **Fixture test improvements**
  - Replace byte-for-byte comparisons for numeric outputs with parsing + numeric comparison.
  - Add `tests/utils/assertions.py` (or equivalent) helper(s) that accept explicit `atol` and `rtol` values; fixture tests must pass explicit tolerances.
  - Keep expected fixture values stable; only normalize fixture formats if necessary to support parsing/typing.

- **Release CI (`.github/workflows/release.yml`)**
  - Include steps: setup → install → tests → PyInstaller build → packaging → validate required bundle files → upload artifact.
  - Validation step should explicitly check for: `VERSION`, `manifest.json`, templates dir, default config, runner script, README with `# How to run`, and the bundled executable.

- **Docs (`docs/RELEASE_CHECKLIST.md`)**
  - Include concrete commands for:
    - building via PyInstaller (`release.spec`),
    - running packaging,
    - validating bundle contents,
    - running the workflow (or referencing how to trigger it in CI).
  - List expected bundle contents explicitly.

## Notes
<details>
<summary>Background (previous attempt context)</summary>

- **What failed:** Relying on the system's Python interpreter via a hard-coded `python` call in `run_counter_risk.cmd`  
  **Why it failed:** This violates the portability requirement and prevents execution on systems without Python installed.  
  **What to try instead:** Use a bundled executable (built with PyInstaller) and update the runner script to reference that executable bundled with the release.

- **What failed:** Deduping templates based solely on filename order without handling duplicate names between `templates/` and `tests/fixtures/`  
  **Why it failed:** This can lead to order-dependent behavior and silent selection conflicts if duplicates exist.  
  **What to try instead:** Implement conflict detection and enforce a deterministic policy (explicit precedence or error listing conflicts).

</details>
```
</details>

## Deferred Tasks (Requires Human)

- [ ] Add a GitHub Actions workflow `.github/workflows/release.yml` that (1) sets up Python, (2) installs dependencies, (3) runs unit + fixture tests, (4) builds the PyInstaller executable with `release.spec`, (5) runs the packaging script to assemble `release/<version>/...`, (6) validates required bundle files exist, and (7) uploads the release bundle as an artifact. (AGENT_LIMITATIONS: Cannot modify .github/workflows/*.yml (protected) | Create a template workflow file at a non-protected location (e.g., docs/templates/release.yml.template) with detailed inline comments, then document in RELEASE_CHECKLIST.md that a maintainer must manually copy it to .github/workflows/release.yml)