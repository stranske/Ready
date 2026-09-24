Scorecard: 4 work / 0 partial / 1 broken / 0 fabricated / 2 not exercised of 7; journey: stops at "Scan belt promotion queue"; surfaces unscored 2; closed-still-broken 0.

# Workflows Track D audit — 2026-09-24

Audited `stranske/Workflows` at current remote `main` tip `887d5908495907fee45c144085fec5d56fe39e82` (release 1.36.0). The previous 2026-09-24 scorecard was read as continuity, along with the dossier, ledger, and the open issue set supplied by the unit. This was a demand-driven recheck of the remaining broken core function, not a source-code change.

## Core-function evidence

- C1 consumer manifest compilation works: `python3 scripts/sync_manifest_compiler.py --manifest .github/sync-manifest.yml --output-json /tmp/workflows-sync-plan.json` compiled 241 copy entries and 17 removals with SHA-256 `2d278c5fd04b3d91d683cf61e4985ad1e876bf349d79695a7c90f5d2302f192c`.
- C2 run-contract validation works: `pytest -q tests/contracts/test_validate_run_contract.py tests/scripts/test_validate_run_contract.py` passed 127 tests, including conforming and rejecting fixture paths.
- C3 capability selection/prompt composition works: `node --test .github/scripts/__tests__/capability-bundle-contract.test.js` passed 13 tests, including matching-bundle application and nonmatching-bundle rejection.
- C4 metrics-dashboard behavior works: `pytest -q tests/e2e/test_metrics_dashboard.py` passed 2 tests; its fixture assertions continue to distinguish the alpha and beta dashboard values.
- C5 remains broken. A fresh real-wrapper probe constructed an Octokit-shaped client, called `createRateLimitedGithub`, then called `checkRateLimitStatus`. It failed with `TypeError: 'get' on proxy: property '__getTokenSource' is a read-only and non-configurable data property on the proxy target but the proxy did not return its actual value`. The cause is still visible in `.github/scripts/github-rate-limited-wrapper.js:191-196`, which binds function properties, while `:215-220` defines `__getTokenSource` as non-configurable and non-writable. `checkRateLimitStatus` reads that metadata at `.github/scripts/github-api-with-retry.js:1016-1018`.

The focused wrapper/API suite passed 43 tests, but it does not cover the actual Proxy path: its existing already-wrapped test defines properties directly on a plain object. The open, deduplicated issue [#3525](https://github.com/stranske/Workflows/issues/3525) describes precisely this missing regression and remains open; no duplicate issue was filed.

The newest `Agents 70 Orchestrator` runs (for example [35991190430](https://github.com/stranske/Workflows/actions/runs/35991190430)) succeeded only through eligibility; both Initialize and Execute were skipped. Those runs are not a live C5 success and do not refute the local current-tip reproduction. C6 consumer delivery and C7 synthetic Gate events remain intentionally unexercised because executing them would mutate production consumers.

## Reconciliation

No new reproducible, non-duplicate finding survived this round. No repository code was changed, no issue was filed, and the source clone remained clean. The next meaningful verification is a repair for #3525 with the required actual wrapped-client regression, followed by a scheduled Agents 70 run that reaches Execute / Scan belt promotion queue.
