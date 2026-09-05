# Fine-Art-Archive audit — resumed delivery reconciliation

Unit: `D-audit-Fine-Art-Archive--2026-09-05T04-00-31Z`. Attempt: 2. Completed research reconciliation: 2026-09-05T04:17:16.604641+00:00.
Verified clone HEAD and live remote main: `d149861964fa4093d4228ef424853fa5de1dced0`.

The prior executor's unit-specific checkpoint had reached Phase 5 and already filed nine issues. This run continued that checkpoint, verified the existing delivery, and staged corrected bodies. It created no issues, dispatched no agents, changed no repository code, and added no duplicate intake rows. The executor's research-only instruction takes precedence over the brief's filing instruction.

## What the artifact establishes

All nine recorded issue URLs exist and are open. All nine intake-log rows exist exactly once. The prior full SHA `d149861e60f089868be5aa28373bdf5d3513a290` was incorrect; the SHA above is verified with git and remote Actions. The tracked checkout remains unchanged; the pre-existing untracked dossier-out directory was preserved.

Synthetic read-only probes reproduced the NaN allocator exceptions (#689), offset-naive timestamp exception (#690), missing canonical artist URI (#691), tenfold 3D millimetre parsing error (#692), max=0 resize HTTP 500 plus missing query bounds (#693), missing canonical conflict kept value (#694), missing-only CLI exit 2 despite FAA_WORKS_DIR (#695), blank manifest year despite year_min (#696), and explicit None strength TypeError / NaN first-pair retention (#697). Evidence and reproducible probe source are in `/Users/teacher/.codex/automations/research-program/artifacts/audits/Fine-Art-Archive-2026-09-05-resume`.

Material corrections:
- #689: zero shares do not establish a crash and retain documented lens-floor behavior. Corrected body targets non-finite/negative inputs without prohibiting valid zero weights.
- #693: a huge max did not upscale a 100 by 100 fixture; request-sized allocation was not established. The zero-size failure and missing declared bounds are confirmed. Two shortened main.py citations were expanded to real repo-relative paths.
- #694: completeness status counts still use field_provenance; the defect concerns kept_value in conflict detail for canonical-only records. Corrected the malformed symbol-as-path citation.
- #697: None violates the declared dict[str, float] input type. No production next_pair caller was found in src or scripts. Retain as low-priority defensive hardening; do not describe it as a production outage. NaN can retain the first pair rather than simply dropping all pairs.
- Removed other bare-file citation advisories from the staged bodies. The repository's actual format validator passes all nine corrected bodies without advisories. They are staged corrections for existing issues, not new issue candidates, and have not been published.

## Existing remote format evidence

| Issue | State | Remote format verdict |
|---|---|---|
| [#689](https://github.com/stranske/Fine-Art-Archive/issues/689) | OPEN | No successful remote guard: cancelled/skipped only |
| [#690](https://github.com/stranske/Fine-Art-Archive/issues/690) | OPEN | [Passed](https://github.com/stranske/Fine-Art-Archive/actions/runs/33943694227) |
| [#691](https://github.com/stranske/Fine-Art-Archive/issues/691) | OPEN | [Passed with advisory](https://github.com/stranske/Fine-Art-Archive/actions/runs/33943695192) |
| [#692](https://github.com/stranske/Fine-Art-Archive/issues/692) | OPEN | [Passed](https://github.com/stranske/Fine-Art-Archive/actions/runs/33943695938) |
| [#693](https://github.com/stranske/Fine-Art-Archive/issues/693) | OPEN | [Passed with advisory](https://github.com/stranske/Fine-Art-Archive/actions/runs/33943696268) |
| [#694](https://github.com/stranske/Fine-Art-Archive/issues/694) | OPEN | [Passed with advisory](https://github.com/stranske/Fine-Art-Archive/actions/runs/33943696568) |
| [#695](https://github.com/stranske/Fine-Art-Archive/issues/695) | OPEN | [Passed](https://github.com/stranske/Fine-Art-Archive/actions/runs/33943697525) |
| [#696](https://github.com/stranske/Fine-Art-Archive/issues/696) | OPEN | [Passed with advisory](https://github.com/stranske/Fine-Art-Archive/actions/runs/33943697839) |
| [#697](https://github.com/stranske/Fine-Art-Archive/issues/697) | OPEN | [Passed](https://github.com/stranske/Fine-Art-Archive/actions/runs/33943698396) |

The eight passing results above were verified in the validation step's log, not inferred from workflow success alone. #689's remote format validation remains unproven; its corrected local body passes. No rerun or issue edit was sent from this research-only role. None of the nine has a needs-human label in this snapshot; their labels are bug/enhancement, priority, and testing only, so this report does not claim nine newly dispatched or agent-ready jobs.

## Scope and coverage limits

This is a resumed correctness-refill audit, not a fresh whole-repository audit. The dossier supplied scope: versioned software and policy, with artwork masters/live sidecars external. Historical issue inventory (150 open/recently closed records) was checked for overlap: #695 is a remaining CLI default case after #671; #690 is a timestamp edge case in #673's source-quality path; #691 is a canonical-identifier gap after #249's crosswalk delivery. No further issues were filed.

The retained checkpoint claimed all eight dimensions and 1,899 passing tests. No raw full-suite execution log was retained alongside this audit; that test count is prior-executor reporting, not independently confirmed here. This run used direct bounded reproduction instead of repeating the full suite. D1 correctness, D2 root-helper consolidation, D3 wiring, and D6 manifest metadata received concrete source/probe checks. D4 has API function/OpenAPI observations only: no rendered-browser capture or UX panel, so no usability score or full UX completion claim. D5 confirms a local crosswalk projection gap, not a current public-field survey. D7 has the actual format validator, not a tool-market comparison. D8 has local CLI maintenance behavior, not fleet capacity/effectiveness measurement. Broader UX, public-field/tool research and local-fleet effectiveness remain deferred beyond this recovery; no new evidence is implied by the inherited eight-dimension headings.

## Handoff

Use the corrected bodies in `/Users/teacher/.codex/automations/research-program/artifacts/audits/Fine-Art-Archive-2026-09-05-resume/corrected-issue-bodies` when a publishing-capable lane next reconciles existing issues #689–697. Prioritize #689/#690 correctness; treat #697 as optional defensive hardening. Confirm #689's remote guard when an authorized lane next edits/revalidates it. The audit is research-complete with these explicit limitations; implementation and publishing of corrections are separate work.

Canonical recovery report: `/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits/Fine-Art-Archive/2026-09-05-resume-reconciliation.md`.
