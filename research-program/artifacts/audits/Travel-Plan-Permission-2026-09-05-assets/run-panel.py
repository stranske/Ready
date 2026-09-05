import sys,json
from pathlib import Path
sys.path.insert(0,'/Users/teacher/.codex/orchestrator-mirror')
import ux_review
p=Path(__file__).resolve().parent
bundle=json.loads((p/'bundle.json').read_text())
report=ux_review.review(bundle,evaluators=['codex','cursor','gemini','vibe'],adversary='cursor',timeout=420)
(p/'report.json').write_text(json.dumps(report,indent=2))
(p/'improvements.json').write_text(json.dumps(ux_review.synthesize_improvements(report),indent=2))
print('Panel and improvement artifacts written')
