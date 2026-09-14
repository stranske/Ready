# Manager-Database ETL/data-integrity review

**Audit unit:** `D-audit-Manager-Database--2026-09-14T06-49-50Z`  
**Baseline:** `4523cf50dac3f3fe2ba338b8243e630940c54fd0` (`main`)  
**Scope reviewed:** `etl/`, `adapters/`, `diff_holdings.py`, `schema.sql`,
`alembic/`, `embeddings.py`, and focused tests. Read-only review; no repository
changes, issue filing, or remote mutation.

## Executive judgment

Five actionable defects are verified. The strongest is authority-selection drift:
the holdings-diff path explicitly prefers an amendment on a filing-date tie, but
the point-in-time path silently takes the largest ID instead. That is a data
integrity defect, not merely an ordering preference, because point-in-time
holdings feed both backtesting and attribution.

The other high-confidence findings are manager-attribution loss caused by global
document hash deduplication, a non-atomic legacy scheduled EDGAR path, duplicate
news alerts for a batch duplicate, and repeated OpenFIGI calls for known-unmapped
CUSIPs. Four are direct deterministic SQLite repros; the OpenFIGI behavior is
deterministic but its priority assumes repeated ingestion and a constrained API
quota. No provider or production calls were made.

## Verified findings

| ID | Severity | Finding | Confidence |
| --- | --- | --- | --- |
| ETL-1 | P1 / major | Point-in-time authority selection can return an original rather than a same-day amendment | High |
| ETL-2 | P1 / major | Document hash deduplication drops the second manager association | High |
| ETL-3 | P1 / major | Scheduled EDGAR wrapper commits a filing document before the filing transaction | High |
| ETL-4 | P2 / normal | Duplicate items in one news batch inflate a `news_spike` alert | High |
| ETL-5 | P2 / normal | OpenFIGI retries every known-unmapped CUSIP without a bounded negative-cache policy | High on behavior; medium on operational impact |

### ETL-1 — point-in-time selection disagrees with amendment reconciliation

**Evidence.** `diff_holdings.py:62-72` ranks candidates by filed date, then
amendment status, then filing ID; its function contract says the latest amendment
is authoritative (`diff_holdings.py:28-34`). In contrast,
`etl/point_in_time.py:101-136` selects each period only by `filed_date` and
`filing_id`; it never selects or ranks `filings.type`. Its output is consumed by
the backtest boundary (`etl/backtest_flow.py:245-248`) and the attribution
boundary (`etl/attribution_flow.py:195-208`).

**Impact.** When an original and `13F-HR/A` share the date granularity retained
by `filings.filed_date`, an ID assignment/order in which the original has the
larger ID makes `holdings_as_of()` return the original portfolio. That corrupts
historical holdings and any backtest or attribution built from it. The existing
test exercises an amendment only when it has a later filing date
(`tests/test_bitemporal_holdings.py:82-119`), so it cannot detect this tie.

**Offline reproduction.** Create SQLite filings for one manager and period:
`(id=1, type='13F-HR/A', filed_date='2024-05-15', holding='AMENDED')` and
`(id=2, type='13F-HR', filed_date='2024-05-15', holding='ORIGINAL')`, with both
holdings known by May 16. Calling
`holdings_as_of(conn, 7, date(2024, 5, 16))` returned `['ORIGINAL']` at the
audited SHA. The correct shared selector would choose `AMENDED`.

**Fix/test shape.** Centralize the authoritative-filing rank (period, filed date,
amendment status, stable ID) and use it from `diff_holdings.py`,
`etl/point_in_time.py`, `etl/manager_similarity_flow.py`, and the attribution
filing lookup. Add a same-day original/amendment test with intentionally inverted
IDs, plus the existing later-date case. Preserve pre-amendment visibility by
applying the knowledge-time cut before authority ranking.

**Dedup/refutation.** Closed #1324 implemented reconciliation in the diff/ingest
path; its supplied issue body does not cover this point-in-time tie. Closed #1463
introduced the bitemporal layer, but the current selector still lacks a type
rank. This is not a duplicate of open #1653 (Postgres DDL for similarity).
The defect requires a same-date tie, so it is not a claim that every amendment is
wrong.

### ETL-2 — global text deduplication loses manager provenance

**Evidence.** The canonical documents schema contains a scalar `manager_id`
(`schema.sql:393-401`) but makes `sha256` globally unique
(`schema.sql:404-406`). `embeddings.py:145-191` inserts on that hash conflict
and returns the existing document ID without adding any relationship or updating
the manager. SQLite does the same with `INSERT OR IGNORE` followed by a hash-only
lookup (`embeddings.py:207-249`). Searches may filter by `manager_id`
(`embeddings.py:272-298`, `embeddings.py:316-337`).

**Impact.** The same memo/filing text uploaded or ingested for a second manager
is stored only under the first manager; manager-filtered RAG/search silently
cannot retrieve it for the second. This violates the metadata wiring introduced
for manager-filtered filing text and can produce misleading absence-of-evidence
results.

**Offline reproduction.** In a fresh SQLite database with managers 1 and 2,
calling `store_document('same memo', manager_id=1)` and then the identical call
with `manager_id=2` returned IDs `1, 1`; querying documents yielded only
`[(manager_id=1, count=1)]`. This uses `USE_SIMPLE_EMBED=1` and no model/network.

**Fix/test shape.** Choose and document one model: either make uniqueness
manager-scoped (for example a partial unique key on `(manager_id, sha256)`) or
keep a globally deduplicated document table and add a `document_managers` relation
used by storage and search. Cover two managers sharing content, global/unlinked
documents, both SQLite and Postgres, and an ingestion caller.

**Dedup/refutation.** Closed #1628 correctly passes manager metadata to generic
ingestion; it does not alter the global hash uniqueness or add multi-manager
provenance. The existing hash-dedup test (`tests/test_embeddings.py:80-103`)
checks repeat storage but only one manager. A global singleton may be intentional
only if documents are deliberately unowned; the current schema and manager
filters contradict that interpretation.

### ETL-3 — the scheduled EDGAR compatibility path is not transactionally aligned

**Evidence.** The generic ingest path deliberately documents one database
transaction for index and filing writes (`etl/ingest_flow.py:643-656`) and passes
its already-open connection to `store_document` (`etl/ingest_flow.py:693-703`).
The actually deployed wrapper delegates each CIK to its own
`etl/edgar_flow.py:447-455` `fetch_and_store`. That wrapper opens `conn` at
`etl/edgar_flow.py:371-375`, calls `store_document` with only `db_path` at
`etl/edgar_flow.py:393-403` (therefore a second connection which commits inside
`embeddings.py:126-134`), and only subsequently parses, upserts, replaces
holdings, and commits (`etl/edgar_flow.py:405-422`).

**Impact.** A parse, filing upsert, or holdings failure leaves a searchable
`filing_text` document that has no corresponding filing/holdings record. It also
reintroduces the second-connection locking/atomicity risk which generic ingest
was explicitly changed to avoid. Raw-object persistence is separately intended;
the orphaned database index is not.

**Offline reproduction.** With a temporary SQLite schema and a stub adapter,
force `_upsert_filing_legacy` to raise after the wrapper has indexed raw XML.
After `fetch_and_store.fn()` raises, the database contained `orphan_docs=1` and
`filings=0`. No S3 or provider call was made.

**Fix/test shape.** Retire the parallel persistence implementation or make the
wrapper pass `connection=conn` and place all per-filing DB work in a rollback and
unconditional-close boundary. Add an EDGAR-wrapper regression that forces a
post-index write failure and proves zero documents, filings, and holdings commit;
retain the documented independent S3 retention behavior.

**Dedup/refutation.** Closed #1309 and #1628 fixed lifecycle/metadata in generic
`etl/ingest_flow.py`; neither removes this current separately scheduled legacy
path. Existing EDGAR tests monkeypatch the wrapper's document writer
(`tests/test_edgar_flow.py:220-235`, `tests/test_edgar_flow.py:499-505`), which
masks the connection/commit boundary. This finding does not assert S3 rollback.

### ETL-4 — intra-batch duplicates alert before persistence deduplicates

**Evidence.** `etl/news_flow.py:334-345` calls `SELECT` once per input item but
does not remember a candidate already selected in the current batch. The flow
then sends that pre-insert list to alerts (`etl/news_flow.py:374-379`). Persistence
uses `ON CONFLICT(url, published_at) DO NOTHING` (`etl/news_flow.py:296-325`),
while `emit_news_spike_alerts` increments `news_count` for every supplied item
(`etl/news_flow.py:191-224`).

**Impact.** Two copies of a source item in one fetch (for example overlapping RSS
feeds or repeated provider results) create one database row but an alert payload
with `news_count=2`. This can cross an alert threshold and makes downstream
analyst evidence disagree with the stored news table.

**Offline reproduction.** For two equal item dictionaries with the same URL and
publication time, `inserted_news_items()` returned 2 while
`persist_news.fn()` inserted 1. The alert call therefore receives both copies.

**Fix/test shape.** Deduplicate candidates by the same non-null conflict key
before alert aggregation, or have persistence return the records it actually
inserted (`RETURNING` on Postgres plus an SQLite equivalent). Add a duplicate
within one batch and an already-persisted duplicate test, verifying one stored
row and an alert payload of `news_count=1`.

**Dedup/refutation.** The unique index prevents database duplication but does not
prevent the pre-write alert inflation. No supplied open/recent issue targets
news alert candidate identity. The defect is conditional on duplicated input;
it does not claim each source always duplicates records.

### ETL-5 — unmapped CUSIPs are repeatedly sent to OpenFIGI

**Evidence.** `adapters/openfigi.py:236-245` considers every CUSIP absent from
the positive cache as missing and sends it to `map_cusips`; only nonempty live
resolutions are persisted (`adapters/openfigi.py:240-243`). No negative state,
attempt timestamp, or retry policy exists. The cache schema has no such field
(`adapters/openfigi.py:160-216`).

**Impact.** A common valid-but-unmapped CUSIP incurs a network request on every
filing/reingestion and continues consuming the conservative keyless pacing
budget. It increases ingest latency and provider-load risk while the resulting
unmapped-rate metric communicates no distinction between a first miss and a
known miss.

**Offline reproduction.** A fake OpenFIGI client returning `[{}]` for CUSIP
`111111111` was invoked twice across two `resolve_holding_identifiers()` calls;
`identifier_resolution_cache` still had zero rows.

**Fix/test shape.** Store a negative resolution state with `attempted_at` and a
bounded retry TTL/configuration; treat it as unmapped for metrics while excluding
it from live lookup until retry is due. Test first miss, second call inside TTL,
and a refreshed lookup after TTL. Do not make misses permanent because provider
coverage can improve.

**Dedup/refutation.** Closed #1321 added positive resolution and unmapped-rate
metrics, not negative caching. Retrying may be a deliberate freshness tradeoff,
which would lower this to a documented operational decision; absent a TTL or
stated policy, the current behavior is an unbounded repeat request.

## Review controls and dispositions

- The provided dedup corpus (150 open/recently closed issue records) was searched
  for ETL, adapter, amendment, bitemporal, embeddings, upload, schema, EDGAR,
  OpenFIGI, and backtest terms. It shows open #1653 (Postgres manager-similarity
  DDL), which is deliberately excluded as already open, and closed #1298, #1309,
  #1324, and #1628, which were read and distinguished above.
- A direct live `gh issue list` recheck could not run because this worker has no
  authenticated `gh` session. The supplied corpus is therefore the dedup
  authority used here; a lead filing these findings should rerun the live search.
- Focused offline tests for bitemporal holdings, diffs, embeddings, OpenFIGI,
  EDGAR flow, and news flow completed without a test failure at this SHA. The
  failures above pass because their boundary cases are absent from those tests.
- Rejected as non-novel or already tracked: PostgreSQL manager-similarity DDL
  (open #1653); generic ingest document metadata/transaction work (closed #1628);
  generic ID and re-ingest duplication work (closed #1302/#1298); and ordinary
  later-dated 13F amendments (covered by the current diff and bitemporal tests).

## Suggested implementation order

1. ETL-1: repair the shared authoritative-filing contract before relying on
   backtest, attribution, or similarity outputs.
2. ETL-3: remove the scheduled-wrapper transaction fork; it can create lasting
   database provenance errors on a failed ingest.
3. ETL-2: decide the document ownership model, then migrate safely.
4. ETL-4 and ETL-5: tighten alert and provider behavior with bounded tests.

