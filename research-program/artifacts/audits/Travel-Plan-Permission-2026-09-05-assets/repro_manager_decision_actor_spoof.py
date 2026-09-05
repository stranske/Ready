"""Show a valid approver token can record a manager decision as another person."""

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from travel_plan_permission.http_service import PlannerProposalStore, create_app
from travel_plan_permission.models import TripPlan
from travel_plan_permission.planner_auth import Permission, mint_bootstrap_token
from travel_plan_permission.policy_api import check_trip_plan, get_policy_snapshot
from travel_plan_permission.review_workflow import ReviewRequest, ReviewStatus


def main() -> None:
    os.environ.update(
        {
            "TPP_BASE_URL": "http://testserver",
            "TPP_OIDC_PROVIDER": "google",
            "TPP_AUTH_MODE": "bootstrap-token",
            "TPP_BOOTSTRAP_SIGNING_SECRET": "bootstrap-secret-123",
        }
    )
    fixture = Path("tests/fixtures/planner_integration/proposal_submission.json")
    trip_plan = TripPlan.model_validate(json.loads(fixture.read_text(encoding="utf-8")))
    now = datetime.now(UTC)
    review = ReviewRequest(
        review_id="review-1",
        draft_id="draft-1",
        trip_plan=trip_plan,
        policy_snapshot=get_policy_snapshot(trip_plan),
        policy_result=check_trip_plan(trip_plan),
        status=ReviewStatus.PENDING_MANAGER_REVIEW,
        submitted_at=now,
        updated_at=now,
    )
    store = PlannerProposalStore()
    store.manager_reviews.reviews_by_id[review.review_id] = review
    store.manager_reviews.review_ids_by_draft_id[review.draft_id] = review.review_id
    token = mint_bootstrap_token(
        subject="authenticated-approver",
        permissions=(Permission.APPROVE,),
        provider="google",
        secret="bootstrap-secret-123",
        expires_in_seconds=600,
    )

    response = TestClient(create_app(store)).post(
        "/portal/manager/reviews/review-1/decision",
        data={
            "actor_id": "forged-manager-id",
            "action": "approve",
            "rationale": "Approved after review.",
        },
        headers={"Authorization": f"Bearer {token}"},
        follow_redirects=False,
    )
    updated = store.lookup_manager_review("review-1")

    assert response.status_code == 303, response.text
    assert updated is not None
    assert updated.trip_plan.approval_history[-1].approver_id == "forged-manager-id"
    print("authenticated-approver recorded the decision as forged-manager-id")


if __name__ == "__main__":
    main()
