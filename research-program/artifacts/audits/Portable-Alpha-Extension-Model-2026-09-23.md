Scorecard: 2 work / 1 partial / 0 broken / 0 fabricated / 3 not exercised of 6; journey: passes at CLI through sweep metrics and Excel export, stops at Streamlit wizard/results and silent PNG on default sweep path; surfaces unscored 3; closed-still-broken 0.

Issues filed: 2 — https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2306, https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2307

REFUTED: https://github.com/stranske/Portable-Alpha-Extension-Model/issues/1910 — regime-enabled sweeps now change `Total` `terminal_AnnReturn` by ~0.0077 vs a no-regime config on the same seed (see `artifacts/audits/paem-20260923-evidence/regime-sweep-diff.txt`).

## Run report — Track D — 2026-09-23

**Repo:** `stranske/Portable-Alpha-Extension-Model` @ `a1a872e7`  
**Unit:** `D-audit-Portable-Alpha-Extension-Model--2026-09-23T09-11-16Z`

### Phase 0–1

Shallow clone created (prior `./clones` path missing). Read dossier, Dropbox `Code/Audits/Portable-Alpha-Extension-Model/` continuity (2026-09-20 product contract; no parseable 2026-09-20 scorecard file). Orientation: 598 py/md files, seven Streamlit pages, `pa` CLI subcommands; isolated venv install from `requirements-dev.txt`; golden tutorials **11 passed**.

Open agent-ready issues before round: **4** (refill threshold 3 per `artifacts/audit-refill.md`).

### Phase 1.5 (scorecard)

Core functions F1–F6 from `Code/Audits/Portable-Alpha-Extension-Model/2026-09-20-product-contract.md`. Live CLI exercises with varying-input diffs for F1–F2; F3 export partial (Excel OK, `--png` absent on sweep path). F4–F6 not driven (Streamlit); not scored as fabricated. Full scorecard: `Code/Audits/Portable-Alpha-Extension-Model/2026-09-23-SCORECARD.md`.

### Phases 2–4 (condensed)

| Area | Outcome |
|---|---|
| D3 wiring | Stale regime disclaimer vs live `sweep.py` regime paths → **#2306** |
| D3 wiring | Sweep CLI branch returns before `--png` handling → **#2307** |
| Dedup | #2281 still open (InternalPA CRN); not re-filed; alpha_shares repro delta 0 on tip (may differ from issue’s theta sweep) |
| Dedup | #2284, #2285 remain open; wheel missing `templates/` confirmed (`pyproject.toml` package-data only ships `data/*.csv`) |
| Closed issues | #2278–#2280, #2282–#2283, #2286–#2287 closed; F1 θ probe and golden tests green; no closed-still-broken rows |

### Filing

| Issue | Title |
|---|---|
| [#2306](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2306) | [P1] Model limitations falsely claim regimes are ignored in parameter sweeps |
| [#2307](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2307) | [P1] CLI --png/--pdf/--pptx silently ignored on parameter-sweep path |

Format guard workflow run **skipped** for both issues within 45s; labels show `priority: high` only (no `agents:formatted` yet).

### Artifacts

- OUT (this file): `artifacts/audits/Portable-Alpha-Extension-Model-2026-09-23.md`
- Evidence: `artifacts/audits/paem-20260923-evidence/`
- Issue bodies: `artifacts/audits/paem-20260923-issue-bodies/`
- Checkpoint: `artifacts/audits/D-audit-Portable-Alpha-Extension-Model--2026-09-23T09-11-16Z.CHECKPOINT.md`

### Not filed (with reason)

- `run-contract/v1` emitter / `scripts/emit_reference_run.sh` — fleet integration epic; no open duplicate found; defer to dedicated conformance issue when owner prioritizes backplane opt-in.
- `Scenario.sleeves` unwiring — acknowledged in schema/README; not a contradicted promise.
- Streamlit UX — not observed this round (coverage gap recorded in scorecard, not a defect filing).
