Scorecard: 8 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 9; journey: passes; surfaces unscored 0; closed-still-broken 0.

# Audit — stranske/Travel-Plan-Permission — 2026-11-03

Audited `main` at `04c1098ce0b2b30ce022d90d351dfd8d17f88105`. Scope was current first-party application, CLI/API and portal product paths, excluding synced workflow implementation and `stranske/Orchestrator`. The strongest objection to the previous 12-surface scorecard debt is valid: the expense reimbursement workflow is a real user-facing product capability but absent from the product contract. It was verified live and filed as a contract-coverage defect, not misstated as a runtime failure.

## Product scorecard

| id | Core function | Result | Current-tip evidence |
| --- | --- | --- | --- |
| PP1 | Planner policy evaluation | WORK | `tests/python/test_http_service.py:338` exercises proposal/status/evaluation routes. Policy outcome changes with the submitted plan. |
| PP2 | Traveller draft/review/submit | WORK | Existing portal flow plus handoff prefill/review tests passed (`tests/python/test_http_service.py:809-855`). |
| PP3 | Exception request and attributed terminal decision | WORK | `tests/python/test_http_service.py:2808-2868` passed for approve/reject first decisions and rejected a later mutation with 409. |
| PP4 | Overdue-exception escalation | WORK | `tests/python/test_http_service.py:4227-4287` passed through draft/admin listing with a 49-hour control and persisted tier changes. |
| PP5 | Manager decision | WORK | Current typed planner-readback cases passed at `tests/python/test_portal_receipt_api.py:668`; decisions alter the readback state. |
| PP6 | Correction after changes requested | PARTIAL | `tests/python/test_http_service.py:4090` passed, but the documented contract remains new-draft-only rather than an in-place correction. |
| PP7 | Policy-gated travel artifacts | WORK | The route family is covered by the portal scorecard path and its artifact authorization tests; prior compliant/blocked live results remain consistent with this tip. |
| PP8 | Policy snapshot | WORK | Proposal and snapshot exercise responds to policy inputs; `docs/PRODUCT_CONTRACT.md:20` now contains PP8. |
| PP9 | Expense reimbursement/export | WORK | `tests/python/test_http_service.py:1121-1154` returned CSV/XLSX for an approved linkage; `test_expense_portal_blocks_export_when_linkage_not_approved` supplied the blocking control. |

The primary journey now passes through the exception branch: policy evaluation, draft/review, exception terminality, overdue escalation, manager/readback, correction boundary, and artifact gates all ran against the current local ASGI product entry point with isolated test state. The current contract's PP6 limitation is intentional but user-visible, so it remains PARTIAL.

## Surface inventory and coverage

The 30-route OpenAPI inventory was reconciled against `docs/PRODUCT_CONTRACT.md:13-20`. Health/readiness are operational interiors; planner intake and handoff routes support PP1/PP2; demo is synthetic-only; expense form/review/artifact routes are PP9. This mapping reduces `surfaces unscored` from 12 to 0 for this round. The repository must persist that reduction by accepting the PP9 contract addition below.

## Verified finding filed

1. [#1724 — Add expense reimbursement workflow to the product contract scorecard](https://github.com/stranske/Travel-Plan-Permission/issues/1724) (P2, documentation/coverage): `docs/PRODUCT_CONTRACT.md:4-20` claims export workflows yet omits the active expense routes implemented at `src/travel_plan_permission/http_service.py:1686-1692`, `:1813-1848`, and `:2269-2310`. The issue includes current repo-relative evidence, a named contract test, an approved-versus-unapproved runtime gate, and deliberate-break → revert proof.

Its body is preserved at `Travel-Plan-Permission-2026-11-03-issue-01-product-contract-expense-workflow.md`. The requested measurement intake record was appended. The post-filing `gh run list -R stranske/Travel-Plan-Permission` read showed a pending `Agents Guard Fork Status Publisher` run (`41620800789`), but no completed issue-format guard verdict for #1724; that verdict is UNKNOWN, not reported as a pass.

## Deduplication and refutations

REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1658 — authenticated current-ASGI manager decisions reach typed planner status/evaluation readback (`tests/python/test_portal_receipt_api.py:668` passed).

REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1668 — artifact-download audit events survive immediate restart and persistence failure returns 503 (`tests/python/test_http_service.py:3184-3280` targeted cases passed).

REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1669 — foreign or conflicting generic proposal replay cannot replace a bound execution (`tests/python/test_portal_receipt_api.py:463-642` targeted cases passed).

REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1721 — the former PP8/PP4 contract claim is false on the live tip: PP8 is present and PP4 is marked WORKS at `docs/PRODUCT_CONTRACT.md:16-20`.

The only open issues at audit start were durable trackers (#1494, #1238, #1203, #977); none duplicate #1724. No runtime defect candidate survived the current-tip reproduction pass.

## Verification record

- `/opt/anaconda3/bin/python3 -m pytest --collect-only -q tests/python`: 1,433 collected, 1 deselected.
- Current scorecard test group: 8 passed in 3.85s.
- Closed-defect reproduction group: 24 passed in 8.27s.
- Expense/handoff/intake group: 9 passed in 1.35s.
- Current GitHub workflows at this SHA were successful when checked; local tests are evidence for the exercised paths, not a substitute for hosted CI.

Confidence is high for the scorecard rows and #1724 because the cited current files were opened and the behavior was exercised through the ASGI entry points. Confidence is medium that no additional issue exists outside this surface because this was a bounded, evidence-led audit; a future route added without a PP10+ contract row should be treated as unscored until exercised.

## Current-tip reconciliation — 2026-11-03 22:44 CST

The prior report was audited at `04c1098ce0b2b30ce022d90d351dfd8d17f88105`; the assigned clone is one commit newer, `0ccee0fab0840de107c8f761f1e7c5e8d45c5f82`. That delta is the merged #1724 documentation/contract fix. It adds PP9 to `docs/PRODUCT_CONTRACT.md:21`, updates `tests/python/test_product_contract.py` to enforce PP1 through PP9 and PP9's exact expense routes/outcomes, and does not change the product runtime route implementation.

Current-tip evidence: `/opt/anaconda3/bin/python3 -m pytest -q tests/python/test_product_contract.py` plus the PP1/PP3/PP4/PP6/PP9 ASGI tests passed **90** cases in 4.46s; the PP2/PP5/PP7 portal/readback selection passed **6** cases in 3.58s. The repository-selected `.venv/bin/python` lacks `pytest`, so the permitted shared Anaconda interpreter supplied these results. They are isolated-ASGI product-path evidence, not a hosted-deployment claim.

REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1724 — its claim that PP9 was absent is false on the live tip: PP9 is now present and guarded by the contract regression.

No new issue was filed. The only open items are durable trackers, and no current-tip defect candidate matched them. The issue-format guard for #1724 is now confirmed: run `41669183476` (`Agents Issue Format Guard`) completed successfully; the current-tip CI run `41668859367` also completed successfully. The scorecard headline above remains unchanged: `8 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 9; journey passes; surfaces unscored 0; closed-still-broken 0`.
