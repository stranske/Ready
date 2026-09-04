# Work-Environment Issue Wave — B5 Filing Report

**Filed:** 2026-09-04  
**Source:** [INFORMATION-REQUEST-RESPONSE.md](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)  
**Dedup:** Checked open/recent issues in each target repo; no duplicates filed against wave-1 issues (#2–#4 Doc-Lineage, #2–#4 Deliverable-Render, #3368 Workflows).

## Summary

| # | Repo | Issue | Response section |
|---|------|-------|------------------|
| 1 | Doc-Lineage | [#5 — Lineage and comparison engine](https://github.com/stranske/Doc-Lineage/issues/5) | §D consultant-report comparison tool (segment vocabulary, T1/T2/T3 tiers); §D communication synthesis tool (silence-is-weak-evidence); §C Q9 (supersession); Appendix item 2 (shared extraction context) |
| 2 | Deliverable-Render | [#5 — Word memo renderer](https://github.com/stranske/Deliverable-Render/issues/5) | §D consultant-report comparison tool (Word memos: change, continuity, cross-consultant) |
| 3 | Deliverable-Render | [#6 — Structured-store validator + evidence alignment](https://github.com/stranske/Deliverable-Render/issues/6) | §D communication synthesis tool (orphan ID vanish, `$36B`→`B` shell-substitution); Appendix items 1 & 3 (shared record/evidence format) |
| 4 | Inv-Man-Intake | [#947 — Doc-Lineage #3 extraction adapter](https://github.com/stranske/Inv-Man-Intake/issues/947) | Appendix item 2 (one shared PDF extraction library); depends on [Doc-Lineage #3](https://github.com/stranske/Doc-Lineage/issues/3) |
| 5 | Pension-Data | [#878 — Doc-Lineage #3 extraction adapter](https://github.com/stranske/Pension-Data/issues/878) | Appendix item 2; §C Q8 (mandatory OCR for scanned legal PDFs); depends on [Doc-Lineage #3](https://github.com/stranske/Doc-Lineage/issues/3) |
| 6 | Travel-Plan-Permission | [#1513 — Local-first delivery shape](https://github.com/stranske/Travel-Plan-Permission/issues/1513) | §F item 17 (travel policy engine blocked: no server-hosted apps in target environment); §A Q3 (local-file deep links) |
| 7 | learning-management-system | [#580 — Local-first delivery shape](https://github.com/stranske/learning-management-system/issues/580) | §F item 17 (learning platform blocked: internal web service + database); §A Q1 (local Python) |
| 8 | Workflows | [#3370 — Consumer template target work-environment note](https://github.com/stranske/Workflows/issues/3370) | §A Q1 (runtime inventory); §A Q3 (local-file links); §F item 17 (hosting block); §E Q15 (delivery today) |

## Body files

All bodies written under `artifacts/issues/B5-wave/`:

- `Doc-Lineage-05-lineage-comparison-engine.md`
- `Deliverable-Render-05-word-memo-renderer.md`
- `Deliverable-Render-06-store-validation-and-evidence-alignment.md`
- `Inv-Man-Intake-05-doc-lineage-extraction-adapter.md`
- `Pension-Data-08-doc-lineage-extraction-adapter.md`
- `Travel-Plan-Permission-09-local-first-delivery.md`
- `learning-management-system-09-local-first-delivery.md`
- `Workflows-06-target-work-environment-template.md`

## Intake log

Eight entries appended to `/Users/teacher/.codex/orchestrator/measurement/intake-2026-09-04.log` in `repo|body-file|url` form.

## Not filed (per instructions)

- stranske/Orchestrator — excluded
- Wave-1 duplicates — Doc-Lineage #2–#4, Deliverable-Render #2–#4, Workflows #3368

## Format status (post-file)

Six issues were auto-reformatted by the fleet optimizer and carry `agents:formatted`: Deliverable-Render #5–#6, Inv-Man-Intake #947, Pension-Data #878, Travel-Plan-Permission #1513, learning-management-system #580.

Two issues still fail the format validator on the generic "Perform deliberate-break verification" task line and retain `agents:format`: Doc-Lineage #5, Workflows #3370. The optimizer rewrote the deliberate-break task in the other six to name a concrete file (e.g. `src/deliverable_render/docx/memo.py`); those two need the same one-line task fix before agents can pick them up.

## Checkpoint

Resume state recorded in `artifacts/issues/B5-work-env-issue-wave.CHECKPOINT.md`.
