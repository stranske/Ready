## Why (verified evidence)

Post-merge verification (D4-verify-merged-2026-09-16T02) of stranske/Ready#570 (merge `4d90bfb83c077dd8dbbdab80202b57f47c5391ca`) against #557 found core Black exclusion behavior landed, but one adversarial acceptance item remains open.

- `pyproject.toml` sets both `extend-exclude` and `force-exclude` for `research-program/artifacts` (merge diff lines 9–14).
- `tests/test_repo_hygiene.py` tests recursive `black --check .` with `extend-exclude` stripped (force-exclude cleared to isolate).
- Issue #557 follow-up requires a deliberate-break where **`force-exclude` alone** is removed while CI-style explicit-path invocation still passes artifacts — no test currently removes `force-exclude` and asserts explicit-path `black --check research-program/artifacts/...` fails.

## Tasks

- [ ] In `tests/test_repo_hygiene.py`, add a test that runs Black with an explicit artifact path (matching CI) after removing only `force-exclude` from `pyproject.toml` → expect non-zero exit referencing the probe artifact.
- [ ] Retain `extend-exclude` in that test to prove `force-exclude` is independently required for explicit-path CI invocations.

## Acceptance Criteria

- Named test: `test_black_force_exclude_required_for_explicit_paths` (or equivalent) in `tests/test_repo_hygiene.py` asserting explicit-path Black fails when only `force-exclude` is removed.
- Deliberate-break → revert: remove `force-exclude` from config under test → named test FAILS → restore `force-exclude` → passes.

## Non-Goals

- Do NOT weaken the existing recursive `extend-exclude` regression from #570.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-16T02; verified against squash diff `Ready-570.diff` and issue #557. Related: #557, merged PR #570._
