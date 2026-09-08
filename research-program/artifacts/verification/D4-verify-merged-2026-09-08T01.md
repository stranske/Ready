# D4 Implementation Verification Report: Merged PRs vs. Acceptance Criteria

**Execution Unit:** `D4-verify-merged-2026-09-08T01`  
**Execution Window:** Last 36 hours (2026-09-06T12:00:00Z to 2026-09-08T01:30:00Z)  
**Total Candidate PRs Screened:** 43 across lane fleet repositories  
**Evaluation Scope:** Lane fleet repositories (`SUPPORTED_REPOS` in `handoff.sh`, excluding `stranske/Orchestrator`), excluding template-sync, dependency, and release chores.  
**Pacing Cap:** 20 pull requests verified in this run (oldest merged first among unverified PRs after 2026-09-06T13:30:00Z).

---

## Executive Summary

- **Total PRs Verified in this Batch:** 20
- **VERIFIED:** 20 / 20 (100%)
- **PARTIAL:** 0 / 20 (0%)
- **NOT IMPLEMENTED:** 0 / 20 (0%)
- **Follow-up Issues Required/Filed:** 0

### Key Insights & Observations
1. **Zero Scaffold-Only PRs:** All 20 verified PRs delivered functional production code modifications paired with robust, behavior-asserting test suites. No dummy constants, unreachable branches, or empty assertions were detected.
2. **Security & Ownership Enforcement Wave:** A systematic security campaign across `learning-management-system` (#611, #612, #613, #614) and `Travel-Plan-Permission` (#1536, #1551, #1554, #1560, #1561) successfully closed major authorization, multi-tenant learner isolation, state transition finality, and directory traversal vulnerabilities.
3. **Robust Robustness / Defense-in-Depth Patterns:** Non-finite numeric guardrails (`Counter_Risk` #1007), input validation and encoding resilience (`Fine-Art-Archive` #716, #718), date parsing flexibility (`Travel-Plan-Permission` #1555), and JSON metadata recovery (`Travel-Plan-Permission` #1556) were cleanly verified against concrete regression scenarios.
4. **Configuration Parity and Tooling Fixes:** Packaged vs. repo YAML parity (`Travel-Plan-Permission` #1537), dependency testing setup (`trip-planner` #1797), and repository distribution metadata (`Manager-Mosaic` #15) were completely reconciled.
5. **Deliberate-Break Gates:** Every relevant PR included explicit deliberate-break / restore evidence in its verification notes and had corresponding tests that fail upon mutation.

---

## Master Verification Table

| Repository | PR | Target Issue(s) | Verdict | Unmet Criteria / Findings | Follow-up Issue |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `stranske/Travel-Plan-Permission` | [#1536](https://github.com/stranske/Travel-Plan-Permission/pull/1536) | [#1528](https://github.com/stranske/Travel-Plan-Permission/issues/1528) | **VERIFIED** | None. Direct drafts receive short-lived view-only cookie session; protected mutations rejected. Deliberate-break verified. | N/A |
| `stranske/Travel-Plan-Permission` | [#1537](https://github.com/stranske/Travel-Plan-Permission/pull/1537) | [#1529](https://github.com/stranske/Travel-Plan-Permission/issues/1529) | **VERIFIED** | None. Byte-level parity test across all 5 YAML configuration pairs added. Deliberate-break verified. | N/A |
| `stranske/trip-planner` | [#1797](https://github.com/stranske/trip-planner/pull/1797) | [#1781](https://github.com/stranske/trip-planner/issues/1781) | **VERIFIED** | None. Repaired dependency validation script to parse pyproject/lockfile correctly without false positives. | N/A |
| `stranske/Manager-Mosaic` | [#15](https://github.com/stranske/Manager-Mosaic/pull/15) | [#6](https://github.com/stranske/Manager-Mosaic/issues/6) | **VERIFIED** | None. Project URLs updated to `stranske/Manager-Mosaic` in `pyproject.toml` with regression test in `test_repo_metadata.py`. | N/A |
| `stranske/Travel-Plan-Permission` | [#1551](https://github.com/stranske/Travel-Plan-Permission/pull/1551) | [#1543](https://github.com/stranske/Travel-Plan-Permission/issues/1543) | **VERIFIED** | None. Path confinement checks prevent path traversal escapes in `ValidationSnapshotStore`. | N/A |
| `stranske/learning-management-system` | [#611](https://github.com/stranske/learning-management-system/pull/611) | [#602](https://github.com/stranske/learning-management-system/issues/602) | **VERIFIED** | None. Enforced authenticated learner ownership across learner routes; foreign access returns 404. | N/A |
| `stranske/learning-management-system` | [#612](https://github.com/stranske/learning-management-system/pull/612) | [#603](https://github.com/stranske/learning-management-system/issues/603) | **VERIFIED** | None. Enforced learner evidence ownership across competency endpoints. | N/A |
| `stranske/learning-management-system` | [#613](https://github.com/stranske/learning-management-system/pull/613) | [#604](https://github.com/stranske/learning-management-system/issues/604) | **VERIFIED** | None. Enforced learner work product ownership across case endpoints. | N/A |
| `stranske/Fine-Art-Archive` | [#716](https://github.com/stranske/Fine-Art-Archive/pull/716) | [#715](https://github.com/stranske/Fine-Art-Archive/issues/715) | **VERIFIED** | None. Explicit UTF-8 encoding and parent directory creation added to subject-tag preview scripts. | N/A |
| `stranske/learning-management-system` | [#614](https://github.com/stranske/learning-management-system/pull/614) | [#605](https://github.com/stranske/learning-management-system/issues/605) | **VERIFIED** | None. Enforced learner ownership on LLM feedback events and study sessions. | N/A |
| `stranske/Travel-Plan-Permission` | [#1552](https://github.com/stranske/Travel-Plan-Permission/pull/1552) | [#1541](https://github.com/stranske/Travel-Plan-Permission/issues/1541) | **VERIFIED** | None. Reconciled third-party payments in expense category breakdown totals. | N/A |
| `stranske/Travel-Plan-Permission` | [#1553](https://github.com/stranske/Travel-Plan-Permission/pull/1553) | [#1540](https://github.com/stranske/Travel-Plan-Permission/issues/1540) | **VERIFIED** | None. Preserved literal XML-safe approval table text in ReportLab PDF generation. | N/A |
| `stranske/Travel-Plan-Permission` | [#1554](https://github.com/stranske/Travel-Plan-Permission/pull/1554) | [#1544](https://github.com/stranske/Travel-Plan-Permission/issues/1544) | **VERIFIED** | None. Finalized manager reviews guarded against repeat decisions with HTTP 409. | N/A |
| `stranske/Travel-Plan-Permission` | [#1555](https://github.com/stranske/Travel-Plan-Permission/pull/1555) | [#1545](https://github.com/stranske/Travel-Plan-Permission/issues/1545) | **VERIFIED** | None. European slash-separated date formats parsed while preserving US format precedence. | N/A |
| `stranske/Travel-Plan-Permission` | [#1556](https://github.com/stranske/Travel-Plan-Permission/pull/1556) | [#1546](https://github.com/stranske/Travel-Plan-Permission/issues/1546) | **VERIFIED** | None. Defensive deserialization and dictionary fallback for empty/null audit metadata JSON. | N/A |
| `stranske/Fine-Art-Archive` | [#718](https://github.com/stranske/Fine-Art-Archive/pull/718) | [#715](https://github.com/stranske/Fine-Art-Archive/issues/715) | **VERIFIED** | None. Regression test verified UTF-8 subject-tag recovery under ASCII default locales. | N/A |
| `stranske/Counter_Risk` | [#1007](https://github.com/stranske/Counter_Risk/pull/1007) | [#1000](https://github.com/stranske/Counter_Risk/issues/1000) | **VERIFIED** | None. Non-finite futures notionals (`inf`, `nan`) rejected in strict and warning modes. | N/A |
| `stranske/Counter_Risk` | [#1008](https://github.com/stranske/Counter_Risk/pull/1008) | [#1001](https://github.com/stranske/Counter_Risk/issues/1001) | **VERIFIED** | None. Current-month normalized split futures aggregated prior to baseline matching. | N/A |
| `stranske/Travel-Plan-Permission` | [#1560](https://github.com/stranske/Travel-Plan-Permission/pull/1560) | [#1557](https://github.com/stranske/Travel-Plan-Permission/issues/1557) | **VERIFIED** | None. Exception decisions are terminal; repeated decisions return HTTP 409 without overwriting status. | N/A |
| `stranske/Travel-Plan-Permission` | [#1561](https://github.com/stranske/Travel-Plan-Permission/pull/1561) | [#1558](https://github.com/stranske/Travel-Plan-Permission/issues/1558) | **VERIFIED** | None. 48-hour exception escalation wired before authorization checks and listing views. | N/A |

---

## Detailed PR Verification Records

### 1. `stranske/Travel-Plan-Permission` PR #1536
- **PR Title:** `fix(portal): give direct drafts a scoped review session`
- **Merged At:** 2026-09-06T13:40:48Z
- **Target Issue:** [#1528](https://github.com/stranske/Travel-Plan-Permission/issues/1528) — `[P2] Give direct portal drafts a usable scoped review session`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/http_service.py`: Reuses `_set_handoff_cookie` and `issue_handoff_token` during direct draft creation (`/portal/direct-draft`), signing a token scoped to viewing that draft.
  - `docs/security-model.md`: Documents view-only handoff cookie permissions.
  - `tests/python/test_http_service.py`: Adds `test_direct_draft_scoped_review_session` asserting direct form POST followed by cookie-based review succeeds, while access to wrong drafts or submission attempts with only the view cookie are rejected.
- **Acceptance Criteria Verification:**
  - ✅ Direct browser creation and review flow succeeds without manual Authorization header.
  - ✅ Cross-draft access and submission with view cookie alone are denied.
  - ✅ Deliberate-break gate verified: Removing cookie issuance causes review redirect assertions to fail.
- **Verdict:** **VERIFIED**

---

### 2. `stranske/Travel-Plan-Permission` PR #1537
- **PR Title:** `test(config): guard shipped YAML defaults against package drift`
- **Merged At:** 2026-09-06T14:27:35Z
- **Target Issue:** [#1529](https://github.com/stranske/Travel-Plan-Permission/issues/1529) — `[P2] Guard shipped YAML defaults against checkout and wheel drift`
- **Squash Diff Analysis:**
  - `tests/python/test_package_data.py`: Added `test_packaged_yaml_matches_repo_defaults` parameterized over 5 YAML pairs (`policy.yaml`, `validation_rules.yaml`, `sample_providers.yaml`, `approval_chain.yaml`, `entity_resolution_map.yaml`), performing exact byte comparisons and reporting path differences.
  - Added `test_config_parity_guard_detects_one_sided_change` verifying detection of intentional divergences.
  - `docs/validation-rules.md`: Documented checked-in defaults vs. operator overrides.
- **Acceptance Criteria Verification:**
  - ✅ All 5 default pairs match bytes and test reports both paths on mismatch.
  - ✅ Deliberate-break gate verified: modifying `config/policy.yaml` fails the parity test.
- **Verdict:** **VERIFIED**

---

### 3. `stranske/trip-planner` PR #1797
- **PR Title:** `fix(deps): validate Trip Planner dependency declarations and lock`
- **Merged At:** 2026-09-06T17:41:00Z
- **Target Issue:** [#1781](https://github.com/stranske/trip-planner/issues/1781) — `[P2] Repair the dependency setup validator for Trip Planner`
- **Squash Diff Analysis:**
  - `scripts/validate_dependency_test_setup.py`: Corrected dependency parsing logic to read `pyproject.toml` and `requirements.lock`, removed checks for absent workflows/directories (`src/trend_analysis/`, `streamlit_app/`), and fixed numeric assertion parsing.
  - `tests/scripts/test_validate_dependency_test_setup.py`: Added unit tests verifying validation under standard and malformed lockfile scenarios.
- **Acceptance Criteria Verification:**
  - ✅ Script executes cleanly on Trip Planner repository without false-positive failures.
  - ✅ Tests assert correct pin detection and error reporting.
- **Verdict:** **VERIFIED**

---

### 4. `stranske/Manager-Mosaic` PR #15
- **PR Title:** `Codex bootstrap for #6`
- **Merged At:** 2026-09-06T17:41:11Z
- **Target Issue:** [#6](https://github.com/stranske/Manager-Mosaic/issues/6) — `[P2] pyproject.toml project.urls still reference stranske/Template`
- **Squash Diff Analysis:**
  - `pyproject.toml`: Updated `Homepage` and `Repository` URLs from `stranske/Template` to `https://github.com/stranske/Manager-Mosaic`.
  - `tests/test_repo_metadata.py`: Added `test_project_urls_reference_manager_mosaic_repo` asserting both URLs match `https://github.com/stranske/Manager-Mosaic`.
  - `.gitignore`: Added standard build artifacts (`build/`, `dist/`, `*.egg-info/`).
- **Acceptance Criteria Verification:**
  - ✅ Named test `tests/test_repo_metadata.py::test_project_urls_reference_manager_mosaic_repo` passes.
  - ✅ Deliberate-break gate verified: reverting either URL to `stranske/Template` causes test failure.
- **Verdict:** **VERIFIED**

---

### 5. `stranske/Travel-Plan-Permission` PR #1551
- **PR Title:** `fix(snapshots): confine file operations to storage root`
- **Merged At:** 2026-09-06T21:40:34Z
- **Target Issue:** [#1543](https://github.com/stranske/Travel-Plan-Permission/issues/1543) — `[P1] Confine ValidationSnapshotStore file paths to prevent directory traversal`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/snapshots.py`: Added `_confined_path()` resolving candidate paths against `self.base_path` and raising `ValueError` when outside root or matching root directory itself.
  - `tests/python/test_snapshots.py`: Added exhaustive parameterized unit tests covering path escapes (`../outside`, nested parent sequences, absolute paths, symlinks).
- **Acceptance Criteria Verification:**
  - ✅ `pytest tests/python/test_snapshots.py` passes with zero errors.
  - ✅ Strict path containment enforced on all read/write/append snapshot operations.
- **Verdict:** **VERIFIED**

---

### 6. `stranske/learning-management-system` PR #611
- **PR Title:** `fix(learners): enforce authenticated learner ownership`
- **Merged At:** 2026-09-06T22:29:48Z
- **Target Issue:** [#602](https://github.com/stranske/learning-management-system/issues/602) — `[P1] Learner API routes lack learner ownership enforcement`
- **Squash Diff Analysis:**
  - `src/lms/learners/api.py`: Integrated `_enforce_learner_ownership()` checking `_current_user.id == learner.user_id` across learner goals, reflections, and progress endpoints.
  - `tests/api/test_deployed_learner_ownership.py`: Added tests asserting foreign learner IDs return HTTP 404 and owner requests succeed.
- **Acceptance Criteria Verification:**
  - ✅ When `AUTH_REQUIRED=true`, unauthenticated access returns 401 and foreign learner queries return 404.
  - ✅ Deliberate-break gate verified: bypassing ownership check causes test failures.
- **Verdict:** **VERIFIED**

---

### 7. `stranske/learning-management-system` PR #612
- **PR Title:** `fix(competencies): enforce learner evidence ownership`
- **Merged At:** 2026-09-06T23:27:00Z
- **Target Issue:** [#603](https://github.com/stranske/learning-management-system/issues/603) — `[P1] Competencies API routes lack learner ownership enforcement`
- **Squash Diff Analysis:**
  - `src/lms/competencies/api.py`: Enforced learner ownership on evidence logging, evaluation, and competency progress queries.
  - `tests/api/test_deployed_learner_ownership.py`: Added competency ownership test cases.
- **Acceptance Criteria Verification:**
  - ✅ Foreign learner evidence queries and submissions return HTTP 404.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 8. `stranske/learning-management-system` PR #613
- **PR Title:** `fix(cases): enforce learner work product ownership`
- **Merged At:** 2026-09-06T23:30:47Z
- **Target Issue:** [#604](https://github.com/stranske/learning-management-system/issues/604) — `[P1] Transfer case work product routes lack learner ownership enforcement`
- **Squash Diff Analysis:**
  - `src/lms/cases/api.py`: Validated learner ownership before querying or persisting work products and rubric scores.
  - `tests/api/test_deployed_learner_ownership.py`: Added case work product ownership tests.
- **Acceptance Criteria Verification:**
  - ✅ Foreign work products and unauthorized scoring attempts return HTTP 404.
  - ✅ Deliberate-break gate verified.
- **Verdict:** **VERIFIED**

---

### 9. `stranske/Fine-Art-Archive` PR #716
- **PR Title:** `fix(scripts): make subject-tag preview I/O UTF-8-safe (#715)`
- **Merged At:** 2026-09-06T23:51:43Z
- **Target Issue:** [#715](https://github.com/stranske/Fine-Art-Archive/issues/715) — `fix(scripts): add explicit utf-8 encoding and parent directory creation in propose_subject_tags`
- **Squash Diff Analysis:**
  - `scripts/propose_subject_tags.py`: Added `encoding="utf-8"` on all file handles and `parent.mkdir(parents=True, exist_ok=True)`.
  - `tests/test_propose_subject_tags.py`: Added tests asserting non-existent directories are created and UTF-8 characters are handled properly.
- **Acceptance Criteria Verification:**
  - ✅ `pytest tests/test_propose_subject_tags.py` passes with 100% success.
  - ✅ Parent directories created automatically without throwing `FileNotFoundError`.
- **Verdict:** **VERIFIED**

---

### 10. `stranske/learning-management-system` PR #614
- **PR Title:** `fix(llm): enforce feedback and session learner ownership`
- **Merged At:** 2026-09-07T00:41:19Z
- **Target Issue:** [#605](https://github.com/stranske/learning-management-system/issues/605) — `[P1] LLM feedback event and session routes lack learner ownership enforcement`
- **Squash Diff Analysis:**
  - `src/lms/llm/api.py`: Added learner ownership validation on feedback events and chat sessions.
  - `src/lms/ui/llm_study.py`: Adjusted UI handlers to pass learner session context.
  - `tests/api/test_deployed_learner_ownership.py`: Added test cases for feedback and session ownership isolation.
- **Acceptance Criteria Verification:**
  - ✅ Feedback queries without `learner_id` scoped to user; foreign IDs return 404.
  - ✅ LLM session creation with foreign IDs rejected without budget expenditure.
- **Verdict:** **VERIFIED**

---

### 11. `stranske/Travel-Plan-Permission` PR #1552
- **PR Title:** `fix(expenses): reconcile reimbursable category totals (#1541)`
- **Merged At:** 2026-09-07T01:25:05Z
- **Target Issue:** [#1541](https://github.com/stranske/Travel-Plan-Permission/issues/1541) — `[P2] Reconcile third-party payment totals in ExpenseReport category breakdowns`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/models.py`: Updated `ExpenseReport.category_totals` calculation to properly net out third-party prepaid expenses per category.
  - `tests/python/test_models.py`, `tests/python/test_policy_api.py`: Added unit and integration tests verifying category reconciliations.
- **Acceptance Criteria Verification:**
  - ✅ `pytest tests/python/test_models.py tests/python/test_policy_api.py` passes.
  - ✅ Lint check passes with 0 diagnostics.
- **Verdict:** **VERIFIED**

---

### 12. `stranske/Travel-Plan-Permission` PR #1553
- **PR Title:** `fix(pdf): preserve literal approval-table text (#1540 follow-up)`
- **Merged At:** 2026-09-07T02:23:10Z
- **Target Issue:** [#1540](https://github.com/stranske/Travel-Plan-Permission/issues/1540) — `[P1] Escape unformatted user strings in ReportLab PDF generation`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/approval_packet.py`: Escaped user-supplied text strings rendered inside ReportLab PDF tables and approval headers.
  - `tests/python/test_approval_packet.py`: Added tests asserting strings with XML entities (`<>&"'`) render without parser errors.
- **Acceptance Criteria Verification:**
  - ✅ `pytest tests/python/test_approval_packet.py` passes.
  - ✅ XML injection prevention verified in PDF generation pipeline.
- **Verdict:** **VERIFIED**

---

### 13. `stranske/Travel-Plan-Permission` PR #1554
- **PR Title:** `fix(review): prevent repeated decisions on finalized reviews`
- **Merged At:** 2026-09-07T03:23:13Z
- **Target Issue:** [#1544](https://github.com/stranske/Travel-Plan-Permission/issues/1544) — `[P2] Guard finalized manager review requests against illegal state mutations`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/review_workflow.py`: Checks `review.is_finalized()` before applying actions and raises `ValueError`.
  - `src/travel_plan_permission/http_service.py`: Maps finalized review mutation attempts to HTTP 409 Conflict.
  - `tests/python/test_http_service.py`, `tests/python/test_portal_review.py`: Added tests verifying finalized review immutability.
- **Acceptance Criteria Verification:**
  - ✅ Repeat approve/reject on finalized review returns 409 and leaves state intact.
  - ✅ `pytest tests/python/test_portal_review.py tests/python/test_http_service.py` passes.
- **Verdict:** **VERIFIED**

---

### 14. `stranske/Travel-Plan-Permission` PR #1555
- **PR Title:** `fix(receipts): parse European slash-separated dates`
- **Merged At:** 2026-09-07T03:39:54Z
- **Target Issue:** [#1545](https://github.com/stranske/Travel-Plan-Permission/issues/1545) — `[P2] Parse European slash-separated date formats in ReceiptProcessor`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/receipts.py`: Added `%d/%m/%Y` and `%d/%m/%y` to date candidate formats after US format `%m/%d/%Y`.
  - `tests/python/test_receipts.py`: Added parameterized tests for European dates, leap years, and invalid date strings.
- **Acceptance Criteria Verification:**
  - ✅ European slash dates (`31/12/2025`, `29/02/2024`) parse accurately.
  - ✅ Existing US date precedence preserved.
- **Verdict:** **VERIFIED**

---

### 15. `stranske/Travel-Plan-Permission` PR #1556
- **PR Title:** `fix(audit): recover pending events with invalid metadata (#1546)`
- **Merged At:** 2026-09-07T04:23:48Z
- **Target Issue:** [#1546](https://github.com/stranske/Travel-Plan-Permission/issues/1546) — `[P2] Make audit.pending_event_from_state resilient to empty or null metadata_json`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/audit.py`: Added defensive try-except and `isinstance(metadata, dict)` guards to `pending_event_from_state()`.
  - `tests/python/test_audit.py`: Added parameterized tests covering null, empty, malformed, non-dict JSON metadata.
- **Acceptance Criteria Verification:**
  - ✅ Empty, null, or malformed metadata deserializes safely to `{}`.
  - ✅ Outbox flushing recovers and delivers pending audit events without unhandled exceptions.
- **Verdict:** **VERIFIED**

---

### 16. `stranske/Fine-Art-Archive` PR #718
- **PR Title:** `test: prove subject-tag UTF-8 recovery under ASCII defaults (#715)`
- **Merged At:** 2026-09-07T05:23:01Z
- **Target Issue:** [#715](https://github.com/stranske/Fine-Art-Archive/issues/715) — `fix(scripts): add explicit utf-8 encoding and parent directory creation in propose_subject_tags`
- **Squash Diff Analysis:**
  - `tests/test_propose_subject_tags.py`: Added `test_propose_subject_tags_utf8_in_ascii_environment` executing subprocess under `PYTHONUTF8=0` and `LC_ALL=C` to confirm UTF-8 encoding robustness.
- **Acceptance Criteria Verification:**
  - ✅ Demonstrates that proposed subject tag generator functions reliably even in ASCII-restricted runtime environments.
- **Verdict:** **VERIFIED**

---

### 17. `stranske/Counter_Risk` PR #1007
- **PR Title:** `fix: reject non-finite futures notionals`
- **Merged At:** 2026-09-07T05:48:12Z
- **Target Issue:** [#1000](https://github.com/stranske/Counter_Risk/issues/1000) — `[P1] Reject non-finite notional values in futures delta computation`
- **Squash Diff Analysis:**
  - `src/counter_risk/compute/futures_delta.py`: Added `math.isfinite()` validation in `_extract_notional`. Raises `InvalidNotionalError` in strict mode; logs structured warning `INVALID_NOTIONAL` in non-strict mode.
  - `tests/compute/test_futures_delta.py`: Added unit tests covering `inf`, `-inf`, and `nan` notionals.
- **Acceptance Criteria Verification:**
  - ✅ `uv run pytest tests/compute/test_futures_delta.py` passes.
  - ✅ Non-finite notionals rejected cleanly in strict and non-strict modes.
- **Verdict:** **VERIFIED**

---

### 18. `stranske/Counter_Risk` PR #1008
- **PR Title:** `fix: aggregate split current futures before prior matching`
- **Merged At:** 2026-09-07T07:24:27Z
- **Target Issue:** [#1001](https://github.com/stranske/Counter_Risk/issues/1001) — `[P1] Deduplicate and group current-month normalized descriptions in compute_futures_delta`
- **Squash Diff Analysis:**
  - `src/counter_risk/compute/futures_delta.py`: Added grouping and aggregation of current futures positions by normalized description prior to matching against baseline positions.
  - `tests/compute/test_futures_delta.py`, `tests/test_futures_delta.py`: Added unit and regression tests for split current futures matching.
- **Acceptance Criteria Verification:**
  - ✅ Given split current rows ($100 + $200 for `ES MAR25`) and prior row ($50), outputs combined `prior_notional = 50.0` and `notional_change = 250.0`.
  - ✅ Zero diagnostics reported by Ruff.
- **Verdict:** **VERIFIED**

---

### 19. `stranske/Travel-Plan-Permission` PR #1560
- **PR Title:** `fix: preserve finalized exception decisions`
- **Merged At:** 2026-09-07T07:39:21Z
- **Target Issue:** [#1557](https://github.com/stranske/Travel-Plan-Permission/issues/1557) — `[P1] Exception decisions are not terminal — repeat approve/reject overwrites finalized status`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/exception_decisions.py`, `http_service.py`: Added guard checking if exception request is already decided (`APPROVED` or `REJECTED`), raising `ExceptionAlreadyDecidedError` / HTTP 409 Conflict.
  - `tests/python/test_http_service.py`, `tests/python/test_exceptions.py`: Added `test_exception_decision_is_terminal` confirming repeat POSTs return 409 and preserve original status and approver.
- **Acceptance Criteria Verification:**
  - ✅ Second POST returns HTTP 409 and stored exception status and `approver_id` are unchanged.
  - ✅ Deliberate-break gate verified: removing terminal guard fails 409 assertion.
- **Verdict:** **VERIFIED**

---

### 20. `stranske/Travel-Plan-Permission` PR #1561
- **PR Title:** `fix: escalate overdue exceptions before tier authorization`
- **Merged At:** 2026-09-07T09:28:55Z
- **Target Issue:** [#1558](https://github.com/stranske/Travel-Plan-Permission/issues/1558) — `[P1] Wire 48-hour exception escalation before authorization and decisions`
- **Squash Diff Analysis:**
  - `src/travel_plan_permission/http_service.py`, `exception_decisions.py`: Escalates pending exceptions older than 48 hours to higher approval tiers (Director / Board) before executing authorization checks and listing views.
  - `tests/python/test_http_service.py`: Added `test_exception_escalation_before_authorization` and persistence failure rollback tests.
- **Acceptance Criteria Verification:**
  - ✅ Overdue pending requests escalate before authorization; generic manager receives HTTP 403 while director can decide.
  - ✅ Deliberate-break gate verified: skipping escalation call fails the test assertion.
- **Verdict:** **VERIFIED**

