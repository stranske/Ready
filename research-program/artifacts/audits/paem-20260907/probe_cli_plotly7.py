import json,subprocess,os
from pathlib import Path
import yaml
b=Path('/Users/teacher/.codex/automations/research-program')
r=b/'clones/Portable-Alpha-Extension-Model'
out=b/'artifacts/audits/paem-20260907/cli-plotly7-proof';out.mkdir(exist_ok=True)
config={'N_SIMULATIONS':100,'N_MONTHS':12,'financing_mode':'per_path','sweep':{'method':'grid','parameters':{'theta_extpa':{'values':[0.5]}}}}
(out/'config.yaml').write_text(yaml.safe_dump(config))
cmd=['/tmp/paem-audit-plotly7-venv/bin/python','-m','pa_core.cli','--config',str(out/'config.yaml'),'--index',str(r/'data/sp500tr_fred_divyield.csv'),'--output',str(out/'out.xlsx'),'--bundle',str(out/'bundle'),'--seed','123','--index-frequency','daily','--log-json']
env=dict(os.environ,PYTHONPATH=str(r))
with (out/'cli.log').open('w') as f:p=subprocess.run(cmd,cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=90)
print(json.dumps({'returncode':p.returncode,'log':str(out/'cli.log')},indent=2))
assert p.returncode != 0
assert "unexpected keyword argument 'engine'" in (out/'cli.log').read_text()
