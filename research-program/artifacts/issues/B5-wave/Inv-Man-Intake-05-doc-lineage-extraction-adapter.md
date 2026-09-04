## Why

The work-environment appendix names **one shared "extract structured facts from a PDF, with page pointers" library** instead of three independently built implementations, and states consolidating would cut three maintenance surfaces to one ([INFORMATION-REQUEST-RESPONSE.md Appendix §What looks worth systematizing, item 2](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). Inv-Man-Intake still routes PDFs through its own `PdfPrimaryExtractionProvider` for the default pyodide-light path — regex over content streams, explicitly *not production OCR* (`src/inv_man_intake/extraction/providers/pdf_primary.py:20-26`) — and only optionally through `stranske_pdf_extract` Docling (`src/inv_man_intake/extraction/service.py:104-115`, `118-128`). **Missing behavior:** no adapter to the Doc-Lineage extraction library once [Doc-Lineage #3](https://github.com/stranske/Doc-Lineage/issues/3) lands. **Latent fragility** — a fourth PDF extraction surface if left unchanged.

## Scope

Replace the in-repo PDF primary provider path with a thin adapter to the Doc-Lineage extraction library (page pointers + mandatory OCR fallback per Doc-Lineage #3), keeping the existing `ExtractionService` port at `src/inv_man_intake/extraction/service.py:27-35`.

## Non-Goals

- Do NOT block on Doc-Lineage #3 merging — land the adapter behind a feature flag or optional extra until #3 publishes a stable import path; remove `pdf-primary` once #3 is wired.
- Do NOT remove PPTX extraction (`pptx_primary.py`) in this issue.
- Do NOT implement the comparison/lineage engine (Doc-Lineage).
- Scaffold-only completion does NOT count: leaving `build_pyodide_light_service()` on `PdfPrimaryExtractionProvider` as the default while adding an unused adapter module is a failure.

## Tasks

- [ ] Add `src/inv_man_intake/extraction/providers/doc_lineage_adapter.py` wrapping the Doc-Lineage extraction entry point from #3, mapping results to `ExtractedDocumentResult` at `src/inv_man_intake/extraction/providers/base.py:8-13`.
- [ ] Add optional dependency group `extraction-doc-lineage` in `pyproject.toml` pointing at the Doc-Lineage package once #3 exposes `doc_lineage.extract`.
- [ ] Update `build_pyodide_light_service()` at `src/inv_man_intake/extraction/service.py:104-115` to select `DocLineageExtractionProvider` when the extra is installed, falling back to `PdfPrimaryExtractionProvider` only when the extra is absent (document the fallback as temporary).
- [ ] Add `tests/extraction/providers/test_doc_lineage_adapter.py` using a synthetic PDF fixture with expected page pointers.
- [ ] Update `tests/extraction/test_extraction_service.py` to assert the doc-lineage backend is selected when the extra is present.
- [ ] Perform deliberate-break verification (see Acceptance Criteria), capture FAIL output, then revert.

## Acceptance Criteria

- [ ] Named test: `tests/extraction/providers/test_doc_lineage_adapter.py::test_adapter_emits_page_pointers` passes — extracted fields include `SourceLocation.page` values from the Doc-Lineage library, not regex-only guesses.
- [ ] Named test: `tests/extraction/test_extraction_service.py::test_pyodide_light_prefers_doc_lineage_when_installed` passes when the `extraction-doc-lineage` extra is installed.
- [ ] **Deliberate-break gate:** temporarily edit `doc_lineage_adapter.py` to return `page=None` for all fields. `tests/extraction/providers/test_doc_lineage_adapter.py::test_adapter_emits_page_pointers` **must FAIL**. Revert after capturing the failure.

## Implementation Notes

- Reference [Doc-Lineage #3](https://github.com/stranske/Doc-Lineage/issues/3) for the shared extraction contract (page pointers + OCR fallback).
- Existing Docling path via `stranske_pdf_extract` (`service.py:118-128`) should delegate to the same Doc-Lineage library after #3 to avoid two OCR implementations.
- Confirmed-green local reproduction: `python -m pytest tests/extraction/test_pdf_primary_provider.py -q` → passes today on `main`.
