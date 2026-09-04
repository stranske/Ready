## Why

Doc-Lineage is scaffold-only (`README.md:5-6`). Fleet needs ingest→extract→diff→HTML but M1 is ingest+segment only. Verified: `src/my_project/__init__.py:1-5` exports template helpers only; no `ingest` module under `src/`. **Depends on:** B2-001 vocabulary, adopt Docling (B2-012) as segmenter.

## Scope

M1 CLI `doc-lineage ingest <path>` producing `artifact-manifest/v1` + parsed JSON segments via Docling adapter stub with synthetic fixture.

## Non-Goals

- Do NOT ship blackline/diff (B2-005).
- Do NOT emit `tracked-variable/v1` until Workflows B2-003 lands.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Rename package from `my_project` to `doc_lineage` in `pyproject.toml` and `src/`.
- [ ] Add `src/doc_lineage/ingest.py` with `ingest_document(path: Path) -> IngestResult` writing manifest per synced `artifact-manifest-v1.schema.json`.
- [ ] Add `src/doc_lineage/adapters/docling_segmenter.py` wrapping Docling with offline fixture fallback for CI.
- [ ] Add CLI entry `doc-lineage` in `pyproject.toml` `[project.scripts]`.
- [ ] Add `tests/ingest/test_ingest_synthetic_pdf.py` using committed synthetic PDF under `tests/fixtures/`.
- [ ] Replace `tests/test_main.py` template tests with package import smoke.

## Acceptance Criteria

- [ ] Named test: `tests/ingest/test_ingest_synthetic_pdf.py::test_ingest_writes_valid_manifest` passes.
- [ ] **Deliberate-break gate:** skip manifest `sha256` computation in `ingest.py` → test **must FAIL** → revert.
- [ ] `doc-lineage ingest tests/fixtures/synthetic_lpa.pdf --output /tmp/out` exits 0 locally.

## Implementation Notes

Depends on Workflows `tracked-variable/v1` for M2; M1 uses manifest only.

_Surfaced by B2-002._
