## Why (verified evidence)

Post-merge verification (D4-verify-merged-2026-09-16T02) of stranske/Manager-Database#1678 (merge `25e497f834e10333b7f7f830bbe8c57c3ea7b974`) against #1669 found junction-table logic and SQLite tests landed, but Postgres acceptance is opt-in only.

- Migration `022_document_managers.py`, `embeddings.py` association inserts, and SQLite tests are present in squash diff.
- `tests/test_embeddings.py` Postgres leg uses `pytest.skip` unless `DOCUMENT_TEST_POSTGRES_URL` is set — issue #1669 acceptance requires disposable Postgres verification in CI, not skip-by-default.

## Tasks

- [ ] Add CI Postgres service (or documented disposable URL) so `test_document_association_migration_and_search` runs the Postgres leg in Gate without manual env.
- [ ] Ensure shared-document and search-dedup regressions execute on both SQLite and Postgres in CI.

## Acceptance Criteria

- Named test: `pytest tests/test_embeddings.py -k document_association` passes on Gate with Postgres available (no skip of postgres leg).
- Deliberate-break → revert: disable `document_managers` insert in `embeddings.py` → shared-document test FAILS on Postgres → restore → passes.

## Non-Goals

- Do NOT remove SQLite coverage from #1678.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-16T02; verified against squash diff `Manager-Database-1678.diff` and issue #1669. Related: #1669, merged PR #1678._
