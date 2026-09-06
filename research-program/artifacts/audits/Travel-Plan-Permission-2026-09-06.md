# Travel-Plan-Permission Audit Run Report — 2026-09-06

- **Unit ID:** `D-audit-Travel-Plan-Permission--2026-09-06T04-25-49Z`
- **Title:** Audit stranske/Travel-Plan-Permission and file issues (supply 1 <= 2)
- **Repository:** `stranske/Travel-Plan-Permission`
- **Target Git SHA:** `3e53ddea64838fd863146c6efd169e1e32a8ec02` (clean tip of `main`)
- **Timestamp:** 2026-09-06T04:55:00Z
- **Auditor:** Gemini via Antigravity (agy)

---

## 1. Executive Summary

This demand-driven refill audit was triggered for `stranske/Travel-Plan-Permission` after open agent-ready issue supply dropped to 1 (threshold <= 2). The audit conducted a comprehensive multi-dimensional review across the core application library (`src/travel_plan_permission/`), FastAPI HTTP service, review portal, accounting export service, Excel population engine, policy engine, templates, and test suite.

All 8 candidate findings were adversarially validated on the live commit `3e53ddea64838fd863146c6efd169e1e32a8ec02`. Each finding was authored in `AGENT_ISSUE_FORMAT` Markdown and verified against the repository definition of ready using `issue_lint.py` (8/8 PASS). All 8 issues were successfully filed to GitHub with validated repository labels (`bug`, `enhancement`, `risk:major`, `risk:minor`, `priority:high`, `priority:normal`) and confirmed to pass the remote GitHub Actions `Agents Issue Format Guard` workflow with 100% success (0 format rejections, 0 warning comments).

---

## 2. Inventory of Filed Issues

| # | Priority | Dimension | Title | Target File:Line | Filed URL | Format Guard Run |
|---|---|---|---|---|---|---|
| 1 | P1 | D3 | `[P1] Enforce permissions on expense intake, review, and export` | `src/travel_plan_permission/http_service.py:1726, 1799, 2253` | [#1523](https://github.com/stranske/Travel-Plan-Permission/issues/1523) | `34012628561` (SUCCESS) |
| 2 | P1 | D3 | `[P1] Authenticate exception creation and bind its audit actor` | `src/travel_plan_permission/http_service.py:1815, 1867, 1884` | [#1524](https://github.com/stranske/Travel-Plan-Permission/issues/1524) | `34012628561` (SUCCESS) |
| 3 | P1 | D3 | `[P1] Bind approval history to the authenticated decision maker` | `src/travel_plan_permission/http_service.py:2033, 2041, 2074, 2123` | [#1525](https://github.com/stranske/Travel-Plan-Permission/issues/1525) | `34012628561` (SUCCESS) |
| 4 | P1 | D1 | `[P1] Preserve untrusted export text as literal spreadsheet cells` | `src/travel_plan_permission/export.py:62, 85, 110` | [#1526](https://github.com/stranske/Travel-Plan-Permission/issues/1526) | `34012628561` (SUCCESS) |
| 5 | P1 | D6 | `[P1] Replace placeholder receipt links with a verifiable delivery contract` | `src/travel_plan_permission/export.py:25, 40`, `http_service.py:1294` | [#1527](https://github.com/stranske/Travel-Plan-Permission/issues/1527) | `34012628561` (SUCCESS) |
| 6 | P2 | D4 | `[P2] Give direct portal drafts a usable scoped review session` | `src/travel_plan_permission/http_service.py:1696, 1703, 1721, 1762` | [#1528](https://github.com/stranske/Travel-Plan-Permission/issues/1528) | `34012628561` (SUCCESS) |
| 7 | P2 | D7 | `[P2] Guard shipped YAML defaults against checkout and wheel drift` | `src/travel_plan_permission/config_loader.py:35`, `tests/python/test_policy_api.py:1276` | [#1529](https://github.com/stranske/Travel-Plan-Permission/issues/1529) | `34012628561` (SUCCESS) |
| 8 | P2 | D3 | `[P2] Bind routed exception levels to authenticated approval authority` | `src/travel_plan_permission/models.py:194, 263`, `http_service.py:2114` | [#1530](https://github.com/stranske/Travel-Plan-Permission/issues/1530) | `34012628561` (SUCCESS) |

---

## 3. Detailed Finding Breakdown & Adversarial Reproduction

### Finding 1: Unauthenticated Expense Intake, Review, and Export ([#1523](https://github.com/stranske/Travel-Plan-Permission/issues/1523))
- **File & Lines:** `src/travel_plan_permission/http_service.py:1726, 1799, 2253`, `src/travel_plan_permission/security.py:14, 55`
- **Defect:** `POST /portal/expenses/review` (intake), `GET /portal/expenses/{draft_id}` (saved detail), and `GET /portal/expenses/{draft_id}/artifacts/{name}` (CSV/XLSX export) have no `authorization` header requirements or permission checks. An anonymous caller knowing an approved request ID can draft expenses, inspect details, and download export artifacts.
- **Reproduction:** Executed unauthenticated requests against the portal routes; received HTTP 303 (creation), HTTP 200 (detail view), and HTTP 200 (CSV artifact download) without credentials.
- **Test Gate:** `pytest tests/python/test_http_service.py::test_expense_routes_enforce_permissions`

### Finding 2: Unauthenticated Exception Creation and Mutable Attribution ([#1524](https://github.com/stranske/Travel-Plan-Permission/issues/1524))
- **File & Lines:** `src/travel_plan_permission/http_service.py:1815, 1867, 1884`, `docs/security-model.md:148`
- **Defect:** `POST /portal/review/{draft_id}/exceptions` defines exception creation without authorization checks. Furthermore, line 1867 attributes the requestor to stored traveler text (`str(draft.answers.get("traveler_name") or "portal-traveler")`) rather than an authenticated identity.
- **Reproduction:** Submitted anonymous POST to `/portal/review/{draft_id}/exceptions`; returned 303 and successfully persisted an exception request attributed to traveler display text.
- **Test Gate:** `pytest tests/python/test_http_service.py::test_exception_creation_requires_create_permission`

### Finding 3: Decision Actor Identity Forgery via POST Form Payload ([#1525](https://github.com/stranske/Travel-Plan-Permission/issues/1525))
- **File & Lines:** `src/travel_plan_permission/http_service.py:2033, 2041, 2074, 2123`
- **Defect:** While manager and exception decision endpoints authenticate `Permission.APPROVE` (lines 2033, 2114), they read `actor_id` from the unverified form body (`parsed.get("actor_id")`) and record that value into the decision history and audit trail rather than using `auth_context.subject`.
- **Reproduction:** Authenticated with valid approver token for `approver-1` and submitted form with `actor_id=manager-vip`; approval record and audit history persisted `manager-vip` as decision maker.
- **Test Gate:** `pytest tests/python/test_http_service.py::test_approval_actor_comes_from_token`

### Finding 4: Untrusted Text Preserved as Formula Cells in Generated Spreadsheets ([#1526](https://github.com/stranske/Travel-Plan-Permission/issues/1526))
- **File & Lines:** `src/travel_plan_permission/export.py:62, 85, 110`
- **Defect:** `ExportService.to_excel()` directly appends raw user strings (`vendor`, `cost_center`) via `ws.append()`. Strings beginning with `=`, `+`, `-`, or `@` (e.g. `=1+1`, `=2+2`) are evaluated as active formula cells (`data_type='f'`) by openpyxl and Excel rather than plain strings.
- **Reproduction:** Generated Excel export with `vendor="=1+1"` and `cost_center="=2+2"`; openpyxl inspection showed cell types `f` with formula values instead of string literals.
- **Test Gate:** `pytest tests/python/test_export_service.py::test_export_preserves_literal_user_text`

### Finding 5: Placeholder Receipt Links Emitted as Unverified URLs ([#1527](https://github.com/stranske/Travel-Plan-Permission/issues/1527))
- **File & Lines:** `src/travel_plan_permission/export.py:25, 40`, `src/travel_plan_permission/http_service.py:1294`, `docs/accounting-integration.md:16, 32`
- **Defect:** `ExportService` defaults to `https://receipts.example.com` and appends `?expires_at=...` with no cryptographic signature or hash. `http_service.py:1294` instantiates `ExportService()` with default parameters, emitting placeholder links in production accounting exports despite documentation promising 7-day signed access.
- **Reproduction:** Executed expense export; output CSV and XLSX emitted `https://receipts.example.com/receipt.pdf?expires_at=...` with unsigned query parameters.
- **Test Gate:** `pytest tests/python/test_http_service.py::test_portal_receipt_delivery_configuration` and `tests/python/test_export_service.py::test_receipt_link_requires_real_delivery_mode`

### Finding 6: Direct Browser Draft Creation Redirects Without Scoped Session Cookie ([#1528](https://github.com/stranske/Travel-Plan-Permission/issues/1528))
- **File & Lines:** `src/travel_plan_permission/http_service.py:1696, 1703, 1721, 1762`
- **Defect:** Sibling handoff (`POST /portal/handoff/draft`, line 1696) issues a scoped HMAC view cookie so browser users can view their review summary. Direct draft creation (`POST /portal/draft`, line 1703) saves the draft and redirects to `/portal/review/{draft_id}` without setting any cookie, causing `/portal/review/{draft_id}` to reject the browser user with 401 "Missing bearer token".
- **Reproduction:** Submitted public draft form in browser; followed redirect to `/portal/review/{draft_id}` and received HTTP 401 raw JSON error. Injected synthetic bearer token and the page rendered correctly.
- **Test Gate:** `pytest tests/python/test_http_service.py::test_direct_draft_scoped_review_session`

### Finding 7: YAML Packaging Parity Regression Gate ([#1529](https://github.com/stranske/Travel-Plan-Permission/issues/1529))
- **File & Lines:** `src/travel_plan_permission/config_loader.py:35`, `tests/python/test_policy_api.py:1276`, `tests/python/test_template_assets.py:61`
- **Defect:** `config_loader.py` falls back to packaged resources when root configuration is absent (e.g. in built wheels). Existing tests assert packaged file existence but do not enforce byte-level parity between root YAML files (`config/*.yaml`) and packaged copies (`src/travel_plan_permission/config/*.yaml`), risking silent divergence during edits.
- **Reproduction:** Verified that all 5 YAML pairs currently match byte-for-byte, but modifying a packaged default in isolation is undetected by the current test suite.
- **Test Gate:** `pytest tests/python/test_package_data.py::test_packaged_yaml_matches_repo_defaults`

### Finding 8: Exception Approval Lacks Routed Tier Entitlement Check ([#1530](https://github.com/stranske/Travel-Plan-Permission/issues/1530))
- **File & Lines:** `src/travel_plan_permission/models.py:194, 263`, `src/travel_plan_permission/http_service.py:2114`, `docs/exception-policy.md:53`
- **Defect:** `models.py:194-211` defines monetary thresholds routing exceptions to Manager, Director ($5,000+), or Board ($20,000+). However, `http_service.py:2114` checks only generic `Permission.APPROVE`, allowing any approver-level credential to finalize high-value director/board exceptions without entitlement verification.
- **Reproduction:** Submitted a $25,000 exception request (routed to Board level); approved using a generic `approver` role token; returned HTTP 303 and successfully recorded a Board-level approval record.
- **Test Gate:** `pytest tests/python/test_http_service.py::test_exception_approval_enforces_tier`

---

## 4. Verification & Continuity Record

1. **Intake Measurement Log**: Appended 8 entries to `~/.codex/orchestrator/measurement/intake-2026-09-04.log` (`Travel-Plan-Permission|01-expense-authorization.md|https://github.com/stranske/Travel-Plan-Permission/issues/1523` through `08-exception-tier-authority.md`).
2. **Durable Ledger**: Updated `Code/Audits/AUDIT_LEDGER.md` and `Code/Audits/Travel-Plan-Permission/README.md` with complete 2026-09-06 audit entries and issue mappings.
3. **Checkpoints**: Written to `artifacts/audits/D-audit-Travel-Plan-Permission--2026-09-06T04-25-49Z.CHECKPOINT.md` and appended to `artifacts/audits/CHECKPOINT.md`.
4. **Format Guard Checks**: Evaluated remote `Agents Issue Format Guard` runs on GitHub Actions; all 8 issues passed with status `SUCCESS`.
