Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0 (this unit). GitHub CLI unauthenticated (`gh auth login` / `GH_TOKEN` required) — open-issue dedup, `gh issue create`, format-guard readback, and `gh run list` not performed.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/47 — `tests/test_package_identity.py` and fact-key-map export modules pass on tip `09681ce`; sdist includes export fixtures.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/48 — `tests/test_identity_manifest.py` passes symlink/containment cases on tip.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/49 — `tests/test_identity_manifest.py` passes oversized-document policy on tip.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/50 — `tests/harvest/test_edgar_ex10_offline.py` passes harvest atomicity on tip.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/51 — `pyproject.toml` URLs and wheel metadata tests pass on tip.

# Doc-Lineage audit — 2026-09-23 (attempt 2)

Audited `stranske/Doc-Lineage` `main` at `09681ce1f1b39ffa912b43a7013ed60c7a3d6a94` (fresh `git pull --ff-only`). Scope: repo-owned product code (`src/doc_lineage/`, `tests/`, package metadata, user docs); Workflows-synced `.github/` excluded except the issue-format contract. No dossier in this workspace.

## Orientation

~9.3k Python/JSON LOC in `src/` + `tests/`; 330 collected tests; `python -m ruff check src tests` clean. Editable install in `/tmp/dl-audit-venv` drives all live CLI probes below.

## Product scorecard (live)

| Core function | Score | Evidence |
|---|---|---|
| Ingest PDF → segments + artifact manifest | WORKS | `doc-lineage ingest tests/fixtures/synthetic_lpa.pdf` → 5 segments / 2 pages; `ingest tests/fixtures/public_corpus/calpers/ic/default.pdf` → 1 segment / 1 page; segment counts differ across materially different inputs. |
| Page-attributed extraction (+ OCR when needed) | PARTIAL | `extract()` on synthetic LPA → 2 spans (`stable_id` prefix `b709931830bf`); on CalPERS `default.pdf` → 0 spans (`4c3b40a26097`) with unreadable text layer; Tesseract absent here so OCR integration not live-driven (correctly partial, not fabricated). |
| Comparison / fact-key-map export | WORKS | `doc-lineage export-fact-key-map tests/fixtures/fact_key_map/tracked_variables.json --output <dir>` writes `artifact-manifest.json`; `tests/export/test_fact_key_map*.py` 27/27 passed. |
| DOCX blackline export | WORKS | `tests/export/test_docx_redline.py` 5/5; CLI blackline path covered in `tests/test_cli.py`. |
| EDGAR EX-10 harvest (fixture mode) | WORKS | `harvest-edgar --cik 0000320193 --fixture tests/fixtures/harvest/edgar_ex10_filing.json` → 2 exhibits + manifest. |

Primary journey passes: ingest → manifest/segments, then fact-key-map export on the same venv. CLI inventory (`ingest`, `export-docx`, `export-fact-key-map`, `harvest-edgar`) maps to the five scored functions; surfaces unscored 0.

## Regression gates

- Closed-issue regression: `tests/test_package_identity.py`, `tests/test_identity_manifest.py`, `tests/harvest/test_edgar_ex10_offline.py` — 67/67 passed.
- Product slice: `tests/ingest`, `compare`, `mutations`, `export`, `harvest`, `blackline`, package/identity/schema/CLI — **203 passed**, 1 failed (`test_console_script_runs_the_documented_command`: broken global `doc-lineage` on base interpreter shadows editable install; same test passes in isolated venv).
- Full suite minus OCR-dependent cases: **323 passed**, 7 failed (all OCR/Tesseract; expected without executable).

## Eight dimensions

No new adversarially verified defect survived dedup against prior work. Open historical follow-ups (#36–#38, #45) are deliberate-break-evidence gaps from merged PR verification, not newly discovered product breakage on this tip. #60 (line preservation) remains closed; `tests/test_extract_lines.py` passes where not OCR-gated.

## Delivery

No issue bodies filed: no fresh verified candidate and no GitHub credentials in this executor. Canonical continuity: `Code/Audits/Doc-Lineage/2026-09-23-SCORECARD.md` and `AUDIT_LEDGER.md` (attempt 2 row). Intake log not appended (no URLs).

Confidence: **high** on scorecard and #47–#51 refutations (live CLI + named tests on current tip). **Medium-high** that no additional P1/P2 defect exists without authenticated issue/CI readback or a Tesseract-equipped OCR exercise.
