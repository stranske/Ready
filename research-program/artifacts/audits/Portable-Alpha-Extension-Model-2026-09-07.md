# Portable Alpha Extension Model — demand-driven audit report

- **Unit:** `D-audit-Portable-Alpha-Extension-Model--2026-09-07T17-01-44Z`
- **Audit Date:** 2026-09-07
- **Target Repository:** `stranske/Portable-Alpha-Extension-Model`
- **Audited Commit (HEAD/main):** `59cb12be9d4b06434d41bc1b71612167ea6d9cfc`
- **Filing Outcome:** 10 verified issues filed (#2278–#2287: 7 P1, 3 P2)
- **Format Verification:** 10/10 PASS on repository-native `issue_format.py` (0 errors, 0 advisories); GitHub Actions `Agents Issue Format Guard` verified with 0 rejections / 0 comments.
- **Intake Log:** 10 rows appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.

---

## Executive Summary

A comprehensive, multi-dimensional audit of `stranske/Portable-Alpha-Extension-Model` was conducted following the `repo-audit` methodology across all 8 dimensions: code quality & numeric correctness, duplication, functionality & wiring, observed design/UX, public field comparators, missed opportunities, tool integration, and local automation.

The core Monte Carlo engine and PSD projection mathematics are robust and well-structured. However, the audit identified 10 concrete, adversarially verified defect classes spanning simulation parameter sweep compilation, fee schedule wiring, financing cost scaling, random number stream coupling, confidence interval statistical calibration, run bundle manifest finalization, UI provenance binding, wheel packaging of sample assets, default sample data sizing, and Plotly 7 image export compatibility.

All 10 findings were verified with isolated deterministic reproductions, compiled into strict `docs/AGENT_ISSUE_FORMAT.md` work orders with verified repo-relative file:line citations and deliberate-break acceptance gates, and filed to GitHub under authorized refill execution.

---

## Filed and Verified Issues Backlog

| Issue | Priority | Title | Labels | Repo Citations | Reproduction / Proof |
|---|---|---|---|---|---|
| [#2278](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2278) | P1 | Recompile derived agents for sweep and allocation overrides | `bug`, `engine`, `priority: high` | `pa_core/sweep.py:610`, `pa_core/sleeve_suggestor.py:281`, `pa_core/config.py:674`, `pa_core/agents/registry.py:57` | Deterministic theta/allocation deltas are zero without re-compiling derived agent objects; control yields 0.2682 delta. |
| [#2279](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2279) | P1 | Apply configured fee schedules to parameter sweeps | `bug`, `engine`, `priority: high` | `pa_core/sweep.py:715-725`, `pa_core/simulations.py:86-128`, `pa_core/orchestrator.py` | Sweeps call `simulate_agents` without `fee_schedule`, leaving returns gross of fees while single runs apply them. |
| [#2280](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2280) | P1 | Scale InternalPA financing by sleeve contribution share | `bug`, `engine`, `priority: high` | `pa_core/agents/internal_pa.py:24`, `pa_core/agents/external_pa.py:22`, `pa_core/agents/active_ext.py:24` | `InternalPAAgent` subtracts unscaled monthly financing series, charging small sleeves the same absolute dollar drag as 100% sleeves. |
| [#2281](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2281) | P2 | Preserve common random draws for InternalPA sweep financing | `bug`, `engine`, `priority: medium` | `pa_core/sweep.py:603,711`, `pa_core/sim/paths.py` | `resolve_internal_pa_financing_series` consumes `fin_rngs['internal']` already advanced by `draw_financing_series`, coupling random streams. |
| [#2282](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2282) | P1 | Calibrate the exported CVaR confidence intervals | `bug`, `engine`, `priority: high` | `pa_core/sim/metrics.py:437-466`, `pa_core/sim/metrics.py:23` | CVaR confidence interval computes SE only over tail realizations, ignoring quantile threshold estimation variance (81% empirical coverage on 95% CI). |
| [#2283](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2283) | P1 | Finalize manifest provenance before creating run bundles | `bug`, `data`, `priority: high` | `pa_core/cli.py:1414`, `pa_core/cli.py:910-955`, `pa_core/run_artifact_bundle.py:50-75` | Bundles are created before `_emit_run_end()` finalizes warnings, timing, and costs; bundled copy contains stale null metadata. |
| [#2284](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2284) | P2 | Keep Run Logs provenance bound to the selected run | `bug`, `ui`, `priority: medium` | `dashboard/pages/7_Run_Logs.py:59-68` | When run-end metadata is missing, page falls back to any `manifest.json` in CWD, falsely binding unrelated run provenance. |
| [#2285](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2285) | P2 | Ship asset and portfolio samples in installed packages | `bug`, `ui`, `priority: medium` | `dashboard/utils.py:146,177`, `pyproject.toml:88-89` | `dashboard/utils.py` resolves repo `templates/` directory which is omitted from wheel package data, breaking non-editable installs. |
| [#2286](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2286) | P1 | Make the bundled Asset Library sample load with defaults | `bug`, `ui`, `priority: high` | `templates/asset_timeseries_wide_returns.csv:2`, `dashboard/pages/1_Asset_Library.py:116,204` | Sample CSV contains 24 monthly observations, but Asset Library UI defaults to `min_obs=36`, failing the one-click onboarding path. |
| [#2287](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2287) | P1 | Support Plotly 7 image export or constrain installation | `bug`, `infra`, `priority: high` | `pa_core/viz/export_backend.py:88,100`, `pyproject.toml:119` | Passing `engine="kaleido"` crashes under Plotly 7.0.0+ where keyword was removed; `pyproject.toml` lacks upper version bound. |

---

## Dimension Breakdown & Verification Details

### 1. Code Correctness & Numeric Invariants (D1)
- **Derived Agent Stale State (#2278):** `ModelConfig.model_copy(update=overrides)` creates a new config instance with updated top-level parameters (`theta`, `active_share`, sleeve capitals) but leaves `self.agents` holding the agent dictionaries compiled during the initial load in `pa_core/config.py:674`. When `sweep.py` or `sleeve_suggestor.py` calls `build_from_config()`, the old compiled agent parameters are used, making sweep variations in allocation and theta inert.
- **Unscaled InternalPA Financing (#2280):** In `InternalPAAgent.monthly_returns()`, the financing stream is subtracted directly (`return self.p.alpha_share * alpha_stream - financing`) rather than scaled by `self.p.beta_share` (capital contribution weight), unlike `ExternalPAAgent` and `ActiveExtensionAgent`.
- **CVaR Standard Error Underestimation (#2282):** `cvar_confidence_interval()` in `pa_core/sim/metrics.py:459` estimates the standard error of conditional value at risk as $s_{tail}/\sqrt{n_{tail}}$. Because the VaR threshold is itself an estimated quantile from the same sample, the variance of the threshold estimator adds substantial covariance. In 1,000 independent normal calibration trials (2,000 draws each, seed 20260907), nominal 95% confidence intervals achieved only 81.0% empirical coverage.

### 2. Duplication & Consolidation (D2)
- Sweep and sleeve optimization both implement ad-hoc parameter overriding without derived agent re-compilation. Issue #2278 consolidates these two consumer paths into a unified agent-refresh mechanism.

### 3. Functionality & Wiring (D3)
- **Fee Schedules in Sweeps (#2279):** Single runs via `SimulatorOrchestrator` pass `fee_schedule` to `simulate_agents()`, reporting net returns. The parameter sweep loop in `pa_core/sweep.py:715-725` omitted the argument entirely, causing sweep results and grid summaries to silently report gross returns.
- **RNG Coupling (#2281):** In `pa_core/sweep.py:711`, `resolve_internal_pa_financing_series` draws from `fin_rngs.get("internal")`, which is the exact same generator already advanced by `draw_financing_series()`. This couples internal financing draws to general financing draws across iterations.
- **Bundle Provenance Timing (#2283):** In `pa_core/cli.py:1414`, `_maybe_write_bundle()` writes `bundle.json` and copies `manifest.json` before `_emit_run_end()` at line 1415 records run warnings, duration timing, and cost metrics into the manifest. As a result, the bundled manifest has `warnings=null` and `cost=null`.

### 4. Observed Design & UX (D4)
- **Asset Library Default Sample Failure (#2286):** `dashboard/pages/1_Asset_Library.py` loads `templates/asset_timeseries_wide_returns.csv` (24 rows), but the page's default minimum observation count is 36. Clicking "Load bundled sample" raises an unhandled `ValueError` at line 204.
- **Run Logs Ambiguous Provenance (#2284):** `dashboard/pages/7_Run_Logs.py:61` glob-searches `Path.cwd()` for `manifest.json` when the selected run lacks a `run_end.json` manifest pointer. This displays the root repository manifest rather than indicating missing provenance.
- **Wheel Sample Resolution (#2285):** `dashboard/utils.py:146` resolves sample templates via parent directory traversal, which fails in non-editable wheel installations because `templates/` is not included in `[tool.setuptools.package-data]`.

### 5. Public Field & Ecosystem Compatibility (D5 / D7)
- **Plotly 7 Engine Keyword Removal (#2287):** Plotly 7 removed the `engine` keyword argument from `to_image()` and `write_image()`. `pa_core/viz/export_backend.py:88,100` explicitly passes `engine="kaleido"`. While the current lockfile pins Plotly 6.9.0, `pyproject.toml:119` specifies `plotly>=5.24.1` with no upper bound, causing fresh installations without a lockfile to fail on CLI workbook and chart exports.

### 6. Opportunities & Local Automation (D6 / D8)
- Live issue tracking, format-guard CI enforcement, and intake logging were completed in full.

---

## Reconciliation & Quality Proofs

- **Local Format Validator:** All 10 issue bodies validated using `python3 .github/scripts/issue_format.py` inside `clones/Portable-Alpha-Extension-Model/` — **10/10 PASS** with 0 errors and 0 advisories.
- **Remote Format Guard:** Monitored GitHub Actions runs for workflow `agents-issue-format-guard.yml` across all 10 issues (#2278–#2287). All runs completed with 0 rejections, 0 failure comments, and clean format acceptance.
- **Intake Logging:** Appended 10 records to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Continuity Artifacts:** Updated `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/AUDIT_LEDGER.md` and `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Portable-Alpha-Extension-Model/README.md`.
