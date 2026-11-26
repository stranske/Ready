# D4 verify merged — 2026-11-26T00

**Window:** merges after `2026-11-24T12:49:03Z` (36h), lane fleet per `handoff.sh` `SUPPORTED_REPOS` (excluding Orchestrator).

**Run limits:** 12 PRs verified (issue-linked, non-chore); API pacing observed; no secondary rate limit.

**Reproduction / offload:** Issue `Reproduction:` blocks re-run on merged tip where noted below. This invocation is an **offload** — GitHub follow-up issues, comments, and reopens were **not** performed (authorized in the unit brief but blocked by offload rules).

## Summary

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| Portable-Alpha-Extension-Model | [#2535](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2535) | [#2534](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2534) | VERIFIED | — | No (offload) |
| Counter_Risk | [#1268](https://github.com/stranske/Counter_Risk/pull/1268) | [#1267](https://github.com/stranske/Counter_Risk/issues/1267) | VERIFIED | — | No (offload) |
| learning-management-system | [#861](https://github.com/stranske/learning-management-system/pull/861) | [#859](https://github.com/stranske/learning-management-system/issues/859) | VERIFIED | — | No (offload) |
| Deliverable-Render | [#157](https://github.com/stranske/Deliverable-Render/pull/157) | [#155](https://github.com/stranske/Deliverable-Render/issues/155) | VERIFIED | — | No (offload) |
| Fine-Art-Archive | [#904](https://github.com/stranske/Fine-Art-Archive/pull/904) | [#903](https://github.com/stranske/Fine-Art-Archive/issues/903) | VERIFIED | — | No (offload) |
| Trend_Model_Project | [#6247](https://github.com/stranske/Trend_Model_Project/pull/6247) | [#6246](https://github.com/stranske/Trend_Model_Project/issues/6246) | VERIFIED | — | No (offload) |
| learning-management-system | [#862](https://github.com/stranske/learning-management-system/pull/862) | [#860](https://github.com/stranske/learning-management-system/issues/860) | VERIFIED | — | No (offload) |
| Counter_Risk | [#1273](https://github.com/stranske/Counter_Risk/pull/1273) | [#1272](https://github.com/stranske/Counter_Risk/issues/1272) | VERIFIED | — | No (offload) |
| Workflows | [#5172](https://github.com/stranske/Workflows/pull/5172) | [#5161](https://github.com/stranske/Workflows/issues/5161) | VERIFIED | — | No (offload) |
| Workflows | [#5183](https://github.com/stranske/Workflows/pull/5183) | [#5161](https://github.com/stranske/Workflows/issues/5161) | VERIFIED | — | No (offload) |
| Workflows | [#5176](https://github.com/stranske/Workflows/pull/5176) | [#4784](https://github.com/stranske/Workflows/issues/4784) | VERIFIED | — | No (offload) |
| Workflows | [#5179](https://github.com/stranske/Workflows/pull/5179) | [#5167](https://github.com/stranske/Workflows/issues/5167) | VERIFIED | — | No (offload) |

**Skipped (not verified this run):** `chore: sync workflow templates`, `deps: sync dev tool versions`, `chore(main): release *`, and `Ready#697` (mirror-only CI chore). Numerous Workflows catalog/doc PRs with no issue reference in body or `closingIssuesReferences` were excluded per scope.

## Per-PR notes

### Portable-Alpha-Extension-Model #2535 → #2534

- **Diff:** `pa_core/reporting/disclaimers.py`, README, `tests/test_regime_disclaimer_single_run.py`, `tests/test_model_limitations_1923.py`.
- **AC:** Named test present; asserts `"single runs"` in regime caveat — met.
- **Reproduction:** Re-run on `main` clone: `with_reg` vs `plain` delta `> 1e-4` (passed). `pytest tests/test_regime_disclaimer_single_run.py::test_limitations_mention_single_run_regimes` passed locally.

### Counter_Risk #1268 → #1267

- **Diff:** Banner line in `docs/audit/22-design-ux.md`; gate `tests/docs/test_audit_log_historical.py::test_dimension_audit_logs_marked_historical` updated/passes.

### learning-management-system #861 → #859

- **Diff:** `src/lms/ui/api.py` hidden `prompt_version_id` + `elapsed_seconds`; new `test_learn_post_preserves_presented_prompt_version_and_elapsed_seconds`.
- **Reproduction:** Full manual browser scenario not re-run; named gate test **passed** on merged tip (`pytest …/test_learner_loop.py::test_learn_post_preserves…`).

### Deliverable-Render #157 → #155

- **Diff:** `_resolve_console_script` via `sys.executable` parent; `test_console_script_ignores_stale_global_path_entry` added (PATH-prefix stale binary).
- **Gate:** Local run blocked by host Python 3.12 vs package `>=3.13` and missing editable install; diff satisfies AC; CI is the authoritative gate.

### Fine-Art-Archive #904 → #903

- **Diff:** `AGENTS.md` / `CLAUDE.md` script paths; gate `test_agents_and_claude_guides_name_only_real_scripts` **passed**.

### Trend_Model_Project #6247 → #6246

- **Diff:** Winsorise applied in preprocessing pipeline + `tests/stages/test_winsorise_preprocessing.py::test_winsorise_limits_clip_outlier_returns` **passed**.

### learning-management-system #862 → #860

- **Diff:** `src/lms/api/inspect.py` live overview shell; gate `test_inspect_shell_links_to_live_overview_content` **passed**.

### Counter_Risk #1273 → #1272

- **Diff:** `src/counter_risk/cli/__init__.py` prints `result.error_message` in headless failure path.
- **AC:** Gate lives in `tests/test_cli_coverage_round.py::test_gui_headless_preserves_unsuccessful_exit_code` (issue text cited `test_counter_risk_cli.py` — path drift only). Test **passed**.

### Workflows #5172 + #5183 → #5161

- **#5172:** Eight scoped docs updated; PR body documents **`docs/STRUCTURE.md` verified zero drift** (no file change required).
- **#5183:** Closer repair on `AGENTS_POLICY.md`, `WORKFLOWS.md`, `WORKFLOW_SYSTEM.md` (missing `path:line` citations from #5172).
- **Fleet gates:** `pytest -q tests/workflows/…` not re-run locally (Node + full suite cost); checklist items are doc/evidence fixes with existing workflow test gates on merge.

### Workflows #5176 → #4784

- **Diff:** `docs/reports/workflow-decisions.md`, `docs/reports/workflows-cleanup-tracker.md` only — matches issue (Stages 1A–5 tracker; no checkbox churn).

### Workflows #5179 → #5167

- **Diff:** `agents-guard.js` (+ consumer template) and `tests/workflows/test_agents_guard.py` (Agents 70 legacy retirement / protection tests).
- **Fleet state:** `agents-70-orchestrator.yml`, `reusable-70-init.yml`, `reusable-16.yml` **absent** on `main`; `agents-73-codex-belt-conveyor-dispatch.yml` present. This merge is the guard/test slice; retirements landed in earlier merges (#5162/#5163 per issue narrative).

## Belt ledger

No PR in this batch was **ledger-only** (`.agents/issue-*-ledger.yml` only).

## Confidence

**High** for product-repo PRs with named pytest gates executed on merged tip. **Medium** for Deliverable-Render (host Python floor) and Workflows doc suites (full `tests/workflows/` not re-run here). **Would change:** CI conclusions on merge commits, or Python 3.13 local env for Deliverable-Render console tests.

---

_Generated 2026-11-26 by D4-verify-merged (Cursor composer), attempt 1._