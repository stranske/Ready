## Why

R6 requires a single golden catalog so home development does not re-download per repo (B2-037; grounding: [INFORMATION-REQUEST-RESPONSE.md](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). Verified: no dedicated fixtures corpus exists in this repo — extraction and lineage tests need synthetic and public PDFs with recorded provenance. Pension-Data replay gate (B2-043) needs corpus entries wired here rather than a separate `public-doc-fixtures` repo. **Missing behavior:** no fleet-wide fixture manifest checked into Doc-Lineage.

## Scope

Add `tests/fixtures/public_corpus/manifest.json` conforming to the synced `artifact-manifest/v1` record shape (contract name, not a file), entries for synthetic LPA fixtures plus one public CalPERS IC PDF (owner default #9) with `source_url`, `content_sha256`, `doc_type_id`, and a validator script.

## Non-Goals

- Do NOT create a separate GitHub repo for fixtures — this repo owns extraction and lineage tests.
- Do NOT duplicate Pension-Data PPD/5500 downloaders (B2-R parallel reject).
- Do NOT commit proprietary PDFs.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `tests/fixtures/public_corpus/manifest.json` with `schema_version` `artifact-manifest/v1`.
- [ ] Register one public CalPERS IC PDF entry with `source_url`, `content_sha256`, `doc_type_id`.
- [ ] Add `scripts/validate_fixture_manifest.py` using synced JSON Schema from Workflows.
- [ ] Add `tests/fixtures/test_public_corpus_manifest.py` asserting ≥1 entry and valid sha256 lengths.
- [ ] Document LFS setup for large PDFs in `tests/fixtures/public_corpus/README.md`.

## Acceptance Criteria

- [ ] Named test: `tests/fixtures/test_public_corpus_manifest.py::test_manifest_has_calpers_entry` passes.
- [ ] **Deliberate-break gate:** corrupt sha256 on entry → test **must FAIL** → revert.

## Implementation Notes

Retargeted from B4 public-doc-fixtures slice per B6 disposition: fixtures live with extraction/lineage tests in Doc-Lineage, not a greenfield repo.

_Surfaced by B2-037; verified absent from Doc-Lineage checkout 2026-09-04._
