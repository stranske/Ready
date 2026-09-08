from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json,os,sys
from counter_risk.build import release
from counter_risk.runtime_paths import resolve_runtime_path
from counter_risk.chat import session

with TemporaryDirectory(prefix='counter-risk-audit-') as d:
 root=Path(d)/'source';out=Path(d)/'release';root.mkdir();(root/'release.spec').write_text('# synthetic existing spec')
 dist=root/'dist/counter-risk';dist.mkdir(parents=True)
 (dist/release._executable_filename()).write_text('bootloader sentinel')
 (dist/'libpython-sentinel.dll').write_text('runtime dependency')
 (dist/'config').mkdir();(dist/'config/all_programs.yml').write_text('bundled: true')
 with patch.object(release,'_run_pyinstaller',lambda *_: None):exe=release._copy_bundled_executable(root,out)
 print('COPY:',json.dumps({'copied_exe':exe.is_file(),'runtime_copied':(exe.parent/'libpython-sentinel.dll').exists(),'config_copied':(exe.parent/'config/all_programs.yml').exists()}))
 # A corrected complete one-dir tree includes config at sys._MEIPASS, per actual spec.
 with patch.object(sys,'frozen',True,create=True),patch.object(sys,'_MEIPASS',str(dist),create=True),patch.object(sys,'executable',str(dist/release._executable_filename())),patch.dict(os.environ,{'COUNTER_RISK_BUNDLE_ROOT':str(dist)}):
  print('COMPLETE_TREE_CONFIG_CONTROL:',resolve_runtime_path('config/all_programs.yml').read_text())
 print('CHAT_PARSE_NAN:',session._parse_float(float('nan')))
 print('CHAT_FORMAT_NAN:',session._format_exposure_value(float('nan')))
launcher=Path('clones/Counter_Risk/run_counter_risk_gui.cmd').read_text()
print('GUI_BIN_LOOKUP_PRESENT:',r'%~dp0bin\counter-risk.exe' in launcher)
print('CLI_BIN_LOOKUP_PRESENT:',r'bin\counter-risk.exe' in Path('clones/Counter_Risk/src/counter_risk/build/release.py').read_text().replace('\\\\','\\'))
