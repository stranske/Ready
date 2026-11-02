Scorecard: 6 work / 1 partial / 0 broken / 0 fabricated / 1 not exercised of 8; journey: passes — full-product verification business journey PASS on isolated DB; surfaces unscored 4; closed-still-broken 0.

# stranske/trip-planner audit — 2026-11-02

Tip audited: `67b839e1f7cd0c2605ee40cadcc2d3b59527c7b0` on `main` (+1 doc commit since 2026-10-02 scorecard tip `8bca24b5`).

## Run summary

Track D refill (`audit-refill.md`: 2 open agent-ready vs threshold 2; scorecard age 31d). Phases: orientation, live product scorecard (`check_full_product_verification` + contract report + TP3/TP4 adversarial checks), dedup against open/closed issues, one verified filing.

**Issues filed (1):** [#1962](https://github.com/stranske/trip-planner/issues/1962) — `[P1] Contract probe omits trip origin so TP3 is falsely FABRICATED on every product-probe run`. Evidence: `scripts/check_full_product_verification.py:238-243`, `inventory.py:655-689`, compare figures in `Code/Audits/trip-planner/2026-11-02-assets/evidence/tp3-with-origin.txt`.

REFUTED: https://github.com/stranske/trip-planner/issues/1883 — on tip `67b839e`, `_extract_destination_mentions` no longer returns `Nov` and metadata blocks no longer re-ask for dates for the Oct audit reproduction string.

**Dedup (not re-filed):** Open #1910 owns publishing contract verdicts to CI (this issue fixes probe inputs only). Closed #1839 compare-truthfulness tests still pass (`tests/app/test_compare_truthfulness.py`). Sync-only open #1961 (Cross-Repo Smoke / dev-tool pin) is Workflows template debt, not a trip-planner product defect.

## Scorecard notes

- **TP3 WORKS** for UI-shaped trips (origin + destination vary lead `travel_minutes`). The shipped `run_contract_report()` path still reads **FABRICATED** until #1962 lands.
- **TP4 PARTIAL** — deterministic fallback without LLM credentials; not a regression.
- **TP7 NOT-EXERCISED** — print/export not re-run in browser this round; 2026-10-01 evidence retained.
- **surfaces unscored 4** — new handoff and flight-search API routes since 2026-10-01 inventory (listed in canonical `2026-11-02-SCORECARD.md`).

## Artifacts

- Canonical scorecard: `Code/Audits/trip-planner/2026-11-02-SCORECARD.md`
- Audit run: `2026-11-02-audit-run.md`, issue body `2026-11-02-issue-bodies/01-contract-probe-missing-origin.md`
- Probe output copy: unit scratch `product-probe.json` / `product-probe.log`

## Format guard

Run `41434489592` (Agents Issue Format Guard for #1962) completed **skipped** on 2026-11-02; re-check on next issue edit if `agents:formatted` is required for lanes.
