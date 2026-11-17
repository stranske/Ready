# D4 verification — 2026-11-17T00

Checked 2026-11-16 (UTC run ~2026-11-17T00:08Z). Discovery covered the 36-hour
window beginning **2026-11-15T12:08:00Z** across `SUPPORTED_REPOS` in
`handoff.sh`, excluding Orchestrator and owner-excluded `stranske/Collab-Admin`.
**75** merged PRs were found in the window. Template-sync and `deps: sync dev
tool versions` chores were skipped for verify (two waves ~2026-11-15T19:05Z and
~2026-11-16T01:03–08:03Z plus Workflows#4705). **20** issue-linked merges were
verified oldest-first (API cap). No GitHub secondary-rate-limit response. This
offload did not post GitHub comments, reopen issues, or file follow-ups
(read-only).

| Repo | PR | Issue | Verdict | Unmet criteria / evidence | Follow-up |
|---|---:|---|---|---|---|
| Doc-Lineage | [#183](https://github.com/stranske/Doc-Lineage/pull/183) | [#182](https://github.com/stranske/Doc-Lineage/issues/182) | **VERIFIED** | Squash diff: `links.py` `_mirror_url` treats `mirror_root "."`; named `test_published_legal_variable_resolves_from_claims_dir` + file gate; deliberate-break evidence. Not re-run locally. | — |
| Portable-Alpha-Extension-Model | [#2512](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2512) | [#2511](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2511) | **VERIFIED** | `3_Scenario_Wizard.py` persists `wizard_run_requested`; AppTest named gate + evidence. | — |
| Manager-Database | [#1918](https://github.com/stranske/Manager-Database/pull/1918) | [#1916](https://github.com/stranske/Manager-Database/issues/1916) | **VERIFIED** | `alerts/db.py` conviction replay identity without `occurred_at`; named + file tests with documented break/revert. | — |
| trip-planner | [#2035](https://github.com/stranske/trip-planner/pull/2035) | [#2033](https://github.com/stranske/trip-planner/issues/2033) | **VERIFIED** | `budget.py` counts unallocated category spend in `actual_total`; API + frontend tests. | — |
| Fine-Art-Archive | [#891](https://github.com/stranske/Fine-Art-Archive/pull/891) | [#890](https://github.com/stranske/Fine-Art-Archive/issues/890) | **VERIFIED** | `eink/targets.py` median on artwork crop only (contain letterbox); named duotone test + evidence. | — |
| Deliverable-Render | [#140](https://github.com/stranske/Deliverable-Render/pull/140) | [#139](https://github.com/stranske/Deliverable-Render/issues/139) | **VERIFIED** | `validate.py` rejects non-dict native locators with diagnostic; parametrized named test. | — |
| Workflows | [#4707](https://github.com/stranske/Workflows/pull/4707) | [#4700](https://github.com/stranske/Workflows/issues/4700) | **VERIFIED** | `weekly_metrics_artifacts.js` try/catch on repo listing; node test + consumer template sync. | — |
| Trend_Model_Project | [#6226](https://github.com/stranske/Trend_Model_Project/pull/6226) | [#6225](https://github.com/stranske/Trend_Model_Project/issues/6225) | **VERIFIED** | `monte_carlo/runner.py` user-weighted NAV when scenario costs absent; named + invariance tests. | — |
| learning-management-system | [#832](https://github.com/stranske/learning-management-system/pull/832) | [#831](https://github.com/stranske/learning-management-system/issues/831) | **VERIFIED** | `project-plan.md` points at locked protocol; docs consistency named test. | — |
| Workflows | [#4704](https://github.com/stranske/Workflows/pull/4704) | [#4698](https://github.com/stranske/Workflows/issues/4698) | **VERIFIED** | `validate_backplane_registry.py` surfaces expired deferrals as stale warnings; CLI/test gates + evidence. | — |
| Workflows | [#4713](https://github.com/stranske/Workflows/pull/4713) | [#4697](https://github.com/stranske/Workflows/issues/4697) | **VERIFIED** | Stops live workflow recount in sealed #3743 validators; re-sealed bindings; `test_shebang_rejection_ignores_new_workflows.py`. | — |
| Workflows | [#4710](https://github.com/stranske/Workflows/pull/4710) | [#4702](https://github.com/stranske/Workflows/issues/4702) | **VERIFIED** | Workflow catalog docs match repo files; existence test + deliberate-break evidence pattern. | — |
| Workflows | [#4709](https://github.com/stranske/Workflows/pull/4709) | [#4701](https://github.com/stranske/Workflows/issues/4701) | **VERIFIED** | `check_checks_reported.py` ordering favors timestampless queued over older pass; expanded pytest file. | — |
| Workflows | [#4708](https://github.com/stranske/Workflows/pull/4708) | [#4699](https://github.com/stranske/Workflows/issues/4699) | **VERIFIED** | `maint-66-monthly-audit.yml` removes erroneous `jq -s`; named maint66 test. | — |
| Inv-Man-Intake | [#1078](https://github.com/stranske/Inv-Man-Intake/pull/1078) | [#1077](https://github.com/stranske/Inv-Man-Intake/issues/1077) | **VERIFIED** | Repository/integration identity: same fund name under two firms stays distinct; named + file tests. | — |
| trip-planner | [#2036](https://github.com/stranske/trip-planner/pull/2036) | [#2034](https://github.com/stranske/trip-planner/issues/2034) | **VERIFIED** | `check_full_product_verification.py` probes distinct TP3 component totals; named script test + contract drift test. | — |
| Counter_Risk | [#1249](https://github.com/stranske/Counter_Risk/pull/1249) | [#1248](https://github.com/stranske/Counter_Risk/issues/1248) | **VERIFIED** | Squash hunk is tests/evidence only; new tests exercise `_refresh_ppt_links` FAILURE path and bytecode needle forbids hollow `except: continue` in `run.py`. Assumes merge tip matches needle (not re-run pytest here). | — |
| Manager-Mosaic | [#156](https://github.com/stranske/Manager-Mosaic/pull/156) | [#155](https://github.com/stranske/Manager-Mosaic/issues/155) | **VERIFIED** | `discrepancy.py` exact Fraction relative spread; parametrized boundary test + red/green evidence. | — |
| Travel-Plan-Permission | [#1750](https://github.com/stranske/Travel-Plan-Permission/pull/1750) | [#1748](https://github.com/stranske/Travel-Plan-Permission/issues/1748) | **VERIFIED** | `exception_decisions.py` rejects foreign namespace before approve; named parametrized API test. | — |
| Pension-Data | [#1033](https://github.com/stranske/Pension-Data/pull/1033) | [#1031](https://github.com/stranske/Pension-Data/issues/1031) | **VERIFIED** | `build_workspace_bundle.py` rejects failed/foreign/out-of-run pilot artifacts; named test + deliberate-break docs. | — |

## Skipped / deferred (same window)

- **Chores (not verified):** template-sync merges on 15 fleet repos (×2),
  `deps: sync dev tool versions` (×2), `Workflows#4705` PyPI dev pins,
  `Travel-Plan-Permission#1749`, etc.
- **Earlier window merges** already ledgered in
  [`D4-verify-merged-2026-11-15T23.md`](D4-verify-merged-2026-11-15T23.md), including **PARTIAL**
  [`Workflows#4687`](https://github.com/stranske/Workflows/pull/4687) (live consumer sync proof).
- **Not verified this run (cap):** among others
  [`Ready#685`](https://github.com/stranske/Ready/pull/685) / [#683](https://github.com/stranske/Ready/issues/683),
  [`Workflows#4712`](https://github.com/stranske/Workflows/pull/4712),
  [`Workflows#4717`](https://github.com/stranske/Workflows/pull/4717) (no issue close).

## Critical findings

- **Outcome count:** **20 VERIFIED**, **0 PARTIAL**, **0 NOT IMPLEMENTED** in this ledger (cap 20).
- **Counter_Risk#1249:** strongest reservation — squash diff does not show `run.py` edits;
  verdict rests on in-PR tests that import production `_refresh_ppt_links` and a source needle
  test. A merge that only added tests atop an unfixed `run.py` would fail CI; confidence is
  **medium-high** without a local pytest re-run.
- **Carry-over:** `Workflows#4687` partial live-sync criterion from the prior D4 run remains open;
  not re-triaged here.
- No linked issues in this batch carried `Reproduction:` blocks; none reopened.
- Offload constraint: no GitHub writes; no follow-ups filed.

## Confidence

**High** on diff-read verdicts for P2 fixes with production hunks + named gates (Doc-Lineage,
Deliverable-Render, Manager-Mosaic, Pension-Data, TMP#6226, Workflows 4704–4713). **Medium-high**
on Counter_Risk#1249 (tests-only squash). Local pytest re-run on merge SHAs would raise Counter_Risk
and bootstrap PRs to **high**.