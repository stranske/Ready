# Travel-Plan-Permission audit reconciliation — 2026-09-07

Unit: `D-audit-Travel-Plan-Permission--2026-09-07T04-47-30Z`; attempt 2; verified 2026-09-07T07:16:25.145626+00:00.
OUT: `/Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-07.md`.
Current clone and remote main: `37f7ed8afbfb4d6e16ffc613c9856421605ad359`.

Resumed the retained Phase 5 checkpoint; no audit restart, new filing, code edits, or offloads. The previous executor filed three P1 issues. All three remain open and the underlying defects remain present on main. This run independently verified the cited code, reproduced the model/store behaviors, validated the exact live issue bodies, and reconciled delivery evidence.

| Finding | Current evidence and disposition |
|---|---|
| [#1557](https://github.com/stranske/Travel-Plan-Permission/issues/1557) exception decisions are not terminal | `models.py:252-277`: approve then reject produces rejected status while retaining the first approver; reject then approve also succeeds. `http_service.py:885-905,2205` exposes these unguarded methods. Open PR [#1560](https://github.com/stranske/Travel-Plan-Permission/pull/1560) targets this issue; no merge or acceptance verdict made here. |
| [#1558](https://github.com/stranske/Travel-Plan-Permission/issues/1558) overdue escalation is unwired | `docs/exception-policy.md:68` promises escalation after 48 hours. `models.py:279-293` implements it; search finds the definition but no production calls. The 49-hour synthetic request stays pending/manager until the helper is explicitly invoked, then becomes escalated/director. Decision route `http_service.py:2187-2205` authorizes the unchanged tier. Remains open. |
| [#1559](https://github.com/stranske/Travel-Plan-Permission/issues/1559) manager resubmit retains stale data | `review_workflow.py:188-209` returns the stored review without refreshing new inputs. Reproduced create → request changes → resubmit: submitted CHANGED-TRAVELER, stored Jordan Lee, status still changes_requested. `http_service.py:735-751,2025` wires this store into portal submit. Remains open. |

All shortened source paths in this table are under `src/travel_plan_permission/` except the explicit docs path. All cited source lines were opened in the target clone. Runtime evidence is at `/Users/teacher/.codex/automations/research-program/artifacts/audits/tpp-20260907-recovery/reproduction.txt`; its executable reproduction uses synthetic inputs and the repository fixtures. These are model/store reproductions plus static route tracing, not end-to-end browser tests.

## Format and delivery evidence

- Exact live issue bodies: all three pass `.github/scripts/issue_format.py` at the audited head. All lack recommended Scope and Implementation Notes sections. #1558 and #1559 additionally trigger path advisories for ordinary slash-separated prose (pending/escalated and queue/detail); these are not missing source files.
- #1557 successful format run: [34092973521](https://github.com/stranske/Travel-Plan-Permission/actions/runs/34092973521).
- #1559 successful format run: [34092977334](https://github.com/stranske/Travel-Plan-Permission/actions/runs/34092977334).
- #1558: only cancelled/skipped runs in the available workflow inventory; remote validation is UNCONFIRMED. Latest observed [34092976957](https://github.com/stranske/Travel-Plan-Permission/actions/runs/34092976957) skipped. Local validation is a separate positive result.
- Current-head CI succeeded: [34082936960](https://github.com/stranske/Travel-Plan-Permission/actions/runs/34082936960).
- Existing intake log contains exactly one row for each issue (#1557–1559, lines 136–138 at inspection). No duplicate rows added. Original staged issue bodies and audit records remain intact.
- Raw remote snapshots and format outputs: `/Users/teacher/.codex/automations/research-program/artifacts/audits/tpp-20260907-recovery`.

## Coverage and corrections

The retained audit is a focused correctness/wiring refill, not a verified comprehensive eight-dimension audit. D1 and D3 have fresh source/runtime evidence. D2, D5, D6, D7 and D8 lack fresh comprehensive evidence in this unit. D4 was described as static workflow review: that does not establish observed UX coverage. No fresh browser captures or panel exist for this unit; no UX score or gate pass is claimed.

The previous report's 1,106 collected tests with five collection errors, attribution to Dropbox, and broad claims that all prior-wave fixes were verified are historical executor statements, not independently established by this recovery. The clone is outside Dropbox. Current-head remote CI is confirmed, but does not explain the prior local errors. Prior-wave #1547 and other disposition claims are retained in the archived report rather than reasserted as current verified facts.

The original #1559 Tasks offer a new review id for finalized reviews while its Non-Goals forbid reopening finalized records. An implementation should preserve immutable finalized records and refresh the changes-requested path; this ambiguity does not refute the reproduced defect.

Next delivery actions: implement/review the three existing issues through their owning lanes; obtain a successful remote format verdict for #1558 if required by intake. Full observed UX and the unverified audit dimensions remain coverage gaps. No implementation, issue mutation, workflow dispatch, or new issue filing was performed by this executor.
