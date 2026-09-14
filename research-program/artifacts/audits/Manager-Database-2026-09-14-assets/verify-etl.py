import os,sqlite3,tempfile,json,asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from datetime import date
os.environ['USE_SIMPLE_EMBED']='1'
os.environ['RAW_DIR']=str(Path(__file__).parent/'raw')
os.environ.pop('DB_URL',None);os.environ.pop('DATABASE_URL',None)
from etl.point_in_time import holdings_as_of
from diff_holdings import _select_authoritative_filings
from embeddings import store_document,search_documents
from etl.news_flow import inserted_news_items,persist_news,emit_news_spike_alerts
import etl.edgar_flow as edgar
import etl.news_flow as news
r={}
c=sqlite3.connect(':memory:');c.row_factory=sqlite3.Row
c.executescript("CREATE TABLE filings(filing_id INTEGER PRIMARY KEY,manager_id INT,type TEXT,period_end TEXT,filed_date TEXT); CREATE TABLE holdings(holding_id INTEGER PRIMARY KEY,filing_id INT,cusip TEXT,knowledge_time TEXT,superseded_at TEXT);")
c.executemany('INSERT INTO filings VALUES(?,?,?,?,?)',[(1,7,'13F-HR/A','2024-03-31','2024-05-15'),(2,7,'13F-HR','2024-03-31','2024-05-15')])
c.executemany('INSERT INTO holdings VALUES(?,?,?,?,?)',[(1,1,'AMENDED','2024-05-15T12:00:00Z',None),(2,2,'ORIGINAL','2024-05-15T12:00:00Z',None)])
r['pit']={'returned':[x['cusip'] for x in holdings_as_of(c,7,date(2024,5,16))],'diff_selector':_select_authoritative_filings(7,c)}
assert r['pit']['returned']==['ORIGINAL'] and r['pit']['diff_selector'][0][1]==1
c.close()
with tempfile.TemporaryDirectory() as td:
 path=str(Path(td)/'documents.sqlite')
 c=sqlite3.connect(path);c.execute('CREATE TABLE managers(manager_id INTEGER PRIMARY KEY,name TEXT)');c.executemany('INSERT INTO managers VALUES(?,?)',[(1,'one'),(2,'two')]);c.commit();c.close()
 ids=[store_document('same audit memo',path,manager_id=i) for i in [1,2]]
 c=sqlite3.connect(path);r['documents']={'ids':ids,'owners':c.execute('SELECT manager_id FROM documents').fetchall()};c.close()
 os.environ['DB_PATH']=path
 r['documents']['manager2_results']=len(search_documents('same audit memo',db_path=path,manager_id=2))
 assert ids[0]==ids[1] and r['documents']['manager2_results']==0
n=sqlite3.connect(':memory:');n.execute('CREATE TABLE news_items(manager_id INT,published_at TEXT,source TEXT,headline TEXT,url TEXT,body_snippet TEXT,topics TEXT,confidence REAL)')
item={'manager_id':1,'published_at':'2026-01-01T00:00:00Z','source':'rss','headline':'duplicate','url':'https://example.invalid/audit-news','body_snippet':'','topics':[],'confidence':0.1}
items=[dict(item),dict(item)];candidates=inserted_news_items(items,n);stored=persist_news.fn(items,n);captured=[]
async def capture(conn,event):captured.append(event.payload);return []
with patch.object(news,'fire_alerts_for_event',capture):asyncio.run(emit_news_spike_alerts(candidates,n))
r['news']={'candidates':len(candidates),'stored':stored,'alert_payload':captured};assert stored==1 and captured[0]['news_count']==2
n.close()
class FakeAdapter:
 async def list_new_filings(self,*args):return [{'accession':'audit','filed':'2024-05-01','form':'13F-HR'}]
 async def download(self,*args):return '<xml>synthetic orphan audit</xml>'
 async def parse(self,*args):return []
def boom(*args,**kwargs):raise RuntimeError('audit forced filing write failure')
with tempfile.TemporaryDirectory() as td:
 path=str(Path(td)/'edgar.sqlite')
 c=sqlite3.connect(path);c.execute('CREATE TABLE managers(manager_id INTEGER PRIMARY KEY,name TEXT,cik TEXT)');c.execute("INSERT INTO managers VALUES(1,'one','0000000001')");edgar._ensure_legacy_tables(c);c.commit();c.close()
 with patch.object(edgar,'DB_PATH',path),patch.object(edgar,'ADAPTER',FakeAdapter()),patch.object(edgar,'S3',SimpleNamespace(put_object=lambda **kw:None)),patch.object(edgar,'_upsert_filing_legacy',boom):
  try:asyncio.run(edgar.fetch_and_store.fn('0000000001','2024-01-01'))
  except RuntimeError as e:assert 'audit forced' in str(e)
 c=sqlite3.connect(path);r['edgar']={'documents':c.execute('SELECT COUNT(*) FROM documents').fetchone()[0],'filings':c.execute('SELECT COUNT(*) FROM filings').fetchone()[0]};c.close()
 assert r['edgar']=={'documents':1,'filings':0}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
