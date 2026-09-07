# [P1] Business ranking must honor TPP comparable_requirements from organization_context

## Why

`trip_planner/business/objective_derivation.py:123-127` builds `ComparableRequirementObjectives.required_categories` only from `profile.vendor_constraints.comparison_requirements`. TPP import stores `organization_context.comparable_requirements` (`trip_planner/integrations/tpp/policy_sync.py:383-388`) and reload preserves them (`trip_planner/app/services/policy.py:446`), but ranking penalties in `trip_planner/ranking/business.py:822-840` never see TPP-mandated comparable counts.

## Scope

Objective derivation and business ranking inputs for comparable requirements.

## Tasks

- [ ] Add `test_objective_derivation_uses_tpp_comparable_requirements_for_ranking_penalties` in `tests/ranking/test_business_ranking.py` with imported `comparable_requirements` overriding profile defaults.
- [ ] Merge `organization_context.comparable_requirements` into `_comparable_requirements` in `trip_planner/business/objective_derivation.py`.
- [ ] Pass the merged comparable objectives through the business ranking path that computes comparable-readiness penalties in `trip_planner/ranking/business.py`.

## Acceptance Criteria

- `pytest tests/ranking/test_business_ranking.py::test_objective_derivation_uses_tpp_comparable_requirements_for_ranking_penalties` passes.
- `pytest tests/ranking/test_business_ranking.py` passes.
- Deliberate-break → revert: ignore `organization_context.comparable_requirements` in `trip_planner/business/objective_derivation.py` and confirm the new test fails; revert.

## Non-Goals

- Leisure ranking changes in `trip_planner/ranking/leisure.py`.
- Scaffold-only completion does NOT count: copying comparable requirements into notes without affecting ranking penalties is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._
