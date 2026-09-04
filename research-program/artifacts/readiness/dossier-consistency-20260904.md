# Dossier consistency pass — 2026-09-04

**Unit:** `readiness-dossier-consistency-20260904` (attempt 1)  
**Sources:** `artifacts/dossiers/Pension-Data.md`, `Portable-Alpha-Extension-Model.md`, `Travel-Plan-Permission.md` and their `.verification.md` tables (reverified 2026-09-04).  
**Owner context:** `OWNER_NOTES.md` work-environment answers (local Python exists; stlite/WASM unverified; prefer local-first with hosted accommodation brief when required).

## Summary

Opened all mandated downstream artifacts and followed references to the three corrected dossiers. **Six files edited** where claims contradicted the 2026-09-04 verification tables; **seven artifacts checked with no edit** (claims already aligned or out of scope for these repos). **Two packaged work-bundle mirrors** flagged for the docx/packaging queue — not regenerated in this pass.

The largest downstream defect was a **false PAEM stlite rejection** propagated from an earlier dossier draft into R5 and B2. Portable-Alpha verification (54 claims, 13 corrected) established that `web/index.html` mounts the full Streamlit dashboard via stlite with vendored wheels; README line 19 disclaims support but does not negate the implementation. R5 §2.2 and B2 B2-035 incorrectly stated PAEM "explicitly rejects stlite" / "PAEM-incompatible deps." Those lines now match the dossier: local Python is the work-default; browser delivery remains unverified.

## Artifacts checked and disposition

### Edited

| Artifact | Section | Change |
|----------|---------|--------|
| `artifacts/dossiers/00-INDEX.md` | §1 fleet table, PAEM row | Primary surface adds **Browser/stlite (unverified)**; biggest gap adds stale README regime caveat. |
| `artifacts/dossiers/00-INDEX.md` | §1 fleet table, TPP row | Portal route corrected to `/portal/draft/new`; production-usable labeled **Yes (alpha)**; gaps add unwired security-model REST docs (verification §8). |
| `artifacts/research/R5-output-substrate.md` | §2.2 fleet repos table | PAEM row: replaced "explicitly rejects stlite" with stlite mount evidence + README disclaimer + work-unverified fit note. |
| `artifacts/research/R5-output-substrate.md` | §4.2 reject table | "PAEM-incompatible deps" → stlite entry exists but README-disclaimed and work-unprobed. |
| `artifacts/research/B2-gap-analysis.md` | Tier-4 adopt table B2-035 | Same PAEM stlite correction. |
| `artifacts/research/B2-gap-analysis.md` | §6 reject themes | "PAEM WASM rejection" → work-side WASM unproven. |
| `artifacts/research/C-skill-curriculum.md` | §1.1 learn-first; module 17 | PAEM static/offline wording aligned to stlite entry + portable zip; module 17 drops implied "Pyodide bundle" certainty. |

### Checked — no change required

| Artifact | Rationale |
|----------|-----------|
| `artifacts/dossiers/00-PERSONAL-REUSE-NOTE.md` | Pension-Data adoption steps (`entities/service.py` collision guard, evidence ledger) match corrected dossier §9–§11; no PAEM/TPP-specific claims. |
| `artifacts/skill-coverage/COVERAGE_MATRIX.md` | PAEM already lists `web/index.html` (bundled stlite/Pyodide) as CENTRAL — consistent with corrected dossier. |
| `artifacts/research/B3-interop-architecture.md` | Pension-Data supersession, entity merge, and partial `run-contract/v1` emission align with verification (61 CONFIRMED, 1 cite-drift, 1 UNVERIFIABLE). No PAEM/TPP sections required edits. |
| `artifacts/research/B7-PROGRAM-PLAN-v3.md` | Pension-Data issues (#879–#883), TPP #1513 local-first + accommodation brief, and D10 stlite-unverified decision match owner notes and dossiers. |
| `artifacts/issues/*` (Pension-Data, TPP, B5-wave) | Issue bodies cite surfaces and gaps consistent with verification; no stale PAEM stlite or TPP portal-route claims found. |
| `artifacts/research/R6-public-corpora-and-synthetic-data.md` | Pension-Data "1,382-test gate" (B2-043) matches executed `pytest -q` in verification. |
| `artifacts/research/R7-trip-planning-core.md` | "Live TPP disabled in trip-planner" remains accurate as integration posture; TPP HTTP contract and cross-repo smoke scaffolding confirmed in TPP verification. |

### Packaging queue (not edited)

| File | Stale content |
|------|----------------|
| `artifacts/work-bundle/Portable-Alpha-Extension-Model.md` | Pre-correction claims: ~1240 tests, content-addressed persistence, PNG-helper-only browser path. |
| `artifacts/work-bundle/Travel-Plan-Permission.md` | Portal route `/portal/requests/new` (actual: `/portal/draft/new`). |

Regenerate via existing `tools/md_to_docx.py` / work-bundle sync when the packaging unit runs.

## Per-repo verification carry-forward

**Pension-Data** (63 claims: 61 CONFIRMED, 1 cite-drift, 1 UNVERIFIABLE): Downstream already treats repo as sole conformant `run-contract/v1` emitter and **Partial** production-usable (API fixtures, desktop scaffold). No downstream contradicted the desktop Tauri correction (`src-tauri/src/main.rs` exists; `src-ui/` empty). Cite-drift on `run_one_pdf_pilot` lines 282–505 was dossier-only; no downstream cited the old 498 bound.

**Portable-Alpha-Extension-Model** (54 claims: 40 CONFIRMED, 13 WRONG corrected in dossier, 1 UNVERIFIABLE): Material corrections propagated to R5/B2/C-skill-curriculum. Not propagated to work-bundle mirror (queue). Other corrections (CSV-only index loader via `load_index_returns`; Run Logs reads `run.log`/`run_end.json` not `run.json`; sweep regimes implemented despite README; manifest hashes are path-keyed not content-addressed storage) are dossier-local — no downstream artifact asserted the refuted forms.

**Travel-Plan-Permission** (54 claims: 44 CONFIRMED, 9 WRONG corrected in dossier, 1 UNVERIFIABLE): Index row updated for portal route and alpha status. Expense-report schema "contract only, not Python-consumed" and orchestration-plan "long-term goal" framing were already correct in dossier; no downstream file repeated the refuted `/portal/requests/new` path except work-bundle mirror (queued).

## Still-unverified claims (preserved)

1. **Pension-Data:** PPD and EDGAR live HTTP endpoints (sandbox off-network) — fixture/cache paths only verified.
2. **PAEM:** Current pytest collection count, measured coverage, and CI runtime outcomes — historical `COVERAGE_GAPS.md` (2025-01-27) cited; configured 60% floor and gate jobs confirmed in source only.
3. **PAEM:** stlite dashboard end-to-end usability at work — owner notes mark WASM/stlite UNKNOWN; probe still required (B7 D10, Deliverable-Render #4).
4. **TPP:** Live end-to-end cross-repo smoke with running `trip-planner` services — contract fixtures and CI scaffolding verified; runtime pairing UNVERIFIABLE off-clone.

## Confidence

**High** that the PAEM stlite downstream contradiction was real and is now fixed — the verification table row 29 and dossier §8 explicitly refute "PNG helper only" / "rejects stlite," and R5/B2 repeated that false claim verbatim.

**High** that Pension-Data and TPP downstream artifacts required no substantive edits beyond the index TPP row — spot-checked B3, B7, R6, issue bodies against verification tables.

**Medium** on completeness of work-bundle staleness — only the two mirrors with grep-visible contradictions were flagged; full work-bundle resync was out of scope for this bounded pass.

What would change this conclusion: if `artifacts/work-bundle/*.md` are considered in-scope deliverables rather than packaging queue, they need immediate regeneration from the corrected dossiers.


### Packaging follow-up — 2026-09-04 23:38 UTC

The stale Markdown/Word packaging flags are resolved by the [verified export refresh](export-refresh-20260904.md). Seven Word destinations and three Work-bundle Markdown copies now include the corrected evidence.
