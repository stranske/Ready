Scorecard: 5 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes (headless ingest → thresholds → performance → queue artifact → export, via staged bundle tests and CLI score probes); surfaces unscored 0; closed-still-broken 0.

# Audit report — stranske/Inv-Man-Intake — 2026-11-02

**Tip:** `2960e93cb0a1c1e1cb2917dcbd0e13e651ee62b5`  
**Trigger:** Track D refill — scorecard dated 2026-10-02 (>30 days); open agent-ready supply 1/0 last filed set (`artifacts/audit-refill.md`).  
**Issues filed:** 1 — [#1061](https://github.com/stranske/Inv-Man-Intake/issues/1061) (headless runbook quickstart documents a failing command).

## Run summary

One commit landed since the prior scorecard (`2960e93` syncs `LABELS.md` from Workflows). Exact-tip CI succeeded (run `41179599679`, including the dedicated static SPA Playwright job). Core function probes matched the October scorecard: intake-through-export wiring is green on focused acceptance tests (68), headless pipeline regressions (110), and evidence-backed scoring plus varying-input CLI score tests (52 selected). Local Playwright browser scenarios were skipped in this session (module-level skip without `STATIC_SPA_E2E`); CI remains authoritative for the static operator surface.

## Scorecard detail

| id | Core function | Verdict | Evidence |
|---|---|---|---|
| IMI-1 | Ingest package → registered run + artifacts | WORKS | `tests/test_v1_acceptance_smoke.py`, staged `run_pipeline` via `stage_headless_reference_bundle` |
| IMI-2 | Extract fields with provenance | WORKS | Acceptance smoke asserts page/snippet/confidence on mixed PDF corpus |
| IMI-3 | Threshold escalation summary | WORKS | Same smoke + threshold decision assertions |
| IMI-4 | Normalize workbook performance | WORKS | Smoke metrics + `test_ingest_score_workbook_change_changes_performance_component` |
| IMI-5 | Priority score + explainability | PARTIAL | Production path emits `final_score: null` when evidence insufficient (by design); smoke headline score remains fixture-only; component derivation tests pass |
| IMI-6 | Validation queue handoff | PARTIAL | `validation-queue.json` emitted and API tests pass; persistence is local handoff not hosted queue |
| IMI-7 | Export named artifacts + manifest | WORKS | `tests/run/test_manifest.py` + manifest hashes on staged ingest |

**Primary journey:** passes at the CLI/API layer exercised above; static browser journey not re-driven locally (CI green).

**Surface inventory:** `inv-man-ingest`, `app/index.html` — unchanged from 2026-09-24 inventory; unscored 0.

## Verified finding filed

**Runbook quickstart vs production byte resolution.** `docs/runbooks/headless_ingest.md:15-18` instructs operators to run ingest against `tests/fixtures/intake/pdf_primary_mixed_bundle.json`, but `run_pipeline` loads bytes from the bundle directory only (`src/inv_man_intake/run.py:179`), while fixture bytes live in `tests/fixtures/extraction/` (`tests/conftest.py:47-49`). Reproduction fails with `real document bytes not found` — filed as #1061.

## Dedup and continuity

- **#1017** (open): primary-only / reorder ingest — `test_ingest_primary_only_pdf_and_pptx` now passes; issue appears stale but was not refuted (still open, not a closed dedup drop).
- **#693** (closed): credit-only production scoring — prior rounds REFUTED; evidence-backed scoring tests remain green.
- **#948** (closed): ontology vocabulary — owner decision; not duplicated.

## Dimension notes (abbreviated)

No new wiring or correctness defect beyond the runbook operator trap. Duplication/consolidation, public-field, and tooling passes deferred with no candidate above verification bar except the documented quickstart failure.

## Artifacts

- Canonical scorecard: `Code/Audits/Inv-Man-Intake/2026-11-02-SCORECARD.md`
- Audit run: `Code/Audits/Inv-Man-Intake/2026-11-02-audit-run.md`
- Issue body archive: unit `issue-bodies/01-headless-runbook-quickstart.md`
