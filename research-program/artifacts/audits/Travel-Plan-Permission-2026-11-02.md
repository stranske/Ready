Scorecard: 7 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 12; closed-still-broken 0.

**Issues filed:** #1720 (stale `/portal/requests/*` operator docs), #1721 (`docs/PRODUCT_CONTRACT.md` PP8 + PP4 status drift). Agents Issue Format Guard: runs `41428823591`, `41428824589` success.

## Run summary (Track D refill 2026-11-02)

Audited `stranske/Travel-Plan-Permission` at `503eae9504ce071c17513da6aa184ef22266fc1d` (31 days after prior scorecard). Phase 1.5 re-exercised PP1–PP8 via the same FastAPI/TestClient gate as 2026-10-02 (13 focused tests passed in ~4s) plus CLI `fill-spreadsheet` success test. Primary portal journey still reaches submission, exception/admin escalation, manager decision, resubmit refresh, and artifact download without fabricated constants on probed branches.

**Product verdict:** Core travel-policy and portal workflow remains healthy on the contract rows; PP6 stays partial by design (new draft after `changes_requested`, not silent in-place edit). No new core-function regression found; two operator/contract documentation drifts verified and filed.

## Dimension notes (abbreviated)

| Dim | outcome |
|---|---|
| 1 Quality | No new adversarial code defect beyond open #1669 (owner-bound execution overwrite). |
| 2 Duplication | Not expanded this round (prior rounds mined). |
| 3 Wiring/output | Policy snapshot + portal routes match config on probed paths. |
| 4 UX | Unmeasured (TestClient only); not claimed as UX pass. |
| 5–7 Field/opportunities/tools | No filable delta on tip. |
| 8 Automations | Format guard green on filed bodies. |

## Dedup / refutation

- **#1669** remains open and valid on tip (`planner_http_routes.py:146` records generic submissions without owner guard) — not re-filed.
- **#1559** closed; resubmit refresh reproduction passes (`test_manager_review_resubmit_refreshes_trip_plan`).
- No `REFUTED:` lines (no closed-issue reproduction contradicted this run).

## Artifacts

- Scorecard: `Code/Audits/Travel-Plan-Permission/2026-11-02-SCORECARD.md`
- Surface inventory: `Code/Audits/Travel-Plan-Permission/2026-11-02-surface-inventory.txt`
- Issue bodies (local): unitdir `issue-bodies/01-*.md`, `02-*.md`
- CI reference: `41277412044` (main green)

## Intake log

```
stranske/Travel-Plan-Permission|issue-bodies/01-stale-portal-requests-doc-paths.md|https://github.com/stranske/Travel-Plan-Permission/issues/1720
stranske/Travel-Plan-Permission|issue-bodies/02-product-contract-pp8-and-status-drift.md|https://github.com/stranske/Travel-Plan-Permission/issues/1721
```
