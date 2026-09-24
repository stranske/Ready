Scorecard: 4 work / 0 partial / 1 broken / 0 fabricated / 2 not exercised of 7; journey: stops at "Scan belt promotion queue"; surfaces unscored 2; closed-still-broken 0.

# Workflows audit — Track D refill — attempt 3 — 2026-09-24

Audited `stranske/Workflows` `main` at `fccf1c6aa3510fa75fbe7efe1a8f4a3a4538b722` (unchanged since attempt 2; no new commits on tip).

**Refill trigger:** fleet `newest_scorecard` on canonical `Code/Audits/Workflows/2026-09-23-SCORECARD.md` now parses (`Scorecard:` headline backfilled on attempt 1). Re-queue from stale queue state / auth-blocked filing rounds, not a missing headline on tip.

## Scorecard summary

| CF | Result | Note |
|---|---|---|
| C1 sync compile | WORKS | 240 copies / 17 removals (`sha256:5e5eb0d1…`) |
| C2 run-contract self-smoke | WORKS | six invalid fixtures reject; valid conform |
| C3 capability bundle | WORKS | `capability-bundle-contract.test.js` green |
| C4 metrics dashboard | WORKS | `tests/e2e/test_metrics_dashboard.py` (2 passed) |
| C5 belt scan preflight | **BROKEN** | `ensureRateLimitWrapped` + `checkRateLimitStatus` (belt-scan stack) throws Proxy invariant on `__getTokenSource` — same text as #3525 |
| C6 consumer sync delivery | NOT-EXERCISED | no production consumer mutation |
| C7 Gate on consumer PR | NOT-EXERCISED | no synthetic PR event |

## Issues filed

**0** — `gh` not authenticated (`GH_TOKEN` unset; `gh auth login` required). Open **#3525** remains the verified C5 defect; re-ran belt-scan-shaped reproduction on tip — defect **still reproduces** (not refuted). No duplicate filed.

## Adversarial verification

- **#3525:** Reproduction matches issue stack (`reusable-70-orchestrator-main.yml` belt-scan step uses `ensureRateLimitWrapped` then `checkRateLimitStatus`). Root cause unchanged: `.github/scripts/github-rate-limited-wrapper.js` Proxy `get` trap binds `target.__getTokenSource` instead of returning the non-configurable property defined on the wrapper (see lines 191–196 vs 215–220).
- **Dimensions 2–8:** No additional verified, non-duplicate defect beyond C5 on this tip; interior gaps (LangSmith export paused, backplane partial adoption) already tracked elsewhere.

## Evidence paths

- `artifacts/audits/Workflows-2026-09-23-assets/evidence/` (`*-attempt3.txt` plus updated `belt-proxy-repro.txt`)
- Canonical scorecard: `Code/Audits/Workflows/2026-09-24-SCORECARD.md` (attempt 3 row appended)
