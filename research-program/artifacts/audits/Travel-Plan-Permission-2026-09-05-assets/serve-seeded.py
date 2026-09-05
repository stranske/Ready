import os,sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[3];repo=root/'clones/Travel-Plan-Permission';sys.path[:0]=[str(repo),str(repo/'src')]
os.environ.update(TPP_BASE_URL='http://127.0.0.1:38474',TPP_OIDC_PROVIDER='google',TPP_AUTH_MODE='bootstrap-token',TPP_BOOTSTRAP_SIGNING_SECRET='bootstrap-secret-123',TPP_HANDOFF_SIGNING_SECRET='synthetic-audit-signing-material')
from travel_plan_permission.http_service import create_app,PlannerProposalStore
from travel_plan_permission.planner_auth import mint_bootstrap_token
from travel_plan_permission.security import Permission
from tests.python.test_http_service import _seed_manager_review,_expense_form_payload
store=PlannerProposalStore();_seed_manager_review(store)
p=Path(__file__).resolve().parent
(p/'synthetic-expense.json').write_text(json.dumps(_expense_form_payload()))
t=mint_bootstrap_token(subject='audit-reviewer',permissions=tuple(Permission),provider='google',secret='bootstrap-secret-123',expires_in_seconds=600)
(p/'synthetic-auth.json').write_text(json.dumps({'Authorization':'Bearer '+t}))
import uvicorn
uvicorn.run(create_app(store),host='127.0.0.1',port=38474,access_log=False)
