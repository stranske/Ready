## Why

A two-node cyclic CSV passes dry_run, then real import raises raw ValueError instead of CsvGraphImportError. The CLI catches only CsvGraphImportError at `src/lms/__main__.py`:526. This is a current dry-run and error-contract break. Evidence: `src/lms/importers/csv_graph.py:56`.

## Scope

Repair the demonstrated boundary in `src/lms/importers/csv_graph.py` and cover it in `tests/importers/test_csv_graph_importer.py`.

## Non-Goals

- Do not redesign unrelated subsystems or modify synced workflows.
- Scaffold-only completion does NOT count: editing signatures or adding a test that skips the demonstrated boundary is a failure of this issue.

## Tasks

- [ ] In `src/lms/importers/csv_graph.py`, Validate cyclic prerequisite graphs during dry_run before writes, and translate graph creation ValueError into CsvGraphImportError with row context in the actual import path. Preserve caller rollback.
- [ ] In `tests/importers/test_csv_graph_importer.py`, add `test_csv_cycles_raise_domain_error` with the demonstrated failing case and a valid-input control.

## Acceptance Criteria

- [ ] `pytest tests/importers/test_csv_graph_importer.py -k test_csv_cycles_raise_domain_error` passes and verifies the specified boundary and valid control.
- [ ] Deliberate-break gate in `src/lms/importers/csv_graph.py`: Temporarily remove cycle validation and the domain-error translation; the named test must fail because dry_run accepts the cycle or real import raises raw ValueError; restore both protections. Run `pytest tests/importers/test_csv_graph_importer.py -k test_csv_cycles_raise_domain_error` for this proof.
- [ ] Existing tests in `tests/importers/test_csv_graph_importer.py` pass.

## Implementation Notes

- Existing CI is green at the audited commit; the new regression is prospective and has not been implemented.
- Test runner: `pytest tests/importers/test_csv_graph_importer.py`.
