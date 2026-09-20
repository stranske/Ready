## Why (verified evidence)

`stranske/Manager-Mosaic#25` merged the core model for `#3`, but the issue's acceptance criteria require a deliberate-break demonstration on production `derive_gaps()` — not a test-local anti-pattern helper.

- `tests/test_model_validation.py::test_silence_invariant_deliberate_break_then_revert` asserts `_forbidden_infer_exit_on_gap()` (defined in the test file) returns `"EXITED"` while `derive_gaps()` leaves status unchanged.
- The issue gate at `#3` requires: deliberately make `derive_gaps` set an entry status to exited on absence, confirm the silence invariant test fails, then revert.
- Merge commit `bfa4b552667438a5f950bf073b4539cfb16d9d14` never documents RED/GREEN output from mutating `src/manager_mosaic/model.py::derive_gaps`.

## Tasks

- [ ] In a follow-up PR linked to `#3`, temporarily mutate `src/manager_mosaic/model.py::derive_gaps` so an uncovered period sets `entry.status` to an exited value.
- [ ] Run `pytest tests/test_model_validation.py::test_derive_gaps_leaves_status_unchanged -q` and capture the failing output.
- [ ] Revert the mutation and capture passing output; paste both blocks in the PR body.

## Acceptance Criteria

- Named test: `tests/test_model_validation.py::test_derive_gaps_leaves_status_unchanged` passes on `main`.
- Deliberate-break → revert: make `derive_gaps` mutate `entry.status` on absence → confirm `test_derive_gaps_leaves_status_unchanged` FAILS → revert and confirm it passes. Paste RED and GREEN blocks in the PR.

## Non-Goals

- Do not change `derive_gaps` production semantics beyond the temporary break/revert demonstration.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-17T02; verified by reading squash diff for PR #25 at merge SHA `bfa4b552`._
