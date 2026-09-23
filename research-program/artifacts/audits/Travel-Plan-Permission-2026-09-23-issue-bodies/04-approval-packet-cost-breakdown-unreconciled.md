## Why (verified evidence)

`build_approval_packet` sums the optional `cost_breakdown` override without reconciling it to `trip_plan.estimated_cost` or the plan's authoritative breakdown. Managers can receive approval emails and PDFs showing a total that bears no relation to the trip object submitted for policy evaluation.

- `src/travel_plan_permission/approval_packet.py:230-238` — `raw_costs = cost_breakdown or trip_plan.expense_breakdown`; `total_cost = sum(costs.values(), Decimal("0"))` with no cross-check.
- `src/travel_plan_permission/approval_packet.py:255-265` — PDF and `ApprovalPacket.total_cost` use the unchecked total.
- Reproduction: `_sample_trip_plan()` with `estimated_cost=1250.50` and `cost_breakdown={"airfare": Decimal("1")}` yields `pkt.total_cost == Decimal("1")`.

## Tasks

- [ ] In `src/travel_plan_permission/approval_packet.py:219-238`, when `cost_breakdown` is supplied, require it to match `trip_plan.expense_breakdown` and/or `trip_plan.estimated_cost` within the project's existing decimal tolerance, or raise `ValueError` with a clear message.
- [ ] When `cost_breakdown` is omitted, keep current behavior (derive from plan).

## Acceptance Criteria

- Named test: `tests/python/test_approval_packet.py::test_build_packet_rejects_cost_breakdown_that_disagrees_with_trip_total` — mismatched override raises `ValueError`.
- Deliberate-break → revert: remove reconciliation → named test FAILS → revert.

## Non-Goals

- Do NOT change PDF layout or email templates beyond the total figure source.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Reproduction:_
```python
from decimal import Decimal
from travel_plan_permission.approval_packet import build_approval_packet, ApprovalLinks
from tests.python.test_approval_packet import _sample_trip_plan
plan = _sample_trip_plan()
links = ApprovalLinks(approve_url="http://a", reject_url="http://r", override_url="http://o")
pkt = build_approval_packet(trip_plan=plan, compliance_status="ok", approval_links=links, cost_breakdown={"airfare": Decimal("1")})
assert pkt.total_cost == plan.estimated_cost  # fails: 1 vs 1250.50
```

_Surfaced by Track D repo-audit 2026-09-23; verified on clone tip._
