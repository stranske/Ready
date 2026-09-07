# Travel-Plan-Permission targeted audit findings

Audited read-only at commit `5be7204`. The focused test run passed (`146 passed`), but its homogeneous and single-threaded fixtures leave the concrete cases below unexercised.

## 1. Bind role-change approval to an authenticated administrator instead of a caller-supplied role

**SEVERITY: P0**

**EVIDENCE:** `src/travel_plan_permission/security.py:443-467`

```python
def approve_role_change(
    self, admin_actor: str, admin_role: RoleName, request_id: str
) -> RoleChangeRequest:
    """Approve a pending role change; only admins may approve."""

    if admin_role not in {RoleName.SYSTEM_ADMIN, RoleName.POLICY_ADMIN}:
        ...
        raise PermissionError("Only admin roles may approve role changes")

    request = self.pending_role_changes.get(request_id)
    if request is None:
        raise KeyError(f"No pending role change for id '{request_id}'")

    request.state = RoleChangeState.APPROVED
```

`admin_actor` is never resolved against a role assignment; authorization is entirely determined by the independently supplied `admin_role`. Any caller able to invoke this public security operation can claim `SYSTEM_ADMIN` and approve another user's elevation.

**TRIGGER:** Create a pending request, then call `approve_role_change(admin_actor="eve", admin_role=RoleName.SYSTEM_ADMIN, request_id=request.request_id)`. The method approves it even though no code establishes that Eve is a system administrator.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_security_model.py::test_role_change_requires_admin_approval_and_is_logged` varies only `admin_role=APPROVER` versus a hard-coded `SYSTEM_ADMIN`; it never supplies a non-admin actor paired with the privileged enum.

**PROPOSED TEST GATE:** Add `tests/python/test_security_model.py::test_role_change_approval_derives_admin_role_from_actor` with an identity/role resolver containing `eve: APPROVER`; assert that an attempt to pass `SYSTEM_ADMIN` for Eve raises `PermissionError` and leaves the request pending.

## 2. Reject role-change decisions after their first terminal decision

**SEVERITY: P1**

**EVIDENCE:** `src/travel_plan_permission/security.py:463-488` and `src/travel_plan_permission/security.py:510-535`

```python
request = self.pending_role_changes.get(request_id)
if request is None:
    raise KeyError(f"No pending role change for id '{request_id}'")

request.state = RoleChangeState.APPROVED
...
return request
```

```python
request = self.pending_role_changes.get(request_id)
if request is None:
    raise KeyError(f"No pending role change for id '{request_id}'")

request.state = RoleChangeState.REJECTED
...
return request
```

Neither decision path checks for `PENDING_APPROVAL`, and approved/rejected requests are never removed. A later admin can rewrite the decision and leave contradictory audit events for the same request.

**TRIGGER:** Approve a request, then call `reject_role_change` with the same `request_id` and an admin role. Its state changes from `APPROVED` to `REJECTED`.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_security_model.py::test_role_change_requires_admin_approval_and_is_logged` performs exactly one successful decision and never attempts a second decision on that request.

**PROPOSED TEST GATE:** Add `tests/python/test_security_model.py::test_role_change_decision_is_terminal`; approve a request, assert that a subsequent reject raises a transition error, and assert state/audit-event count remain unchanged.

## 3. Serialize SQLite reads with writes on the shared connection

**SEVERITY: P1**

**EVIDENCE:** `src/travel_plan_permission/persistence/sqlite_store.py:74-85` and `src/travel_plan_permission/persistence/sqlite_store.py:98-106`

```python
conn = sqlite3.connect(
    self._path,
    isolation_level=None,
    check_same_thread=False,
)
...
self._conn = conn
```

```python
def _select_all(self) -> tuple[list[tuple[str, str, object]], list[tuple[str, object]]]:
    conn = self._connection()
    records = conn.execute(
        "SELECT namespace, record_key, payload_json FROM portal_records"
    ).fetchall()
    singletons = conn.execute(
        "SELECT namespace, payload_json FROM portal_singletons"
    ).fetchall()
```

Writes take `_write_lock`, but `_select_all` takes no lock while sharing the same `check_same_thread=False` connection. SQLite permits the read on that connection to observe the writer's uncommitted delete/upsert sequence, so a portal request can return an incomplete snapshot.

**TRIGGER:** Start `save_snapshot(..., replace=True)` on the shared store and pause after `_delete_absent_records`; concurrently call `load_snapshot()`. The read can observe the deleted namespace before its replacements are inserted/committed.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_portal_state_store.py::TestSQLitePortalStateStore::test_concurrent_writers_do_not_lose_each_others_records` varies concurrent writers only. It never reads while a replace transaction is open.

**PROPOSED TEST GATE:** Add `tests/python/test_portal_state_store.py::TestSQLitePortalStateStore::test_load_waits_for_inflight_replace`; pause the delete hook with threading events, invoke `load_snapshot` in a second thread, and assert it blocks until commit and returns the complete replacement snapshot.

## 4. Do not let a Postgres read commit another thread's transaction

**SEVERITY: P0**

**EVIDENCE:** `src/travel_plan_permission/persistence/postgres_store.py:90-104`

```python
def _select_all(self) -> tuple[list[tuple[str, str, object]], list[tuple[str, object]]]:
    conn = self._connection()
    with conn.cursor() as cur:
        cur.execute("SELECT namespace, record_key, payload_json FROM tpp.portal_records")
        records = cur.fetchall()
        cur.execute("SELECT namespace, payload_json FROM tpp.portal_singletons")
        singletons = cur.fetchall()
    conn.commit()
    return records, singletons

@contextmanager
def _transaction(self) -> Iterator[Cursor[object]]:
    conn = self._connection()
    with self._write_lock, conn.transaction(), conn.cursor() as cur:
        yield cur
```

The single connection is shared, but only writers acquire `_write_lock`. A concurrent `load_snapshot()` can run `conn.commit()` while a writer is between the delete and upsert statements in its `conn.transaction()`, prematurely persisting the partial replacement (or breaking the writer's transaction).

**TRIGGER:** With two threads on one `PostgresPortalStateStore`, pause a `replace=True` save after its DELETE, then call `load_snapshot` from the other thread. Its unconditional `conn.commit()` commits the deletion before the writer can upsert the retained rows.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_portal_state_store.py::TestPostgresPortalStateStore::test_load_snapshot_returns_records` uses one `MagicMock` cursor with no open writer transaction; the Postgres suite never interleaves a read and write on the cached connection.

**PROPOSED TEST GATE:** Add `tests/python/test_portal_state_store.py::TestPostgresPortalStateStore::test_load_does_not_commit_inflight_write`, using a transaction-aware fake connection and two barriers; assert a read cannot call `commit` until the replacing writer exits successfully.

## 5. Verify persisted snapshot hashes and predecessor links when loading snapshots

**SEVERITY: P1**

**EVIDENCE:** `src/travel_plan_permission/snapshots.py:79-95` and `src/travel_plan_permission/snapshots.py:170-172`

```python
@model_validator(mode="after")
def _set_hashes(self) -> ValidationSnapshot:
    payload = {
        "trip_id": self.trip_id,
        "timestamp": self.timestamp.isoformat(),
        "policy_version": self.policy_version,
        "input_data": self.input_data,
        "results": [result.model_dump(mode="json") for result in self.results],
        "previous_hash": self.previous_hash,
    }
    content_hash = _hash_payload(payload)
    ...
    object.__setattr__(self, "snapshot_hash", content_hash)
    object.__setattr__(self, "chain_hash", chain_hash)
```

```python
def load_snapshot(self, path: str | Path) -> ValidationSnapshot:
    data = json.loads(self._confined_path(path).read_text(encoding="utf-8"))
    return ValidationSnapshot.model_validate(data)
```

Loading recomputes and overwrites the file's `snapshot_hash` and `chain_hash`; it never compares them to the serialized values or checks each `previous_hash` against the preceding file. An edited snapshot is therefore silently accepted as newly self-consistent, defeating the stated tamper-evidence property.

**TRIGGER:** Append a snapshot, edit its JSON `input_data.purpose` while leaving its saved hashes unchanged, then call `load_snapshot`. It returns a snapshot containing the edited purpose instead of raising an integrity error.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_snapshots.py::test_snapshot_chain_and_recheck` only links two snapshots produced in memory. The path-confinement tests vary traversal/symlink inputs, never valid in-store JSON whose content or predecessor hash was altered.

**PROPOSED TEST GATE:** Add `tests/python/test_snapshots.py::test_load_snapshot_rejects_content_hash_mismatch`; mutate `input_data` in an appended JSON file and assert `load_snapshot` raises `ValueError` mentioning the hash mismatch. Add a companion chain-link mismatch assertion in `load_trip_snapshots`.

## 6. Reject approval-packet cost breakdowns that disagree with the plan total

**SEVERITY: P1**

**EVIDENCE:** `src/travel_plan_permission/approval_packet.py:219-260`

```python
raw_costs = cost_breakdown or trip_plan.expense_breakdown
costs = {
    str(getattr(category, "value", category)): amount for category, amount in raw_costs.items()
}
if not costs and trip_plan.estimated_cost:
    costs["estimated_total"] = trip_plan.estimated_cost

history = tuple(approval_history or trip_plan.approval_history)
total_cost = sum(costs.values(), Decimal("0"))

base_context = {
    "trip": trip_plan,
    "total_cost": total_cost,
    "compliance_status": compliance_status,
    "history_count": len(history),
}
...
pdf_bytes = generate_packet_pdf(
    trip_plan=trip_plan,
    compliance_status=compliance_status,
    cost_breakdown=costs,
```

The optional caller-supplied breakdown becomes the packet's total without any reconciliation to `trip_plan.estimated_cost` or its authoritative breakdown. A packet can therefore solicit approval for a materially lower amount than the trip object later submitted.

**TRIGGER:** Build a packet for a plan with `estimated_cost=Decimal("1250")` and `cost_breakdown={"airfare": Decimal("1")}`. The manager email, PDF, and `ApprovalPacket.total_cost` say `$1.00`.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_approval_packet.py::test_manager_email_contains_required_fields` uses a breakdown equal to the sample plan's estimated cost; its fixtures never supply an inconsistent override.

**PROPOSED TEST GATE:** Add `tests/python/test_approval_packet.py::test_build_packet_rejects_cost_breakdown_that_disagrees_with_trip_total`; pass the mismatched values above and assert `ValueError` (or assert the packet uses the plan's canonical total after an explicit reconciliation policy is chosen).

## 7. Generate collision-resistant IDs for canonical trip submissions

**SEVERITY: P1**

**EVIDENCE:** `src/travel_plan_permission/canonical.py:121-127` and `src/travel_plan_permission/canonical.py:198-205`

```python
def _slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").upper()
    return cleaned or "TRAVELER"


def _default_trip_id(plan: CanonicalTripPlan) -> str:
    return f"TRIP-{plan.depart_date:%Y%m%d}-{_slugify(plan.traveler_name)}"
```

```python
return TripPlan(
    trip_id=_default_trip_id(plan),
    traveler_name=plan.traveler_name,
    department=plan.cost_center,
    destination=_format_destination(plan),
    departure_date=plan.depart_date,
    return_date=plan.return_date,
```

The canonical schema has no source ID, and the generated ID includes only traveler and departure date. Two different trips by the same traveler departing the same day collide, allowing proposal/persistence state keyed by trip ID to be overwritten or incorrectly associated.

**TRIGGER:** Submit canonical payloads for `Dana Analyst`, both departing `2026-10-01`, one to Chicago and one to Denver. Both convert to `TRIP-20261001-DANA-ANALYST`.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_canonical_trip_plan.py::test_load_trip_plan_payload_handles_canonical` only asserts that one fixture's ID starts with `TRIP-`; it never converts two same-day plans for the same traveler.

**PROPOSED TEST GATE:** Add `tests/python/test_canonical_trip_plan.py::test_canonical_conversion_generates_distinct_ids_for_distinct_same_day_trips`; vary destination/purpose while holding traveler and depart date fixed, and assert distinct IDs (or require a canonical caller-provided immutable ID).

## 8. Reject canonical trips whose return date precedes departure

**SEVERITY: P1**

**EVIDENCE:** `src/travel_plan_permission/canonical.py:81-110` and `src/travel_plan_permission/models.py:353-465`

```python
class CanonicalTripPlan(BaseModel):
    """Canonical TripPlan contract aligned to schemas/trip_plan.min.schema.json."""

    type: Literal["trip"]
    traveler_name: str = Field(..., min_length=1)
    business_purpose: str = Field(..., min_length=1)
    ...
    depart_date: date
    return_date: date
    event_registration_cost: Decimal | None = Field(default=None, ge=0)
```

```python
class TripPlan(BaseModel):
    ...
    departure_date: date = Field(..., description="Date of departure")
    return_date: date = Field(..., description="Date of return")
    purpose: str = Field(..., description="Business purpose of the trip")
    ...
    def duration_days(self) -> int:
        return (self.return_date - self.departure_date).days + 1
```

Neither model validates date ordering. The converted plan can have a zero or negative duration, which downstream duration, hotel, and per-diem computations can treat as a real trip rather than rejecting malformed travel dates.

**TRIGGER:** Canonical input with `depart_date=2026-02-03` and `return_date=2026-02-01` validates and converts; `duration_days()` returns `-1`.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_canonical_trip_plan.py::test_canonical_plan_validates` and all conversion fixtures use chronologically ordered dates; no test supplies an inverted pair.

**PROPOSED TEST GATE:** Add `tests/python/test_canonical_trip_plan.py::test_canonical_trip_plan_rejects_return_before_departure`; assert `CanonicalTripPlan.model_validate` raises `ValidationError` for the inverted dates.

## 9. Revalidate overrides in the deprecated minimal-conversion adapter

**SEVERITY: P1**

**EVIDENCE:** `src/travel_plan_permission/conversion.py:33-50`

```python
payload_dict = dict(payload)
payload_dict.setdefault("type", "trip")
plan_input = load_trip_plan_input(payload_dict)
overrides: dict[str, object] = {"trip_id": trip_id, "status": status}
if traveler_role is not None:
    overrides["traveler_role"] = traveler_role
...
if transportation_mode is not None:
    overrides["transportation_mode"] = transportation_mode

return plan_input.plan.model_copy(update=overrides)
```

Pydantic's `model_copy(update=...)` does not validate the update mapping. Although annotated, Python callers can pass `trip_id=None`, `status="not-a-status"`, or an invalid transport mode and receive a `TripPlan` instance with invalid field values that later consumers trust.

**TRIGGER:** Call `trip_plan_from_minimal(valid_payload, trip_id=None, status="not-a-status")`. It returns a plan whose `trip_id is None` and whose `status == "not-a-status"`.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_minimal_conversion.py::test_trip_plan_from_minimal_applies_overrides` supplies only `TripStatus.SUBMITTED` and a valid city; it never supplies malformed runtime values.

**PROPOSED TEST GATE:** Add `tests/python/test_minimal_conversion.py::test_trip_plan_from_minimal_validates_overrides`; call with `trip_id=None` and `status="not-a-status"`, and assert `ValidationError` rather than an invalid `TripPlan`.

## 10. Evaluate provider approval for the trip date, not the server's current date

**SEVERITY: P1**

**EVIDENCE:** `src/travel_plan_permission/policy_api.py:1447-1454` and `src/travel_plan_permission/providers.py:76-82`

```python
engine = PolicyEngine.from_file()
validator = PolicyValidator.from_runtime_config()
context = _context_from_plan(plan)
policy_results = engine.validate(context)
validation_results = validator.validate_plan(plan)
issues = [
    *[_issue_from_result(result) for result in policy_results if not result.passed],
    *[_issue_from_validation_result(result) for result in validation_results],
]
```

```python
def is_active(self, reference_date: date | None = None) -> bool:
    """Return True when the provider contract is active for the reference date."""

    check_date = reference_date or date.today()
    if check_date < self.valid_from:
        return False
    return not (self.valid_to and check_date > self.valid_to)
```

`check_trip_plan` does not pass `plan.departure_date` to the validation layer. Provider approval therefore defaults to `date.today()`, unlike `list_allowed_vendors`, which explicitly uses the planned departure date. A future-trip provider can be incorrectly rejected before its contract begins, or an expired-on-travel-date provider can be accepted today.

**TRIGGER:** With today's date before a provider's `valid_from`, submit a plan departing after `valid_from` and selecting that provider. `check_trip_plan` produces an unapproved-provider issue even though the contract is active on departure.

**WHY EXISTING TESTS MISS IT:** `tests/python/test_validation.py::TestProviderApprovalRule::test_skips_when_provider_is_approved_for_destination` explicitly supplies a matching `reference_date`; `tests/python/test_policy_api.py` does not vary provider contract validity relative to the plan's departure date through `check_trip_plan`.

**PROPOSED TEST GATE:** Add `tests/python/test_policy_api.py::test_check_trip_plan_uses_departure_date_for_provider_contract`; monkeypatch a registry with a provider active only on the plan's future departure date, then assert no provider-approval issue.
