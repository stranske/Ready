## Why

R4 document-access substrate requires a cross-system mirror manifest (`artifacts/research/B2-gap-analysis.md` B2-023). Pension-Data implements checksum supersession internally (`clones/Pension-Data/src/pension_data/ingest/artifacts.py:52-56` `ingest_raw_artifacts`) but no fleet `document-mirror/v1` schema exists. Verified: `clones/Workflows/docs/contracts/schemas/` has no `document-mirror-v1.schema.json`. **Missing behavior:** doc-mirror CLI and HTML triple-link resolver cannot validate catalogs.

## Scope

Add `document-mirror/v1` JSON Schema, spec, golden fixture, validator flag, sync-manifest entries.

## Non-Goals

- Do NOT implement `doc-mirror` CLI (separate repo issue B2-024).
- Do NOT wire Graph/SharePoint delta sync (B2-026 — IT blocked).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Create `docs/contracts/schemas/document-mirror-v1.schema.json` with `mirror_root`, `blobs[]` entries (`content_sha256`, `blob_path`, `doc_type_id`, `source_refs[]`) per B3 §2.3 / R4 brief.
- [ ] Create `docs/contracts/document-mirror-v1.md`.
- [ ] Add `tests/fixtures/backplane/valid_document_mirror.json`.
- [ ] Extend `scripts/validate_run_contract.py` with `--mirror-manifest` flag.
- [ ] Add `test_document_mirror_fixture_validates` in `tests/contracts/test_backplane_schemas.py`.
- [ ] Append `.github/sync-manifest.yml` entries.

## Acceptance Criteria

- [ ] Named test: `tests/contracts/test_backplane_schemas.py::test_document_mirror_fixture_validates` passes.
- [ ] **Deliberate-break gate:** change a blob `content_sha256` to 63 hex chars in the fixture → test **must FAIL** → revert.
- [ ] `python scripts/validate_run_contract.py --mirror-manifest tests/fixtures/backplane/valid_document_mirror.json` exits 0.

## Implementation Notes

Reference Pension-Data supersession pattern at `clones/Pension-Data/src/pension_data/ingest/artifacts.py:32-35` for `artifact:` ID shape only — do not import Pension-Data code.

_Surfaced by B2-023 / R4; verified absent from Workflows schemas dir._
