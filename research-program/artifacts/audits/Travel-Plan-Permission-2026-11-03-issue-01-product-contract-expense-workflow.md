## Why

`docs/PRODUCT_CONTRACT.md:4-20` says the product drives export workflows but its core-functions table ends at PP8 and contains no reimbursement/expense workflow. Current runtime routes implement that user flow at `src/travel_plan_permission/http_service.py:1686-1692`, `:1813-1848`, and `:2269-2310`: an authorized user can create an expense review and download CSV/XLSX only when its approved-request linkage remains valid. `tests/python/test_http_service.py:1121-1154` drives the real ASGI route and observes both exports; the contract omission leaves those routes unscored in the Phase 1.5 inventory.

This is current documentation/coverage drift, not a claim that the expense runtime is broken.

## Scope

- Add a PP9 row to `docs/PRODUCT_CONTRACT.md` for the expense-reimbursement workflow: an authorized user creates an expense review and sees policy-gated CSV/XLSX accounting artifacts through `/portal/expenses/new`, `POST /portal/expenses/review`, and `/portal/expenses/{draft_id}/artifacts/{artifact_name}`.
- Give PP9 a probe that varies approved versus unapproved request linkage and records the different export response.
- Add a contract-table regression in `tests/python/test_product_contract.py` that requires PP1 through PP9 and requires PP9 to name the expense route and its policy-gated artifact outcome.

## Non-Goals

- Do not change expense authorization, export bytes, accounting integration, OCR, or reimbursement-system writes.
- Do not relabel a blocked artifact response as successful reimbursement.
- Scaffold-only or partial completion does not count as done: a row without the route, policy-gated outcome, and regression assertion does not satisfy this issue.

## Tasks

- [ ] In `docs/PRODUCT_CONTRACT.md` after PP8, add PP9 with the verified expense entry points and an approved-versus-unapproved-linkage varying-input probe.
- [ ] Add `tests/python/test_product_contract.py` to parse `docs/PRODUCT_CONTRACT.md` and assert that PP1 through PP9 exist and PP9 names `/portal/expenses/review` plus an artifact route.
- [ ] Keep `tests/python/test_http_service.py::test_expense_portal_generates_exports_and_policy_warning` and `tests/python/test_http_service.py::test_expense_portal_blocks_export_when_linkage_not_approved` as the runtime evidence named by the contract row.

## Acceptance Criteria

- [ ] `pytest tests/python/test_product_contract.py -q` passes and proves the product contract contains PP1 through PP9, including PP9's expense-review route and artifact outcome.
- [ ] `pytest tests/python/test_http_service.py::test_expense_portal_generates_exports_and_policy_warning tests/python/test_http_service.py::test_expense_portal_blocks_export_when_linkage_not_approved -q` passes: an approved linkage yields CSV/XLSX artifacts and an unapproved linkage is blocked.
- [ ] Deliberate break: temporarily remove PP9 from `docs/PRODUCT_CONTRACT.md`; `tests/python/test_product_contract.py -q` fails; restore PP9 and rerun the test successfully.

## Implementation Notes

- `docs/PRODUCT_CONTRACT.md:4-20` is the Phase 1.5 scorecard contract.
- `src/travel_plan_permission/http_service.py:1686-1692`, `:1813-1848`, and `:2269-2310` are the existing expense form, persisted review, and artifact routes.
- `tests/python/test_http_service.py:1121-1154` is the current success-path ASGI evidence; `tests/python/test_http_service.py::test_expense_portal_blocks_export_when_linkage_not_approved` provides the blocking control.
