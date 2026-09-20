import json,subprocess,time
from pathlib import Path
b=Path(__file__).resolve().parent
root=Path.cwd()
for p in json.loads((b/'selection.json').read_text())['selected']:
 d=b/(p['repo']+'-'+str(p['number']));pr=json.loads((d/'pr.json').read_text());sha=pr['mergeCommit']['oid'];repo=p['repo']
 out=d/'push-runs.json'
 if not out.exists():
  r=subprocess.run(['gh','api',f'repos/stranske/{repo}/actions/runs?head_sha={sha}&event=push&per_page=100'],capture_output=True,text=True)
  if r.returncode: (b/'supplement-error.txt').write_text(r.stderr);raise SystemExit(r.stderr)
  out.write_text(r.stdout);time.sleep(1)
 runs=json.loads(out.read_text())['workflow_runs']
 print(repo,p['number'],[(r['name'],r['conclusion'],r['id']) for r in runs if 'ci' in r['name'].lower() or 'gate' in r['name'].lower() or 'publication' in r['name'].lower()],flush=True)
 clone=root/'clones'/repo
 check=subprocess.run(['git','-C',str(clone),'cat-file','-e',sha],capture_output=True)
 if check.returncode:
  r=subprocess.run(['git','-C',str(clone),'fetch','-q','origin',sha],capture_output=True,text=True)
  if r.returncode:print('FETCH FAILED',repo,r.stderr[:100],flush=True);continue
 # Capture merged tree content and CI paths locally; no checkout or code mutation.
 paths=[f['path'] for f in pr['files']]+['.github/workflows/ci.yml','.github/workflows/pr-00-gate.yml','pyproject.toml']
 for path in dict.fromkeys(paths):
  r=subprocess.run(['git','-C',str(clone),'show',sha+':'+path],capture_output=True)
  if r.returncode:continue
  dest=d/'merged'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(r.stdout)
