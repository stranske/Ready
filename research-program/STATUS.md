# Research Program 2026-09 — STATUS (generated 2026-09-04T17:58:41Z)

Units: 32 — claimed 4, done 24, queued 4
Paused: False   Phase stops: []
Capacity (Orchestrator): codex=ok claude=ok cursor=ok gemini=shed vibe=ok aider=ok
CLAUDE CONSERVATION ACTIVE until 2026-09-06T12:00:00Z — cheap agents only (launchd driver every 15 min); claude-only units deferred.
Owner inbox: https://github.com/stranske/Ready/issues/553

| id | track | phase | status | agent | executor | title |
|---|---|---|---|---|---|---|
| A-verify-Trend_Model_Project | A | A1 | claimed | cursor | driver | Verify dossier artifacts/dossiers/Trend_Model_Project.md against ../cl |
| A-verify-Workflows | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/Workflows.md against ../clones/Workf |
| A-verify-learning-management-system | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/learning-management-system.md agains |
| A-verify-Collab-Admin | A | A1 | done | codex | claude | Verify dossier artifacts/dossiers/Collab-Admin.md against ../clones/Co |
| A-verify-Counter_Risk | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Counter_Risk.md against ../clones/Co |
| A-verify-Fine-Art-Archive | A | A1 | done | gemini | codex | Verify dossier artifacts/dossiers/Fine-Art-Archive.md against ../clone |
| A-verify-Inv-Man-Intake | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Inv-Man-Intake.md against ../clones/ |
| A-verify-Manager-Database | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Manager-Database.md against ../clone |
| A-verify-Orchestrator | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Orchestrator.md against ../clones/Or |
| A-verify-Pension-Data | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Pension-Data.md against ../clones/Pe |
| A-verify-Portable-Alpha-Extension-Model | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Portable-Alpha-Extension-Model.md ag |
| A-verify-Template | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Template.md against ../clones/Templa |
| A-verify-Travel-Plan-Permission | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Travel-Plan-Permission.md against .. |
| A-verify-trip-planner | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/trip-planner.md against ../clones/tr |
| A-dossier-index | A | A2 | done | cursor | driver | Fleet index and shared vocabulary from verified dossiers (needs >=12 v |
| A-personal-reuse-note | A | A2 | done | cursor | driver | Reuse note across personal repos (FAA, Reader, trip-planner) |
| A-work-side-bundle | A | A3 | done | cursor | driver | Work-side bundle: redaction pass, cover memo, safety grep |
| A-work-side-bundle-refresh | A | A3 | queued | codex |  | Refresh the work-side bundle with the three late dossiers and re-run t |
| A-dossier-docx | A | A3 | claimed | cursor | driver | Word versions of all verified dossiers (venv + python-docx) |
| B1-citefix-R1-legal-decomposition | B | B1 | done | cursor | driver | Fix unreachable citations in R1-legal-decomposition.md |
| B1-citefix-R4-document-access-substrate | B | B1 | done | cursor | driver | Fix unreachable citations in R4-document-access-substrate.md |
| R1-legal-decomposition | B | B1 | done | codex | driver | Brief R1: legal fund-document decomposition and lineage |
| R2-consultant-report-diffing | B | B1 | done | codex | driver | Brief R2: consultant-report and periodic-communication diffing |
| R3-manager-mosaic | B | B1 | done | codex | driver | Brief R3: manager mosaic synthesis, discrepancy and thesis monitoring |
| R4-document-access | B | B1 | done | codex | driver | Brief R4: Backstop/MCP/SharePoint mirror substrate (adversarial) |
| R5-output-substrate | B | B1 | done | cursor | driver | Brief R5: robust no-install output surfaces |
| R6-public-corpora | B | B1 | claimed | cursor | driver | Brief R6: public and synthetic corpora |
| R7-trip-planning-core | B | B1 | claimed | codex | driver | Brief R7: trip-planning core (transport, lodging, constraints) |
| B2-gap-analysis | B | B2 | queued | codex |  | Gap analysis and disposition of all candidates |
| B3-interop-architecture | B | B3 | queued | codex |  | Interoperability architecture (identity, typology, tracked variables,  |
| B4-issue-drafting | B | B4 | queued | codex |  | Draft AGENT_ISSUE_FORMAT issue bodies from decisions |
| C-skill-curriculum | C | C1 | done | codex | driver | Skill curriculum + tool-literacy loop design (LMS-connected) |

## Last checkpoints

- 2026-09-04T17:55:29Z — A-verify-learning-management-system — claimed by driver (agent cursor)
- 2026-09-04T17:55:30Z — B1-citefix-R4-document-access-substrate — route — router picked cursor from ['codex', 'cursor', 'gemini']
- 2026-09-04T17:55:30Z — B1-citefix-R4-document-access-substrate — claimed by driver (agent cursor)
- 2026-09-04T17:56:44Z — R6-public-corpora — route — router picked cursor from ['codex', 'cursor']
- 2026-09-04T17:56:44Z — R6-public-corpora — claimed by driver (agent cursor)
- 2026-09-04T17:57:25Z — A-verify-learning-management-system — done — cursor produced 1634 words at artifacts/dossiers/learning-management-system.md in 116s
- 2026-09-04T17:57:28Z — R7-trip-planning-core — route — router picked codex from ['codex', 'gemini']
- 2026-09-04T17:57:28Z — R7-trip-planning-core — claimed by driver (agent codex)
- 2026-09-04T17:58:00Z — B1-citefix-R4-document-access-substrate — done — cursor produced 2545 words at artifacts/research/R4-document-access-substrate.md in 150s
- 2026-09-04T17:58:02Z — A-dossier-docx — route — router picked cursor from ['codex', 'cursor']
- 2026-09-04T17:58:02Z — A-dossier-docx — claimed by driver (agent cursor)
- 2026-09-04T17:58:41Z — A-verify-Workflows — done — cursor produced 1681 words at artifacts/dossiers/Workflows.md in 192s
