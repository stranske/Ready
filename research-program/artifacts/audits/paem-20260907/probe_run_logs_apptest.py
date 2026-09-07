import os,json,tempfile
from pathlib import Path
from streamlit.testing.v1 import AppTest
page=Path('/Users/teacher/.codex/automations/research-program/clones/Portable-Alpha-Extension-Model/dashboard/pages/7_Run_Logs.py')
with tempfile.TemporaryDirectory() as td:
 p=Path(td);(p/'runs/run-selected').mkdir(parents=True);(p/'runs/run-selected/run.log').write_text('selected run log\n');(p/'manifest.json').write_text(json.dumps({'run':'WRONG_UNRELATED_RUN'}));os.chdir(p)
 at=AppTest.from_file(str(page)).run(timeout=20)
 assert not at.exception
 shown=[str(c.value) for c in at.code]
 print(json.dumps({'selected':at.selectbox[0].value,'rendered_code':shown},indent=2))
 assert any('WRONG_UNRELATED_RUN' in x for x in shown)
