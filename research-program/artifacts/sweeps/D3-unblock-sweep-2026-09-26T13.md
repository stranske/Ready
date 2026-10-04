# D3 unblock sweep — 2026-09-26T13 (attempt 1)

**Coverage (8/14):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen repaired | Left for owner / left alone | Stalled PR reroutes | Default-branch state | Agent-ready supply |
|---|---:|---|---:|---|---:|
| Workflows | 0 (1 agent-fixable, offload) | [#3123](https://github.com/stranske/Workflows/issues/3123) LangSmith tracker (`needs-human`, `tracker:durable`); [#3586](https://github.com/stranske/Workflows/issues/3586) `agents:auto-pilot-pause` (format attempt cap) | 0 | [Agents Issue Format Guard success on head `b4c0862`](https://github.com/stranske/Workflows/actions/runs/36246676064); no `CI` workflow on repo | 41 (23 `priority:*` / 41 impl) |
| Travel-Plan-Permission | 0 | — | 0 | [green CI on head `9de5b6f`](https://github.com/stranske/Travel-Plan-Permission/actions/runs/36112685630) | 34 (9 / 34) |
| Trend_Model_Project | 0 | — | 0 | [green CI on head `82ba985`](https://github.com/stranske/Trend_Model_Project/actions/runs/36218780952) | 0 (0 / 0 impl; only durable trackers open) |
| Portable-Alpha-Extension-Model | 0 | — | 0 | [green CI on head `66c1beb`](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/36156074633) | 4 (4 / 4) |
| Counter_Risk | 0 | — | 0 | **red** [CI on head `d7701d6`](https://github.com/stranske/Counter_Risk/actions/runs/36237008168) — `black --check` (1 file; confirmed on local clone at `d7701d6`) | 1 (1 / 1) |
| Manager-Database | 0 | — | 0 | **red** [CI on head `ae68cd2`](https://github.com/stranske/Manager-Database/actions/runs/36162820402) — `test_document_managers_migration` FK on `document_managers_doc_id_fkey`; Docker stack smoke `unauthorized` pulling images | 2 (2 / 2) |
| Inv-Man-Intake | 0 | — | 0 | [green CI on head `2881609`](https://github.com/stranske/Inv-Man-Intake/actions/runs/36112769519) | 2 (2 / 2) |
| Pension-Data | 0 | — | 0 | [green CI on head `8a11773`](https://github.com/stranske/Pension-Data/actions/runs/36112748977) | 6 (6 / 6) |

**Frozen / silent claims:** [#3586](https://github.com/stranske/Workflows/issues/3586) — optimizer hit 3-attempt cap; body is follow-up narrative without agent-template `Tasks` / `Acceptance Criteria` (paths verified: `.github/scripts/agents_verifier_context.js`, `.github/scripts/__tests__/agents-verifier-context.test.js`). **Agent-repairable** on a non-offload pass. [#3568](https://github.com/stranske/Workflows/issues/3568) is a stale `agent:retry` claim (~34h, no open PR) but **not released** — owner comment requires verify:compare PASS before further auto-pilot; releasing would contradict that hold.

**Stalled agent PRs:** 0 reroutes (no open `agent:*` PR idle >4h without `agent:auto` across covered repos).

**Red main (offload — no PR):** Counter_Risk still needs a one-file `black` autofix on `main`. Manager-Database needs schema/test + registry auth investigation, not a blind agent patch.

**Priority gaps:** Workflows 23/41, Travel-Plan-Permission 9/34 implementation issues carry `priority:*`.

## Genuinely needs the owner

- Workflows [#3123](https://github.com/stranske/Workflows/issues/3123) — confirm whether LangSmith / intentional-pause tracker degradation still blocks fleet automation or can clear `needs-human` after pause review.

**Offload:** Live GitHub via `with-gh-auth.sh gh`; local `black --check` (Counter_Risk clone at `d7701d6`). **No** `gh issue edit`, label mutations, `gh pr create`, or git push this pass.

**Confidence:** High on counts and head-matched CI (~2026-09-26T13:54Z). **Objection:** `gh run list --branch main` is crowded by keepalive workflows; head-matched workflow API used for CI/Gate disposition. **Uncertainty:** Counter_Risk head unchanged since prior sweep but supply dropped (6→1) as issues closed or gained blocking labels — not re-audited issue-by-issue here.
