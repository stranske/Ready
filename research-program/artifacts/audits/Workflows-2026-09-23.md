Scorecard: 4 work / 0 partial / 1 broken / 0 fabricated / 2 not exercised of 7; journey: stops at "Scan belt promotion queue"; surfaces unscored 2; closed-still-broken 0.

# Workflows audit — Track D refill — attempt 2 — 2026-09-24

Audited `stranske/Workflows` `main` at `fccf1c6aa3510fa75fbe7efe1a8f4a3a4538b722` (+1 commit since attempt 1 at `37a83f28`: #3530 Maint 71 GraphQL quota / token-balancer routing; does not touch the belt-scan Proxy invariant).

**Refill trigger (attempt 1):** canonical `Code/Audits/Workflows/2026-09-23-SCORECARD.md` omitted the load-bearing `Scorecard:` headline — backfilled on attempt 1; headline now parses for the fleet engine.

## Scorecard summary

| CF | Result | Note |
|---|---|---|
| C1 sync compile | WORKS | 240 copies / 17 removals (`sha256:5e5eb0d1…`) |
| C2 run-contract self-smoke | WORKS | six invalid fixtures reject; valid conform |
| C3 capability bundle | WORKS | contract tests pass |
| C4 metrics dashboard | WORKS | `tests/e2e/test_metrics_dashboard.py` (2 passed) |
| C5 belt scan preflight | **BROKEN** | `createRateLimitedGithub` + `checkRateLimitStatus` still throws Proxy invariant on `__getTokenSource` (same text as #3525) |
| C6 consumer sync delivery | NOT-EXERCISED | no production consumer mutation |
| C7 Gate on consumer PR | NOT-EXERCISED | no synthetic PR event |

## Issues filed

**0** — `gh` / `GH_TOKEN` still return HTTP 401 (keychain token invalid in this executor). Open **#3525** remains the verified C5 defect; re-ran issue-shaped reproduction on tip — defect **still reproduces** (not refuted). No duplicate filed.

## Dimension notes (abbreviated)

- **Wiring:** #3530 adds GraphQL rate-limit detection and `preferredSource` / `rateResource` token selection for Maint 71; 61 focused Node tests pass; belt preflight stack unchanged.
- **Product contract:** still no `docs/PRODUCT_CONTRACT.md`; adoption issue not filed (auth blocked).

## Evidence paths

- `artifacts/audits/Workflows-2026-09-23-assets/evidence/` (sync, self-smoke, capability, belt proxy repro, pytest, node)
- Canonical scorecard: `[LOCAL_HOME]/Library/CloudStorage/Dropbox/Learning/Code/Audits/Workflows/2026-09-24-SCORECARD.md` (attempt 2 row appended)
