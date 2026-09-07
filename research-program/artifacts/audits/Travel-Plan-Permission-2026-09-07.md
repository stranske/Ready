# Travel-Plan-Permission Refill Audit Report (2026-09-07)

**Unit ID:** `D-audit-Travel-Plan-Permission--2026-09-07T04-47-30Z`  
**Repository:** `stranske/Travel-Plan-Permission`  
**Tip SHA:** `37f7ed8afbfb4d6e16ffc613c9856421605ad359`  
**Trigger:** Open agent-ready supply 2/9 (≤25% threshold)  
**Filed Issues:** 3 verified P1 issues (#1557–#1559)

---

## Executive Summary

Demand-driven refill audit on tip `37f7ed8` (includes merged #1556 audit-metadata fix and closure of most 2026-09-06 wave issues). Prior-wave defects in policy NaN handling, PDF escaping, snapshot confinement, expense auth, and European date parsing are **fixed on main**; only #1547 (workbook_ooxml NaN guard) remains open from the prior set.

This run focused on **exception workflow** and **manager review resubmit** gaps introduced or left exposed by recent exception-authority work. Three adversarially verified findings were filed as AGENT_ISSUE_FORMAT issues; local `issue_format.py` passed all three (advisories only).

---

## Orientation

| Metric | Value |
|---|---|
| Python LOC (src/tests/scripts) | ~61,410 |
| Tests collected | 1,106 (5 baseline collection errors on Dropbox — CI is ground truth) |
| Open issues pre-audit | 6 (#1547 + housekeeping/docs) |
| Prior refill issues merged since 2026-09-06 | #1539, #1540, #1542, #1543, #1544, #1545, #1546, #1556 (+ others) |

---

## Filed Issues

1. **#1557** `[P1] Exception decisions are not terminal — repeat approve/reject overwrites finalized status`
   - Evidence: `src/travel_plan_permission/models.py:252-277`, `src/travel_plan_permission/http_service.py:885-905`, `2205`
   - Labels: `bug`, `risk:major`, `priority:high`, `type:workflow`

2. **#1558** `[P1] Wire 48-hour exception escalation before authorization and decisions`
   - Evidence: `docs/exception-policy.md:66-68`, `src/travel_plan_permission/models.py:279-293` (no `src/` callers)
   - Labels: `bug`, `risk:major`, `priority:high`, `type:workflow`

3. **#1559** `[P1] Manager review resubmit keeps stale trip plan from first submission`
   - Evidence: `src/travel_plan_permission/review_workflow.py:196-200`, `src/travel_plan_permission/http_service.py:746`, `2025`
   - Labels: `bug`, `risk:major`, `priority:high`, `type:workflow`

---

## Non-Filed / Deferred

| Finding | Disposition |
|---|---|
| #1547 workbook_ooxml NaN guard | Already open; not duplicated |
| Exception filing without draft-scope check | Downgraded — same CREATE-scoped pattern as other portal routes; weaker than terminal/SLA defects |
| Prior-wave items (#1523–#1546) | Verified fixed or closed on tip |

---

## Artifacts

- `Code/Audits/Travel-Plan-Permission/2026-09-07-issue-bodies/` (01..03)
- `Code/Audits/Travel-Plan-Permission/2026-09-07-audit-run.md`
- `Code/Audits/Travel-Plan-Permission/2026-09-07-verification-log.md`
- Checkpoint: `artifacts/audits/D-audit-Travel-Plan-Permission--2026-09-07T04-47-30Z.CHECKPOINT.md`

---

## Confidence

**High** on all three filed issues — each reproduced on live tip or confirmed by docs/code parity (`rg` zero `src/` callers for escalation). **Medium** that resubmit refresh is the only stale-state path; other `create_or_get` callers may need the same guard.

**Would change my mind:** If product intent is explicitly single-shot manager reviews (no resubmit), issue #1559 should be closed as non-actionable — but `request_changes` flow and docs imply resubmit is supported.
