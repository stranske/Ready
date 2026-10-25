Scorecard: 6 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0.

# Doc-Lineage audit — 2026-10-25

Audited `stranske/Doc-Lineage` at `b05b49e09876cb0550f12d8aaee35e16c4fb1061`.

## Outcome

The prior scorecard was stale because the repository has added real product surfaces, not merely tests. All current CLI product paths were inventoried from `src/doc_lineage/cli.py:31-148` and driven using isolated data under `/tmp`:

| Core function | Result | Evidence |
| --- | --- | --- |
| Ingest an offline PDF to a manifested run | WORKS | Two generated PDFs produced distinct run/source hashes and segments. |
| Recover text for pages without a text layer | PARTIAL | The local Tesseract binary is absent. The code correctly returns no backend rather than silently claiming coverage (`src/doc_lineage/extract/ocr.py:62-78`), but real transcription could not be exercised. |
| Create and replay a persisted section pairing | WORKS | `pair-sections` produced `cmp_912b221900a042a38c277c326ae1abca`; replay returned decisions that varied with before/after section titles. The artifact binds inputs and revalidates them (`src/doc_lineage/blackline.py:365-455`). |
| Create a DOCX comparison and native tracked-changes document | WORKS | `create-comparison` followed by `export-docx --blackline <ID>` produced a redline with a SHA-256 distinct from both generated inputs. ID replay verifies the recorded input bytes (`src/doc_lineage/cli.py:152-199`). |
| Extract the documented legal-fee subset and export a fact-key map | PARTIAL | `extract-variables` then `export-fact-key-map` succeeded using `fund:alpha_iv`; the bounded subset is accurately documented as partial (`README.md:12`). |
| Harvest EX-10 exhibits to a manifest | WORKS | Fixture-backed harvest yielded two exhibits and a manifest; publication stages before promotion (`src/doc_lineage/harvest/edgar_ex10.py:275-314`). |
| Build confirmed supersession edges from supplied evidence | PARTIAL | The direct API returned a content-bound edge for a valid owner assertion and none without evidence, as designed. The CLI exposes only hints, matching the explicitly partial README claim (`README.md:16`). |
| Extract page-attributed PDF text for consumers | WORKS | The offline text path produced page-attributed spans for the synthetic source; complete coverage was reported.

The primary offline journey passes: ingest → bounded variable extraction → fact-key map, plus a separate ingest-pair → persisted comparison → replay journey. All current CLI surfaces map to a scorecard row; no surfaces are unscored.

## Verification and deduction

- `ruff check src tests` passed; 717 tests collect.
- Current GitHub scheduled runs at this head, including `Maint Coverage Guard`, are successful.
- Full local suite: 716 passed, 1 failed. The sole failure is `tests/ingest/test_ingest_synthetic_pdf.py::test_console_script_runs_the_documented_command`, whose editable install targets an unwritable host path under `[LOCAL_HOME]/.local`. This is an audit-host permission confound, not a repository failure: a fresh temporary virtual environment installed the package, ran the installed `doc-lineage` command, and passed that same test.
- No browser/native UI exists; the CLI operator surface was directly exercised, so no static-only UX claim is made.
- The consumer automation tree is Workflows-owned by `AGENTS.md`; no local issue was proposed for synced infrastructure.
- Open #111, #112, and #113 are existing roadmap work. No distinct, current-tip defect or bounded implementation gap survived verification and deduplication.

## Closed-issue rechecks

REFUTED: https://github.com/stranske/Doc-Lineage/issues/47 — temporary-environment package tests confirm the source distribution includes the fact-key-map fixture.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/48 — current manifest containment tests reject out-of-root and in-root symlinks.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/49 — current manifest/ingest tests reject the same over-limit document.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/50 — current fixture-backed harvest completed its staged publication without partial output.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/51 — package identity tests verify the published project URLs.

## Risks and limits

Confidence is high that there is no new filable defect in the exercised first-party surfaces. It is medium—not high—for production OCR and live SEC-network behavior: neither can be concluded from this environment. OCR remains scorecard-partial until a host with Tesseract produces a real scanned-page transcription; fixture harvest is not a substitute for live SEC availability or rate-limit behavior.

The unit-declared dossier and verification-table paths were absent, and the write boundary forbids updating the canonical `Code/Audits` ledger directly. This report and its checkpoint carry the complete handoff record.
