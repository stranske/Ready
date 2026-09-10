# learning-management-system Audit Run Report (2026-09-10)

## 1. Audit Metadata
- **Unit**: `D-audit-learning-management-system--2026-09-10T17-45-16Z`
- **Target Repository**: `stranske/learning-management-system`
- **Lead Agent**: Gemini via Antigravity (`agy`)
- **Remote Tip / Base SHA**: `6e299bdf6e44b8ee34f9a0c71fa9706306e685f4` on `main`
- **Audit Trigger**: Track D refill (Open agent-ready supply = 2 <= 2; #666 and #580; trackers #41, #292, #334 excluded)
- **Scope**: `src/lms/`, `alembic/`, `tests/`, `scripts/`, `docs/`, `config/` (excluding synced `.github/` workflows and `design-system/`)

## 2. Test Baseline & Environment
- **Pytest**: `2,070 passed, 6 skipped in 143.33s` (`uv run pytest -n auto -m "not slow" -q --no-cov`)
- **Ruff**: `0 diagnostics` (`uv run ruff check .`)
- **Git Status**: clean working tree on `main` tip `6e299bd`

## 3. Findings & Categorization Across All 8 Dimensions

### Dimension 1: Code Quality & Correctness
- **Finding LMS-01 [P2]**: `create_attempt` in `src/lms/evidence/repository.py:50-81` omits Python-level validation for `confidence_rating` (1..5), `support_level` (`SUPPORT_LEVELS`), and `elapsed_seconds` (>= 0), causing unhandled database `IntegrityError` exceptions on `session.flush()` when invalid inputs are provided. Filed as [#667](https://github.com/stranske/learning-management-system/issues/667).
- **Finding LMS-02 [P2]**: `create_evidence_record` in `src/lms/evidence/repository.py:146-224` omits Python-level domain validation across score bounds (`raw_score >= 0`, `max_score > 0`), difficulty estimates (`0.0 <= item_difficulty_estimate <= 1.0`), duration fields, and categorical enums (`EVIDENCE_KINDS`, `DEMAND_LEVELS`, `KNOWLEDGE_TYPES`, `SCORER_TYPES`, `SCORING_METHODS`), crashing on `session.flush()` with unhandled database `IntegrityError`. Filed as [#668](https://github.com/stranske/learning-management-system/issues/668).
- **Finding LMS-03 [P2]**: `create_source_reference` and `update_source_reference` in `src/lms/sources/repository.py:79-121, 148-182` accept raw string inputs for `source_type`, `source_visibility`, `multi_source_role`, and `drift_status` without verifying membership in domain tuples (`SOURCE_TYPES`, `SOURCE_VISIBILITIES`, `MULTI_SOURCE_ROLES`, `DRIFT_STATUSES`), crashing with unhandled `IntegrityError` on flush. Filed as [#669](https://github.com/stranske/learning-management-system/issues/669).

### Dimension 2: Duplication & Consolidation
- **Finding LMS-04 [P2]**: `set_item_tier` in `src/lms/maintenance/service.py:289-312` mutates `item.retention_tier` and `card.retention_tier` without checking `retention_tier in RETENTION_TIERS` (`'hot'`, `'warm'`, `'cold'`), bypassing application logic and failing with database `IntegrityError` on flush. Filed as [#670](https://github.com/stranske/learning-management-system/issues/670).

### Dimension 3: Functionality & Wiring
- **Finding LMS-05 [P2]**: `goal_progress_for_learner` in `src/lms/learners/repository.py:308-349` takes `mastery_threshold: float = MASTERY_THRESHOLD` without validating `math.isfinite(mastery_threshold)` or `0.0 <= mastery_threshold <= 1.0`. Passing `float('nan')` causes comparisons `estimate >= nan` to evaluate to `False` for all target nodes, silently reporting 0 mastered nodes and 0 progress. Filed as [#671](https://github.com/stranske/learning-management-system/issues/671).
- **Finding LMS-06 [P2]**: `estimate_capacity` and `_weighted` in `src/lms/maintenance/budget.py:118-160` fail to validate that `active_items` and `tier_counts` values are non-negative integers. Negative counts distort weighted interval averages and inflate capacity headroom above sustainable intake. Filed as [#672](https://github.com/stranske/learning-management-system/issues/672).
- **Finding LMS-07 [P2]**: `score_attempt_with_rubric` in `src/lms/feedback/scoring.py:77-165` accepts `feedback_threshold` and `remediation_threshold` without validating finite unit interval bounds or relative ordering (`remediation_threshold <= feedback_threshold`). Passing `NaN` marks 100% scores as incorrect (`correctness=False`) while suppressing feedback creation. Filed as [#673](https://github.com/stranske/learning-management-system/issues/673).

### Dimension 4: Design & UX
- Evaluated learner feedback generation and mastery progress dashboards. Identified silent failure modes where invalid thresholds suppressed user feedback and produced false zero-mastery progress indications.

### Dimension 5: Approach vs Public Field
- Analyzed evidence logging contracts and FSRS scheduling pipelines against the database constraint layer. Identified that reliance on database-level CHECK constraints for basic domain validation violates standard clean architecture boundaries, causing HTTP/API handlers to crash with raw 500 errors instead of clean 422/ValueError responses.

### Dimension 6: Missed Opportunities
- Identified opportunities to centralize domain enum membership validation helpers across repository modules (`evidence`, `sources`, `maintenance`, `feedback`).

### Dimension 7: Tools Worth Integrating
- Recommended extending pre-commit linting or schema-reflection checks to ensure every database CheckConstraint has a corresponding Python-level validation check in repository helpers.

### Dimension 8: Local Skills, Automations & Human Touchpoints
- All 7 staged issue bodies validated 100% clean (0 errors, 0 advisories) against `.github/scripts/issue_format.py` and `issue_lint.py`.

## 4. Filed Issue Portfolio (Refill Run)

| Issue # | Severity | Subsystem | Title | URL |
|---|---|---|---|---|
| [#667](https://github.com/stranske/learning-management-system/issues/667) | P2 (`priority:normal`) | `evidence` | Enforce Python-level validation for confidence rating, support level, and elapsed duration in attempt creation | https://github.com/stranske/learning-management-system/issues/667 |
| [#668](https://github.com/stranske/learning-management-system/issues/668) | P2 (`priority:normal`) | `evidence` | Validate scores, difficulty estimates, durations, and categorical enums before evidence record persistence | https://github.com/stranske/learning-management-system/issues/668 |
| [#669](https://github.com/stranske/learning-management-system/issues/669) | P2 (`priority:normal`) | `sources` | Enforce enum validation for source type, visibility, drift status, and role in source reference helpers | https://github.com/stranske/learning-management-system/issues/669 |
| [#670](https://github.com/stranske/learning-management-system/issues/670) | P2 (`priority:normal`) | `maintenance` | Validate retention tier enum membership in maintenance item tier updates | https://github.com/stranske/learning-management-system/issues/670 |
| [#671](https://github.com/stranske/learning-management-system/issues/671) | P2 (`priority:normal`) | `learners` | Enforce finite unit interval bounds for mastery threshold in goal progress calculation | https://github.com/stranske/learning-management-system/issues/671 |
| [#672](https://github.com/stranske/learning-management-system/issues/672) | P2 (`priority:normal`) | `maintenance` | Reject negative item counts and negative tier distributions in maintenance capacity estimation | https://github.com/stranske/learning-management-system/issues/672 |
| [#673](https://github.com/stranske/learning-management-system/issues/673) | P2 (`priority:normal`) | `feedback` | Validate finite bounds and relative ordering for feedback and remediation thresholds in rubric scoring | https://github.com/stranske/learning-management-system/issues/673 |

## 5. Intake Log & Checkpoint Status
- 7 URLs appended to `~/.codex/orchestrator/measurement/intake-2026-09-04.log`.
- Dropbox audit directory updated: `README.md`, `2026-09-10-refill-verification-log.md`, `2026-09-10-refill-audit-run.md`, `2026-09-10-refill-AUDIT_REPORT.md`, and `2026-09-10-refill-issue-bodies/`.
- Checkpoint file finalized at `/Users/teacher/.codex/automations/research-program/artifacts/audits/D-audit-learning-management-system--2026-09-10T17-45-16Z.CHECKPOINT.md`.
