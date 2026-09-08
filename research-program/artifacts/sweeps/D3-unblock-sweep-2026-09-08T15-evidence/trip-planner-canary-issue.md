# [P1] Make browser canary startup use a prepared Python environment

Staged issue body only; not filed. Recheck duplicates before filing.

## Why

At main 70db2be47f7a145480b99639f8d18adc744325fd, CI https://github.com/stranske/trip-planner/actions/runs/34197427655 fails Browser first-use canary after approximately 15 seconds. The backend log only reports CPython 3.14.7 and creating .venv; the frontend log is empty. This is a startup failure before browser assertions, not evidence of a signup product defect.

## Scope

scripts/run_two_trip_ui_canary.sh and .github/workflows/ci.yml browser-canary dependency setup.

## Tasks

- [ ] Reproduce ./scripts/run_two_trip_ui_canary.sh in the CI Python 3.14 and Node 22 environment after the current workflow dependency step, retaining backend startup and dependency-resolution logs.
- [ ] Align .github/workflows/ci.yml installation with scripts/run_two_trip_ui_canary.sh execution: the workflow uses python -m pip install -e ".[dev]", while the script invokes uv run --extra dev, which creates a separate .venv on a clean runner. Prepare the environment used by the runtime before starting readiness polling.
- [ ] Improve wait_for_url in scripts/run_two_trip_ui_canary.sh so a failed backend process reports its exit and logs; retain a bounded readiness deadline with meaningful diagnostics.

## Acceptance Criteria

- [ ] `bash scripts/run_two_trip_ui_canary.sh` exits 0 and prints Two-trip UI canary PASS on a fresh runner using CI dependency installation.
- [ ] The script invokes the frontend `npm run test:e2e:canary` suite and the Browser first-use canary CI job passes without skipping signup or workspace assertions.
- [ ] A deliberately failing backend command yields a bounded, diagnostic nonzero result rather than an unexplained wait timeout.

## Implementation Notes

The script polls 60 times with sleep 0.25, giving approximately 15 seconds plus curl time. The measured CI interval and absence of frontend output agree with backend-readiness exhaustion. Separate pip/uv environments are verified statically; dependency resolution as the precise blocking cause remains an inference pending clean-run reproduction. Do not merely increase the timeout or alter product code without that evidence.

## Non-Goals

Changing trip ranking, signup behavior, remote hosting, shared workflow templates, or weakening the browser assertions.
