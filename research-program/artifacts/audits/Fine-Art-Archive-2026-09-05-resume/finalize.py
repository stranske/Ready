from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,shutil
base=Path('/Users/teacher/.codex/automations/research-program');out=base/'artifacts/audits/Fine-Art-Archive-2026-09-05-resume'
canonical=Path('/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Fine-Art-Archive')
now=datetime.now(timezone.utc).isoformat();unit='D-audit-Fine-Art-Archive--2026-09-05T04-00-31Z'
root=base/'clones/Fine-Art-Archive'
validation=[]
for f in sorted((out/'corrected-issue-bodies').glob('*.md')):
 p=subprocess.run([str(root/'.venv/bin/python'),'.github/scripts/issue_format.py',str(f)],cwd=root,capture_output=True,text=True,check=True)
 assert 'advisories' not in p.stdout,p.stdout
 validation.append({'file':f.name,'exit':0,'verdict':p.stdout.strip()})
(out/'corrected-body-validation.json').write_text(json.dumps(validation,indent=2))
guards=json.loads((out/'guards.json').read_text());issues=json.loads((out/'issues.json').read_text())
rows=[]
for i in sorted(issues,key=lambda x:x['number']):
 if not 689<=i['number']<=697:continue
 matches=[g for g in guards if g['displayTitle']==i['title'] and g['conclusion']=='success']
 verdict='No successful remote guard: cancelled/skipped only'
 if matches:
  g=matches[0];verdict=f"[Passed{' with advisory' if i['number'] in [691,693,694,696] else ''}]({g['url']})"
 rows.append(f"| [#{i['number']}]({i['url']}) | {i['state']} | {verdict} |")
report=f'''# Fine-Art-Archive audit — resumed delivery reconciliation

Unit: `{unit}`. Attempt: 2. Completed research reconciliation: {now}.
Verified clone HEAD and live remote main: `d149861964fa4093d4228ef424853fa5de1dced0`.

The prior executor's unit-specific checkpoint had reached Phase 5 and already filed nine issues. This run continued that checkpoint, verified the existing delivery, and staged corrected bodies. It created no issues, dispatched no agents, changed no repository code, and added no duplicate intake rows. The executor's research-only instruction takes precedence over the brief's filing instruction.

## What the artifact establishes

All nine recorded issue URLs exist and are open. All nine intake-log rows exist exactly once. The prior full SHA `d149861e60f089868be5aa28373bdf5d3513a290` was incorrect; the SHA above is verified with git and remote Actions. The tracked checkout remains unchanged; the pre-existing untracked dossier-out directory was preserved.

Synthetic read-only probes reproduced the NaN allocator exceptions (#689), offset-naive timestamp exception (#690), missing canonical artist URI (#691), tenfold 3D millimetre parsing error (#692), max=0 resize HTTP 500 plus missing query bounds (#693), missing canonical conflict kept value (#694), missing-only CLI exit 2 despite FAA_WORKS_DIR (#695), blank manifest year despite year_min (#696), and explicit None strength TypeError / NaN first-pair retention (#697). Evidence and reproducible probe source are in `{out}`.

Material corrections:
- #689: zero shares do not establish a crash and retain documented lens-floor behavior. Corrected body targets non-finite/negative inputs without prohibiting valid zero weights.
- #693: a huge max did not upscale a 100 by 100 fixture; request-sized allocation was not established. The zero-size failure and missing declared bounds are confirmed. Two shortened main.py citations were expanded to real repo-relative paths.
- #694: completeness status counts still use field_provenance; the defect concerns kept_value in conflict detail for canonical-only records. Corrected the malformed symbol-as-path citation.
- #697: None violates the declared dict[str, float] input type. No production next_pair caller was found in src or scripts. Retain as low-priority defensive hardening; do not describe it as a production outage. NaN can retain the first pair rather than simply dropping all pairs.
- Removed other bare-file citation advisories from the staged bodies. The repository's actual format validator passes all nine corrected bodies without advisories. They are staged corrections for existing issues, not new issue candidates, and have not been published.

## Existing remote format evidence

| Issue | State | Remote format verdict |
|---|---|---|
'''+ '\n'.join(rows)+f'''

The eight passing results above were verified in the validation step's log, not inferred from workflow success alone. #689's remote format validation remains unproven; its corrected local body passes. No rerun or issue edit was sent from this research-only role. None of the nine has a needs-human label in this snapshot; their labels are bug/enhancement, priority, and testing only, so this report does not claim nine newly dispatched or agent-ready jobs.

## Scope and coverage limits

This is a resumed correctness-refill audit, not a fresh whole-repository audit. The dossier supplied scope: versioned software and policy, with artwork masters/live sidecars external. Historical issue inventory (150 open/recently closed records) was checked for overlap: #695 is a remaining CLI default case after #671; #690 is a timestamp edge case in #673's source-quality path; #691 is a canonical-identifier gap after #249's crosswalk delivery. No further issues were filed.

The retained checkpoint claimed all eight dimensions and 1,899 passing tests. No raw full-suite execution log was retained alongside this audit; that test count is prior-executor reporting, not independently confirmed here. This run used direct bounded reproduction instead of repeating the full suite. D1 correctness, D2 root-helper consolidation, D3 wiring, and D6 manifest metadata received concrete source/probe checks. D4 has API function/OpenAPI observations only: no rendered-browser capture or UX panel, so no usability score or full UX completion claim. D5 confirms a local crosswalk projection gap, not a current public-field survey. D7 has the actual format validator, not a tool-market comparison. D8 has local CLI maintenance behavior, not fleet capacity/effectiveness measurement. Broader UX, public-field/tool research and local-fleet effectiveness remain deferred beyond this recovery; no new evidence is implied by the inherited eight-dimension headings.

## Handoff

Use the corrected bodies in `{out/'corrected-issue-bodies'}` when a publishing-capable lane next reconciles existing issues #689–697. Prioritize #689/#690 correctness; treat #697 as optional defensive hardening. Confirm #689's remote guard when an authorized lane next edits/revalidates it. The audit is research-complete with these explicit limitations; implementation and publishing of corrections are separate work.

Canonical recovery report: `{canonical/'2026-09-05-resume-reconciliation.md'}`.
'''
(base/'artifacts/audits/Fine-Art-Archive-2026-09-05.md').write_text(report)
(canonical/'2026-09-05-resume-reconciliation.md').write_text(report)
shutil.copytree(out/'corrected-issue-bodies',canonical/'2026-09-05-corrected-issue-bodies',dirs_exist_ok=True)
for path in [canonical/'2026-09-05-verification-log.md',canonical/'2026-09-05-AUDIT_REPORT.md',canonical/'README.md',canonical.parent/'AUDIT_LEDGER.md']:
 with path.open('a') as f:f.write(f'\n\n## {now} — Codex attempt-2 reconciliation\nContinued {unit} from completed Phase 5; nine existing issues verified, eight remote guard passes (four with path advisories), #689 remote guard unproven. Corrected full SHA to d149861964fa4093d4228ef424853fa5de1dced0. Nine corrected local bodies pass actual repo validator without advisories. Narrowed #689/#693/#694/#697 claims; no new filing, dispatch, code change, or duplicate intake entry. Full-suite and comprehensive UX/field/tool/fleet claims remain unverified. The current qualification of the prior report is [resume reconciliation]({canonical/"2026-09-05-resume-reconciliation.md"}). Next: publishing-capable lane applies staged corrections and validates #689 remotely.\n')
for checkpoint in [base/'artifacts/audits/CHECKPOINT.md',base/f'artifacts/audits/{unit}.CHECKPOINT.md']:
 with checkpoint.open('a') as f:f.write(f'\n## {now} — Attempt 2 Phase 3–5 reconciliation completed\nReopened every cited source location and reproduced bounded behavior; corrected SHA and overclaims. Verified nine existing issue URLs and intake entries, eight remote guard verdicts, #689 guard unproven. Nine staged corrected bodies pass actual validator without advisories. OUT and canonical recovery report written; ledger and index appended. No repository edits, new issue filing, dispatch, or duplicate intake writes. Broader audit dimensions explicitly qualified. Ready for program.py done.\n')
print('OUT written; canonical reports and checkpoints appended; 9/9 corrected bodies pass without advisories.')
