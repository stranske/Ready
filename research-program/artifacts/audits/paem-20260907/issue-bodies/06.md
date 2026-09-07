## Why

`pa_core/cli.py:1414` and `pa_core/cli.py:2100` create the portable bundle before run-end finalization at `pa_core/cli.py:944`. A real successful 100-path one-point CLI sweep with JSON logging and an index-frequency warning yields two warnings and a cost record in the final manifest, but null warnings and cost in the bundled manifest; timing also differs. This survives the repository lock versions Plotly 6.9.0 and Kaleido 1.3.0. Closed #1834 covered the run envelope; the portable copy remains stale.

## Scope

Finalize manifest provenance before creating run bundles. First-party data behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] Reorder or refactor manifest finalization and bundle creation in `pa_core/cli.py` so finalized warnings, cost and timing reach the bundled manifest on every successful completion branch.
- [ ] Extend `tests/test_run_artifact_bundle.py` with a real CLI run that emits a warning and compares the final standalone and bundled manifest fields; retain bundle hash verification.

## Acceptance Criteria

- [ ] Bundled and standalone manifests agree on captured warnings, cost and finalized timing after successful CLI completion; bundle.verify returns true.
- [ ] Run `pytest tests/test_run_artifact_bundle.py tests/test_run_record_warnings.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Restore bundle creation before finalization; the new manifest-parity regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
