Scorecard: 7 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: #1715, #1716, #1717 (3 P1).

# Manager-Database Track D audit — 2026-09-22

**Tip:** `3c7d3f9c2f28d931cebb955f28c3f72db1a506a2`  
**Trigger:** audit refill (1 open agent-ready ≤ 25% of last set of 4)

## Summary

Re-audited after the 2026-09-21 batch merged (#1706-#1709). All four prior fixes re-verified on tip. Eight core functions exercised live; MDB-4 scored PARTIAL because production Postgres paths lack semantic search parity and mis-attribute manager names in filtered vector retrieval. Three new P1 issues filed.

## Closed-issue re-probe

| issue | result |
|---|---|
| #1706 new_filing alert keys | fixed — AlertEngine fires |
| #1707 acknowledge-all filters | fixed — merged |
| #1708 duplicate CIK | fixed — HTTP 409 |
| #1709 bulk import atomicity | fixed — merged #1713 |

## Findings filed

1. **#1715** — `embeddings.py:303-308` Postgres `search_documents` joins `m.manager_id` to the filter literal instead of the document owner (MDB-4).
2. **#1716** — `ui/alerts.py:172-186` offers `delta_type: net` but ETL only emits `buy`/`sell` (MDB-8).
3. **#1717** — `api/search.py` Postgres branch uses FTS only; SQLite merges pgvector hits (MDB-4).

## Declined

- `diff_holdings.py:96-103` duplicate CUSIP dict overwrite — MINOR interior data-quality; no user-visible failure path filed.

## Artifacts

- Scorecard: `Code/Audits/Manager-Database/2026-09-22-SCORECARD.md`
- Issue bodies: `Code/Audits/Manager-Database/2026-09-22-issue-bodies/`
- Dimension notes: `artifacts/audits/Manager-Database-2026-09-22-dim-findings.md`
