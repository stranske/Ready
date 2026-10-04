# D3 unblock sweep — 2026-09-25T21 (attempt 1)

**Coverage (8/14):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen repaired | Left for owner / left alone | Stalled PR reroutes | Default-branch state | Agent-ready supply |
|---|---:|---|---:|---|---:|
| Workflows | 0 | [#3123](https://github.com/stranske/Workflows/issues/3123) LangSmith tracker (`needs-human`, `tracker:durable`) | 0 | [green proxy](https://github.com/stranske/Workflows/actions/runs/36193414005) Agents Issue Format Guard on `main` head; no CI / Gate runs on `main` | 39 (23 `priority:*` / 39 impl) |
| Travel-Plan-Permission | 0 | — | 0 | [green CI on head](https://github.com/stranske/Travel-Plan-Permission/actions/runs/36112685630) | 34 (9 / 34) |
| Trend_Model_Project | 0 | — | 0 | [green CI on head](https://github.com/stranske/Trend_Model_Project/actions/runs/36112873271) | 5 (5 / 5) |
| Portable-Alpha-Extension-Model | 0 | — | 0 | [green CI on head](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/36156074633) | 4 (4 / 4) |
| Counter_Risk | 0 | — | 0 | **red** [CI on head](https://github.com/stranske/Counter_Risk/actions/runs/36112731000) — `black --check` on `tests/pipeline/test_langsmith_fleet_data_quality_status.py` (confirmed in local clone) | 6 (6 / 6) |
| Manager-Database | 0 | — | 0 | **red** [CI on head](https://github.com/stranske/Manager-Database/actions/runs/36162820402) — `test_document_managers_migration` FK violation + Docker Hub `unauthorized` in stack smoke | 2 (2 / 2) |
| Inv-Man-Intake | 0 | — | 0 | [green CI on head](https://github.com/stranske/Inv-Man-Intake/actions/runs/36112769519) | 2 (2 / 2) |
| Pension-Data | 0 | — | 0 | [green CI on head](https://github.com/stranske/Pension-Data/actions/runs/36112748977) | 6 (6 / 6) |

**Frozen / silent claims:** No `agents:auto-pilot-pause`. [#3568](https://github.com/stranske/Workflows/issues/3568) is a stale `agent:retry` claim (~18h, no open PR) but **not released** — owner comment forbids further auto-pilot dispatch until verify:compare completes; releasing would violate explicit hold.

**Stalled agent PRs:** 0 reroutes (no open `agent:*` PR idle &gt;4h without `agent:auto`; Portable-Alpha #2315 already has `agent:auto`).

**Red main (offload — no PR):** Counter_Risk needs a one-file `black` autofix on `main`. Manager-Database needs product/test investigation (FK + schema errors), not a blind agent patch.

**Priority gaps:** Workflows 23/39, Travel-Plan-Permission 9/34 implementation issues carry `priority:*`.

## Genuinely needs the owner

- Workflows [#3123](https://github.com/stranske/Workflows/issues/3123) — confirm LangSmith / cloud observability credentials and whether degraded tracker state still blocks fleet automation.

**Offload:** Live GitHub via `with-gh-auth.sh gh`; local clone black check (Counter_Risk). **No** `gh pr create` / git push / issue label mutations this pass.

**Confidence:** High on counts and head-matched CI (API ~2026-09-25T21:49Z). **Objection:** `gh run list --branch main` omits Gate/CI on busy repos; head-matched workflow API used instead. **Uncertainty:** Workflows has no `CI` on `main`; health is format-guard proxy only.
