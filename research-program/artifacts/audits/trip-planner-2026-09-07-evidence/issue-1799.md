# [P1] Live TPP policy snapshot must map lodging and airfare rules into constraint_set

## Why

`trip_planner/integrations/tpp/client.py:899-911` builds `result_payload.constraint_set` with empty `airfare_rules`, `lodging_rules`, `ground_transport_rules`, and `meal_rules` on the live HTTP path. Fixture import preserves caps (for example `tests/fixtures/integrations/tpp/policy/standard_policy_sync.json` includes `lodging_rules.max_nightly_rate_usd`). After a real TPP sync, compare preview and ranking never see imported spend or lodging limits.

## Scope

Live HTTP policy snapshot adaptation in `trip_planner/integrations/tpp/client.py`.

## Tasks

- [ ] Add `test_live_policy_snapshot_maps_lodging_and_airfare_rules_into_constraint_set` in `tests/integrations/test_policy_sync.py` using a fake HTTP response that includes `lodging_rules` and `airfare_rules`.
- [ ] Map TPP response rule blocks into `result_payload.constraint_set` in `trip_planner/integrations/tpp/client.py` instead of hard-coded empty dicts at lines 905-908.
- [ ] Populate `organization_context.comparable_requirements` in `trip_planner/integrations/tpp/client.py:921` from the HTTP payload when present.

## Acceptance Criteria

- `pytest tests/integrations/test_policy_sync.py::test_live_policy_snapshot_maps_lodging_and_airfare_rules_into_constraint_set` passes.
- `pytest tests/integrations/test_policy_sync.py` passes.
- Deliberate-break → revert: restore empty `lodging_rules` in `trip_planner/integrations/tpp/client.py` and confirm the new test fails; revert.

## Non-Goals

- Implementing new TPP transport endpoints beyond the existing `PUT /policy` client.
- Scaffold-only completion does NOT count: leaving empty rule dicts while only adding logging is a failure of this issue.

_Surfaced by repo-audit Track D 2026-09-07; verified on clone tip 8077785._
