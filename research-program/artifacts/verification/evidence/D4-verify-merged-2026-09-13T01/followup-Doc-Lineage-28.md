## Why (verified evidence)

`stranske/Doc-Lineage#28` merged the extraction library for `#3`, but the issue's test gate requires a production-code deliberate break that is not evidenced in the squash diff or PR body.

- `src/doc_lineage/extract/pdf.py` detects missing text layers per page and invokes OCR fallback (merge SHA `c3fa0461a15333a6f0f8d351fb53e2fa9491b883`).
- `tests/test_extract_coverage.py::test_mixed_pdf_recognizes_only_missing_text_layer_page` guards per-page behavior.
- Issue `#3` requires mutating text-layer detection to per-document, confirming the mixed-PDF test FAILS, reverting, and recording both outcomes in the PR.
- PR #28 documents the gate via `test_deliberate_break_per_document_detection_violates_mixed_pdf_contract`, which compares expected counts without mutating production code or pasting RED/GREEN output.

## Tasks

- [ ] In a follow-up PR linked to `#3`, temporarily change text-layer detection in `src/doc_lineage/extract/pdf.py` to treat the whole document as text-layer-present when any page has text.
- [ ] Run `pytest tests/test_extract_coverage.py::test_mixed_pdf_recognizes_only_missing_text_layer_page -q` and capture failing output.
- [ ] Revert and capture passing output; paste both blocks in the PR body.

## Acceptance Criteria

- Named test: `tests/test_extract_coverage.py::test_mixed_pdf_recognizes_only_missing_text_layer_page` passes on `main`.
- Deliberate-break → revert: per-document text-layer detection in `src/doc_lineage/extract/pdf.py` → confirm the named test FAILS → revert and confirm it passes. Paste RED and GREEN blocks in the PR.

## Non-Goals

- Do not remove OCR fallback, cache-keying, or office-format readers.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-13T01; verified by reading squash diff for PR #28 at merge SHA `c3fa0461`._
