# [P1] Replace placeholder receipt links with a verifiable delivery contract

## Why

Current break: accounting exports advertise signed receipt links, but the portal emits a placeholder receipts.example.com URL with only an editable expiry timestamp. `src/travel_plan_permission/export.py:25` supplies the placeholder origin; `src/travel_plan_permission/export.py:40` appends a query parameter without a signature; `src/travel_plan_permission/http_service.py:1294` always constructs the default service. `docs/accounting-integration.md:16` and `docs/accounting-integration.md:32` promise seven-day signed access. The goal is a usable and accurately described source-receipt reference; no deployed receipt server or signature-verification bypass was demonstrated.

## Scope

Explicit receipt delivery mode and origin/signer wiring from the portal into ExportService, plus truthful offline and hosted behavior.

## Non-Goals

Uploading data to an external service, selecting an ERP or requiring hosted infrastructure for local receipt references. Scaffold-only completion does NOT count: renaming the helper while production exports retain placeholder URLs represented as signed links is a failure of this issue.

## Tasks

- [ ] In `src/travel_plan_permission/export.py`, require explicit hosted signer configuration for signed-link mode and reject placeholder or malformed signer results; define a separately named local-reference mode without a false expiry promise.
- [ ] In `src/travel_plan_permission/http_service.py`, pass the selected receipt delivery configuration into `_expense_export_artifacts` and show an actionable validation error when a referenced receipt cannot be resolved in that mode.
- [ ] Update `docs/accounting-integration.md` to specify the two mode contracts, including local reference resolution and hosted expiry validation.
- [ ] Add `test_portal_receipt_delivery_configuration` to `tests/python/test_http_service.py` and `test_receipt_link_requires_real_delivery_mode` to `tests/python/test_export_service.py` with temporary local receipt files and a deterministic signer and verifier fixture.

## Acceptance Criteria

- [ ] Run pytest `tests/python/test_http_service.py::test_portal_receipt_delivery_configuration` and `tests/python/test_export_service.py::test_receipt_link_requires_real_delivery_mode`; local references resolve to the fixture, hosted references verify before expiry and fail verification after tampering or expiry, and missing configuration emits no placeholder link.
- [ ] Deliberate-break gate: restore the default timestamp-only URL path in `src/travel_plan_permission/export.py`; `tests/python/test_export_service.py::test_receipt_link_requires_real_delivery_mode` must fail its missing-configuration or signature assertion; revert the break.

## Implementation Notes

Audited remote main: 3ba14a8541b97338586ab6c253ea30e2aed7b86e.

Independent unsigned-link repro and expense-proof.json confirm the portal constructor path. Honor owner guidance: local files and Python are available; do not impose hosting when local references meet the goal. Any hosted adapter must document the specific IT accommodation it needs.
