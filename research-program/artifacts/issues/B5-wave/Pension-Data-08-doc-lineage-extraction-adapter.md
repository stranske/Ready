## Why

The work-environment appendix calls for **one shared PDF extraction library** instead of three overlapping implementations ([INFORMATION-REQUEST-RESPONSE.md Appendix §What looks worth systematizing, item 2](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). Pension-Data maintains its own multi-stage fallback chain in `src/pension_data/parser/pdf_pipeline.py:492-519` (`table_primary` → `text_fallback` → `full_fallback` OCR) atop `pypdf` and `stranske_pdf_extract.orchestration` (`pdf_pipeline.py:10-12`). That is a fourth extraction surface alongside Inv-Man-Intake and the two work-side tools Doc-Lineage #3 replaces. **Missing behavior:** no adapter to consume Doc-Lineage #3 once it lands. **Latent fragility** — OCR fallback behavior will diverge across repos ([response §C Q8](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) scanned-image legal PDFs require mandatory OCR).

## Scope

Route the one-PDF pilot and parser entry points through the Doc-Lineage extraction library ([Doc-Lineage #3](https://github.com/stranske/Doc-Lineage/issues/3)) instead of the bespoke `pdf_pipeline.py` fallback chain, preserving `PDFParserResult` shape for downstream actuarial extraction.

## Non-Goals

- Do NOT change actuarial metric extraction logic in `src/pension_data/extract/actuarial/metrics.py`.
- Do NOT remove `stranske-pdf-extract` from the fleet — Doc-Lineage #3 should wrap or re-export it, not duplicate it.
- Do NOT implement consultant-report diffing (Doc-Lineage comparison engine).
- Scaffold-only completion does NOT count: adding an unused adapter while `parse_pdf_to_funded_input()` still calls the old chain is a failure.

## Tasks

- [ ] Add `src/pension_data/parser/doc_lineage_backend.py` adapting Doc-Lineage #3 extraction output into `PDFParserInput`/`PDFParserResult` shapes used by `parse_pdf_to_funded_input()` at `pdf_pipeline.py:492`.
- [ ] Add optional dependency `doc-lineage` in `pyproject.toml` referencing the Doc-Lineage package once #3 publishes `doc_lineage.extract`.
- [ ] Update `parse_pdf_to_funded_input()` to call `doc_lineage_backend.extract()` when the extra is installed; retain the existing chain as a documented fallback until #3 is stable, then remove in a follow-up.
- [ ] Update `src/pension_data/ops/one_pdf_pilot.py:282-335` to pass through the Doc-Lineage backend flag.
- [ ] Add `tests/parser/test_doc_lineage_backend.py` with `tests/parser/fixtures/calpers_fy2024_excerpt.pdf` asserting page-attributed text and OCR escalation on a scanned-image fixture.
- [ ] Extend `tests/golden/test_one_pdf_pilot_golden.py` to cover the doc-lineage backend path when installed.
- [ ] Perform deliberate-break verification (see Acceptance Criteria), capture FAIL output, then revert.

## Acceptance Criteria

- [ ] Named test: `tests/parser/test_doc_lineage_backend.py::test_scanned_fixture_triggers_ocr_path` passes — scanned-image PDF fixture must not return empty text without an OCR escalation event.
- [ ] Named test: `tests/parser/test_doc_lineage_backend.py::test_text_pdf_emits_page_pointers` passes on `calpers_fy2024_excerpt.pdf`.
- [ ] **Deliberate-break gate:** temporarily edit `doc_lineage_backend.py` to force `enable_ocr=False` for all inputs. `tests/parser/test_doc_lineage_backend.py::test_scanned_fixture_triggers_ocr_path` **must FAIL**. Revert after capturing the failure.

## Implementation Notes

- Depends on [Doc-Lineage #3](https://github.com/stranske/Doc-Lineage/issues/3) for the shared extraction API.
- OCR requirement grounded in [response §C Q8 and §Scope item 6](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) (20+ scanned legal documents silently skipped before recognition pass).
- Confirmed-green local reproduction: `python -m pytest tests/parser/test_pdf_pipeline.py -q` → passes today on `main`.
