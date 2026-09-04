# Cover memo — tool collection for colleagues

**Date:** 4 September 2026  
**From:** Investment office research programme  
**Audience:** Investment staff and IT partners evaluating whether internally built tools can be adopted safely

---

## What this collection is

This folder is a redacted, work-safe bundle describing a family of software tools built to support pension investment work. Each document explains one tool: what problem it solves, how a non-developer would use it, what data it touches, how mature it is, and—importantly—where marketing claims diverge from what the code actually does today.

The bundle contains eleven verified dossiers. Three additional tools exist in the wider programme but were not included because their verification pass is not yet complete. Nothing here is a sales pitch; the claims-versus-reality sections are deliberately blunt.

## How these tools were built, and why that matters

Every tool in this collection was built by a single investment-office practitioner using commercial AI coding assistants, guided by repeatable engineering standards shared across repositories. That is not a novelty detail—it changes what adoption looks like.

Traditional enterprise software assumes a vendor, a procurement cycle, and a dedicated engineering team. These tools invert part of that model. The author can describe a workflow in plain language, generate an initial implementation, and then harden it with automated tests, typed interfaces, and review gates—the same quality practices a small software team would use, but at a fraction of the headcount. For sceptical IT readers, the implication is practical: you are not being asked to trust “vibe-coded” spreadsheets. You are being asked to evaluate repositories that carry thousands of automated tests, explicit data contracts, and documented gaps.

The trade-off is also honest. One person cannot operate eleven production systems simultaneously. Several tools are genuinely usable today; others are strong foundations with incomplete surfaces (browser dashboards still on fixtures, fleet-wide identifier schemes documented but not emitted everywhere). The dossiers say which is which.

## Four categories

**Staging and infrastructure** tools do not analyse investments. They standardise how new Python repositories are created, how continuous integration runs, and how automated agents are kept inside guardrails. The Template family and the Orchestrator belong here. Think of them as the factory floor, not the product.

**Work-related analytics and operations** tools address recurring investment-office tasks: tracking external managers and filings, extracting facts from pension documents, producing counterparty exposure packs, modelling portable-alpha structures, standardising manager due-diligence intake, and governing travel policy. These are the tools most colleagues will care about first.

**Personal tools** sit outside the office mandate. The fine-art archive catalogue is included for completeness because it shares engineering patterns (local-first storage, provenance tracking, offline review surfaces) that may inform how office tools are deployed—but it is not a pension system.

**Governance and collaboration** (Collab-Admin) is a rulebook and instrumentation layer for a specific multi-person collaboration, not an analytics engine. It may still be useful as a pattern for how rubrics, time logs, and review artifacts can be validated mechanically.

## Production-ready versus prototype

A concise maturity picture:

| Maturity | Tools |
|----------|-------|
| **Usable today for real workflows** | Counterparty risk reporting, manager surveillance database, portable-alpha simulator, manager intake pipeline, travel policy engine, trip planning application, staging templates, personal art archive (on maintainer hardware) |
| **Strong core, partial product surface** | Pension document extraction (extraction pipeline works; live dashboard and several API routes are fixture-only), collaboration governance (validators work; scheduled dashboard output is still a stub) |
| **Infrastructure / gated** | Agent orchestrator (valuable locally for quota tracking and verification; automated remote dispatch is intentionally disabled after poor outcomes) |

Alpha labels appear in several repositories. That reflects packaging status, not necessarily analytical weakness—some alpha-labelled tools have test counts in four figures.

## Operating constraints the tools were designed for

These tools share a common design envelope shaped by public-sector technology reality:

1. **No mandatory installs for operators.** Where possible, colleagues interact through a browser, Excel, or a packaged executable—not by cloning source code.
2. **Browser and Office as primary surfaces.** Streamlit and React apps, Excel macro workbooks, and board-pack exports are first-class—not afterthoughts.
3. **One-click traceability back to source documents.** Extraction and reporting tools retain page-level pointers, hashes, and run manifests so a number shown in a meeting can be walked back to an input file.
4. **No proprietary data leaving the environment by default.** Local SQLite, on-prem databases, offline browser bundles, and explicit “demo mode” deployments are deliberate. Optional large-language-model features are gated behind configuration and often ship with offline stubs for testing.

## Interoperability programme (one paragraph)

Across repositories, the author is converging on shared contracts for run records, artifact manifests, evidence objects, and canonical entity identifiers (managers, funds, pensions). Today only a subset of tools emit conformant records; many document the standard without yet writing files. The dossiers call out identifier collisions explicitly—e.g., one system uses integer manager keys while another expects regulator filing numbers in a prefixed string format—because silent mismatch would poison any future data join. The interoperability work is real but incomplete; treat exported JSON and CSV from each tool as the practical integration surface until fleet-wide envelopes are wired.

## What I would suggest we could use

1. **Manager surveillance platform** — Ingests regulatory filings, diffs quarterly holdings, scores conviction, and supports research chat with citations; deployable behind a firewall or as an offline browser demo.
2. **Counterparty risk reporting** — Replaces a legacy spreadsheet workflow with button-driven Windows operation, producing Excel history, board slides, and an auditable manifest each month.
3. **Pension document extraction** — Turns PDF actuarial and financial reports into structured, reviewable facts with confidence routing; safest use today is controlled document-to-artifact runs inside the network perimeter.
4. **Travel policy and reimbursement engine** — Checks trips against policy, fills the official travel workbook, and hosts a review portal; pairs with the separate trip-planning application for pre-travel scenario work.

## Quick reference

| Tool | What it does | State | How a colleague would run it |
|------|--------------|-------|------------------------------|
| Manager surveillance | Track managers, holdings, activism | Production-usable | Web dashboard or offline browser demo |
| Counterparty risk | Monthly exposure Excel and board pack | Production-usable | Windows desktop app or Excel macro workbook |
| Pension data extraction | Facts from pension PDFs | Partial (pipeline yes, live UI no) | Command-line pilot on approved PDFs; browser bundle for review |
| Manager intake | Score and explain diligence packages | Production-usable (narrow formats) | Local command or offline browser demo |
| Portable-alpha model | Monte Carlo sleeve scenarios | Production-usable | Scenario wizard in private Python environment |
| Travel policy engine | Policy check and workbook fill | Production-usable (alpha) | Internal web service; public site is synthetic demo only |
| Trip planner | Plan and rank travel scenarios | Production-usable (catalog data) | Browser application on internal server |
| Staging templates | Standard CI and agent guardrails | Production-usable | Create new repo from template; no end-user UI |
| Agent orchestrator | Route coding tasks across AI subscriptions | Gated / local research | Maintainer workstation only |
| Collaboration admin | Rubrics, logs, review validators | Partial | Local dashboard; CSV validators in continuous integration |
| Fine-art archive | Personal museum catalogue | Production on maintainer machine | Local web app when artwork storage is mounted |

---

*End of cover memo.*
