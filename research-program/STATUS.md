# Research Program 2026-09 — STATUS (generated 2026-09-05T20:59:26Z)

Units: 51 — done 51
Paused: False   Phase stops: []
Capacity (Orchestrator): codex=ok claude=ok cursor=ok gemini=ok vibe=ok aider=ok
CLAUDE CONSERVATION ACTIVE until 2026-09-06T12:00:00Z — non-Claude executors continue (launchd driver every 15 min); claude-only units deferred.
Owner inbox: https://github.com/stranske/Ready/issues/553

| id | track | phase | status | agent | executor | title |
|---|---|---|---|---|---|---|
| readiness-dossier-consistency-20260904 | A | A | done | cursor | driver | Reconcile recovered dossier corrections into existing downstream artif |
| A-verify-Trend_Model_Project | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/Trend_Model_Project.md against ../cl |
| A-verify-Workflows | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/Workflows.md against ../clones/Workf |
| A-verify-learning-management-system | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/learning-management-system.md agains |
| A-verify-Collab-Admin | A | A1 | done | codex | claude | Verify dossier artifacts/dossiers/Collab-Admin.md against ../clones/Co |
| A-verify-Counter_Risk | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Counter_Risk.md against ../clones/Co |
| A-verify-Fine-Art-Archive | A | A1 | done | gemini | codex | Verify dossier artifacts/dossiers/Fine-Art-Archive.md against ../clone |
| A-verify-Inv-Man-Intake | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Inv-Man-Intake.md against ../clones/ |
| A-verify-Manager-Database | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Manager-Database.md against ../clone |
| A-verify-Orchestrator | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Orchestrator.md against ../clones/Or |
| A-verify-Pension-Data | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/Pension-Data.md against ../clones/Pe |
| A-verify-Portable-Alpha-Extension-Model | A | A1 | done | cursor | codex | Verify dossier artifacts/dossiers/Portable-Alpha-Extension-Model.md ag |
| A-verify-Template | A | A1 | done | gemini | driver | Verify dossier artifacts/dossiers/Template.md against ../clones/Templa |
| A-verify-Travel-Plan-Permission | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/Travel-Plan-Permission.md against .. |
| A-verify-trip-planner | A | A1 | done | cursor | driver | Verify dossier artifacts/dossiers/trip-planner.md against ../clones/tr |
| A-dossier-index | A | A2 | done | cursor | driver | Fleet index and shared vocabulary from verified dossiers (needs >=12 v |
| A-personal-reuse-note | A | A2 | done | cursor | driver | Reuse note across personal repos (FAA, Reader, trip-planner) |
| A-memo-correction | A | A3 | done | cursor | driver | Correct cover-memo maturity labels against the audit ledger and open i |
| A-work-side-bundle | A | A3 | done | cursor | driver | Work-side bundle: redaction pass, cover memo, safety grep |
| A-work-side-bundle-refresh | A | A3 | done | cursor | driver | Refresh the work-side bundle with the three late dossiers and re-run t |
| A-dossier-docx | A | A3 | done | cursor | codex | Word versions of all verified dossiers (venv + python-docx) |
| B1-citefix-B3-interop-architecture | B | B1 | done | cursor | driver | Fix unreachable citations in B3-interop-architecture.md |
| B1-citefix-R1-legal-decomposition | B | B1 | done | cursor | driver | Fix unreachable citations in R1-legal-decomposition.md |
| B1-citefix-R4-document-access-substrate | B | B1 | done | cursor | driver | Fix unreachable citations in R4-document-access-substrate.md |
| B1-citefix-R5-output-substrate | B | B1 | done | codex | codex | Fix unreachable citations in R5-output-substrate.md |
| B1-citefix-R6-public-corpora-and-synthetic-data | B | B1 | done | cursor | driver | Fix unreachable citations in R6-public-corpora-and-synthetic-data.md |
| B1-citefix-R7-trip-planning-core | B | B1 | done | cursor | driver | Fix unreachable citations in R7-trip-planning-core.md |
| R4-document-access | B | B1 | done | codex | driver | Brief R4: Backstop/MCP/SharePoint mirror substrate (adversarial) |
| R5-output-substrate | B | B1 | done | cursor | driver | Brief R5: robust no-install output surfaces |
| R1-legal-decomposition | B | B1 | done | codex | driver | Brief R1: legal fund-document decomposition and lineage |
| R2-consultant-report-diffing | B | B1 | done | codex | driver | Brief R2: consultant-report and periodic-communication diffing |
| R3-manager-mosaic | B | B1 | done | codex | driver | Brief R3: manager mosaic synthesis, discrepancy and thesis monitoring |
| R6-public-corpora | B | B1 | done | cursor | driver | Brief R6: public and synthetic corpora |
| R7-trip-planning-core | B | B1 | done | codex | driver | Brief R7: trip-planning core (transport, lodging, constraints) |
| B2-gap-analysis | B | B2 | done | codex | driver | Gap analysis and disposition of all candidates |
| B3-interop-architecture | B | B3 | done | codex | driver | Interoperability architecture, anchored on the work tools’ real field  |
| B4-issue-drafting | B | B4 | done | cursor | driver | Draft AGENT_ISSUE_FORMAT issue bodies from decisions |
| B5-work-env-issue-wave | B | B5 | done | cursor | driver | File the second wave of issues from the work-environment answers |
| B6-file-drafted-issues | B | B6 | done | cursor | driver | Verify, correct and file the B4-drafted issue bodies |
| B7-program-plan-v3 | B | B7 | done | codex | driver | Consolidated program plan v3 plus the progress-artifact specification |
| B7-program-plan-v3-default | B | B7 | done | codex | driver | Consolidated program plan v3 plus the progress-artifact specification |
| C-skill-curriculum | C | C1 | done | codex | driver | Skill curriculum + tool-literacy loop design (LMS-connected) |
| D2-issue-body-repair | D | D | done | cursor | driver | Repair issue bodies citing scratchpad paths and unblock the paused aut |
| D3-unblock-sweep-2026-09-04T21 | D | D | done | codex | driver | Unblock sweep: frozen issues, stalled agent PRs, red default branches |
| D3-unblock-sweep-2026-09-05T05 | D | D | done | codex | driver | Unblock sweep: frozen issues, stalled agent PRs, red default branches |
| D3-unblock-sweep-2026-09-05T13 | D | D | done | cursor | driver | Unblock sweep: frozen issues, stalled agent PRs, red default branches |
| D-audit-Fine-Art-Archive--2026-09-05T04-00-31Z | D | D | done | codex | codex | Audit stranske/Fine-Art-Archive and file issues (supply 1 <= 2) |
| D-audit-Manager-Mosaic--2026-09-05T04-00-25Z | D | D | done | codex | driver | Audit stranske/Manager-Mosaic and file issues (supply 2 <= 2) |
| D-audit-Travel-Plan-Permission--2026-09-05T16-11-36Z | D | D | done | codex | codex | Audit stranske/Travel-Plan-Permission and file issues (supply 3 <= 3) |
| D-audit-learning-management-system--2026-09-05T04-00-30Z | D | D | done | codex | driver | Audit stranske/learning-management-system and file issues (supply 2 <= |
| D4-verify-merged-2026-09-05T01 | D | D | done | cursor | driver | Verify merged PRs against their issues' acceptance criteria |

## Last checkpoints

- 2026-09-05T16:11:40Z — D-audit-Travel-Plan-Permission--2026-09-05T16-11-36Z — claimed by codex (agent codex)
- 2026-09-05T16:39:40Z — D-audit-Travel-Plan-Permission--2026-09-05T16-11-36Z — done — Audit establishes six reproduced behavior defects and two bounded hardening proposals; eight issue bodies validate without advisories and remain staged under th
- 2026-09-05T16:58:23Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T17:12:04Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T17:13:26Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T17:28:31Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T17:43:33Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T17:58:35Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T18:13:00Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T18:13:45Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T18:28:47Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues
- 2026-09-05T18:43:49Z — mirror — deferred — Ready#555 exact-head sync review; publication resumes by 2026-09-05T18:54:56+00:00; local work continues

## Questions


### q-B7-program-plan-v3 (2026-09-04T19:53:40Z) — unit B7-program-plan-v3
**Question:** Where should the manager-mosaic capability live: Manager-Database, Inv-Man-Intake, or a fourth new repo? (Orchestrator question q-f774f07b2a2d6ae7)
**Default being followed:** Inv-Man-Intake, because it already enforces document-and-page provenance and no new repo is needed; the drafted bodies stay unfiled under artifacts/issues/Manager-Mosaic/ until you decide.

