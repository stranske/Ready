# Fine-Art-Archive dossier verification — 2026-09-04

Verification scope: all substantive claims in sections 4, 5, 8, and 9 of the dossier. “Confirmed” means the cited repository code or document supports the stated claim; “Wrong” records the corrected wording now used in the dossier.

| Section | Claim checked | Result | Repository evidence |
| --- | --- | --- | --- |
| 4 | Sidecar schema is canonical per-work JSON and the module validates/writes it. | CONFIRMED | `src/fine_art_archive/sidecar.py:27-42,92-100`; `schemas/meta.schema.json:4-20` |
| 4 | UI navigation is manifest-backed. | CONFIRMED | `scripts/build_manifest.py:2-24`; `api/store.py:110-129` |
| 4 | D017 is sha256 → pHash → artist Q-ID → title → DINOv2. | WRONG — second stage is **dHash**, followed by title metadata matching. | `collect/dedup_cascade.py:1-16` |
| 4 | Acquisition flow combines collection, verification, quality, and dedup assessment. | CONFIRMED | `collect/acquisition_flow.py:1-42,146-210` |
| 4 | Wikidata discovery/resolution uses SPARQL and creator-QID matching. | CONFIRMED | `known_works/fetchers.py:1-15,57-105`; `enrichment/work_qid_by_creator.py:1-28` |
| 4 | Field provenance records per-field status, source, reference, and conflicts. | CONFIRMED | `provenance.py:11-18,74-155` |
| 4 | Companion API exposes browse, dossier/research, review, and e-ink surfaces. | CONFIRMED | `api/main.py:356-400,595-833,874-1045,1279-1304` |
| 4 | Rocchio, Bradley-Terry, exhibition selection, and lenses are implemented. | CONFIRMED | `preference/rocchio.py:50-176`; `bradley_terry.py:42-231`; `exhibition.py:38-100`; `selection/lenses.py:53-366` |
| 4 | Crosswalk and IIIF modules project sidecars to the stated formats. | CONFIRMED | `crosswalk.py:62-166`; `iiif.py:106-107` |
| 4 | E-ink feeds use clock-derived playlist rotation. | CONFIRMED | `eink/feed.py:17-28,148-161` |
| 5 | `work_id` is a seven-character SHA-256 prefix plus a slug. | CONFIRMED | `meta.schema.json:17-26`; `sidecar.py:114-123` |
| 5 | Wikidata, accession, artist, and ULAN identifiers are schema-supported. | CONFIRMED | `meta.schema.json:457-548` |
| 5 | Persistence is file-based rather than an application database. | CONFIRMED | `api/store.py:1-45`; `build_manifest.py:1-40` |
| 5 | Schema version is `1.0` and `prior_value` is declared for provenance. | CONFIRMED | `meta.schema.json:22-26,651-667` |
| 5 | The run/artifact/evidence contracts have a validator but no local emitter. | CONFIRMED | `validate_run_contract.py:32-52,207-259,358-409`; `backplane-conformance.yml:45-55` |
| 5 | `capability-bundle/v1` is documented/schema’d but has no local runtime consumer. | CONFIRMED | `contracts/capability-bundle-v1.md:1-3`; `schemas/capability-bundle-v1.schema.json:1-19` |
| 5 | Identity-map conventions are documentation-only for the archive. | CONFIRMED | `contracts/identity-map-conventions.md:1-10,43-90` |
| 8 | Three named visual-operation scripts are cited in `AGENTS.md` but absent from `scripts/`. | CONFIRMED | `AGENTS.md:186-232`; filesystem check |
| 8 | Backplane CI lacks a configured participant registry and repo-specific emitter. | CONFIRMED | `backplane-conformance.yml:5-12,45-55`; absent `config/backplane_participants.json` |
| 8 | Validator self-smoke looks for a missing `tests/fixtures/backplane/`. | CONFIRMED | `validate_run_contract.py:395-430`; filesystem check |
| 8 | A fresh clone serves its fixture work by default. | WRONG — clone contains one staged fixture, but API store defaults to Dropbox `Art/works`; `FAA_WORKS_DIR` or legacy `FAA_STAGING_DIR` selects another sidecar tree. | `api/config.py:13-18`; `api/store.py:23-45`; `api/main.py:59-70` |
| 8 | `companion_app_design.md` is plan-referenced but absent from the clone. | CONFIRMED | `docs/NEXT_PHASE_PLAN.md:45-48`; filesystem search |
| 8 | Fleet identity vocabulary has no artwork entity type. | CONFIRMED | `contracts/identity-map-conventions.md:43-90` |
| 9 | Sidecars, Q-IDs, provenance, crosswalks, JSONL, and embeddings are viable offered artifacts. | CONFIRMED | `meta.schema.json:457-548,672-679`; `crosswalk.py:62-166`; `iiif.py:106-107`; `api/main.py:3,862-1045`; `visual_dedupe.py:1-6` |
| 9 | No current consumer maps fleet manager/fund identifiers to holders. | CONFIRMED | `identity-map-conventions.md:81-90`; repository search found no consumer in `src/` |
| 9 | This repo’s run-contract support is validation-only. | CONFIRMED | `validate_run_contract.py:207-259,358-409`; `backplane-conformance.yml:45-55` |
| 9 | Archive IDs, Wikidata Q-IDs, and fleet manager/fund IDs use distinct namespaces. | CONFIRMED | `meta.schema.json:17-20,457-548`; `sidecar.py:43-49`; `identity-map-conventions.md:43-76` |

Out-of-scope factual corrections: the clone currently has 125 rather than 123 `test_*.py` modules, and `PROJECT_TODO.md` / `A_SERIES_ROADMAP.md` reside under `docs/`.
