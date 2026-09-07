# [P1] PolicyConstraintSet must persist budget_rules for scenario preview caps

## Why

`trip_planner/app/services/scenario_policy_preview.py:189-196` reads `constraint_set.budget_rules` for spend-cap preview. `trip_planner/business/policy_contracts.py:47-58` defines `PolicyConstraintSet` without a `budget_rules` field, and `trip_planner/integrations/tpp/policy_sync.py:322-356` cannot import it. Fixture policy state includes `budget_rules` (`trip_planner/resources/state/policy/business_client_summit_policy.json:7-10`), but TPP import persists `imported.constraint_set.to_dict()` in `trip_planner/app/services/policy.py:735`, which drops budget caps after sync.

## Scope

`PolicyConstraintSet` contract, TPP import, and reload normalization for `budget_rules`.

## Tasks

- [ ] Add `budget_rules: dict[str, Any]` to `PolicyConstraintSet` in `trip_planner/business/policy_contracts.py` with validation mirroring other rule maps.
- [ ] Map `budget_rules` through `trip_planner/integrations/tpp/policy_sync.py` import and `trip_planner/app/services/policy.py` `_normalize_constraint_set_payload`.
- [ ] Add `test_policy_import_persists_budget_rules_for_scenario_preview` in `tests/app/test_scenario_policy_preview.py` importing a fixture with `budget_rules` and asserting preview violations surface.

## Acceptance Criteria

- `pytest tests/app/test_scenario_policy_preview.py::test_policy_import_persists_budget_rules_for_scenario_preview` passes.
- `pytest tests/app/test_policy.py tests/app/test_scenario_policy_preview.py` pass.
- Deliberate-break → revert: remove `budget_rules` from `PolicyConstraintSet.to_dict()` and confirm the new test fails; revert.

## Non-Goals

- Changing unrelated ranking weights in `trip_planner/ranking/business.py`.
- Scaffold-only completion does NOT count: adding `budget_rules` to the dataclass without wiring import, reload, and preview is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._
