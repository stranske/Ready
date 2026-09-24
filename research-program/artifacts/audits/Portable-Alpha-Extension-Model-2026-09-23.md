Scorecard: 2 work / 1 partial / 0 broken / 0 fabricated / 3 not exercised of 6; journey: passes via CLI simulate and sweep Excel on default configs, stops at silent `--png` on sweep path and undriven Streamlit wizard/results; surfaces unscored 3; closed-still-broken 0.

Issues filed: 0

REFUTED: https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2306 — `pa_core/reporting/disclaimers.py` and README now state regimes apply in parameter sweeps on tip `43a86ec` (PR #2306).

## Run report — Track D — 2026-09-23 (evening refill)

**Repo:** `stranske/Portable-Alpha-Extension-Model` @ `43a86ec47b8aba361eb7a108013db9e5e1d7d3fe`  
**Unit:** `D-audit-Portable-Alpha-Extension-Model--2026-09-23T22-11-14Z`

### Phase 0–1

`git pull` fast-forwarded `a1a872e` → `43a86ec` (disclaimer/README alignment for regime sweeps). Read dossier, `Code/Audits/Portable-Alpha-Extension-Model/` continuity, morning mirror `artifacts/audits/Portable-Alpha-Extension-Model-2026-09-23.md`. Orientation: seven Streamlit pages, `pa` subcommands per surface inventory; venv install reused from AM round.

### Phase 1.5 (scorecard)

Re-ran F1–F3 CLI probes on corrected config path `examples/scenarios/my_first_scenario.yml`. F1/F2 varying-input diffs move as expected. F3: `pa run … --png` on default returns-mode sweep completes Excel with **zero** PNG artifacts (`pa_core/cli.py:1268-1446` delegates to sweep and returns before export-flag handling). F4–F6 not driven (Streamlit). Canonical scorecard: `Code/Audits/Portable-Alpha-Extension-Model/2026-09-23-SCORECARD.md`.

### Phases 2–4 (condensed)

| Area | Outcome |
|---|---|
| D3 wiring | #2307 still open and reproduced; not re-filed |
| Dedup | #2281, #2284, #2285 remain open from 2026-09-07; #2306 fixed on tip |
| Docs | No remaining “regimes ignored in sweeps” strings in repo (grep clean) |
| Product contract | No `docs/PRODUCT_CONTRACT.md` in repo; adoption issue **not** filed (see below) |
| Closed issues | #2306 claim refuted on tip; no closed-still-broken core-function rows |

### Filing

`gh` / `GH_TOKEN` unavailable in this environment — **no issues created**, format guard not checked.

Prepared but **not filed** (would be the allowed non-defect adoption issue; dedup not possible without API): body at `artifacts/audits/paem-20260923-issue-bodies/01-adopt-product-contract.md`.

No new verified defect beyond open **#2307** and the existing 2026-09-07 backlog (#2281, #2284, #2285).

### Confidence

**High** that filing zero new defect issues is correct on this tip: the only delta since the AM audit is the merged #2306 docs fix, and sweep PNG silence is already **#2307**. **Medium** on whether product-contract adoption should have been filed despite auth failure — skill permits one adoption issue per repo; would file when `gh auth login` or `GH_TOKEN` is available.

### Artifacts

- OUT (this file): `artifacts/audits/Portable-Alpha-Extension-Model-2026-09-23.md`
- Evidence: `artifacts/audits/paem-20260923-evidence-43a86ec/`
- Unit checkpoint: `artifacts/audits/D-audit-Portable-Alpha-Extension-Model--2026-09-23T22-11-14Z.CHECKPOINT.md`

### Attempt 2 reconciliation — 2026-09-24

The reissued unit was a stale queue claim, not a new scorecard failure: `program.newest_scorecard("Portable-Alpha-Extension-Model")` reads the canonical 2026-09-23 scorecard and parses the headline as 2 work / 1 partial / 0 broken / 0 fabricated / 3 not exercised; `refill_trigger_for` returns healthy. On the unchanged remote tip `43a86ec47b8aba361eb7a108013db9e5e1d7d3fe`, re-ran the exact open #2307 reproduction in the isolated audit venv: exit 0, workbook present, zero PNG artifacts. Evidence: `artifacts/audits/paem-20260923-evidence-43a86ec/attempt2-2307-observation.txt`. No new non-duplicate issue was filed. The closed #2306 claim remains refuted by the live disclaimer text at `pa_core/reporting/disclaimers.py:20-21`.
