# Track D Refill Audit Report: learning-management-system (2026-09-09)

## Executive Summary
- **Unit**: `D-audit-learning-management-system--2026-09-09T05-14-48Z`
- **Target Repository**: `stranske/learning-management-system`
- **Remote Tip / Clone HEAD SHA**: `1015f28616fcfd6adb8acff50e1cb2998b17a7f5` (branch `main`)
- **Audit Date**: 2026-09-09
- **Prior Open Supply**: 1 issue (#580, `Document local-first delivery shape...`)
- **Supply Trigger**: Open agent-ready supply was 1 (<= 2), triggering a Track D demand-driven audit refill.
- **Issues Filed**: 7 verified issues (#638–#644: 2×P1, 5×P2)
- **New Open Supply**: 8 issues (healthy backlog replenished)
- **Quality Standard**: 100% conforming to `docs/AGENT_ISSUE_FORMAT.md` (7/7 PASS with 0 errors and 0 advisories validated via `.github/scripts/issue_format.py`).

---

## Baseline Environment & Codebase Verification

- **Workspace Path**: `/Users/teacher/.codex/automations/research-program/clones/learning-management-system`
- **Python / Dependencies**: Python 3.12, FastAPI, SQLAlchemy 2.0 ORM, Alembic, Pydantic v2, pytest-xdist
- **Codebase Scope**:
  - `src/lms/`: 137 files / 30,661 LOC
  - `tests/`: 178 files / 30,845 LOC
  - `alembic/`: 42 files / 4,089 LOC
  - `scripts/`: 50 files / 24,296 LOC
- **Test Suite Baseline**:
  - `1,607` tests collected, `1,597` passed, `2` skipped, `8` deselected in `43.70s` (`uv run pytest -n auto -m "not slow" -q --no-cov`).
- **Linter Status**:
  - `uv run ruff check .` clean (0 diagnostics).

---

## 8-Dimension Audit Findings & Analysis

### Dimension 1: Code Quality & Correctness
1. **Maintenance Budget Capacity NaN Bounds Crash**: `items_affordable_per_day` and `estimate_capacity` in `src/lms/maintenance/budget.py:98-112, 133-166` evaluated `min(max(anchor_share, 0.0), 1.0)`. In Python, non-finite values like `math.nan` evaluate to `nan`, triggering an unhandled `ValueError: cannot convert float NaN to integer` at `int((settings.daily_minutes * 60) // seconds_each)`.
   - *Filed*: **#641** (`Validate finite numeric bounds in maintenance budget capacity estimation`).
2. **Draft Field Type Coercion & NaN Injection**: `_coerce_like` in `src/lms/ui/drafts.py:251-267` matched `int` values via `isinstance(current, (int, float))` and unconditionally returned `float(text)`, mutating integer draft payload fields (such as period years or threshold counts) into floating-point numbers. Furthermore, `float("nan")` and `float("inf")` parsed without throwing `ValueError`, injecting NaN values into draft payloads.
   - *Filed*: **#642** (`Preserve integer types and reject non-finite strings in UI draft field coercion`).
3. **Rating Bounds & Dispute Float Parsing**: `score_to_rating` in `src/lms/maintenance/service.py:132-144` performed raw `>=` checks without finite interval validation `[0.0, 1.0]`, allowing `float('inf')` to evaluate as `>= 0.85` (awarding rating 3 Good). In `src/lms/ui/maintenance.py:258-263`, `_float_or_none` parsed `"nan"` strings into NaN floats persisted to `GradeDispute.machine_grade`.
   - *Filed*: **#644** (`Enforce finite unit interval bounds on maintenance grade ratings and dispute parsing`).

### Dimension 2: Duplication & Consolidation
4. **Review Queue Completion Anti-Enumeration & Auth Parity**: `complete_review_queue_item_route` (`POST /review-queue/{review_queue_item_id}/complete`) in `src/lms/scheduling/api.py:115-150` implemented manual user ID comparison without checking `settings.auth_required`. This emitted `HTTP 403 Forbidden` with detail `"Review queue item does not belong to the current user."` (leaking item existence and violating anti-enumeration) and broke local dev/testing workflows when `auth_required=False`.
   - *Filed*: **#643** (`Standardize learner ownership enforcement and 404 anti-enumeration on review queue complete route`).

### Dimension 3: Functionality & Wiring
5. **UI Author Learning Goal Learner Ownership**: `create_author_goal_route` (`POST /app/author/goals`) in `src/lms/ui/api.py:608-641` accepted `learner_id` directly from form payload data without verifying ownership against `current_user: CurrentUserDep`. In deployed mode (`AUTH_REQUIRED=true`), an authenticated user could inject arbitrary learning goals onto foreign learner profiles.
   - *Filed*: **#638** (`Enforce learner ownership on UI author learning goal creation route`).
6. **LLM Authoring-Assist Propose Learner Ownership**: `authoring_assist_propose_route` (`POST /llm/authoring-assist/propose`) in `src/lms/llm/api.py:354-400` accepted `learner_id` and `learning_goal_id` without `CurrentUserDep` or `SettingsDep` validation, allowing users to submit authoring draft proposals that attribute LLM session tokens to foreign learners.
   - *Filed*: **#639** (`Enforce learner ownership authorization on LLM authoring-assist propose route`).
7. **JSONL Export/Import Missing Domain Models**: `MODEL_BY_TYPE` and `EXPORT_ORDER` in `src/lms/export_import.py:68-153` omitted 8 database models (`MaintenanceItem`, `GradeDispute`, `DraftRejection`, `ReviewCardState`, `LearningInteractionSkill`, `LLMFeedbackEvent`, `LLMProposal`, and `AuditLog`), causing silent data loss on backup export dumps.
   - *Filed*: **#640** (`Register maintenance, dispute, and LLM domain models in JSONL export and import pipeline`).

### Dimension 4: Design & UX Review
- Server-rendered HTML surfaces in `src/lms/ui/` follow Pico CSS principles with clear visual hierarchy, accessible form elements, and responsive layout.
- The maintenance loop cleanly separates qualitative idea recall from quantitative reference-class anchor typicality estimation.

### Dimension 5: Approach vs Public Field
- Spaced repetition scheduling is implemented cleanly via FSRS (Free Spaced Repetition Scheduler), advancing memory stability and item difficulty.
- Maintenance anchor grading relies on distribution bands rather than memorized point values.

### Dimension 6: Missed Opportunities
- Introduce an automated test in `tests/export_import/` that introspects SQLAlchemy `Base.registry` to ensure any newly added ORM model is automatically registered in `MODEL_BY_TYPE` and `EXPORT_ORDER`.

### Dimension 7: Tools Worth Integrating
- Continuous integration schema linter to check that all database tables have corresponding JSONL backup export handlers.

### Dimension 8: Local Skills, Automations & Test Gate Integrity
- Automated pre-flight validation using `.github/scripts/issue_format.py` ensures 100% compliance with `docs/AGENT_ISSUE_FORMAT.md`.

---

## Verification Log & Adversarial Proofs

| Issue Body File | GitHub Issue URL | Adversarial Reproduction Proof |
|---|---|---|
| `2026-09-09-01-ui-author-goal-learner-ownership.md` | [#638](https://github.com/stranske/learning-management-system/issues/638) | **CONFIRMED**: FastAPI TestClient authenticated as user Bob (`u2`) submitted `POST /app/author/goals` specifying `learner_id="l1"` (Alice). The route returned `HTTP 200` and created a `LearningGoal` attached to Alice's profile without authorization checks. |
| `2026-09-09-02-llm-authoring-assist-propose-learner-ownership.md` | [#639](https://github.com/stranske/learning-management-system/issues/639) | **CONFIRMED**: Authenticated user Bob (`u2`) submitted `POST /llm/authoring-assist/propose` with `learner_id="l1"` (Alice). The route returned `HTTP 200` and persisted an `LLMSession` attributed to Alice without verifying ownership. |
| `2026-09-09-03-export-import-missing-domain-models.md` | [#640](https://github.com/stranske/learning-management-system/issues/640) | **CONFIRMED**: Programmatic introspection revealed 48 database models in `Base.__subclasses__()` vs 40 in `MODEL_BY_TYPE` and `EXPORT_ORDER`. The 8 missing models (`MaintenanceItem`, `GradeDispute`, `DraftRejection`, `ReviewCardState`, `LearningInteractionSkill`, `LLMFeedbackEvent`, `LLMProposal`, `AuditLog`) are omitted from JSONL exports. |
| `2026-09-09-04-maintenance-budget-nan-bounds-validation.md` | [#641](https://github.com/stranske/learning-management-system/issues/641) | **CONFIRMED**: Passing `anchor_share=float('nan')` to `items_affordable_per_day` crashed with unhandled `ValueError: cannot convert float NaN to integer`. |
| `2026-09-09-05-drafts-type-coercion-integer-preservation.md` | [#642](https://github.com/stranske/learning-management-system/issues/642) | **CONFIRMED**: `_coerce_like(5, "5")` returned `5.0` (`float`) rather than preserving `int`. `_coerce_like(1.5, "nan")` returned `float('nan')` without finite validation. |
| `2026-09-09-06-scheduling-complete-review-queue-anti-enumeration.md` | [#643](https://github.com/stranske/learning-management-system/issues/643) | **CONFIRMED**: Authenticated user Bob (`u2`) submitted `POST /review-queue/rq-alice-1/complete`. Route emitted `HTTP 403 Forbidden` with detail `"Review queue item does not belong to the current user."`, leaking item existence instead of returning `404 Not Found` via `require_learner_ownership`. |
| `2026-09-09-07-maintenance-score-to-rating-bounds.md` | [#644](https://github.com/stranske/learning-management-system/issues/644) | **CONFIRMED**: `score_to_rating(float('inf'))` returned `3` (Good rating). `_float_or_none("nan")` returned `nan`, propagating into `GradeDispute.machine_grade`. |

### Refuted Candidate Hypotheses (Not Filed)
- **Admin Inspection Route Auth Bypass**: Hypothesized that `GET /app/admin` in `src/lms/ui/support_admin.py` was exposed unauthenticated. Refuted upon code analysis: `src/lms/main.py:131` attaches `dependencies=auth` (`require_authenticated_user`) to `support_admin_ui_router` when mounting the router in `create_app()`. Unauthenticated requests correctly receive `401 Unauthorized` / `302 Redirect` when `AUTH_REQUIRED=true`.
- **Knowledge Edge NaN Confidence**: Hypothesized that `confidence` in `create_knowledge_edge` accepted NaN. Refuted upon code analysis: `src/lms/graphs/repository.py:317` checks `not 0.0 <= confidence <= 1.0`, which evaluates to `True` for NaN, correctly raising `ValueError`.

---

## Filed Issues Summary

| Issue # | Title | Severity | Labels | GitHub Issue Link |
|---|---|---|---|---|
| **#638** | Enforce learner ownership on UI author learning goal creation route | High | `bug`, `priority:high` | https://github.com/stranske/learning-management-system/issues/638 |
| **#639** | Enforce learner ownership authorization on LLM authoring-assist propose route | High | `bug`, `priority:high` | https://github.com/stranske/learning-management-system/issues/639 |
| **#640** | Register maintenance, dispute, and LLM domain models in JSONL export and import pipeline | Normal | `bug`, `priority:normal` | https://github.com/stranske/learning-management-system/issues/640 |
| **#641** | Validate finite numeric bounds in maintenance budget capacity estimation | Normal | `bug`, `priority:normal` | https://github.com/stranske/learning-management-system/issues/641 |
| **#642** | Preserve integer types and reject non-finite strings in UI draft field coercion | Normal | `bug`, `priority:normal` | https://github.com/stranske/learning-management-system/issues/642 |
| **#643** | Standardize learner ownership enforcement and 404 anti-enumeration on review queue complete route | Normal | `bug`, `priority:normal` | https://github.com/stranske/learning-management-system/issues/643 |
| **#644** | Enforce finite unit interval bounds on maintenance grade ratings and dispute parsing | Normal | `bug`, `priority:normal` | https://github.com/stranske/learning-management-system/issues/644 |

---

## Audit Accounting & Ledger Updates
- Appended 7 rows to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- Updated `Code/Audits/learning-management-system/README.md` and `Code/Audits/AUDIT_LEDGER.md`.
- Staged all 7 validated issue markdown bodies under `Code/Audits/learning-management-system/2026-09-09-issue-bodies/`.
- Unit checkpoint recorded at `artifacts/audits/D-audit-learning-management-system--2026-09-09T05-14-48Z.CHECKPOINT.md` and shared `artifacts/audits/CHECKPOINT.md`.
