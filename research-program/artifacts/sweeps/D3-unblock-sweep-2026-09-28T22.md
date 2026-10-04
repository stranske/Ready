# D3 unblock sweep — 2026-09-28T22 (attempt 1)

**Coverage (8/15):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen (repaired / left for owner) | Stalled PR reroutes | Default branch | Agent-ready supply |
|---|---|---:|---|---:|
| Workflows | **2 repaired** [#3611](https://github.com/stranske/Workflows/issues/3611), [#3612](https://github.com/stranske/Workflows/issues/3612) — AC lacked runnable gate; hit format-guard attempt cap after 14:00 “repair”; added `pytest` / `node --test` AC + dropped `agents:auto-pilot-pause` / **1 left** [#3123](https://github.com/stranske/Workflows/issues/3123) `needs-human` LangSmith tracker | 0 | [Agents Issue Format Guard **success**](https://github.com/stranske/Workflows/actions/runs/36493985263) on `main` (`f7bb878`) | 25 (13 `priority:*` / 25 impl) |
| Travel-Plan-Permission | 0 / — | 0 | [CI **success**](https://github.com/stranske/Travel-Plan-Permission/actions/runs/36478991043) on `42c1e9d` | 31 (6 / 31) |
| Trend_Model_Project | 0 / — | 0 | [CI **success**](https://github.com/stranske/Trend_Model_Project/actions/runs/36355095632) on `069e070` | 0 (0 / 0 impl; durable trackers only) |
| Portable-Alpha-Extension-Model | 0 / — | 0 | [CI **success**](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/36480979858) on `c818bd3` | 0 (0 / 0 impl; durable trackers only) |
| Counter_Risk | 0 / — | 0 | **red** [CI **failure**](https://github.com/stranske/Counter_Risk/actions/runs/36403540930) on `ff4bc19` — `black --check` would reformat `tests/pipeline/test_langsmith_fleet_data_quality_status.py` | 0 (0 / 0 impl; durable trackers only) |
| Manager-Database | 0 / — | 0 | **red** [CI **failure**](https://github.com/stranske/Manager-Database/actions/runs/36362664895) on `4e384db` — `Docker stack smoke` / `docker: unauthorized` on image pull | 0 (0 / 0 impl; durable trackers only) |
| Inv-Man-Intake | 0 / — | 0 | [CI **success**](https://github.com/stranske/Inv-Man-Intake/actions/runs/36370204483) on `209f989` | 2 (2 / 2) |
| Pension-Data | 0 / — | 0 | [CI **success**](https://github.com/stranske/Pension-Data/actions/runs/36373780606) on `062bd84` | 2 (2 / 2) |

**Silent claims:** [#3568](https://github.com/stranske/Workflows/issues/3568) — stale `agent:retry` (~90h, no open PR). **Not released:** owner forbids further auto-pilot until verify:compare PASS on merged #3569.

**Stalled agent PRs:** 0 reroutes (no open `agent:*` PR idle >4h without `agent:auto` in covered repos).

**Priority gaps:** Workflows 13/25, Travel-Plan-Permission 6/31, Inv-Man-Intake and Pension-Data fully labelled among impl issues.

**Red main (offload — no PR):** Counter_Risk needs a one-file `black` autofix on `tests/pipeline/test_langsmith_fleet_data_quality_status.py`. Manager-Database needs valid Docker registry credentials or a job skip — not a safe blind code patch.

## Genuinely needs the owner

- Workflows [#3123](https://github.com/stranske/Workflows/issues/3123) — confirm whether LangSmith observability tracker degradation still requires `needs-human` or can clear after pause review.
- Workflows [#3596](https://github.com/stranske/Workflows/issues/3596) — refresh or rotate `CODEX_AUTH_JSON` before expiry (credential; no `needs-human` label).
- Manager-Database — restore Docker Hub (or configured registry) pull auth for `Docker stack smoke` on `main`, or disable that job until credentials work.

**Mutations this pass:** `gh issue edit` on Workflows #3611, #3612 (body + removed `agents:auto-pilot-pause`). **No** `gh pr create` / git push (offload).

**Confidence:** High on live GitHub reads and #3611/#3612 repairs (~2026-09-28T23:05Z). **Objection:** The 14:00 sweep reported #3611/#3612 as repaired but left bodies that still fail the format guard; auto-pilot re-paused them within minutes — that was a false “repaired” unless pause labels stayed off (they did not). **Uncertainty:** Whether the new AC lines pass the optimizer without hitting the 3-attempt cap again (commands verified in `[LOCAL_WORKSPACE]/Workflows` on disk).
