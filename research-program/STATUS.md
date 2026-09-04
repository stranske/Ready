# Research Program 2026-09 — STATUS (generated 2026-09-04T17:11:39Z)

Units: 28 — claimed 1, done 2, queued 25
Paused: False   Phase stops: []
Capacity (Orchestrator): codex=ok claude=ok cursor=ok gemini=ok vibe=ok aider=ok
CLAUDE CONSERVATION ACTIVE until 2026-09-06T12:00:00Z — cheap agents only (launchd driver every 15 min); claude-only units deferred.
Owner inbox: https://github.com/stranske/Ready/issues/553

| id | track | phase | status | agent | executor | title |
|---|---|---|---|---|---|---|
| A-verify-Collab-Admin | A | A1 | done | codex | claude | Verify dossier artifacts/dossiers/Collab-Admin.md against ../clones/Co |
| A-verify-Counter_Risk | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Counter_Risk.md against ../clones/Co |
| A-verify-Fine-Art-Archive | A | A1 | claimed | gemini | codex | Verify dossier artifacts/dossiers/Fine-Art-Archive.md against ../clone |
| A-verify-Inv-Man-Intake | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Inv-Man-Intake.md against ../clones/ |
| A-verify-Manager-Database | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Manager-Database.md against ../clone |
| A-verify-Orchestrator | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Orchestrator.md against ../clones/Or |
| A-verify-Pension-Data | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Pension-Data.md against ../clones/Pe |
| A-verify-Portable-Alpha-Extension-Model | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Portable-Alpha-Extension-Model.md ag |
| A-verify-Template | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Template.md against ../clones/Templa |
| A-verify-Travel-Plan-Permission | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Travel-Plan-Permission.md against .. |
| A-verify-Trend_Model_Project | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Trend_Model_Project.md against ../cl |
| A-verify-Workflows | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/Workflows.md against ../clones/Workf |
| A-verify-learning-management-system | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/learning-management-system.md agains |
| A-verify-trip-planner | A | A1 | queued | codex |  | Verify dossier artifacts/dossiers/trip-planner.md against ../clones/tr |
| A-dossier-index | A | A2 | queued | codex |  | Fleet index and shared vocabulary from verified dossiers (needs >=12 v |
| A-personal-reuse-note | A | A2 | queued | cursor |  | Reuse note across personal repos (FAA, Reader, trip-planner) |
| A-dossier-docx | A | A3 | queued | claude |  | Word versions of all dossiers (Claude executor: use the docx skill) |
| R1-legal-decomposition | B | B1 | queued | codex |  | Brief R1: legal fund-document decomposition and lineage |
| R2-consultant-report-diffing | B | B1 | queued | codex |  | Brief R2: consultant-report and periodic-communication diffing |
| R3-manager-mosaic | B | B1 | queued | codex |  | Brief R3: manager mosaic synthesis, discrepancy and thesis monitoring |
| R4-document-access | B | B1 | queued | codex |  | Brief R4: Backstop/MCP/SharePoint mirror substrate (adversarial) |
| R5-output-substrate | B | B1 | queued | cursor |  | Brief R5: robust no-install output surfaces |
| R6-public-corpora | B | B1 | queued | cursor |  | Brief R6: public and synthetic corpora |
| R7-trip-planning-core | B | B1 | queued | codex |  | Brief R7: trip-planning core (transport, lodging, constraints) |
| B2-gap-analysis | B | B2 | queued | codex |  | Gap analysis and disposition of all candidates |
| B3-interop-architecture | B | B3 | queued | codex |  | Interoperability architecture (identity, typology, tracked variables,  |
| B4-issue-drafting | B | B4 | queued | codex |  | Draft AGENT_ISSUE_FORMAT issue bodies from decisions |
| C-skill-curriculum | C | C1 | queued | codex |  | Skill curriculum + tool-literacy loop design (LMS-connected) |

## Last checkpoints

- 2026-09-04T17:08:33Z — A-verify-CHECKPOINT — fail — not-ready: no cheap agent has capacity right now
- 2026-09-04T17:08:33Z — A-verify-Counter_Risk — route — router unavailable (ModuleNotFoundError); using capacity_ok; capacity_ok -> codex
- 2026-09-04T17:08:33Z — A-verify-Counter_Risk — claimed by driver (agent codex)
- 2026-09-04T17:08:33Z — A-verify-Counter_Risk — fail — not-ready: no cheap agent has capacity right now
- 2026-09-04T17:08:34Z — A-verify-Fine-Art-Archive — route — router unavailable (ModuleNotFoundError); using capacity_ok; capacity_ok -> codex
- 2026-09-04T17:08:34Z — A-verify-Fine-Art-Archive — claimed by driver (agent codex)
- 2026-09-04T17:08:34Z — A-verify-Fine-Art-Archive — fail — not-ready: no cheap agent has capacity right now
- 2026-09-04T17:10:13Z — A-verify-Counter_Risk — route — router picked gemini from ['codex', 'cursor', 'gemini']
- 2026-09-04T17:10:13Z — A-verify-Counter_Risk — claimed by driver (agent gemini)
- 2026-09-04T17:10:56Z — A-verify-Fine-Art-Archive — route — router picked gemini from ['codex', 'cursor', 'gemini']
- 2026-09-04T17:10:56Z — A-verify-Fine-Art-Archive — claimed by codex (agent gemini)
- 2026-09-04T17:11:39Z — A-verify-Counter_Risk — done — Counter_Risk dossier verified against HEAD 3f3ae3d: 52 claims checked, 39 confirmed, 11 corrected (5 substantive), 2 off-platform unverifiable — the in-repo doc
