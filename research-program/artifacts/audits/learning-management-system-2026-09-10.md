# learning-management-system Audit Run Report (2026-09-10)

## 1. Audit Metadata
- **Unit**: `D-audit-learning-management-system--2026-09-10T05-35-47Z`
- **Target Repository**: `stranske/learning-management-system`
- **Lead Agent**: Gemini via Antigravity (`agy`)
- **Remote Tip / Base SHA**: `09d509e88aa5bdad244d4029737ea22b6f13a95d` on `main`
- **Audit Trigger**: Track D refill (agent-ready open issue supply = 1 <= 2; issue #580 open; milestone/trackers #41, #292, #334 excluded)
- **Scope**: `src/lms/`, `alembic/`, `tests/`, `scripts/`, `docs/`, `config/` (excluding synced `.github/` workflows and `design-system/`)

## 2. Test Baseline & Environment
- **Pytest**: `1,745 passed, 6 skipped in 75.81s` (`uv run pytest -n auto -m "not slow" -q --no-cov`)
- **Ruff**: `0 diagnostics` (`uv run ruff check .`)
- **Git Status**: clean working tree on `main` tip `09d509e88aa5bdad244d4029737ea22b6f13a95d`

## 3. Findings & Categorization Across All 8 Dimensions

### Dimension 1: Code Quality & Correctness
- **Finding LMS-02 [P2]**: `_select_passage` in `src/lms/sources/repository.py:388-400` fails on inverted line ranges like `"5-0"` by calculating `start - 1 == -1`, resulting in Python list slicing `lines[-1:5]` which extracts only `"line 5\n"` due to negative indexing. Filed as [#653](https://github.com/stranske/learning-management-system/issues/653).
- **Finding LMS-03 [P2]**: `score_work_product` in `src/lms/cases/repository.py:386-395` lacks finite numeric validation for `score` and `max_score`, persisting `inf` and `nan` into evidence records. Filed as [#654](https://github.com/stranske/learning-management-system/issues/654).
- **Finding LMS-04 [P2]**: `prepare_draft` in `src/lms/maintenance/drafts.py:59-65, 182-194` accepts `central_value=float("nan")`, computing `typical_low=nan, typical_high=nan` which bricks draft queues when validated. Filed as [#655](https://github.com/stranske/learning-management-system/issues/655).

### Dimension 2: Duplication & Consolidation
- **Finding LMS-05 [P2]**: `create_review_queue_item` and `create_remediation_trigger` in `src/lms/scheduling/repository.py:25-54, 328-365` lack Python-level validation for priority ranges [0.0, 1.0] and trigger type enum codes, deferring to DB CHECK constraints and crashing with raw `IntegrityError` instead of standard `ValueError`. Filed as [#656](https://github.com/stranske/learning-management-system/issues/656).

### Dimension 3: Functionality & Wiring
- **Finding LMS-01 [P1]**: UI author rubric creation endpoint `POST /app/author/rubrics` (`src/lms/ui/api.py:794-823, 1976-1980` & `src/lms/feedback/repository.py:961-987`) crashes with HTTP 500 when submitted with `criterion_order="0"` or non-finite points (`"nan"`), because values violate SQLite CHECK constraints without Python-level pre-validation. Filed as [#652](https://github.com/stranske/learning-management-system/issues/652).
- **Finding LMS-06 [P2]**: `update_knowledge_edge` in `src/lms/graphs/repository.py:419-450` allows changing `edge_type` to `"prerequisite"` without checking `_ordering_edge_closes_cycle`, permitting cycle creation in DAGs. Filed as [#657](https://github.com/stranske/learning-management-system/issues/657).
- **Finding LMS-07 [P2]**: `create_hint` and `create_model_answer` in `src/lms/feedback/repository.py:623-648, 703-725` lack validation for `reveal_order >= 1` and enum constraints (`support_level`), crashing with DB `IntegrityError`. Filed as [#658](https://github.com/stranske/learning-management-system/issues/658).

### Dimension 4: Design & UX
- Authoring UI form error handling: invalid input crashes were identified in UI author rubric creation (LMS-01/Issue #652) and rectified by proposing clean input validation and client flash errors.

### Dimension 5: Approach vs Public Field
- Investigated spaced repetition scheduling (FSRS-4.5) and DAG topological sort invariants. Evaluated prerequisite cycle detection guarantees (LMS-06/Issue #657).

### Dimension 6: Missed Opportunities
- Identified lack of cycle checks on graph edge mutations and missing domain validation layers in low-level repository functions.

### Dimension 7: Tools Worth Integrating
- Identified value in automated linting / AST checks for SQLite CHECK constraints vs Python repository validation helpers.

### Dimension 8: Local Skills, Automations & Human Touchpoints
- All 7 staged issue bodies validated 100% clean (0 errors, 0 advisories) against `docs/AGENT_ISSUE_FORMAT.md`.

## 4. Filed Issue Portfolio

| Issue # | Severity | Subsystem | Title | URL |
|---|---|---|---|---|
| #652 | P1 (`priority:high`) | `ui/authoring`, `feedback` | Enforce finite positive points and order bounds in rubric creation to prevent unhandled 500 crashes | https://github.com/stranske/learning-management-system/issues/652 |
| #653 | P2 (`priority:normal`) | `sources` | Fix negative line index wrap in source reference passage range extraction for inverted ranges | https://github.com/stranske/learning-management-system/issues/653 |
| #654 | P2 (`priority:normal`) | `cases` | Enforce finite numeric bounds in transfer case work product scoring | https://github.com/stranske/learning-management-system/issues/654 |
| #655 | P2 (`priority:normal`) | `maintenance` | Reject non-finite central values in maintenance draft preparation and default band calculation | https://github.com/stranske/learning-management-system/issues/655 |
| #656 | P2 (`priority:normal`) | `scheduling` | Add Python-level validation for priority bounds and reason codes in review queue repository | https://github.com/stranske/learning-management-system/issues/656 |
| #657 | P2 (`priority:normal`) | `graphs` | Prevent prerequisite cycle creation during knowledge edge type updates | https://github.com/stranske/learning-management-system/issues/657 |
| #658 | P2 (`priority:normal`) | `feedback` | Enforce positive reveal orders and enum constraints in feedback hint and model answer repository helpers | https://github.com/stranske/learning-management-system/issues/658 |

## 5. Intake & Durable Records
- **Intake Log**: 7 entries appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- **Durable Audit Ledger**: Updated `Code/Audits/AUDIT_LEDGER.md` with 2026-09-10 index entry and full run record.
- **Durable Audit Directory**: Updated `Code/Audits/learning-management-system/README.md`, written `2026-09-10-AUDIT_REPORT.md`, `2026-09-10-verification-log.md`, and `2026-09-10-audit-run.md`.
- **Staged Issue Bodies**: Persisted under `Code/Audits/learning-management-system/2026-09-10-issue-bodies/`.
