## Why

CalPERS seeded but IC items not crawled (R6). Verified: `clones/Pension-Data/dossier-out/DOSSIER.md:1-20` documents CalPERS source_map seeding but `grep -r calpers_ic clones/Pension-Data/src` returns no harvest module. Owner default #9: CalPERS-style per-item PDFs. **Missing behavior:** no IC packet crawler.

## Scope

Harvester registering items into public-doc-fixtures manifest format.

## Non-Goals

- Do NOT parallel SWIB consolidated books (owner default).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/pension_data/harvest/calpers_ic.py` with offline test fixture.
- [ ] Add `tests/harvest/test_calpers_ic_offline.py`.

## Acceptance Criteria

- [ ] Named test: `tests/harvest/test_calpers_ic_offline.py::test_ic_items_parsed` passes.
- [ ] **Deliberate-break gate:** return zero items → test **must FAIL** → revert.

_Surfaced by B2-038._
