Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0 (blocked: `gh` not authenticated; no `GH_TOKEN` / `GITHUB_TOKEN`).

REFUTED: https://github.com/stranske/Doc-Lineage/issues/47 — sdist includes export tests and `tests/fixtures/fact_key_map/tracked_variables.json`; `tests/test_package_identity.py::test_sdist_includes_fact_key_map_fixture_with_export_tests` passes on tip.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/48 — `tests/test_identity_manifest.py` symlink/containment cases pass; manifest no longer hashes out-of-root symlink targets.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/49 — `test_manifest_and_ingest_reject_same_oversized_pdf` passes (shared size policy).
REFUTED: https://github.com/stranske/Doc-Lineage/issues/50 — `test_harvest_failure_leaves_no_partial_publication` passes (atomic harvest publication).
REFUTED: https://github.com/stranske/Doc-Lineage/issues/51 — `test_built_wheel_publishes_doc_lineage_project_urls` passes (`stranske/Doc-Lineage` URLs).

# Doc-Lineage audit run report — 2026-09-23 (attempt 2)

**Clone:** shallow `main` @ `09681ce1f1b39ffa912b43a7013ed60c7a3d6a94` (already up to date).

## Attempt 2 delta

Resumed from unit checkpoint after attempt 1 completed analysis but could not file. Re-ran live scorecard probes, issue-linked tests, and a non-OCR pytest slice on a fresh editable venv (`/tmp/dl-audit-venv`). **Judgment:** the attempt-1 “zero new defects” conclusion still holds on the merits; the refill still **does not restore agent-ready supply** because filing remains blocked and open-issue dedup could not be re-checked (GitHub API/`gh` unavailable in this executor).

## Scope

Application code `src/doc_lineage/`, `tests/`, contracts under `docs/contracts/`. Excluded fleet `.github/` vendored infra.

## Phase 1 orientation

- 330 tests collected; `ruff check` clean on `src` + `tests`.
- Pytest (non-OCR slice, PATH via venv): **307 passed**, 1 failed — `test_console_script_runs_the_documented_command` when a broken global `doc-lineage` on `PATH` shadows the venv entrypoint (environment coupling, not a product defect on tip).

## Phase 1.5 scorecard (live, attempt 2)

| CF | Result | Evidence |
|---|---|---|
| Identity / manifest / ingest | WORKS | Live `ingest tests/fixtures/synthetic_lpa.pdf`; `export-fact-key-map` on fixture → `fact_key_map.json` + manifest |
| Extract + OCR | PARTIAL | `extract` on `synthetic_lpa.pdf` vs `public_corpus/calpers/ic/default.pdf` → different `stable_id` and span counts; OCR path not exercised (no Tesseract here) |
| Schema / classify / mutations | WORKS | `tests/export/test_fact_key_map_cli.py` + `tests/test_identity_manifest.py` (59 tests) green in focused run |
| DOCX redline export | WORKS | Covered by export/CLI test modules (unchanged from attempt 1) |
| EDGAR harvest + links | WORKS | Harvest failure atomicity test green |

Primary journey (ingest → segments + manifest; plus `export-fact-key-map` on tracked-variables fixture) **passes**.

## Phases 2–4

No new adversarially verified AGENT_ISSUE_FORMAT candidate. Interior gaps noted but not filed: missing `docs/PRODUCT_CONTRACT.md` (README is detailed; docs-adoption issue would be the only non-defect filing the skill allows — **declined** this round because refill priority is defect backlog and `gh` is blocked).

## Filing and ledger

- `gh auth status`: not logged in; tokens unset.
- Issues filed: **0**; intake log **not** appended.
- Canonical continuity unchanged: `Code/Audits/Doc-Lineage/2026-09-23-SCORECARD.md`, verification log, mirror this file.

## Confidence

**High** that #47–#51 claims are refuted on tip (named tests re-run). **Medium-high** that no additional P1/P2 defect exists without CI run-list / open-issue inventory this session — would revise if open issues still describe fixed behavior or if CI is red on `main`. **High** that OCR “partial” is environmental unless CI’s OCR job is disabled.
