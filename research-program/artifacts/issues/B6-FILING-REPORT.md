# B6 Filing Report — B4 Drafted Issue Bodies

**Completed:** 2026-09-04 19:59 UTC

## Summary

| Disposition | Count |
|-------------|------:|
| Filed as drafted | 24 |
| Corrected then filed | 7 |
| Dropped | 1 |
| Deduped (not re-filed) | 0 |
| Awaiting owner decision | 1 |

## Filed

- [[P0] Add tracked-variable/v1 + clause-variable satellite schemas (B2-003)](https://github.com/stranske/Workflows/issues/3371) (`Workflows/01-tracked-variable-v1-schemas.md`)
- [[P0] Add mosaic-core/v1 schemas and manifest kind extensions (B2-015)](https://github.com/stranske/Workflows/issues/3372) (`Workflows/02-mosaic-core-schemas.md`)
- [[P0] Add output-substrate/v1 contract schema (B2-028)](https://github.com/stranske/Workflows/issues/3374) (`Workflows/04-output-substrate-v1.md`)
- [[P1] Extend output-substrate/v1 with manifest CSV export slice (B2-032)](https://github.com/stranske/Workflows/issues/3375) (`Workflows/05-excel-manifest-csv-export.md`)
- [[P0] M1 ingest pipeline: parse, segment, manifest (B2-002)](https://github.com/stranske/Doc-Lineage/issues/8) (`Doc-Lineage/02-core-pipeline-m1-ingest.md`)
- [[P1] Emit evidence-object/v1 at manifest boundary (B2-004)](https://github.com/stranske/Doc-Lineage/issues/9) (`Doc-Lineage/03-stranske-pdf-evidence-emission.md`)
- [[P1] Clause blackline engine over segment trees (B2-005)](https://github.com/stranske/Doc-Lineage/issues/10) (`Doc-Lineage/04-clause-blackline-engine.md`)
- [[P2] EDGAR EX-10 LPA harvest lane (B2-007)](https://github.com/stranske/Doc-Lineage/issues/11) (`Doc-Lineage/05-edgar-ex10-lpa-harvest.md`)
- [[P2] Export fact_key_map artifact for mosaic joins (B2-020)](https://github.com/stranske/Doc-Lineage/issues/13) (`Doc-Lineage/07-variable-fact-key-map.md`)
- [[P2] HTML triple-link resolver for mirror manifests (B2-025)](https://github.com/stranske/Doc-Lineage/issues/14) (`Doc-Lineage/08-html-triple-link-resolver.md`)
- [[P2] Word tracked-changes export lane (B2-034)](https://github.com/stranske/Doc-Lineage/issues/15) (`Doc-Lineage/09-word-tracked-changes-export.md`)
- [[P1] Consultant section ontology aligned to tracked-variable/v1 (B2-010)](https://github.com/stranske/Inv-Man-Intake/issues/948) (`Inv-Man-Intake/01-consultant-section-ontology.md`)
- [[P2] CalPERS IC document harvester (B2-038)](https://github.com/stranske/Pension-Data/issues/879) (`Pension-Data/04-calpers-ic-harvester.md`)
- [[P2] N-CSR sample ingest lane (B2-042)](https://github.com/stranske/Pension-Data/issues/880) (`Pension-Data/05-ncsr-sample-ingest.md`)
- [[P1] report-spec.json renderer contract (B2-031)](https://github.com/stranske/Inv-Man-Intake/issues/950) (`Inv-Man-Intake/03-report-spec-json.md`)
- [[P2] ILPA DDQ synthetic fill harness (B2-040)](https://github.com/stranske/Inv-Man-Intake/issues/951) (`Inv-Man-Intake/04-ilpa-ddq-synthetic-fill.md`)
- [[P1] Evidence + identity-map projection emitter (B2-018)](https://github.com/stranske/Pension-Data/issues/881) (`Pension-Data/01-evidence-entity-projection.md`)
- [[P1] Factor renderer-shell from apps/web (B2-029)](https://github.com/stranske/Pension-Data/issues/882) (`Pension-Data/02-renderer-shell-extraction.md`)
- [[P1] workspace-bundle.json contract wiring (B2-030)](https://github.com/stranske/Pension-Data/issues/883) (`Pension-Data/03-workspace-bundle-json.md`)
- [[P2] Replay corpus expansion for public PDF gate (B2-043)](https://github.com/stranske/Pension-Data/issues/884) (`Pension-Data/06-replay-corpus-expansion.md`)
- [[P2] Doc-Lineage variable staging import (B2-044)](https://github.com/stranske/Pension-Data/issues/885) (`Pension-Data/07-doc-lineage-staging-import.md`)
- [[P2] Amtrak GTFS source adapter (B2-046)](https://github.com/stranske/trip-planner/issues/1783) (`trip-planner/02-amtrak-gtfs-adapter.md`)
- [[P2] ConstraintEvaluation envelope contract (B2-048)](https://github.com/stranske/trip-planner/issues/1784) (`trip-planner/04-constraint-evaluation-envelope.md`)
- [[P2] Ranking fixture eval harness (B2-047)](https://github.com/stranske/trip-planner/issues/1786) (`trip-planner/03-fixture-eval-harness.md`)

## Corrected then filed

- [[P0] Add document-mirror/v1 schema and validator hook (B2-023)](https://github.com/stranske/Workflows/issues/3373) (`Workflows/03-document-mirror-v1-schema.md`)
- [[P0] Add fund-clause vocabulary v1 data file (B2-001)](https://github.com/stranske/Doc-Lineage/issues/6) (`Doc-Lineage/01-fund-clause-vocabulary-v1.md`)
- [[P1] Public and synthetic fixture corpus with manifest and provenance (B2-037)](https://github.com/stranske/Doc-Lineage/issues/7) (`Doc-Lineage/10-public-doc-fixtures-manifest.md`)
- [[P2] Synthetic mutation harness for CI ground truth (B2-008)](https://github.com/stranske/Doc-Lineage/issues/12) (`Doc-Lineage/06-synthetic-mutation-harness.md`)
- [[P1] Evidence-object/v1 emitter replacing page-pointer refs (B2-017)](https://github.com/stranske/Inv-Man-Intake/issues/949) (`Inv-Man-Intake/02-evidence-object-emitter.md`)
- [[P2] Duffel flight source adapter (B2-045)](https://github.com/stranske/trip-planner/issues/1785) (`trip-planner/01-duffel-flight-adapter.md`)
- [[P2] Lodging deep-link capture adapter (B2-050)](https://github.com/stranske/trip-planner/issues/1787) (`trip-planner/05-lodging-deep-link-capture.md`)

## Dropped

- `doc-mirror/01-doc-mirror-cli.md` — Repo does not exist; merged CLI slice into comment on Doc-Lineage #2 (dedup: Doc-Lineage #2)

## Deduped

_No exact title collisions filed._ Checked open/recent issues (`gh issue list --state all --limit 60`) in each target repo against wave-1 issues (Doc-Lineage #2–#4, Deliverable-Render #2–#4, Workflows #3368) and B5 wave (Doc-Lineage #5, Deliverable-Render #5–#6, Inv-Man-Intake #947, Pension-Data #878, Workflows #3370, etc.). Related but distinct:

- Workflows #3368 (document-identity convention) complements B2-003/B2-023; not a duplicate.
- Doc-Lineage #2–#5 (wave 1 + B5) cover identity, extraction adapter, ledger schemas, comparison engine; B4 bodies filed as #6–#15 are downstream implementation slices.
- Inv-Man-Intake #947 / Pension-Data #878 (B5 extraction adapters) are prerequisites for B2-017/B2-018 emitters, not duplicates.

## Awaiting owner decision

- `Manager-Mosaic/01-sqlite-html-importer.md` — **recommended repo:** `Manager-Database` — Already a fleet data hub with backplane participant entry, SQLite patterns, and manager identity work; importing mosaic manifests extends existing storage rather than a fourth greenfield repo. Inv-Man-Intake is a producer, not a join store.

## Work-environment corrections applied

- No bodies premised on browser-only/no-Python work constraints were filed; B5 wave already corrected delivery-shape issues.
- `public-doc-fixtures/01` retargeted to Doc-Lineage as `Doc-Lineage/10-public-doc-fixtures-manifest.md` (fixtures live with extraction tests).
- `doc-mirror/01` merged into comment on [Doc-Lineage #2](https://github.com/stranske/Doc-Lineage/issues/2) per TARGET CHECK.

## Citation verification

All bodies re-verified against pulled `clones/<repo>` checkouts 2026-09-04. Corrections: `test_main.py:1-33`, `src/inv_man_intake/run.py:113-118`, `trip_planner/app/services/inventory.py:858`, cross-repo Pension-Data paths in Workflows/03, Inv-Man-Intake vocabulary reference.

## Intake log

Appended 31 entries to `/Users/teacher/.codex/orchestrator/measurement/intake-2026-09-04.log`.
