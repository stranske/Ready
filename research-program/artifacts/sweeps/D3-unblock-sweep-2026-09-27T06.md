# D3 unblock sweep — 2026-09-27T06 (attempt 1)

**Coverage (8/14):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen repaired | Left for owner / repairable (offload) | Stalled PR reroutes | Default-branch state | Agent-ready supply |
|---|---:|---|---:|---|---:|
| Workflows | 0 | [#3123](https://github.com/stranske/Workflows/issues/3123) owner (`needs-human`, `tracker:durable`); [#3586](https://github.com/stranske/Workflows/issues/3586) **agent-repairable** (`agents:auto-pilot-pause`, format cap — missing `Tasks`/`Acceptance Criteria`; cited verifier paths verified in clone); [#3595](https://github.com/stranske/Workflows/issues/3595) **agent-repairable** (format cap — body cites `.github/workflows/agents-81-gate-followups.yml`; live path is `templates/consumer-repo/.github/workflows/agents-81-gate-followups.yml`) | 0 | [Agents Issue Format Guard **success** on head `a8f1e45`](https://github.com/stranske/Workflows/actions/runs/36298671964); no standalone `CI` on `main` | 37 (17 `priority:*` / 35 impl) |
| Travel-Plan-Permission | 0 | — | 0 | [green CI + format guard on head `35da666`](https://github.com/stranske/Travel-Plan-Permission/actions/runs/36298082105) | 33 (8 / 33) |
| Trend_Model_Project | 0 | — | 0 | [green CI on head `6c972f3`](https://github.com/stranske/Trend_Model_Project/actions/runs/36259314803) | 0 (0 / 0 impl; durable trackers only) |
| Portable-Alpha-Extension-Model | 0 | — | 0 | [green format guard on head `8b98491`](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/36270184194) | 2 (2 / 2) |
| Counter_Risk | 0 | — | 0 | **red** [CI on head `41445bb`](https://github.com/stranske/Counter_Risk/actions/runs/36259286551) — `black --check` on `tests/pipeline/test_langsmith_fleet_data_quality_status.py` (confirmed on local clone at `41445bb`) | 2 (2 / 2) |
| Manager-Database | 0 | — | 0 | **red** [CI on head `051b304`](https://github.com/stranske/Manager-Database/actions/runs/36289135380) — `test_document_managers_migration` FK `document_managers_doc_id_fkey`; Docker smoke also logs `crowded_trades.manager_id` / `holder_count` column drift | 2 (2 / 2) |
| Inv-Man-Intake | 0 | — | 0 | [green CI on head `d321bc3`](https://github.com/stranske/Inv-Man-Intake/actions/runs/36259293258) | 2 (2 / 2) |
| Pension-Data | 0 | — | 0 | [green CI on head `dd56e15`](https://github.com/stranske/Pension-Data/actions/runs/36295165495) | 5 (5 / 5) |

**Silent claims:** [#3568](https://github.com/stranske/Workflows/issues/3568) — stale `agent:retry` (~51h, no open PR). **Not released:** owner comment forbids further auto-pilot until verify:compare PASS on merged #3569; releasing the claim would contradict that hold (conflicts with generic 1b release rule — owner hold wins).

**Stalled agent PRs:** 0 reroutes (no open `agent:*` PR idle >4h without `agent:auto` across covered repos).

**Red main (offload — no PR):** Counter_Risk still needs a one-file `black` autofix on `main`. Manager-Database needs migration/schema + integration-test fix, not a blind patch.

**Priority gaps:** Workflows 17/35, Travel-Plan-Permission 8/33 implementation issues carry `priority:*`.

## Genuinely needs the owner

- Workflows [#3123](https://github.com/stranske/Workflows/issues/3123) — confirm whether LangSmith observability tracker degradation still requires `needs-human` or can clear after pause review.

**Offload:** Live GitHub via `with-gh-auth.sh gh`; local `black --check` (Counter_Risk clone at `41445bb`). **No** `gh issue edit`, label mutations, `gh pr create`, or git push this pass.

**Confidence:** High on counts and head-matched CI/Gate (~2026-09-27T06:15Z). **Objection:** `#3595` format guard flags missing paths because the issue body uses consumer-relative paths without the `templates/consumer-repo/` prefix — repair is rewrite + label drop, not owner input. **Uncertainty:** Whether any deferred-repo silent claims exist (not scanned this pass).
