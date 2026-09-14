import os,json,importlib.metadata
from pathlib import Path
from streamlit.testing.v1 import AppTest
os.environ.pop('DB_URL',None);os.environ.pop('DATABASE_URL',None)
os.environ['UI_USERNAME']='audit';os.environ['UI_PASSWORD']='synthetic-audit-password'
os.environ['USE_SIMPLE_EMBED']='1'
os.environ['DB_PATH']=str(Path(__file__).parent/'demo/manager_demo.sqlite')
a=AppTest.from_file(str(Path.cwd()/'ui/app.py')).run(timeout=20)
r={'authenticator':importlib.metadata.version('streamlit-authenticator'),'exceptions':[x.message for x in a.exception]}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2));print(r)
assert any('Hasher.__init__' in s for s in r['exceptions'])
