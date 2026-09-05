# Correctness audit — expense, receipt, persistence, policy, and authorization boundaries

Audited commit: `3ba14a8541b97338586ab6c253ea30e2aed7b86e` (`main`)

Baseline: 857 tests collected, with 1 intentionally deselected. The clone had a pre-existing untracked `dossier-out/` directory; this audit did not modify source, configuration, Git state, or remote state.

Focused verification: `uv run --no-sync pytest -q -p no:cacheprovider tests/python/test_export_service.py tests/python/test_http_service.py::test_expense_portal_generates_exports_and_policy_warning tests/python/test_http_service.py::test_manager_review_decision_updates_status_and_history tests/python/test_http_service.py::test_exception_decision_updates_review_detail_and_audit_log tests/python/test_http_service.py::test_expense_review_state_survives_restart` completed with **10 passed, 1 deselected**.

## Retained findings (5)

### 1. [MAJOR] Expense CSV/XLSX downloads bypass the export authorization boundary

**Current runtime evidence.** `GET /portal/expenses/{draft_id}/artifacts/{artifact_name}` accepts neither a request nor an authorization header and returns the cached expense export after only a linkage check. This conflicts with the defined `export` permission and allows any caller that obtains a 12-character draft ID to download reimbursement data and receipt links. The existing HTTP test deliberately performs this download with no auth header at `tests/python/test_http_service.py:924-932`.

**Evidence.** `src/travel_plan_permission/security.py:14-21` defines `Permission.EXPORT`, and `src/travel_plan_permission/security.py:55-61` grants it to finance administrators. The API permission map assigns expense exports that permission at `src/travel_plan_permission/security.py:84-95`. In contrast, the portal expense artifact handler begins at `src/travel_plan_permission/http_service.py:2253-2257` without an authorization parameter or authorization call, then returns the artifact at `src/travel_plan_permission/http_service.py:2278-2295`.

**Minimal repro.** From the target-repo root: `uv run --no-sync python /Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/repro_expense_export_without_auth.py`. It receives HTTP 200 without `Authorization`.

**Fix direction.** Require `Permission.EXPORT` for the expense-detail and artifact endpoints, or explicitly issue a short-lived, draft-scoped capability with the narrowly documented export right. Bind the export audit actor to the authenticated/capability subject. Add missing-token, view-only-token, export-token, and expired-capability cases.

**Dedup.** Closed #821 and #822 protected the pre-trip review artifact surface (`/portal/review/...`) and its authenticated audit metadata. They do not cover the distinct expense route above, which remains unauthenticated at this head.

### 2. [MAJOR] An anonymous caller can create an exception request and it is attributed to the traveler

**Current runtime evidence.** The exception-creation handler has no authorization or handoff-capability check. It reads a draft by ID, constructs an exception, and writes it; the requestor is copied from the stored traveler's name instead of the network caller. An attacker who obtains a draft ID can create workflow noise or a misleading exception/audit entry under that traveler.

**Evidence.** `src/travel_plan_permission/http_service.py:1815-1819` declares the mutating route with only request and draft ID; `src/travel_plan_permission/http_service.py:1820-1825` accepts any existing draft; `src/travel_plan_permission/http_service.py:1864-1870` assigns `requestor` from saved draft data; and `src/travel_plan_permission/http_service.py:1884-1888` persists it. The scoped handoff contract says a capability is limited to one saved draft and only `view` permission at `docs/security-model.md:143-150`; this route enforces neither normal authentication nor that capability.

**Minimal repro.** From the target-repo root: `uv run --no-sync python /Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/repro_exception_request_without_auth.py`. It receives HTTP 303 and creates the request without credentials.

**Fix direction.** Require authenticated `create` permission, or allow only a valid handoff capability whose subject equals the draft ID; record the authenticated subject separately from the traveler/requestor. Cover absent, expired, wrong-draft, create-capable, and successful scoped-handoff cases.

**Dedup.** Closed #800 created the exception UI but did not specify an anonymous write path. Closed #821 covered saved-review reads/downloads, not exception creation. This is a remaining handler-level authorization gap.

### 3. [BLOCKER] Any generic `approve` credential can approve an exception routed to the board

**Current runtime evidence.** A $20,000 exception is routed to `board`, but the HTTP decision endpoint checks only generic `Permission.APPROVE`. The decision method then marks the request approved and records its precomputed `board` level; it never verifies that the authenticated subject is entitled to that level. The resulting audit record falsely presents the generic approver as a board approval.

**Evidence.** Threshold escalation selects board at `src/travel_plan_permission/models.py:194-211`; a request stores that derived level at `src/travel_plan_permission/models.py:247-250`. Its `approve` method accepts the level without an authorization check and changes status to approved at `src/travel_plan_permission/models.py:252-272`. The endpoint requires only generic approval at `src/travel_plan_permission/http_service.py:2106-2118`, takes the body-supplied actor at `src/travel_plan_permission/http_service.py:2119-2135`, and delegates without a level/principal check. The role model gives both an ordinary approver and finance administrator generic `approve` at `src/travel_plan_permission/security.py:47-62`.

**Minimal repro.** From the target-repo root: `uv run --no-sync python /Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/repro_board_exception_approved_by_generic_approver.py`. A bootstrap token containing only `approve` receives HTTP 303 and changes a board-level exception to approved.

**Fix direction.** Model the authority required for manager/director/board exception decisions, derive the actor's authority from the authenticated identity (not form data), reject insufficient authority, and preserve the actual authority in the audit event. Test manager/director/board boundaries and both amount- and escalation-derived board routing.

**Dedup.** No open or recently closed inventory issue names tier-specific exception authorization. #1506 explicitly excluded decision-route authorization from its scope.

### 4. [MAJOR] Approval and exception decisions can forge the recorded approver identity

**Current runtime evidence.** The manager-decision handler authenticates a token but ignores its subject. It passes `actor_id` from the form into the state transition, approval history, and audit log. Existing coverage encodes the mismatch: token subject `manager-reviewer` with form actor `manager-17` is expected at `tests/python/test_http_service.py:1707-1730`. The exception-decision route repeats the same form-controlled identity pattern.

**Evidence.** Manager decisions authenticate at `src/travel_plan_permission/http_service.py:2026-2037`, read the body actor at `src/travel_plan_permission/http_service.py:2039-2042`, and forward it to the transition at `src/travel_plan_permission/http_service.py:2069-2076`. The exception route similarly accepts body `actor_id` at `src/travel_plan_permission/http_service.py:2114-2135`. The persisted approval event accepts that caller-provided identifier at `src/travel_plan_permission/review_workflow.py:95-145` and `src/travel_plan_permission/models.py:446-498`.

**Minimal repro.** From the target-repo root: `uv run --no-sync python /Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/repro_manager_decision_actor_spoof.py`. A token for `authenticated-approver` produces an approval history entry for `forged-manager-id`.

**Fix direction.** Use `auth_context.subject` as the immutable actor for all authorization-sensitive transitions and audit records. If a delegate/principal distinction is needed, model it explicitly as a separately authorized `on_behalf_of` field with both identities recorded. Reject arbitrary form actor IDs. Add regression tests with mismatched token subject/body actor.

**Dedup.** Closed #1506 fixed caller-controlled `actor_role` for the admin console but expressly excluded manager and exception decision authorization. This is a distinct, still-current identity-integrity gap.

### 5. [MAJOR] The portal emits a placeholder URL with no signature while documenting a signed receipt link

**Current runtime evidence.** Portal exports instantiate `ExportService()` with no configured signer. The fallback turns a user-controlled receipt reference into an `https://receipts.example.com/...` URL and adds only a public expiry timestamp. It has neither a storage backend nor a cryptographic signature, despite the accounting contract calling the field a signed URL valid for seven days. Finance receives a nonfunctional placeholder rather than the supporting receipt; the expiry value provides no access control.

**Evidence.** The default base URL and absent signer are at `src/travel_plan_permission/export.py:22-29`; the fallback simply constructs the URL plus `expires_at` at `src/travel_plan_permission/export.py:40-47`; and each export emits it at `src/travel_plan_permission/export.py:49-67`. The portal uses the default constructor at `src/travel_plan_permission/http_service.py:1289-1308`. The documented contract promises a signed URL at `docs/accounting-integration.md:9-16` and `docs/accounting-integration.md:30-32`. Existing tests verify only the timestamp/scheme, not that a real signer or receipt host is configured, at `tests/python/test_export_service.py:91-105`.

**Minimal repro.** From the target-repo root: `uv run --no-sync python /Users/teacher/.codex/automations/research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/repro_unsigned_receipt_link.py`. The emitted CSV contains `receipts.example.com` and no signature.

**Fix direction.** Make a production receipt signer and storage-origin configuration mandatory when an expense has a receipt URL; fail closed with a visible review error if unavailable. Define an allowed internal reference format, verify the signer output is HTTPS and origin-allowed, and test a real signed-link adapter plus missing/malformed configuration.

**Dedup.** Closed #801 introduced receipt and export surfaces but no inventory issue covers false signed-link generation. This is not an OCR-quality claim.

## Dispositions and deliberately excluded claims

| Candidate | Disposition | Reason |
| --- | --- | --- |
| Export audit event disappears after restart | Deduplicated | Closed #1436 explicitly records this successful-export under-reporting case. Repro remains in this asset bundle for confirmation, but it is not a new finding. |
| A policy-flagged $7,500 report still downloads CSV/XLSX | Not filed | Current code and `tests/python/test_http_service.py:899-932` intentionally treat the export as accounting-review handoff, not proof of reimbursement. An ERP-posting or reimbursement-release claim would need downstream evidence. |
| Receipt/OCR total mismatch only warns | Not filed | `docs/expense-workflow.md:9-13` explicitly makes OCR advisory and permits manual correction. |
| Policy config key/override defects | Excluded by scope | Already tracked by #1507 and #1508. |

## Repro inventory

- `repro_expense_export_without_auth.py` — retained finding 1, executed successfully.
- `repro_exception_request_without_auth.py` — retained finding 2, executed successfully.
- `repro_board_exception_approved_by_generic_approver.py` — retained finding 3, executed successfully.
- `repro_manager_decision_actor_spoof.py` — retained finding 4, executed successfully.
- `repro_unsigned_receipt_link.py` — retained finding 5, executed successfully.
- `repro_expense_export_audit_lost_on_restart.py` — confirmed but deduplicated against closed #1436.

Confidence: high for findings 1–5; each is source-traced and runtime-reproduced at the audited commit. The remaining deployment-dependent uncertainty is whether the browser portal is deliberately public in a local-only installation. That does not remove the permission-model contradictions or the anonymous cross-request behavior; it would only change deployment severity.
