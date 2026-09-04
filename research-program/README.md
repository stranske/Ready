# Research Program 2026-09 — how to restart or steer me

**Owner inbox (phone-friendly):** https://github.com/stranske/Ready/issues/553 — comment `answer <qid>: …`, `pause`, `resume`, `resume <unit>`, `stop phase <n>`, `note: …`.
**Live status:** https://github.com/stranske/Ready/blob/main/research-program/STATUS.md (rewritten every tick; mirror of this directory).

## What runs where
| Executor | Cadence | Trigger | Depends on |
|---|---|---|---|
| Codex automation `research-program` (Astra/high) | hourly :10 | Codex app (must be running) | ChatGPT Pro window |
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
Track A dossiers → A-verify → 00-INDEX → docx; Track B briefs R1–R7 → B2 gap analysis → B3 interop architecture → B4 issue bodies; Track C coverage matrix → curriculum + tool-literacy loop design; Track D demand-driven audits (`program.py refill-check`, every 12 hours). Plan: `Code/Projects/research-program-2026-09/`.

## 2026-09-04 readiness repair

The launchd driver runs one unit per invocation every 15 minutes, through the local
Orchestrator mirror. `clones/` is now a durable directory under this engine, not a
temporary-session symlink. Phase stops are enforced at claim time. Offload process
status, dispatcher result status, and fresh output are all required for completion.
The inbox is paginated; mirror delivery is serialized and pending pushes retry on
subsequent ticks, including empty ticks. Audit identifiers are unique per round.

The 80% cross-provider allowance is a planning target, not an independently measured
aggregate-spend cap in this engine. Routing still uses Orchestrator capacity controls.
