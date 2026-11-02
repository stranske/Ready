Scorecard: 5 work / 1 partial / 0 broken / 0 fabricated / 2 not exercised of 8; journey: stops at "exception request and escalation"; surfaces unscored 12; closed-still-broken 0.

# Audit — stranske/Travel-Plan-Permission — 2026-11-02

Audited tip: `04c1098ce0b2b30ce022d90d351dfd8d17f88105` (`main`). Scope was first-party application/CLI/HTTP/portal behavior; synced automation implementation is excluded under `AGENTS.md`. No issues filed.

## Product scorecard

| Core function | Result | Live evidence |
| --- | --- | --- |
| PP1 — planner policy evaluation | WORK | A live compliant plan ($1,190.50) returned `policy_status=pass`; an otherwise identical $9,999.00 plan returned `policy_status=fail` with `BUD-001`, through `GET /api/planner/policy-snapshot` and `POST /api/planner/proposals`. The repo-native smoke then completed snapshot → submission → status → evaluation. |
| PP2 — traveller draft/review/submit | WORK | `POST /portal/draft` returned 303, the authenticated review returned 200, and submit returned 200 with a queued manager-review page. |
| PP3 — exception request and decision | NOT-EXERCISED | No live failing portal draft was carried through exception creation and attributed decision in this bounded pass. |
| PP4 — overdue exception escalation | NOT-EXERCISED | No user-visible route can age a pending request by 48 hours; the prior status was not reused as live proof. |
| PP5 — manager decision | WORK | The authenticated manager queue and review detail returned 200; `request_changes` returned 303 and the detail retained `changes_requested`. |
| PP6 — correction after changes requested | PARTIAL | A corrected `POST /portal/draft` produced a distinct ID while the original review stayed `changes_requested`. This matches the explicitly documented limitation: no existing-draft edit/resubmit route. |
| PP7 — policy-gated artifacts | WORK | The compliant review returned summary PDF (200, 1,742 bytes) and itinerary XLSX (200, 1,288,801 bytes). A minimal incomplete draft returned 403 for its artifact, showing the gate responds to state. |
| PP8 — policy snapshot | WORK | The PP1 input variation changed the snapshot from pass to fail and added `BUD-001`. |

The live service was started with isolated SQLite state and bootstrap credentials. `/readyz` reported ready. The local selected `.venv` has the runtime dependencies but no `pytest`; no local test-suite outcome is claimed. GitHub CI run `41524763565` on this exact tip succeeded.

## Surface and journey coverage

The live OpenAPI inventory exposes 29 routes. The product contract defines eight core functions in `docs/PRODUCT_CONTRACT.md:10-19`; the 12 ancillary/unmapped surfaces reported by the refill trigger remain unscored, so this audit does not claim the coverage debt fell. The primary journey completed draft, submission, manager request-for-changes, correction-as-new-draft, and artifact delivery; it stopped before the exception branch.

## Findings and disposition

No independently reproducible, agent-ready defect survived review of the current tip, the six open issues, and applicable recently closed issues. The highest-risk historical classes (policy validation, snapshot caps, artifact authorization, manager decision state, and cross-repo receipt state) have current code/contract coverage and were not re-filed without a new reproduction.

REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1559 — its old same-draft edit/resubmit reproduction cannot reproduce because the current product explicitly creates a new draft and preserves the original review state.

The legacy module-size concern is already guarded, not a new filing: `tests/python/test_policy_api.py:47-52` sets current ceilings for `http_service.py` and `policy_api.py`; CI invokes that exact test in `.github/workflows/ci.yml:40-47`. Its existence does not prove the modules are ideal, but it defeats a claim that their growth is unguarded.

## Dedup and delivery

Open issues were checked before disposition, including #1658 and #1669; neither describes a newly reproduced result from this audit. Closed #1559 was re-evaluated as above. No issue bodies were created, no labels were changed, and there is no format-guard run to report.

## Confidence and limits

Confidence is high for PP1, PP2, PP5, PP6, PP7, and PP8 because each was driven through the real HTTP service on the audited tip with isolated state; medium for the no-new-issue conclusion because PP3 and PP4 were deliberately left unscored rather than simulated by mutating private state. A fresh issue would be warranted if a live exception can be created from a failing portal draft and either its decision attribution or 48-hour escalation fails.
