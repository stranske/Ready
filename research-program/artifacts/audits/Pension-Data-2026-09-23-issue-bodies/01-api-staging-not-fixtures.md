## Why (verified evidence)
Product core function **F2** (`docs/PRODUCT_CONTRACT.md:14`) requires plan analytics keyed by entity after a pilot run. The internal FastAPI app always injects hard-coded CA-PERS fixtures and never reads pilot/staging output:

- `src/pension_data/api/app.py:71` passes `_fixture_funding_trend_inputs()` into `run_saved_view_endpoint` regardless of request or environment.
- `src/pension_data/api/app.py:95` passes `_fixture_metric_history_rows()` (single CA-PERS `funded_ratio` at `0.81`, `benchmark_version="fixture-v1"`) into `run_metric_history_endpoint`.
- `_fixture_*` definitions at `src/pension_data/api/app.py:164-212` are static; no call into `src/pension_data/query/metric_history_service.py:123-130` (`build_metric_history_rows`) or staging persistence.

**User-facing consequence:** after `one-pdf-pilot` publishes `SYN-PLAN` metrics (e.g. funded ratio `0.784` in `staging_core_metrics.json`), `pension-data-serve` still returns fixture `CA-PERS` / `0.81` for `/api/metric-history/CA-PERS` and zero rows for `/api/metric-history/SYN-PLAN`. The primary journey stops at “view plan analytics via API.”

**Reproduction:**
```bash
pip install -e .
AUDIT=/tmp/pd-audit-api
one-pdf-pilot --pdf-path tests/golden/one_pdf_pilot/fixture_synthetic.pdf \
  --plan-id SYN-PLAN --plan-period FY2024 --effective-date 2024-06-30 \
  --ingestion-date 2026-01-01 --output-root "$AUDIT/out" --run-id api-probe
python3 - <<'PY'
import json
from pathlib import Path
from fastapi.testclient import TestClient
from pension_data.api.app import create_app
from pension_data.api.auth import SCOPE_QUERY, APIKeyStore
store = APIKeyStore()
secret, _ = store.create_key(scopes=(SCOPE_QUERY,), label="probe")
client = TestClient(create_app(key_store=store))
h = {"Authorization": f"Bearer {secret}"}
syn_rows = client.get("/api/metric-history/SYN-PLAN", headers=h).json()["rows"]
ca_rows = client.get("/api/metric-history/CA-PERS", headers=h).json()["rows"]
print("SYN-PLAN rows", len(syn_rows), "CA-PERS normalized", ca_rows[0]["normalized_value"] if ca_rows else None)
PY
```
Expected after wiring: metric-history for `SYN-PLAN` includes pilot funded ratio (~`0.784`). Observed on tip `33a29aa`: `SYN-PLAN rows 0`, `CA-PERS normalized 0.81` (fixture).

## Tasks
- [ ] Add an artifact- or DB-backed query data loader (env-configured root, e.g. `PENSION_DATA_QUERY_ARTIFACT_ROOT`) that reads pilot `staging_core_metrics.json` / staged facts and maps them to `FundingTrendInput` and `MetricHistoryRow` (`src/pension_data/query/saved_views/models.py`, `src/pension_data/query/metric_history_service.py:123-130`).
- [ ] Replace `_fixture_funding_trend_inputs()` / `_fixture_metric_history_rows()` usage in `src/pension_data/api/app.py:71` and `:95` with the loader; keep fixtures only under an explicit demo mode (e.g. `PENSION_DATA_DATA_ZONE=fixture`).
- [ ] Extend `tests/api/test_app_serving.py` with a test that points the app at a tmp pilot output directory and asserts `/api/metric-history/SYN-PLAN` returns the pilot funded ratio, not `0.81`.

## Acceptance Criteria
- Named test: `tests/api/test_app_serving.py::test_metric_history_serves_pilot_staging_not_hardcoded_fixture` asserting entity-filtered rows from a tmp pilot artifact root.
- Deliberate-break → revert: restore unconditional `_fixture_metric_history_rows()` in `src/pension_data/api/app.py:95` → confirm the named test FAILS → revert.

## Non-Goals
- Do NOT implement LangChain `/api/nl/query` or findings routes in this issue.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by repo-audit Track D 2026-09-23; verified on clone tip `33a29aa` with live `one-pdf-pilot` + TestClient reproduction._
