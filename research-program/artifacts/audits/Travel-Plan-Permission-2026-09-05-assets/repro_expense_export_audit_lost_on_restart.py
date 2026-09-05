"""Show that an expense export audit event is not persisted before a restart."""

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from decimal import Decimal

from fastapi.testclient import TestClient

from travel_plan_permission.http_service import (
    PlannerProposalStore,
    PortalArtifact,
    create_app,
)
from travel_plan_permission.models import ExceptionRequest, ExceptionType


def main() -> None:
    with TemporaryDirectory() as directory:
        state_path = Path(directory) / "portal.sqlite3"
        store = PlannerProposalStore(state_path=state_path)
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
                    content=b"date,vendor,amount\n",
                    media_type="text/csv",
                )
            },
        )

        response = TestClient(create_app(store)).get(
            f"/portal/expenses/{draft.draft_id}/artifacts/expense-csv"
        )
        assert response.status_code == 200, response.text
        assert any(event.outcome == "artifact_downloaded" for event in store.list_audit_events())

        restored = PlannerProposalStore(state_path=state_path)
        assert not any(
            event.outcome == "artifact_downloaded" for event in restored.list_audit_events()
        )
        print("expense export audit event disappears after restart")


if __name__ == "__main__":
    main()
