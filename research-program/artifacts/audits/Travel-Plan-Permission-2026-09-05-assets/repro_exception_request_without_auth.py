"""Show that an unauthenticated client can attach an exception to a portal draft."""

from fastapi.testclient import TestClient

from travel_plan_permission.http_service import PlannerProposalStore, create_app


def main() -> None:
    store = PlannerProposalStore()
    draft = store.save_portal_draft({"traveler_name": "Alice"})
    response = TestClient(create_app(store)).post(
        f"/portal/review/{draft.draft_id}/exceptions",
        data={
            "exception_type": "advance_booking",
            "amount": "100",
            "justification": "Business need documented with sufficient detail for approval.",
        },
        follow_redirects=False,
    )

    requests = store.list_exception_requests(draft.draft_id)
    assert response.status_code == 303, response.text
    assert len(requests) == 1 and requests[0].requestor == "Alice"
    print(f"unauthenticated client created an exception on draft {draft.draft_id}")


if __name__ == "__main__":
    main()
