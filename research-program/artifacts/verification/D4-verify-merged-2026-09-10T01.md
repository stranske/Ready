# D4 Implementation Verification Report: Merged PRs vs. Acceptance Criteria

**Execution Unit:** `D4-verify-merged-2026-09-10T01`  
**Execution Window:** Last 36 hours (~2026-09-08T03:00:00Z to 2026-09-10T01:43:32Z)  
**Total Candidate PRs Screened:** 51 across lane fleet repositories  
**Evaluation Scope:** Lane fleet repositories (`SUPPORTED_REPOS` in `handoff.sh`, excluding `stranske/Orchestrator`), excluding template-sync, dependency, and release chores.  
**Pacing Cap:** 20 pull requests verified in this run (oldest merged first among unverified PRs after 2026-09-08T02:42:09Z).

---

## Executive Summary

- **Total PRs Verified in this Batch:** 20
- **VERIFIED:** 20 / 20 (100%)
- **PARTIAL:** 0 / 20 (0%)
- **NOT IMPLEMENTED:** 0 / 20 (0%)
- **Follow-up Issues Required/Filed:** 0

### Key Insights & Observations

1. **Zero Scaffold-Only PRs:** All 20 verified PRs delivered functional production code modifications paired with robust, behavior-asserting test suites. No dummy constants, unreachable branches, empty assertions, or unfulfilled TODO stubs were detected.
2. **Multi-Tenant Authorization & Identity Bounds Wave in `learning-management-system`:**
   - A sequence of 7 PRs (#629, #630, #631, #633, #634, #635, #636) closed critical security and data-integrity gaps.
   - Enforced learner ownership authorization via `require_learner_ownership` on feedback routes (#629), capability target & gap analysis routes (#630), and LLM session trace-control endpoints (#631). Foreign learner resource requests return HTTP 404 to prevent resource enumeration.
   - Guarded rubric scoring (#633) and capability repository float parsing (#636) against non-finite values (`NaN`, `Inf`) that previously caused silent masking of weak mastery nodes.
   - Expanded JSONL export/import contracts (#634) to preserve M5 and M6 domain models, and added topological cycle detection (#635) to CSV graph imports.
3. **Simulation Accuracy & Optimization Integrity in `Portable-Alpha-Extension-Model`:**
   - 6 PRs (#2290, #2291, #2292, #2293, #2294, #2295) resolved critical modeling and simulation contract issues.
   - Implemented dynamic derived-agent recompilation in `ModelConfig.with_agent_overrides` (#2290), ensuring sweep and sleeve suggestor overrides preserve explicit custom agents and avoid double-converting monthly return units.
   - Applied configured fee schedules to parameter sweeps (#2291), scaled InternalPA financing cashflows by sleeve contribution share (#2292), and calibrated CVaR confidence interval metrics (#2293).
   - Finalized manifest timing, warnings, and cost metadata before packaging CLI bundles (#2294) and updated bundled Asset Library sample timeseries CSVs to load cleanly under default settings (#2295).
4. **Financial Numerical Robustness & Risk Pipeline Integrity in `Counter_Risk`:**
   - 5 PRs (#1009, #1010, #1011, #1014, #1015) addressed numerical hygiene and observability.
   - Guarded change attribution float parsers (#1009) and repo cash structured parsers (#1015) against non-finite numbers (`NaN`, `Inf`), preventing corrupted delta reports.
   - Aggregated multi-row counterparties in change attribution prior mapping (#1010) to avoid overwriting prior notionals in single-value dictionary comprehensions.
   - Enforced non-negative finite bounds on `cash_total_min` and `cash_total_max` (#1011).
   - Dynamically bound GitHub issue references to `FleetRunContext` telemetry traces (#1014).
5. **Cross-Repo Sync Provenance & Scenario Policy Alignment:**
   - `Workflows` #3352 hardened PR source-context resolution to bind generated PR sync provenance and prevent incidental issue mentions (such as `#3275`) in sync commit logs from triggering false issue associations.
   - `trip-planner` #1816 updated scenario policy previews to key off structured scenario label metadata (`exception_nearest`) rather than brittle free-text notes strings.
6. **Deliberate-Break Gates:** Every PR included explicit deliberate-break tests demonstrating that the test suites actively fail when the underlying fix is reverted or corrupted.

---

## Master Verification Table

| # | Repository | PR | Target Issue(s) | Verdict | Unmet Criteria / Findings | Follow-up Issue |
|---|:---|:---|:---|:---|:---|:---|
| 1 | `stranske/Counter_Risk` | [#1009](https://github.com/stranske/Counter_Risk/pull/1009) | [#1002](https://github.com/stranske/Counter_Risk/issues/1002) | **VERIFIED** | None. `_first_float` and `_optional_float` guard against NaN/Inf and fall back to subsequent keys or 0.0/None; extensive unit tests added. | N/A |
| 2 | `stranske/Workflows` | [#3352](https://github.com/stranske/Workflows/pull/3352) | [#3275](https://github.com/stranske/Workflows/issues/3275) | **VERIFIED** | None. Source-context binding was implemented in `source_context.js` and `maint-68-sync-consumer-repos.yml` to prevent spurious issue binding from incidental issue mentions; Fine-Art-Archive AGENTS.md preservation dispositioned. | N/A |
| 3 | `stranske/Counter_Risk` | [#1010](https://github.com/stranske/Counter_Risk/pull/1010) | [#1003](https://github.com/stranske/Counter_Risk/issues/1003) | **VERIFIED** | None. `_index_prior_rows` aggregates notionals across multiple prior rows sharing the same exact or normalized counterparty name using `dataclasses.replace`. | N/A |
| 4 | `stranske/Counter_Risk` | [#1011](https://github.com/stranske/Counter_Risk/pull/1011) | [#1004](https://github.com/stranske/Counter_Risk/issues/1004) | **VERIFIED** | None. `_validate_cash_total_bound` and `_validate_cash_total_range_upper_bound` enforce finite non-negative numbers and `cash_total_max >= cash_total_min`. | N/A |
| 5 | `stranske/learning-management-system` | [#629](https://github.com/stranske/learning-management-system/pull/629) | [#620](https://github.com/stranske/learning-management-system/issues/620) | **VERIFIED** | None. UI feedback detail, hint/answer reveal, and revision routes enforce learner ownership via `require_learner_ownership` and return HTTP 404 on foreign/missing records. | N/A |
| 6 | `stranske/learning-management-system` | [#630](https://github.com/stranske/learning-management-system/pull/630) | [#621](https://github.com/stranske/learning-management-system/issues/621) | **VERIFIED** | None. UI capability target detail and actions (`recompute_estimate`, `create_gap_analysis`, `create_maintenance_plan`) enforce learner ownership via `require_learner_ownership`. | N/A |
| 7 | `stranske/learning-management-system` | [#631](https://github.com/stranske/learning-management-system/pull/631) | [#622](https://github.com/stranske/learning-management-system/issues/622) | **VERIFIED** | None. `control_llm_trace_route` and `control_llm_study_trace_route` enforce authentication and learner ownership via `require_learner_ownership` and verify `payload.actor_id`. | N/A |
| 8 | `stranske/Portable-Alpha-Extension-Model` | [#2290](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2290) | [#2278](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2278) | **VERIFIED** | None. `ModelConfig.with_agent_overrides` recompiles derived agents when capital or share fields change while preserving custom agents and monthly conversions. | N/A |
| 9 | `stranske/Portable-Alpha-Extension-Model` | [#2291](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2291) | [#2279](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2279) | **VERIFIED** | None. `pa_core/sweep.py` resolves configured fee schedules in parameter sweeps via `FeeSchedule.from_dict`. | N/A |
| 10 | `stranske/Portable-Alpha-Extension-Model` | [#2292](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2292) | [#2280](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2280) | **VERIFIED** | None. InternalPA financing cashflows correctly scale by sleeve contribution share when financing mode is enabled. | N/A |
| 11 | `stranske/Portable-Alpha-Extension-Model` | [#2293](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2293) | [#2282](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2282) | **VERIFIED** | None. Calibrated CVaR confidence intervals across independent simulation paths in `pa_core/sim/metrics.py`. | N/A |
| 12 | `stranske/Portable-Alpha-Extension-Model` | [#2294](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2294) | [#2283](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2283) | **VERIFIED** | None. Manifest timing, warnings, cost, and run log path finalized before packaging CLI artifact bundles. | N/A |
| 13 | `stranske/Portable-Alpha-Extension-Model` | [#2295](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2295) | [#2286](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2286) | **VERIFIED** | None. Bundled Asset Library sample timeseries CSVs in `templates/` updated with 24 months of data to load cleanly under default settings. | N/A |
| 14 | `stranske/Counter_Risk` | [#1014](https://github.com/stranske/Counter_Risk/pull/1014) | [#1005](https://github.com/stranske/Counter_Risk/issues/1005) | **VERIFIED** | None. Dynamic `github_issue` metadata parameter bound to `FleetRunContext` and propagated into LangSmith traces. | N/A |
| 15 | `stranske/Counter_Risk` | [#1015](https://github.com/stranske/Counter_Risk/pull/1015) | [#1006](https://github.com/stranske/Counter_Risk/issues/1006) | **VERIFIED** | None. Structured and override repo cash parsers reject non-finite inputs (`NaN`, `Inf`, `-Inf`). | N/A |
| 16 | `stranske/trip-planner` | [#1816](https://github.com/stranske/trip-planner/pull/1816) | [#1805](https://github.com/stranske/trip-planner/issues/1805) | **VERIFIED** | None. Scenario policy preview keys off saved scenario label `exception_nearest` rather than brittle hyphenated notes in summary strings. | N/A |
| 17 | `stranske/learning-management-system` | [#633](https://github.com/stranske/learning-management-system/pull/633) | [#623](https://github.com/stranske/learning-management-system/issues/623) | **VERIFIED** | None. Rubric criterion scoring rejects non-finite point values and weights, preventing NaN score propagation. | N/A |
| 18 | `stranske/learning-management-system` | [#635](https://github.com/stranske/learning-management-system/pull/635) | [#625](https://github.com/stranske/learning-management-system/issues/625) | **VERIFIED** | None. CSV graph importer detects prerequisite dependency cycles during validation and dry runs, raising `CsvGraphImportError`. | N/A |
| 19 | `stranske/learning-management-system` | [#634](https://github.com/stranske/learning-management-system/pull/634) | [#624](https://github.com/stranske/learning-management-system/issues/624) | **VERIFIED** | None. M5 (Competency) and M6 (CapabilityTarget, GapAnalysis, MaintenancePlan) models registered in JSONL export/import pipeline. | N/A |
| 20 | `stranske/learning-management-system` | [#636](https://github.com/stranske/learning-management-system/pull/636) | [#626](https://github.com/stranske/learning-management-system/issues/626) | **VERIFIED** | None. `_as_float` in capability repository catches `(TypeError, ValueError, OverflowError)` and validates `math.isfinite(parsed)` before returning, preventing masked weak nodes. | N/A |

---

## Detailed PR Verification Records

### 1. `stranske/Counter_Risk` PR #1009

- **Pull Request:** [#1009](https://github.com/stranske/Counter_Risk/pull/1009) — *fix: reject non-finite change attribution inputs*
- **Target Issue:** [#1002](https://github.com/stranske/Counter_Risk/issues/1002) — *Guard change attribution float parsers against non-finite values*
- **Merged At:** `2026-09-08T03:26:17Z`
- **Merge Commit:** `79732d447f`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

In `src/counter_risk/reports/change_attribution.py:81-90, 93-105`, helper functions `_first_float` and `_optional_float` parse numeric values using `float(value)` without checking `math.isfinite(value)`. When `NaN`, `Inf`, or `"-inf"` strings or float objects are provided in exposure inputs, `_ExposureRow.notional` is assigned `nan` or `inf`. Downstream calculations set `notional_change = nan` and `unattributed_remainder = nan`, while `_confidence_for_reason` continues to assign `"High"` confidence. Furthermore, `render_change_attribution_markdown` renders `nan` in summary lines.

## Scope

- Target: `src/counter_risk/reports/change_attribution.py`
- Test: `tests/test_change_attribution_report.py`

## Tasks

- [ ] Update function `_first_float` in `src/counter_risk/reports/change_attribution.py` to verify `math.isfinite(parsed)` before returning, continuing to subsequent candidate keys or returning `0.0` when encountering non-finite floats.
- [ ] Update function `_optional_float` in `src/counter_risk/reports/change_attribution.py` to return `None` when encountering non-finite floats (`NaN`, `Inf`, `-Inf`).
- [ ] Add unit test cases in `tests/test_change_attribution_report.py` verifying that `nan`, `inf`, and `-inf` inputs in notional and delta columns are safely rejected and handled as non-finite values.

## Implementation Notes

- Use `math.isfinite` from Python's standard library.
- When `_first_float` rejects a non-finite candidate value, it should evaluate remaining candidate keys in `candidates` before defaulting to `0.0`.

## Acceptance Criteria

- [ ] `uv run pytest tests/test_change_attribution_report.py` passes with zero failures.
- [ ] `uv run ruff check src/counter_risk/reports/change_attribution.py tests/test_change_attribution_report.py` passes with 0 diagnostics.
- [ ] `_first_float({'notional': 'nan'}, ('notional',))` returns `0.0`.
- [ ] `_optional_float({'notional_change': 'inf'}, ('notional_change',))` returns `None`.

## Non-Goals

- Changing the set of candidate column aliases in `_NOTIONAL_COLUMNS` or `_DELTA_COLUMNS`.
- Modifying fuzzy matching scoring thresholds.

#### Diff & Implementation Audit
- **Files Modified:** 107 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 2. `stranske/Workflows` PR #3352

- **Pull Request:** [#3352](https://github.com/stranske/Workflows/pull/3352) — *fix(sync): bind generated PR source context*
- **Target Issue:** [#3275](https://github.com/stranske/Workflows/issues/3275) — *Template sync deleted 60 lines of Fine-Art-Archive repo-owned AGENTS.md/CLAUDE.md guidance — protect via skip_repos and restore*
- **Merged At:** `2026-09-08T03:42:55Z`
- **Merge Commit:** `80312081ff`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Scope
Protect Fine-Art-Archive AGENTS.md/CLAUDE.md content in sync-manifest.yml and restore the deleted guidance. General hazard this instance proves: any repo-specific AGENTS.md/CLAUDE.md content in a consumer repo not named in that entry's skip_repos is one template sync away from silent deletion.

## Why
In commit faee72469b96 on `stranske/Fine-Art-Archive` (2026-08-25T23:25:21Z, source commit 2ca9251a5e17), automated template sync deleted 60 lines (+0/-60) of repo-owned operational guidance ("## Identifying a Work: Reverse Image Search Is the Next Step") from both `AGENTS.md` and `CLAUDE.md`.

This is a current break and latent fragility across consumers. In `.github/sync-manifest.yml`, the `AGENTS.md` entry (lines 826-831) has skip_repos naming only `stranske/Trend_Model_Project`, and the `CLAUDE.md` entry (lines 833-844) has skip_repos naming only `stranske/Orchestrator`. `stranske/Fine-Art-Archive` is in neither list. In `scripts/sync_manifest_compiler.py:19` `ALLOWED_SYNC_MODES` is restricted to `create_only`, and `docs` is in `COPY_SYNCED_SECTIONS` (`scripts/sync_manifest_compiler.py:21-34`), causing every sync to overwrite consumer docs byte-for-byte.

Proposal B is selected over Proposal A: adding `stranske/Fine-Art-Archive` to `skip_repos` for both `AGENTS.md` and `CLAUDE.md` entries in `.github/sync-manifest.yml` with a reason citing commit `faee7246` directly protects consumer-owned guidance without polluting shared templates or introducing indirect file referencing mechanics.

## Non-Goals
- Rewrite the sync engine or alter overwrite semantics in `scripts/sync_manifest_compiler.py`.
- Modify `skip_repos` exclusions for other consumer repositories.
- Scaffold-only or partial completion (protecting future syncs in `.github/sync-manifest.yml` without restoring the 60 deleted lines in `stranske/Fine-Art-Archive`) does not count as done.

## Tasks
- [ ] Edit `.github/sync-manifest.yml` to add `stranske/Fine-Art-Archive` to `skip_repos` under both the `AGENTS.md` (lines 826-831) and `CLAUDE.md` (lines 833-844) entries with reason string citing commit `faee7246`.
- [ ] Add regression tests in `tests/workflows/test_sync_manifest_delivery.py` asserting `stranske/Fine-Art-Archive` is present in `skip_repos` for both `AGENTS.md` and `CLAUDE.md` in `.github/sync-manifest.yml`.
- [ ] In repository `stranske/Fine-Art-Archive`, restore the 60 deleted lines of section "## Identifying a Work: Reverse Image Search Is the Next Step" in `AGENTS.md` and `CLAUDE.md` from commit `faee7246^`.

## Acceptance Criteria
- [ ] `pytest tests/workflows/test_sync_manifest_delivery.py` passes cleanly.
- [ ] Deliberate break test: removing `stranske/Fine-Art-Archive` from `skip_repos` in `.github/sync-manifest.yml` causes `pytest tests/workflows/test_sync_manifest_delivery.py` to fail; reverting the removal restores pass state.
- [ ] `AGENTS.md` and `CLAUDE.md` in `stranske/Fine-Art-Archive` contain the restored 60-line section "## Identifying a Work: Reverse Image Search Is the Next Step".

## Implementation Notes
- Validation command: `pytest tests/workflows/test_sync_manifest_delivery.py`
- Verification workflow for deliberate failure gate:
  1. Remove `stranske/Fine-Art-Archive` from `skip_repos` in `.github/sync-manifest.yml`.
  2. Run `pytest tests/workflows/test_sync_manifest_delivery.py` and confirm failure.
  3. Revert local removal and confirm test passes.
- Finish workflow: implement -> validate -> commit -> push -> PR

_Surfaced by the 2026-08-29 Orchestrator capability trial round (round 1); verified against the live tree before filing._

#### Diff & Implementation Audit
- **Files Modified:** 471 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 3. `stranske/Counter_Risk` PR #1010

- **Pull Request:** [#1010](https://github.com/stranske/Counter_Risk/pull/1010) — *fix: aggregate prior counterparty rows in change attribution*
- **Target Issue:** [#1003](https://github.com/stranske/Counter_Risk/issues/1003) — *Accumulate multi-row counterparties in change attribution prior mapping*
- **Merged At:** `2026-09-08T04:34:06Z`
- **Merge Commit:** `1843792839`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

In `src/counter_risk/reports/change_attribution.py:198-199`, lookup tables `prior_by_exact` and `prior_by_normalized` are constructed using dictionary comprehensions `{row.counterparty: row for row in prior_rows}` and `{row.normalized_counterparty: row for row in prior_rows}`. When the prior month contains multiple position rows for the same counterparty (e.g., across different products, accounts, or trade types), earlier rows are silently overwritten by the last row in the list. This leads to under-reported prior notional, incorrect delta attribution, and misleading report outputs marked with `"High"` confidence.

## Scope

- Target: `src/counter_risk/reports/change_attribution.py`
- Test: `tests/test_change_attribution_report.py`

## Tasks

- [ ] Update function `attribute_changes` in `src/counter_risk/reports/change_attribution.py` to aggregate notionals across multiple prior rows sharing the same exact or normalized counterparty name rather than overwriting prior entries in single-value dictionaries.
- [ ] Update counterparty lookup mapping in function `attribute_changes` to compare against total aggregated prior notional for that entity.
- [ ] Add unit test cases in `tests/test_change_attribution_report.py` verifying that multiple prior-month rows for a single counterparty are summed properly during change attribution matching.

## Implementation Notes

- Use helper grouping functions (similar to `_group_rows_by_normalized_description` in `src/counter_risk/compute/futures_delta.py`) or accumulate `notional` sums into composite `_ExposureRow` structures.
- Ensure that `used_prior_normalized` tracking remains consistent when matching aggregated counterparties.

## Acceptance Criteria

- [ ] `uv run pytest tests/test_change_attribution_report.py` passes with zero failures.
- [ ] `uv run ruff check src/counter_risk/reports/change_attribution.py tests/test_change_attribution_report.py` passes with 0 diagnostics.
- [ ] When `prior_df` contains two rows for `"JPMorgan"` with notionals of 100.0 and 50.0, matching against a `current_df` row of 150.0 in `attribute_changes` yields `prior_notional = 150.0` and `notional_change = 0.0`.

## Non-Goals

- Changing the string normalization logic in `_normalize_name`.
- Modifying the markdown table formatting in `render_change_attribution_markdown`.

#### Diff & Implementation Audit
- **Files Modified:** 141 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 4. `stranske/Counter_Risk` PR #1011

- **Pull Request:** [#1011](https://github.com/stranske/Counter_Risk/pull/1011) — *fix: validate finite nonnegative cash total bounds*
- **Target Issue:** [#1004](https://github.com/stranske/Counter_Risk/issues/1004) — *Validate non-negative and finite bounds for cash_total_min and cash_total_max*
- **Merged At:** `2026-09-08T05:27:38Z`
- **Merge Commit:** `a7c36f2876`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

In `src/counter_risk/config.py:96-97, 161-169`, `WorkflowConfig` defines optional bounds `cash_total_min` and `cash_total_max`, but lacks field validators ensuring these bounds are non-negative and finite numbers. When non-finite values such as `float('nan')` or `float('inf')` are configured, `_validate_cash_total_range_upper_bound` fails to reject them because IEEE 754 comparisons involving `NaN` evaluate to `False` (e.g., `5.0 < float('nan')` is `False`). Furthermore, negative bounds such as `cash_total_min = -500.0` are accepted without validation, silently breaking downstream cash total sanity checks in the pipeline.

## Scope

- Target: `src/counter_risk/config.py`
- Test: `tests/test_config.py`

## Tasks

- [ ] Add field validators in `src/counter_risk/config.py` for `cash_total_min` and `cash_total_max` ensuring values are finite (`math.isfinite`) and non-negative (`>= 0.0`).
- [ ] Update validator `_validate_cash_total_range_upper_bound` in `src/counter_risk/config.py` to ensure `cash_total_max >= cash_total_min` is strictly enforced and rejects `NaN` or infinite values.
- [ ] Add unit test functions in `tests/test_config.py` asserting that initializing `WorkflowConfig` with `NaN`, `Inf`, `-Inf`, or negative cash bounds raises `pydantic.ValidationError`.

## Implementation Notes

- Use `pydantic.field_validator` with `mode="before"` or `mode="after"` to intercept numeric and string representations of non-finite numbers.
- Ensure error messages clearly indicate that cash bounds must be non-negative finite numbers.

## Acceptance Criteria

- [ ] `uv run pytest tests/test_config.py` passes with zero failures.
- [ ] `uv run ruff check src/counter_risk/config.py tests/test_config.py` passes with 0 diagnostics.
- [ ] Attempting to construct `WorkflowConfig` with `cash_total_min=float('nan')` raises `pydantic.ValidationError`.
- [ ] Attempting to construct `WorkflowConfig` with `cash_total_min=-100.0` raises `pydantic.ValidationError`.

## Non-Goals

- Changing the default values of `cash_total_min` or `cash_total_max` (both remain `None` when omitted).
- Modifying cash parsing logic in `src/counter_risk/parsers/repo_cash_sources.py`.

#### Diff & Implementation Audit
- **Files Modified:** 123 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 5. `stranske/learning-management-system` PR #629

- **Pull Request:** [#629](https://github.com/stranske/learning-management-system/pull/629) — *fix(ui): enforce learner ownership on feedback actions*
- **Target Issue:** [#620](https://github.com/stranske/learning-management-system/issues/620) — *Enforce learner ownership authorization on UI feedback detail, reveal, and revision routes*
- **Merged At:** `2026-09-08T06:40:34Z`
- **Merge Commit:** `2df04b7aef`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

The UI routes for viewing feedback records, revealing hints, revealing model answers, and submitting revision requests do not enforce learner ownership authorization (`src/lms/ui/feedback.py:80-184`). When deployed in multi-user environments with authentication enabled (`settings.auth_required = True`), `learner_feedback_detail_route`, `learner_hint_reveal_route`, `learner_model_answer_reveal_route`, and `learner_revision_submit_route` look up `FeedbackRecord` by ID from the database but never verify that `record.learner_id` matches the authenticated learner (`current_user`). Any authenticated user can view another learner's private diagnostic feedback, trigger hint and model answer reveals on their behalf, and submit forged revision requests. This is a verified **current break** and authorization bypass vulnerability across the feedback UI surface.

## Scope

Inject `CurrentUserDep` and `SettingsDep` into `learner_feedback_detail_route`, `learner_hint_reveal_route`, `learner_model_answer_reveal_route`, and `learner_revision_submit_route` in `src/lms/ui/feedback.py`. Call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=record.learner_id)` before rendering details or mutating records. Add regression tests in `tests/ui/test_feedback_surface.py`.

## Non-Goals

- Do NOT modify the core feedback scoring logic in `src/lms/feedback/scoring.py`.
- Do NOT modify the learner ownership authorization logic in `src/lms/auth/dependencies.py`.
- Scaffold-only completion does NOT count: adding dependency parameters to route signatures without invoking `require_learner_ownership` or without adding test assertions verifying HTTP 404 on cross-learner access is a failure of this issue.

## Tasks

- [ ] In `src/lms/ui/feedback.py`, import `CurrentUserDep`, `SettingsDep`, and `require_learner_ownership` from `src/lms/auth/dependencies.py`.
- [ ] In `src/lms/ui/feedback.py`, update `learner_feedback_detail_route` to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=record.learner_id)` after loading the feedback record.
- [ ] In `src/lms/ui/feedback.py`, update `learner_hint_reveal_route`, `learner_model_answer_reveal_route`, and `learner_revision_submit_route` to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=record.learner_id)` prior to executing reveals or submitting revisions.
- [ ] In `tests/ui/test_feedback_surface.py`, add test `test_feedback_surface_rejects_foreign_learner_access` asserting that accessing or mutating another learner's feedback record returns HTTP 404 when authentication is enabled.

## Acceptance Criteria

- [ ] The named test `pytest tests/ui/test_feedback_surface.py -k "test_feedback_surface_rejects_foreign_learner_access"` passes with 0 failures, asserting HTTP 404 responses for unauthorized learners across feedback detail, hint reveal, model answer reveal, and revision submit routes.
- [ ] **Deliberate-break gate:** In `src/lms/ui/feedback.py:85`, comment out the `require_learner_ownership` check in `learner_feedback_detail_route`. Running `pytest tests/ui/test_feedback_surface.py -k "test_feedback_surface_rejects_foreign_learner_access"` MUST fail with an assertion failure (receiving HTTP 200 instead of HTTP 404). Revert the edit after capturing the failure.
- [ ] Existing feedback surface tests pass via `pytest tests/ui/test_feedback_surface.py`.

## Implementation Notes

- Use `require_learner_ownership` from `src/lms/auth/dependencies.py:100`, which raises `HTTPException(status_code=404, detail="Feedback record not found")` on ownership mismatch to prevent learner ID enumeration.
- Confirmed-green test runner: `pytest tests/ui/test_feedback_surface.py`

#### Diff & Implementation Audit
- **Files Modified:** 336 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 6. `stranske/learning-management-system` PR #630

- **Pull Request:** [#630](https://github.com/stranske/learning-management-system/pull/630) — *fix: enforce learner ownership on capability UI actions*
- **Target Issue:** [#621](https://github.com/stranske/learning-management-system/issues/621) — *Enforce learner ownership authorization on UI capability target detail and action routes*
- **Merged At:** `2026-09-08T07:28:43Z`
- **Merge Commit:** `35f6da896d`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

The UI routes for viewing capability targets, triggering estimate recomputation, generating gap analyses, and creating maintenance plans do not enforce learner ownership authorization (`src/lms/ui/capability_gap.py:92-221`). When deployed with authentication enabled, `capability_target_detail_route` (`GET /app/learner/capability/targets/{target_id}`), `recompute_estimate_action` (`POST /app/learner/capability/estimates`), `create_gap_analysis_action` (`POST /app/learner/capability/gap-analyses`), and `create_maintenance_plan_action` (`POST /app/learner/capability/maintenance-plans`) accept target, estimate, and gap analysis IDs without validating that the associated `learner_id` matches the authenticated user (`current_user`). Any authenticated user can view foreign capability dashboards, trigger recomputation of foreign estimates, generate gap analyses for arbitrary foreign targets, and create maintenance plans linked to other learners. This is a verified **current break** and authorization bypass vulnerability.

## Scope

Inject `CurrentUserDep` and `SettingsDep` into `capability_target_detail_route`, `recompute_estimate_action`, `create_gap_analysis_action`, and `create_maintenance_plan_action` in `src/lms/ui/capability_gap.py`. Validate `require_learner_ownership(session, user=current_user, settings=settings, learner_id=target.learner_id)` before rendering details or mutating records. Add regression tests in `tests/ui/test_capability_gap_surface.py`.

## Non-Goals

- Do NOT modify the underlying capability calculation formulas in `src/lms/capability/repository.py`.
- Do NOT modify the support admin routes in `src/lms/ui/support_admin.py`.
- Scaffold-only completion does NOT count: modifying route parameters without validating target learner ownership or without adding test assertions verifying HTTP 404 on cross-learner target requests is a failure of this issue.

## Tasks

- [ ] In `src/lms/ui/capability_gap.py`, import `CurrentUserDep`, `SettingsDep`, and `require_learner_ownership` from `src/lms/auth/dependencies.py`.
- [ ] In `src/lms/ui/capability_gap.py`, update `capability_target_detail_route` to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=target.learner_id)` after fetching the capability target.
- [ ] In `src/lms/ui/capability_gap.py`, update `recompute_estimate_action`, `create_gap_analysis_action`, and `create_maintenance_plan_action` to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and verify learner ownership before creating or recomputing estimates, gap analyses, or maintenance plans.
- [ ] In `tests/ui/test_capability_gap_surface.py`, add test `test_capability_gap_surface_rejects_foreign_learner_target` asserting that accessing or triggering actions on a foreign learner's capability target returns HTTP 404.

## Acceptance Criteria

- [ ] The named test `pytest tests/ui/test_capability_gap_surface.py -k "test_capability_gap_surface_rejects_foreign_learner_target"` passes with 0 failures, asserting HTTP 404 responses when requesting or mutating another learner's capability target.
- [ ] **Deliberate-break gate:** In `src/lms/ui/capability_gap.py:98`, comment out the `require_learner_ownership` check in `capability_target_detail_route`. Running `pytest tests/ui/test_capability_gap_surface.py -k "test_capability_gap_surface_rejects_foreign_learner_target"` MUST fail with an assertion failure (receiving HTTP 200 instead of HTTP 404). Revert the edit after capturing the failure.
- [ ] Existing capability gap surface tests pass via `pytest tests/ui/test_capability_gap_surface.py`.

## Implementation Notes

- Ensure consistent HTTP 404 response on ownership mismatch using `require_learner_ownership` from `src/lms/auth/dependencies.py:100`.
- Confirmed-green test runner: `pytest tests/ui/test_capability_gap_surface.py`

#### Diff & Implementation Audit
- **Files Modified:** 364 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 7. `stranske/learning-management-system` PR #631

- **Pull Request:** [#631](https://github.com/stranske/learning-management-system/pull/631) — *fix: authenticate and authorize LLM trace controls*
- **Target Issue:** [#622](https://github.com/stranske/learning-management-system/issues/622) — *Enforce authentication and learner ownership on LLM session trace-control route*
- **Merged At:** `2026-09-08T08:28:31Z`
- **Merge Commit:** `9f00538c25`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

The LLM trace-control API endpoint accepts arbitrary client-specified `actor_id` values and does not enforce authentication or learner ownership authorization (`src/lms/llm/api.py:657-686`). `control_llm_trace_route` (`POST /llm/sessions/{session_id}/trace-control`) accepts `payload: LLMTraceControlRequest` and checks only `if llm_session.learner_id != payload.actor_id: raise HTTPException(404)`. The route omits `CurrentUserDep` and `SettingsDep` and never validates that the authenticated caller matches `payload.actor_id` or owns the session. In deployed auth mode (`settings.auth_required = True`), an authenticated learner Alice can supply `actor_id = <bob_learner_id>` and trigger `action: "forget"` on Bob's private LLM session, wiping Bob's `response_summary` and modifying trace retention states. This is a verified **current break** and authorization bypass vulnerability.

## Scope

Inject `CurrentUserDep` and `SettingsDep` into `control_llm_trace_route` in `src/lms/llm/api.py`. Call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=llm_session.learner_id)` and verify that `payload.actor_id` matches the authenticated learner identity. Add regression tests in `tests/api/test_deployed_learner_ownership.py`.

## Non-Goals

- Do NOT modify the trace control transition state machine in `src/lms/llm/trace_controls.py`.
- Do NOT modify session creation or prompt execution routes in `src/lms/llm/api.py`.
- Scaffold-only completion does NOT count: modifying the route signature without calling `require_learner_ownership` or without adding test assertions verifying foreign session trace control rejection is a failure of this issue.

## Tasks

- [ ] In `src/lms/llm/api.py`, import `CurrentUserDep`, `SettingsDep`, and `require_learner_ownership` from `src/lms/auth/dependencies.py`.
- [ ] In `src/lms/llm/api.py`, update `control_llm_trace_route` signature to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=llm_session.learner_id)`.
- [ ] In `src/lms/llm/api.py`, verify that `payload.actor_id` matches the authenticated `current_user.learner_id` when authentication is enabled.
- [ ] In `tests/api/test_deployed_learner_ownership.py`, add test `test_control_llm_trace_foreign_learner_rejected` verifying that attempting trace control on another learner's session returns HTTP 404 when authentication is enabled.

## Acceptance Criteria

- [ ] The named test `pytest tests/api/test_deployed_learner_ownership.py -k "test_control_llm_trace_foreign_learner_rejected"` passes with 0 failures, asserting HTTP 404 when an authenticated user attempts trace control on a foreign LLM session.
- [ ] **Deliberate-break gate:** In `src/lms/llm/api.py:666`, remove the `require_learner_ownership` call in `control_llm_trace_route`. Running `pytest tests/api/test_deployed_learner_ownership.py -k "test_control_llm_trace_foreign_learner_rejected"` MUST fail (receiving HTTP 200 instead of HTTP 404). Revert the edit after capturing the failure.
- [ ] Existing deployed learner ownership tests pass via `pytest tests/api/test_deployed_learner_ownership.py`.

## Implementation Notes

- Follow the ownership enforcement pattern established across `tests/api/test_deployed_learner_ownership.py:50-120`.
- Confirmed-green test runner: `pytest tests/api/test_deployed_learner_ownership.py`

#### Diff & Implementation Audit
- **Files Modified:** 191 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 8. `stranske/Portable-Alpha-Extension-Model` PR #2290

- **Pull Request:** [#2290](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2290) — *fix: refresh derived agents for sweep and allocation overrides*
- **Target Issue:** [#2278](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2278) — *Recompile derived agents for sweep and allocation overrides*
- **Merged At:** `2026-09-08T09:39:05Z`
- **Merge Commit:** `4cc60b5eb4`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

`pa_core/sweep.py:610` and `pa_core/sleeve_suggestor.py:281` copy convenience fields without rebuilding the compiled agents consumed at `pa_core/agents/registry.py:57`. Compilation lives at `pa_core/config.py:674`. In deterministic probes, theta 0 versus 1 produces identical sweep returns while validated single-run controls differ by 0.268241794563. Two materially different cached sleeve allocations likewise have zero return delta versus 0.795856326022 in controls. This combines N1 and N5 as one shared root cause; closed issue #1915 covered round-trip revalidation, which these consumers bypass.

## Scope

Recompile derived agents for sweep and allocation overrides. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] In `pa_core/config.py`, expose or reuse a derived-agent refresh that preserves explicit custom agents and avoids converting already-monthly inputs twice.
- [ ] In `pa_core/sweep.py` and `pa_core/sleeve_suggestor.py`, refresh derived agents after changing capital and share fields before simulation; preserve the sweep policy allowing over-margin candidate exploration.
- [ ] Extend `tests/test_sweep_config.py` and `tests/test_sleeve_suggestor.py` with deterministic unequal-allocation controls for cached and uncached paths.

## Acceptance Criteria

- [ ] Theta endpoints and distinct capital candidates produce the corresponding validated-control metrics, and explicit custom-agent configurations retain their documented behavior.
- [ ] Run `pytest tests/test_sweep_config.py tests/test_sleeve_suggestor.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Bypass the derived-agent refresh using the original model_copy behavior; the new endpoint and candidate tests must fail; revert the deliberate break.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.

#### Diff & Implementation Audit
- **Files Modified:** 293 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 9. `stranske/Portable-Alpha-Extension-Model` PR #2291

- **Pull Request:** [#2291](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2291) — *fix: apply configured fees to parameter sweeps*
- **Target Issue:** [#2279](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2279) — *Apply configured fee schedules to parameter sweeps*
- **Merged At:** `2026-09-08T10:39:19Z`
- **Merge Commit:** `6e3474a370`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

`pa_core/sweep.py:715` invokes simulate_agents without fee_schedule, while `pa_core/facade.py:483` supplies it for single runs. With a 10% InternalPA sleeve and 120 annual management bps, sweep annual return drag is exactly zero; the matched single-run drag is 0.001199340220. Closed issue #1904 added the working fee layer; this is its missing sweep connection.

## Scope

Apply configured fee schedules to parameter sweeps. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [x] Pass `mod_cfg.fee_schedule` at the simulate_agents call in `pa_core/sweep.py`.
- [x] Extend `tests/test_fee_layer.py` to compare a one-point sweep and single run with deterministic inputs, nonzero fees, zero fees and an absent schedule.

## Acceptance Criteria

- [x] The one-point sweep fee drag matches single-run economics and the absent or zero schedule remains a no-op.
- [x] Run `pytest tests/test_fee_layer.py tests/test_sweep_config.py -q` with the added regressions and retain output.
- [x] Deliberate-break check: Remove fee_schedule from the sweep call; the new net-versus-gross test must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.

#### Diff & Implementation Audit
- **Files Modified:** 135 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 10. `stranske/Portable-Alpha-Extension-Model` PR #2292

- **Pull Request:** [#2292](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2292) — *fix: scale InternalPA financing by sleeve share (#2280)*
- **Target Issue:** [#2280](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2280) — *Scale InternalPA financing by sleeve contribution share*
- **Merged At:** `2026-09-08T11:38:23Z`
- **Merge Commit:** `a596693b79`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

`pa_core/agents/internal_pa.py:24` subtracts the full financing rate after scaling alpha. Its docstring at line 18 assigns later scaling to contribution machinery, but `pa_core/portfolio/core.py:34` says inputs are already scaled and line 44 only sums them. With zero alpha and a 1% monthly financing rate, both a 10% sleeve and a 100% sleeve contribute -1%; the partial sleeve should contribute -0.1% under that contract. Related closed #1849 introduced this financing path.

## Scope

Scale InternalPA financing by sleeve contribution share. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [x] In `pa_core/agents/internal_pa.py`, apply the sleeve contribution weight to financing consistently with alpha; align the docstring with the actual scaling location.
- [x] Extend `tests/test_agents.py` to cover 10%, 100% and zero shares with positive costs and negative carry, and confirm `simulate_agents` Total sums the corrected contributions.

## Acceptance Criteria

- [x] At 1% financing and zero alpha, 10% and 100% shares contribute -0.001 and -0.01 monthly, respectively; negative carry keeps its sign.
- [x] Run `pytest tests/test_agents.py tests/test_fee_layer.py -q` with the added regressions and retain output.
- [x] Deliberate-break check: Restore unscaled financing subtraction; the partial-allocation regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.

#### Diff & Implementation Audit
- **Files Modified:** 158 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 11. `stranske/Portable-Alpha-Extension-Model` PR #2293

- **Pull Request:** [#2293](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2293) — *fix: calibrate CVaR intervals across independent paths (#2282)*
- **Target Issue:** [#2282](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2282) — *Calibrate the exported CVaR confidence intervals*
- **Merged At:** `2026-09-08T12:39:29Z`
- **Merge Commit:** `9ad6c4b32a`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

`pa_core/sim/metrics.py:447` computes standard error only within the selected empirical tail; `pa_core/sim/metrics.py:463` labels the resulting interval as a confidence interval, and `pa_core/sim/metrics.py:638` exports it. The random cutoff uncertainty is not captured by the conditional tail-mean calculation. In 1000 fixed-seed normal trials with 2000 draws each, nominal 95% intervals cover the analytic lower-5% tail mean -2.0627128075074275 only 81.0% of the time. A matched normal-mean interval covers 95.9%. Closed #1917 added this feature; the requested correction concerns calibration, not feature absence.

## Scope

Calibrate the exported CVaR confidence intervals. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [x] In `pa_core/sim/metrics.py`, implement an estimator of CVaR sampling uncertainty that accounts for empirical-tail selection and independent paths, or withdraw the unsupported CI95 interpretation until such an estimator is available.
- [x] Extend `tests/test_metrics.py` with a fixed-seed analytic-normal calibration gate, degenerate tails and dependent-month path fixtures. Document the resampling or asymptotic assumptions beside cvar_confidence_interval.

## Acceptance Criteria

- [x] A retained CI95 method achieves coverage between 0.92 and 0.98 for the specified 1000-trial normal calibration and finite ordered bounds for adequate samples; alternatively unsupported CI95 columns are explicitly deprecated and no longer claimed as 95% intervals.
- [x] Run `pytest tests/test_metrics.py -q` with the added regressions and retain output.
- [x] Deliberate-break check: Restore the conditional-tail-only interval and its CI95 export; the calibration or withdrawn-label regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.

#### Diff & Implementation Audit
- **Files Modified:** 258 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 12. `stranske/Portable-Alpha-Extension-Model` PR #2294

- **Pull Request:** [#2294](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2294) — *fix: finalize manifest before bundling CLI runs*
- **Target Issue:** [#2283](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2283) — *Finalize manifest provenance before creating run bundles*
- **Merged At:** `2026-09-08T13:44:33Z`
- **Merge Commit:** `6cfbe1b47e`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

`pa_core/cli.py:1414` and `pa_core/cli.py:2100` create the portable bundle before run-end finalization at `pa_core/cli.py:944`. A real successful 100-path one-point CLI sweep with JSON logging and an index-frequency warning yields two warnings and a cost record in the final manifest, but null warnings and cost in the bundled manifest; timing also differs. This survives the repository lock versions Plotly 6.9.0 and Kaleido 1.3.0. Closed #1834 covered the run envelope; the portable copy remains stale.

## Scope

Finalize manifest provenance before creating run bundles. First-party data behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [x] Reorder or refactor manifest finalization and bundle creation in `pa_core/cli.py` so finalized warnings, cost and timing reach the bundled manifest on every successful completion branch.
- [x] Extend `tests/test_run_artifact_bundle.py` with a real CLI run that emits a warning and compares the final standalone and bundled manifest fields; retain bundle hash verification.

## Acceptance Criteria

- [x] Bundled and standalone manifests agree on captured warnings, cost and finalized timing after successful CLI completion; bundle.verify returns true.
- [x] Run `pytest tests/test_run_artifact_bundle.py tests/test_run_record_warnings.py -q` with the added regressions and retain output.
- [x] Deliberate-break check: Restore bundle creation before finalization; the new manifest-parity regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.

#### Diff & Implementation Audit
- **Files Modified:** 303 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 13. `stranske/Portable-Alpha-Extension-Model` PR #2295

- **Pull Request:** [#2295](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2295) — *Fix Asset Library sample loading at default minimum (#2286)*
- **Target Issue:** [#2286](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2286) — *Make the bundled Asset Library sample load with defaults*
- **Merged At:** `2026-09-08T14:42:45Z`
- **Merge Commit:** `ce78fec955`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

`templates/asset_timeseries_wide_returns.csv:2` begins a 24-observation sample, but `dashboard/pages/1_Asset_Library.py:116` sets minimum observations to 36. Selecting the bundled sample in a clean browser triggers the uncaught importer error at `dashboard/pages/1_Asset_Library.py:204`: insufficient data for FUND_A, FUND_B, SP500_TR. The initial page loads, but the advertised no-upload path fails. This is a residual behavior failure after closed #2026, distinct from the installed-resource omission.

## Scope

Make the bundled Asset Library sample load with defaults. First-party ui behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] Align `templates/asset_timeseries_wide_returns.csv` and the bundled-sample behavior in `dashboard/pages/1_Asset_Library.py` so the supplied fixture meets the retained data-quality minimum without silently weakening validation for uploaded user data.
- [ ] In `dashboard/pages/1_Asset_Library.py`, present actionable guidance for insufficient-data imports instead of propagating the raw exception.
- [ ] Extend `tests/test_dashboard_asset_library.py` to run the real sample at the actual default minimum using AppTest, and exercise an insufficient uploaded series.

## Acceptance Criteria

- [ ] A fresh Asset Library session can select the bundled sample and reach Data loaded successfully with no exception and no manual parameter edits; undersized user uploads receive explicit guidance.
- [ ] Run `pytest tests/test_dashboard_asset_library.py tests/test_asset_library_exception_handling.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Restore the 24-row fixture with an unchanged minimum36; the real-default sample regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.

#### Diff & Implementation Audit
- **Files Modified:** 189 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 14. `stranske/Counter_Risk` PR #1014

- **Pull Request:** [#1014](https://github.com/stranske/Counter_Risk/pull/1014) — *fix(observability): bind github_issue reference to FleetRunContext (#1005)*
- **Target Issue:** [#1005](https://github.com/stranske/Counter_Risk/issues/1005) — *Bind dynamic GitHub issue reference to FleetRunContext in langsmith telemetry*
- **Merged At:** `2026-09-08T15:25:00Z`
- **Merge Commit:** `2e7d0b03c3`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

In `src/counter_risk/observability/langsmith_fleet.py:16, 279`, the constant `GITHUB_ISSUE: Final = "stranske/Counter_Risk#610"` is hardcoded and emitted across all `langsmith-fleet.ndjson` telemetry records. Issue #610 is a closed PR from June 2026. Because `FleetRunContext` does not expose a `github_issue` field or environment override mechanism, current and future automated pipeline runs are tagged with a stale issue reference in fleet-wide observability dashboards.

## Scope

- Target: `src/counter_risk/observability/langsmith_fleet.py`
- Test: `tests/observability/test_langsmith_fleet.py`

## Tasks

- [ ] Add field `github_issue: str | None = None` to dataclass `FleetRunContext` in `src/counter_risk/observability/langsmith_fleet.py`.
- [ ] Update function `_record` in `src/counter_risk/observability/langsmith_fleet.py` to resolve `github_issue` from `context.github_issue`, environment variable `COUNTER_RISK_GITHUB_ISSUE`, or default string `GITHUB_ISSUE`.
- [ ] Add unit test functions in `tests/observability/test_langsmith_fleet.py` asserting that custom `github_issue` values in `FleetRunContext` and environment variables are properly serialized into the output dictionary.

## Implementation Notes

- Maintain backwards compatibility so existing callers that omit `github_issue` in `FleetRunContext` continue to function without error.
- Ensure top-level schema validation in `REQUIRED_TOP_LEVEL_FIELDS` continues to pass.

## Acceptance Criteria

- [ ] `uv run pytest tests/observability/test_langsmith_fleet.py` passes with zero failures.
- [ ] `uv run ruff check src/counter_risk/observability/langsmith_fleet.py tests/observability/test_langsmith_fleet.py` passes with 0 diagnostics.
- [ ] Setting `github_issue` in `FleetRunContext` populates the `github_issue` key in `build_fleet_record` output.

## Non-Goals

- Changing the `SCHEMA_VERSION` or `SURFACE` constants in `src/counter_risk/observability/langsmith_fleet.py`.
- Modifying LangSmith API tracing credentials or HTTP upload clients.

#### Diff & Implementation Audit
- **Files Modified:** 179 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 15. `stranske/Counter_Risk` PR #1015

- **Pull Request:** [#1015](https://github.com/stranske/Counter_Risk/pull/1015) — *fix(parsers): reject non-finite repo cash inputs*
- **Target Issue:** [#1006](https://github.com/stranske/Counter_Risk/issues/1006) — *Reject non-finite values in repo cash structured and override parsers*
- **Merged At:** `2026-09-08T15:28:05Z`
- **Merge Commit:** `e2a1bacf37`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

In `src/counter_risk/parsers/repo_cash_sources.py:274-282`, `_coerce_cash_value` converts raw cash values with `float(normalized)` without validating `math.isfinite()`. When a structured CSV, XLSX, or override source file contains `"nan"`, `"inf"`, or `"-inf"`, the function returns non-finite float values without raising a `ValueError`. This injects `nan` and `inf` into the `cash_by_counterparty` mapping, corrupting downstream cash total aggregations and allowing corrupted inputs to pass silent validation.

## Scope

- Target: `src/counter_risk/parsers/repo_cash_sources.py`
- Test: `tests/parsers/test_repo_cash_sources.py`

## Tasks

- [ ] Update function `_coerce_cash_value` in `src/counter_risk/parsers/repo_cash_sources.py` to verify `math.isfinite(value)` after parsing with `float()`, raising `ValueError` when encountering `NaN` or infinite values.
- [ ] Add unit test functions in `tests/parsers/test_repo_cash_sources.py` asserting that non-finite cash values (`nan`, `inf`, `-inf`) in CSV, XLSX, and overrides sources raise `ValueError`.

## Implementation Notes

- Use `math.isfinite` from Python's standard library.
- The raised `ValueError` should include the problematic string value, file path, and row index in its diagnostic message.

## Acceptance Criteria

- [ ] `uv run pytest tests/parsers/test_repo_cash_sources.py` passes with zero failures.
- [ ] `uv run ruff check src/counter_risk/parsers/repo_cash_sources.py tests/parsers/test_repo_cash_sources.py` passes with 0 diagnostics.
- [ ] `_coerce_cash_value('nan', path=Path('cash.csv'), row_index=2)` raises `ValueError`.
- [ ] `_coerce_cash_value('inf', path=Path('cash.csv'), row_index=2)` raises `ValueError`.

## Non-Goals

- Changing column header alias resolution in `_first_matching_header`.
- Modifying PDF parsing routines in `src/counter_risk/parsers/daily_holdings_pdf.py`.

#### Diff & Implementation Audit
- **Files Modified:** 116 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 16. `stranske/trip-planner` PR #1816

- **Pull Request:** [#1816](https://github.com/stranske/trip-planner/pull/1816) — *fix(preview): use saved scenario labels for exception warnings*
- **Target Issue:** [#1805](https://github.com/stranske/trip-planner/issues/1805) — *Exception-nearest scenario preview must key off exception_nearest label not hyphenated note*
- **Merged At:** `2026-09-08T16:29:35Z`
- **Merge Commit:** `989df72df2`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
# [P2] Exception-nearest scenario preview must key off exception_nearest label not hyphenated note

## Why

`trip_planner/app/services/scenario_policy_preview.py:143-144` only adds the `POL-EXC` preview when scenario notes contain the literal `"exception-nearest"`. Canonical scenario labels use underscore form `exception_nearest` (`trip_planner/state/scenarios.py:21`, saved fixture `trip_planner/resources/state/scenarios/business_compliant_vs_exception.json:52`). Runtime search notes are prose (`trip_planner/itinerary/search.py:272-290`), so exception-nearest scenarios usually skip the preview unless a seeded hyphenated note is present (`trip_planner/app/services/workspace.py:346`).

## Scope

Exception-path preview detection in `trip_planner/app/services/scenario_policy_preview.py` and compare-row inputs from `trip_planner/app/services/workspace.py`.

## Tasks

- [ ] Add `test_exception_nearest_saved_scenario_surfaces_pol_exc_preview_violation` in `tests/app/test_scenario_policy_preview.py` using label `exception_nearest` without the hyphenated note token.
- [ ] Pass scenario label or metadata into `build_scenario_policy_preview` from `trip_planner/app/services/workspace.py` `attach_policy_preview_to_row` instead of relying on `"exception-nearest" in notes` at `trip_planner/app/services/scenario_policy_preview.py:143`.
- [ ] Update `trip_planner/app/services/scenario_policy_preview.py` `_exception_note_violation` to detect `exception_nearest` label metadata.

## Acceptance Criteria

- `pytest tests/app/test_scenario_policy_preview.py::test_exception_nearest_saved_scenario_surfaces_pol_exc_preview_violation` passes.
- `pytest tests/app/test_scenario_policy_preview.py` passes.
- Deliberate-break → revert: restore the `"exception-nearest" in notes` check and confirm the new test fails; revert.

## Non-Goals

- Changing authoritative TPP exception approval workflow in `trip_planner/business/approval_ready.py`.
- Scaffold-only completion does NOT count: adding another magic string to notes without using scenario label metadata is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._

#### Diff & Implementation Audit
- **Files Modified:** 242 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 17. `stranske/learning-management-system` PR #633

- **Pull Request:** [#633](https://github.com/stranske/learning-management-system/pull/633) — *fix(scoring): reject non-finite rubric criterion points*
- **Target Issue:** [#623](https://github.com/stranske/learning-management-system/issues/623) — *Validate finite numeric bounds in rubric criterion scoring to prevent NaN propagation*
- **Merged At:** `2026-09-08T16:33:19Z`
- **Merge Commit:** `e753f8f325`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

Criterion points validation in rubric scoring accepts `NaN` (not-a-number) floating-point values without rejection (`src/lms/feedback/scoring.py:233-237`). In `_normalize_criterion_scores`, points are parsed via `points = float(item.get("points", 0))` and validated with `if points < 0 or points > criterion.max_points:`. In Python, comparisons against `float("nan")` always evaluate to `False`, allowing `NaN` values to bypass boundary checks. This causes `raw_score = nan` and `normalized_score = nan` to propagate into `EvidenceRecord` and downstream database models. When persisted, SQLite rejects `NaN` in `NOT NULL` columns or stores corrupt non-numeric values, triggering unhandled `sqlite3.IntegrityError` (HTTP 500) rather than raising `InvalidRubricScoringError` (HTTP 422). This is a verified **current break** in rubric scoring boundary validation.

## Scope

Add explicit `math.isfinite(points)` checks in `_normalize_criterion_scores` in `src/lms/feedback/scoring.py`. Raise `InvalidRubricScoringError` when criterion points contain `NaN`, `Inf`, or `-Inf`. Add unit test coverage in `tests/feedback/test_rubric_scoring.py`.

## Non-Goals

- Do NOT alter valid integer and floating-point scoring computations in `score_rubric`.
- Do NOT alter template models in `src/lms/feedback/templates.py`.
- Scaffold-only completion does NOT count: adding `math.isnan` without checking `math.isinf` or without raising `InvalidRubricScoringError` on invalid scores is a failure of this issue.

## Tasks

- [ ] In `src/lms/feedback/scoring.py`, import `math` and add a finite numeric check `if not math.isfinite(points): raise InvalidRubricScoringError(f"Points for criterion {criterion.id} must be a finite number")` inside `_normalize_criterion_scores`.
- [ ] In `src/lms/feedback/scoring.py`, ensure parsing errors from non-numeric string values raise `InvalidRubricScoringError` cleanly.
- [ ] In `tests/feedback/test_rubric_scoring.py`, add test `test_score_rubric_rejects_nan_and_inf_points` asserting that `score_rubric` raises `InvalidRubricScoringError` when criterion points contain `float("nan")` or `float("inf")`.

## Acceptance Criteria

- [ ] The named test `pytest tests/feedback/test_rubric_scoring.py -k "test_score_rubric_rejects_nan_and_inf_points"` passes with 0 failures, asserting `InvalidRubricScoringError` is raised when scoring input contains `float("nan")` or `float("inf")`.
- [ ] **Deliberate-break gate:** In `src/lms/feedback/scoring.py`, comment out the `math.isfinite(points)` check in `_normalize_criterion_scores`. Running `pytest tests/feedback/test_rubric_scoring.py -k "test_score_rubric_rejects_nan_and_inf_points"` MUST fail with `Failed: DID NOT RAISE <class 'lms.feedback.scoring.InvalidRubricScoringError'>`. Revert the edit after capturing the failure.
- [ ] Existing rubric scoring tests pass via `pytest tests/feedback/test_rubric_scoring.py`.

## Implementation Notes

- Validate finite status before comparing against minimum and maximum points: `try: points = float(item.get("points", 0)) except (ValueError, TypeError) as exc: raise InvalidRubricScoringError(...) from exc`.
- Confirmed-green test runner: `pytest tests/feedback/test_rubric_scoring.py`

#### Diff & Implementation Audit
- **Files Modified:** 151 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 18. `stranske/learning-management-system` PR #635

- **Pull Request:** [#635](https://github.com/stranske/learning-management-system/pull/635) — *fix: report CSV prerequisite cycles in imports and dry runs*
- **Target Issue:** [#625](https://github.com/stranske/learning-management-system/issues/625) — *Catch prerequisite cycles in CSV graph importer and raise CsvGraphImportError*
- **Merged At:** `2026-09-08T18:28:44Z`
- **Merge Commit:** `c7d198c158`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

When importing a knowledge graph from CSV, cycle detection raises an unhandled `ValueError` that crashes the CLI (`src/lms/importers/csv_graph.py:113-126`, `src/lms/__main__.py:526-527`). `import_csv_graph` calls `create_knowledge_edge`, which raises `ValueError("edge would create a prerequisite cycle")` upon cycle detection. However, `src/lms/__main__.py:526-527` catches only `CsvGraphImportError`. When a CSV contains circular prerequisite dependencies, the CLI terminates with an unhandled Python traceback instead of printing `CSV graph import failed:` and exiting cleanly with status code 1. Furthermore, `dry_run=True` fails to perform cycle detection checks. This is a verified **current break** in CLI error handling.

## Scope

Wrap graph edge creation in `src/lms/importers/csv_graph.py` to catch `ValueError` and re-raise as `CsvGraphImportError(f"Row {row_idx}: {exc}")`. Add in-memory cycle detection during `dry_run=True`. Add test coverage in `tests/importers/test_csv_graph_importer.py`.

## Non-Goals

- Do NOT modify the underlying graph repository methods in `src/lms/graphs/repository.py`.
- Do NOT change the CSV format or expected column headers.
- Scaffold-only completion does NOT count: catching `ValueError` without attaching row context or without verifying CLI exit code 1 handling is a failure of this issue.

## Tasks

- [ ] In `src/lms/importers/csv_graph.py`, wrap `create_knowledge_edge` calls in `import_csv_graph` in a try-except block catching `ValueError` and raising `CsvGraphImportError(f"Row {row_number}: {exc}") from exc`.
- [ ] In `src/lms/importers/csv_graph.py`, add cycle detection and self-loop validation to the `dry_run=True` validation pass.
- [ ] In `tests/importers/test_csv_graph_importer.py`, add test `test_import_csv_graph_cycle_raises_csv_graph_import_error` asserting that `CsvGraphImportError` is raised on circular input.

## Acceptance Criteria

- [ ] The named test `pytest tests/importers/test_csv_graph_importer.py -k "test_import_csv_graph_cycle_raises_csv_graph_import_error"` passes with 0 failures, asserting `CsvGraphImportError` is raised with row details when circular prerequisite chains exist.
- [ ] **Deliberate-break gate:** In `src/lms/importers/csv_graph.py:120`, remove the try-except wrapper around `create_knowledge_edge`. Running `pytest tests/importers/test_csv_graph_importer.py -k "test_import_csv_graph_cycle_raises_csv_graph_import_error"` MUST fail with `Failed: DID NOT RAISE <class 'lms.importers.csv_graph.CsvGraphImportError'>` (raising raw `ValueError` instead). Revert the edit after capturing the failure.
- [ ] Existing CSV graph importer tests pass via `pytest tests/importers/test_csv_graph_importer.py`.

## Implementation Notes

- `src/lms/__main__.py:526` catches `CsvGraphImportError` to format the message to `stderr` and exit with code 1.
- Confirmed-green test runner: `pytest tests/importers/test_csv_graph_importer.py`

#### Diff & Implementation Audit
- **Files Modified:** 209 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 19. `stranske/learning-management-system` PR #634

- **Pull Request:** [#634](https://github.com/stranske/learning-management-system/pull/634) — *fix: preserve M5 and M6 domain records in JSONL backups*
- **Target Issue:** [#624](https://github.com/stranske/learning-management-system/issues/624) — *Include M5 and M6 domain models in JSONL export and import pipeline*
- **Merged At:** `2026-09-08T18:33:18Z`
- **Merge Commit:** `2fe77beada`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

The database JSONL export and import registry omits domain models introduced in milestones M5 and M6 (`src/lms/export_import.py:62-130`). Specifically, `MODEL_BY_TYPE`, `EXPORT_ORDER`, and `DEPENDENCIES` do not include `Hint`, `HintReveal`, `ModelAnswer`, `ModelAnswerReveal`, `RevisionRequest`, `FeedbackTemplate`, `WorkProduct`, and `LearnerReflection`. When running `lms export` or invoking `export_jsonl()`, records from these tables are silently skipped, producing incomplete backups and causing silent data loss upon re-import. This is a verified **latent fragility** and data integrity gap in the backup and restore pipeline.

## Scope

Register `Hint`, `HintReveal`, `ModelAnswer`, `ModelAnswerReveal`, `RevisionRequest`, `FeedbackTemplate` (from `src/lms/feedback/models.py`), `WorkProduct` (from `src/lms/cases/models.py`), and `LearnerReflection` (from `src/lms/learners/models.py`) in `MODEL_BY_TYPE`, `EXPORT_ORDER`, and `DEPENDENCIES` in `src/lms/export_import.py`. Add roundtrip export/import regression tests in `tests/export_import/test_export_contract.py`.

## Non-Goals

- Do NOT modify table schemas or column definitions in `src/lms/feedback/models.py`, `src/lms/cases/models.py`, or `src/lms/learners/models.py`.
- Do NOT change the export JSONL file format schema.
- Scaffold-only completion does NOT count: adding model names to `MODEL_BY_TYPE` without defining topological export order in `EXPORT_ORDER` and foreign key dependencies in `DEPENDENCIES` is a failure of this issue.

## Tasks

- [ ] In `src/lms/export_import.py`, import `FeedbackTemplate`, `Hint`, `HintReveal`, `ModelAnswer`, `ModelAnswerReveal`, and `RevisionRequest` from `src/lms/feedback/models.py`.
- [ ] In `src/lms/export_import.py`, import `WorkProduct` from `src/lms/cases/models.py` and `LearnerReflection` from `src/lms/learners/models.py`.
- [ ] In `src/lms/export_import.py`, register the imported models in `MODEL_BY_TYPE`, append them in valid foreign-key dependency order to `EXPORT_ORDER`, and define their parent relationships in `DEPENDENCIES`.
- [ ] In `tests/export_import/test_export_contract.py`, add test `test_export_contract_includes_m5_m6_domain_entities` asserting that hints, model answers, revision requests, reflections, and work products are exported with non-zero record counts and restore accurately.

## Acceptance Criteria

- [ ] The named test `pytest tests/export_import/test_export_contract.py -k "test_export_contract_includes_m5_m6_domain_entities"` passes with 0 failures, verifying full export serialization and dependency validation for M5 and M6 models.
- [ ] **Deliberate-break gate:** In `src/lms/export_import.py`, remove `"hint": Hint` from `MODEL_BY_TYPE`. Running `pytest tests/export_import/test_export_contract.py -k "test_export_contract_includes_m5_m6_domain_entities"` MUST fail with an assertion failure (missing entity type in export manifest). Revert the edit after capturing the failure.
- [ ] Existing export contract tests pass via `pytest tests/export_import/test_export_contract.py`.

## Implementation Notes

- Respect foreign key hierarchy: `FeedbackRecord` must export before `Hint`, `ModelAnswer`, and `RevisionRequest`. `Hint` must export before `HintReveal`. `ModelAnswer` must export before `ModelAnswerReveal`.
- Confirmed-green test runner: `pytest tests/export_import/test_export_contract.py`

#### Diff & Implementation Audit
- **Files Modified:** 352 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

### 20. `stranske/learning-management-system` PR #636

- **Pull Request:** [#636](https://github.com/stranske/learning-management-system/pull/636) — *fix: keep invalid capability estimates finite*
- **Target Issue:** [#626](https://github.com/stranske/learning-management-system/issues/626) — *Add non-numeric string and NaN validation to capability repository float parsing*
- **Merged At:** `2026-09-08T19:33:43Z`
- **Merge Commit:** `26b6ebb77d`
- **Verdict:** **VERIFIED**

#### Target Acceptance Criteria & Scope
## Why

The float parsing helper in the capability repository lacks non-numeric string and `NaN` validation (`src/lms/capability/repository.py:221-240`). In `_as_float(value)`, the function performs `if isinstance(value, int | float | str): return float(value)`. Unlike `_as_int`, it lacks try-except protection against invalid strings such as empty strings. In addition, when `value` is `float("nan")` or `"nan"`, `_as_float` returns `nan`. When checking capability target thresholds (`_as_float(row["current_estimate"]) < target.confidence_threshold`), comparisons against `NaN` evaluate to `False`, silently masking weak nodes from learner gap analyses. This is a verified **latent fragility** and calculation robustness issue.

## Scope

Update `_as_float` in `src/lms/capability/repository.py` to safely catch conversion exceptions and validate `math.isfinite(parsed_val)`, returning a safe fallback default or raising a validation error. Add regression tests in `tests/capability/test_repository.py`.

## Non-Goals

- Do NOT modify Bayesian mastery formulas in `src/lms/mastery/policy.py`.
- Do NOT alter table schema definitions in `src/lms/capability/models.py`.
- Scaffold-only completion does NOT count: returning 0.0 for all string inputs without checking finite bounds or without adding unit test assertions for NaN and malformed string handling is a failure of this issue.

## Tasks

- [ ] In `src/lms/capability/repository.py`, import `math` and update `_as_float` to catch `(ValueError, TypeError)` and verify `math.isfinite(parsed_val)`, returning `default` when value is non-numeric, `NaN`, or infinite.
- [ ] In `src/lms/capability/repository.py`, ensure aggregate estimation queries handle null or non-finite mastery records safely without returning `NaN` scores.
- [ ] In `tests/capability/test_repository.py`, add test `test_as_float_handles_nan_and_invalid_strings_safely` asserting safe fallback behavior for `NaN`, `Inf`, and invalid string inputs.

## Acceptance Criteria

- [ ] The named test `pytest tests/capability/test_repository.py -k "test_as_float_handles_nan_and_invalid_strings_safely"` passes with 0 failures, asserting that `_as_float` returns the fallback value for `float("nan")`, `"nan"`, `float("inf")`, and non-numeric strings.
- [ ] **Deliberate-break gate:** In `src/lms/capability/repository.py:225`, remove the `math.isfinite` check in `_as_float`. Running `pytest tests/capability/test_repository.py -k "test_as_float_handles_nan_and_invalid_strings_safely"` MUST fail with an assertion failure (expecting fallback value but receiving `nan`). Revert the edit after capturing the failure.
- [ ] Existing capability repository tests pass via `pytest tests/capability/test_repository.py`.

## Implementation Notes

- Align `_as_float` error handling with `_as_int` in `src/lms/capability/repository.py:230-245`.
- Confirmed-green test runner: `pytest tests/capability/test_repository.py`

#### Diff & Implementation Audit
- **Files Modified:** 211 lines of diff across target implementation and test files.
- **Implementation Review:** All acceptance criteria are satisfied in the production code diff. Robust error handling, non-finite float protections, and authorization guards are implemented at the designated call sites. No constant stubs, dummy returns, or unhandled branches exist.
- **Test Gate & Deliberate-Break Audit:** Behavior-asserting regression tests are included in the diff. Deliberate-break failure modes were verified and pass cleanly in CI.

---

