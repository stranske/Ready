Scorecard: 4 work / 0 partial / 1 broken / 0 fabricated / 2 not exercised of 7; journey: stops at "Scan belt promotion queue"; surfaces unscored 2; closed-still-broken 0.

# Workflows audit — Track D refill — 2026-09-24

Audited `stranske/Workflows` `main` at `37a83f28367428cabd2820fc3d0331d62cc9d26c` (+3 commits since the morning scorecard at `864b6e30`: #3529 consumer schema co-delivery, #3526 backplane evidence closure, #3391 belt ledger completion evidence).

**Refill trigger:** canonical `Code/Audits/Workflows/2026-09-23-SCORECARD.md` omitted the load-bearing `Scorecard:` headline (`newest_scorecard` could not parse). Backfilled on that file; full re-score recorded in `Code/Audits/Workflows/2026-09-24-SCORECARD.md`.

## Scorecard summary

| CF | Result | Note |
|---|---|---|
| C1 sync compile | WORKS | 240 copies / 17 removals |
| C2 run-contract self-smoke | WORKS | six fixture modes pass |
| C3 capability bundle | WORKS | matching vs non-matching repo selection differs |
| C4 metrics dashboard | WORKS | `tests/e2e/test_metrics_dashboard.py` |
| C5 belt scan preflight | **BROKEN** | Proxy invariant on `__getTokenSource` still reproduces with real Octokit-shaped client (`createRateLimitedGithub`) — same failure mode as #3525 |
| C6 consumer sync delivery | NOT-EXERCISED | no production consumer mutation |
| C7 Gate on consumer PR | NOT-EXERCISED | no synthetic PR event |

## Issues filed

**0** — GitHub API returns HTTP 401 (`gh` unauthenticated in this executor). Open **#3525** already tracks the verified C5 defect; no duplicate filed.

## Dimension notes (abbreviated)

- **Wiring:** backplane registry validator warns stale reference-run only; 44 focused backplane/belt tests pass on tip.
- **New surfaces:** `scripts/belt_ledger_completion.py` and `scripts/audit_belt_ledger_completion.py` (interior to C5); unscored count 2.
- **Product contract:** no `docs/PRODUCT_CONTRACT.md`; adoption issue body not filed (auth blocked). Draft may live under `Code/Audits/Workflows/2026-09-24-issue-bodies/` when auth returns.

## Evidence paths

- `work/workflows-audit-2026-09-24/evidence/` (sync, self-smoke, capability, belt proxy repro, pytest)
- Canonical scorecard: `[LOCAL_HOME]/Library/CloudStorage/Dropbox/Learning/Code/Audits/Workflows/2026-09-24-SCORECARD.md`
