## Why

`src/doc_lineage/manifest.py:64-74` accepts every `Path.is_file()` result from the library traversal, and `src/doc_lineage/manifest.py:147-159` records the lexical in-library path before `src/doc_lineage/identity.py:73-75` reads that path's target bytes. This is a current containment break: an in-library PDF symlink pointing outside the library yields a manifest row with the in-library path and the outside file's SHA-256. A manifest therefore claims that unscanned external content belongs to the managed library.

## Scope

Keep manifest scanning confined to regular files physically contained by the resolved library root, and cover the rejected link behavior.

## Non-Goals

- Do not change the content-hash identity algorithm for regular in-library documents.
- Do not follow directory symlinks or add a second external-library traversal mode in this issue.
- Scaffold-only completion does NOT count: checking only the lexical `row.path` while still hashing an out-of-root symlink target is a failure of this issue.

## Tasks

- [ ] Update `src/doc_lineage/manifest.py:64-74` so `_iter_documents` rejects symlinked document entries and verifies a candidate's resolved path remains under the resolved library root before `build_manifest_rows` calls `compute_identity`.
- [ ] Add a containment regression case in `tests/test_identity_manifest.py` that creates an in-library PDF symlink to an out-of-root file and asserts `build_manifest_rows` neither returns its lexical path nor hashes its target.
- [ ] Preserve the existing regular-file and in-library-output rejection behavior in `tests/test_identity_manifest.py:322-536`.

## Acceptance Criteria

- [ ] `pytest tests/test_identity_manifest.py` passes, including the new out-of-root symlink test, while regular fixture PDFs continue to produce their current content identities.
- [ ] Deliberate-break gate: temporarily remove the symlink containment rejection from `src/doc_lineage/manifest.py`; the new symlink test must fail because the external file digest appears in a manifest row. Restore the rejection before requesting review.

## Implementation Notes

- Verified current evidence at `src/doc_lineage/manifest.py:64-74`, `src/doc_lineage/manifest.py:147-159`, and `src/doc_lineage/identity.py:73-75`.
- Current reproduction created a symlink under a temporary library root: `build_manifest_rows` returned a lexical in-library row with the SHA-256 of the external target.
