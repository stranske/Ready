from pathlib import Path
from datetime import datetime
import tempfile,json,math,os
from openpyxl import Workbook
from PIL import Image
from counter_risk.compute.rollups import compute_concentration_metrics
from counter_risk.compute.limits import check_limits,find_missing_limit_entities
from counter_risk.pipeline.run import _build_concentration_exposure_rows,_build_limit_exposure_rows,_resolve_input_paths,_resolve_screenshot_input_mapping
from counter_risk.parsers.exposure_maturity_schedule import parse_exposure_maturity_schedule
from counter_risk.config import load_config
art=Path(__file__).resolve().parent
os.chdir(art.parents[2]/'[LOCAL_WORKSPACE]/Counter_Risk')
split=[{'counterparty':'Alpha','Notional':60},{'counterparty':'Alpha','Notional':60}]+[{'counterparty':f'Beta-{i}','Notional':10} for i in range(10)]
merged=[{'counterparty':'Alpha','Notional':120}]+split[2:]
def concentration(rows):return compute_concentration_metrics(_build_concentration_exposure_rows({'all':{'totals':rows}})).to_dict('records')[0]
a,b=concentration(split),concentration(merged)
assert math.isclose(b['top5_share'],160/220) and math.isclose(b['hhi'],15400/48400)
assert a['hhi']<b['hhi'] and a['top5_share']<b['top5_share']
limits={'schema_version':1,'limits':[{'entity_type':'counterparty','entity_name':'bank_of_america','limit_kind':'absolute_notional','limit_value':100,'severity':'fail'}]}
ex=_build_limit_exposure_rows({'all':{'totals':[{'counterparty':'Bank of America, NA','Notional':200}],'futures':[]}})
actual=check_limits(ex,limits).to_dict('records');assert not actual
control=[{**ex[0],'counterparty':'bank_of_america'}]
assert len(check_limits(control,limits))==1
with tempfile.TemporaryDirectory(prefix='cr-seams-',dir=art) as tmp:
 p=Path(tmp);w=Workbook();s=w.active;s.title='Exposure Maturity Schedule'
 for row,col,val in [(4,7,'Px Date'),(4,8,datetime(2025,11,30)),(10,3,'NISA TIPS'),(11,6,'Total'),(14,2,datetime(2026,1,8)),(14,6,'not-a-number'),(15,2,'Total')]:s.cell(row,col,val)
 source=p/'invalid-schedule.xlsx';w.save(source)
 schedule=parse_exposure_maturity_schedule(source);assert schedule.rows[0].total==0
 image=p/'actual.png';Image.new('RGB',(8,8)).save(image)
 cfg=load_config(Path('config/fixture_replay.yml')).model_copy(update={'enable_screenshot_replacement':True,'screenshot_inputs':{'synthetic_section':image},'exposure_summary_xlsx':source})
 assert _resolve_screenshot_input_mapping(cfg)['synthetic_section']==image
 paths=_resolve_input_paths(cfg); assert image not in paths.values() and source not in paths.values()
 result={'split_concentration':a,'aggregated_control':b,'canonical_alias_missing':find_missing_limit_entities(ex,limits),'alias_breaches':actual,'canonical_control_breaches':check_limits(control,limits).to_dict('records'),'real_xlsx_invalid_total_parsed':schedule.rows[0].total,'valid_png_and_maturity_xlsx_in_input_hash_mapping':False,'correction':'Raw offload expected Top5=1.0 was wrong; correct Top5 is160/220=0.7272727. HHI remains0.3181818.'}
 (art/'lead-numerical-seams.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
