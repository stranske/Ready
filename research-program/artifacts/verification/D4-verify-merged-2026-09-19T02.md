# D4-verify-merged-2026-09-19T02

**Window:** merged ≥ 2026-09-17T20:56:00Z (36h before run start)  
**Repos:** 15 lane fleet (`SUPPORTED_REPOS`, excluding Orchestrator)  
**Cap:** 20 PRs (8 verified this run)  
**Method:** Squash diffs via `git show` on local clones (`[LOCAL_WORKSPACE]/*/origin/main`); issue bodies from GitHub web + cached sweep evidence. `gh` unavailable (not logged in) — could not run `gh pr diff` / `gh issue view` or file follow-ups.

## Summary

| Metric | Count |
|--------|------:|
| PRs verified | 8 |
| VERIFIED | 1 |
| PARTIAL | 7 |
| NOT IMPLEMENTED | 0 |
| Follow-ups filed this run | 0 |
| Follow-ups blocked (gh auth) | 7 |
| Rate-limit stop | No |

## Results

| Repo | PR | Issue | Verdict | Unmet criteria | Follow-up filed |
|------|-----|-------|---------|----------------|-----------------|
| Manager-Database | [#1685](https://github.com/stranske/Manager-Database/pull/1685) | [#1685](https://github.com/stranske/Manager-Database/issues/1685) | PARTIAL | Production fix + `test_fetch_and_store_rollback_boundary_*` land in `etl/edgar_flow.py` / `tests/test_alert_postgres_integration.py`; issue AC “Latest `CI` workflow on `main` concludes success” still unmet per D3 sweep 2026-09-18 (postgres job red on head `aa016bd`) | not filed (gh auth) |
| Ready | [#576](https://github.com/stranske/Ready/pull/576) | [#576](https://github.com/stranske/Ready/issues/576) | PARTIAL | `publication-guard.yml` prepare→scan wiring + PKCS#8/ENCRYPTED fixtures + `test_publication_guard_workflow_runs_prepare_then_scan` land; shared `scripts/publication_patterns.py` already on `main` from #569; deliberate-break RED/GREEN transcript absent from squash diff | not filed (gh auth) |
| Trend_Model_Project | [#6019](https://github.com/stranske/Trend_Model_Project/pull/6019) | [#6019](https://github.com/stranske/Trend_Model_Project/issues/6019) | PARTIAL | Parametrized `test_compute_signal_uses_cache` / `without_cache` consolidated in `tests/test_pipeline_helpers_additional.py`; duplicates removed from `tests/test_pipeline_run_cache_fallbacks.py` (`rg` → one match on `origin/main`); deliberate-break production-mutation transcript absent | not filed (gh auth) |
| Trend_Model_Project | [#6021](https://github.com/stranske/Trend_Model_Project/pull/6021) | [#6021](https://github.com/stranske/Trend_Model_Project/issues/6021) | PARTIAL | `TrendSpec.__post_init__` + `compute_signal` guards and `test_trend_spec_rejects_min_periods_above_window` / extended `test_compute_signal_error_paths` land; deliberate-break guard-removal demonstration absent from squash diff | not filed (gh auth) |
| Ready | [#563](https://github.com/stranske/Ready/pull/563) | [#563](https://github.com/stranske/Ready/issues/563) | PARTIAL | All `DEFAULT_TRIAGE_PATTERNS.playbook_url` values point at `docs/CI_SYSTEM_GUIDE.md#ci-is-failing`; `test_ci_failure_triage_playbook_urls_resolve_to_existing_docs` lands; deliberate-break transcript absent | not filed (gh auth) |
| Trend_Model_Project | [#6020](https://github.com/stranske/Trend_Model_Project/pull/6020) | [#6020](https://github.com/stranske/Trend_Model_Project/issues/6020) | PARTIAL | `_divide_by_gross_abs` + ambiguous-total path in `src/trend_analysis/util/weights.py`; `test_normalize_weights_ambiguous_total` and boundary cases land; deliberate-break transcript absent | not filed (gh auth) |
| Workflows | [#3348](https://github.com/stranske/Workflows/pull/3348) | [#3348](https://github.com/stranske/Workflows/issues/3348) | VERIFIED | — | — |
| Trend_Model_Project | [#6023](https://github.com/stranske/Trend_Model_Project/pull/6023) | [#6023](https://github.com/stranske/Trend_Model_Project/issues/6023) | PARTIAL | `math.isfinite` guards on `portfolio.lambda_tc` in `config/model.py` + `config/models.py` (both pydantic and fallback paths); `test_lambda_tc_rejects_non_finite` + fallback coverage land; deliberate-break transcript absent | not filed (gh auth) |

## Skipped (not verified)

| Reason | Count | Examples |
|--------|------:|----------|
| Already verified in D4-verify-merged-2026-09-18T02 | 8 | Manager-Mosaic #34; Doc-Lineage #28/#30/#32/#35; Ready #572/#561/#562 |
| Template-sync / infra chore (no issue AC) | 4 | Workflows #3464; Inv-Man-Intake / Fine-Art-Archive / Deliverable-Render template sync |

## Notable findings

1. **Manager-Database #1685** — Real product fix: `fetch_and_store` now rolls back only on exception (`etl/edgar_flow.py`), with a non-vacuous Postgres integration regression (`test_fetch_and_store_rollback_boundary_calls_quietly_only_on_exception`). Local edgar unit tests pass; postgres CI on `main` was still red at last observed run — treat as environmental/CI re-run need unless a new defect surfaces.
2. **Ready #576** — Closes the D4-filed follow-up from #574. Functional gaps (PKCS#8 regex via `publication_patterns.py`, shared scanner/exporter patterns, CI staging pipeline) are present on merged `main`; recurring gap remains deliberate-break transcript hygiene, not scaffold-only delivery.
3. **Trend_Model_Project burst (#6019–#6023)** — Four substantive merges with non-vacuous tests; all four share the fleet deliberate-break transcript gap.
4. **Workflows #3348** — Clean upstream sync-debt fix: hyphen boundary bug in `_extract_fallback_test_name` + template parity tests (`168 passed` locally).
5. **gh auth** — executor cannot file the seven PARTIAL follow-ups; next run should retry filing if credentials are restored.

## Evidence

Squash diffs and issue bodies: `artifacts/verification/evidence/D4-verify-merged-2026-09-19T02/`

Local gate runs (`--no-cov` where applicable):
- Workflows: `pytest tests/scripts/test_check_deliberate_break.py -q` → **168 passed**
- Ready: `pytest tests/test_main.py::test_ci_failure_triage_playbook_urls_resolve_to_existing_docs tests/test_publication_safety.py -k private_key -q` → **21 passed**
- Trend_Model_Project: `pytest tests/test_pipeline_helpers_additional.py -k compute_signal tests/test_pipeline_run_cache_fallbacks.py -q` → **6 passed**; `pytest tests/test_weights_utils.py::test_normalize_weights_ambiguous_total tests/test_config_turnover_validation.py::test_lambda_tc_rejects_non_finite -q` → **4 passed**
