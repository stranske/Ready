from datetime import UTC, datetime, timedelta
from pathlib import Path
import json
from travel_plan_permission.models import ExceptionRequest, ExceptionType, TripPlan
from travel_plan_permission.policy_contract_models import PlannerPolicySnapshot, PolicyCheckResult
from travel_plan_permission.review_workflow import ReviewWorkflowStore, ReviewAction

def request():
 return ExceptionRequest(type=ExceptionType.ADVANCE_BOOKING,justification='Synthetic audit justification. '*4,requestor='audit',requested_at=datetime.now(UTC)-timedelta(hours=49))
r=request();r.approve(approver_id='first');r.reject()
print('1557 approve then reject:',r.status.value,'retained approver:',r.approval.approver_id)
r=request();r.reject();r.approve(approver_id='second');print('1557 reject then approve:',r.status.value)
r=request();print('1558 overdue before explicit helper:',r.status.value,r.approval_level.value);r.escalate_if_overdue();print('1558 explicit helper control:',r.status.value,r.approval_level.value)
f=Path('tests/fixtures/planner_integration')
p=TripPlan.model_validate_json((f/'proposal_submission.json').read_text())
s=PlannerPolicySnapshot.model_validate_json((f/'policy_snapshot_response.json').read_text())
result=PolicyCheckResult(status='pass',issues=[],policy_version='audit-v1')
store=ReviewWorkflowStore();a=store.create_or_get(draft_id='audit',trip_plan=p,policy_snapshot=s,policy_result=result)
store.apply_action(a.review_id,action=ReviewAction.REQUEST_CHANGES,actor_id='manager',rationale='Please update the trip.')
p2=p.model_copy(update={'traveler_name':'CHANGED-TRAVELER'})
b=store.create_or_get(draft_id='audit',trip_plan=p2,policy_snapshot=s,policy_result=result)
print('1559 resubmission:',json.dumps({'original':p.traveler_name,'submitted':p2.traveler_name,'stored':b.trip_plan.traveler_name,'status':b.status.value}))
assert b.trip_plan.traveler_name==p.traveler_name and b.trip_plan.traveler_name!=p2.traveler_name
