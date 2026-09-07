# Trip-planner Track D audit — 2026-09-07

**Unit:** `D-audit-trip-planner--2026-09-07T04-47-34Z`  
**Repo:** [stranske/trip-planner](https://github.com/stranske/trip-planner)  
**Tip:** `8077785611d5c96a533eb4f0bc42877718ea66d1`  
**Trigger:** 2 open agent-ready issues ≤ recorded threshold 2 (last set 4). The engine refill table establishes this trigger; 2/4 is 50%, so the earlier ≤25% wording was incorrect.

## Summary

Refill audit on current `main` after the September wave (#1778–#1781) landed. Prior fail-open fixes are real but incomplete on the **live TPP HTTP path** and **public workspace** surfaces. Prior executor filed **8 issues, reverified in attempt 3** (#1798–#1805): 7×P1 policy/TPP/ranking wiring, 1×P2 compare-preview token mismatch.

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
4. **Frontend wiring, static only** — compliant headline vs disabled export (#1803); submission context gap (#1802). No observed UX review or score established.  
5–7. **Field/opportunities/tools** — deferred (source adapters remain roadmap issues #1783–#1787)  
8. **Automations** — format guard exercised on all filings

## Next ledger action

Verify squash delivery of #1798–#1805; prioritize #1799/#1800/#1802 (live TPP + public workspace seams).


## Attempt 3 reconciliation — 2026-09-07T08:16:10.742185+00:00

Resumed retained Phase 5; no restart, repository source edits, new issues, label changes, dispatches, or duplicate intake entries. Required dossier exists and was read fully, along with owner notes and prior checkpoints. The audit unit is complete as a focused refill and reconciliation; implementation of the eight defects remains open.

### Current remote evidence

Clone and remote main both `8077785611d5c96a533eb4f0bc42877718ea66d1`. [Current-head CI](https://github.com/stranske/trip-planner/actions/runs/34049370795) and [Cross-Repo Smoke](https://github.com/stranske/trip-planner/actions/runs/34049370450) succeeded. No open PRs returned by live query.

| Issue | Current state | Remote issue-format run |
|---|---|---|
| [#1798](https://github.com/stranske/trip-planner/issues/1798) | open | [success](https://github.com/stranske/trip-planner/actions/runs/34094896263) |
| [#1799](https://github.com/stranske/trip-planner/issues/1799) | open | [success](https://github.com/stranske/trip-planner/actions/runs/34094896498) |
| [#1800](https://github.com/stranske/trip-planner/issues/1800) | open | [success](https://github.com/stranske/trip-planner/actions/runs/34094898561) |
| [#1801](https://github.com/stranske/trip-planner/issues/1801) | open | [success](https://github.com/stranske/trip-planner/actions/runs/34094900509) |
| [#1802](https://github.com/stranske/trip-planner/issues/1802) | open | [success](https://github.com/stranske/trip-planner/actions/runs/34094900839) |
| [#1803](https://github.com/stranske/trip-planner/issues/1803) | open | [success](https://github.com/stranske/trip-planner/actions/runs/34094902912) |
| [#1804](https://github.com/stranske/trip-planner/issues/1804) | open | [success](https://github.com/stranske/trip-planner/actions/runs/34094903992) |
| [#1805](https://github.com/stranske/trip-planner/issues/1805) | open | [success](https://github.com/stranske/trip-planner/actions/runs/34094906379) |

Exact live issue bodies passed the repository's actual format validator **8/8**, each with the advisory that Implementation Notes is absent. The prior verification log's queued-guard statement is superseded by these successful runs. Intake rows 139–146 contain all eight URLs exactly once; no rows were appended.

### Evidence and limits

- Reopened all explicit file-and-line citations in the current issue bodies; source patterns remain at the audited tip. Evidence snapshots and exact bodies: [trip-planner-2026-09-07-evidence](/Users/teacher/.codex/automations/research-program/artifacts/audits/trip-planner-2026-09-07-evidence).
- **#1798 reproduced at function level:** explicit pass plus one blocking issue returns compliant with no failure reasons. Freshness was patched to fresh to isolate this branch; this is not a full persisted-reload test.
- **#1800 reproduced through real TPP contract normalization:** injected budget rule `max_trip_total_usd=100` disappears from the serialized imported constraint set.
- **#1801 reproduced through real scenario preview:** configured lodging cap plus absent nightly breakdown returns compliant and an empty violation list.
- **#1805 reproduced at preview function level:** underscore token returns compliant; hyphen token produces POL-EXC. Saved-scenario end-to-end behavior was not exercised.
- **#1799 static confirmation:** HTTP adapter still constructs empty airfare/lodging/ground/meal maps and comparable requirements. No real TPP server was queried; an implementation must confirm the upstream schema supports the proposed rule payloads rather than merely pass a fabricated client fixture.
- **#1802/#1803 static confirmation:** public workspace strips identifiers/verdict diagnostics while frontend reads debug context or the stripped verdict. This establishes a wiring contradiction, not observed browser usability or an end-to-end submission/export result.
- **#1804 static confirmation:** comparable objectives still take category counts only from profile constraints; imported organization counts are not consumed by that derivation. Ranking outcome sensitivity was not executed this attempt.
- Historical 1,278-test collection and six collection errors were not reproduced; no raw evidence establishes their cause. They are not treated as verified baseline failures. No full test suite or browser panel ran this attempt.

### Coverage reconciliation and next work

D1/D3 received focused defect verification. D2 was deferred by the original executor after the parser work; no fresh duplication sweep is established. D4 remains unobserved (no screenshots/panel evidence retained for this wave). D5–D7 remain deferred roadmap work under prior source-adapter issues, not a completed field/tool comparison. D8 establishes format-guard operation only, not a fleet automation audit. Completion of this queue unit does not certify a comprehensive eight-dimension audit.

Prior candidate dispositions are retained: hidden approval requirements overlap #1803 (deferred), raw map status and next-step CTA polish are deferred pending observation; legacy build-script dependency claim remains unverified and was not refiled. Follow-up should implement and verify #1799/#1800/#1802 first, and include real upstream TPP contract evidence and default non-debug browser journeys. Existing triage-only issue labels remain unchanged.
