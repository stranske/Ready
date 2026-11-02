# D4 merged-PR verification — 2026-11-02T21

**Outcome:** 11 eligible PRs inspected (cap: 20): 3 VERIFIED, 5 PARTIAL, 2 NOT IMPLEMENTED, and 1 evidence-incomplete.  The real-input reproduction for Inv-Man-Intake #1062 still exits 1, so its merged status is not evidence of delivery.

Scope was the 36-hour window ending 2026-11-02T21:09Z across `SUPPORTED_REPOS`, excluding Orchestrator, release/dependency/template-sync chores, and the owner-excluded Collab-Admin repository. Squash diffs, issue bodies, and merge check evidence were read. A GitHub secondary-rate-limit response was not received.

| Repo | PR | Issue | Verdict | Unmet criteria / evidence | Follow-up filed |
|---|---:|---:|---|---|---|
| Doc-Lineage | #167 | #112 | **NOT IMPLEMENTED** | The squash diff changes only `pyproject.toml` (`reportlab==4.4.2`). It does not add the required persisted-run comparison API/CLI, content-bound artifact, opaque lookup, tamper/source-order rejection, integration tests, or deliberate-break proof. | No — this offload forbids GitHub writes. |
| Workflows | #4139 | #3986 | **PARTIAL** | Diff contains implemented subscription-auth path, guard tests, and deliberate-red/green evidence. Full issue AC-to-diff mapping could not be completed inside the bounded run; not promoted to VERIFIED. | No — none drafted without a confirmed unmet AC. |
| Workflows | #4362 | #4363 (referenced) | **EVIDENCE-INCOMPLETE** | Diff removes GitHub Models fallback rows and adds/updates behavior tests, but the referenced issue was not supplied as a closing reference and was not fetched before the run boundary. | No. |
| Manager-Database | #1875 | #1840 | **PARTIAL** | 845-line test-only diff targets `api/chat.py`, consistent with the coverage task. The required CI coverage delta and each deliberate-break result are asserted in PR evidence but were not independently re-run from the merge commit. | No — no specific failed criterion established. |
| Manager-Database | #1876 | #1842 | **PARTIAL** | 160-line test-only diff covers the requested coverage round, but does not itself establish the requested whole-CI coverage delta or break-and-revert proof for each new case. | No — no specific failed criterion established. |
| Ready | #638 | #623 | **VERIFIED** | Diff adds measured script coverage sources/floors, a dedicated `publication_coverage_gate.py`, baseline assertions, and deliberate-break evidence. This directly addresses the three ACs; named Gate checks were successful. | — |
| trip-planner | #1959 | #1958 | **VERIFIED** | Diff adds the named stale/invalidation regression and persisted disconnected/restored transcript; the test contains behavior assertions rather than a no-raise check. | — |
| trip-planner | #1963 | #1962 | **VERIFIED** | Diff adds Seattle to the real probe and tests both real non-fabrication and the missing-origin negative control. The regression explicitly rejects the 45-minute local-only fallback. | — |
| Travel-Plan-Permission | #1722 | #1720 | **PARTIAL** | Diff changes both specified docs paths and adds the named docs guard. Reproduction was required, but cannot be completed here: `uv sync` was denied while creating its configured Python-install directory outside the writable sandbox. | No — no failure observed. |
| Inv-Man-Intake | #1062 | #1061 | **NOT IMPLEMENTED** | Reproduction against merged tip `324ea010757cafed97e05ce067225b09208171af`: `inv-man-ingest tests/fixtures/intake/pdf_primary_mixed_bundle.json --out /tmp/d4-imi-runbook-out` printed `real document bytes not found`, exited **1**, and did not create `run.json`. This violates the issue’s success-form reproduction and named acceptance outcome. | No — offload prohibits required issue comment/reopen/follow-up creation. |
| Travel-Plan-Permission | #1723 | #1721 | **PARTIAL** | Diff adds a PP1–PP8 contract test and updates the contract, but also changes unrelated portal-receipt and CI-standard tests. The named test/deliberate-break were not independently run before the boundary. | No — no specific failed criterion established. |

## Excluded merged chores

Workflows #4349 and #4361 (release), trip-planner #1956 and Portable-Alpha-Extension-Model #2453 (template sync), and Travel-Plan-Permission #1717, Counter_Risk #1226, and Portable-Alpha-Extension-Model #2455 (dependency chores) were excluded by scope. Portable-Alpha-Extension-Model #2456 was a fleet campaign CI chore without a linked issue in the PR metadata, so it was not scored.

## Reproduction receipts and limits

- **Inv-Man-Intake #1061:** real success-form command result was `REPRO_EXIT=1`, `RUN_JSON=absent`; this is decisive against VERIFIED.
- **Travel-Plan-Permission #1720:** the required Python reproduction was not run because `uv sync --all-extras` failed before dependency resolution: `failed to create directory .../.local/share/uv/python: Operation not permitted`. That is an environment limitation, not a pass or a product failure.
- This synchronous offload expressly prohibits posting comments, reopening issues, or filing issues. Therefore no remote follow-up was filed, including for the two NOT IMPLEMENTED findings. The caller with write authority must comment/reopen #1061 with the receipt and file/link follow-ups for #112 and #1061.

Confidence: high for #112 and #1061; medium for the three VERIFIED rows because the named behavior is visible in the squash diff and successful merge checks, though no fresh clone test was run; low-to-medium for PARTIAL/EVIDENCE-INCOMPLETE rows, which are intentionally conservative rather than claims of a defect.
