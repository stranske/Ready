## Why

Current break on tip 54e4f406: `DELETE /managers/{id}` returns 204 while related filings and documents remain, so the advertised one-click GDPR erasure path in `Manager-Intel-Platform.md:104` does not remove manager intelligence data. `api/managers.py:488-495` deletes only the `managers` row; `schema.sql:29-31` defines `filings.manager_id` with a foreign key and no `ON DELETE CASCADE`, and `documents` rows are likewise left behind (verified live: after DELETE, `filings=1` and `documents=1` remain).

## Scope

Manager deletion semantics across SQLite and Postgres: cascade or explicitly purge filings, holdings, documents, embeddings, and object-storage keys tied to the manager before returning success.

## Non-Goals

Do not remove the DELETE route or change list/create manager validation. Scaffold-only completion does NOT count: returning 204 while any manager-linked filing, document, or blob remains is a failure of this issue.

## Tasks

- [ ] Replace the single-row delete in `api/managers.py:488-495` with an ordered cascade that removes dependent filings, holdings, documents, embeddings, and MinIO blobs referenced by those rows before deleting the manager record.
- [ ] Map every foreign-key child of `managers` in `schema.sql` and ensure each is covered by the cascade or an explicit purge step with dialect-portable SQL via `adapters/base.py`.
- [ ] Add `tests/test_manager_api.py` coverage that seeds a manager plus filing and document rows, calls DELETE, and asserts zero remaining rows in each dependent table.

## Acceptance Criteria

- Named test: `tests/test_manager_api.py::test_delete_manager_cascades_related_records` must pass and assert zero filings and documents remain after a successful DELETE.
- Deliberate-break → revert: restore the single-row delete in `api/managers.py:488-495` so dependent rows survive; the named test must fail; revert and rerun pytest.

## Implementation Notes

Reproduction on audited tip: create manager id 1 with one filing and one document; `DELETE /managers/1` → 204; SQLite still contains the filing and document rows. On Postgres with enforced FKs the same call fails instead of erasing data—both outcomes violate the product contract.
