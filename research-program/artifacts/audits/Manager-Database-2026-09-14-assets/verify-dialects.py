import os,sqlite3,shutil,json
from pathlib import Path
import llm
from ui import dashboard,daily_report
from chains.rag_search import RAGSearchChain
p=Path(__file__).parent
results={}
for key in ['manager_id','id']:
 db=p/f'dialect-{key}.sqlite';shutil.copyfile(p/'demo/manager_demo.sqlite',db)
 with sqlite3.connect(db) as c:
  if key=='id': c.execute('ALTER TABLE managers RENAME COLUMN manager_id TO id')
  c.execute('DROP VIEW IF EXISTS mv_daily_report')
 os.environ.pop('DB_URL',None);os.environ.pop('DATABASE_URL',None);os.environ['DB_PATH']=str(db)
 dashboard.load_managers.clear();daily_report.load_news.clear();daily_report.load_diffs.clear()
 r={'manager_rows':len(dashboard.load_managers()),'qc_rows':len(dashboard.load_all_managers_summary()['stale_managers']),'news_rows':len(daily_report.load_news('2026-03-15'))}
 try:r['diff_rows']=len(daily_report.load_diffs('2026-03-15'))
 except Exception as e:r['diff_error']=str(e)
 with sqlite3.connect(db) as c:
  chain=RAGSearchChain(db_conn=c);r['rag_catalog']=chain._manager_catalog();r['entities']=chain._entity_extraction('What does Elliott Investment Management L.P. hold?')
 results[key]=r
p.joinpath('dialect-results.json').write_text(json.dumps(results,indent=2,default=str));print(json.dumps(results,indent=2,default=str))
assert results['manager_id']['manager_rows']==2 and results['id']['manager_rows']==0
assert results['manager_id']['news_rows']==1 and results['id']['news_rows']==0
assert results['manager_id']['diff_rows']==2 and 'm.manager_id' in results['id']['diff_error']
assert results['manager_id']['rag_catalog'] and not results['id']['rag_catalog']
assert results['manager_id']['qc_rows']>0 and results['id']['qc_rows']==0
