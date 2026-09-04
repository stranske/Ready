## Why

Expand replay corpus after CalPERS harvester (B2-038). Verified: `tools/replay/runner.py:130-172` replays golden corpus but manifest entries from `public-doc-fixtures` are not referenced in replay config. **Missing behavior:** public PDFs not wired into replay gate. **Depends on:** B2-038.

## Scope

Add harvested PDFs to test replay fixtures without bloating git (use manifest refs).

## Non-Goals

- Do NOT commit multi-GB blobs outside LFS.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `config/replay_corpus_manifest.json` referencing Doc-Lineage `tests/fixtures/public_corpus/manifest.json` entries.
- [ ] Add `tests/replay/test_corpus_manifest_wiring.py`.

## Acceptance Criteria

- [ ] Named test: `tests/replay/test_corpus_manifest_wiring.py::test_replay_loads_manifest_entry` passes.
- [ ] **Deliberate-break gate:** break manifest sha → test **must FAIL** → revert.

## Implementation Notes

Depends on CalPERS harvester (B2-038) and Doc-Lineage public corpus manifest (B2-037).

_Surfaced by B2-043._
