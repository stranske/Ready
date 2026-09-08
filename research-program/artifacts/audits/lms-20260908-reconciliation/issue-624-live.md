## Why

The database JSONL export and import registry omits domain models introduced in milestones M5 and M6 (`src/lms/export_import.py:62-130`). Specifically, `MODEL_BY_TYPE`, `EXPORT_ORDER`, and `DEPENDENCIES` do not include `Hint`, `HintReveal`, `ModelAnswer`, `ModelAnswerReveal`, `RevisionRequest`, `FeedbackTemplate`, `WorkProduct`, and `LearnerReflection`. When running `lms export` or invoking `export_jsonl()`, records from these tables are silently skipped, producing incomplete backups and causing silent data loss upon re-import. This is a verified **latent fragility** and data integrity gap in the backup and restore pipeline.

## Scope

Register `Hint`, `HintReveal`, `ModelAnswer`, `ModelAnswerReveal`, `RevisionRequest`, `FeedbackTemplate` (from `src/lms/feedback/models.py`), `WorkProduct` (from `src/lms/cases/models.py`), and `LearnerReflection` (from `src/lms/learners/models.py`) in `MODEL_BY_TYPE`, `EXPORT_ORDER`, and `DEPENDENCIES` in `src/lms/export_import.py`. Add roundtrip export/import regression tests in `tests/export_import/test_export_contract.py`.

## Non-Goals

- Do NOT modify table schemas or column definitions in `src/lms/feedback/models.py`, `src/lms/cases/models.py`, or `src/lms/learners/models.py`.
- Do NOT change the export JSONL file format schema.
- Scaffold-only completion does NOT count: adding model names to `MODEL_BY_TYPE` without defining topological export order in `EXPORT_ORDER` and foreign key dependencies in `DEPENDENCIES` is a failure of this issue.

## Tasks

- [ ] In `src/lms/export_import.py`, import `FeedbackTemplate`, `Hint`, `HintReveal`, `ModelAnswer`, `ModelAnswerReveal`, and `RevisionRequest` from `src/lms/feedback/models.py`.
- [ ] In `src/lms/export_import.py`, import `WorkProduct` from `src/lms/cases/models.py` and `LearnerReflection` from `src/lms/learners/models.py`.
- [ ] In `src/lms/export_import.py`, register the imported models in `MODEL_BY_TYPE`, append them in valid foreign-key dependency order to `EXPORT_ORDER`, and define their parent relationships in `DEPENDENCIES`.
- [ ] In `tests/export_import/test_export_contract.py`, add test `test_export_contract_includes_m5_m6_domain_entities` asserting that hints, model answers, revision requests, reflections, and work products are exported with non-zero record counts and restore accurately.

## Acceptance Criteria

- [ ] The named test `pytest tests/export_import/test_export_contract.py -k "test_export_contract_includes_m5_m6_domain_entities"` passes with 0 failures, verifying full export serialization and dependency validation for M5 and M6 models.
- [ ] **Deliberate-break gate:** In `src/lms/export_import.py`, remove `"hint": Hint` from `MODEL_BY_TYPE`. Running `pytest tests/export_import/test_export_contract.py -k "test_export_contract_includes_m5_m6_domain_entities"` MUST fail with an assertion failure (missing entity type in export manifest). Revert the edit after capturing the failure.
- [ ] Existing export contract tests pass via `pytest tests/export_import/test_export_contract.py`.

## Implementation Notes

- Respect foreign key hierarchy: `FeedbackRecord` must export before `Hint`, `ModelAnswer`, and `RevisionRequest`. `Hint` must export before `HintReveal`. `ModelAnswer` must export before `ModelAnswerReveal`.
- Confirmed-green test runner: `pytest tests/export_import/test_export_contract.py`
