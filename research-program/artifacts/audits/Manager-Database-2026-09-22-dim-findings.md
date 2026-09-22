# Manager-Database dimension audit findings — 2026-09-22

**Repo:** `stranske/Manager-Database`  
**Tip:** `3c7d3f9c2f28d931cebb955f28c3f72db1a506a2`  
**Scope:** `api/`, `etl/`, `chains/`, `alerts/`, `adapters/`, `llm/`, `ui/`, `web/`, `embeddings.py`, `diff_holdings.py`, `utils/`  
**Excluded (already filed/fixed on tip):** #1706 (new_filing condition keys), #1707 (acknowledge-all filters), #1708 (duplicate CIK), #1709 (bulk import atomicity)

---

## Finding 1 — Postgres `search_documents` manager join uses filter id, not document FK

**Severity:** [MAJOR]

**Evidence:** `embeddings.py:303-308`

```python
manager_join = str(int(manager_id)) if manager_id is not None else "d.manager_id"
...
f"FROM documents d LEFT JOIN managers m ON {manager_join} = m.manager_id "
```

When `manager_id` is passed, SQL becomes `LEFT JOIN managers m ON 42 = m.manager_id` instead of joining through `d.manager_id` (or `document_managers`). Every returned row gets the same `manager_name` (manager #42) regardless of which manager owns the document; if that manager does not exist, `manager_name` is always `NULL`.

**Reproduction:**

```bash
cd [LOCAL_WORKSPACE]/Manager-Database
python3 -c "
import embeddings
from unittest.mock import patch

class Conn:
    info = object()
    def execute(self, sql, params=None):
        print(sql.split('FROM documents')[1].split('WHERE')[0].strip())
        class R:
            def fetchall(self): return []
        return R()
    def close(self): pass

with patch.object(embeddings, 'connect_db', lambda p=None: Conn()):
    with patch.object(embeddings, 'register_vector', None):
        with patch.object(embeddings, 'embed_text', lambda t: [0.1]*384):
            embeddings.search_documents('q', manager_id=42, k=3)
"
# Expect bug: prints "d LEFT JOIN managers m ON 42 = m.manager_id"
```

**Core function:** MDB-4 (search / document retrieval); also affects `chains/rag_search.py:108` (`_vector_search` → `search_documents`).

**Likely GitHub issue:** No — not covered by closed #1696–#1709 or open alert/manager issues from 2026-09-21 dossier.

---

## Finding 2 — `large_delta` alert UI offers `net` but ETL never emits it

**Severity:** [MAJOR]

**Evidence:**

- `ui/alerts.py:172-186` — selectbox includes `"net"` and persists `condition_json["delta_type"] = "net"`.
- `alerts/engine.py:88-90` — exact string match: `payload.get("delta_type") != expected` → rule fails.
- `etl/daily_diff_flow.py:229-234` — normalizes `ADD`/`INCREASE` → `"buy"`, `EXIT`/`DECREASE` → `"sell"` only; `"net"` is never produced.

**Reproduction:**

```bash
cd [LOCAL_WORKSPACE]/Manager-Database
python3 -c "
import json, sqlite3
from alerts.db import ensure_alert_tables
from alerts.engine import AlertEngine
from alerts.models import AlertEvent

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE managers (manager_id INTEGER PRIMARY KEY, name TEXT)')
ensure_alert_tables(conn)
conn.execute(
    'INSERT INTO alert_rules(name, event_type, condition_json, channels, enabled) VALUES (?,?,?,?,?)',
    ('net rule', 'large_delta', json.dumps({'delta_type': 'net', 'value_usd_gt': 0}), '[\"streamlit\"]', 1),
)
conn.commit()
buy = AlertEvent(event_type='large_delta', manager_id=1, payload={'delta_type': 'buy', 'value_usd': 500000})
sell = AlertEvent(event_type='large_delta', manager_id=1, payload={'delta_type': 'sell', 'value_usd': 500000})
print('matches buy:', len(AlertEngine(conn).evaluate(buy)))
print('matches sell:', len(AlertEngine(conn).evaluate(sell)))
"
# Both print 0 — net rules can never fire.
```

**Core function:** MDB-8 (alerts rule evaluation / UI rule builder).

**Likely GitHub issue:** No — distinct from fixed #1706 (`new_filing` key mismatch).

---

## Finding 3 — Postgres `universal_search` skips pgvector document retrieval

**Severity:** [MAJOR]

**Evidence:**

- `api/search.py:610-654` (`_search_sqlite`) — after LIKE match, calls `embeddings.search_documents` for semantic hits and merges them into ranked results.
- `api/search.py:423-475` (`_search_postgres`) — document branch uses FTS (`to_tsvector` / `plainto_tsquery`) only; never calls `search_documents` or pgvector distance despite `embeddings.py:289-325` implementing Postgres vector search.

SQLite dev/test therefore exercises semantic document search via `GET /api/search`; production Postgres does not, even when `documents.embedding` is populated.

**Reproduction:**

```bash
cd [LOCAL_WORKSPACE]/Manager-Database
rg -n "search_documents" api/search.py
# Only appears in _search_sqlite block (~line 612), not in _search_postgres.

pytest tests/test_search.py::test_universal_search_sqlite_uses_embedding_search_for_documents -q
# Passes — proves SQLite path uses embeddings.

pytest tests/test_search.py -k "postgres and embedding" -q
# No postgres+embedding parity test exists.
```

**Core function:** MDB-4 (`GET /api/search?q=…`; Search UI via `ui/search.py:99`).

**Likely GitHub issue:** No — not in #1696–#1709; separate from alert/manager refill.

---

## Finding 4 — `diff_holdings` silently drops duplicate CUSIPs within one filing

**Severity:** [MINOR]

**Evidence:** `diff_holdings.py:96-103` — holdings fetched into `{cusip: {...}}` dict; duplicate `cusip` rows overwrite earlier rows with no warning.

**Reproduction:**

```bash
cd [LOCAL_WORKSPACE]/Manager-Database
python3 -c "
import sqlite3
from diff_holdings import _fetch_holdings_for_filing

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE holdings (cusip TEXT, shares INTEGER, value_usd REAL, name_of_issuer TEXT, filing_id INTEGER)')
conn.executemany('INSERT INTO holdings VALUES (?,?,?,?,?)', [
    ('037833100', 100, 1000.0, 'Apple A', 1),
    ('037833100', 200, 2000.0, 'Apple B', 1),
])
print(_fetch_holdings_for_filing(conn, 1))
"
# Prints single entry with shares=200 (second row wins); first row lost.
```

**Core function:** Interior / holdings diff pipeline (feeds `etl/daily_diff_flow.py` and MDB-2 delta outputs).

**Likely GitHub issue:** No — not in recent #1696–#1709 set.

---

## Summary

| Severity | Count |
|----------|------:|
| BLOCKER  | 0 |
| MAJOR    | 3 |
| MINOR    | 1 |

**Top one-liners:**

1. Postgres `search_documents(manager_id=…)` JOINs `m.manager_id` to the filter literal, mis-attributing (or nulling) manager names.
2. Alert rules with `delta_type: "net"` can never match because ETL only emits `buy`/`sell`.
3. Postgres `/api/search` has no pgvector document path while SQLite does — semantic search parity gap in production.
4. `diff_holdings` collapses duplicate CUSIPs per filing via dict overwrite without surfacing data-quality signal.
