## Why

Current data loss: `schema.sql:395` stores a single manager owner while `schema.sql:404` makes text hash globally unique. On a hash conflict, `embeddings.py:185` and `embeddings.py:243` return the first document without preserving the second manager association. Storage of identical memo text for managers 1 and 2 returned document IDs 1 and 1; manager-2-filtered retrieval returned zero documents. `embeddings.py:274` filters on the single owner.

## Scope

Preserve each explicitly supplied manager association while retaining stable document identity and content deduplication.

## Non-Goals

Do not infer associations from similar text or weaken access controls. Scaffold-only completion does NOT count: creating a junction table without wiring storage and both search paths is a failure of this issue.

## Tasks

- [ ] Add an additive document-to-manager association table with backfill of existing non-null owners through a new migration under `alembic/versions/`, and mirror the contract in `schema.sql`.
- [ ] Update `embeddings.py` storage to persist each supplied manager association, including repeated content first stored without a manager, on both SQLite and Postgres.
- [ ] Update manager-filtered retrieval in `embeddings.py` and document search in `api/search.py` to use the association model without duplicate result rows.
- [ ] Add regression cases in `tests/test_embeddings.py` for two managers sharing content, unlinked-then-linked content, repeated identical association, and retention of stable document IDs.

## Acceptance Criteria

- [ ] pytest tests/test_embeddings.py must pass; the new shared-document test must retrieve the same content for each explicitly associated manager, return no unrelated manager match, and avoid duplicate results. Verify the migration and retrieval against SQLite and a disposable Postgres database.
- [ ] Deliberate-break gate: Disable association insertion on a hash conflict in `embeddings.py`; the new shared-document test in `tests/test_embeddings.py` must fail for manager 2; revert and rerun.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Preserving explicit associations is distinct from closed issue 1628, which passed metadata into ingestion. Backfill conservatively from existing ownership; do not invent missing historical associations. Keep the original scalar field compatible until callers are migrated.
