from pathlib import Path
from datetime import date
import json,tempfile
from counter_risk.gui.runner import GuiRunState,_validate_path_roots,execute_gui_run
from counter_risk.runner_launch import data_quality_status_label
out=Path(__file__).parent
with tempfile.TemporaryDirectory(prefix='cr-gui-observation-') as root:
 p=Path(root)
 default_hint=_validate_path_roots(GuiRunState(as_of_date='2025-12-31',input_root=str(p/'missing'),output_root=str(p)))[1]
 def controlled_runner(args):
  run=Path(args[args.index('--output-dir')+1]);run.mkdir(parents=True)
  (run/'DATA_QUALITY_SUMMARY.txt').write_text('Overall status: fail (RED) - Do not send.\n')
  return 0
 state=GuiRunState(as_of_date='2025-11-15',input_root=str(p),output_root=str(p))
 r=execute_gui_run(state=state,runner=controlled_runner,temp_dir=p,cleanup_settings_file=True)
 observations={'missing_input_message':default_hint,'offcycle_date_selected':'2025-11-15','actual_cli_date':r.cli_args[r.cli_args.index('--as-of-date')+1],'data_quality_color':r.data_quality_color,'data_quality_label':r.data_quality_status,'status_labels':{x:data_quality_status_label(x) for x in ['GREEN','YELLOW','RED']},'limitation':'Function-level controls, fake runner; not Windows/Tk/Excel end-to-end.'}
 (out/'operator-observations.json').write_text(json.dumps(observations,indent=2));print(json.dumps(observations,indent=2))
