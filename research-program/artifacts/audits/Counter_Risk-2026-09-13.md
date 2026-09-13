# Counter_Risk research audit — 2026-09-13

Unit: D-audit-Counter_Risk--2026-09-13T18-41-41Z  
Status: research complete; eight issue bodies staged, none filed  
Verified clone and remote main: 6e2a87b27be9a23d388155e37ed01675b1e27dc7  
Completed research: 2026-09-13T19:30:49.576074+00:00

Eight retained findings (2 P1, 6 P2) establish new failures at identity, aggregation, parser, chat, provenance, and output-order boundaries. Prior September fixes were deduplicated against 85 recent issue bodies, a fresh open inventory, and a focused historical chat search. The supply trigger was 1 <= 2; this research-only executor does not claim to have replenished GitHub supply.

| Draft | Priority | Finding | Verified behavior | Evidence and draft |
| --- | --- | --- | --- | --- |
| 01 | P1 | Registry alias skips a fail-severity cap | 200 exposure /100 cap: alias has no breach; canonical spelling breaches by 100. | [evidence]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/lead-numerical-seams.json) / [body]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/issue-bodies/01.md) |
| 02 | P1 | Split counterparties understate concentration | HHI 0.16942149 vs0.31818182; Top5 0.68181818 vs0.72727273 after consolidation. | [evidence]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/lead-numerical-seams.json) / [body]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/issue-bodies/02.md) |
| 03 | P2 | Malformed maturity amount becomes zero | Real XLSX Total=not-a-number parses as 0.0 instead of rejecting input. | [evidence]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/lead-numerical-seams.json) / [body]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/issue-bodies/03.md) |
| 04 | P2 | Live chat loses change-delta facts | Computed DeltaOnlyBank 876543.21 is absent from actual LangChain invoke messages. | [evidence]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/lead-chat-delta-proof.json) / [body]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/issue-bodies/04.md) |
| 05 | P2 | PPT status confuses refresh with generation | Distribution exists and succeeds while summary says generation skipped; yellow refresh warning itself remains justified. | [evidence]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/verified-ppt-status.txt) / [body]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/issue-bodies/05.md) |
| 06 | P2 | PDF request disappears under conflicting flags | export_pdf=True + distribution=False yields no PDF and no warning. | [evidence]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/verified-export-pdf.txt) / [body]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/issue-bodies/06.md) |
| 07 | P2 | Optional source hashes are missing | Valid PNG and maturity XLSX missing from provenance enumeration; production consumers confirmed. | [evidence]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/lead-numerical-seams.json) / [body]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/issue-bodies/07.md) |
| 08 | P2 | PDF export precedes concentration-slide append | Real fixture pipeline export source has 23 slides; final PPTX has 24. PDF rendering intercepted, not exercised. | [evidence]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/lead-final-deck-proof.json) / [body]([LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/issue-bodies/08.md) |

## Verification and limits

- All eight bodies pass the actual repository issue-format validator with zero advisories. Every cited source path and line was opened; extracts are in cited-line-evidence.json. Draft labels are bug plus priority:high for P1 or priority:normal for P2, verified present in the repo. No remote format-guard verdict is claimed because nothing was filed.
- Orientation: 26,119 first-party Python lines; 2,109 tests collected. Current-SHA Python 3.12/3.13, Ruff, format and mypy checks succeed in [Python CI](https://github.com/stranske/Counter_Risk/actions/runs/34768897975); the similarly named older ci.yml runs were not used as current evidence.
- Local operator, chat and fixture checks: 145 passed in 126.22 seconds. A focused overlapping subset had 142 passed; these are not additive. Numerical offload recorded 92 passed in affected modules. Independent lead proofs exercise real pipeline reshapers, a real malformed XLSX, valid PNG validation, final chat transport, and the complete fixture pipeline to the PDF generator boundary. The seven-file synthetic demo artifact command succeeded and output paths were checked.
- Cursor offload completed successfully. Codex offload returned dispatcher OFFLOAD_INCOMPLETE despite a finished nonempty report/proof packet; its findings were retained only after independent validation. Its stated Top5=1.0 was wrong: the correct consolidated result is 160/220. Raw reports are preserved as reviewer evidence and are superseded by this synthesis.
- Browser connection timed out twice before DOM/screenshots. Windows frozen GUI, Runner workbook macros, and real Excel/PowerPoint COM execution are unverified. Function controls show missing-input guidance and RED/Do not send status correctly. The PDF proof records the exported source, not rendered PDF pages.
- Source remains unchanged; pre-existing untracked dossier-out and uv.lock remain. No source edits, PRs, issue publication, labels, or intake measurement rows. Raw agent transcripts are local under logs/D-audit-Counter_Risk--2026-09-13T18-41-41Z, outside the mirrored research artifact tree.

## Coverage across eight dimensions

| Dimension | Outcome |
| --- | --- |
| 1 Correctness | Drafts 01–03; finite/bool issues already fixed were discarded. |
| 2 Duplication | Five identical demo helper bodies and one table iterator pair confirmed by AST. No demonstrated behavior divergence; consolidation deferred rather than manufactured as a defect. |
| 3 Wiring | Drafts 04,06–08 plus canonical identity matching. |
| 4 UX | Function/CLI observations and a four-evaluator panel; complete visual/platform coverage unavailable. Drafts 04–06. See UX report and handoff. |
| 5 Public-field comparison | Risk-data completeness and traceability favor preserving rejected inputs and input identity; advisory benchmark, not a claim that bank-specific regulation applies to this tool. |
| 6 Opportunities | Effective-input lineage, shared run-envelope/identity adapter, and a static manifest review hub are staged roadmap options, not existing failures. |
| 7 Tools | Property-based split/merge and alias-invariance tests are a useful next increment; Office recalculation must stay an explicit platform test. No package or service added. |
| 8 Local automation | Research queue owns one claim; repo-owned CI green; synced workflow internals remain Workflows-owned. Duplicate-looking draft publication is prevented by research-only staging. No lane wakeup. |

## Adjudications and next work

The original-config-versus-generated-input snapshot mismatch (W-1) is real, but replacing the original config is not necessarily correct. The original raw NISA inputs are already hashed. Defer this to an additive effective-input lineage design with a stated replay contract, not a P1 defect. W-5's speculative external-relationship concern is replaced by the verified PDF/PPT slide mismatch (draft 08). GUI off-cycle help conflicts with month-end normalization; keep the monthly calculation behavior and defer a small wording clarification.

The panel's raw overall score is 3.0 (medians: wiring 4, usability 6, help 6, productivity 6), with four nonempty evaluator outputs and a nonempty Cursor critic. These scores cover supplied function evidence only; they do not rate unseen application screens. Its three overlapping chat findings collapse into draft 04, rated P2 because core reporting still works. The aggregate mixed unrelated date hints into chat findings; hints were reviewed individually. Gate reports not done because Gate 1 is unavailable, score below 7, and panel blockers. This is an explicit product-readiness gap, not a claim that the research unit is incomplete.

Publishing/implementation can begin with canonical limit identity and concentration aggregation, followed by the six P2 drafts. Actual Windows and browser acceptance follow the handoff brief. No owner decision is required to finish this research unit.
