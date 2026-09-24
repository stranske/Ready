Scorecard: 3 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 3; journey: passes; surfaces unscored 0; closed-still-broken 0.

# Pension-Data Track D audit — 2026-09-23 (attempt 2)

Audited `stranske/Pension-Data` `main` at `388a06a4194f7863a1cbc6e231d7bfe07ef8fcbf` (three commits since the morning scorecard at `33a29aa`: staging API wiring #4a1bd20, replay corpus #913, Doc-Lineage variable staging #885). CI green on the tip push.

REFUTED: https://github.com/stranske/Pension-Data/issues/914 — exact reproduction without `PENSION_DATA_QUERY_ARTIFACT_ROOT` now returns HTTP 503, not fixture `CA-PERS`/`0.81`; with artifact root set, `test_metric_history_serves_pilot_staging_not_hardcoded_fixture` behavior holds (`SYN-PLAN` `0.784` vs `CA-PERS` `0.768`).

## Product scorecard

| Core function | Result | Evidence |
| --- | --- | --- |
| F1 — PDF pilot → staged artifacts | WORKS | `tests/ops/test_one_pdf_pilot_cli.py` (8/8); synthetic vs CalPERS excerpt funded ratios differ (`0.784` vs `0.768`). |
| F2 — plan analytics keyed by entity | WORKS | `tests/api/test_app_serving.py::test_metric_history_serves_pilot_staging_not_hardcoded_fixture`; live two-run probe with `PENSION_DATA_QUERY_ARTIFACT_ROOT` returns distinct funded ratios per plan. |
| F3 — workspace bundle with provenance | WORKS | `tests/export/test_workspace_bundle.py` + `tests/web/test_build_workspace_bundle.py` (10/10). |

Primary journey (pilot → staged facts → analytics → bundle) completes when the serve path sets `PENSION_DATA_QUERY_ARTIFACT_ROOT` to the pilot output root. Following `README.md` proprietary `pension-data-serve` alone still yields **503** on analytics routes; that operator-doc gap is filed as [#918](https://github.com/stranske/Pension-Data/issues/918), not a core-function code regression.

OpenAPI surface inventory unchanged (7 paths); Doc-Lineage staging import and replay corpus manifest are interior capabilities with passing tests (`tests/staging/test_doc_lineage_import.py`, `tests/replay/test_corpus_manifest_wiring.py`).

## Dimension sweep (abbreviated)

1–3: No new verified code defects beyond the doc/contract drift above; #914 fix verified on tip.  
4: Static web path unchanged; bundle-only review remains `serve_local` with empty `apiBaseUrl`.  
5–8: No filable gaps this round (replay corpus wiring matches pinned Doc-Lineage revision in `config/replay_corpus_manifest.json`).

## Issues

| Action | Issue |
| --- | --- |
| Filed | [#918](https://github.com/stranske/Pension-Data/issues/918) — operator docs omit `PENSION_DATA_QUERY_ARTIFACT_ROOT` |
| Already open (dedup) | [#915](https://github.com/stranske/Pension-Data/issues/915) — stale `run-contract-v1.md` emitter claim |
| Closed verified | [#914](https://github.com/stranske/Pension-Data/issues/914) — API staging wiring (refuted on tip as still broken) |

Focused regression selection: **42/42** passed (`tests/api/*`, pilot CLI, workspace export/build, doc-lineage staging, replay corpus).

Agents Issue Format Guard for #918: run `35936550851` concluded **skipped** (same pattern as #914/#915 this morning); `priority:normal` present, `agents:formatted` not yet applied.

Canonical continuity: `Code/Audits/Pension-Data/2026-09-23-SCORECARD.md`, `2026-09-23-audit-run.md`.

Issues filed: 1 ([#918](https://github.com/stranske/Pension-Data/issues/918)).
