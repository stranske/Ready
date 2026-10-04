# D3 unblock sweep — 2026-09-26T21 (attempt 1)

**Coverage (8/14):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen repaired | Left for owner / left alone | Stalled PR reroutes | Default-branch state | Agent-ready supply |
|---|---:|---|---:|---|---:|
| Workflows | 0 (1 agent-fixable, offload) | [#3123](https://github.com/stranske/Workflows/issues/3123) LangSmith tracker (`needs-human`, `tracker:durable`); [#3586](https://github.com/stranske/Workflows/issues/3586) `agents:auto-pilot-pause` (format attempt cap) | 0 | [Agents Issue Format Guard success on head `3262dbd`](https://github.com/stranske/Workflows/actions/runs/36274445487); no standalone `CI` on `main` | 35 (16 `priority:*` / 40 impl) |
| Travel-Plan-Permission | 0 | — | 0 | [green CI on head `5026048`](https://github.com/stranske/Travel-Plan-Permission/actions/runs/36259280989) | 33 (8 / 34) |
| Trend_Model_Project | 0 | — | 0 | [green CI on head `6c972f3`](https://github.com/stranske/Trend_Model_Project/actions/runs/36259314803) | 0 (0 / 0 impl; durable trackers only) |
| Portable-Alpha-Extension-Model | 0 | — | 0 | [green Agents Gate + format guard on head `8b98491`](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/36273106188) | 2 (2 / 2) |
| Counter_Risk | 0 | — | 0 | **red** [CI on head `41445bb`](https://github.com/stranske/Counter_Risk/actions/runs/36259286551) — `black --check` on `tests/pipeline/test_langsmith_fleet_data_quality_status.py` (confirmed on local clone at `41445bb`) | 1 (1 / 1) |
| Manager-Database | 0 | — | 0 | **red** [CI on head `c270918`](https://github.com/stranske/Manager-Database/actions/runs/36259305028) — Postgres chain: `document_managers_doc_id_fkey` + schema/query drift (`manager_id` / `holder_count` on `crowded_trades`) | 2 (2 / 2) |
| Inv-Man-Intake | 0 | — | 0 | [green CI on head `d321bc3`](https://github.com/stranske/Inv-Man-Intake/actions/runs/36259293258) | 2 (2 / 2) |
| Pension-Data | 0 | — | 0 | [green CI on head `80e8370`](https://github.com/stranske/Pension-Data/actions/runs/36259289163) | 6 (6 / 6) |

**Frozen / silent claims:** [#3586](https://github.com/stranske/Workflows/issues/3586) — optimizer hit 3-attempt cap; body lacks agent-template `Tasks` / `Acceptance Criteria` with runnable gates (cited paths exist in clone: `.github/scripts/agents_verifier_context.js`, `.github/scripts/__tests__/agents-verifier-context.test.js`). **Agent-repairable** on a non-offload pass (rewrite body, drop `agents:auto-pilot-pause`). [#3568](https://github.com/stranske/Workflows/issues/3568) is a stale `agent:retry` claim (~42h, no open PR referencing it) but **not released** — owner comments forbid further auto-pilot until verify:compare PASS; releasing would contradict that hold.

**Stalled agent PRs:** 0 reroutes (no open `agent:*` PR idle >4h without `agent:auto` across covered repos; e.g. Workflows [#3587](https://github.com/stranske/Workflows/pull/3587), Portable-Alpha [#2317](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2317) already carry `agent:auto` and updated <4h).

**Red main (offload — no PR):** Counter_Risk still needs a one-file `black` autofix on `main`. Manager-Database needs schema/migration + integration-test investigation, not a blind agent patch.

**Priority gaps:** Workflows 16/40, Travel-Plan-Permission 8/34 implementation issues carry `priority:*`.

## Genuinely needs the owner

- Workflows [#3123](https://github.com/stranske/Workflows/issues/3123) — confirm whether LangSmith / intentional-pause tracker degradation still blocks fleet automation or can clear `needs-human` after pause review.

**Offload:** Live GitHub via `with-gh-auth.sh gh`; local `black --check` (Counter_Risk clone at `41445bb`). **No** `gh issue edit`, label mutations, `gh pr create`, or git push this pass.

**Confidence:** High on counts and head-matched CI (~2026-09-26T22:00Z). **Objection:** `gh run list --branch main` is dominated by keepalive workflows; head-matched workflow API used for CI/Gate disposition. **Uncertainty:** Workflows `priority:*` count dropped vs prior sweeps (label churn on issues outside the `--limit 60` window is unlikely but not re-proven issue-by-issue).
