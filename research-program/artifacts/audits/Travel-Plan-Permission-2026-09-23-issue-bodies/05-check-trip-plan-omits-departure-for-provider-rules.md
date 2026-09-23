## Why (verified evidence)

`check_trip_plan`, the planner verdict entry point, runs `PolicyValidator.validate_plan(plan)` without passing the trip's departure date. Rules such as `ProviderApprovalRule` default `reference_date` to `date.today()`, so provider-contract validity is evaluated at submission time instead of travel date—unlike `list_allowed_vendors`, which uses the plan departure date.

- `src/travel_plan_permission/policy_api.py:1455-1456` — `validation_results = validator.validate_plan(plan)` (no `reference_date`).
- `src/travel_plan_permission/validation.py:367-372` — `validate_plan` forwards `reference_date` to each rule; `None` becomes today inside `ProviderRegistry.is_active`.
- `src/travel_plan_permission/validation.py:235-260` — `ProviderApprovalRule.evaluate` passes `reference_date` through to registry checks.

User-facing consequence: a provider that is inactive today but active on the departure date can spuriously fail (or the converse) on the planner policy verdict.

## Tasks

- [ ] In `src/travel_plan_permission/policy_api.py:1456`, call `validator.validate_plan(plan, reference_date=plan.departure_date)` (or a shared helper used by both `check_trip_plan` and `list_allowed_vendors`).
- [ ] Align any other policy-api paths that call `validate_plan` without a reference date on the same rule.

## Acceptance Criteria

- Named test: `tests/python/test_policy_api.py::test_check_trip_plan_uses_departure_date_for_provider_contract` — registry fixture where the selected provider is inactive today but active on `plan.departure_date`; assert `check_trip_plan` does not emit a provider-approval issue for that provider.
- Deliberate-break → revert: pass `reference_date=None` again → named test FAILS → revert.

## Non-Goals

- Do NOT change `config/providers.yaml` contents in this issue.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Reproduction:_
Compare `ProviderApprovalRule.evaluate(plan, reference_date=plan.departure_date)` (passes) vs `check_trip_plan(plan)` (uses today via `validate_plan(plan)` at `policy_api.py:1456`) when the registry entry's `valid_from` is after today but before departure.

_Surfaced by Track D repo-audit 2026-09-23; verified by code trace and rule API contract._
