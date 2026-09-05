import os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root/'clones/Travel-Plan-Permission/src'))
os.environ.update(TPP_BASE_URL='http://127.0.0.1:38473',TPP_OIDC_PROVIDER='google',TPP_AUTH_MODE='static-token',TPP_ACCESS_TOKEN='synthetic-audit-token',TPP_HANDOFF_SIGNING_SECRET='synthetic-audit-signing-material')
from travel_plan_permission.http_service import create_app,PlannerProposalStore
import uvicorn
app=create_app(PlannerProposalStore())
uvicorn.run(app,host='127.0.0.1',port=38473,access_log=False)
