## Why (verified evidence)

`stranske/Doc-Lineage#32` merged the M1 ingest pipeline for `#8`, but the issue requires a deliberate-break demonstration on manifest `sha256` computation that is absent from the squash diff and PR body.

- `src/doc_lineage/ingest.py::ingest_document` writes artifact and source `sha256` hashes (merge SHA `c0e7d8b16076a32ebf314e86663bc55018a31b9c`).
- `tests/ingest/test_ingest_synthetic_pdf.py::test_ingest_writes_valid_manifest` asserts those hashes match on-disk bytes.
- Issue `#8` acceptance criteria require skipping manifest `sha256` computation in `ingest.py`, confirming the named test FAILS, then reverting with RED/GREEN output in the PR.
- PR #32 body checks the deliberate-break box but provides no mutation transcript; the diff contains only a comment referencing the gate.

## Tasks

- [ ] In a follow-up PR linked to `#8`, temporarily skip artifact `sha256` computation in `src/doc_lineage/ingest.py` (the path guarded by `test_ingest_writes_valid_manifest`).
- [ ] Run `pytest tests/ingest/test_ingest_synthetic_pdf.py::test_ingest_writes_valid_manifest -q` and capture failing output.
- [ ] Revert and capture passing output; paste both blocks in the PR body.

## Acceptance Criteria

- Named test: `tests/ingest/test_ingest_synthetic_pdf.py::test_ingest_writes_valid_manifest` passes on `main`.
- Deliberate-break → revert: skip manifest `sha256` computation in `src/doc_lineage/ingest.py` → confirm the named test FAILS → revert and confirm it passes. Paste RED and GREEN blocks in the PR.

## Non-Goals

- Do not rework ingest segmentation, Docling adapter wiring, or CLI flags.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-13T01; verified by reading squash diff for PR #32 at merge SHA `c0e7d8b1`._
