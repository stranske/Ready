## Why

When importing a knowledge graph from CSV, cycle detection raises an unhandled `ValueError` that crashes the CLI (`src/lms/importers/csv_graph.py:113-126`, `src/lms/__main__.py:526-527`). `import_csv_graph` calls `create_knowledge_edge`, which raises `ValueError("edge would create a prerequisite cycle")` upon cycle detection. However, `src/lms/__main__.py:526-527` catches only `CsvGraphImportError`. When a CSV contains circular prerequisite dependencies, the CLI terminates with an unhandled Python traceback instead of printing `CSV graph import failed:` and exiting cleanly with status code 1. Furthermore, `dry_run=True` fails to perform cycle detection checks. This is a verified **current break** in CLI error handling.

## Scope

Wrap graph edge creation in `src/lms/importers/csv_graph.py` to catch `ValueError` and re-raise as `CsvGraphImportError(f"Row {row_idx}: {exc}")`. Add in-memory cycle detection during `dry_run=True`. Add test coverage in `tests/importers/test_csv_graph_importer.py`.

## Non-Goals

- Do NOT modify the underlying graph repository methods in `src/lms/graphs/repository.py`.
- Do NOT change the CSV format or expected column headers.
- Scaffold-only completion does NOT count: catching `ValueError` without attaching row context or without verifying CLI exit code 1 handling is a failure of this issue.

## Tasks

- [ ] In `src/lms/importers/csv_graph.py`, wrap `create_knowledge_edge` calls in `import_csv_graph` in a try-except block catching `ValueError` and raising `CsvGraphImportError(f"Row {row_number}: {exc}") from exc`.
- [ ] In `src/lms/importers/csv_graph.py`, add cycle detection and self-loop validation to the `dry_run=True` validation pass.
- [ ] In `tests/importers/test_csv_graph_importer.py`, add test `test_import_csv_graph_cycle_raises_csv_graph_import_error` asserting that `CsvGraphImportError` is raised on circular input.

## Acceptance Criteria

- [ ] The named test `pytest tests/importers/test_csv_graph_importer.py -k "test_import_csv_graph_cycle_raises_csv_graph_import_error"` passes with 0 failures, asserting `CsvGraphImportError` is raised with row details when circular prerequisite chains exist.
- [ ] **Deliberate-break gate:** In `src/lms/importers/csv_graph.py:120`, remove the try-except wrapper around `create_knowledge_edge`. Running `pytest tests/importers/test_csv_graph_importer.py -k "test_import_csv_graph_cycle_raises_csv_graph_import_error"` MUST fail with `Failed: DID NOT RAISE <class 'lms.importers.csv_graph.CsvGraphImportError'>` (raising raw `ValueError` instead). Revert the edit after capturing the failure.
- [ ] Existing CSV graph importer tests pass via `pytest tests/importers/test_csv_graph_importer.py`.

## Implementation Notes

- `src/lms/__main__.py:526` catches `CsvGraphImportError` to format the message to `stderr` and exit with code 1.
- Confirmed-green test runner: `pytest tests/importers/test_csv_graph_importer.py`
