# Comprehensive Audit Report: stranske/learning-management-system (2026-09-08)

**Audit Date:** 2026-09-08  
**Target Repository:** `stranske/learning-management-system`  
**Tip Commit:** `0ae9443cdb72ae4f0ccae10346bb5ab30033c2ca` (Branch `main`)  
**Auditor:** Gemini (agy) via Antigravity Agent Runtime  
**Lead Verification:** 100% Adversarially Verified on Live Tip  
**Issues Filed:** 8 Conforming Issues ([#620](https://github.com/stranske/learning-management-system/issues/620)–[#627](https://github.com/stranske/learning-management-system/issues/627))  
**Format Guard Status:** 100% Passed (0 Errors, 0 Advisories across all filed bodies)  

---

## 1. Executive Summary & Verdict

`learning-management-system` is an active Python/FastAPI learning platform implementing mastery-based spaced repetition (FSRS), capability gap analyses, rubric-based diagnostic evaluation, and AI study coaching. Over recent development cycles (milestones M5 and M6), the platform expanded significantly with new authoring, feedback, and capability modeling surfaces.

Recent PR merges (#610, #616, #617, #618) resolved prior API-layer learner ownership gaps. However, deep adversarial analysis of the live tip (`0ae9443`) revealed that authorization enforcement remained incomplete across several crucial user-facing UI surfaces and the LLM trace-control route. Furthermore, several data integrity, numeric edge case, and CLI error handling defects were identified.

### Summary of Filed Issues

| Issue # | Severity | Title | Subsystem | Verification Summary |
|---|---|---|---|---|
| [#620](https://github.com/stranske/learning-management-system/issues/620) | **P1 (Security)** | Enforce learner ownership authorization on UI feedback detail, reveal, and revision routes | `src/lms/ui/feedback.py` | Live repro: `GET /app/learner/feedback/{id}`, hint/answer reveals, and revisions lack learner ownership check in deployed auth mode |
| [#621](https://github.com/stranske/learning-management-system/issues/621) | **P1 (Security)** | Enforce learner ownership authorization on UI capability target detail and action routes | `src/lms/ui/capability_gap.py` | Live repro: Target details, estimate recomputation, gap analysis, and maintenance plan creation accept unverified target/estimate IDs |
| [#622](https://github.com/stranske/learning-management-system/issues/622) | **P1 (Security)** | Enforce authentication and learner ownership on LLM session trace-control route | `src/lms/llm/api.py` | Live repro: `POST /llm/sessions/{id}/trace-control` accepts arbitrary client `actor_id`, allowing cross-tenant session wipe |
| [#623](https://github.com/stranske/learning-management-system/issues/623) | **P2 (Correctness)** | Validate finite numeric bounds in rubric criterion scoring to prevent NaN propagation | `src/lms/feedback/scoring.py` | Live repro: `points = float("nan")` bypasses min/max checks (`nan < 0` is `False`), propagating to DB and causing 500 error |
| [#624](https://github.com/stranske/learning-management-system/issues/624) | **P2 (Data Integrity)** | Include M5 and M6 domain models in JSONL export and import pipeline | `src/lms/export_import.py` | Live repro: `Hint`, `ModelAnswer`, `RevisionRequest`, `WorkProduct`, and `LearnerReflection` omitted from JSONL export/import |
| [#625](https://github.com/stranske/learning-management-system/issues/625) | **P2 (Tooling/CLI)** | Catch prerequisite cycles in CSV graph importer and raise CsvGraphImportError | `src/lms/importers/csv_graph.py` | Live repro: Graph cycle raises raw `ValueError`, crashing `__main__.py` with traceback instead of exiting cleanly |
| [#626](https://github.com/stranske/learning-management-system/issues/626) | **P2 (Robustness)** | Add non-numeric string and NaN validation to capability repository float parsing | `src/lms/capability/repository.py` | Live repro: `_as_float` lacks string try-except and returns `nan`, masking weak nodes when comparing with confidence threshold |
| [#627](https://github.com/stranske/learning-management-system/issues/627) | **P2 (Error Handling)** | Handle duplicate proposal state transitions gracefully in graph design UI routes | `src/lms/ui/graph_design.py` | Live repro: Double-clicking approve/reject proposal raises unhandled exception resulting in HTTP 500 instead of 303 redirect |

---

## 2. Multi-Dimensional Deep Analysis

### Dimension 1: Code Quality and Correctness
- **Finding:** IEEE-754 `NaN` values in Python comparisons evaluate to `False` for all relational operators (`<`, `>`, `<=`, `>=`). In `src/lms/feedback/scoring.py:233-237` and `src/lms/capability/repository.py:221-240`, points and estimate scores parsed without `math.isfinite()` bypass range validation, corrupting persistent state and causing unhandled database exceptions.
- **Remediation:** Strict explicit finite checking (`try: val = float(...) except (ValueError, TypeError): ... if not math.isfinite(val): raise ...`).

### Dimension 2: Duplication and Consolidation
- **Finding:** Authorization checks in the API layer rely on `require_learner_ownership` from `src/lms/auth/dependencies.py`, but the UI routes in `src/lms/ui/feedback.py` and `src/lms/ui/capability_gap.py` reimplemented ad-hoc or omitted ownership checks entirely.
- **Remediation:** Standardize dependency injection across all UI routes using `CurrentUserDep` + `SettingsDep` + `require_learner_ownership`.

### Dimension 3: Functionality and Wiring
- **Finding:** In `src/lms/llm/api.py:657-686`, the trace-control endpoint was wired to accept client-supplied `actor_id` without authenticating the user identity against `current_user.learner_id`. In `src/lms/ui/graph_design.py`, proposal approval actions lacked exception wiring for invalid state transitions.
- **Remediation:** Wire identity checks and exception handlers with user flash notifications.

### Dimension 4: Design and UX
- **Finding:** When graph design proposals are approved concurrently or double-clicked, the author is presented with an unhandled HTTP 500 internal server error page rather than a helpful status message.
- **Remediation:** Catch `(InvalidProposalStateError, ProposalNotFoundError)` and issue HTTP 303 redirects with session flash warnings.

### Dimension 5: Approach versus the Public Field
- **Finding:** The platform's JSONL backup/export system (`src/lms/export_import.py`) guarantees data portability and backup safety, but newly added M5/M6 domain entities were omitted from the registry.
- **Remediation:** Include all active domain entities in `MODEL_BY_TYPE`, `EXPORT_ORDER`, and `DEPENDENCIES` to maintain full roundtrip backup fidelity.

### Dimension 6: Missed Opportunities
- **Finding:** `import_csv_graph` in `src/lms/importers/csv_graph.py` provides a `dry_run=True` parameter, but fails to check for cyclic prerequisite dependencies before touching the database.
- **Remediation:** Add in-memory topological cycle detection to `dry_run` mode and wrap database edge creation in `CsvGraphImportError`.

### Dimension 7: Tools Worth Integrating
- **Finding:** While the test suite has 1,431 collected tests, boundary fuzzing for non-finite IEEE-754 float values (NaN, Inf) and malformed string inputs is currently performed ad-hoc.
- **Recommendation:** Integrate property-based testing (Hypothesis) for scoring engines and repository numeric aggregations.

### Dimension 8: Local Skills, Automations, and Human Touchpoints
- **Finding:** The repository enforces strict issue formatting via `Agents Issue Format Guard` (`.github/scripts/issue_format.py`). All 8 filed issues were pre-flight validated with 0 errors and 0 advisories and cleared the automated CI guard on the first pass.

---

## 3. Test & Verification Summary

- **Total Unit & Integration Tests Collected:** 1,431 tests
- **Baseline CI Status:** 100% Green on tip `0ae9443cdb72ae4f0ccae10346bb5ab30033c2ca`
- **Adversarial Verification:** All 8 findings verified with live Python / FastAPI TestClient execution against the live tip.
- **Format Pre-Flight Check:** All 8 issue bodies passed `.github/scripts/issue_format.py` with exit code 0 and 0 advisories.
- **Remote CI Guard:** `Agents Issue Format Guard` succeeded on all 8 filed issues.

---

## 4. Next Steps & Recommended Execution Order

1. **Sprint 1 (P1 Security Sweep):**
   - Implement [#620](https://github.com/stranske/learning-management-system/issues/620): UI feedback learner ownership
   - Implement [#621](https://github.com/stranske/learning-management-system/issues/621): UI capability target learner ownership
   - Implement [#622](https://github.com/stranske/learning-management-system/issues/622): LLM trace-control learner ownership
2. **Sprint 2 (P2 Correctness & Data Integrity):**
   - Implement [#623](https://github.com/stranske/learning-management-system/issues/623): Rubric scoring NaN points validation
   - Implement [#624](https://github.com/stranske/learning-management-system/issues/624): Export/import M5/M6 domain models
   - Implement [#625](https://github.com/stranske/learning-management-system/issues/625): CSV graph importer cycle error handling
3. **Sprint 3 (P2 Robustness & UI Error Handling):**
   - Implement [#626](https://github.com/stranske/learning-management-system/issues/626): Capability repository `_as_float` NaN protection
   - Implement [#627](https://github.com/stranske/learning-management-system/issues/627): Graph design proposal transition handling
