Scorecard: 6 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0.

# Doc-Lineage audit — 2026-11-25

Audited `stranske/Doc-Lineage` at `8ec540ad537043b51c39c7ec8b554c1d6b676730`.

## Trigger

Track D demand-driven refill: agent-ready open implementation issues at 0% of the last filed set; prior scorecard dated 2026-10-25 (>30 days).

## Outcome

The product contract in `README.md` and mechanical CLI inventory (`build_parser()` in `src/doc_lineage/cli.py`) match the 2026-10-25 round — no new surfaces. Tip advanced one commit (`chore: sync workflow templates`) since `b05b49e`; core offline paths remain healthy.

| Core function | Result | Evidence | Varying-input check |
| --- | --- | --- | --- |
| CF-1 Ingest offline PDF to manifested run | WORKS | `doc-lineage ingest tests/fixtures/synthetic_lpa.pdf --output /tmp/dl_audit_2026-11-25/run1 --no-docling` → 2 segments, source SHA-256 `b7099318…` | `calpers/ic/default.pdf` → 1 segment, SHA-256 `4c3b40a2…` |
| CF-2 OCR recovery for textless pages | PARTIAL | `default_ocr_backend()` → `None` (no Tesseract on host); ingest does not fabricate text | OCR smoke exists in CI (`ocr-smoke.yml`); local real-backend transcription not exercised |
| CF-3 Persisted PDF section pairing + replay | WORKS | Cross-doc `pair-sections` → `cmp_3e5f39b7…`; `lookup-section-pairing` revalidates identity and emits decisions JSON | Cross-doc vs self-pairing changes decision set and unassigned diagnostics |
| CF-4 DOCX comparison + tracked-changes export | WORKS | `tests/export/test_docx_redline_golden.py` (16 tests) via CLI `create-comparison` / `export-docx --blackline` | Distinct redline bytes for distinct revised text in golden scenarios |
| CF-5 Legal-fee extract + fact-key map | PARTIAL | `extract-variables` + `export-fact-key-map` on synthetic LPA run | `fund:alpha_iv` vs `fund:beta_v` changes `entity_ref` and `variable_id`; coverage still management-fee grammar only per `docs/contracts/tracked-variable-v1.md#extraction-coverage` |
| CF-6 EDGAR EX-10 harvest | WORKS | Fixture harvest → 2 exhibits + `artifact-manifest.json` | Staged publication unchanged from #50 contract |
| CF-7 Confirmed supersession edges | PARTIAL | `tests/lineage/` (79 passed) exercise `build_supersession_chain` with/without evidence | Varying evidence presence changes edge list; no top-level CLI |
| CF-8 Page-attributed PDF text extract | WORKS | `doc_lineage.extract.extract` on synthetic LPA → 2 spans / 718 chars; scanned CalPERS PDF → 0 spans | Span count tracks text-layer presence |

Primary journeys (all pass):

1. Ingest → `extract-variables` → `export-fact-key-map`
2. Ingest pair → `pair-sections` → `lookup-section-pairing`
3. DOCX pair → comparison record → native redline (pytest golden + CLI wiring)

Surface inventory diff vs 2026-10-25: **empty** (8 CLI subcommands + documented library surfaces unchanged). Surfaces unscored: 0.

## Verification and deduplication

- **Tests:** Python 3.13 venv, `pytest tests -q` → **761 passed, 1 skipped** (59.45s). CI `ci.yml` green on tip.
- **Lint:** `ruff check src tests` → 0 violations.
- **Closed-issue re-probe:** Named acceptance tests pass for #182 (`test_published_legal_variable_resolves_from_claims_dir`), #185 (`test_offline_synthetic_lpa_yields_sections_1_to_4`), #193 (`test_edgar_manifest_has_accurate_filing_provenance`). No closed-still-broken rows.
- **Historic refutations retained:** #47–#51 reproduction tests still pass on tip (`test_sdist_includes_fact_key_map_fixture_with_export_tests`, manifest symlink/size guards, harvest atomic publication, package identity).
- **Open backlog:** Only tracker issues #1 and #19 remain open; recently closed roadmap items (#111–#113, #144, #182, #185, #186, #193) are reflected in tests and docs. No duplicate filable defects identified.

## Dimension notes (abbreviated)

| Dim | Finding |
| --- | --- |
| 1 Code quality | Ruff clean; no new hotspots on tip delta |
| 2 Duplication | No new root/template drift in app code (`.github` sync-only delta) |
| 3 Wiring | Config→CLI→library paths traced for scored surfaces; outputs respond to inputs in live probes |
| 4 UX | No operator UI; CLI stderr warnings (e.g. unassigned section chars) behave as documented |
| 5–7 Field/tools/opportunities | No new actionable gaps beyond README-documented partial capabilities |
| 8 Local automations | Consumer `.github/` owned by Workflows; out of scope |

## Risks and limits

- High confidence on offline ingest, section pairing, DOCX blackline, harvest, and extraction grammar for the documented management-fee subset.
- CF-2 remains PARTIAL locally without Tesseract; CI `ocr-smoke.yml` is the authoritative real-backend check (#186 delivered).
- CF-5 / CF-7 remain PARTIAL by product contract (bounded extraction grammar; library-only supersession), not regressions.

## Delivery

- Issues filed: **0**
- Artifacts: `Code/Audits/Doc-Lineage/2026-11-25-SCORECARD.md`, `2026-11-25-audit-run.md`, `2026-11-25-surface-inventory.txt`