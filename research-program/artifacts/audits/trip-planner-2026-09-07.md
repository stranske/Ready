# Trip-planner Track D audit — 2026-09-07

**Unit:** `D-audit-trip-planner--2026-09-07T04-47-34Z`  
**Repo:** [stranske/trip-planner](https://github.com/stranske/trip-planner)  
**Tip:** `8077785611d5c96a533eb4f0bc42877718ea66d1`  
**Trigger:** agent-ready supply ≤25% (2 open / last set 4 per `artifacts/audit-refill.md`)

## Summary

Refill audit on current `main` after the September wave (#1778–#1781) landed. Prior fail-open fixes are real but incomplete on the **live TPP HTTP path** and **public workspace** surfaces. Filed **8 verified issues** (#1798–#1805): 7×P1 policy/TPP/ranking wiring, 1×P2 compare-preview token mismatch.

Dominant class: **policy data is imported, stored, or displayed on one path and dropped or misread on the adjacent path** — the same defect family as the August paired audit, now shifted from reload defaults to live-client empty rule maps, missing `budget_rules` on the contract, and frontend submission/export reading debug-only or stripped fields.

## Filed issues

| # | Title | Severity |
|---|---|---|
| [#1798](https://github.com/stranske/trip-planner/issues/1798) | Workspace policy reload must treat pass status with blocking issues as non-compliant | P1 |
| [#1799](https://github.com/stranske/trip-planner/issues/1799) | Live TPP policy snapshot must map lodging and airfare rules into constraint_set | P1 |
| [#1800](https://github.com/stranske/trip-planner/issues/1800) | PolicyConstraintSet must persist budget_rules for scenario preview caps | P1 |
| [#1801](https://github.com/stranske/trip-planner/issues/1801) | Lodging policy preview must not mark compliant when nightly rate is unavailable | P1 |
| [#1802](https://github.com/stranske/trip-planner/issues/1802) | Proposal submission must read policy context from public workspace policy_state | P1 |
| [#1803](https://github.com/stranske/trip-planner/issues/1803) | Policy UI must not show compliant and block export when evaluation_result is stripped | P1 |
| [#1804](https://github.com/stranske/trip-planner/issues/1804) | Business ranking must honor TPP comparable_requirements from organization_context | P1 |
| [#1805](https://github.com/stranske/trip-planner/issues/1805) | Exception-nearest scenario preview must key off exception_nearest label not hyphenated note | P2 |

## Verification

- Local `.github/scripts/issue_format.py`: 8/8 pass (0 errors; advisories only).
- Remote Agents Issue Format Guard: **success** runs observed for filed issue titles at audit close (`gh run list`).
- Every task cites repo-relative paths verified on the clone tip.

## Artifacts

| path | purpose |
|---|---|
| `Code/Audits/trip-planner/2026-09-07-audit-run.md` | run record |
| `Code/Audits/trip-planner/2026-09-07-00-repo-map.md` | Phase 1 orientation |
| `Code/Audits/trip-planner/2026-09-07-verification-log.md` | finding disposition |
| `Code/Audits/trip-planner/2026-09-07-issue-bodies/` | filed bodies |
| `~/.codex/orchestrator/measurement/intake-2026-09-04.log` | intake rows appended |

## Category coverage (abbrev.)

1. **Code quality** — pass+blocking_issues evaluation gap; lodging preview fail-open  
2. **Duplication** — not a focus this round (parser unification landed in #1779)  
3. **Wiring** — live TPP empty rules; budget_rules; comparable_requirements; frontend policy context  
4. **UX** — compliant headline vs disabled export (#1803); submission blocked (#1802)  
5–7. **Field/opportunities/tools** — deferred (source adapters remain roadmap issues #1783–#1787)  
8. **Automations** — format guard exercised on all filings

## Next ledger action

Verify squash delivery of #1798–#1805; prioritize #1799/#1800/#1802 (live TPP + public workspace seams).
