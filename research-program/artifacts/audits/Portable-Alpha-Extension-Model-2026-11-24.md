Scorecard: 2 work / 4 partial / 0 broken / 0 fabricated / 0 not exercised of 6; journey: passes via baseline run_single and alpha_shares sweep probes, stops at Kaleido/Chromium PNG export in audit environment; surfaces unscored 0; closed-still-broken 0.

Issues filed: 1 (#2534).

## Run report — Track D refill 2026-11-24

**Unit:** `D-audit-Portable-Alpha-Extension-Model--2026-11-24T04-25-43Z`  
**Tip:** `690cefd3cf1b21470365c7aa289d163caef022a6`  
**Trigger:** scorecard 2026-10-24 stale (>30d); open agent-ready issues 0/1.

### Phase 1–1.5 (orient + scorecard)

- pytest collect 2253/2256; CI `main` success 2026-11-23.
- Surface inventory unchanged vs 2026-10-24 (15 surfaces).
- F1/F2 exercised live with varying-input diffs; F3 Excel OK, PNG fails locally (`Chromium.get_cli() … headers`).
- F4–F6 via page-module pytest (21 passed wizard/grid/stress batch).
- Golden tutorials 11/11 passed.

### Phases 2–4 (dimensions + verify + file)

- Eight-dimension pass in lead seat: no additional adversarially-verified P0/P1 beyond documentation caveat.
- Dedup: no open issues on regime disclaimer sweep-only text (#2306 fixed opposite error: ignored→sweeps-only).
- **Filed:** [#2534](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2534) — regime disclaimers omit single-run regime switching (`pa_core/facade.py:433-457` vs `pa_core/reporting/disclaimers.py:20-21`). Format guard workflow run `45330979364` completed success; `priority:normal` applied.

### Closed-issue checks

- #2428 (`pa run --help` stub): fixed on tip (`--config` visible).
- #2287 (Plotly engine kw): code path updated; local PNG failure is Kaleido/Chromium env, not silent drop.

### Artifacts

- Scorecard: `Code/Audits/Portable-Alpha-Extension-Model/2026-11-24-SCORECARD.md`
- Issue body: `Code/Audits/Portable-Alpha-Extension-Model/2026-11-24-issue-bodies/regime-disclaimer-single-run.md`