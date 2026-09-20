## Why

`src/doc_lineage/manifest.py:147-159` indexes and hashes every supported document with `compute_identity`, whose default read is unbounded at `src/doc_lineage/identity.py:66-75`. In contrast, `src/doc_lineage/ingest.py:176-177` rejects files above `MAX_INGEST_BYTES`, defined as 100 MiB in `src/doc_lineage/adapters/docling_segmenter.py:21`. This is a current pipeline break: a 100 MiB plus one byte PDF is emitted by `build_manifest_rows` but `ingest_document` rejects that same manifest candidate solely for size, leaving the catalog to advertise a document the mandatory ingest stage cannot process.

## Scope

Define and enforce one explicit size policy at the manifest-to-ingest boundary, with a deterministic operator-visible outcome for oversized documents.

## Non-Goals

- Do not raise the ingest limit or remove bounded reads solely to make the two paths agree.
- Do not silently hash arbitrarily large input as the implementation of a shared policy.
- Scaffold-only completion does NOT count: sharing a constant while `build_manifest_rows` still emits a row that `ingest_document` rejects only for the same size limit is a failure of this issue.

## Tasks

- [ ] Define the manifest-side handling for `MAX_INGEST_BYTES` in `src/doc_lineage/manifest.py:141` and use the canonical limit from `src/doc_lineage/adapters/docling_segmenter.py:21` rather than a duplicate literal.
- [ ] Ensure `src/doc_lineage/identity.py:66-75` is not asked to load an over-limit library document before the manifest policy is applied.
- [ ] Add a matched-boundary test in `tests/test_identity_manifest.py` using `MAX_INGEST_BYTES` that verifies the manifest outcome for an over-limit PDF agrees with the `src/doc_lineage/ingest.py:176-177` ingest outcome.

## Acceptance Criteria

- [ ] `pytest tests/test_identity_manifest.py tests/ingest/test_ingest_synthetic_pdf.py` passes, and the new boundary test proves an over-limit PDF cannot be emitted as an ordinary ingestable manifest row while `ingest_document` rejects it for the same named limit.
- [ ] Deliberate-break gate: temporarily bypass the manifest-side limit check in `src/doc_lineage/manifest.py`; the new boundary test must fail because the over-limit PDF reappears as a manifest row despite the named ingest rejection. Restore the policy before requesting review.

## Implementation Notes

- Verified current evidence at `src/doc_lineage/manifest.py:147`, `src/doc_lineage/identity.py:73`, `src/doc_lineage/ingest.py:176`, and `src/doc_lineage/adapters/docling_segmenter.py:21`.
- Current reproduction indexed a 104857601-byte PDF, then received `document exceeds ingest size limit (104857601 > 104857600 bytes)` from `ingest_document`.
