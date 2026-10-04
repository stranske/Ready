Scorecard: 5 work / 0 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes; surfaces unscored 2; closed-still-broken 0.

# Workflows Track D audit — 2026-09-27 — attempt 3

Audited `stranske/Workflows` `main` at `a8f1e458014b1a296702ccfe1fd5b7093289e5b8` (unchanged since attempt 1; +3 commits since `70eda54`: #3587 belt proxy fix for #3525, #3591/#3593 keepalive sync-review authority). Continuity: dossier, `Code/Audits/Workflows/2026-09-27-SCORECARD.md`, prior OUT through 2026-09-26, open-issue mirror (`artifacts/sweeps/D3-unblock-sweep-2026-09-25T05-evidence/Workflows.json`).

REFUTED: https://github.com/stranske/Workflows/issues/3525 — PR #3587 (`readProxyProperty` in `.github/scripts/github-rate-limited-wrapper.js`) on tip `a8f1e45`; issue reproduction (`createRateLimitedGithub` then `checkRateLimitStatus` with belt-scan thresholds) completes with `safe: true` and no `__getTokenSource` Proxy invariant throw.

## Core-function evidence (attempt 3 re-run)

| CF | Result | Probe |
|---|---|---|
| C1 | WORKS | `sync_manifest_compiler.py` → 242 copy / 17 removal entries; compile SHA `sha256:5d9b592dfcfa035f38a1005f44c5155c2b5b9ab671074864a82140e35899016b` |
| C2 | WORKS | `pytest tests/scripts/test_validate_run_contract.py tests/contracts/test_validate_run_contract.py` → 127 passed |
| C3 | WORKS | `node --test capability-bundle-contract.test.js` → 13 passed |
| C4 | WORKS | `pytest tests/e2e/test_metrics_dashboard.py` → 2 passed |
| C5 | WORKS | `node --test github-api-with-retry.test.js github-rate-limited-wrapper.test.js` → 49 passed (includes wrapped-client preflight test) |
| C6–C7 | NOT-EXERCISED | No production consumer sync or synthetic Gate PR |

**C5:** Regression test `checkRateLimitStatus works on createRateLimitedGithub wrapped client` passes on tip. Prior standalone repro output: `artifacts/audits/Workflows-2026-09-27-assets/evidence/c5-belt-proxy-repro-output.txt`.

**Varying-input checks:** C1 copy count stable at 242; C4 alpha vs beta metrics still diverge in e2e fixtures.

**Tip interior:** `pytest tests/workflows/test_keepalive_authority_delivery.py tests/scripts/test_runner_lib.py` → 193 passed; `node --test .github/scripts/__tests__/*.test.js` from repo root → 1698 passed; `validate_template_sync.py` → all templates in sync.

## Issues filed

**0** — no verified, non-duplicate defect beyond continuity gaps already tracked. `gh` still unauthenticated (`GH_TOKEN` unset; `gh auth login` required). Format-guard run list not checked this attempt.

## Dimensions 2–8 (concise)

No additional adversarially verified, non-duplicate finding. LangSmith host export pause, partial backplane adoption, PDF-extract scaffold, and C6/C7 coverage gaps remain documented with existing tracking—not re-filed.

## Reconciliation

Scorecard unchanged from attempt 1 on the same tip. #3525 claim refuted on live preflight stack; do not re-file. Next verification: scheduled Agents 70 Execute reaching belt scan in Actions (not observed here).
