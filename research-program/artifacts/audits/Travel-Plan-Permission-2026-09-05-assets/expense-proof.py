from pathlib import Path
import sys,json,re,csv,io
root=Path(__file__).resolve().parents[3];repo=root/'clones/Travel-Plan-Permission'
sys.path[:0]=[str(repo),str(repo/'src')]
from fastapi.testclient import TestClient
from tests.python.test_http_service import _seed_manager_review,_expense_form_payload
from travel_plan_permission.http_service import create_app,PlannerProposalStore
store=PlannerProposalStore();_seed_manager_review(store)
client=TestClient(create_app(store));payload=_expense_form_payload();payload['expense_vendor']='=1+1';payload['expense_amount']='7500';payload['receipt_total']='7500'
r=client.post('/portal/expenses/review',data=payload,follow_redirects=False);draft=r.headers['location'].split('/')[-1]
detail=client.get(r.headers['location']);export=client.get(f'/portal/expenses/{draft}/artifacts/expense-csv')
row=list(csv.DictReader(io.StringIO(export.text)))[0]
result={'anonymous_create':r.status_code,'anonymous_detail':detail.status_code,'anonymous_export':export.status_code,'policy_warning':'Policy warning' in detail.text,'exported_row':row,'draft_id':draft}
# Unknown request is rejected, showing that the missing auth check is distinct from linkage validation.
payload['approved_request_id']='NO-SUCH-REQUEST';result['unknown_link_control']=client.post('/portal/expenses/review',data=payload).status_code
print(json.dumps(result,indent=2))
