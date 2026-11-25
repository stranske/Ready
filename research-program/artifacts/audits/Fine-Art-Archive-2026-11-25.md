Scorecard: 5 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 1 — https://github.com/stranske/Fine-Art-Archive/issues/903

## Run report — Track D refill, tip `f6858ee9192e4e876dd451137358602b8eac2ec1`

Trigger: scorecard **2026-10-25** was 31 days old; open agent-ready issues at 0/1 filed set. Tip moved by one commit (`chore: sync workflow templates`) with no application-code delta since the prior scorecard.

Phase 1.5 re-exercised contract core functions **C1–C5** on isolated data (`FAA_WORKS_DIR=staging_sidecars`): 260 tests in the scorecard batch (`test_eink_feed_endpoints`, weekly review, companion API, known works) plus 115 interior-route tests and healthz drift suite — all green. OpenAPI surface inventory **49** paths, unchanged vs 2026-10-25 (`Code/Audits/Fine-Art-Archive/2026-11-25-surface-inventory.txt`).

Closed issues re-reproduced on tip: **#847** (dossier year 0) and **#893** (weekly review collision copy) — both fixed; no `closed-still-broken`. No `REFUTED:` line (no open-issue claim disproved; dedup did not drop a live finding against a closed duplicate).

## Verified finding

**[#903](https://github.com/stranske/Fine-Art-Archive/issues/903)** — `[P2] AGENTS.md/CLAUDE.md cite acquisition scripts that are not in the repository`.

`AGENTS.md:186-188` and parallel `CLAUDE.md` text instruct running `scripts/visual_find_in_unindexed.py`; `AGENTS.md:229-232` names `promote_acquisitions.py`, `build_unindexed_embed_cache.py`, and `embed_cache_maintenance.py`. None of these paths exist under `scripts/` on tip (verified `glob` / `Path.is_file()`). `tests/test_operator_messages_name_real_artifacts.py` guards `api/main.py` but not the repo guides — drift survived. Body on disk: `Code/Audits/Fine-Art-Archive/2026-11-25-issue-bodies/01-agents-md-phantom-scripts.md`.

Format guard: **Agents Issue Intake** succeeded (runs https://github.com/stranske/Fine-Art-Archive/actions/runs/45555528796, https://github.com/stranske/Fine-Art-Archive/actions/runs/45555528883). `Agents Issue Format Guard` run https://github.com/stranske/Fine-Art-Archive/actions/runs/45555528293 reported **skipped** (intake path).

Intake log entry appended. No changes to repository source files.

## Confidence

- **High** scorecard headline unchanged in meaning from 2026-10-25 (all five core functions work on isolated probes; unscored count stays 0).
- **High** on #903 (guide lines and missing paths verified by direct read/list).
- **Medium** that no additional interior defects exist — this round did not execute the full 2634-test suite with coverage thresholds; dimension sweep was lead-driven, not eight parallel agents.