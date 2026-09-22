Scorecard: 8 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

# Manager-Database Track D follow-up audit — 2026-09-22

**Audited tip:** `77be429e8d2f04c9c6ed83303e9fd835d757a521` (`main`)

The previous refill's three P1 findings have all landed and were re-exercised before this disposition: #1715 fixes the Postgres document-owner join in `embeddings.py:307-327`; #1716 makes `net` alert rules match emitted buy/sell deltas in `alerts/engine.py:88-98`; and #1717 merges Postgres vector-document hits into unified search in `api/search.py:491-526`. All three issues are closed. The independently launched Cursor read pass did not produce an artifact and was stopped after four minutes, so this conclusion rests only on the recorded local evidence and current remote CI.

## Product scorecard

The primary journey—register manager, ingest/search, research, dashboard, and alerts—passes in the isolated SQLite/API harness. Focused real-entry-point tests exercised distinct manager IDs and duplicate-CIK rejection (MDB-1), changed list-filter results (MDB-2), holdings diff fixtures (MDB-3), document and vector search (MDB-4), chat endpoint (MDB-5), the no-filings dashboard empty state (MDB-6), text/Markdown upload persistence (MDB-7), and positive/negative alert matching (MDB-8). The targeted product probes passed 5/5; the broader regression set passed 162 tests with one intentional skip. Current scheduled and maintenance workflows on the audited SHA are green.

## Audit outcome

No new actionable defect was established. I reviewed the newly merged seam code and its dedicated tests, rechecked open issues (only #1682 is an existing Postgres-CI coverage item; the other two open entries are durable holders), and did not file speculative duplicates. The only prospective concern—how multiple manager associations are presented by the Postgres vector branch—does not have a live failure reproduction, so it is not a filing candidate.

## Coverage and reconciliation

App-local paths were audited; synced `tools/`, `scripts/langchain/`, and CI wrappers remain out of scope. Dimension 1–4 evidence came from live targeted tests and line-by-line verification of the new search/alert seams. Dimensions 5–8 were reconciled against the current ledger and open-issue set; no new evidence supports a product, tooling, or automation issue. Every candidate is either verified fixed, already tracked, or insufficiently evidenced. No issue bodies or measurement-intake rows were created in this round.
