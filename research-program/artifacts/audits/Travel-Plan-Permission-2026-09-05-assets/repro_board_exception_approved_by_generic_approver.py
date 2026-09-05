"""Show that a generic approve credential can approve a board-level exception."""

import os
from decimal import Decimal

from fastapi.testclient import TestClient

from travel_plan_permission.http_service import PlannerProposalStore, create_app
from travel_plan_permission.models import ExceptionRequest, ExceptionStatus, ExceptionType
from travel_plan_permission.planner_auth import Permission, mint_bootstrap_token


def main() -> None:
    os.environ.update(
        {
            "TPP_BASE_URL": "http://testserver",
            "TPP_OIDC_PROVIDER": "google",
            "TPP_AUTH_MODE": "bootstrap-token",
            "TPP_BOOTSTRAP_SIGNING_SECRET": "bootstrap-secret-123",
        }
    )
    store = PlannerProposalStore()
    draft = store.save_portal_draft({"traveler_name": "Alice"})
    store.create_exception_request(
        draft.draft_id,
        ExceptionRequest(
            type=ExceptionType.ADVANCE_BOOKING,
            justification="Business need documented with sufficient detail for approval.",
            requestor="Alice",
            amount=Decimal("20000"),
        ),
    )
    token = mint_bootstrap_token(
        subject="ordinary-approver",
        permissions=(Permission.APPROVE,),
        provider="google",
        secret="bootstrap-secret-123",
        expires_in_seconds=600,
    )

    response = TestClient(create_app(store)).post(
        f"/portal/admin/exceptions/{draft.draft_id}/0/decision",
        data={"actor_id": "ordinary-approver", "decision": "approve"},
        headers={"Authorization": f"Bearer {token}"},
        follow_redirects=False,
    )
    updated = store.list_exception_requests(draft.draft_id)[0]

    assert response.status_code == 303, response.text
    assert updated.status == ExceptionStatus.APPROVED
    assert updated.approval is not None and updated.approval.level.value == "board"
    print("generic approve credential approved a board-level exception")


if __name__ == "__main__":
    main()
