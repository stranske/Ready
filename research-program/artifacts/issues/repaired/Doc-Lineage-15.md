## Why

Counsel sign-off requires Word redlines (B2 owner decision #12). Verified: `pyproject.toml:1-20` has no `python-redlines` dependency; `src/doc_lineage/__init__.py:1-5` has no export module. **Missing behavior:** no DOCX tracked-changes export. **Depends on:** python-redlines adopt (B2-011), B2-002 pipeline.

## Scope

`doc-lineage export-docx --blackline <id>` using python-redlines.

## Non-Goals

- Do NOT install Word automation on work PC — ship `.docx` only.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/doc_lineage/export/docx_redline.py` wrapping python-redlines.
- [ ] Add `tests/export/test_docx_redline_golden.py` with synthetic DOCX pair.

## Acceptance Criteria

- [ ] Named test: `tests/export/test_docx_redline_golden.py::test_tracked_changes_present` passes.
- [ ] **Deliberate-break gate:** disable redline markup → test **must FAIL** → revert.

_Surfaced by B2-034._
