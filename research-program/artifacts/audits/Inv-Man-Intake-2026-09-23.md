Scorecard: 5 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 1; closed-still-broken 0.

Issues filed: 0 (GitHub CLI: `GH_TOKEN` rejected with HTTP 401; one verified P1 candidate body at `Code/Audits/Inv-Man-Intake/2026-09-23-issue-bodies/01-production-scoring-when-performance-available.md`).

REFUTED: https://github.com/stranske/Inv-Man-Intake/issues/693 — `tests/scoring/test_weights_config.py` launch-class tests pass on tip; `compute_score` loads all eight TOML registries via `weights_for_registry()` (`src/inv_man_intake/scoring/engine.py:60-73`).

## Run report — Track D refill — 2026-09-23

**Repo:** stranske/Inv-Man-Intake  
**Tip:** `62811ac84ffdff26aaa6dc6723f6528eb244bb95` (shallow clone)  
**Unit:** D-audit-Inv-Man-Intake--2026-09-23T09-11-17Z  

### Phase 0–1 (orient)

- ~16.9k LOC Python under `src/`; 1010 tests collected; CLI entry `inv-man-ingest`.
- Open agent-formatted issues (API): #950, #948 (+ tracker #559, #330). Refill trigger: 2 open vs last set 8 (`artifacts/audit-refill.md`).
- Prior scorecard baseline: `docs/PRODUCT_CONTRACT.md` (2026-09-20).

### Phase 1.5 (scorecard)

Core functions IMI-1–IMI-7 exercised via live `inv-man-ingest`, `run_pipeline`, and targeted tests. **IMI-5** remains **PARTIAL**: production run with `performance.status=available` and non-null metrics still yields `final_score: null` because scoring is gated inside `if smoke_mode:` only (`src/inv_man_intake/v1_smoke.py:399-426`). **IMI-6** **PARTIAL**: `validation_queue_api` filters/sorts in tests; CLI does not persist queue DB. **IMI-4** varying-input confirmed (workbook 0.12 vs 0.24 changes metrics). Static operator SPA (`app/index.html`) unscored (interior to contract).

Canonical scorecard: `Code/Audits/Inv-Man-Intake/2026-09-23-SCORECARD.md`.

### Phases 2–3 (dimensions, verification)

| Area | Result |
|---|---|
| D1 correctness | No new BLOCKER beyond documented IMI-5 gap; engine/red-flag paths covered by tests |
| D2 duplication | No new consolidation finding |
| D3 wiring | **Verified:** production performance → metrics without `compute_score` (see issue body) |
| D4 UX | Static app not driven; CLI/API exercised per owner 2026-09-20 rule |
| D5–D8 | No new filable interior finding this round |

Adversarial: #693 credit-only claim **refuted** on tip (see REFUTED line). Closed issues #966/#943 addressed performance/TOML finiteness; not re-filed.

### Phase 4–5 (file, ledger)

- **Candidate issue (not filed):** `[P1] Production inv-man-ingest skips compute_score when performance metrics exist (IMI-5)` — body on disk; filing blocked by auth.
- Ledger + audit-run updated under `Code/Audits/Inv-Man-Intake/`.
- Format guard: not run (no issue created).

### Delivery

| Item | Status |
|---|---|
| OUT artifact | this file |
| AUDIT_LEDGER | appended |
| intake log | skipped (no filed URL) |
