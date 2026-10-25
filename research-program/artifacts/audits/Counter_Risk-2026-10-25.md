Scorecard: 4 work / 2 partial / 0 broken / 0 fabricated / 1 not exercised of 7; journey: passes; surfaces unscored 1; closed-still-broken 1.

**Issues filed:** 1 — [#1188](https://github.com/stranske/Counter_Risk/issues/1188) (dimension audit files still lack historical superseded banner; #1182 acceptance test never landed).

REFUTED: https://github.com/stranske/Counter_Risk/issues/1182 — closed 2026-10-24 but `test_dimension_audit_logs_marked_historical` is absent and eleven `docs/audit/*.md` dimension files still lack the banner.

## Run report (2026-10-25)

**Tip:** `affd8bf1c1adeca336c23662abf503304f9ef1c7` on branch `fix/black-langsmith-fleet-test` (black-format fleet test; ledger notes `main` at `15830ec`). **Host:** macOS, Python 3.12 (`/opt/anaconda3`). **Scope:** app code per dossier; excluded `.github/` (Workflows sync) and dev boilerplate.

### Scorecard vs prior round (2026-10-24)

| Metric | 2026-10-24 | 2026-10-25 | Notes |
|---|---|---|---|
| Work / partial / NE | 4 / 1 / 2 | 4 / 2 / 1 | CF6 scored **PARTIAL** via `tests/test_runner_workbook.py` (static Form Control wiring); CF7 still Windows-only |
| Surfaces unscored | 2 | 1 | Runner COM click-test replaced by artifact tests; frozen bundle remains |
| Coverage debt (NE+unscored) | 4 | 2 | Reduced per unit trigger |
| closed-still-broken | 0 | 1 | #1182 |

### Live probes

- **CF1:** `counter_risk.cli run --fixture-replay` with `config/fixture_replay.yml` — completed; manifest and deliverables written.
- **CF3:** `pytest tests/compute/test_concentration_metrics.py -k hhi` — 5 passed.
- **CF4:** `pytest tests/pipeline/test_langsmith_fleet_data_quality_status.py` — 6 passed.
- **CF6:** `pytest tests/test_runner_workbook.py` + `tests/compute/test_limits.py` — 101 passed; seven macros wired (D5 Dry-Run, I5 Ask-about still label-only — open #1183).

### Eight dimensions (summary)

No new code-defect surfaced beyond docs continuity. Dimension files under `docs/audit/` still advertise superseded BLOCKERs without banners (#1188). Open operator gaps unchanged: #1183 (Runner labels), #1186 (CI Python matrix), Windows frozen verification (CF7).

### Dedup / refutation

- **#1182:** Re-ran issue acceptance (`pytest …::test_dimension_audit_logs_marked_historical`) — test missing; dimension headers verified — **closed-still-broken** → #1188 filed.
- **#1183, #1186:** Already open; not re-filed.

### Artifacts

- Canonical scorecard: `Code/Audits/Counter_Risk/2026-10-25-SCORECARD.md`
- Checkpoint: `artifacts/audits/D-audit-Counter_Risk--2026-10-25T08-11-10Z.CHECKPOINT.md`
- Format guard: Agents Issue Format Guard run `40175737436` — success.
