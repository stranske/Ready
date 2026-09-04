# Research Program 2026-09 — STATUS (generated 2026-09-04T17:50:43Z)

Units: 31 — done 24, queued 7
Paused: False   Phase stops: []
Capacity (Orchestrator): codex=ok claude=ok cursor=ok gemini=shed vibe=ok aider=ok
CLAUDE CONSERVATION ACTIVE until 2026-09-06T12:00:00Z — cheap agents only (launchd driver every 15 min); claude-only units deferred.
Owner inbox: https://github.com/stranske/Ready/issues/553

| id | track | phase | status | agent | executor | title |
|---|---|---|---|---|---|---|
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
| A-verify-Trend_Model_Project | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Trend_Model_Project.md against ../cl |
| A-verify-Workflows | A | A1 | done | codex | driver | Verify dossier artifacts/dossiers/Workflows.md against ../clones/Workf |
| A-verify-learning-management-system | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/learning-management-system.md agains |
| A-verify-trip-planner | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/trip-planner.md against ../clones/tr |
| A-dossier-index | A | A2 | done | cursor | driver | Fleet index and shared vocabulary from verified dossiers (needs >=12 v |
| A-personal-reuse-note | A | A2 | done | cursor | driver | Reuse note across personal repos (FAA, Reader, trip-planner) |
| A-work-side-bundle | A | A3 | done | cursor | driver | Work-side bundle: redaction pass, cover memo, safety grep |
| A-dossier-docx | A | A3 | queued | cursor |  | Word versions of all verified dossiers (venv + python-docx) |
| B1-citefix-R1-legal-decomposition | B | B1 | done | cursor | driver | Fix unreachable citations in R1-legal-decomposition.md |
| B1-citefix-R4-document-access-substrate | B | B1 | queued | codex |  | Fix unreachable citations in R4-document-access-substrate.md |
| R1-legal-decomposition | B | B1 | done | codex | driver | Brief R1: legal fund-document decomposition and lineage |
| R2-consultant-report-diffing | B | B1 | done | codex | driver | Brief R2: consultant-report and periodic-communication diffing |
| R3-manager-mosaic | B | B1 | done | codex | driver | Brief R3: manager mosaic synthesis, discrepancy and thesis monitoring |
| R4-document-access | B | B1 | done | codex | driver | Brief R4: Backstop/MCP/SharePoint mirror substrate (adversarial) |
| R5-output-substrate | B | B1 | done | cursor | driver | Brief R5: robust no-install output surfaces |
| R6-public-corpora | B | B1 | queued | cursor |  | Brief R6: public and synthetic corpora |
| R7-trip-planning-core | B | B1 | queued | codex |  | Brief R7: trip-planning core (transport, lodging, constraints) |
| B2-gap-analysis | B | B2 | queued | codex |  | Gap analysis and disposition of all candidates |
| B3-interop-architecture | B | B3 | queued | codex |  | Interoperability architecture (identity, typology, tracked variables,  |
| B4-issue-drafting | B | B4 | queued | codex |  | Draft AGENT_ISSUE_FORMAT issue bodies from decisions |
| C-skill-curriculum | C | C1 | done | codex | driver | Skill curriculum + tool-literacy loop design (LMS-connected) |

## Last checkpoints

- 2026-09-04T17:46:26Z — C-skill-curriculum — fail — cursor produced 0 words at /Users/teacher/.codex/automations/research-program/artifacts/research/C-skill-curriculum.md (min 400); rotating agent
- 2026-09-04T17:46:26Z — C-skill-curriculum — route — router picked codex from ['codex', 'gemini']
- 2026-09-04T17:46:26Z — C-skill-curriculum — claimed by driver (agent codex)
- 2026-09-04T17:46:52Z — citations — enqueued B1-citefix-R1-legal-decomposition
- 2026-09-04T17:46:52Z — citations — enqueued B1-citefix-R4-document-access-substrate
- 2026-09-04T17:47:30Z — A-personal-reuse-note — done — cursor produced 1387 words at artifacts/dossiers/00-PERSONAL-REUSE-NOTE.md in 66s
- 2026-09-04T17:47:35Z — B1-citefix-R1-legal-decomposition — route — router picked cursor from ['codex', 'cursor', 'gemini']
- 2026-09-04T17:47:35Z — B1-citefix-R1-legal-decomposition — claimed by driver (agent cursor)
- 2026-09-04T17:47:53Z — C-skill-curriculum — done — cursor produced 2785 words at artifacts/research/C-skill-curriculum.md in 86s
- 2026-09-04T17:48:18Z — R5-output-substrate — done — cursor produced 2355 words at artifacts/research/R5-output-substrate.md in 114s
- 2026-09-04T17:49:08Z — A-work-side-bundle — done — cursor produced 421 words at artifacts/work-bundle/00-RUN-REPORT.md in 165s
- 2026-09-04T17:50:43Z — B1-citefix-R1-legal-decomposition — done — cursor produced 2188 words at artifacts/research/R1-legal-decomposition.md in 187s
