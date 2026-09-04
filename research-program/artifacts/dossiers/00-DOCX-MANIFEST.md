# DOCX Conversion Manifest

*Generated 2026-09-04T18:10:25Z*

The 14 dossier names also occur in `artifacts/work-bundle/`; that bundle is
the final, redacted source for those same-name Word outputs. `00-INDEX` and
`00-PERSONAL-REUSE-NOTE` come from `artifacts/dossiers/`.

| File | KB | Headings | Tables | Status |
|------|-----|----------|--------|--------|
| 00-COVER-MEMO.docx | 39.7 | 9 | 2 | FAIL |
| 00-INDEX.docx | 41.1 | 17 | 4 | PASS |
| 00-PERSONAL-REUSE-NOTE.docx | 42.3 | 22 | 1 | PASS |
| Collab-Admin.docx | 43.0 | 13 | 3 | PASS |
| Counter_Risk.docx | 47.0 | 13 | 3 | PASS |
| Fine-Art-Archive.docx | 42.3 | 13 | 3 | PASS |
| Inv-Man-Intake.docx | 43.5 | 13 | 2 | PASS |
| Manager-Database.docx | 44.7 | 13 | 1 | PASS |
| Orchestrator.docx | 46.4 | 13 | 1 | PASS |
| Pension-Data.docx | 44.6 | 13 | 1 | PASS |
| Portable-Alpha-Extension-Model.docx | 46.6 | 13 | 3 | PASS |
| README.docx | 37.7 | 7 | 6 | FAIL |
| REDACTIONS.docx | 37.1 | 1 | 0 | FAIL |
| Template.docx | 42.7 | 13 | 2 | PASS |
| Travel-Plan-Permission.docx | 46.0 | 13 | 3 | PASS |
| Trend_Model_Project.docx | 43.9 | 13 | 1 | PASS |
| Workflows.docx | 45.9 | 17 | 1 | PASS |
| learning-management-system.docx | 42.7 | 13 | 2 | PASS |
| trip-planner.docx | 44.0 | 16 | 1 | PASS |

**Summary:** 16/19 PASS. The three failures are faithful conversions whose
source Markdown does not itself meet the required structural thresholds:
`00-COVER-MEMO` has 38 paragraphs and 9 headings, `README` has 14 paragraphs
and 7 headings, and `REDACTIONS` has one heading. All 19 documents reopen and
their Word-table counts exactly match their Markdown-table counts.
