import os,sys,tempfile,json
from pathlib import Path
from unittest.mock import patch
root=Path('/Users/teacher/.codex/automations/research-program/clones/Fine-Art-Archive')
sys.path[:0]=[str(root/'src'),str(root)]
# Keep any API initialization and rendering inside disposable synthetic storage.
with tempfile.TemporaryDirectory(prefix='faa-audit-resume-') as tmp:
 for key in ['FAA_WORKS_DIR','FAA_STAGING_DIR','FAA_ART_WORKS_ROOT','FAA_IMAGE_CACHE_DIR','FAA_DATA_DIR']:
  os.environ[key]=tmp
 from fine_art_archive.selection.lenses import allocate,allocate_monthly
 from fine_art_archive.quality.source_quality import score_for
 from fine_art_archive.crosswalk import to_linked_art
 from fine_art_archive.provenance import _field_value,completeness_report
 from fine_art_archive.parsers.dimension_utils import parse_dimension_pair
 from fine_art_archive.preference.bradley_terry import next_pair
 from fine_art_archive.api import main
 from scripts import build_manifest,rank_known_works
 from PIL import Image
 results={}
 def probe(name,fn):
  try: results[name]={'result':repr(fn())}
  except Exception as e:results[name]={'exception':type(e).__name__,'message':str(e)}
 shares={'canon':float('nan'),'atypicality':1.0}
 probe('689-allocate-nan',lambda:allocate(10,list(shares),shares))
 probe('689-monthly-nan',lambda:allocate_monthly(10,list(shares),shares,monthly_cap=100,spent={}))
 probe('689-zero-control',lambda:allocate(10,['canon','atypicality'],{'canon':0.,'atypicality':1.}))
 rec={'empirical':{},'first_seen':'2026-08-01T12:00:00'}
 probe('690-naive',lambda:score_for('s','c',aggregates={'sources':{'s':{'c':rec}}}))
 meta={'work_id':'test','title':'test','artist':{'name':'Test','canonical':{'wikidata_q':'Q123'}},'year':None,'year_min':1563}
 probe('691-canonical',lambda:to_linked_art(meta)['produced_by']['carried_out_by'])
 probe('692-3d-mm',lambda:parse_dimension_pair('535 x 463 x 52 mm'))
 probe('694-canonical',lambda:_field_value(meta,'artist_qid'))
 probe('696-year',lambda:build_manifest._row('test',meta)['year'])
 probe('697-none',lambda:next_pair(['a','b'],[],strengths={'a':None,'b':1.}))
 probe('697-nan-selection',lambda:next_pair(['a','b','c'],[],strengths={'a':float('nan'),'b':1.,'c':1.}))
 with patch.object(rank_known_works,'gather',return_value=[]),patch.dict(os.environ,{'FAA_WORKS_DIR':tmp}):
  os.environ.pop('FAA_STAGING_DIR',None)
  try:rank_known_works.main(['--artist-qid','Q123','--missing-only'])
  except SystemExit as e:results['695-missing-only']={'system_exit':e.code}
 imagepath=Path(tmp)/'sample.png';Image.new('RGB',(100,100)).save(imagepath)
 with patch.object(main,'IMAGE_CACHE_DIR',Path(tmp)/'cache'):
  probe('693-zero',lambda:main._serve_resized(imagepath,'sample',0))
  response=main._serve_resized(imagepath,'sample',100000000)
  with Image.open(response.path) as im:results['693-huge-no-upscale']={'size':im.size}
 from fastapi.testclient import TestClient
 with patch.object(main,'_serve_resized'):
  # OpenAPI is sufficient to verify declared request bounds without touching corpus.
  schema=main.app.openapi()['paths']['/variant_upgrades/{existing_wid}/candidate_image']['get']['parameters']
  results['693-query-schema']=[v for v in schema if v['name']=='max']
 print(json.dumps(results,indent=2))
