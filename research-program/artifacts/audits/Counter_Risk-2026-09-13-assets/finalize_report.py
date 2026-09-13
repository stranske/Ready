from pathlib import Path
from datetime import datetime,timezone
import json,shutil
b=Path('/Users/teacher/.codex/automations/research-program');p=b/'artifacts/audits/Counter_Risk-2026-09-13-assets';out=b/'artifacts/audits/Counter_Risk-2026-09-13.md';aud=Path('/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits');dest=aud/'Counter_Risk';unit='D-audit-Counter_Risk--2026-09-13T18-41-41Z';now=datetime.now(timezone.utc).isoformat();sha='6e2a87b27be9a23d388155e37ed01675b1e27dc7'
issues=json.load(open(p/'staged-issues.json'));loc=sum(json.load(open(p/'orientation.json'))['source_loc_by_parent'].values())
rows=[('01','P1','Registry alias skips a fail-severity cap','200 exposure /100 cap: alias has no breach; canonical spelling breaches by100.','lead-numerical-seams.json'),('02','P1','Split counterparties understate concentration','HHI0.16942149 vs0.31818182; Top5 0.68181818 vs0.72727273 after consolidation.','lead-numerical-seams.json'),('03','P2','Malformed maturity amount becomes zero','Real XLSX Total=not-a-number parses as0.0 instead of rejecting input.','lead-numerical-seams.json'),('04','P2','Live chat loses change-delta facts','Computed DeltaOnlyBank876543.21 is absent from actual LangChain invoke messages.','lead-chat-delta-proof.json'),('05','P2','PPT status confuses refresh with generation','Distribution exists and succeeds while summary says generation skipped; yellow refresh warning itself remains justified.','verified-ppt-status.txt'),('06','P2','PDF request disappears under conflicting flags','export_pdf=True + distribution=False yields no PDF and no warning.','verified-export-pdf.txt'),('07','P2','Optional source hashes are missing','Valid PNG and maturity XLSX missing from provenance enumeration; production consumers confirmed.','lead-numerical-seams.json'),('08','P2','PDF export precedes concentration-slide append','Real fixture pipeline export source has23 slides; final PPTX has24. PDF rendering intercepted, not exercised.','lead-final-deck-proof.json')]
table='\n'.join(f'| {i} | {pr} | {title} | {proof} | [evidence]({p/evidence}) / [body]({p/"issue-bodies"/(i+".md")}) |' for i,pr,title,proof,evidence in rows)
report=f'''# Counter_Risk research audit — 2026-09-13

Unit: {unit}  
Status: research complete; eight issue bodies staged, none filed  
Verified clone and remote main: {sha}  
Completed research: {now}

Eight retained findings (2 P1, 6 P2) establish new failures at identity, aggregation, parser, chat, provenance, and output-order boundaries. Prior September fixes were deduplicated against 85 recent issue bodies, a fresh open inventory, and a focused historical chat search. The supply trigger was 1 <= 2; this research-only executor does not claim to have replenished GitHub supply.

| Draft | Priority | Finding | Verified behavior | Evidence and draft |
| --- | --- | --- | --- | --- |
{table}

## Verification and limits

- All eight bodies pass the actual repository issue-format validator with zero advisories. Every cited source path and line was opened; extracts are in cited-line-evidence.json. Draft labels are bug plus priority:high for P1 or priority:normal for P2, verified present in the repo. No remote format-guard verdict is claimed because nothing was filed.
- Orientation: {loc:,} first-party Python lines; 2,109 tests collected. Current-SHA Python3.12/3.13, Ruff, format and mypy checks succeed in [Python CI](https://github.com/stranske/Counter_Risk/actions/runs/34768897975); the similarly named older ci.yml runs were not used as current evidence.
- Local operator, chat and fixture checks:145 passed in126.22 seconds. A focused overlapping subset had142 passed; these are not additive. Numerical offload recorded92 passed in affected modules. Independent lead proofs exercise real pipeline reshapers, a real malformed XLSX, valid PNG validation, final chat transport, and the complete fixture pipeline to the PDF generator boundary. The seven-file synthetic demo artifact command succeeded and output paths were checked.
- Cursor offload completed successfully. Codex offload returned dispatcher OFFLOAD_INCOMPLETE despite a finished nonempty report/proof packet; its findings were retained only after independent validation. Its stated Top5=1.0 was wrong: the correct consolidated result is160/220. Raw reports are preserved as reviewer evidence and are superseded by this synthesis.
- Browser connection timed out twice before DOM/screenshots. Windows frozen GUI, Runner workbook macros, and real Excel/PowerPoint COM execution are unverified. Function controls show missing-input guidance and RED/Do not send status correctly. The PDF proof records the exported source, not rendered PDF pages.
- Source remains unchanged; pre-existing untracked dossier-out and uv.lock remain. No source edits, PRs, issue publication, labels, or intake measurement rows. Raw agent transcripts are local under logs/{unit}, outside the mirrored research artifact tree.

## Coverage across eight dimensions

| Dimension | Outcome |
| --- | --- |
| 1 Correctness | Drafts01–03; finite/bool issues already fixed were discarded. |
| 2 Duplication | Five identical demo helper bodies and one table iterator pair confirmed by AST. No demonstrated behavior divergence; consolidation deferred rather than manufactured as a defect. |
| 3 Wiring | Drafts04,06–08 plus canonical identity matching. |
| 4 UX | Function/CLI observations and a four-evaluator panel; complete visual/platform coverage unavailable. Drafts04–06. See UX report and handoff. |
| 5 Public-field comparison | Risk-data completeness and traceability favor preserving rejected inputs and input identity; advisory benchmark, not a claim that bank-specific regulation applies to this tool. |
| 6 Opportunities | Effective-input lineage, shared run-envelope/identity adapter, and a static manifest review hub are staged roadmap options, not existing failures. |
| 7 Tools | Property-based split/merge and alias-invariance tests are a useful next increment; Office recalculation must stay an explicit platform test. No package or service added. |
| 8 Local automation | Research queue owns one claim; repo-owned CI green; synced workflow internals remain Workflows-owned. Duplicate-looking draft publication is prevented by research-only staging. No lane wakeup. |

## Adjudications and next work

The original-config-versus-generated-input snapshot mismatch (W-1) is real, but replacing the original config is not necessarily correct. The original raw NISA inputs are already hashed. Defer this to an additive effective-input lineage design with a stated replay contract, not a P1 defect. W-5's speculative external-relationship concern is replaced by the verified PDF/PPT slide mismatch (draft08). GUI off-cycle help conflicts with month-end normalization; keep the monthly calculation behavior and defer a small wording clarification.

The panel's raw overall score is3.0 (medians: wiring4, usability6, help6, productivity6), with four nonempty evaluator outputs and a nonempty Cursor critic. These scores cover supplied function evidence only; they do not rate unseen application screens. Its three overlapping chat findings collapse into draft04, rated P2 because core reporting still works. The aggregate mixed unrelated date hints into chat findings; hints were reviewed individually. Gate reports not done because Gate1 is unavailable, score below7, and panel blockers. This is an explicit product-readiness gap, not a claim that the research unit is incomplete.

Publishing/implementation can begin with canonical limit identity and concentration aggregation, followed by the six P2 drafts. Actual Windows and browser acceptance follow the handoff brief. No owner decision is required to finish this research unit.
'''
# Space numeric tokens for readability.
for a,c in [('HHI0','HHI 0'),('by100','by 100'),('as0','as 0'),('Bank876','Bank 876'),('has23','has 23'),('has24','has 24'),('Python3','Python 3'),('checks:145','checks: 145'),('in126','in 126'),('had142','had 142'),('recorded92','recorded 92'),('is160','is 160'),('is3.0','is 3.0'),('wiring4','wiring 4'),('usability6','usability 6'),('help6','help 6'),('productivity6','productivity 6'),('Gate1','Gate 1'),('below7','below 7'),('draft08','draft 08'),('draft04','draft 04'),('Drafts01','Drafts 01'),('Drafts04','Drafts 04')]:report=report.replace(a,c)
out.write_text(report);(dest/'2026-09-13-AUDIT_REPORT.md').write_text(report)
roadmap='''# Public field, opportunities, tooling and automation

The BCBS risk-data principles emphasize accuracy, completeness and reliable reporting. This is a useful engineering comparison for this file-based reporting tool, not a claim of regulatory applicability or compliance. Drafts01–03 and07 address concrete mismatches with those aims. [BIS principles](https://www.bis.org/publications/201301-guidelines-principles-effective-risk-data-aggregation-and-risk-reporting).

Near-term test opportunity: define invariance under splitting/merging a counterparty, replacing an alias with a canonical key, and toggling an unrelated output option. Hypothesis generates inputs and simplifies failing examples; a narrowly scoped dev-only trial on concentration and limit properties would be testable without a new production service. Existing fixed regression examples should remain. [Hypothesis documentation](https://hypothesis.readthedocs.io/en/latest/).

Office artifact verification remains platform-specific. openpyxl's data_only reads cached values; it is not a recalculation result. Retain file-level checks locally and require the existing Windows COM path for rendering/recalculation acceptance rather than substituting another unverified Office runtime. [openpyxl tutorial](https://openpyxl.readthedocs.io/en/3.1/tutorial.html).

Roadmap decisions: (1) add effective-input lineage beside original config, including generated NISA-derived workbooks; original inputs remain necessary for replay. (2) Add a run-envelope adapter and shared provider IDs only against the existing fleet contracts; source search confirms no run.json emission today, while its contract explicitly describes staging, so this is not a new defect. (3) A static, no-server manifest review hub fits the work-environment response: local Python, COM, and local HTML already work there. No need to assume WASM availability. First acceptance should be one synthetic run reviewed by a colleague; avoid a broad hosted migration unless a specific goal requires it.

AST duplication: five demo helper bodies are identical across demo_artifact and web_demo, plus the limits/rollups table iterator. No change proposed until an actual divergence or shared-test payoff is demonstrated.

Automation inspection: current branch checked via direct remote SHA and current check-runs, fresh issue inventory saved, and one queue unit claimed. The repo AGENTS contract identifies Workflows as owner of synced infrastructure. Shared opener/closer automation prompts mention Counter_Risk, but this audit has no authority to wake lanes. The Research Program instruction to stage issue bodies overrides the generic brief's filing step; no intake row is valid without a filed URL. No provider-capacity shortage was observed; the numerical dispatch falsely reported incomplete despite a complete report, so only independently reproduced content was banked. This incident is a local telemetry/workflow observation, not a Counter_Risk code issue.
'''
(p/'roadmap-and-tools.md').write_text(roadmap);(dest/'2026-09-13-roadmap-and-tools.md').write_text(roadmap)
ux=f'''# Counter_Risk UX evidence and handoff

Coverage is partial. [Bundle]({p/'bundle.json'}), [panel]({p/'report.json'}), [improvement hints]({p/'improvements.json'}), [gate]({p/'gate.json'}). Four evaluator rubric files and the critic are nonempty under /Users/teacher/.codex/orchestrator-mirror/ux_reviews/stranske_Counter_Risk_uxreview_2026-09-13-function-surfaces.

| Surface | Driven | Evidence or blocker |
| --- | --- | --- |
| Maintainer CLI help | yes | cli-help.txt; console entry succeeds. python -m counter_risk is not the documented entry and was discarded as a bad probe. |
| Fixture download generation | yes | demo-output and demo-proof.txt;145 operator/demo/chat tests pass. |
| GUI function control | yes, controlled runner | operator-observations.json; missing-input guidance, month-end normalization and status-label reading. No Tk visual inference. |
| Chat delta provider transport | yes, intercepted final transport | lead-chat-delta-proof.json; omitted facts. Actual LLM answer not observed. |
| Browser fixture page | no | Browser connection timed out twice; no DOM/screenshot, no browser usability conclusion. |
| Windows frozen GUI | no | No Windows host. |
| Runner.xlsm and COM | no | No Excel/PowerPoint Windows runtime. |

Raw medians: wiring4, usability6, help6, productivity6; overall3.0. Gate not done. These are function-evidence scores, not a full app rating. Aggregate chat findings are duplicates; retain one P2 draft. Reject trusted-block suggestion for untrusted delta text; preserve guarded data delimiters. Retain link-refresh-specific message wording without requiring green status. Defer date-help wording to clarify month-end behavior, rather than changing domain semantics without a contract.

The initial controlled RED summary fixture omitted the expected parenthesized color and produced empty status. That was an invalid probe, not a product defect. The corrected fixture returns RED - Do not send; operator-observations.json contains that corrected observation. The original panel bundle is preserved as its input record; no finding depends on the invalid status probe.

## Platform acceptance handoff

At source SHA {sha}, use the repo's documented portable build and launch commands from docs/gui_runner.md and run_counter_risk_gui.cmd. On Windows launch from a folder outside the repository; exercise all, ex_trend and trend modes, manual and discover inputs, ambiguous discovery selection, missing roots, a second same-date run, and Open Output/Manifest/Summary/PPT. Open Runner.xlsm and exercise all seven macros. Verify selected/effective date is explicit, newly written files open from the completed run, and RED blocks distribution operationally. Save screenshots, executed command, exit code and manifest into a dated platform-verification artifact folder.

For draft08, enable export_pdf and include_concentration_table_in_ppt together on a synthetic fixture: final PPTX and rendered PDF must contain the same concentration slide and counts; repeat with each toggle disabled. Capture real PDF pages and PowerPoint output. Browser handoff: serve web locally with python -m http.server, open index, capture DOM and screenshot and verify the fixture-only boundary; do not score real-file upload/processing that the static page does not claim to implement.
'''
(dest/'2026-09-13-UX_REVIEW.md').write_text(ux);(p/'UX_REVIEW.md').write_text(ux)
verify='\n'.join(f'- {i} {title}: STAGED, priority {pr}; proof {ev}; no GitHub issue created.' for i,pr,title,proof,ev in rows)
verify+='\n- W-1: DEFERRED with reason; original config preserves user input and raw NISA already hashed; additive lineage needs a defined contract.\n- W-5: REPLACED by draft08 with final export-boundary proof.\n- AST duplicate helpers: DEFERRED, no observed behavior divergence.\n- Old finite/bool/mixed-sign/packaging/gui/discovery findings: REFUTED or DUPLICATE against current source.\n- Risk proxy prior-volatility and signed unused breakdown helper: INSUFFICIENT evidence of a current contract failure.\n- GUI date guidance: DEFERRED wording correction; keep month-end semantics.\n- Browser and Windows visual/platform checks: HANDOFF, environment unavailable.\n- No candidate was silently dropped; raw offload reports are subordinate to this adjudication.\n'
(dest/'2026-09-13-verification-log.md').write_text(verify);(p/'verification-log.md').write_text(verify)
bodydest=dest/'2026-09-13-issue-bodies';bodydest.mkdir(exist_ok=True)
for f in (p/'issue-bodies').glob('*.md'):shutil.copy2(f,bodydest/f.name)
with (aud/'AUDIT_LEDGER.md').open('a') as f:f.write(f'\n- {now} Counter_Risk {unit}: RESEARCH COMPLETE at {sha}; eight verified drafts (2 P1/6 P2),8/8 local format PASS without advisories. Eight dimensions considered; browser/Windows coverage incomplete with handoff.145 local tests passed, independent proofs,4-evaluator function panel. No source edits/PRs/issue filing/intake rows. Report {out}; canonical Counter_Risk/2026-09-13-AUDIT_REPORT.md. Next: publish/implement drafts01–02 first and run platform acceptance.\n')
with (dest/'README.md').open('a') as f:f.write(f'\n### 2026-09-13 — research complete\nEight staged bodies,2 P1/6 P2, zero-advisory format checks. See 2026-09-13-AUDIT_REPORT.md, 2026-09-13-verification-log.md, 2026-09-13-UX_REVIEW.md, 2026-09-13-roadmap-and-tools.md, and 2026-09-13-issue-bodies/. No issues filed.\n')
for path in [b/'artifacts/audits/CHECKPOINT.md',b/f'artifacts/audits/{unit}.CHECKPOINT.md']:
 with path.open('a') as f:f.write(f'\n## {now} {unit} Phase 5 complete\nOUT and Code/Audits report/index/ledger,8 bodies, source extracts, dedup inventory, verification dispositions, roadmap, UX panel and platform handoff written. Source unchanged at remote6e2a87b. Research complete; close unit next.\n')
print('wrote',out,'bytes',out.stat().st_size,'source LOC',loc)
