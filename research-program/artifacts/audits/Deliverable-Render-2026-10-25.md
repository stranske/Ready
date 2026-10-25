Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0.

REFUTED: https://github.com/stranske/Deliverable-Render/issues/89 — native `locator.page` / `document_ref.page` conflicts fail validation (`evidence-page-conflict`) and block all three public renderers before publication on live tip `57d443c`.

# Deliverable-Render Audit Report — 2026-10-25

**Tip:** `57d443ccef620252b005d6e96e33a80c0761445b` on `main`  
**Host Environment:** macOS Darwin, Python 3.12 (`/opt/anaconda3` + clean isolated virtualenv in `$TMPDIR`)  
**Scope:** Repository-owned `src/`, `tests/`, `README.md`, `docs/contracts/`. Excluded `.github/` workflow templates and synced scripts (managed upstream by `stranske/Workflows` per `AGENTS.md`) except for CI verification and issue format alignment. Dossier and verification table files were absent.

## Executive Summary & Critical Evaluation

This Track D audit was triggered because the canonical scorecard for `stranske/Deliverable-Render` was recorded as 31 days old (`2026-09-24`). An earlier execution today (`D-audit-Deliverable-Render--2026-10-25T08-11-07Z`) completed an audit run but refrained from writing to `[LOCAL_HOME]/Library/CloudStorage/Dropbox/Learning/Code/Audits/Deliverable-Render/2026-10-25-SCORECARD.md` under the mistaken assumption that `Code/Audits` was inside the protected program workspace rather than the external canonical audit repository. Consequently, `program.py`'s `refill_trigger_for` continued to observe `2026-09-24-SCORECARD.md` as newest and re-queued the audit.

We have now executed the complete multi-dimensional audit and product scorecard, verified all 7 core functions with live isolated data and varying-input diffs, updated the canonical scorecard and audit ledger, and cleared the staleness trigger.

On the merits of the codebase:
- The core deliverable pipeline is robust and healthy. All 353 test cases pass with 91.24% branch coverage, and Ruff linting is clean.
- The primary user journey (`validate-structured-store` -> `render-html-hub`, `render-pptx-deck`, `render-docx-memo`) passes without manual intervention. Output contents respond faithfully to input modifications.
- The open issue #89 claiming contradictory native page anchors are accepted without flagging is REFUTED on the current tip: `_validate_native_page_agreement` in `src/deliverable_render/store/validate.py:113-123` rejects contradictory anchors with `evidence-page-conflict` and `communication.py:64-84` blocks publication.
- Open issue #104 (Python 3.13/3.14 migration) is already tracked and active, with PR #107 open and passing checks.
- Zero new defects or filable issues were identified.

## 1. Product Scorecard

| ID | Core Function | Result | Live Exercise & Varying-Input Verification |
| --- | --- | --- | --- |
| CF1 | An operator can validate a communication-synthesis store | WORKS | `validate-structured-store tests/fixtures/stores/communication_render.json` returned exit 0 (`structured store valid`). Semantic rejection verified on `orphan_entry_id.json` and contradictory native page fixtures. |
| CF2 | A developer can render a deep-linked offline HTML hub | WORKS | `render-html-hub` rendered `hub_alpha.html`. Varying mention text from `"Capital of $36B"` to `"Assets under management grew to $750M"` produced `hub_beta.html`; verified exact diff in rendered HTML table rows. |
| CF3 | A developer can build a manifest-gated PPTX deck | WORKS | `render-pptx-deck` rendered `deck_alpha.pptx` with `communication_deck.json` manifest. Varying mention text confirmed in re-read slide shape text. `--strict` correctly blocks incomplete manifests. |
| CF4 | An operator can render consultant memos | WORKS | `render-docx-memo --profile communication-synthesis` generated valid 36,715-byte `.docx` document. |
| CF5 | An operator can run offline capability probes | WORKS | `deliverable_render.probe.build_probe` generated 9,862-character valid offline HTML probe. All 10 tests in `test_probe_offline_and_minimal.py` passed. |
| CF6 | Validated store renders to HTML, PPTX, and DOCX without translation | WORKS | Interoperability verified: `hub.html`, `deck.pptx`, and `memo.docx` all rendered directly from `communication_render.json` without conversion. |
| CF7 | Invalid memo tiers and rendering seams are rejected before publication | WORKS | `render-docx-memo` with `T99_INVALID` rejected before output creation (exit 2). Conflicting native page anchors rejected with `evidence-page-conflict`. |

**Primary User Journey:** Structured store validation -> offline HTML hub + PPTX deck + DOCX memo. **Status:** PASSES.

## 2. Dedup & Issue Refutations

- **Open Issue #89:** *"Reject conflicting native evidence page anchors before rendering"*  
  **Status: REFUTED.**  
  Issue #89 asserted that `locator.page=0` and `document_ref.page=9` validate without error and publish misleading links. On live tip `57d443c`, `_validate_native_page_agreement` in `src/deliverable_render/store/validate.py:113-123` raises `EvidencePageConflictError`, reporting `evidence-page-conflict /entries/0/mentions/0/src/locator/page: locator.page=0 conflicts with document_ref.page=9`. Furthermore, `src/deliverable_render/store/communication.py:64-84` raises `CommunicationRenderError` before any output is created. Regression test `test_native_pages_validation_cli_reports_conflicting_pointer` in `tests/store/test_evidence_object_projection.py` covers this behavior.
- **Open Issue #104:** *"[P2] CI still tests Python 3.12"*  
  **Status: ALREADY TRACKED.**  
  Active PR #107 (`ci: adopt Python 3.13/3.14 modern standard`) was opened 1 hour ago and is currently passing CI checks.
- **Closed Issues #27, #28, #31, #32, #36, #37, #40, #41, #47:**  
  Re-checked all closed seams: cross-entry mention IDs, missing publication detail/state, missing entry periods, zero-page conversions, duplicate document IDs, unknown memo tiers, and empty renderable text. All corresponding tests pass on current tip; no regressions found.

## 3. Eight-Dimension Analysis

- **D1 Code Quality:** Clean codebase. 353 unit and integration tests passed in 5.47s in an isolated Python 3.12 virtual environment. Branch coverage is 91.24% (exceeding 80% threshold). `ruff check src tests` reports zero diagnostics.
- **D2 Duplication:** Modular separation between CLI entrypoints, output formatters (`html.py`, `pptx/manifest.py`, `docx/memo.py`), and store adapter logic.
- **D3 Wiring & Output Correctness:** Data flow from raw JSON -> validator (`validate.py`) -> adapter (`communication.py`) -> renderers verified with varying inputs. Output text accurately reflects store inputs.
- **D4 Operator UX:** No browser GUI exists. Per standing direction, all 4 public CLI surfaces (`validate-structured-store`, `render-html-hub`, `render-pptx-deck`, `render-docx-memo`) were driven and verified with `--help` and live runs.
- **D5 Approach vs. Public Field:** Architecture conforms to the constrained enterprise environment documented in `docs/TARGET_WORK_ENVIRONMENT.md` (offline static HTML, zero-dependency client viewing, COM-free fallback generation).
- **D6 Missed Opportunities:** None of actionable two-week scope. Feature set completely covers the communication-synthesis store specification.
- **D7 Tools Worth Integrating:** No additional external dependencies warranted.
- **D8 Local Skills & Automations:** GitHub Actions CI is green at exact head `57d443c`. Format guard and keeper workflows are functioning as expected.

## 4. Continuity & Artifact Storage

- **OUT File:** `artifacts/audits/Deliverable-Render-2026-10-25.md`
- **Unit Checkpoint:** `artifacts/audits/D-audit-Deliverable-Render--2026-10-25T20-34-21Z.CHECKPOINT.md`
- **Global Checkpoint:** `artifacts/audits/CHECKPOINT.md`
- **Canonical Scorecard:** `Code/Audits/Deliverable-Render/2026-10-25-SCORECARD.md`
- **Canonical Run Log:** `Code/Audits/Deliverable-Render/2026-10-25-audit-run.md`
- **Audit Ledger:** Updated `Code/Audits/AUDIT_LEDGER.md` (top entry) and `Code/Audits/Deliverable-Render/README.md`.
- **Engine Trigger Status:** `program.refill_trigger_for("Deliverable-Render")` evaluated live: `(False, 'scorecard 2026-10-25 healthy (0B/0F, debt 0, 0d old)')`. Staleness resolved.

## 5. Confidence & Falsification Conditions

- **Confidence:** High.
- **What would change our mind:**
  1. Discovery of an unhandled edge case in store validation where conflicting document IDs or malformed monetary strings silently pass into output generation.
  2. Failure of the generated offline HTML hub or PowerPoint deck to open correctly in Microsoft Office or restricted enterprise browsers on the target platform.
  3. Failure of the Python 3.13/3.14 migration in PR #107 due to incompatible C-extensions or bytecode changes in upstream dependencies (`python-docx`, `python-pptx`, `lxml`).
