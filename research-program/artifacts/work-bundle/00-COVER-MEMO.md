# Cover memo — tool collection for colleagues

**Date:** 4 September 2026  
**From:** Investment office research programme  
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

## Production-ready versus prototype

A concise maturity picture:

| Maturity | Tools |
|----------|-------|
| **Usable today for real workflows** | Fleet standards hub, counterparty risk, manager surveillance, portable-alpha simulator, trend portfolio model, manager intake, travel policy engine, trip planner, staging templates, personal art archive |
| **Strong core, partial product surface** | Pension extraction (pipeline yes; live UI no), collaboration governance (validators yes; dashboard stub), learning platform (credible prototype; firm controls placeholder) |
| **Infrastructure / gated** | Agent orchestrator (local quota tracking; remote dispatch disabled after poor outcomes) |

Alpha labels appear in several repositories. That reflects packaging status, not necessarily analytical weakness.

## Operating constraints the tools were designed for

These tools share a common design envelope shaped by public-sector technology reality:

1. **No mandatory installs for operators.** Browser, Excel, or packaged executables—not source-code clones.
2. **Browser and Office as primary surfaces.** Dashboards, workbooks, and board-pack exports are first-class.
3. **Traceability back to source documents.** Page pointers, hashes, and run manifests support audit.
4. **No proprietary data leaving the environment by default.** Local databases, offline bundles, and demo modes are deliberate; optional AI features are configuration-gated.

## Interoperability programme (one paragraph)

Across repositories, the author is converging on shared contracts for run records, artifact manifests, evidence objects, and canonical entity identifiers. Only a subset emit conformant records today; the central workflows hub validates fleet-wide while most producers use legacy envelopes. Dossiers document identifier collisions explicitly. Treat exported spreadsheets and JSON as the practical integration surface until fleet-wide envelopes are wired.

## What I would suggest we could use

1. **Manager surveillance platform** — Ingests regulatory filings, diffs quarterly holdings, scores conviction, and supports research chat with citations; deployable behind a firewall or as an offline browser demo.
2. **Counterparty risk reporting** — Replaces a legacy spreadsheet workflow with button-driven Windows operation, producing Excel history, board slides, and an auditable manifest each month.
3. **Trend-following portfolio model** — Walk-forward manager ranking and allocation simulation with institutional Excel output; runs locally or in a zero-install browser bundle.
4. **Central fleet standards hub** — Enforces shared continuous integration, contract validation, and template sync across all repositories; the prerequisite for safe multi-tool adoption.

## Quick reference

| Tool | What it does | State | How a colleague would run it |
|------|--------------|-------|------------------------------|
| Fleet workflows hub | CI standards, contract validation, template sync | Production-usable | Automatic on every pull request; maintainers review sync delivery branches |
| Manager surveillance | Track managers, holdings, activism | Production-usable | Web dashboard or offline browser demo |
| Counterparty risk | Monthly exposure Excel and board pack | Production-usable | Windows desktop app or Excel macro workbook |
| Trend portfolio model | Manager ranking and walk-forward simulation | Production-usable | Command line, browser dashboard, or offline browser bundle |
| Pension data extraction | Facts from pension PDFs | Partial (pipeline yes, live UI no) | Command-line pilot on approved PDFs; browser bundle for review |
| Manager intake | Score and explain diligence packages | Production-usable (narrow formats) | Local command or offline browser demo |
| Portable-alpha model | Monte Carlo sleeve scenarios | Production-usable | Scenario wizard in private Python environment |
| Travel policy engine | Policy check and workbook fill | Production-usable (alpha) | Internal web service; public site is synthetic demo only |
| Trip planner | Plan and rank travel scenarios | Production-usable (catalog data) | Browser application on internal server |
| Staging templates | Standard CI and agent guardrails | Production-usable | Create new repo from template; no end-user UI |
| Agent orchestrator | Route coding tasks across AI subscriptions | Gated / local research | Maintainer workstation only |
| Collaboration admin | Rubrics, logs, review validators | Partial | Local dashboard; CSV validators in continuous integration |
| Learning platform | Source-to-practice training prototype | Partial | Internal web service with database server |
| Fine-art archive | Personal museum catalogue | Production on maintainer machine | Local web app when artwork storage is mounted |

---

*End of cover memo.*
