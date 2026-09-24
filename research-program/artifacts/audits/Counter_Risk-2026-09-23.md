Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes; surfaces unscored 2; closed-still-broken 0.

Issues filed: 1 (this attempt) — https://github.com/stranske/Counter_Risk/issues/1113 ([P2] PRODUCT_CONTRACT status stale). Prior same-day attempt filed #1112 (still open).

REFUTED: https://github.com/stranske/Counter_Risk/issues/1062 — split Alpha rows now consolidate before HHI (`rollups.py:598-608`; `test_split_counterparty_preserves_concentration` PASS on tip).

## Run report — Track D refill attempt 2 — 2026-09-23

**Unit:** `D-audit-Counter_Risk--2026-09-23T22-11-15Z`  
**Tip:** `2f92b174303f3ef977828ed4588794fcec42e6ef` (unchanged since morning attempt).

### Why attempt 2 ran

`program.py` `newest_scorecard(Counter_Risk)` read `Code/Audits/Counter_Risk/2026-09-23-SCORECARD.md` and returned **no parseable headline** — the morning round wrote the scorecard tables but omitted the load-bearing `Scorecard: …` line required by `reference/product-scorecard.md`. That falsely re-triggered Track D despite a complete morning audit.

### Corrective + verification actions

- Inserted the canonical headline into `Code/Audits/Counter_Risk/2026-09-23-SCORECARD.md` (line 3).
- Re-ran Phase 1.5 probes on tip: fixture-replay CF1 → `/tmp/cr-audit-20260923-attempt2`; CF3–CF5 targeted pytest gates green (13 + 5 + 1 tests).
- Phase 3: closed #1062 reproduction no longer shows split-row concentration drift; #1104/#1107 fixes remain green.
- Phase 4: filed #1113 for stale `docs/PRODUCT_CONTRACT.md` status (distinct from #1112 audit-log supersession). Open #1106 (`_format_deltas` first-mover-only) unchanged and not re-filed.

### Surface inventory

CLI unchanged: `counter-risk {run,gui}`, `mapping_diff_report`. Unscored: Runner.xlsm COM workflow (CF6), frozen PyInstaller bundle (CF7).

### Format guard

Agents Issue Format Guard: success on #1113 (run 35938041921).
