# Research Program 2026-09 — how to restart or steer me

**Owner inbox (phone-friendly):** https://github.com/stranske/Ready/issues/553 — comment `answer <qid>: …`, `pause`, `resume`, `resume <unit>`, `stop phase <n>`, `note: …`.
**Live status:** https://github.com/stranske/Ready/blob/main/research-program/STATUS.md (rewritten every tick; mirror of this directory).

## What runs where
| Executor | Cadence | Trigger | Depends on |
|---|---|---|---|
| Codex automation `research-program-worker` | hourly :10 | Codex app (must be running) | ChatGPT Pro window |
| Claude scheduled task `research-program-worker` | 06:00, 12:00, 18:00 local | Claude desktop app (open, logged in) | Claude Max window |
| Orchestrator offloads (gemini/cursor/vibe) | called by either executor | dispatcher.py | their own pools |
| Stall detector `research-program` (checkin.py) | every 6 h | launchd `com.stranske.checkin-runner` | nothing else |
| Cloud routine "Research Program — inbox responder" | on inbox comment + daily 13:00 UTC | claude.ai (no local dependency) | Ready repo only |

All state is in this directory (local disk, not Dropbox): `queue.jsonl`, `CHECKPOINT.md`, `QUESTIONS.md`, `STATUS.md`, `state.json`, `artifacts/`. The engine is `program.py` (deterministic; run `python3 program.py --help`).

## If nothing has happened for a while
1. Open STATUS.md. If the last checkpoint is > 8 h old: the executors are not firing. Check (a) the Codex app is running, (b) the Claude desktop app is open and signed in (`~/Library/Logs/Claude/main.log` for `oauth failed`), (c) capacity: `~/.codex/handoff/capacity.json` agents' `state`.
2. Any Claude session (desktop, web, phone with a computer environment) can act as an executor: paste EXECUTOR_PROMPT.md and run it with `--executor claude`.
3. A dead unit: `python3 program.py release <id>` then let the next tick pick it up; its CHECKPOINT.md is in the unit's OUT directory.
4. Comment `pause` on the inbox to stop all executors; `resume` to continue.

## Program shape
Track A dossiers → A-verify → 00-INDEX → docx; Track B briefs R1–R7 → B2 gap analysis → B3 interop architecture → B4 issue bodies; Track C coverage matrix → curriculum + tool-literacy loop design; Track D demand-driven audits (`~/.codex/bin/audit-refill.py`, daily). Plan: `Code/Projects/research-program-2026-09/`.
