## Why

Expand replay corpus after CalPERS harvester (B2-038). Verified: `clones/Pension-Data/tools/replay/runner.py:130-172` replays golden corpus but manifest entries from `public-doc-fixtures` are not referenced in replay config. **Missing behavior:** public PDFs not wired into replay gate. **Depends on:** B2-038.

## Scope

Add harvested PDFs to test replay fixtures without bloating git (use manifest refs).

## Non-Goals

- Do NOT commit multi-GB blobs outside LFS.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Extend replay fixture config to reference `public-doc-fixtures` manifest entries.
- [ ] Add `tests/replay/test_corpus_manifest_wiring.py`.

## Acceptance Criteria

- [ ] Named test: `tests/replay/test_corpus_manifest_wiring.py::test_replay_loads_manifest_entry` passes.
- [ ] **Deliberate-break gate:** break manifest sha → test **must FAIL** → revert.

_Surfaced by B2-043._
