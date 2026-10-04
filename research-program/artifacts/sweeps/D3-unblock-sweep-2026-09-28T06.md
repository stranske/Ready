# D3 unblock sweep — 2026-09-28T06 (attempt 1)

**Coverage (8/14):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen (repaired / left for owner) | Stalled PR reroutes | Default branch | Agent-ready supply |
|---|---|---:|---|---:|
| Workflows | **3 repaired** [#3586](https://github.com/stranske/Workflows/issues/3586), [#3606](https://github.com/stranske/Workflows/issues/3606), [#3607](https://github.com/stranske/Workflows/issues/3607) — added `Tasks`/`Acceptance Criteria`, dropped `agents:auto-pilot-pause` | 0 | [Agents Issue Format Guard **success**](https://github.com/stranske/Workflows/actions/runs/36384250169) on `main`; no `Gate` runs on branch | 35 (18 `priority:*` / 35 impl) |
| Travel-Plan-Permission | 0 / — | 0 | [CI **success**](https://github.com/stranske/Travel-Plan-Permission/actions/runs/36330835711) on `1647cec` | 33 (7 / 33) |
| Trend_Model_Project | 0 / — | 0 | [CI **success**](https://github.com/stranske/Trend_Model_Project/actions/runs/36355095632) on `069e070` | 0 (0 / 0 impl; durable trackers only) |
| Portable-Alpha-Extension-Model | 0 / — | 0 | [CI **success**](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/36356635050) on `75ad1fb` | 2 (0 / 2 impl — **no `priority:*`**) |
| Counter_Risk | 0 / — | 0 | **red** [CI **failure**](https://github.com/stranske/Counter_Risk/actions/runs/36360361159) on `af156e8` — `black --check` would reformat `tests/pipeline/test_langsmith_fleet_data_quality_status.py` (confirmed on clone) | 1 (1 / 1) |
| Manager-Database | 0 / — | 0 | **red** [CI **failure**](https://github.com/stranske/Manager-Database/actions/runs/36362664895) on `4e384db` — `Docker stack smoke` / MinIO `unauthorized` (Python CI jobs green) | 0 (0 / 0 impl; durable trackers only) |
| Inv-Man-Intake | 0 / — | 0 | [CI **success**](https://github.com/stranske/Inv-Man-Intake/actions/runs/36370204483) on `209f989` | 2 (2 / 2) |
| Pension-Data | 0 / — | 0 | [CI **success**](https://github.com/stranske/Pension-Data/actions/runs/36373780606) on `062bd84` | 3 (2 / 3 impl) |

**Silent claims:** [#3568](https://github.com/stranske/Workflows/issues/3568) — stale `agent:retry` (~75h, no open PR). **Not released:** owner comments forbid further auto-pilot until verify:compare PASS on merged #3569.

**Stalled agent PRs:** 0 reroutes (no open `agent:*` PR idle >4h without `agent:auto` in covered repos).

**Priority gaps:** Workflows 18/35, Travel-Plan-Permission 7/33, Portable-Alpha-Extension-Model 0/2 ([#2321](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2321), [#2322](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2322)), Pension-Data 2/3 ([#935](https://github.com/stranske/Pension-Data/issues/935) missing `priority:*`).

**Red main (offload — no PR):** Counter_Risk needs a one-file `black` autofix on `main`. Manager-Database Docker/MinIO auth is not a safe blind code patch.

## Genuinely needs the owner

- Workflows [#3123](https://github.com/stranske/Workflows/issues/3123) — confirm whether LangSmith observability tracker degradation still requires `needs-human` or can clear after pause review.
- Workflows [#3596](https://github.com/stranske/Workflows/issues/3596) — refresh or rotate `CODEX_AUTH_JSON` before expiry (credential).
- Manager-Database — restore Docker Hub / MinIO pull credentials for `Docker stack smoke` on `main`, or disable that job until credentials are valid.

**Mutations this pass:** `gh issue edit` on Workflows #3586, #3606, #3607 (body + removed `agents:auto-pilot-pause`). **No** `gh pr create` / git push (offload).

**Confidence:** High on live GitHub reads and repairs (~2026-09-28T06:35Z). **Objection:** Manager-Database’s failing job is infra auth, not the FK/schema defect from 2026-09-27 — treating it as “same red main” would mis-route a fix. **Uncertainty:** Whether edited issues #3586/#3607 pass the format guard on next optimizer pass (bodies follow #3605 template; not re-run guard in this pass).
