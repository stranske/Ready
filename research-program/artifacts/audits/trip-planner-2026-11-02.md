Scorecard: 5 work / 3 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes — full-product verification business journey PASS on isolated DB; surfaces unscored 0; closed-still-broken 0.

# stranske/trip-planner audit — 2026-11-02 (resume @ e9a53fa)

Tip audited: `e9a53fadb56fb988ddb9df30711a76b3171db669` on `main` (#1963 merges contract-probe origin fix from closed #1962).

## Run summary

Track D refill (`audit-refill.md`: coverage debt 5 — not exercised 1 + unscored 4 — unchanged on the 2026-11-02 morning scorecard at `67b839e`). This pass re-ran the scorecard on the **current** tip after #1963, scored the four API surfaces added since 2026-10-01, and filed one verified documentation drift issue.

**Issues filed (1):** [#1964](https://github.com/stranske/trip-planner/issues/1964) — `[P2] PRODUCT_CONTRACT status column contradicts live product-probe on main`. Evidence: `docs/PRODUCT_CONTRACT.md:24-35` still marks TP3 `FABRICATED` and TP5–TP7 `BROKEN` while `python scripts/check_full_product_verification.py --live-tpp off --contract-report product-probe.json` on this tip prints `WORKS 4, PARTIAL 3, BROKEN 0, FABRICATED 0 of 7`.

**Prior filing this calendar day:** [#1962](https://github.com/stranske/trip-planner/issues/1962) closed fixed via #1963 on tip; not re-filed.

**Dedup (not re-filed):** Open #1910 owns publishing per-function probe verdicts to CI. Open #1961 is Workflows sync/dev-tool debt. TP3 `PARTIAL` is the contract probe’s party-size pair (travel_minutes identical for party 1 vs 8); destination pair moves (410 vs 643 min) — product behavior, not missing origin.

## Scorecard notes

| id | verdict | note |
|---|---|---|
| TP1–TP2, TP5–TP6 | WORKS | contract probe |
| TP3, TP4, TP7 | PARTIAL | TP3 party determinant flat; TP4 deterministic fallback; TP7 backend-only packet inputs per `_probe_packet` |
| TP8 enter sourced prices | WORKS | business journey PUT `/api/workspace/{id}/prices` in full-product verification |

**surfaces unscored 0** — exercised this round: `POST /api/workspace/{trip_id}/flights/search` (`tests/app/test_flight_search_sandbox.py`, 21 passed); `POST .../proposal/handoff`, `.../handoff/status`, `.../handoff/submit` (`tests/app/test_proposal.py -k handoff`, 60 passed).

**UX panel:** not re-run; no new UX-gate line.

## Commands / evidence

```text
TRIP_PLANNER_DATABASE_URL=sqlite:///<unit-scratch>/trip_planner_audit2.db \
  python scripts/check_full_product_verification.py --live-tpp off --contract-report product-probe2.json
# → product-probe: WORKS 4, PARTIAL 3, BROKEN 0, FABRICATED 0 of 7
```

Canonical scorecard mirror: update `Code/Audits/trip-planner/2026-11-02-SCORECARD.md` with tip `e9a53fa` and unscored 0 (Dropbox ledger).

## Format guard

Format guard run `41541563223` for #1964 completed **skipped** on 2026-11-02.
