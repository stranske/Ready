Scorecard: 4 work / 0 partial / 1 broken / 0 fabricated / 2 not exercised of 7; journey: stops at "Scan belt promotion queue"; surfaces unscored 2; closed-still-broken 0.

# Workflows Track D audit — 2026-09-26 — attempt 2

Audited `stranske/Workflows` `main` at `70eda54e5b0b3dcfba8889cf1bdcd79ee26b1318` (+10 commits since `8d1cc914`; includes #3590 `agent:auto` routing fix and maint-77/78 model-registry work). Continuity: dossier, `Code/Audits/Workflows/2026-09-24-SCORECARD.md`, prior OUT artifacts, open-issue mirror (`artifacts/sweeps/D3-unblock-sweep-2026-09-25T05-evidence/Workflows.json`).

## Core-function evidence

| CF | Result | Probe |
|---|---|---|
| C1 | WORKS | `sync_manifest_compiler.py` → 242 copy / 17 removal entries; plan SHA `6b14136aade657d84c62863594d5350ebc17605ed33bd30a625aa27a84395c4d` |
| C2 | WORKS | `pytest` run-contract suites → 127 passed |
| C3 | WORKS | `node --test capability-bundle-contract.test.js` → 13 passed |
| C4 | WORKS | `pytest tests/e2e/test_metrics_dashboard.py` → 2 passed (alpha vs beta figures differ in fixture) |
| C5 | **BROKEN** | Real wrapped-client preflight (see below) |
| C6–C7 | NOT-EXERCISED | No production consumer sync or synthetic Gate PR |

**C5 reproduction (tip `70eda54`, matches open #3525):** After `createRateLimitedGithub({ github: octokit-shaped mock })`, `checkRateLimitStatus(wrapped, { threshold: 0, reserveFraction: 0.15, estimatedCost: 200 })` throws:

`'get' on proxy: property '__getTokenSource' is a read-only and non-configurable data property on the proxy target but the proxy did not return its actual value`

Cause unchanged: proxy `get` trap at `.github/scripts/github-rate-limited-wrapper.js` lines 191–196 binds function properties from `target` instead of returning the non-configurable `__getTokenSource` defined on the wrapper at lines 215–220; `checkRateLimitStatus` reads it at `.github/scripts/github-api-with-retry.js` lines 1016–1018. Evidence: `artifacts/audits/Workflows-2026-09-26-assets/evidence/c5-belt-proxy-repro-output.txt`. Focused `github-rate-limited-wrapper.test.js` (19 passed) still does not cover this path.

**Varying-input checks:** C1 entry count moved 241→242 with manifest growth (hash changes). C2/C3 binary pass/fail matrices unchanged. C4 dashboard test asserts distinct repo metrics.

**Recent-tip interior exercise:** Offline `python3 tools/check_model_registry_freshness.py --json` → `ok: true`, advisory review-overdue only (maint-77 gate path). Focused tests on changed tip files: 232 passed (`test_runner_lib`, sync template validation, model-eval workflow tests, autofix routing).

## Issues filed

**0** — `gh` not authenticated (`GH_TOKEN` unset; `gh auth login` required). **#3525** remains the verified, non-duplicate C5 defect on this tip; filing blocked, not waived.

**#3519 / #3590:** `resolveAgentRoutingFromLabels(['agent:auto','agent:claude'])` now returns `{ mode: 'auto', agentKey: 'claude' }` on tip (prior rejection fixed). Issue close state not confirmed without API auth; no REFUTED line emitted.

## Dimensions 2–8 (concise)

No additional verified, non-duplicate defect beyond C5. Duplication/wiring spot-check on `scripts/runner_lib/core.py`, `sync_templates.sh`, and `validate_template_sync.py` covered by new tests (all green). LangSmith host export pause, partial backplane adoption, and PDF-extract scaffold remain documented gaps with existing tracking—not re-filed.

## Reconciliation

Scorecard headline unchanged from 2026-09-24/25 rounds except tip SHA and C1 plan hash. Next verification: merge fix for #3525 with a regression that wraps a real client through `createRateLimitedGithub`, then an Agents 70 run whose Execute job reaches **Scan belt promotion queue**.
