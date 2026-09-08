## Why

MODEL_BY_TYPE and EXPORT_ORDER omit Hint, HintReveal, ModelAnswer, ModelAnswerReveal, RevisionRequest, FeedbackTemplate, WorkProduct, and LearnerReflection. Runtime registry inspection confirms all eight omissions. This is a current export coverage break for existing records, not evidence from a completed populated backup/restore experiment. Evidence: `src/lms/export_import.py:62`.

## Scope

Repair the demonstrated boundary in `src/lms/export_import.py` and cover it in `tests/export_import/test_export_contract.py`.

## Non-Goals

- Do not redesign unrelated subsystems or modify synced workflows.
- Scaffold-only completion does NOT count: editing signatures or adding a test that skips the demonstrated boundary is a failure of this issue.

## Tasks

- [ ] In `src/lms/export_import.py`, Register all eight existing models using their case-sensitive class names, actual foreign-key relationships, and a valid dependency order. Read actual model declarations in `src/lms/feedback/models.py`, `src/lms/cases/models.py`, and `src/lms/learners/models.py`; do not assume hints depend on FeedbackRecord.
- [ ] In `tests/export_import/test_export_contract.py`, add `test_m5_m6_models_survive_export_restore` with the demonstrated failing case and a valid-input control.

## Acceptance Criteria

- [ ] `pytest tests/export_import/test_export_contract.py -k test_m5_m6_models_survive_export_restore` passes and verifies the specified boundary and valid control.
- [ ] Deliberate-break gate in `src/lms/export_import.py`: Temporarily remove Hint from EXPORT_ORDER; the named populated roundtrip test must fail on the missing hint; restore the entry. Run `pytest tests/export_import/test_export_contract.py -k test_m5_m6_models_survive_export_restore` for this proof.
- [ ] Existing tests in `tests/export_import/test_export_contract.py` pass.

## Implementation Notes

- Existing CI is green at the audited commit; the new regression is prospective and has not been implemented.
- Test runner: `pytest tests/export_import/test_export_contract.py`.
