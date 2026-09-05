from pathlib import Path
import json
base=Path(__file__).resolve().parent
out=base/'issue-bodies';out.mkdir(exist_ok=True)
head='3ba14a8541b97338586ab6c253ea30e2aed7b86e'
items=[
('01-expense-authorization','P1','Enforce permissions on expense intake, review, and export','security',
'''Current break at the audited head: an anonymous HTTP client can create an expense draft (303), read its saved details (200), and download its accounting CSV (200). A valid approved-request linkage is checked, but it does not establish the caller identity. `src/travel_plan_permission/http_service.py:1726` accepts the expense POST, `src/travel_plan_permission/http_service.py:1799` renders saved details, and `src/travel_plan_permission/http_service.py:2253` serves exports without authentication. The role model distinguishes view, create, and export at `src/travel_plan_permission/security.py:14` and grants export to finance administrators at `src/travel_plan_permission/security.py:55`. The goal is an authenticated accounting handoff. A caller must know or obtain an existing identifier; no enumeration exploit is claimed.''',
'Expense portal route authorization, with existing linkage validation retained. Use create for intake, view for saved details, and export for downloadable accounting artifacts.',
'Changing reimbursement policy, OCR, or pre-trip permission requirements. Scaffold-only completion does NOT count: protecting only the navigation while direct expense requests still succeed without permission is a failure of this issue.',
[
'In `src/travel_plan_permission/http_service.py`, authorize expense POST, saved-detail GET, and artifact GET before reading or mutating draft state using the matching Permission member from `src/travel_plan_permission/security.py`.',
'In `src/travel_plan_permission/http_service.py`, record the authenticated subject for expense export audit events instead of the constant expense-portal actor.',
'Add `test_expense_routes_enforce_permissions` to `tests/python/test_http_service.py`, with missing-token, view-only, create-only, export-enabled and invalid-linkage controls; assert denied operations do not mutate state or emit success events.'
],
[
'Run pytest `tests/python/test_http_service.py::test_expense_routes_enforce_permissions`; unauthenticated requests return 401, insufficient permissions return 403, and allowed requests retain the existing linkage checks.',
'Deliberate-break gate: temporarily remove the expense export authorization call in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_expense_routes_enforce_permissions` must fail its missing-token export assertion; revert the break.'
],
'Independent proof: expense-proof.json records 303/200/200 without credentials and 400 for an unknown approved request. Closed issue 821 covered pre-trip review reads; this is the separate expense route. Tests should preserve the deliberate accounting-review handoff behavior for flagged reports.'),
('02-exception-create-authorization','P1','Authenticate exception creation and bind its audit actor','security',
'''Current break: an anonymous POST creates an exception against an existing travel draft and attributes it to the traveler. `src/travel_plan_permission/http_service.py:1815` defines the mutation without authorization, `src/travel_plan_permission/http_service.py:1867` derives the requestor from stored traveler text, and `src/travel_plan_permission/http_service.py:1884` persists it. The existing handoff capability is explicitly view-only in `docs/security-model.md:145`. The goal is that exception submissions are attributable to an authorized creator, including when the draft identifier is known.''',
'Authorization and immutable caller attribution for exception creation on the saved travel-draft route.',
'Changing exception routing thresholds or allowing view-only handoff cookies to mutate drafts. Scaffold-only completion does NOT count: hiding the exception form while anonymous POST still persists a request is a failure of this issue.',
[
'In `src/travel_plan_permission/http_service.py`, require Permission.CREATE before exception request parsing or persistence and retain the authenticated context.',
'In `src/travel_plan_permission/http_service.py`, bind the exception requestor and audit actor to the authenticated subject; keep traveler display data separately if required.',
'Add `test_exception_creation_requires_create_permission` to `tests/python/test_http_service.py` for anonymous, view-only token, view-only handoff cookie, expired token and create-enabled requests; verify rejected calls leave the exception store unchanged.'
],
[
'Run pytest `tests/python/test_http_service.py::test_exception_creation_requires_create_permission`; anonymous requests return 401, view-only credentials cannot create, and a valid creator gets a request attributed to its token subject.',
'Deliberate-break gate: remove the creation permission check in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_exception_creation_requires_create_permission` must fail the anonymous mutation assertion; revert the break.'
],
'The independently executed anonymous exception repro returned 303 and persisted one traveler-attributed request. Closed issues 800 and 821 introduced UI and read permissions, respectively; neither covers this remaining mutation. Preserve the view-only handoff contract.'),
('03-approval-actor-integrity','P1','Bind approval history to the authenticated decision maker','security',
'''Current break: a token for authenticated-approver can write an approval-history entry for forged-manager-id. `src/travel_plan_permission/http_service.py:2033` authenticates a manager decision, but `src/travel_plan_permission/http_service.py:2041` accepts actor_id from the form and `src/travel_plan_permission/http_service.py:2074` forwards it as the decision actor. The exception decision repeats this at `src/travel_plan_permission/http_service.py:2123`. The goal is an audit trail whose approving identity reflects the authenticated caller. This does not claim an unauthenticated approval; the attacker already has generic approve permission.''',
'Authenticated identity propagation for manager and exception approval/rejection histories and success audit events.',
'Changing role grants, exception tier policy or silently treating an arbitrary actor_id as delegation. Scaffold-only completion does NOT count: correcting a page label while persisted approval events retain the forged body identity is a failure of this issue.',
[
'In `src/travel_plan_permission/http_service.py`, use auth_context.subject for manager and exception decision actor_id; reject conflicting supplied actor_id or remove it from the form contract.',
'Update `src/travel_plan_permission/templates/manager_review_detail.html` and `src/travel_plan_permission/templates/portal_admin.html` so operator text cannot override the authenticated actor identity.',
'Add `test_approval_actor_comes_from_token` to `tests/python/test_http_service.py`, covering mismatched form actor values on both decision routes and inspecting persisted history and audit events.'
],
[
'Run pytest `tests/python/test_http_service.py::test_approval_actor_comes_from_token`; accepted decisions record the token subject, or conflicting form actors cause a rejection with unchanged state.',
'Deliberate-break gate: restore parsed form actor_id as the manager decision argument in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_approval_actor_comes_from_token` must fail its recorded-identity assertion; revert the break.'
],
'Independent actor-spoof repro succeeded against the unchanged remote head. Closed issue 1506 explicitly excluded decision authorization; this is not another admin-console actor_role finding. Authorized delegation, if later added, must retain both actual caller and represented principal.'),
('04-export-literal-text','P1','Preserve untrusted export text as literal spreadsheet cells','bug',
'''Current break: vendor =1+1 and cost center =2+2 become formula cells in the generated workbook, and are emitted unchanged in CSV. `src/travel_plan_permission/export.py:59` copies vendor and cost-center strings into export rows, `src/travel_plan_permission/export.py:84` writes CSV rows, and `src/travel_plan_permission/export.py:110` appends those strings into openpyxl cells. Independent inspection of the saved XLSX reports data_type f for B2 and E2. The goal is faithful export of expense metadata as text. Only benign arithmetic formulas were used in verification; no external data access was attempted.''',
'Literal-text handling for user-controlled vendor, cost-center and receipt-link fields in CSV and XLSX exports, preserving numeric amount cells.',
'Changing accounting schema, disabling all hyperlinks or evaluating formulas during tests. Scaffold-only completion does NOT count: escaping only the displayed portal text while downloaded workbooks retain formula cells is a failure of this issue.',
[
'In `src/travel_plan_permission/export.py`, serialize user-controlled XLSX text with explicit text cell semantics so leading formula characters cannot change cell type.',
'In `src/travel_plan_permission/export.py`, apply and document a CSV literal-text policy for leading formula/control prefixes without altering amount values or permitted receipt URLs.',
'Add `test_export_preserves_literal_user_text` to `tests/python/test_export_service.py` for equals, plus, minus, at-sign and leading whitespace/control variants; inspect saved cell types and parsed CSV fields.'
],
[
'Run pytest `tests/python/test_export_service.py::test_export_preserves_literal_user_text`; workbook B2 and E2 preserve the supplied strings with text types, CSV follows the documented policy, and C2 remains numeric.',
'Deliberate-break gate: restore direct user text writes in `src/travel_plan_permission/export.py`; `tests/python/test_export_service.py::test_export_preserves_literal_user_text` must fail its formula-type or CSV-prefix assertions; revert the break.'
],
'formula-proof.json captures f cell types for benign formulas. The browser expense route also exported a vendor value beginning with equals. No matching issue appears in the current 150-issue inventory.'),
('05-receipt-link-contract','P1','Replace placeholder receipt links with a verifiable delivery contract','bug',
'''Current break: accounting exports advertise signed receipt links, but the portal emits a placeholder receipts.example.com URL with only an editable expiry timestamp. `src/travel_plan_permission/export.py:25` supplies the placeholder origin; `src/travel_plan_permission/export.py:40` appends a query parameter without a signature; `src/travel_plan_permission/http_service.py:1294` always constructs the default service. `docs/accounting-integration.md:16` and `docs/accounting-integration.md:32` promise seven-day signed access. The goal is a usable and accurately described source-receipt reference; no deployed receipt server or signature-verification bypass was demonstrated.''',
'Explicit receipt delivery mode and origin/signer wiring from the portal into ExportService, plus truthful offline and hosted behavior.',
'Uploading data to an external service, selecting an ERP or requiring hosted infrastructure for local receipt references. Scaffold-only completion does NOT count: renaming the helper while production exports retain placeholder URLs represented as signed links is a failure of this issue.',
[
'In `src/travel_plan_permission/export.py`, require explicit hosted signer configuration for signed-link mode and reject placeholder or malformed signer results; define a separately named local-reference mode without a false expiry promise.',
'In `src/travel_plan_permission/http_service.py`, pass the selected receipt delivery configuration into `_expense_export_artifacts` and show an actionable validation error when a referenced receipt cannot be resolved in that mode.',
'Update `docs/accounting-integration.md` to specify the two mode contracts, including local reference resolution and hosted expiry validation.',
'Add `test_portal_receipt_delivery_configuration` to `tests/python/test_http_service.py` and `test_receipt_link_requires_real_delivery_mode` to `tests/python/test_export_service.py` with temporary local receipt files and a deterministic signer/verifier fixture.'
],
[
'Run pytest `tests/python/test_http_service.py::test_portal_receipt_delivery_configuration` and `tests/python/test_export_service.py::test_receipt_link_requires_real_delivery_mode`; local references resolve to the fixture, hosted references verify before expiry and fail verification after tampering/expiry, and missing configuration emits no placeholder link.',
'Deliberate-break gate: restore the default timestamp-only URL path in `src/travel_plan_permission/export.py`; `tests/python/test_export_service.py::test_receipt_link_requires_real_delivery_mode` must fail its missing-configuration or signature assertion; revert the break.'
],
'Independent unsigned-link repro and expense-proof.json confirm the portal constructor path. Honor owner guidance: local files and Python are available; do not impose hosting when local references meet the goal. Any hosted adapter must document the specific IT accommodation it needs.'),
('06-browser-draft-recovery','P2','Give direct portal drafts a usable scoped review session','enhancement',
'''Current browser break: completing the public form and clicking Save draft and review ends at raw JSON saying Missing bearer token. With an injected synthetic bearer token, the same saved draft renders. `src/travel_plan_permission/http_service.py:1703` saves the public direct draft, then redirects at line 1721 without a browser session. Review authorization at `src/travel_plan_permission/http_service.py:1762` rejects it. The sibling handoff flow already issues a short-lived draft-specific view cookie at `src/travel_plan_permission/http_service.py:1695`. The goal is a complete direct browser drafting/review flow while retaining protected mutation and download permissions.''',
'Direct draft creation and review-session recovery using the existing view-only handoff capability contract.',
'Granting anonymous create/approve/export permissions, removing bearer checks globally or exposing tokens in URLs. Scaffold-only completion does NOT count: replacing the raw error with static prose while a newly saved direct draft remains inaccessible to its creator is a failure of this issue.',
[
'In `src/travel_plan_permission/http_service.py`, reuse the existing `_set_handoff_cookie` and `issue_handoff_token` flow for a successfully created direct draft, limited to viewing that draft with the existing expiry and cookie attributes.',
'In `src/travel_plan_permission/http_service.py`, verify signing configuration before saving a direct draft and return a browser-readable recoverable error when the capability cannot be issued.',
'Add `test_direct_draft_scoped_review_session` to `tests/python/test_http_service.py`, covering direct form POST followed by browser-cookie review, wrong draft, expiry and denied submission using only the view cookie.'
],
[
'Run pytest `tests/python/test_http_service.py::test_direct_draft_scoped_review_session`; a new browser session completes direct draft creation and review without manually supplied headers, but cannot view a different draft or submit with the cookie alone.',
'Deliberate-break gate: remove cookie issuance from direct draft creation in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_direct_draft_scoped_review_session` must fail the follow-redirect review assertion; revert the break.',
'Capture browser verification of the completed synthetic form leading to its review page and a separate denied mutation with the view-only cookie.'
],
'Browser screenshots anonymous-draft-result and authenticated-draft-result establish the matched control. Closed issue 821 intentionally protects review access; this issue preserves it by reusing the existing narrowly scoped capability. The four-evaluator UX panel corroborated the recovery failure.'),
('07-config-parity-guard','P2','Guard shipped YAML defaults against checkout and wheel drift','validation',
'''Latent fragility, not a current configuration divergence: all five paired YAML files are byte-identical at this head. `src/travel_plan_permission/config_loader.py:35` chooses a filesystem path or packaged fallback, so checkout and wheel execution can consume different copies. `tests/python/test_policy_api.py:1188` checks packaged file existence, but does not compare content. `tests/python/test_template_assets.py:61` separately reads the root mapping. The goal is that checked-in default policy, validation, provider, approval and mapping configuration agree across installation modes; operator-supplied overrides remain intentional.''',
'A default-config parity regression gate in existing tests, limited to tracked repository defaults and their packaged copies.',
'Deleting either configuration tree, changing override precedence, or reopening shared-loader refactoring from issue 1151. Scaffold-only completion does NOT count: testing existence of both files while different contents still pass is a failure of this issue.',
[
'In `tests/python/test_package_data.py`, add `test_packaged_yaml_matches_repo_defaults` parameterized over the five tracked YAML pairs, comparing bytes and naming both files on failure.',
'In `tests/python/test_package_data.py`, add `test_config_parity_guard_detects_one_sided_change` against temporary paired files so a one-sided content change is demonstrably detected.',
'Update `docs/validation-rules.md` to distinguish synchronized checked-in defaults from explicit operator override files and name the parity test command.'
],
[
'Run pytest `tests/python/test_package_data.py::test_packaged_yaml_matches_repo_defaults`; all five default pairs match and a mismatch report identifies the two paths.',
'Deliberate-break gate: temporarily change only `config/policy.yaml`; `tests/python/test_package_data.py::test_packaged_yaml_matches_repo_defaults` must fail the policy pair; revert the break.'
],
'Root and packaged files were independently byte-compared. Existing packaged-default tests protect presence and construction; this adds content equivalence. Retain intentional editable defaults and packaged fallback behavior.'),
('08-exception-tier-authority','P2','Bind routed exception levels to authenticated approval authority','architecture',
'''Verified enforcement gap: a credential containing only generic approve can approve a 20,000 exception and create a board-level record. `src/travel_plan_permission/models.py:194` defines director/board thresholds and `src/travel_plan_permission/models.py:263` records the routed level, while `src/travel_plan_permission/http_service.py:2114` checks only generic Permission.APPROVE. This is bounded design hardening, not a claimed violation of an existing tier-entitlement contract: `docs/exception-policy.md:48` explicitly describes the current generic approve-capable portal. The goal is to make routing levels enforceable authority requirements instead of labels inferred from the request.''',
'Explicit authenticated exception-tier entitlement and fail-closed checks on portal approval, with synthetic configuration fixtures and accurate audit records.',
'Assigning real employees to director or board roles, changing monetary thresholds, or treating actor_role query text as authority. Scaffold-only completion does NOT count: displaying a board label while the generic approve token still finalizes board requests is a failure of this issue.',
[
'In `src/travel_plan_permission/security.py`, define an explicit trusted subject-to-exception-tier entitlement contract; missing higher-tier entitlement must not imply director or board authority.',
'In `src/travel_plan_permission/http_service.py`, check the authenticated subject entitlement against the exception current routed level before calling decide_exception_request; reject insufficient authority without history mutation.',
'Update `docs/exception-policy.md` to distinguish generic approval permission, exception-tier entitlement, and the deployment responsibility to configure actual principals.',
'Add `test_exception_approval_enforces_tier` to `tests/python/test_http_service.py` covering manager/director/board, amount-derived levels, 48-hour escalation, missing entitlement, and spoofed actor fields.'
],
[
'Run pytest `tests/python/test_http_service.py::test_exception_approval_enforces_tier`; generic approve alone cannot finalize a board exception, an explicitly entitled synthetic board subject can, and rejected decisions preserve state.',
'Deliberate-break gate: bypass the tier comparison in `src/travel_plan_permission/http_service.py`; `tests/python/test_http_service.py::test_exception_approval_enforces_tier` must fail the generic-approver board case; revert the break.'
],
'Independent board-exception repro returned 303 and a board-level approval using only generic approve. Lead review downgraded the delegate BLOCKER classification because the current documented scope permits approve-capable roles; this is an explicit extension of the authorization model. Use synthetic entitlements in tests; leave actual organizational mapping unconfigured for the owner to supply at deployment.')
]
manifest=[]
for slug,priority,title,label,why,scope,nongoals,tasks,accept,notes in items:
 text=f'# [{priority}] {title}\n\n## Why\n\n{why}\n\n## Scope\n\n{scope}\n\n## Non-Goals\n\n{nongoals}\n\n## Tasks\n\n'+''.join('- [ ] '+s+'\n' for s in tasks)+'\n## Acceptance Criteria\n\n'+''.join('- [ ] '+s+'\n' for s in accept)+f'\n## Implementation Notes\n\nAudited remote main: {head}.\n\n{notes}\n'
 p=out/(slug+'.md');p.write_text(text)
 manifest.append({'id':slug,'priority':priority,'title':title,'body_file':str(p),'labels':[label,'priority:high' if priority=='P1' else 'priority:normal'],'status':'staged_research_only','url':None})
(base/'issue-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Wrote',len(items),'issue bodies')
