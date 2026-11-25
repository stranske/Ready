Scorecard: 4 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 4; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 1 — [#6246](https://github.com/stranske/Trend_Model_Project/issues/6246) (`preprocessing.winsorise` inert despite `config/defaults.yml` shipping `enabled: true`).

## Run summary

**Repo / tip:** `stranske/Trend_Model_Project` @ `bb216c4b5068a92192507f86de64db5741136d95` (`main`).

**Phase 0 scope:** `src/`, `streamlit_app/`, `config/`, `tests/`; exclude vendored `.github` Workflows sync. Deliverables: scorecard + filed AGENT_ISSUE_FORMAT issues. Owner answers empty — defaults applied.

**Phase 1 orient:** 7107 tests collected; CI recent runs green on `main`; open agent-ready issues were 0 (trackers only) before this round.

**Phase 1.5 scorecard:** All four `docs/PRODUCT_CONTRACT.md` core functions exercised. C1/C2/C4 via live CLI/report on `config/demo.yml`. C3 via cost-model varying-input diff on demo (`per_trade_bps` 0 vs 50) and named regime lookback wiring test. Primary journey completes to HTML report.

**Dimensions (abbreviated):** Scanned prior round bodies and `proposed-issues/` — stale candidates (Streamlit int/float diff, `run_real_model` RF alignment, `bfill` alias coercion, `check_branch.sh` syntax) refuted on tip. Closed MC regressions (#6230 terminal_wealth path) pass. One new verified config→consumer gap: winsorization keys declared and allowlisted but not applied in `stages/preprocessing.py`.

**Adversarial / dedup:** No duplicate of #6246 topic in open issues. Re-ran closed #6127 reproduction: `store_paths` now fails fast (see REFUTED below).

**Agents Issue Format Guard:** run `45566882998` completed `skipped` (duplicate trigger cancellation); issue carries `status:ready` and `priority:high`. Re-check `agents:formatted` on next guard completion if absent.

## REFUTED (closed-issue reproduction on tip)

REFUTED: https://github.com/stranske/Trend_Model_Project/issues/6127 — `outputs.store_paths` is rejected during Monte Carlo scenario load with `ValueError` (`tests/monte_carlo/test_output_store_paths.py` passes); doc now states unsupported at `docs/phase-3/MonteCarlo.md:654`.

## Artifacts

- Scorecard: `artifacts/audits/Trend_Model_Project-2026-11-25-SCORECARD.md`
- Issue body: `unitdirs/D-audit-Trend_Model_Project--2026-11-25T04-28-15Z/issue-bodies/01-winsorise-inert.md`
- Intake log: `~/.codex/orchestrator/measurement/intake-2026-09-04.log` (append line for #6246)