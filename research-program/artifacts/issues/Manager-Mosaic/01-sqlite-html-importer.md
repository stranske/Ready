## Why

Fleet lacks cross-source join for investment mosaic (R3). Verified: `clones/Workflows/config/backplane_participants.json:200-208` lists Inv-Man-Intake as `planned` with `reference_state: missing` — no fleet mosaic importer exists. **Depends on:** B2-015 mosaic-core schemas. Owner default: port work-side data model, not greenfield UX (`B2-gap-analysis` owner decision #4).

## Scope

New repo importing `run-contract/v1` manifests from Pension-Data, Inv-Man-Intake, Doc-Lineage into one `.sqlite` per investment + static HTML index.

## Non-Goals

- Do NOT rebuild work-side HTML UX from scratch (B2-R25 reject).
- Do NOT require manager:cik_* projection (B2-019 Tier 4) — use `confidence < 1` fallbacks.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Scaffold repo; add `src/manager_mosaic/import_manifests.py`.
- [ ] SQLite schema for `facts`, `discrepancies` per mosaic-core/v1.
- [ ] Static `dist/index.html` listing discrepancies with links to source evidence.
- [ ] Add `tests/import/test_merge_three_manifests.py` with synthetic fixtures from three repos.

## Acceptance Criteria

- [ ] Named test: `tests/import/test_merge_three_manifests.py::test_surfaces_cross_source_discrepancy` passes.
- [ ] **Deliberate-break gate:** skip one repo manifest → discrepancy count drops → test **must FAIL** → revert.

_Surfaced by B2-016; file after Workflows B2-015._
