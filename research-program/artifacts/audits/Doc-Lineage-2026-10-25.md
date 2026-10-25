Scorecard: 6 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0.

# Doc-Lineage audit — 2026-10-25

Audited `stranske/Doc-Lineage` at `b05b49e09876cb0550f12d8aaee35e16c4fb1061`.

## Outcome

The previous audit scorecard (2026-09-24) was stale (31 days old). The repository has actively progressed and expanded its surface since then, including native DOCX blacklining with persisted comparison ID lookup (#109, #110), persisted PDF section pairing and replay revalidation (#112), bounded legal variable extraction, and fact-key map export.

All current CLI and public product paths were inventoried from `build_parser()` and driven live using isolated data under `/tmp`:

| Core function | Result | Evidence | Varying-input check |
| --- | --- | --- | --- |
| Ingest an offline PDF to a manifested run | WORKS | `doc-lineage ingest tests/fixtures/synthetic_lpa.pdf --output /tmp/... --no-docling` produced 2 segments across 2 pages with source SHA-256 `b709931830bf2185...` and manifest `artifact-manifest/v1`. | Varying input to `tests/fixtures/public_corpus/calpers/ic/default.pdf` produced 1 segment and distinct source SHA-256 `4c3b40a2609796c8...`. |
| Recover text for pages without a text layer | PARTIAL | `get_ocr_backend()` safely reports that the local Tesseract binary is absent on this host (`src/doc_lineage/extract/ocr.py`). The offline ingest path gracefully records missing text layer without hallucinating content. | Absent binary is handled safely; live OCR transcription could not be exercised in this environment. |
| Create and replay a persisted PDF section pairing | WORKS | `pair-sections` on run1 and run2 produced comparison ID `cmp_27fbdcab67a244f69e5ad380a9fc7d1d`; `lookup-section-pairing` revalidated inputs, order, options, and reproduced decisions. | Varying inputs (self-pairing vs cross-document pairing) changed decisions and alignment confidence scores. |
| Create a DOCX comparison and native tracked-changes document | WORKS | `create-comparison` with two synthetic DOCX files produced `cmp_22d45e0ebc3f46df92e85196ee53296a`; `export-docx --blackline <ID>` verified source SHA-256 digests and produced redline DOCX. | Original (`742ee869...`), modified (`a3c7d059...`), and redline (`17025c31...`) have distinct SHA-256 digests; destination aliasing is strictly rejected. |
| Extract the documented legal-fee subset and export a fact-key map | PARTIAL | `extract-variables` on synthetic LPA ingest run with `--entity-ref fund:alpha_iv` produced `tracked-variables.json` with structured management-fee schedule (1.75% / 1.25%); `export-fact-key-map` produced `fact_key_map.json`. | Varying entity from `fund:alpha_iv` to `fund:beta_v` altered `entity_ref` and `variable_id`; non-fee inputs produce empty `tracked-variables.json` and record unresolved items. |
| Harvest EDGAR EX-10 exhibits into a mirror manifest | WORKS | `harvest-edgar --cik 0000320193 --fixture tests/fixtures/harvest/edgar_ex10_filing.json` yielded 2 exhibits (EX-10.1 and EX-10.2) and `artifact-manifest.json`. | Publication stages atomically in a temporary folder before promotion. |
| Build confirmed supersession edges from supplied evidence | PARTIAL | Direct library API `build_supersession_chain` constructed confirmed `SupersessionEdge` when supplied with valid `DocumentRef` and `supersession_evidence`; unevidenced invocation returned `[]`. | Varying claim endpoints alters constructed edges; CLI exposes hints only, matching documented contract. |
| Extract page-attributed PDF text for consumers | WORKS | `doc_lineage.extract.extract` produced 2 page-anchored text spans (874 chars) for synthetic LPA, and 0 spans for scanned CalPERS PDF. | Extracted spans and characters respond directly to physical page content. |

The primary offline user journeys pass cleanly:
1. Ingest → Bounded variable extraction → Fact-key map export.
2. Ingest pair → Persisted section pairing → Lookup and replay.
3. DOCX pair → Comparison record creation → Tracked-changes DOCX export by comparison ID.

All 8 inventory-mapped surfaces have been scored; surfaces unscored: 0.

## Verification and Deduplication

- Test suite: `/opt/anaconda3/bin/python3 -m pytest tests -q` ran 717 collected tests: 717 passed, 0 failed in 77.42s.
- Linter: `/opt/anaconda3/bin/python3 -m ruff check src tests` passed with 0 violations.
- Scheduled GitHub Actions workflows on `main` are green.
- Consumer automation under `.github/` is owned by `stranske/Workflows` per `AGENTS.md` and active PRs #146 (consumer sync) and #147 (gate context seal check) are open.
- Active open issues #111 (wider legal variable extraction), #112 (section pairing CLI commands), #113 (consumer replay test audit), and #144 (Python 3.13/3.14 CI matrix update) already track open roadmap and infrastructure work.
- No new, distinct, reproducible defects or unaddressed product seams were found on live `main`. Issues filed: 0.

## Closed-Issue Refutations

REFUTED: https://github.com/stranske/Doc-Lineage/issues/47 — source distribution tests confirm the sdist contains the fact-key-map fixture and export tests pass.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/48 — manifest containment tests confirm rejection of both in-root and out-of-root symlinks.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/49 — manifest builder and ingest tests confirm rejection of oversized documents exceeding configured limits.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/50 — fixture-backed harvest tests confirm atomic staged publication without partial output.

REFUTED: https://github.com/stranske/Doc-Lineage/issues/51 — package identity tests confirm published project URLs match repository metadata.

## Risks and Limitations

- Confidence is high for the core offline document lineage, blackline comparison, and extraction flows.
- OCR remains scored PARTIAL because Tesseract is not installed in the local execution environment; the fallback logic is verified, but scanned image transcription cannot be exercised locally.
- Legal clause extraction remains scored PARTIAL because only the management fee subset is implemented; broader ontology extraction is tracked in open issue #111.
