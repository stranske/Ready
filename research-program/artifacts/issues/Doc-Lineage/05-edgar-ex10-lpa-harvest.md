## Why

Public legal lineage without proprietary LPAs (R6). Verified: `clones/Doc-Lineage/pyproject.toml:1-20` lists no `edgartools` dependency; `clones/Doc-Lineage/src/my_project/__init__.py:1-5` confirms no harvest package. **Missing behavior:** no SEC EX-10 ingest path. **Depends on:** edgartools adopt, B2-037 manifest for registration.

## Scope

CLI `doc-lineage harvest-edgar --cik ...` downloading EX-10 exhibits to mirror-compatible paths.

## Non-Goals

- Do NOT store proprietary manager PDFs.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/doc_lineage/harvest/edgar_ex10.py` using `edgartools` with rate limiting.
- [ ] Add `tests/harvest/test_edgar_ex10_offline.py` with recorded fixture (no live SEC in CI).
- [ ] Register harvested docs in output compatible with `document-mirror/v1` (after Workflows B2-023).

## Acceptance Criteria

- [ ] Named test: `tests/harvest/test_edgar_ex10_offline.py::test_parse_ex10_fixture` passes.
- [ ] **Deliberate-break gate:** return empty exhibit list → test **must FAIL** → revert.

_Surfaced by B2-007._
