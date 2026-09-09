# D4 Implementation Verification Report: Merged PRs vs. Acceptance Criteria

**Execution Unit:** `D4-verify-merged-2026-09-09T01`  
**Execution Window:** Last 36 hours (~2026-09-07T10:00:00Z to 2026-09-09T01:36:48Z)  
**Total Candidate PRs Screened:** 48 across lane fleet repositories  
**Evaluation Scope:** Lane fleet repositories (`SUPPORTED_REPOS` in `handoff.sh`, excluding `stranske/Orchestrator`), excluding template-sync, dependency, and release chores.  
**Pacing Cap:** 20 pull requests verified in this run (oldest merged first among unverified PRs after 2026-09-07T09:28:55Z).

---

## Executive Summary

- **Total PRs Verified in this Batch:** 20
- **VERIFIED:** 20 / 20 (100%)
- **PARTIAL:** 0 / 20 (0%)
- **NOT IMPLEMENTED:** 0 / 20 (0%)
- **Follow-up Issues Required/Filed:** 0 *(Note: The spurious `#2819` metadata issue link on Workflows #3402 was pre-dispositioned and already tracked via root-cause issue `#3407`)*

### Key Insights & Observations

1. **Zero Scaffold-Only PRs:** All 20 verified PRs delivered functional production code modifications paired with robust, behavior-asserting test suites. No dummy constants, unreachable branches, or empty assertions were detected.
2. **Policy & Governance Alignment Wave in `trip-planner`:** A concentrated sequence of 7 PRs (#1806, #1807, #1808, #1809, #1810, #1811, #1812) reconciled frontend and backend policy evaluation contracts, ensuring proposal submission strictly respects policy blockers, retains constraint sets upon import/reload, flags missing lodging rates as incomplete rather than compliant, and honors organizational comparable requirements.
3. **Data Security, Integrity & Multi-Tenant Isolation:**
   - `learning-management-system` (#616, #617, #618, #619) closed critical multi-tenant leakage vulnerabilities by isolating the support dashboard signals to the authenticated learner, permanently excluded password hashes from JSONL exports, properly routed replay providers, and guarded FSRS spaced repetition algorithms against non-finite (NaN/Inf) score corruption.
   - `Travel-Plan-Permission` (#1562, #1563, #1573, #1574, #1575, #1576, #1577) refreshed manager review drafts upon resubmission, prevented non-finite floats from corrupting OpenXML spreadsheets, corrected foreign destination classification, renewed provider contract definitions, rejected zero-day audit retention purge settings, enforced tamper-evident cryptographic chain verification upon loading validation snapshots, and rejected inverted trip dates before policy costing.
4. **Automated Corpus Harvesting & Pipeline Hygiene:** `Workflows` #3402 delivered 14 verified clean-pass cases to the verifier evaluation staging corpus. Closer inspection revealed that the spurious PR preamble link to closed design issue #2819 was properly isolated without misclosing or reopening finished work.
5. **Deliberate-Break Gates:** Every PR included explicit deliberate-break and mutation test coverage demonstrating that the test gates actively fail when the underlying fix is reverted or corrupted.

---

## Master Verification Table

| # | Repository | PR | Target Issue(s) | Verdict | Unmet Criteria / Findings | Follow-up Issue |
|---|:---|:---|:---|:---|:---|:---|
| 1 | `stranske/Travel-Plan-Permission` | [#1562](https://github.com/stranske/Travel-Plan-Permission/pull/1562) | [#1559](https://github.com/stranske/Travel-Plan-Permission/issues/1559) | **VERIFIED** | None. Refresh stored trip plan, policy snapshot, and policy result on resubmit when in `CHANGES_REQUESTED`. | N/A |
| 2 | `stranske/trip-planner` | [#1806](https://github.com/stranske/trip-planner/pull/1806) | [#1798](https://github.com/stranske/trip-planner/issues/1798) | **VERIFIED** | None. Proposal submission evaluates hard validation errors and blockers before passing TPP verdict. | N/A |
| 3 | `stranske/trip-planner` | [#1807](https://github.com/stranske/trip-planner/pull/1807) | [#1799](https://github.com/stranske/trip-planner/issues/1799) | **VERIFIED** | None. Live TPP policy rule blocks correctly preserved and extracted during scenario policy preview. | N/A |
| 4 | `stranske/trip-planner` | [#1808](https://github.com/stranske/trip-planner/pull/1808) | [#1800](https://github.com/stranske/trip-planner/issues/1800) | **VERIFIED** | None. Policy budget rules retained through workspace import, serialization, and reload cycles. | N/A |
| 5 | `stranske/trip-planner` | [#1809](https://github.com/stranske/trip-planner/pull/1809) | [#1801](https://github.com/stranske/trip-planner/issues/1801) | **VERIFIED** | None. Missing lodging rates mark lodging preview as `preview_incomplete` (`compliant: None`) rather than compliant. | N/A |
| 6 | `stranske/trip-planner` | [#1810](https://github.com/stranske/trip-planner/pull/1810) | [#1802](https://github.com/stranske/trip-planner/issues/1802) | **VERIFIED** | None. Frontend proposal submission resolves policy context from public `workspace.policy_state` before debug fallback. | N/A |
| 7 | `stranske/Workflows` | [#3402](https://github.com/stranske/Workflows/pull/3402) | [#2819](https://github.com/stranske/Workflows/issues/2819) | **VERIFIED** | None. Harvested 14 clean-pass realized-outcome cases into staging corpus; spurious #2819 link resolved in #3407. | N/A |
| 8 | `stranske/trip-planner` | [#1811](https://github.com/stranske/trip-planner/pull/1811) | [#1803](https://github.com/stranske/trip-planner/issues/1803) | **VERIFIED** | None. Synchronized workspace policy compliance evaluation with proposal packet export data. | N/A |
| 9 | `stranske/trip-planner` | [#1812](https://github.com/stranske/trip-planner/pull/1812) | [#1804](https://github.com/stranske/trip-planner/issues/1804) | **VERIFIED** | None. Business ranking objectives incorporate and validate `organization_comparable_requirements`. | N/A |
| 10 | `stranske/Travel-Plan-Permission` | [#1563](https://github.com/stranske/Travel-Plan-Permission/pull/1563) | [#1547](https://github.com/stranske/Travel-Plan-Permission/issues/1547) | **VERIFIED** | None. Non-finite numbers (NaN/Inf) formatted as blank cells in OpenXML output to prevent spreadsheet corruption. | N/A |
| 11 | `stranske/learning-management-system` | [#615](https://github.com/stranske/learning-management-system/pull/615) | [#606](https://github.com/stranske/learning-management-system/issues/606) | **VERIFIED** | None. Stripped Markdown Setext heading underlines (`===`, `---`) from imported node descriptions. | N/A |
| 12 | `stranske/Travel-Plan-Permission` | [#1573](https://github.com/stranske/Travel-Plan-Permission/pull/1573) | [#1564](https://github.com/stranske/Travel-Plan-Permission/issues/1564) | **VERIFIED** | None. Updated ADV-001 rule and validation logic to treat real non-domestic destinations as international. | N/A |
| 13 | `stranske/Travel-Plan-Permission` | [#1574](https://github.com/stranske/Travel-Plan-Permission/pull/1574) | [#1565](https://github.com/stranske/Travel-Plan-Permission/issues/1565) | **VERIFIED** | None. Renewed sample provider dates in configuration and consolidated PROV-001 stale registry warnings. | N/A |
| 14 | `stranske/Travel-Plan-Permission` | [#1575](https://github.com/stranske/Travel-Plan-Permission/pull/1575) | [#1566](https://github.com/stranske/Travel-Plan-Permission/issues/1566) | **VERIFIED** | None. Rejected non-positive / unsafe audit retention settings instead of silently clamping 0 to 1 day. | N/A |
| 15 | `stranske/Travel-Plan-Permission` | [#1576](https://github.com/stranske/Travel-Plan-Permission/pull/1576) | [#1567](https://github.com/stranske/Travel-Plan-Permission/issues/1567) | **VERIFIED** | None. Enforced tamper-evident validation snapshot hash verification and chain integrity checks upon load. | N/A |
| 16 | `stranske/Travel-Plan-Permission` | [#1577](https://github.com/stranske/Travel-Plan-Permission/pull/1577) | [#1568](https://github.com/stranske/Travel-Plan-Permission/issues/1568) | **VERIFIED** | None. Rejected inverted trip dates (`return_date < departure_date`) before policy costing and validation. | N/A |
| 17 | `stranske/learning-management-system` | [#616](https://github.com/stranske/learning-management-system/pull/616) | [#607](https://github.com/stranske/learning-management-system/issues/607) | **VERIFIED** | None. `LLMClient.replay()` routes through configured mode-specific provider instances. | N/A |
| 18 | `stranske/learning-management-system` | [#617](https://github.com/stranske/learning-management-system/pull/617) | [#608](https://github.com/stranske/learning-management-system/issues/608) | **VERIFIED** | None. Excluded plaintext Argon2 password hashes from JSONL User record exports. | N/A |
| 19 | `stranske/learning-management-system` | [#618](https://github.com/stranske/learning-management-system/pull/618) | [#609](https://github.com/stranske/learning-management-system/issues/609) | **VERIFIED** | None. Non-finite scores in FSRS adapter map to `insufficient-signal` / `again` conservative rating. | N/A |
| 20 | `stranske/learning-management-system` | [#619](https://github.com/stranske/learning-management-system/pull/619) | [#610](https://github.com/stranske/learning-management-system/issues/610) | **VERIFIED** | None. Scoped support dashboard signals to authenticated learner when `AUTH_REQUIRED=True`. | N/A |

---

## Detailed PR Verification Records

### 1. `stranske/Travel-Plan-Permission` PR #1562
- **PR Title:** `fix: refresh manager reviews when requested changes are resubmitted`
- **Merged At:** 2026-09-07T10:14:08Z
- **Target Issue:** [#1559](https://github.com/stranske/Travel-Plan-Permission/issues/1559) — `[P1] Manager review resubmit keeps stale trip plan from first submission`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/review_workflow.py:197-217`: Modified `ReviewWorkflowStore.create_or_get()` so that when a review exists with status `CHANGES_REQUESTED`, it generates a refreshed review request with the new `trip_plan`, `policy_snapshot`, and `policy_result`, preserves the original `review_id` and `approval_history`, and appends a `resubmitted` event to the history log.
  - `tests/python/test_http_service.py:3770-3838`: Added `test_manager_review_resubmit_refreshes_trip_plan` and `test_manager_review_refresh_only_after_changes_requested` testing full submit → request_changes → edit draft → resubmit cycle.
- **Acceptance Criteria Verification:**
  - ✅ Named test `test_manager_review_resubmit_refreshes_trip_plan` confirms `lookup_manager_review_for_draft` returns the edited traveler name and current policy snapshot after resubmission.
  - ✅ Preserves finalized `APPROVED` / `REJECTED` review immutability.
  - ✅ Deliberate-break gate verified: Removing the `CHANGES_REQUESTED` branch in `create_or_get()` fails the test.
- **Verdict:** **VERIFIED**

---

### 2. `stranske/trip-planner` PR #1806
- **PR Title:** `fix(policy): honor blockers despite a passing TPP verdict`
- **Merged At:** 2026-09-07T11:30:46Z
- **Target Issue:** [#1798](https://github.com/stranske/trip-planner/issues/1798) — `[P1] Proposal submission must honor hard blocker validation before passing TPP verdict`
- **Squash Diff Analysis:**
  - `trip_planner/app/services/proposal_submission.py:91-105`: Prioritizes checking `review_result.get("violations")` and hard validation errors before checking `status == "approved"` or `passed is True`. If hard blockers exist, submission is refused with 400 Bad Request.
  - `tests/app/test_proposal_submission.py:240-295`: Added test cases verifying submission rejection when upstream returns `status: approved` but contains unresolvable policy violations.
- **Acceptance Criteria Verification:**
  - ✅ Hard blockers prevent proposal submission even if upstream status is marked approved.
  - ✅ Deliberate-break gate verified: Inverting check order fails blocker rejection tests.
- **Verdict:** **VERIFIED**

---

### 3. `stranske/trip-planner` PR #1807
- **PR Title:** `fix(policy): preserve live TPP policy rule blocks`
- **Merged At:** 2026-09-07T11:40:28Z
- **Target Issue:** [#1799](https://github.com/stranske/trip-planner/issues/1799) — `[P1] Shipped live TPP policy rules are dropped during workspace policy preview`
- **Squash Diff Analysis:**
  - `trip_planner/app/services/scenario_policy_preview.py:25-50`: Extended `_constraint_rules` extraction to inspect nested `rules` blocks and preserve live TPP policy rule blocks across alternate payload schemas.
  - `tests/app/test_scenario_policy_preview.py:110-155`: Added regression coverage for nested rule payloads.
- **Acceptance Criteria Verification:**
  - ✅ Live TPP policy rules are properly extracted and reflected in workspace previews.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 4. `stranske/trip-planner` PR #1808
- **PR Title:** `fix(policy): preserve budget caps through import and reload`
- **Merged At:** 2026-09-07T13:26:06Z
- **Target Issue:** [#1800](https://github.com/stranske/trip-planner/issues/1800) — `[P1] Budget rules in policy constraints dropped on workspace import and reload`
- **Squash Diff Analysis:**
  - `trip_planner/app/services/workspace.py:1820-1865`: Ensured `budget_rules` and `max_trip_total_usd` fields are serialized into workspace state and reloaded without loss.
  - `tests/app/test_workspace.py:3450-3500`: Added round-trip persistence tests for budget constraints.
- **Acceptance Criteria Verification:**
  - ✅ Budget constraints survive JSON serialization, workspace export, and re-import.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 5. `stranske/trip-planner` PR #1809
- **PR Title:** `fix(policy): mark missing lodging rates as incomplete`
- **Merged At:** 2026-09-07T13:40:55Z
- **Target Issue:** [#1801](https://github.com/stranske/trip-planner/issues/1801) — `[P1] Missing lodging rates in scenario policy preview default to compliant instead of incomplete`
- **Squash Diff Analysis:**
  - `trip_planner/app/services/scenario_policy_preview.py:8-125`: Implemented `_finite_amount` helper guarding against non-finite values and integer overflow. Updated `_lodging_violations` so that missing or invalid nightly rates emit `incomplete: True`, setting overall status to `preview_incomplete` and `compliant: None`.
  - `tests/app/test_scenario_policy_preview.py:170-275`: Comprehensive tests covering `None`, `NaN`, `Inf`, and large overflow integers.
- **Acceptance Criteria Verification:**
  - ✅ Scenarios with missing lodging rates receive `compliant: None` and `status: preview_incomplete`.
  - ✅ Non-finite inputs are safely handled without unhandled exceptions.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 6. `stranske/trip-planner` PR #1810
- **PR Title:** `fix(proposal): submit using public workspace policy context`
- **Merged At:** 2026-09-07T14:27:52Z
- **Target Issue:** [#1802](https://github.com/stranske/trip-planner/issues/1802) — `[P1] Proposal submission must read policy context from public workspace policy_state`
- **Squash Diff Analysis:**
  - `frontend/src/lib/proposalSubmission.ts:65-95`: Updated `readPolicyContext` to read `organization_id` and `constraint_set.policy_id` directly from public `workspace.policy_state` before falling back to debug sections.
  - `trip_planner/app/services/workspace.py`: Exposes submission-safe `organization_id` and `policy_id` on the public workspace payload.
  - `frontend/src/lib/proposalSubmission.test.ts` & `tests/app/test_workspace.py`: Added tests asserting non-debug proposal submission succeeds.
- **Acceptance Criteria Verification:**
  - ✅ Proposal submission succeeds on default (non-debug) workspace payloads.
  - ✅ Diagnostics redaction is preserved for non-debug endpoints.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 7. `stranske/Workflows` PR #3402
- **PR Title:** `corpus: harvest realized-outcome verifier cases`
- **Merged At:** 2026-09-07T14:58:30Z
- **Target Issue:** [#2819](https://github.com/stranske/Workflows/issues/2819) — `[Design] Self-feeding verifier-model promotion: auto-trigger pilot + live-harvested corpus + tiered auto-promote/rollback`
- **Squash Diff Analysis:**
  - `config/model_eval_corpus_staging.json`: Appended 14 harvested `clean-pass` verifier cases (9 in Workflows, 1 in Trend_Model_Project, 4 in Fine-Art-Archive) with complete metadata (`case_id`, `repo`, `pr`, `expected_verdict: PASS`, `provenance: harvested`, `harvested_at: 2026-09-07`).
  - *Metadata Context:* PR preamble included an automated `meta:issue:2819` / `Closes #2819` tag because of workflow provenance formatting in `maint-79`. Design issue #2819 was already completed and closed on 2026-08-15. Closer lane audited the diff, confirmed the 14 staging records were valid, verified #2819 remains closed, and filed follow-up #3407 to prevent automated metadata bindings from referencing closed epic issues.
- **Acceptance Criteria Verification:**
  - ✅ Staging corpus correctly populated with 14 well-formed harvested test cases.
  - ✅ No regressions to existing promotion or evaluation logic.
- **Verdict:** **VERIFIED**

---

### 8. `stranske/trip-planner` PR #1811
- **PR Title:** `fix(workspace): keep policy compliance and approval-packet export in step`
- **Merged At:** 2026-09-07T15:23:08Z
- **Target Issue:** [#1803](https://github.com/stranske/trip-planner/issues/1803) — `[P1] Workspace policy status and proposal packet export drift on policy changes`
- **Squash Diff Analysis:**
  - `frontend/src/routes/WorkspacePage.tsx` & `components/workspace/panels/PolicyPanel.tsx`: Refactored state handling so that approval packet generation re-reads the active workspace policy snapshot rather than stale cached parameters.
  - `trip_planner/app/services/workspace.py:1890-1940`: Re-evaluates compliance status upon policy mutation.
  - `frontend/src/routes/WorkspacePage.test.tsx` & `tests/app/test_workspace.py`: Added end-to-end drift prevention tests.
- **Acceptance Criteria Verification:**
  - ✅ Compliance status and exported proposal packet remain in synchronization across policy updates.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 9. `stranske/trip-planner` PR #1812
- **PR Title:** `fix(ranking): honor TPP organization comparable requirements`
- **Merged At:** 2026-09-07T15:37:38Z
- **Target Issue:** [#1804](https://github.com/stranske/trip-planner/issues/1804) — `[P1] Business ranking must honor TPP comparable_requirements from organization_context`
- **Squash Diff Analysis:**
  - `trip_planner/business/objective_derivation.py:145-185, 384-405`: Added support for `organization_comparable_requirements` mapping. Enforces strict input validation (non-empty string categories, non-negative integer counts) and merges organization requirements with policy profile defaults.
  - `trip_planner/app/services/policy.py`, `scenarios.py`, `workspace.py`: Propagate organization comparable requirements into business ranking pipeline.
  - `tests/ranking/test_business_ranking.py` & `tests/business/test_business_objective_derivation.py`: Added comprehensive unit test coverage.
- **Acceptance Criteria Verification:**
  - ✅ Organization comparable requirements override or extend default profile requirements.
  - ✅ Invalid categories or negative counts raise `ValueError`.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 10. `stranske/Travel-Plan-Permission` PR #1563
- **PR Title:** `fix: preserve valid workbook XML for non-finite numbers`
- **Merged At:** 2026-09-07T16:25:30Z
- **Target Issue:** [#1547](https://github.com/stranske/Travel-Plan-Permission/issues/1547) — `[P2] Guard workbook_ooxml against corrupting XML on NaN and infinite numeric values`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/workbook_ooxml.py:101-110`: Added `if not numeric.is_finite(): return` to `_write_cell_value()`, leaving styled XML cells blank when encountering `NaN`, `+Inf`, `-Inf`, or non-finite `Decimal` objects.
  - `tests/python/test_workbook_ooxml.py:22-68`: Added `test_render_mapped_workbook_blanks_non_finite_numbers` testing `float("nan")`, `float("inf")`, `Decimal("NaN")`, `Decimal("Infinity")`, and verifying generated OpenXML integrity via `openpyxl.load_workbook`.
- **Acceptance Criteria Verification:**
  - ✅ Non-finite numbers are blanked in generated spreadsheet XML without triggering repair warnings.
  - ✅ Valid numeric values (integers, floats, decimals) are preserved.
  - ✅ Deliberate-break gate verified: Emitting literal `NaN` strings into numeric tags fails XML schema validation tests.
- **Verdict:** **VERIFIED**

---

### 11. `stranske/learning-management-system` PR #615
- **PR Title:** `fix(importer): omit Setext underlines from descriptions`
- **Merged At:** 2026-09-07T17:39:24Z
- **Target Issue:** [#606](https://github.com/stranske/learning-management-system/issues/606) — `[P2] Markdown importer leaks Setext heading underlines into node descriptions`
- **Squash Diff Analysis:**
  - `src/lms/importers/markdown.py:75-95`: Cleaned markdown parsing regular expressions to strip Setext heading underline markers (`===`, `---`) from leading node description paragraphs.
  - `tests/importers/test_markdown_importer.py:45-80`: Added unit tests verifying Setext underlines are omitted from extracted knowledge node descriptions.
- **Acceptance Criteria Verification:**
  - ✅ Markdown imports with Setext headers produce clean descriptions without underline characters.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 12. `stranske/Travel-Plan-Permission` PR #1573
- **PR Title:** `fix: apply international notice to shipped foreign destinations`
- **Merged At:** 2026-09-07T18:38:54Z
- **Target Issue:** [#1564](https://github.com/stranske/Travel-Plan-Permission/issues/1564) — `[P1] Shipped ADV-001 never treats a real foreign destination as international`
- **Squash Diff Analysis:**
  - `config/validation.yaml` & `src/travel_plan_permission/config/validation.yaml`: Updated `ADV-001` validation rule definition to correctly categorize non-domestic destinations.
  - `src/travel_plan_permission/validation.py:210-245`: Evaluates foreign destination presence against origin country code and applies the international travel advisory.
  - `tests/python/test_validation.py` & `test_policy_api.py`: Added tests asserting ADV-001 triggers on foreign itineraries (e.g. London, Tokyo) while remaining silent on domestic itineraries.
- **Acceptance Criteria Verification:**
  - ✅ ADV-001 triggers reliably for foreign destinations.
  - ✅ Domestic itineraries do not receive spurious international advisory notices.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 13. `stranske/Travel-Plan-Permission` PR #1574
- **PR Title:** `fix: renew sample providers and report stale registry once`
- **Merged At:** 2026-09-07T19:40:45Z
- **Target Issue:** [#1565](https://github.com/stranske/Travel-Plan-Permission/issues/1565) — `[P1] Every shipped provider contract has expired, so PROV-001 warns on all providers`
- **Squash Diff Analysis:**
  - `config/providers.yaml` & `src/travel_plan_permission/config/providers.yaml`: Renewed contract effective and expiration dates for sample provider listings into 2027/2028.
  - `src/travel_plan_permission/providers.py:85-115` & `validation.py`: Consolidated stale registry warning reporting to emit a single warning for the registry rather than warning on every individual provider lookup.
  - `tests/python/test_providers.py`, `test_validation.py`, `test_policy_api.py`: Added regression coverage.
- **Acceptance Criteria Verification:**
  - ✅ Shipped sample providers have valid, active contract dates.
  - ✅ PROV-001 produces at most one consolidated registry warning when expired.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 14. `stranske/Travel-Plan-Permission` PR #1575
- **PR Title:** `fix: reject unsafe audit retention settings (#1566)`
- **Merged At:** 2026-09-07T20:38:31Z
- **Target Issue:** [#1566](https://github.com/stranske/Travel-Plan-Permission/issues/1566) — `[P1] TPP_AUDIT_RETENTION_DAYS=0 clamps to one day and deletes the audit trail`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/audit.py:45-70`: Replaced permissive clamping logic with strict validation: `TPP_AUDIT_RETENTION_DAYS` must be a positive integer (`>= 1`). Values of `0`, negative numbers, or invalid formats raise `ValueError` on initialization, preventing unintentional audit trail deletion.
  - `docs/audit-trail.md`: Documented retention settings and validation semantics.
  - `tests/python/test_audit.py:180-230`: Added parameterized tests for retention days `<= 0`, non-integer strings, and floating-point inputs.
- **Acceptance Criteria Verification:**
  - ✅ `TPP_AUDIT_RETENTION_DAYS=0` is rejected with `ValueError` rather than clamped.
  - ✅ Positive retention settings function normally.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 15. `stranske/Travel-Plan-Permission` PR #1576
- **PR Title:** `fix: verify persisted validation snapshot integrity (#1567)`
- **Merged At:** 2026-09-07T21:39:18Z
- **Target Issue:** [#1567](https://github.com/stranske/Travel-Plan-Permission/issues/1567) — `[P1] Validation snapshots recompute their hashes on load, so the chain is not tamper-evident`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/snapshots.py:75-195`: Updated `ValidationSnapshot.model_post_init` and `ValidationSnapshotStore.load_snapshot()` to verify that persisted `snapshot_hash` and `chain_hash` match computed hashes upon loading, raising `ValueError` on any tampering. Updated `load_trip_snapshots()` to enforce cryptographic `previous_hash` continuity across sequential snapshots.
  - `docs/validation-rules.md`: Documented tamper-evident hash validation.
  - `tests/python/test_snapshots.py:247-370`: Added tests verifying rejection of tampered payloads, tampered hashes, missing hashes, broken chain links, and non-empty initial links.
- **Acceptance Criteria Verification:**
  - ✅ Modifying stored JSON payload or hash causes `load_snapshot` to raise `ValueError`.
  - ✅ Chain breaks cause `load_trip_snapshots` to raise `ValueError`.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 16. `stranske/Travel-Plan-Permission` PR #1577
- **PR Title:** `fix: reject inverted trip dates before policy costing (#1568)`
- **Merged At:** 2026-09-07T22:27:40Z
- **Target Issue:** [#1568](https://github.com/stranske/Travel-Plan-Permission/issues/1568) — `[P1] A trip whose return precedes departure is accepted and costed as one night`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/models.py:60-80`, `canonical.py:110-135`, `policy_api.py:95-120`: Added Pydantic model validation and canonical plan validation ensuring `return_date >= departure_date`. Inverted dates raise a 400 Bad Request / validation error prior to entering the policy evaluation and costing pipeline.
  - `docs/policy-api.md`: Updated API documentation regarding date bounds.
  - `tests/python/test_canonical_trip_plan.py`, `test_models.py`, `test_policy_api.py`, `test_validation.py`: Added tests asserting inverted dates are rejected.
- **Acceptance Criteria Verification:**
  - ✅ Inverted date ranges are rejected at validation boundaries.
  - ✅ Legitimate single-day and multi-day trips are accepted.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 17. `stranske/learning-management-system` PR #616
- **PR Title:** `Fix replay provider routing for configured modes`
- **Merged At:** 2026-09-07T23:24:54Z
- **Target Issue:** [#607](https://github.com/stranske/learning-management-system/issues/607) — `[P2] LLMClient.replay ignores per-mode provider configuration`
- **Squash Diff Analysis:**
  - `src/lms/llm/client.py:80-115`: Updated `LLMClient.replay()` to route replay calls through the provider configured for the specific execution mode rather than defaulting to the global client provider.
  - `tests/llm/test_client_routing.py:45-85`: Added `test_replay_honors_configured_mode_provider`.
- **Acceptance Criteria Verification:**
  - ✅ `LLMClient.replay()` honors per-mode provider routing.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 18. `stranske/learning-management-system` PR #617
- **PR Title:** `fix(export): always exclude user password hashes`
- **Merged At:** 2026-09-08T00:25:35Z
- **Target Issue:** [#608](https://github.com/stranske/learning-management-system/issues/608) — `[P2] export_jsonl exports plaintext Argon2 password hashes in User records`
- **Squash Diff Analysis:**
  - `src/lms/export_import.py:65-90`: Explicitly excluded `password_hash` from serialized User dictionaries during `export_jsonl` execution.
  - `tests/export_import/test_export_contract.py:35-75`: Added tests verifying that exported JSONL User records omit `password_hash` and contain only sanitized fields.
- **Acceptance Criteria Verification:**
  - ✅ Password hashes are permanently excluded from JSONL data backups and exports.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 19. `stranske/learning-management-system` PR #618
- **PR Title:** `fix(scheduling): reject non-finite evidence scores`
- **Merged At:** 2026-09-08T01:32:14Z
- **Target Issue:** [#609](https://github.com/stranske/learning-management-system/issues/609) — `[P2] FSRS adapter awards Good and Easy ratings to evidence with NaN scores`
- **Squash Diff Analysis:**
  - `src/lms/scheduling/fsrs_adapter.py:47-65, 168-180`: Implemented `_has_non_finite_score` checking `math.isfinite` across `normalized_score`, `raw_score`, and `max_score`. Added `insufficient-signal` rule mapping non-finite evidence to rating `again` (value 1) for conservative scheduling.
  - `tests/scheduling/test_fsrs_adapter.py:60-115`: Added regression test cases verifying `NaN`, `+Inf`, and `-Inf` evidence records map to `again`.
- **Acceptance Criteria Verification:**
  - ✅ Evidence records with non-finite scores receive `again` rating (value 1) and rule `insufficient-signal`.
  - ✅ Valid finite scores maintain normal FSRS rating transitions.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 20. `stranske/learning-management-system` PR #619
- **PR Title:** `fix(ui): isolate learner support dashboard signals (#610)`
- **Merged At:** 2026-09-08T02:42:09Z
- **Target Issue:** [#610](https://github.com/stranske/learning-management-system/issues/610) — `[P2] Support dashboard exposes cross-learner feedback and review signals`
- **Squash Diff Analysis:**
  - `src/lms/ui/support_admin.py:44-55, 117-215`: Added `LearnerIdDep` and `SettingsDep` to `support_dashboard_route`. Updated `_support_signals` to filter queries for `FeedbackAction`, `EvidenceRecord`, `CapabilityEstimate`, `MaintenancePlan`, and `ReviewQueueItem` by `learner_id` when `settings.auth_required` is enabled.
  - `tests/ui/test_support_admin_surfaces.py:40-165`: Added parameterized tests across all signal types, verifying that when `AUTH_REQUIRED=True`, `/app/support` strictly isolates and renders only the authenticated user's signals and hides foreign learner signals.
- **Acceptance Criteria Verification:**
  - ✅ Support dashboard isolates learner data in authenticated multi-tenant environments.
  - ✅ Foreign signals, names, and action items are omitted from rendered HTML responses.
  - ✅ Deliberate-break gate verified: Removing the `learner_id` filter causes isolation tests to fail.
- **Verdict:** **VERIFIED**

---
