# Ready — research home for the 2026-09 programme

This repository was the fleet's standby consumer. Since 2026-09-04 it is also the **home of the research programme**: the place where the programme's state is published, where its artifacts are read, and where the owner is reached.

## What lives here

| Path | What it is | Who writes it |
|---|---|---|
| `research-program/STATUS.md` | Live programme status: units done, queued, parked; capacity; open questions | The engine, every worker tick |
| `research-program/CHECKPOINT.md` | Append-only log of every claim, completion, question and repair | The engine |
| `research-program/QUESTIONS.md` | Parked questions, each with the default being followed in the owner's absence | The engine |
| `research-program/queue.jsonl` | The unit queue itself | The engine |
| `research-program/artifacts/dossiers/` | One verified dossier per fleet repo, each with a verification table, plus the fleet index and Word versions | Research units, verified adversarially |
| `research-program/artifacts/research/` | The research briefs, gap analysis, interoperability architecture, skill curriculum and programme plan | Research units |
| `research-program/artifacts/work-bundle/` | The redacted bundle prepared for the owner's work colleagues, the information request, and the answers that came back | Research units, redaction-checked |
| `research-program/artifacts/sweeps/` | Unblock sweeps: frozen issues repaired, stalled work re-routed | The recurring sweep |
| Issue [#553](https://github.com/stranske/Ready/issues/553) | The owner inbox. Commands: `answer <qid>: …`, `pause`, `resume`, `resume <unit>`, `stop phase <n>`, `note: …` | Owner and engine |

## The rule that matters if you are an agent working here

**Everything under `research-program/` is machine-owned.** It is a published mirror of a local engine directory, synchronised with deletion enabled: a file you add or edit there is silently removed or overwritten on the next tick. If something in that tree is wrong, the fix belongs upstream in the engine at `~/.codex/automations/research-program/`, not here. Do not hand-edit artifacts, and do not open pull requests against that tree.

Everything outside `research-program/` is ordinary repository code and is yours to change through the normal issue and pull-request flow.

## Why the artifacts deserve a guard

Two defect classes have already reached this tree and both are invisible on a casual read: a scan once printed token prefixes into a working file, and a batch of issue bodies carried a drafting agent's private working-directory paths, which made the issues unactionable. The work bundle in particular is prepared to be handed to colleagues, so a leaked path or credential fragment here is a real disclosure rather than an untidiness. That is what the publication guard exists to prevent.
