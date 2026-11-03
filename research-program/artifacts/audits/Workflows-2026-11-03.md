# Scorecard — stranske/Workflows — 2026-11-03 — tip 62672b61b18b16d6301e5e671dfe43e5fd9f1d15

Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

## Run report

**Trigger:** Track D refill — coverage debt 2 (not exercised C6/C7) unchanged since 2026-10-02.

**Tip delta:** One commit since 2026-11-02 scorecard (`c4633a95` → `62672b61`, #4410 LLM tool type mypy alignment). C1–C5 probes unchanged green.

**Coverage debt cleared this round:** C6 (consumer sync plan compile) and C7 (PR gate change classifier) were scored **WORKS** via local CLI/`node --test` probes without production delivery PRs or live consumer Gate events — matching owner direction to drive the API/CLI when the full journey cannot run live.

| id | score | probe |
|---|---|---|
| C1 | WORKS | `pytest -k "manifest or sync_manifest"` — 455 passed, 1 skipped |
| C2 | WORKS | `pytest -k contract` — 1193 passed |
| C3 | WORKS | `node --test capability-bundle-contract.test.js` |
| C4 | WORKS | `pytest tests/e2e/test_metrics_dashboard.py` — 2 passed |
| C5 | WORKS | `node --test github-rate-limited-wrapper.test.js github-api-with-retry.test.js` |
| C6 | WORKS | `python scripts/sync_manifest_compiler.py --manifest .github/sync-manifest.yml` — 279 copy entries; plan hash tracks manifest (compiler + `tests/workflows/test_sync_manifest_delivery.py`) |
| C7 | WORKS | `node --test __tests__/detect-changes.test.js` — doc-only vs core outputs vary |

**Interior:** `audit_belt_ledger_completion.py --root .` exit 0 (170 unverifiable commits skipped). `validate_backplane_registry.py` exit 1 on expired deferrals (see filing).

**Dedup / refutation:** #4387 (Maint 39 github-models) remains open — not re-filed. Closed #4386 was sync-core handoff only; deferral expiry still reproduces on tip (not refuted).

**Issues filed:** #4411 — roll or replace five expired `issue_deferred.expires_at` values blocking Health 78.

**Productivity verdict:** Scored core-function coverage debt drained (2 → 0 not-exercised). New filable defect is registry/administrative but CI-blocking on backplane-touching PRs.
