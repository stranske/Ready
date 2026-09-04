# Cover memo — tool collection for colleagues

**Date:** 4 September 2026  
**From:** Tim Stranske  
**Audience:** Investment staff and IT partners evaluating internal tools for safe adoption

---

## What this collection is

This folder is a redacted, work-safe bundle describing software tools built to support pension investment work. Each document explains one tool: what problem it solves, how a non-developer would use it, what data it touches, how mature it is, and—importantly—where marketing claims diverge from what the code actually does today.

The bundle contains fourteen verified dossiers covering the full fleet index. Nothing here is a sales pitch; claims-versus-reality sections are deliberately blunt.

## How these tools were built, and why that matters

Every tool in this collection was built by a single investment-office practitioner using commercial AI coding assistants, guided by repeatable engineering standards shared across repositories.

Traditional enterprise software assumes a vendor and a dedicated engineering team. These tools invert part of that model: a workflow can be described in plain language, implemented, and hardened with automated tests and typed interfaces—the same quality practices a small software team would use, but at a fraction of the headcount. For sceptical IT readers, you are not being asked to trust improvised spreadsheets. You are being asked to evaluate repositories that carry thousands of automated tests, explicit data contracts, and documented gaps.

The trade-off is honest. One person cannot operate fourteen production systems simultaneously. Several tools are genuinely usable today; others are strong foundations with incomplete surfaces. The dossiers say which is which.

## Four categories

**Staging and infrastructure** tools do not analyse investments. They standardise how new Python repositories are created, how continuous integration runs across the fleet, and how automated agents are kept inside guardrails. The central workflows hub, staging templates, and local agent orchestrator belong here. Think of them as the factory floor, not the product.

**Work-related analytics and operations** tools address recurring investment-office tasks: manager surveillance, pension document extraction, counterparty exposure reporting, portable-alpha modelling, trend-following portfolio simulation, manager due-diligence intake, and travel governance.

**Personal tools** sit outside the office mandate. The fine-art archive shares deployment patterns but is not a pension system.

**Governance, collaboration, and training** covers collaboration rulebooks and a learning prototype—not validated corporate learning management.

## Maturity at a glance

Three labels only. I do not call a tool usable if a primary user-facing path is known broken; the row states what works instead.

| Maturity | Tools |
|----------|-------|
| **Usable for real work now** | Fleet standards hub, manager surveillance, portable-alpha simulator, staging templates |
| **Usable with a named caveat** | Counterparty risk (maintainer CLI and Excel macro path work; frozen Windows bundle unverified off-platform), trend portfolio model (CLI and institutional Excel export work; Streamlit browser flow shows contradictory fund-selection state and misleading headline metrics), manager intake (local PDF/PPTX validation and scoring work; default CLI is in-memory and formats are narrow), travel policy engine (deterministic policy check and workbook fill work; blocking rules can fail-open on missing or NaN inputs — open #1499, #1504), pension extraction (one-PDF CLI pipeline and backplane emit work; web API serves fixtures only), collaboration admin (CSV validators and rubrics work in CI; local dashboard is a timestamp stub), fine-art archive (works on maintainer machine when artwork storage is mounted) |
| **Prototype or foundation only** | Trip planner (scenario ranking and budget tracking on static catalog data; approval-packet button and remote TPP integration unwired), agent orchestrator (local quota tracking only; remote dispatch disabled after poor outcomes), learning platform (credible test-covered prototype; firm-grade controls and production learner loop incomplete) |

Alpha labels appear in several repositories. That reflects packaging status, not necessarily analytical weakness.

## Operating constraints the tools were designed for

These tools share a common design envelope shaped by public-sector technology reality:

1. **No mandatory installs for operators.** Browser, Excel, or packaged executables—not source-code clones.
2. **Browser and Office as primary surfaces.** Dashboards, workbooks, and board-pack exports are first-class.
3. **Traceability back to source documents.** Page pointers, hashes, and run manifests support audit.
4. **No proprietary data leaving the environment by default.** Local databases, offline bundles, and demo modes are deliberate; optional AI features are configuration-gated.

## Interoperability programme (one paragraph)

Across repositories, I am converging on shared contracts for run records, artifact manifests, evidence objects, and canonical entity identifiers. Only a subset emit conformant records today; the central workflows hub validates fleet-wide while most producers use legacy envelopes. Dossiers document identifier collisions explicitly. Treat exported spreadsheets and JSON as the practical integration surface until fleet-wide envelopes are wired.

## What I would suggest we could use

1. **Manager surveillance platform** — Ingests regulatory filings, diffs quarterly holdings, scores conviction, and supports research chat with citations; deployable behind a firewall or as an offline browser demo. Foreign-filing adapters remain stubbed; treat US EDGAR as the proven path.
2. **Counterparty risk reporting** — Replaces a legacy spreadsheet workflow with button-driven Windows operation, producing Excel history, board slides, and an auditable manifest each month. I have verified the maintainer CLI and macro workbook path; the frozen PyInstaller bundle still needs on-Windows confirmation.
3. **Trend-following portfolio model** — Walk-forward manager ranking and allocation simulation with institutional Excel output. Use the command-line or packaged Excel export path today; do not treat the Streamlit browser dashboard as audit-ready until the selection-state wiring defects are closed.
4. **Central fleet standards hub** — Enforces shared continuous integration, contract validation, and template sync across all repositories; the prerequisite for safe multi-tool adoption.

## Quick reference

| Tool | What it does | State | How a colleague would run it |
|------|--------------|-------|------------------------------|
| Fleet workflows hub | CI standards, contract validation, template sync | Usable for real work now | Automatic on every pull request; maintainers review sync delivery branches |
| Manager surveillance | Track managers, holdings, activism | Usable for real work now | Web dashboard or offline browser demo (US EDGAR path proven; foreign adapters stubbed) |
| Counterparty risk | Monthly exposure Excel and board pack | Usable with a named caveat — maintainer CLI and Excel macro path work; frozen Windows bundle unverified off-platform | Windows desktop app or Excel macro workbook |
| Trend portfolio model | Manager ranking and walk-forward simulation | Usable with a named caveat — CLI pipeline and institutional Excel export work; Streamlit browser flow has contradictory selection metrics (Aug 2026 UX review; open #6017–#6026) | Command line or offline browser bundle for review only; prefer CLI for production runs |
| Pension data extraction | Facts from pension PDFs | Usable with a named caveat — one-PDF CLI pipeline and backplane emit work; web API serves fixtures and LLM routes return 501 | Command-line pilot on approved PDFs; do not treat the browser API as a live data service |
| Manager intake | Score and explain diligence packages | Usable with a named caveat — local PDF/PPTX validation and scoring work; default CLI is in-memory; browser demo is not binary-faithful ingestion | Local command on configured stores; offline browser demo for narrow formats only |
| Portable-alpha model | Monte Carlo sleeve scenarios | Usable for real work now | Scenario wizard in private Python environment |
| Travel policy engine | Policy check and workbook fill | Usable with a named caveat — deterministic checks and spreadsheet fill work; blocking rules can fail-open on missing inputs (#1499, #1504) | Internal web service; public site is synthetic demo only |
| Trip planner | Plan and rank travel scenarios | Prototype or foundation only — ranking and budget on static catalog data work; approval-packet button does not submit proposals and remote TPP is off (`live_tpp=off`) | Browser application for scenario exploration only; not for approval workflows |
| Staging templates | Standard CI and agent guardrails | Usable for real work now | Create new repo from template; no end-user UI |
| Agent orchestrator | Route coding tasks across AI subscriptions | Prototype or foundation only — local quota tracking works; remote dispatch disabled (shadow mode) after poor merge outcomes | Maintainer workstation only |
| Collaboration admin | Rubrics, logs, review validators | Usable with a named caveat — CSV validators and rubrics work in CI; local Streamlit dashboard is a timestamp stub | Local dashboard for rubric review; CSV validators in continuous integration |
| Learning platform | Source-to-practice training prototype | Prototype or foundation only — credible test-covered core; firm-grade controls, validated mastery, and production learner loop incomplete | Internal web service with database server; not validated corporate LMS |
| Fine-art archive | Personal museum catalogue | Usable with a named caveat — works when artwork storage is mounted; corpus lives outside the repo | Local web app when artwork storage is mounted |

---

## Evidence basis

Labels were re-checked on **4 September 2026** against:

1. **Dossier claims-vs-reality sections** — `./artifacts/dossiers/<Repo>.md` for all fourteen tools in this bundle.
2. **Audit ledger and per-repo audit folders** — `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/AUDIT_LEDGER.md` (including 2026-09-04 fleet intake wave entries) and the most recent `2026-09-04-*` reports and verification logs under `Code/Audits/<Repo>/`.
3. **Observed UX traces** — `trip-planner/2026-08-16-UX_REVIEW.md` (Prepare approval packet produces no proposal); `Trend_Model_Project/2026-08-11-UX_REVIEW.md` and `2026-08-23-AUDIT_REPORT.md` (browser operator-surface wiring defects).
4. **Open GitHub issues** — `gh issue list` was attempted but the CLI was unauthenticated in this environment; issue numbers cited are from AUDIT_LEDGER 2026-09-04 filings and are assumed still open unless a dossier or ledger entry records closure.

---

*End of cover memo.*
