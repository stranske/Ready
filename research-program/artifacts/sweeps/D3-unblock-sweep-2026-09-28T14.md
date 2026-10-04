# D3 unblock sweep — 2026-09-28T14 (attempt 1)

**Coverage (8/14):** Workflows → Pension-Data in `SUPPORTED_REPOS` order (Orchestrator excluded). **Deferred:** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic.

| Repository | Frozen (repaired / left for owner) | Stalled PR reroutes | Default branch | Agent-ready supply |
|---|---|---:|---|---:|
| Workflows | **3 repaired** [#3607](https://github.com/stranske/Workflows/issues/3607), [#3611](https://github.com/stranske/Workflows/issues/3611), [#3612](https://github.com/stranske/Workflows/issues/3612) — format-cap / missing Tasks+AC; dropped `agents:auto-pilot-pause` / **1 left** [#3123](https://github.com/stranske/Workflows/issues/3123) `needs-human` LangSmith tracker | 0 | [Agents Issue Format Guard **success**](https://github.com/stranske/Workflows/actions/runs/36254593970) on `main`; no `Gate`/`CI` on branch | 27 (14 `priority:*` / 27 impl) |
| Travel-Plan-Permission | 0 / — | 0 | [CI **success**](https://github.com/stranske/Travel-Plan-Permission/actions/runs/36330835711) on `1647cec` | 32 (6 / 32) |
| Trend_Model_Project | 0 / — | 0 | [CI **success**](https://github.com/stranske/Trend_Model_Project/actions/runs/36355095632) on `069e070` | 0 (0 / 0 impl; durable trackers only) |
| Portable-Alpha-Extension-Model | 0 / — | 0 | [CI **success**](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/36356635050) on `75ad1fb` | 2 (0 / 2 impl — **no `priority:*`**) |
| Counter_Risk | 0 / — | 0 | **red** [CI **failure**](https://github.com/stranske/Counter_Risk/actions/runs/36403540930) on `ff4bc19` — `black --check` would reformat `tests/pipeline/test_langsmith_fleet_data_quality_status.py` | 0 (0 / 0 impl; durable trackers only) |
| Manager-Database | 0 / — | 0 | **red** [CI **failure**](https://github.com/stranske/Manager-Database/actions/runs/36362664895) on `4e384db` — `Docker stack smoke` / MinIO `unauthorized` (Python CI jobs green on earlier heads) | 0 (0 / 0 impl; durable trackers only) |
| Inv-Man-Intake | 0 / — | 0 | [CI **success**](https://github.com/stranske/Inv-Man-Intake/actions/runs/36370204483) on `209f989` | 2 (2 / 2) |
| Pension-Data | 0 / — | 0 | [CI **success**](https://github.com/stranske/Pension-Data/actions/runs/36373780606) on `062bd84` | 3 (2 / 3 impl) |

**Silent claims:** [#3568](https://github.com/stranske/Workflows/issues/3568) — stale `agent:retry` (~83h, no open PR). **Not released:** owner comment on #3568 directs work through merged #3569 and verify:compare PASS before auto-pilot resumes.

**Stalled agent PRs:** 0 reroutes (no open `agent:*` PR idle >4h without `agent:auto` in covered repos).

**Priority gaps:** Workflows 14/27, Travel-Plan-Permission 6/32, Portable-Alpha-Extension-Model 0/2 ([#2321](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2321), [#2322](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2322)), Pension-Data 2/3 ([#935](https://github.com/stranske/Pension-Data/issues/935) missing `priority:*`).

**Red main (offload — no PR):** Counter_Risk needs a one-file `black` autofix on `tests/pipeline/test_langsmith_fleet_data_quality_status.py`. Manager-Database Docker/MinIO auth is not a safe blind code patch.

## Genuinely needs the owner

- Workflows [#3123](https://github.com/stranske/Workflows/issues/3123) — confirm whether LangSmith observability tracker degradation still requires `needs-human` or can clear after pause review.
- Workflows [#3596](https://github.com/stranske/Workflows/issues/3596) — refresh or rotate `CODEX_AUTH_JSON` before expiry (credential).
- Manager-Database — restore Docker Hub / MinIO pull credentials for `Docker stack smoke` on `main`, or disable that job until credentials are valid.

**Mutations this pass:** `gh issue edit` on Workflows #3607, #3611, #3612 (body + removed `agents:auto-pilot-pause`). **No** `gh pr create` / git push (offload).

**Confidence:** High on live GitHub reads and repairs (~2026-09-28T14:39Z). **Objection:** #3607’s prior “repair” at 06:00 left a task bullet the format guard rejects in isolation; this pass inlined `node --test` and file paths in every Tasks line. **Uncertainty:** Whether #3611/#3612 bodies satisfy the guard without triggering another optimizer cap (paths verified on `main` via API).
