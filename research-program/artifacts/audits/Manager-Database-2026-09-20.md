Scorecard: 4 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: stops at "dashboard Historical Filing Trend raises DatabaseError on manager-only SQLite"; surfaces unscored 0; closed-still-broken 0.

Issues filed: 4 ([#1696](https://github.com/stranske/Manager-Database/issues/1696), [#1697](https://github.com/stranske/Manager-Database/issues/1697), [#1698](https://github.com/stranske/Manager-Database/issues/1698), [#1699](https://github.com/stranske/Manager-Database/issues/1699)). Agents Issue Format Guard success on all four (runs 35538240882, 35538188399, 35538189237, 35538190761).

# Manager-Database audit — 2026-09-20

**Tip:** `54e4f406daa4543e9fbfc693faeb99df615cf47f` (`docs: add PRODUCT_CONTRACT.md (core functions the audit scores) (#1695)`)

## Verdict

Track D refill after the 2026-09-14 batch (#1667–#1675) largely landed within six days. This round exercised all seven product-contract core functions live or via targeted API/pytest probes, re-ran closed-issue reproductions (zero closed-still-broken), and filed four verified defects that were not duplicates of open or recently closed work.

| Priority | Finding | Evidence | Filed |
| --- | --- | --- | --- |
| P1 | DELETE /managers/{id} returns 204 while filings and documents remain | `api/managers.py:488-495`; live repro: filings=1 documents=1 after DELETE | [#1696](https://github.com/stranske/Manager-Database/issues/1696) |
| P1 | Dashboard `load_delta()` crashes when `filings` table is absent | `ui/dashboard.py:48-64`; `DatabaseError: no such table: filings` on managers-only SQLite | [#1697](https://github.com/stranske/Manager-Database/issues/1697) |
| P2 | GET /managers ignores `search` and `name` query filters (MDB-2 partial) | `api/managers.py:983-1007`; `search=OnlyOne` returns both managers | [#1698](https://github.com/stranske/Manager-Database/issues/1698) |
| P2 | Conviction scores API accepts `min_conviction_pct=inf` | `api/signals.py:443-453`; HTTP 200 for infinity vs 422 for NaN | [#1699](https://github.com/stranske/Manager-Database/issues/1699) |

## Product scorecard (Phase 1.5)

| ID | Core function | Score | How exercised |
| --- | --- | --- | --- |
| MDB-1 | Add manager, see ID in list | WORKS | TestClient POST two managers → ids 1, 2 |
| MDB-2 | Find managers with filtered list | PARTIAL | jurisdiction filter works; `search`/`name` ignored → #1698 |
| MDB-3 | Record/query holdings, see diffs | WORKS | pytest `tests/test_diff_holdings.py`; PIT amendment repro shares 200 |
| MDB-4 | Search entities, ranked snippets | WORKS | GET /api/search?q=Alpha → one manager hit |
| MDB-5 | Research corpus, grounded answer | WORKS | GET /chat returns structured empty-corpus response |
| MDB-6 | Dashboard KPIs and filing trend | PARTIAL | `load_delta()` raises on managers-only DB → #1697 |
| MDB-7 | Upload documents linked to manager | WORKS | pytest `tests/test_upload.py::test_upload_text_and_markdown_store_in_documents` |

**Primary journey:** register manager → ingest/search/research → dashboard. Stops at Historical Filing Trend when the local SQLite bootstrap has managers but no `filings` table (typical after first POST /managers).

**Closed-still-broken:** re-ran #1668 (PIT amendment authority — fixed, shares 200), #1671/#1672 (SQLite key resolution — fixed via `resolve_manager_id_column`). None of the nine 2026-09-14 issues reproduce at tip.

## Dimension coverage (abbreviated)

| Dim | Notes |
| --- | --- |
| D1 | Four verified defects above; evidence-object schema divergence noted but not filed (interior contract work; #1088 closed arc) |
| D2 | No actionable duplication campaign beyond upstream Workflows sync |
| D3 | Dominant wiring gaps: DELETE cascade, list filters, dashboard guard |
| D4 | Streamlit pages inventoried; login path fixed (#1667); alerts page present (#1673) |
| D5–D8 | No filable near-term items beyond the four defects |

## Verification

- Issue bodies validated locally via `.github/scripts/issue_format.py` (all conforming).
- Format guard: success runs 35538240882 (#1696 manual dispatch), 35538188399 (#1697), 35538189237 (#1698), 35538190761 (#1699).
- Open agent-ready supply before audit: 1 (#1682); after filing: 5 including new issues (labels `bug`, `priority:*`, `testing` only — no auto-dispatch).
- Canonical artifacts: `Code/Audits/Manager-Database/2026-09-20-SCORECARD.md`, `2026-09-20-AUDIT_REPORT.md`.

Confidence: **high** for #1696–#1699. #1696 would be refuted only by a cascade that leaves zero dependent rows after DELETE on both SQLite and Postgres. #1697 by an empty-frame guard covered by the named test. #1698 by working SQL filters on both parameters. #1699 by HTTP 422 for infinity at the API boundary.
