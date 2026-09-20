import json,subprocess,time,re
from pathlib import Path
b=Path(__file__).resolve().parent
selected=json.loads((b/'selection.json').read_text())['selected']
def call(args,out):
 if out.exists(): return out.read_text()
 p=subprocess.run(['gh']+args,capture_output=True,text=True)
 if p.returncode:
  (b/'collection-error.txt').write_text(' '.join(args)+'\n'+p.stderr)
  raise SystemExit(p.stderr)
 out.write_text(p.stdout);time.sleep(0.7);return p.stdout
for p in selected:
 repo=p['repo'];n=p['number'];d=b/(repo+'-'+str(n));d.mkdir(exist_ok=True)
 pr=json.loads(call(['pr','view',str(n),'-R','stranske/'+repo,'--json','number,title,body,mergedAt,mergeCommit,headRefOid,closingIssuesReferences,comments,reviews,files,statusCheckRollup'],d/'pr.json'))
 call(['pr','diff',str(n),'-R','stranske/'+repo],d/'diff.patch')
 call(['api','repos/stranske/'+repo+'/commits/'+pr['mergeCommit']['oid']+'/check-runs?per_page=100'],d/'merge-checks.json')
 issues={x['number'] for x in pr['closingIssuesReferences']}
 # Explicit same-repository target references. Other contextual refs are examined by reviewer.
 explicit={3425:3351,3437:3354,3432:3431,3436:3433,3439:3438,3424:3389,3440:3435,3445:1836,3451:3450,3443:3434,3444:3441}
 if repo=='Workflows' and n in explicit:issues.add(explicit[n])
 if repo=='Deliverable-Render':issues.add(2)
 if repo=='Doc-Lineage':issues.add(6)
 if repo=='Portable-Alpha-Extension-Model':issues.add(2296)
 for issue in sorted(issues):
  call(['issue','view',str(issue),'-R','stranske/'+repo,'--json','number,title,body,state,labels,comments,url'],d/('issue-'+str(issue)+'.json'))
 print(repo,n,'files',len(pr['files']),'issues',sorted(issues),flush=True)
 time.sleep(1)
