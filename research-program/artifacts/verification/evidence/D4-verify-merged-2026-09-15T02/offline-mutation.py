import sys,pytest
from pathlib import Path
root=Path.cwd();sys.path.insert(0,str(root/'src'))
import deliverable_render.html as html
original=html._CSS
try:
 html._CSS += '</style><link rel="stylesheet" href="https://example.invalid/break.css"><style>'
 broken=pytest.main(['tests/test_render_html_offline.py','-k','no_external_resource_references','-q','-o','addopts='])
finally:html._CSS=original
restored=pytest.main(['tests/test_render_html_offline.py','-k','no_external_resource_references','-q','-o','addopts='])
print('DELIBERATE_BREAK_EXIT',broken,'RESTORED_EXIT',restored)
assert broken==1 and restored==0
