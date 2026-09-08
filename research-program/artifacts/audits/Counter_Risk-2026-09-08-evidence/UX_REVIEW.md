# Counter_Risk UX review — 2026-09-08T17:28:42.209627+00:00

Only the static browser page and headless discovery were observed; Windows Tk/Excel/COM/frozen-exe coverage is unverified. This is not a production UI gate pass.

| Surface | Driven | Outcome | Evidence |
|---|---|---|---|
| Static demo page | Yes | Explanation and Ready status render; no artifact retrieval link or control | /Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/browser-dom.txt; /Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/demo.png |
| Source headless GUI discovery | Yes | Completed with explicit fixture config | /Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/gui-discovery-explicit-config.txt |
| Source launch from unrelated cwd without config | Yes | Readable missing-config error; source resolver intentionally keeps relative paths | /Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/gui-discovery.txt |
| Windows Tk, XLSM, Office COM, assembled binary | No | Platform unavailable here | /Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/WINDOWS_TEST_BRIEF.md |

Four nonempty evaluator rubrics (codex/cursor/gemini/vibe), plus cursor adversary, are retained under /Users/teacher/.codex/orchestrator-mirror/ux_reviews/stranske/Counter_Risk_uxreview_2026-09-08-research/. Static-page medians: wiring 5.5, usability 3, help clarity 5, productivity 2.5; overall 3. Consensus flags all true. Gate result is false: no full Gate 1, low static-page median, panel blockers. Scores do not describe the production Tk GUI.

Lead adjudication: the three panel findings are one retrieval-handoff problem, already known as August 24 D4-1 and adjacent to closed #645. Retain as a known follow-up, not a new issue. Accept a precise fixture-artifact location/link or documented handoff. Reject a mandatory browser execution engine or unrestricted upload as scope expansion; fixture-only static labeling is explicit. The high blocker rating is downgraded to a secondary demo usability gap. The headless success line supports command wiring only, not GUI screen quality. Improvements and raw scores are saved without rewriting the panel's conclusions.

Source fixture smoke: 3 passed in 88.72 seconds. Windows handoff remains open. No review-log PR or UI changes were made.
