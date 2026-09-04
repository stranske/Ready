# Fine-Art-Archive — dossier (2026-09-04)

## 1. Purpose in one paragraph

Fine-Art-Archive is the version-controlled **code and policy layer** for a personal museum-grade image archive of roughly 3,400+ artworks. The repository does **not** hold masters or sidecars; those live in a Dropbox workspace (`Dropbox/Pictures/Art/works/`), selected at runtime via `FAA_WORKS_DIR` / `FAA_ART_WORKS_ROOT` (`README.md`, `src/fine_art_archive/api/config.py`). The tool lets one owner **identify, deduplicate, enrich, browse, rate, and display** works with museum-style metadata (Wikidata Q-IDs, holder accessions, field-level provenance) while keeping originals local-first. It assumes a split model: data work on a Mac with the full Dropbox tree, library/CI in GitHub (`docs/NEXT_PHASE_PLAN.md`), with cloud automation unable to see the local corpus.

## 2. Who uses it and how (surfaces)

| Surface | Entry point | Who uses it | Status (evidence) |
|--------|-------------|-------------|-------------------|
| **CLI** (~74 scripts) | `scripts/*.py` — e.g. `build_manifest.py`, `visual_dedupe.py`, `apply_lens_recovery.py` | Owner / local agents | **Working** — 123 `test_*.py` modules |
| **CLI launcher** | `scripts/run_companion_app.sh` | Owner starting browse UI | **Working** — rebuilds `manifest.csv` on launch (`README.md` L48–52) |
| **HTTP API + HTML UI** | `src/fine_art_archive/api/main.py`; `src/fine_art_archive/ui/index.html` | Owner at `http://localhost:8401/` | **Working** — works, ratings, dossiers, e-ink, review routes; `tests/test_companion_app_api.py` |
| **File artifacts (external)** | `Art/works/<work_id>/meta.json`, `manifest.csv` | All surfaces via `api/store.py` | **Working when workspace mounted** — one fixture in `staging_sidecars/test-wid/` |
| **JSONL logs** | `data/ratings_log.jsonl`, `data/research_requests.jsonl` | Companion App | **Working** — append-only (`api/main.py` L3–5) |
| **Backplane contracts** | `docs/contracts/*`, `scripts/validate_run_contract.py` | Fleet (planned) | **Scaffold** — validator only; no emitter (`backplane-conformance.yml` L49–55) |
| **Excel** | — | — | **Not present** |
| **E-ink feed** | API `/eink/*`, `src/fine_art_archive/eink/feed.py` | Owner / LAN panels | **Partial** — logic present; hardware deferred (`docs/NEXT_PHASE_PLAN.md` L48) |

## 3. Structure map

```
Fine-Art-Archive/
├── src/fine_art_archive/     Domain library (sidecar, collect, identity, enrichment, api, eink, preference)
├── schemas/                  meta.json JSON Schema
├── scripts/                  CLI batch operators (~74 files)
├── tests/                    Pytest (123 modules)
├── config/                   Policy YAML/JSON (sources, e-ink, models, hosts)
├── data/                     Repo-local logs and queues (not the artwork corpus)
├── docs/                     Operator docs, contracts, roadmaps
├── tools/                    LLM/CI helpers (outside installable package)
├── staging_sidecars/         Single test sidecar fixture
└── .github/                  Workflows/prompts — largely synced from stranske/Workflows
```

## 4. Major code features you must understand to extend it

- **Sidecar schema** — `sidecar.py` + `schemas/meta.schema.json`: canonical per-work JSON; all pipelines read/write this.

- **Manifest gate** — `build_manifest.py` + `store.py`: UI lists only works in `manifest.csv` (`README.md` L43–46).

- **D017 dedup cascade** — `collect/dedup_cascade.py`: sha256 → pHash → artist Q-ID → title → DINOv2 hook; blocks duplicate acquisitions.

- **Acquisition flow** — `collect/acquisition_flow.py`: museum collectors, verify, quality, dedup in one assessment.

- **Wikidata enrichment** — `enrichment/work_qid_by_creator.py`, `known_works/fetchers.py`: SPARQL oeuvre fetch and Q-ID resolution.

- **Field provenance** — `provenance.py`: per-field research ledger in sidecars (status, source, conflicts).

- **Companion API** — `api/main.py`: browse, rate, review queues, dossiers, e-ink playlists; ratings → JSONL.

- **Preference / selection** — `preference/{rocchio,bradley_terry,exhibition}.py` + `selection/lenses.py`: learned taste and multi-lens acquisition budgeting.

- **Crosswalk / IIIF** — `crosswalk.py`, `iiif.py`: Dublin Core, Linked Art, IIIF from sidecars.

- **E-ink pipeline** — `eink/{render_strategy,gamut,feed}.py`: device-target rendering and clock-based playlist rotation.

## 5. Data model, identifiers and contracts

**Entities:** **work** via `work_id` (7-char hash prefix + slug, `meta.schema.json` L17–20). Stable keys: `stable_identifiers.wikidata_q`, museum accession, `artist.wikidata_q`, ULAN.

**Persistence:** files only — JSON sidecars, CSV manifest, JSONL logs, NPZ embedding caches (`visual_dedupe.py` L19–41). No app database in `src/`.

**Versioning:** `schema_version: "1.0"`; `field_provenance` records supersession via `prior_value` (partially wired).

| Contract | Emits | Consumes |
|----------|-------|----------|
| `schemas/meta.schema.json` | `sidecar.write()` | `sidecar.validate()`, all readers |
| `run-contract/v1` | **No** (`run-contract-v1.md` L16–17) | `scripts/validate_run_contract.py` only |
| `artifact-manifest/v1`, `evidence-object/v1` | **No** | Validator |
| `capability-bundle/v1` | **No** (no code references) | **No** |
| `identity-map-conventions.md` | **Documented only** — fleet `manager:`/`fund:` IDs; art uses `work_id`/Wikidata Q |

## 6. External inputs and dependencies

**Sources:** Wikidata SPARQL (`known_works/fetchers.py`); museum APIs via collector shell scripts; Google Lens JSONL (`apply_lens_recovery.py`); Wikipedia for dossiers (`enrichment/dossier.py`). Corpus on Dropbox (`README.md` L5).

**LLM:** not in core `pyproject.toml`. `tools/llm_provider.py` + `scripts/langchain/*` serve **CI agent automation** (optional LangSmith). Vision tagging: optional `torch`/`transformers` (`[tagger]`, `vision_tag_works.py`).

**Stack:** FastAPI, Pydantic, Pillow, imagehash, jsonschema, numpy; uvicorn for app. Local CLIs + local server; no Docker in README.

## 7. Current state

**CI:** `pr-00-gate.yml` + reusable Python CI; **81% coverage** floor (`ci.yml` L49). Package **Alpha** (`pyproject.toml` L16). 123 test modules.

**Usable now:** sidecar validation, dedup, enrichment scripts, Companion API, manifest rebuild, crosswalk/IIIF.

**Gated / partial:** preference learning (`NEXT_PHASE_PLAN.md` L42–43); physical e-ink; backplane emission; LLM dossier synthesis (`dossier.py` L17–18).

**Key gaps:** corpus outside repo (`PROJECT_TODO.md` L11–14); manifest must be rebuilt after promotion (`README.md` L54–57); lineage fields unread (`PROJECT_TODO.md` L56–63); DINOv2 cache can lag (`AGENTS.md` L227–230); ops scripts named in `AGENTS.md` absent from `scripts/`; Stage C e-ink dormant (`A_SERIES_ROADMAP.md` L33–46).

## 8. Claims vs reality

- **`AGENTS.md` cites `visual_find_in_unindexed.py`, `promote_acquisitions.py`, `build_unindexed_embed_cache.py`** — **not in repo**; only `visual_dedupe.py` exists.

- **`run-contract-v1.md` L16–17** — no emitter; no `config/backplane_participants.json`; CI stub skips (`backplane-conformance.yml` L51–55).

- **`validate_run_contract.py` L409–412** references `tests/fixtures/backplane/` — **missing**.

- **Fresh clone** serves one fixture work unless `FAA_WORKS_DIR` set (`main.py` L66–70).

- **`companion_app_design.md`** referenced in `NEXT_PHASE_PLAN.md` L46 — **not in repo**.

- **Fleet `identity-map`** has no `artwork` entity type; archive IDs do not match `manager:cik_*` shape.

## 9. Interoperability hooks (for the fleet program)

**Can OFFER:** `work_id` + `meta.json` sidecars; Wikidata Q-IDs; `field_provenance` evidence notes; Dublin Core / Linked Art / IIIF exports; ratings and research-request JSONL; DINOv2 embeddings (operational, off-repo).

**Would CONSUME:** fleet manager/fund IDs only via explicit mapping to `holder` — no consumer today; `run-contract/v1` envelopes — validator only.

**Collision risks:** `work_id` is archive-local; Wikidata Q must not denote a series as a work (`sidecar.py` L45–48); fleet `manager:` vs `holder.wikidata_q` are different namespaces; art `category` enum ≠ Inv-Man-Intake asset classes.

## 10. Reuse candidates

| Component | Path |
|-----------|------|
| Sidecar validator/writer | `src/fine_art_archive/sidecar.py` |
| Field provenance ledger | `src/fine_art_archive/provenance.py` |
| Dedup cascade | `src/fine_art_archive/collect/dedup_cascade.py` |
| Multi-lens acquisition selector | `src/fine_art_archive/selection/lenses.py` |
| Exhibition quality×diversity picker | `src/fine_art_archive/preference/exhibition.py` |
| Bradley-Terry ranking | `src/fine_art_archive/preference/bradley_terry.py` |
| Dublin Core / Linked Art crosswalk | `src/fine_art_archive/crosswalk.py` |
| Dossier assembler (commerce-screened) | `src/fine_art_archive/enrichment/dossier.py` |
| E-ink playlist feed | `src/fine_art_archive/eink/feed.py` |
| Run-contract validator | `scripts/validate_run_contract.py` |
| LLM fallback provider | `tools/llm_provider.py` |

## 11. Proposed direction (evidence-based)

**Finish scaffolded:** wire backplane fixtures + `emit_reference_run.sh` (§8); implement `crop_region` consumer (`PROJECT_TODO.md` L62–63); complete `prior_value` re-resolution (`misresolved_work_qid.py` L185); restore or delete missing ops scripts from `AGENTS.md`.

**New capability:** art-specific fleet entity type for Wikidata joins; emit `run-contract/v1` from enrichment batches; post-promotion manifest hook; DINOv2 cache freshness in `/healthz`; demand-ordered dossiers (`A_SERIES_ROADMAP.md` L58–59).

## 12. What a colleague needs to know (5 bullets, no code identifiers)

- This repo is **software for a personal art library**, not the images themselves; originals and metadata sit on the owner's Dropbox and are wired in at runtime.

- The daily interface is a **local web app** to browse works, record preferences, and review acquisitions — but only for works listed in a catalog file that must be refreshed when the archive grows.

- Works are identified through **public museum and Wikidata records** where possible, with explicit handling so copies and variants in different museums stay separate holdings.

- Automated tests validate the **code** well, but full-archive checks and vision models only run on the owner's machine where the files exist.

- Fleet-wide research contracts are **documented here but not yet produced**; linking to investment-office tools will need a agreed mapping between artwork IDs and manager/fund IDs.
