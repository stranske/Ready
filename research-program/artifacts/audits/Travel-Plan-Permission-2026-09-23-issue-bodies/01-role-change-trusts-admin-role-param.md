## Why (verified evidence)

`SecurityModel.approve_role_change` and `reject_role_change` authorize using only the caller-supplied `admin_role` enum; `admin_actor` is logged but never resolved to a role assignment. Any code path that can invoke these methods while passing `RoleName.SYSTEM_ADMIN` can approve or reject role elevation without the actor actually holding an admin role.

- `src/travel_plan_permission/security.py:443-467` — checks `admin_role in {SYSTEM_ADMIN, POLICY_ADMIN}` only; no lookup for `admin_actor`.
- `src/travel_plan_permission/security.py:490-514` — same pattern on reject.
- Reproduction on tip `3aee8e8`: `request_role_change` for `bob` → `FINANCE_ADMIN`, then `approve_role_change(admin_actor="eve", admin_role=RoleName.SYSTEM_ADMIN, ...)` succeeds although Eve was never registered as an admin.

Distinct from #1570 (non-terminal replay); this is impersonation via an unauthenticated role parameter.

## Tasks

- [ ] In `src/travel_plan_permission/security.py:443-535`, resolve `admin_actor` to an assigned role (or consult the same identity map the portal uses) and require that resolved role is admin before mutating `request.state`.
- [ ] Reject calls where `admin_role` disagrees with the resolved role for `admin_actor` (treat as authorization failure, audit, `PermissionError`).
- [ ] Mirror the same guard on `reject_role_change`.

## Acceptance Criteria

- Named test: `tests/python/test_security_model.py::test_role_change_approval_derives_admin_role_from_actor` — security model with `eve` mapped to `RoleName.APPROVER` only; `approve_role_change("eve", RoleName.SYSTEM_ADMIN, request_id)` raises `PermissionError` and leaves the request `PENDING_APPROVAL`.
- Deliberate-break → revert: restore the admin_role-only check → named test FAILS → revert.

## Non-Goals

- Do NOT change exception-tier or portal session auth in this issue.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Reproduction:_
```python
from travel_plan_permission.security import SecurityModel, RoleName, AuditLog
sec = SecurityModel(audit_log=AuditLog())
req = sec.request_role_change(requester="alice", target_user="bob", new_role=RoleName.FINANCE_ADMIN)
sec.approve_role_change(admin_actor="eve", admin_role=RoleName.SYSTEM_ADMIN, request_id=req.request_id)
# Observed: APPROVED. Expected: PermissionError for non-admin eve.
```

_Surfaced by Track D repo-audit 2026-09-23; verified by live Python reproduction on clone tip._
