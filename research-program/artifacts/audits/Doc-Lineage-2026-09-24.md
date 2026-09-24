Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0 (`gh` unauthenticated — `gh auth login` or `GH_TOKEN` required for `gh issue create`, live dedup, and format-guard `gh run list`).

REFUTED: https://github.com/stranske/Doc-Lineage/issues/47 — `tests/test_package_identity.py` passes; sdist/wheel include `tests/fixtures/fact_key_map/tracked_variables.json` on tip `09681ce`.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/48 — `tests/test_identity_manifest.py` symlink/containment cases pass on tip.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/49 — `test_manifest_and_ingest_reject_same_oversized_pdf` passes on tip.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/50 — `tests/harvest/test_edgar_ex10_offline.py::test_harvest_failure_leaves_no_partial_publication` passes on tip.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/51 — `pyproject.toml` Project-URL metadata and package identity tests pass on tip.

# Doc-Lineage audit — 2026-09-24 (attempt 1)

Audited `stranske/Doc-Lineage` `main` at `09681ce1f1b39ffa912b43a7013ed60c7a3d6a94` (`git pull --ff-only` clean). No dossier at `artifacts/dossiers/Doc-Lineage.md` in this workspace; scope from README, prior `Code/Audits/Doc-Lineage/` continuity, and `audit-refill.md` (4 open agent-ready vs threshold 2).

## Orientation

~8.6k LOC in `src/` + `tests/`; 330 tests collected; `ruff check src tests` clean. Editable install with `[dev]` in `/tmp/dl-audit-venv-2026-09-24`.

## Product scorecard (live)

| Core function | Score | Evidence |
|---|---|---|
| Ingest PDF → segments + manifest | WORKS | Synthetic LPA: 5 segments / 2 pages; CalPERS IC PDF: 1 segment; counts and `run_id` hashes differ. |
| Page-attributed extraction | PARTIAL | Synthetic: 2 spans; CalPERS: 0 spans without OCR; Tesseract absent — integration not exercised. |
| Compare / classify / mutations | WORKS | `pytest tests/compare tests/mutations tests/blackline` — 27 passed. |
| DOCX blackline export | WORKS | `tests/export/test_docx_redline.py` — 5/5. |
| EDGAR EX-10 harvest (fixture) | WORKS | `harvest-edgar --fixture …` → 2 exhibits; offline harvest tests 67/67 with identity regressions. |

Primary journey passes: ingest → manifest, then `export-fact-key-map` on fixture JSON. Surface inventory unchanged; unscored 0.

## Eight dimensions (summary)

No new adversarially verified defect at cited `file:line` survived dedup against merged fixes (#47–#51) or known open roadmap (#3, #8–#15, etc.). Duplicate `[project.scripts]` + `[project.entry-points.console_scripts]` in `pyproject.toml` is non-canonical metadata only (wheel/CLI work). Console-script acceptance test fails on this host when `PATH` prefers a broken `/opt/anaconda3/bin/doc-lineage`; venv `doc-lineage` works — treated as environment confound per 2026-09-19 audit, not a product filing.

## Delivery

- Canonical scorecard: `Code/Audits/Doc-Lineage/2026-09-24-SCORECARD.md` (load-bearing headline present).
- Backfilled headline on `2026-09-23-SCORECARD.md` so `newest_scorecard` parsing stops re-queuing on missing headline.
- `AUDIT_LEDGER.md` updated; intake log not appended (no issue URLs).
- Format-guard CI not observed (`gh` unavailable).

## Confidence

**High** on scorecard counts and #47–#51 refutations (live CLI + named tests on current tip). **Medium** on “no additional filable defect” without authenticated open-issue dedup and GitHub CI readback; **low** that OCR-gated behavior hides a regression (not exercised here).
