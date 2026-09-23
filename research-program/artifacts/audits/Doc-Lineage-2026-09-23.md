Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0. GitHub CLI authentication is absent, so authenticated `gh` deduplication, `gh issue create`, issue labels, format-guard verdicts, and `gh run list` are unknown rather than passed.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/47 — `tests/test_package_identity.py` and both fact-key-map export modules pass on tip; the source-distribution fixture is now packaged.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/48 — `tests/test_identity_manifest.py` passes the out-of-root symlink/containment cases; manifest scanning rejects symlinks and uses no-follow descriptor reads.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/49 — `tests/test_identity_manifest.py` includes and passes the matched oversized-document policy check; manifest scanning skips documents above `MAX_INGEST_BYTES`.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/50 — `tests/harvest/test_edgar_ex10_offline.py` passes its failed-harvest atomicity tests; `_publish_run` stages files and restores/removes promotions on failure.
REFUTED: https://github.com/stranske/Doc-Lineage/issues/51 — `pyproject.toml` identifies `stranske/Doc-Lineage`, and `tests/test_package_identity.py` passes the built-wheel metadata checks.

# Doc-Lineage audit run report — 2026-09-23

## Scope and evidence

Fresh shallow `main` is `09681ce1f1b39ffa912b43a7013ed60c7a3d6a94` after `git pull --ff-only`. I audited the repo-owned application and product tests (`src/doc_lineage/`, `tests/`, package metadata and user-facing docs), excluding Workflows-synced `.github/` infrastructure. The named dossier and verification table do not exist in this workspace.

Orientation found 9,326 source/test Python-or-JSON lines, 330 collected tests, and clean `python -m ruff check src tests`. A full local pytest run was 329 passed / 1 failed: `tests/ingest/test_ingest_synthetic_pdf.py::test_console_script_runs_the_documented_command` attempts editable installation into this executor's base Anaconda interpreter. The same editable install and documented console command passed in a fresh isolated virtualenv, so this is an executor write-policy coupling, not verified application breakage.

## Product scorecard

| Core function | Result | Live evidence |
|---|---|---|
| A document-library user can ingest a PDF and receive page-anchored segments plus a manifest | WORKS | Actual `doc-lineage ingest --no-docling` ran against `synthetic_lpa.pdf` (5 segments, 2 pages) and public `default.pdf` (1 segment, 1 page). Source SHA and span-count outputs changed with the materially different inputs. |
| A consumer can extract page-attributed text, with unreadable pages visible and OCR attempted | PARTIAL | The native extraction path and coverage/line/cache gates passed. Tesseract is unavailable in this executor, so the installed OCR integration itself was not live-driven; absence is correctly surfaced rather than silently treated as text. |
| An analyst can classify/comparison-detect document changes and export tracked-variable joins | WORKS | `export-fact-key-map` produced its map and `artifact-manifest.json`; 13 comparison/mutation tests passed with distinct changed/unchanged fixtures. |
| A lawyer can export a DOCX blackline and receive native tracked-change markup | WORKS | Actual `export-docx` on two generated, materially different DOCX inputs produced a 36,473-byte file containing both `w:ins` and `w:del` markup. |
| An operator can harvest recorded EX-10 exhibits into a mirror-compatible manifest | WORKS | Actual offline `harvest-edgar --fixture` produced two exhibit records and an artifact manifest. |

Primary journey passes: ingest through manifest/segments, then fact-key-map export. Mechanical CLI inventory is `ingest`, `export-docx`, `export-fact-key-map`, and `harvest-edgar`; all map to the five scored core functions, so surfaces unscored is zero. The focused product gate passed 113 tests across ingest/manifest, extract, comparison, mutation, DOCX export, fact-key-map export, harvest, and package identity.

## Audit result

The previously filed source-distribution, containment, size-policy, atomic-publication, and package-metadata defects (#47–#51) were re-run on this tip and are refuted above. Public unauthenticated API readback found open #36–#38 and #45; these are historical deliberate-break-evidence follow-ups, not duplicate current product defects. #60, the line-preservation prerequisite for Pension-Data, is closed and its `tests/test_extract_lines.py` coverage passes.

Across the eight dimensions, no additional line-level, live-reproduced defect survived review. In particular, manifest containment and bounded reads are now explicit in `src/doc_lineage/manifest.py`; harvest publication stages before promotion in `src/doc_lineage/harvest/edgar_ex10.py`; packaging identity is guarded in `tests/test_package_identity.py`; and the data/catalog, API wiring, docs, and local automation surfaces showed no new contradiction with live behavior. There is no browser surface; the operator surface is the CLI/API, which was driven directly.

## Delivery and risks

No new issue body was created or filed because no new verified candidate exists. The requested canonical `Code/Audits` ledger and `~/.codex/orchestrator/measurement/intake-2026-09-04.log` are outside this unit's writable root; neither was modified. The lack of `gh` authentication means authenticated issue/CI readback and post-file format-guard verification could not be performed, but it does not justify inventing issue URLs or claiming a pass.

Confidence: high in the scorecard and the five closed-issue refutations, based on current-tip live CLI runs and named regression gates. Medium-high that no fresh P1/P2 defect remains: a future authenticated run that finds changed open/recently closed claims, a CI failure on this exact head, or a live Tesseract run that differs from controlled OCR tests would warrant re-audit.
