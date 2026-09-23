Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0 (blocked: `gh` not authenticated).

REFUTED: https://github.com/stranske/Doc-Lineage/issues/47 — sdist built on tip includes `tests/fixtures/fact_key_map/tracked_variables.json` (`MANIFEST.in` + `python -m build -s`).
REFUTED: https://github.com/stranske/Doc-Lineage/issues/48 — `build_manifest_rows` no longer hashes out-of-root symlink targets; containment tests pass in `tests/test_identity_manifest.py`.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/49 — manifest scan and ingest share `MAX_INGEST_BYTES`; `test_manifest_and_ingest_reject_same_oversized_pdf` passes.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/50 — failed harvest rolls back staged files; `test_harvest_failure_leaves_no_partial_publication` passes.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/51 — wheel metadata `Project-URL` entries point to `stranske/Doc-Lineage`, not Template.

# Doc-Lineage audit run report — 2026-09-23

**Clone:** shallow `main` @ `09681ce1f1b39ffa912b43a7013ed60c7a3d6a94` (created this session under `[LOCAL_WORKSPACE]/Doc-Lineage`).

## Scope

Application code `src/doc_lineage/`, `tests/`, contracts under `docs/contracts/`. Excluded fleet `.github/` and `tools/` except when validating issue format (no new bodies filed).

## Phase 1 orientation

- 330 tests collected; `ruff check` clean.
- Local full pytest: 323 passed, 7 failed — six `tests/test_extract_coverage.py` / `test_extract_lines.py` cases require Tesseract OCR; one `test_console_script_runs_the_documented_command` fails when `/opt/anaconda3/bin/doc-lineage` (no `doc_lineage` module) precedes the editable venv script on `PATH`.

## Phase 1.5 scorecard (live)

| CF | Result | Evidence |
|---|---|---|
| Identity / manifest / ingest | WORKS | CLI ingest synthetic LPA; library manifest 6 docs with supersession edge |
| Extract + OCR | PARTIAL | Text-layer PDF extract varies by input; OCR not exercised (no Tesseract) |
| Schema / classify / mutations | WORKS | 38 tests in compare/schema/mutations/emit slice |
| DOCX redline export | WORKS | export + CLI tests green |
| EDGAR harvest + links | WORKS | offline harvest CLI; render link tests green |

Primary journey (ingest → segments + manifest) **passes**.

## Phases 2–4

Eight-dimension review on tip found **no new** verified, non-duplicate AGENT_ISSUE_FORMAT candidate. The 2026-09-20 five-issue batch is **fixed in source**; reproductions above are REFUTED for the program engine.

## Filing and ledger

- `gh auth status`: not logged in; no `GH_TOKEN`.
- Issues filed: **0**. Intake log not updated.
- Canonical artifacts: `Code/Audits/Doc-Lineage/2026-09-23-SCORECARD.md`, `2026-09-23-AUDIT_REPORT.md`, `2026-09-23-verification-log.md`.

## Confidence

High on fix status for #47–#51 at cited paths. Medium that zero new issues is correct without live GitHub issue inventory and CI run list this session — would revise if open duplicates of fixed work remain labeled agent-ready without merge.
