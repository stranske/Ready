## Why

R6 requires single golden catalog so home development does not re-download per repo (`B2-gap-analysis` B2-037). Verified: no `clones/public-doc-fixtures` directory exists in the research-program workspace (2026-09-04). Pension-Data replay gate (`artifacts/research/B2-gap-analysis.md:95` B2-043) needs corpus entries. **Missing behavior:** no fleet-wide `artifact-manifest/v1` catalog repo.

## Scope

New repo with `manifest.json` conforming to `artifact-manifest/v1`, entries pointing to Git LFS PDFs, validator script.

## Non-Goals

- Do NOT duplicate Pension-Data PPD/5500 downloaders (B2-R parallel reject).
- Do NOT commit proprietary PDFs.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Create repo with `manifest.json` schema_version `artifact-manifest/v1`.
- [ ] Register one public CalPERS IC PDF entry (owner default #9) with `source_url`, `content_sha256`, `doc_type_id`.
- [ ] Add `scripts/validate_manifest.py` using synced JSON Schema from Workflows.
- [ ] Add `tests/test_manifest_entries.py` asserting ≥1 entry and valid sha256 lengths.
- [ ] Document LFS setup in `README.md`.

## Acceptance Criteria

- [ ] Named test: `tests/test_manifest_entries.py::test_manifest_has_calpers_entry` passes.
- [ ] **Deliberate-break gate:** corrupt sha256 on entry → test **must FAIL** → revert.

_Surfaced by B2-037._
