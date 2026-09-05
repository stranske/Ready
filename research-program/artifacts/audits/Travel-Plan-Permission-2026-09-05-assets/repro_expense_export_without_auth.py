"""Reproduce an unauthenticated expense-export download at the audited SHA."""

from decimal import Decimal

from fastapi.testclient import TestClient

from travel_plan_permission.http_service import (
    PlannerProposalStore,
    PortalArtifact,
    create_app,
)
from travel_plan_permission.models import ExceptionRequest, ExceptionType


def main() -> None:
    store = PlannerProposalStore()
    approved_draft = store.save_portal_draft({"traveler_name": "Alice"})
    approved_request = ExceptionRequest(
        type=ExceptionType.ADVANCE_BOOKING,
        justification="Business need documented with sufficient detail for approval.",
        requestor="Alice",
        amount=Decimal("100"),
    )
    approved_request.approve(approver_id="manager")
    store.create_exception_request(approved_draft.draft_id, approved_request)
    draft = store.save_expense_draft(
        {
            "approved_request_id": approved_draft.draft_id,
            "trip_id": "trip-1",
            "traveler_name": "Alice",
            "expense_description": "Hotel",
            "expense_category": "lodging",
            "expense_amount": "250.00",
            "expense_date": "2026-09-01",
        }
    )
    store.cache_expense_artifacts(
        draft.draft_id,
        {
            "expense-csv": PortalArtifact(
                filename="expense.csv",
                content=b"date,vendor,amount\n2026-09-01,Hotel,250.00\n",
                media_type="text/csv",
            )
        },
    )
    client = TestClient(create_app(store))

    response = client.get(f"/portal/expenses/{draft.draft_id}/artifacts/expense-csv")

    assert response.status_code == 200, response.text
    assert response.content.startswith(b"date,vendor,amount")
    print(f"unauthenticated download succeeded for draft {draft.draft_id}")


if __name__ == "__main__":
    main()
