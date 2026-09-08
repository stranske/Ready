from pathlib import Path
import json,datetime,shutil
b=Path.cwd();e=b/'artifacts/audits/Counter_Risk-2026-09-08-evidence';out=b/'artifacts/audits/Counter_Risk-2026-09-08.md';a=Path('/Users/teacher/Library/CloudStorage/Dropbox/Learning/Code/Audits');d=a/'Counter_Risk';u='D-audit-Counter_Risk--2026-09-08T17-11-36Z';now=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=(e/'head.txt').read_text().strip()
labels={x['name'] for x in json.loads((e/'labels.txt').read_text())};print('Applicable labels:',sorted(labels&{'bug','documentation','priority:high','priority:normal','codex','codex-automation'}))
(e/'WINDOWS_TEST_BRIEF.md').write_text('''# Windows operator verification handoff

Status: NOT EXECUTED on this macOS host. Use synthetic fixtures only and an isolated release directory. Do not change operator reservations, source workbooks or live monthly outputs.

1. On Windows, check out the audited revision or the eventual fix, install declared build dependencies and run the existing release assembly command: `python -m counter_risk.build.release --version 0.1.0 --output-dir <scratch-release>`.
2. Inspect the complete assembled bin directory against PyInstaller's dist directory: Python runtime libraries, extensions, config and templates must survive. The current spec places companions alongside the executable. Record a recursive file inventory and hashes.
3. From an unrelated directory, execute `<scratch-release>\\0.1.0\\bin\\counter-risk.exe --help`, then `gui --headless --dry-run-discovery --as-of-date 2025-12-31 --config <absolute-fixture-config> --input-root <fixture-root> --output-root <scratch-output>`. Capture stdout, stderr and exit status. Passing help alone is insufficient.
4. Copy the complete assembled release to a path containing spaces. Exercise `run_counter_risk_gui.cmd` with a command recorder for deterministic selection and argument assertions. The selected executable must be the assembled bin copy, not a global installation. Test a nonzero child result and retained diagnostics.
5. Launch the actual Tk GUI, verify input and date validation, all three modes, discover selection, repeat-run folder suffixes, error recovery, and each post-run Open button. Record screenshots of initial, discovery, completed and failed states.
6. Open the shipped XLSM, enumerate and exercise its seven macro controls on synthetic inputs. Confirm settings are passed, the completed run is selected, and links open that run's manifest, summary and PPT folder.
7. Run fixture replay through the packaged binary and compare captured manifest and workbook values against the reference fixture. Exercise Excel and PowerPoint COM refresh/export, inspect the exported slides and save the evidence. This requires a Windows Office installation; Linux release tests cannot attest it.

Pass criteria: correct packaged process selected, no missing runtime/config assets, schema-valid manifest, numeric fixture equivalence, repeat-run isolation, all links refer to the completed run, readable errors. Fail criteria: any absent runtime companion, global Python fallback, missing output, wrong-run link, macro/COM failure, or unverified output claimed complete. Store logs/screenshots in this evidence directory or the canonical Code/Audits/Counter_Risk assets folder with the tested commit recorded.
''')
ux=f'''# Counter_Risk UX review — {now}

Only the static browser page and headless discovery were observed; Windows Tk/Excel/COM/frozen-exe coverage is unverified. This is not a production UI gate pass.

| Surface | Driven | Outcome | Evidence |
|---|---|---|---|
| Static demo page | Yes | Explanation and Ready status render; no artifact retrieval link or control | {e}/browser-dom.txt; {e}/demo.png |
| Source headless GUI discovery | Yes | Completed with explicit fixture config | {e}/gui-discovery-explicit-config.txt |
| Source launch from unrelated cwd without config | Yes | Readable missing-config error; source resolver intentionally keeps relative paths | {e}/gui-discovery.txt |
| Windows Tk, XLSM, Office COM, assembled binary | No | Platform unavailable here | {e}/WINDOWS_TEST_BRIEF.md |

Four nonempty evaluator rubrics (codex/cursor/gemini/vibe), plus cursor adversary, are retained under /Users/teacher/.codex/orchestrator-mirror/ux_reviews/stranske/Counter_Risk_uxreview_2026-09-08-research/. Static-page medians: wiring 5.5, usability 3, help clarity 5, productivity 2.5; overall 3. Consensus flags all true. Gate result is false: no full Gate 1, low static-page median, panel blockers. Scores do not describe the production Tk GUI.

Lead adjudication: the three panel findings are one retrieval-handoff problem, already known as August 24 D4-1 and adjacent to closed #645. Retain as a known follow-up, not a new issue. Accept a precise fixture-artifact location/link or documented handoff. Reject a mandatory browser execution engine or unrestricted upload as scope expansion; fixture-only static labeling is explicit. The high blocker rating is downgraded to a secondary demo usability gap. The headless success line supports command wiring only, not GUI screen quality. Improvements and raw scores are saved without rewriting the panel's conclusions.

Source fixture smoke: 3 passed in 88.72 seconds. Windows handoff remains open. No review-log PR or UI changes were made.
'''
(e/'UX_REVIEW.md').write_text(ux)
rows=[('CR-1','P1','Infinite configured limit is accepted','100 vs 50: one breach; 100 vs infinity: zero','04-finite-limit.md'),('CR-2','P1','Release assembly drops companion runtime and data files','Copy probe: exe present, library/config absent','01-package-payload.md'),('CR-3','P1','GUI launcher omits the assembled bin path','GUI absent; CLI generator has correct bin path','02-gui-release-launcher.md'),('CR-4','P2','Duplicate Repo rows inflate authoritative cash','10+20 rows with authoritative100 produce120','05-repo-cash-duplicate.md'),('CR-5','P2','Split current attribution reuses prior balance','Actual CSV total change +50 becomes -200','06-current-attribution.md'),('CR-6','P3','HHI guide mixes undated DOJ threshold regimes','Official current source differs from guide lines77–80','03-hhi-doc-reference.md')]
table='| ID | Priority | Finding | Verification | Draft |\n|---|---|---|---|---|\n'+''.join(f'| {i} | {pri} | {title} | {proof} | [{fn}]({e}/issue-bodies/{fn}) |\n' for i,pri,title,proof,fn in rows)
report=f'''# Counter_Risk research audit — 2026-09-08

Unit: `{u}`. Completed research artifact at {now}. Audited and rechecked remote main: `{sha}`. Five code defects and one documentation correction are verified and staged. **No issues were filed:** the executor's explicit research-only instruction overrides the brief's filing step. Implementation supply was not replenished and no intake URLs were appended. No owner decision was needed.

{table}

The strongest findings are the finite-policy acceptance gap and the two independent packaging boundaries. Duplicate-row findings are conditional on such inputs; no claim is made that current operator workbooks contain them. The actual report-writing probe gives a stronger CR-5 reproduction than the delegate's helper example: equivalent single/split current positions emit +50 versus -200, silently duplicating prior total from 250 to 500.

## What was checked

- Clone pulled from aa3173e to current main before audit. Pre-existing untracked dossier-out/ and uv.lock retained; tracked code remains unchanged.
- September 4 dossier, September 7 audit and August 24 verification ledger used for continuity. All seven September 7 issue IDs are closed; current code confirms the relevant prior-side/numeric fixes. They were not re-filed.
- Dedup snapshot: 120 open and closed issues, then final open refresh. #996 is the narrow historical-update coverage item, plus #724 dependency and #499 metrics trackers. One open dependency-sync PR #1013. CR-5 is distinct from prior-only #1003 and futures-only #1001. CR-2/CR-3 sharpen an incomplete assembled-product boundary after closed packaging work such as #78.
- Exact-head main [CI 34244935833](https://github.com/stranske/Counter_Risk/actions/runs/34244935833) passed Black, Ruff, mypy and Python3.12/3.13. 1,738 tests collected locally. Bounded delegated tests: 167 passed, 31 deselected; raw execution evidence extracted to core-tests.json. Source web smoke: 3 passed. No full local suite or Windows execution is claimed.
- Independent lead probes ran the actual limits YAML loader and evaluator, Repo injection and historical aggregator, attribution helper and CSV writer, release-copy function, and frozen config matched control. Probe files and results are under [{e.name}]({e}). First CSV probe used the wrong delta alias and skipped output; corrected to the actual NotionalChange field before accepting the result.
- Six issue bodies passed the target repo's actual `.github/scripts/issue_format.py` validator with **zero advisories**. Every explicit source citation was opened and checked. The deliberate-break tests in the drafts are future implementation acceptance gates; they were not falsely reported as already implemented.

## Eight-dimension coverage

| Dimension | Coverage and disposition |
|---|---|
| 1 Correctness | Two scoped agent reviews, independent reproduction; CR-1 through CR-5 retained |
| 2 Duplication | AST equality scan found four groups; demo-helper consolidation is known, adapters are observations, no deletion recommendation |
| 3 Functionality/wiring | Config→limits, cash→historical output, current/prior→CSV, build→release→launcher traced |
| 4 Design/UX | Static page DOM/screenshot plus four-evaluator panel and mined improvements; headless discovery observed; Windows surface handoff required |
| 5 Public field | Official BIS comparison of complementary measures and stress analysis; documented as roadmap, not a compliance requirement; CR-6 verified against DOJ |
| 6 Opportunities | Scenario comparison and future netting/collateral contracts assessed; no new financial policy chosen |
| 7 Tools | Bounded Hypothesis property-test pilot considered; openpyxl recalculation limits and PyInstaller execution controls documented; no dependency installed |
| 8 Local tooling | Exact-head CI, release/PR gating, scoped coverage issue and queue inclusion inspected; no claim of exhaustive external scheduler coverage |

See [field-and-tools.md]({e}/field-and-tools.md) for source links and decisions. The static demo panel's overall median is 3.0, with a failed UX gate. Three panel findings collapse into one known artifact-retrieval handoff problem; a new browser runtime is not justified. See [UX_REVIEW.md]({e}/UX_REVIEW.md) and [Windows handoff]({e}/WINDOWS_TEST_BRIEF.md). This audit does not certify operator readiness.

## Adversarial disposition and remaining work

- Cursor F1 accepted as CR-2, with a correction: the actual spec sets contents_directory to dot, so no internal-folder layout is assumed. F2 accepted as CR-3; no Windows shell execution claimed.
- Cursor F3 is folded into CR-2: the complete COLLECT tree includes config and passes frozen resolution. The delegate's missing-tree simulation does not prove an additional independent config defect. Operator-editable config precedence can be assessed after packaging works.
- Cursor F4 chat non-finite formatting is a reproducible latent helper weakness; no fresh normal production path was established, so no separate issue staged.
- Core three findings accepted after independent checks. Existing prior-row overwrite, non-finite repo parser and mixed-sign HHI claims rejected as fixed. Permissive standalone top_changes input remains insufficiently connected to file as a live bug.
- Lead web fixture-root hypothesis refuted by execution. Missing source config from an unrelated cwd is expected current source-path behavior and yields a readable failure.
- Known August24 items (demo duplication, static-page handoff, gate coverage/format limitations and previously reported policy/registry fallback candidates) remain continuity follow-ups; this run does not imply that all old findings were resolved. The policy/registry fallback candidates were not re-certified as new findings here.

Next action: an authorized publishing/implementation lane can consume the six staged bodies, starting with CR-1/CR-2/CR-3. Use existing repo labels (`bug`, `documentation`, `priority:high` or `priority:normal` where appropriate); do not auto-dispatch or mark these filed. Windows tests remain necessary to close the packaged-operator verification gap.

## Execution provenance

Orchestrator cursor review completed with nonempty evidence. The codex offload returned exit1 with OFFLOAD_INCOMPLETE detection despite writing its final core report and completing 167 tests; its transcript is not treated as a successful dispatch. Lead synthesis uses only the nonempty artifact and independently verified claims. Raw core/ops reports remain unchanged as evidence; this report's dispositions supersede their overclaims. UX evaluator artifacts are all nonempty. No secrets, source edits, PR changes, issue mutations, or new task claims were made by this executor.
'''
out.write_text(report)
(e/'verification-log.md').write_text(table+'\nAll six: STAGED, not filed. F3 folded into CR-2; F4 latent; web root refuted; UX three findings dedup to known D4-1. Windows verification deferred with concrete handoff.\n')
(d/'2026-09-08-AUDIT_REPORT.md').write_text(report);(d/'2026-09-08-verification-log.md').write_text((e/'verification-log.md').read_text());(d/'2026-09-08-UX_REVIEW.md').write_text(ux)
shutil.copytree(e/'issue-bodies',d/'2026-09-08-issue-bodies',dirs_exist_ok=True)
with (d/'README.md').open('a') as f:f.write(f'\n### 2026-09-08 — research-only refill audit\n{u}, main `{sha}`. Five verified code defects plus one documentation correction; six local bodies pass actual format guard with zero advisories. Nothing filed; supply unchanged. See [report](2026-09-08-AUDIT_REPORT.md), [verification](2026-09-08-verification-log.md), [UX](2026-09-08-UX_REVIEW.md). Next: authorized lane consumes staged bodies; Windows operator handoff remains required.\n')
with (a/'AUDIT_LEDGER.md').open('a') as f:f.write(f'\n- {now} Counter_Risk {u}: RESEARCH COMPLETE at {sha}; all eight dimensions considered, Windows/COM runtime unverified. CR-1 infinite limit, CR-2 missing package payload, CR-3 GUI bin lookup, CR-4 duplicate Repo cash, CR-5 split attribution, CR-6 HHI citation. Six staged bodies PASS0advisories; no issues/PRs filed or changed, no intake rows. MainCI green; 167 bounded tests and3 web tests passed; independent probes. Report {out}; canonical {d}/2026-09-08-AUDIT_REPORT.md. Next: publishing lane and Windows runtime verification.\n')
for name in ['CHECKPOINT.md',u+'.CHECKPOINT.md']:
 with (b/'artifacts/audits'/name).open('a') as f:f.write(f'\n## {now} — {u} — Phases 4–5 complete\nSix research-only issue drafts passed actual repo validator with zero advisories; exact head still {sha}. OUT written, canonical audit report/index/ledger reconciled, no filing/intake or code changes. Windows handoff and failed static-only UX gate documented. Ready for program.py done.\n')
print(out,len(report));print('six draft bodies:',len(list((e/'issue-bodies').glob('*.md'))))
