from pathlib import Path
from tempfile import TemporaryDirectory
import json,yaml
from counter_risk.limits_config import load_limits_config
from counter_risk.compute.limits import check_limits
from counter_risk.pipeline.run import _inject_repo_cash_into_cprs_ch
from counter_risk.reports.change_attribution import attribute_changes

with TemporaryDirectory(prefix='cr-audit-core-') as d:
 p=Path(d)/'limits.yml'
 for value in [50.0,float('inf')]:
  p.write_text(yaml.safe_dump({'schema_version':1,'limits':[{'entity_type':'counterparty','entity_name':'CIBC','limit_value':value,'limit_kind':'absolute_notional','severity':'fail'}]}))
  cfg=load_limits_config(p);rows=check_limits([{'counterparty':'CIBC','notional':100.}],cfg).to_dict(orient='records')
  print('LIMIT',value,'accepted',cfg.limits[0].limit_value,'breaches',len(rows))
for values in [[10.],[10.,20.]]:
 rows=[{'Segment':'repo','Counterparty':'CIBC','Cash':v,'Notional':v} for v in values]
 result=_inject_repo_cash_into_cprs_ch(rows,{'CIBC':100.})
 print('CASH',values,'=>',[r['Cash'] for r in result],'aggregate',sum(r['Cash'] for r in result))
for values in [[300.],[100.,200.]]:
 current=[{'counterparty':'CIBC','Notional':v} for v in values]
 result=attribute_changes(current,[{'counterparty':'CIBC','Notional':50.}])
 print('ATTRIBUTION',values,'=>',json.dumps([{k:r[k] for k in ['current_notional','prior_notional','notional_change']} for r in result['rows']]))
from counter_risk.pipeline.run import _write_change_attribution_outputs, _aggregate_cprs_ch_series_totals
import csv
with TemporaryDirectory(prefix='cr-audit-report-') as d:
 for case,current in [('single',[{'counterparty':'CIBC','Notional':300.,'NotionalChange':50.}]),('split',[{'counterparty':'CIBC','Notional':100.,'NotionalChange':25.},{'counterparty':'CIBC','Notional':200.,'NotionalChange':25.}])]:
  out=Path(d)/case;out.mkdir();warnings=[]
  artifacts=_write_change_attribution_outputs(run_dir=out,parsed_by_variant={'all_programs':{'totals':current}},warnings=warnings)
  with (out/'change_attribution.csv').open() as f:rows=list(csv.DictReader(f))
  print('PIPELINE_ATTRIBUTION',case,'sum_delta',sum(float(r['notional_change']) for r in rows),'sum_prior',sum(float(r['prior_notional']) for r in rows),'warnings',warnings)
 print('REAL_CASH_AGGREGATOR',_aggregate_cprs_ch_series_totals(records=_inject_repo_cash_into_cprs_ch([{'Segment':'repo','Counterparty':'CIBC','Cash':10.},{'Segment':'repo','Counterparty':'CIBC','Cash':20.}],{'CIBC':100.}),value_column='Cash'))
