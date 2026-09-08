## Why

The UI routes for viewing capability targets, triggering estimate recomputation, generating gap analyses, and creating maintenance plans do not enforce learner ownership authorization (`src/lms/ui/capability_gap.py:92-221`). When deployed with authentication enabled, `capability_target_detail_route` (`GET /app/learner/capability/targets/{target_id}`), `recompute_estimate_action` (`POST /app/learner/capability/estimates`), `create_gap_analysis_action` (`POST /app/learner/capability/gap-analyses`), and `create_maintenance_plan_action` (`POST /app/learner/capability/maintenance-plans`) accept target, estimate, and gap analysis IDs without validating that the associated `learner_id` matches the authenticated user (`current_user`). Any authenticated user can view foreign capability dashboards, trigger recomputation of foreign estimates, generate gap analyses for arbitrary foreign targets, and create maintenance plans linked to other learners. This is a verified **current break** and authorization bypass vulnerability.

## Scope

Inject `CurrentUserDep` and `SettingsDep` into `capability_target_detail_route`, `recompute_estimate_action`, `create_gap_analysis_action`, and `create_maintenance_plan_action` in `src/lms/ui/capability_gap.py`. Validate `require_learner_ownership(session, user=current_user, settings=settings, learner_id=target.learner_id)` before rendering details or mutating records. Add regression tests in `tests/ui/test_capability_gap_surface.py`.

## Non-Goals

- Do NOT modify the underlying capability calculation formulas in `src/lms/capability/repository.py`.
- Do NOT modify the support admin routes in `src/lms/ui/support_admin.py`.
- Scaffold-only completion does NOT count: modifying route parameters without validating target learner ownership or without adding test assertions verifying HTTP 404 on cross-learner target requests is a failure of this issue.

## Tasks

- [ ] In `src/lms/ui/capability_gap.py`, import `CurrentUserDep`, `SettingsDep`, and `require_learner_ownership` from `src/lms/auth/dependencies.py`.
- [ ] In `src/lms/ui/capability_gap.py`, update `capability_target_detail_route` to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and call `require_learner_ownership(session, user=current_user, settings=settings, learner_id=target.learner_id)` after fetching the capability target.
- [ ] In `src/lms/ui/capability_gap.py`, update `recompute_estimate_action`, `create_gap_analysis_action`, and `create_maintenance_plan_action` to accept `current_user: CurrentUserDep` and `settings: SettingsDep`, and verify learner ownership before creating or recomputing estimates, gap analyses, or maintenance plans.
- [ ] In `tests/ui/test_capability_gap_surface.py`, add test `test_capability_gap_surface_rejects_foreign_learner_target` asserting that accessing or triggering actions on a foreign learner's capability target returns HTTP 404.

## Acceptance Criteria

- [ ] The named test `pytest tests/ui/test_capability_gap_surface.py -k "test_capability_gap_surface_rejects_foreign_learner_target"` passes with 0 failures, asserting HTTP 404 responses when requesting or mutating another learner's capability target.
- [ ] **Deliberate-break gate:** In `src/lms/ui/capability_gap.py:98`, comment out the `require_learner_ownership` check in `capability_target_detail_route`. Running `pytest tests/ui/test_capability_gap_surface.py -k "test_capability_gap_surface_rejects_foreign_learner_target"` MUST fail with an assertion failure (receiving HTTP 200 instead of HTTP 404). Revert the edit after capturing the failure.
- [ ] Existing capability gap surface tests pass via `pytest tests/ui/test_capability_gap_surface.py`.

## Implementation Notes

- Ensure consistent HTTP 404 response on ownership mismatch using `require_learner_ownership` from `src/lms/auth/dependencies.py:100`.
- Confirmed-green test runner: `pytest tests/ui/test_capability_gap_surface.py`
