## Why

_as_float accepts NaN and infinity, and malformed strings raise ValueError; direct execution confirms each behavior. Its consumers aggregate scores and compare weak-node thresholds at `src/lms/capability/repository.py`:221. This is latent fragility: no current HTTP input path producing such persisted values was established, and upstream mastery filtering mitigates some inputs. Evidence: `src/lms/capability/repository.py:761`.

## Scope

Repair the demonstrated boundary in `src/lms/capability/repository.py` and cover it in `tests/capability/test_repository.py`.

## Non-Goals

- Do not redesign unrelated subsystems or modify synced workflows.
- Scaffold-only completion does NOT count: editing signatures or adding a test that skips the demonstrated boundary is a failure of this issue.

## Tasks

- [ ] In `src/lms/capability/repository.py`, Handle malformed and non-finite values explicitly before aggregation. Preserve valid numeric conversions. Define a conservative invalid-value policy so missing or invalid evidence cannot imply a strong capability score; document any fallback. The existing helper has no default parameter.
- [ ] In `tests/capability/test_repository.py`, add `test_capability_float_rejects_nonfinite_and_malformed` with the demonstrated failing case and a valid-input control.

## Acceptance Criteria

- [ ] `pytest tests/capability/test_repository.py -k test_capability_float_rejects_nonfinite_and_malformed` passes and verifies the specified boundary and valid control.
- [ ] Deliberate-break gate in `src/lms/capability/repository.py`: Temporarily restore bare float conversion; the named test must fail for NaN, infinity, or malformed input; restore validation. Run `pytest tests/capability/test_repository.py -k test_capability_float_rejects_nonfinite_and_malformed` for this proof.
- [ ] Existing tests in `tests/capability/test_repository.py` pass.

## Implementation Notes

- Existing CI is green at the audited commit; the new regression is prospective and has not been implemented.
- Test runner: `pytest tests/capability/test_repository.py`.
