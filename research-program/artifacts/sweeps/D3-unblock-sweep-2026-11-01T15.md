# D3 unblock sweep — 2026-11-01

Covered (the first eight supported repositories): Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, and Pension-Data. Deferred by the mandatory eight-repository cap: Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, and Manager-Mosaic. Orchestrator was not acted on. `stranske/Collab-Admin` was excluded, including a Workflows item whose delivery target references it.

**Critical finding:** the requested remedy to remove every stale claim is unsafe where the issue's own last comment retains an original writer or verifier custody. A missing open PR does not prove that custody was abandoned. I have therefore identified the mechanically releasable cases separately from custody-bound cases; this offload is additionally prohibited from mutating GitHub.

| Repo | Frozen issues / recommended repair | Leave frozen or custody-bound | Stalled agent PRs re-routed | Default-branch state | Agent-ready supply |
|---|---|---|---|---|---:|
| Workflows | `#4363`, `#3978`: body/path repair is mechanically possible; then remove pause. `#4082` is refuted (see below). | `#4338`, `#3901` retain recorded source-owner/closer work; `#4223`, `#4051`, `#3898` lack a verifiable owning checkout or runnable acceptance gate; `#4284` is an active CI-budget measurement, not a delivery task. | None; no stale agent-labelled open PR found. | No Gate/CI run returned in the latest 20 main runs; branch health is **unknown**, not green. | 40 (8 of the 60 listed open issues lack `priority:*`) |
| Travel-Plan-Permission | None | None | None | No Gate/CI in latest 20; unknown. | 4 |
| Trend_Model_Project | None | None | None | No Gate/CI in latest 20; unknown. | 5 |
| Portable-Alpha-Extension-Model | None | None | None | No Gate/CI in latest 20; unknown. | 20 |
| Counter_Risk | None | None | None — PR #1185 was updated at 14:26Z and already has `agent:auto`. | Latest Gate follow-up succeeded (run 41316113453). | 6 |
| Manager-Database | None | `#1786` has a stale progress label but its last source comment preserves a nonterminal `verify:compare` disposition and original-source custody; do not release it without that writer's terminal evidence. | None | No Gate/CI in latest 20; unknown. | 10 |
| Inv-Man-Intake | None | None | None | No Gate/CI in latest 20; unknown. | 1 |
| Pension-Data | None | `#964` is claimed by open PR #985, updated at 14:24Z; do not release. | None | Latest Gate follow-up succeeded (run 41315978058). | 6 |

## Stale silent claims

- Workflows `#4036`, `#4026`, and `#3988` have `status:in-progress`/agent claim labels, no open PR referencing them, and were last updated over 12 hours ago. The prescribed next mutation is to remove their claim labels so the opener can select them. It was **not performed** under the offload boundary.
- Workflows `#4026` additionally has two prior sweep comments stating that its formerly missing file/path evidence is now corrected. It remains a stale claim, not active work.
- Manager-Database `#1786` meets the age/no-open-PR signal but is not a safe automatic release: its recorded acceptance remains a nonterminal comparison under an identified original source owner. This is an ownership gap, not evidence of an abandoned task.

## Genuine owner questions

- Workflows `#4223`: which repository owns the asserted receipt/verification paths, and what runnable command establishes acceptance?
- Workflows `#4051`: should the task be scoped to this repository, or is it authorized to create/use the external `~/.codex/orchestrator-mirror` path? A repo-relative implementation target and test are needed.
- Workflows `#3898`: identify the repository and real paths that own the writable-fork publication behavior, plus an observable acceptance command.

## Refutations

REFUTED: https://github.com/stranske/Workflows/issues/3978 — the fresh `c4633a95058d927c309dc7d666ff1d8dc85c2cc3` clone contains the cited reusable workflows under `.github/workflows/`; the guard's bare-path absence claim is wrong.

REFUTED: https://github.com/stranske/Workflows/issues/4082 — live `.github/workflows/pr-00-gate.yml` triggers on `pull_request` `opened`, `synchronize`, `reopened`, and `ready_for_review`, so the title's `create_only` premise no longer holds.

REFUTED: https://github.com/stranske/Workflows/issues/4026 — the issue's own current sweep evidence says Tasks/AC now cite `.github/scripts/maint71_merge_sync_prs.js`, tests, and `node --test`; the original missing-path block no longer holds.

## Evidence and limitations

All lists were live GitHub reads on 2026-11-01. The issue inventory command is intentionally capped at 60 items per repository, so the supply and priority gap are bounded counts, not a claim of complete repository totals. No most-recent default-branch Gate/CI failure was observed in the queried run windows; absence of a matching Gate/CI run is reported as unknown rather than a passing branch. No body edits, labels, comments, issues, branches, commits, pushes, or PRs were created: those actions are forbidden for this synchronous offload.
