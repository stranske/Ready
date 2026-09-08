## Why

Capability detail and existing-target action routes omit resource ownership enforcement. A synthetic authenticated foreign user received HTTP 200 with the private target title and successfully recomputed its estimate. This is a current break. Target creation already resolves learner identity. Evidence: `src/lms/ui/capability_gap.py:96`.

## Scope

Repair the demonstrated boundary in `src/lms/ui/capability_gap.py` and cover it in `tests/ui/test_capability_gap_surface.py`.

## Non-Goals

- Do not redesign unrelated subsystems or modify synced workflows.
- Scaffold-only completion does NOT count: editing signatures or adding a test that skips the demonstrated boundary is a failure of this issue.

## Tasks

- [ ] In `src/lms/ui/capability_gap.py`, Resolve the owning target for detail, recomputation, gap analysis, and maintenance planning; verify its learner with require_learner_ownership from `src/lms/learners/identity.py` before reads or writes. Import SettingsDep from `src/lms/auth/login.py`.
- [ ] In `tests/ui/test_capability_gap_surface.py`, add `test_foreign_capability_target_is_rejected` with the demonstrated failing case and a valid-input control.

## Acceptance Criteria

- [ ] `pytest tests/ui/test_capability_gap_surface.py -k test_foreign_capability_target_is_rejected` passes and verifies the specified boundary and valid control.
- [ ] Deliberate-break gate in `src/lms/ui/capability_gap.py`: Temporarily remove the target detail ownership check; the named test must fail on foreign HTTP 200; restore the check. Run `pytest tests/ui/test_capability_gap_surface.py -k test_foreign_capability_target_is_rejected` for this proof.
- [ ] Existing tests in `tests/ui/test_capability_gap_surface.py` pass.

## Implementation Notes

- Existing CI is green at the audited commit; the new regression is prospective and has not been implemented.
- Test runner: `pytest tests/ui/test_capability_gap_surface.py`.
