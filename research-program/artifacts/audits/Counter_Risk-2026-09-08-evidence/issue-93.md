# Add Release CI Workflow to Build and Validate Release Bundles

## Why

The work that started in #24 and was implemented across PRs #76 → #79 → #87 still leaves a key original acceptance criterion unmet on `main`: the repo does not contain a release CI workflow at `.github/workflows/release.yml` (it is missing from the current `main` checkout). Because of that, the "drop-in release bundle" is not being standardized/verified/built in CI (build + test + package + validate + upload an artifact).

**Chain / provenance (for traceability):**
- Original issue: #24
- First PR in chain: #76
- Follow-up issue: #78 (created because verifier raised CONCERNS on #76)
- PR: #79 (still marked `needs-human` at the time)
- Follow-up issue: #86
- PR: #87

### What likely caused repeated ineffective attempts

- **Workflow-file constraints / "needs-human" gaps**: earlier follow-ups explicitly called out inability to add `.github/workflows/release.yml`, which meant a core acceptance criterion could not be satisfied even if code/tests existed.
- **Auto-status summaries overstated completion**: multiple PR bodies marked the workflow task as done, but `main` still lacks the file. This suggests the implementation wasn't validated against the actual repository state before declaring acceptance criteria satisfied.
- **Weak linkage between PRs and issues**: PRs in this chain do not consistently use `Fixes #...` (the GitHub API shows empty `closingIssuesReferences`), making it harder to track what truly closed what and which acceptance criteria remained open.

## Scope

Create supporting scripts and documentation for a GitHub Actions workflow that will:
1. Check out the repo
2. Set up Python
3. Install dependencies
4. Run the full test suite
5. Build the packaged executable via `pyinstaller -y release.spec`
6. Run the release bundling step to produce `release/<version>/...`
7. Validate the required bundle contents exist
8. Upload the versioned release bundle as a workflow artifact

The agent will create all supporting scripts and a complete draft workflow YAML file. A human will then manually add the workflow file to `.github/workflows/release.yml`.

## Non-Goals

- Changing the release bundle format or naming (unless required to satisfy validation)
- Adding a full "GitHub Release" publishing step (artifact upload is sufficient for now)
- Agent directly modifying `.github/workflows/` directory (protected per AGENT_LIMITATIONS)

## Tasks

### Supporting Scripts and Documentation

- [ ] Identify the dependency file used by the project for installation (requirements.txt, setup.py, pyproject.toml, etc.)
- [ ] Identify the release assembly script location and invocation command
- [ ] Create a shell script at `scripts/validate_release_bundle.sh` that checks for the existence of VERSION file in the bundle
- [ ] Add validation logic to `scripts/validate_release_bundle.sh` to verify manifest.json exists in the bundle directory
- [ ] Add validation logic to `scripts/validate_release_bundle.sh` to verify the templates directory exists in the bundle
- [ ] Add validation logic to `scripts/validate_release_bundle.sh` to verify the default config file exists in the bundle
- [ ] Add validation logic to `scripts/validate_release_bundle.sh` to verify run_counter_risk.cmd exists in the bundle
- [ ] Add validation logic to `scripts/validate_release_bundle.sh` to verify a README file exists containing the substring "How to run"
- [ ] Add validation logic to `scripts/validate_release_bundle.sh` to verify the built executable exists with platform-specific naming
- [ ] Configure `scripts/validate_release_bundle.sh` to exit with non-zero code if any check fails
- [ ] Create a complete draft workflow YAML file at `docs/release.yml.draft` defining a `workflow_dispatch` trigger
- [ ] Add workflow steps to `docs/release.yml.draft` to check out the repository and set up Python
- [ ] Add workflow step to `docs/release.yml.draft` to install Python dependencies using the identified method
- [ ] Add workflow step to `docs/release.yml.draft` to install PyInstaller if not included in project dependencies
- [ ] Add workflow step to `docs/release.yml.draft` to run the full test suite before any build step
- [ ] Add workflow step to `docs/release.yml.draft` to build the executable using `pyinstaller -y release.spec`
- [ ] Add workflow step to `docs/release.yml.draft` to execute the release assembly script with appropriate arguments
- [ ] Add workflow step to `docs/release.yml.draft` to run `scripts/validate_release_bundle.sh`
- [ ] Add workflow step to `docs/release.yml.draft` to upload the assembled `release/<version>/` directory as a workflow artifact
- [ ] Create documentation file at `docs/RELEASE_WORKFLOW_SETUP.md` explaining how to move the draft workflow to `.github/workflows/release.yml`

## Deferred Tasks (Requires Human)

These tasks require modifying `.github/workflows/*.yml` files, which agents cannot do per AGENT_LIMITATIONS. After the agent completes the tasks above, a human must:

- [ ] Copy `docs/release.yml.draft` to `.github/workflows/release.yml`
- [ ] Commit and push the workflow file to the repository
- [ ] Manually trigger the workflow using `workflow_dispatch` to verify it works
- [ ] Optionally add push/tag triggers to the workflow if desired

## Acceptance Criteria

**Agent-Completable:**
- [ ] The file `scripts/validate_release_bundle.sh` exists and is executable
- [ ] Running `scripts/validate_release_bundle.sh` with a valid release bundle directory exits with code 0
- [ ] Running `scripts/validate_release_bundle.sh` with a missing required file exits with non-zero code
- [ ] The file `docs/release.yml.draft` exists and contains valid GitHub Actions YAML syntax
- [ ] The file `docs/RELEASE_WORKFLOW_SETUP.md` exists and contains instructions for manual workflow setup
- [ ] The draft workflow YAML includes all required steps: checkout, Python setup, dependency installation, test execution, PyInstaller build, release assembly, validation, and artifact upload

**Human-Completable (After Workflow Added):**
- [ ] The file `.github/workflows/release.yml` exists on `main`
- [ ] Running the workflow produces an uploaded workflow artifact that contains the assembled versioned release bundle directory `release/<version>/...`
- [ ] The workflow run fails with a non-zero exit code if any required bundle artifact is missing (e.g., `VERSION`, `manifest.json`, `templates/`, default config file, `run_counter_risk.cmd`, README containing "How to run", built executable)

## Implementation Notes

The validation script should explicitly check for the following required files/directories and fail with a non-zero exit code if any are missing:
- `VERSION`
- `manifest.json`
- `templates/` directory
- Default config file (whatever the bundle currently uses)
- `run_counter_risk.cmd`
- README file containing the substring "How to run"
- Built executable (platform-specific name acceptable)

The draft workflow should run tests before building the executable, then run `pyinstaller -y release.spec`, then run the release assembly step to create `release/<version>/...`, then validate required contents using the validation script, then upload the assembled bundle as an artifact.

Since agents cannot modify `.github/workflows/` directly, this issue creates all supporting infrastructure and a complete draft workflow that a human can review and manually add to the protected directory.