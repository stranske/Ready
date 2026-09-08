# Counter_Risk research audit — 2026-09-08

Unit: `D-audit-Counter_Risk--2026-09-08T17-11-36Z`. Completed research artifact at 2026-09-08T17:28:42.209627+00:00. Audited and rechecked remote main: `e2a1bacf37503217e00e467aa72198988777afa4`. Five code defects and one documentation correction are verified and staged. **No issues were filed:** the executor's explicit research-only instruction overrides the brief's filing step. Implementation supply was not replenished and no intake URLs were appended. No owner decision was needed.

| ID | Priority | Finding | Verification | Draft |
|---|---|---|---|---|
| CR-1 | P1 | Infinite configured limit is accepted | 100 vs 50: one breach; 100 vs infinity: zero | [04-finite-limit.md](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/issue-bodies/04-finite-limit.md) |
| CR-2 | P1 | Release assembly drops companion runtime and data files | Copy probe: exe present, library/config absent | [01-package-payload.md](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/issue-bodies/01-package-payload.md) |
| CR-3 | P1 | GUI launcher omits the assembled bin path | GUI absent; CLI generator has correct bin path | [02-gui-release-launcher.md](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/issue-bodies/02-gui-release-launcher.md) |
| CR-4 | P2 | Duplicate Repo rows inflate authoritative cash | 10+20 rows with authoritative100 produce120 | [05-repo-cash-duplicate.md](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/issue-bodies/05-repo-cash-duplicate.md) |
| CR-5 | P2 | Split current attribution reuses prior balance | Actual CSV total change +50 becomes -200 | [06-current-attribution.md](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/issue-bodies/06-current-attribution.md) |
| CR-6 | P3 | HHI guide mixes undated DOJ threshold regimes | Official current source differs from guide lines77–80 | [03-hhi-doc-reference.md](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/issue-bodies/03-hhi-doc-reference.md) |


The strongest findings are the finite-policy acceptance gap and the two independent packaging boundaries. Duplicate-row findings are conditional on such inputs; no claim is made that current operator workbooks contain them. The actual report-writing probe gives a stronger CR-5 reproduction than the delegate's helper example: equivalent single/split current positions emit +50 versus -200, silently duplicating prior total from 250 to 500.

## What was checked

- Clone pulled from aa3173e to current main before audit. Pre-existing untracked dossier-out/ and uv.lock retained; tracked code remains unchanged.
- September 4 dossier, September 7 audit and August 24 verification ledger used for continuity. All seven September 7 issue IDs are closed; current code confirms the relevant prior-side/numeric fixes. They were not re-filed.
- Dedup snapshot: 120 open and closed issues, then final open refresh. #996 is the narrow historical-update coverage item, plus #724 dependency and #499 metrics trackers. One open dependency-sync PR #1013. CR-5 is distinct from prior-only #1003 and futures-only #1001. CR-2/CR-3 sharpen an incomplete assembled-product boundary after closed packaging work such as #78.
- Exact-head main [CI 34244935833](https://github.com/stranske/Counter_Risk/actions/runs/34244935833) passed Black, Ruff, mypy and Python3.12/3.13. 1,738 tests collected locally. Bounded delegated tests: 167 passed, 31 deselected; raw execution evidence extracted to core-tests.json. Source web smoke: 3 passed. No full local suite or Windows execution is claimed.
- Independent lead probes ran the actual limits YAML loader and evaluator, Repo injection and historical aggregator, attribution helper and CSV writer, release-copy function, and frozen config matched control. Probe files and results are under [Counter_Risk-2026-09-08-evidence](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence). First CSV probe used the wrong delta alias and skipped output; corrected to the actual NotionalChange field before accepting the result.
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

See [field-and-tools.md](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/field-and-tools.md) for source links and decisions. The static demo panel's overall median is 3.0, with a failed UX gate. Three panel findings collapse into one known artifact-retrieval handoff problem; a new browser runtime is not justified. See [UX_REVIEW.md](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/UX_REVIEW.md) and [Windows handoff](/Users/teacher/.codex/automations/research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/WINDOWS_TEST_BRIEF.md). This audit does not certify operator readiness.

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
