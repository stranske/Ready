Scorecard: 5 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 1; closed-still-broken 0.

Issues filed: 0. The one candidate from attempt 1 (IMI-5 production scoring) was re-verified on attempt 2 and **withdrawn**: its fix would put fabricated scores back into production. The underlying methodology question is parked for the owner (see below).

REFUTED: https://github.com/stranske/Inv-Man-Intake/issues/693 — `tests/scoring/test_weights_config.py` launch-class tests pass on tip; `compute_score` loads all eight TOML registries via `weights_for_registry()` (`src/inv_man_intake/scoring/engine.py:60-73`).

## Run report — Track D refill — 2026-09-23 (attempt 2)

**Repo:** stranske/Inv-Man-Intake
**Tip:** `62811ac84ffdff26aaa6dc6723f6528eb244bb95` (unchanged between attempts; confirmed via `gh api repos/stranske/Inv-Man-Intake/commits/main`)
**Unit:** D-audit-Inv-Man-Intake--2026-09-23T09-11-17Z
**Executor:** attempt 1 cursor/composer (artifact rejected at 357 words, and filing blocked by an invalid `GH_TOKEN`); attempt 2 Claude (gh keyring auth valid).

### Phases 0–1.5 (carried from attempt 1; still valid on the same tip)

- About 16.9k LOC of Python under `src/`; 1010 tests collected; CLI entry point `inv-man-ingest`.
- Refill trigger: 2 open agent-formatted issues (#950, #948) against a last filed set of 8 (`artifacts/audit-refill.md`).
- Core functions IMI-1 to IMI-7 were exercised through live `inv-man-ingest`, `run_pipeline` and targeted tests. The primary journey (bundle, then extraction, thresholds, performance, queue and export) passes.
- **IMI-5 PARTIAL:** a production run whose performance is available and whose metrics are non-null still emits `final_score: null`.
- **IMI-6 PARTIAL:** queue filtering and sorting work on constructed rows, but the CLI does not persist to a queue database. This gap is already documented in `docs/PRODUCT_CONTRACT.md`.
- The static operator SPA (`app/index.html`) is unscored because it is interior to the contract; the CLI and API it relies on were driven instead, per the 2026-09-20 owner rule.
- Canonical scorecard: `Code/Audits/Inv-Man-Intake/2026-09-23-SCORECARD.md`.

### Attempt-2 adversarial re-verification of the IMI-5 candidate

The symptom is real. `src/inv_man_intake/v1_smoke.py:399-406` sets `score = None` and only the `if smoke_mode:` block (`:407-426`) calls `compute_score`. But opening the surrounding code refutes the candidate's proposed fix:

1. The block carries an explicit comment: *reference component values … are smoke-only; production scoring remains unavailable until evidence-backed inputs exist.* This is a deliberate gate. It came out of the fixture/production separation in #942 and PR #966, which removed every fixture-derived value from the production path.
2. `_score_components` (`src/inv_man_intake/v1_smoke.py:840-849`) hardcodes four of five components: performance_consistency 0.80, risk_adjusted_returns 0.78, operational_quality 0.69 and transparency 0.74. Only team_experience is derived, and oddly from benchmark correlation. The candidate's Task 1 said to "reuse `_score_components`" in production, which would publish a mostly constant score as if it were evidence-backed. That is a fabrication regression, and the candidate's Non-Goals did not forbid it.
3. `compute_score` rejects any missing component (`src/inv_man_intake/scoring/engine.py:138-144`), and every weight TOML (for example `config/scoring_weights/credit_long_short.toml`) weights all five. No production extractor exists for operational_quality, team_experience or transparency.

So the real work is not a wiring fix. It needs a scoring-methodology decision first: how to map Sharpe, volatility, drawdown and track-record completeness onto 0..1 components, and whether components with no evidence are extracted, or dropped with the weights renormalized. An agent handed this issue would have to invent that methodology, so it is not agent-ready.

**Parked for owner** (`q-D-audit-Inv-Man-Intake--2026-09-23T09-11-17Z`). Default followed: file no implementation issue. IMI-5 stays PARTIAL as a documented gap. The candidate body is kept, headed with a withdrawal note: `Code/Audits/Inv-Man-Intake/2026-09-23-issue-bodies/01-production-scoring-when-performance-available.md`. Once the owner answers, a correct issue can be written from the parked answer, and it must forbid constant components.

### Phases 2–3 (dimensions)

| Area | Result |
|---|---|
| D1 correctness | No new BLOCKER; engine and red-flag paths are covered by tests |
| D2 duplication | No new consolidation finding |
| D3 wiring | Production metrics exist without a score, but this is a deliberate gate (see above), not dead wiring |
| D4 UX | Static app not driven; CLI and API exercised |
| D5–D8 | No new filable finding this round |

Closed issues #966 and #943 (production performance and TOML finiteness) hold on tip and were not re-filed.

### Delivery

| Item | Status |
|---|---|
| OUT artifact | this file |
| AUDIT_LEDGER | appended (attempt-2 correction) |
| Issues filed / format guard | none; nothing to guard |
| Intake log | no URL to append |
| Owner question | parked with the default recorded |

**Lesson:** a verified symptom is not a verified fix. Open the code the Tasks tell the agent to reuse before filing.
