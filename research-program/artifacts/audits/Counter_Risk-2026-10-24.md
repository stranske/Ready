Scorecard: 2 work / 2 partial / 0 broken / 0 fabricated / 1 not exercised of 5; journey: passes; surfaces unscored 1; closed-still-broken 0.

Issues filed: 0. The one current Runner defect is already open as [#1183](https://github.com/stranske/Counter_Risk/issues/1183), with implementation PR [#1185](https://github.com/stranske/Counter_Risk/pull/1185); filing a second issue would duplicate active work.

## Run report — Track D refill — 2026-10-24

Audited live `main` at `57332e855688172f98bf1b292f2b4897f7ba13a5`, not the supplied clone (`affd8bf`, 2026-09-29), which had become stale before this audit. A fresh depth-one clone in `/tmp` was used for all live-tip evidence. Confidence: high for the exercised CLI results; medium for the platform-specific operator paths that this macOS environment cannot drive.

### Product scorecard

| id | core function | verdict | live evidence |
|---|---|---|---|
| C1 | An operator runs the pipeline and sees coherent exposure by variant | WORKS | `counter-risk run` consumed all three shipped workbook variants and exited 0 after writing the run folder. `src/counter_risk/cli/__init__.py:368-408` dispatches this path. |
| C2 | An operator applies identity and limits and sees alias/limit warnings | PARTIAL | The baseline run wrote `limit_breaches.csv` with CME's 35% cap warning; replacing the all-programs workbook with Ex Trend changed that result to a missing-entity warning. The audit did not independently vary an alias at the CLI boundary, so it cannot claim the full contract. Relevant path: `src/counter_risk/cli/__init__.py:368-408`. |
| C3 | An operator sees concentration reflect input exposure | WORKS | With the baseline input, all-programs total HHI was `0.09441189811132489`; replacing only that variant with Ex Trend changed it to `0.09547527364105722` (Top-5 share `0.5391907905874387` to `0.5511887120675214`). Both CLI runs exited 0 and wrote `concentration_metrics.csv`. |
| C4 | An operator receives reporting artifacts and warnings | PARTIAL | The CLI wrote three historical workbooks, a PPT master, concentration and limit outputs, manifest and data-quality summary. PPT link refresh was explicitly skipped as `unsupported_platform`, and PDF export was disabled for the macOS exercise; final Windows/Office distribution remains unverified. |
| C5 | An operator sees source-date conflicts with provenance | NOT-EXERCISED | The contract's source-date conflict/override matrix was not driven through an unmocked CLI run in this round. Existing test coverage is not substituted for that product exercise. |

The primary journey passed through an isolated fixture-backed CLI run. This is meaningful runtime evidence, but not a claim that confidential production inputs or Windows Office automation were exercised.

### Surface inventory and coverage

`counter-risk` exposes `run` and `gui` at `src/counter_risk/cli/__init__.py:63-205`; `mapping_diff_report` is a separate maintainer diagnostic console script declared at `pyproject.toml:71`. The mapping report is interior rather than a core operator journey. The GUI command's headless discovery path returned success, but the rendered Tk surface was not driven; it is the one unscored surface. `Runner.xlsm` and the frozen Windows bundle are platform capabilities, not additional CLI routes; both remain unverified and are not silently counted as passing.

### Verification and disposition

- Scoped collection on the fresh checkout found 2,242 tests. The initial collection from the unit root was invalid because it traversed sibling repositories (307 unrelated errors); it was discarded and rerun from the target checkout.
- GitHub's checks on current `main` show successful Python 3.12, Python 3.13, mypy, Ruff and format gates for the audited main commit.
- The open issue inventory has only #1183 plus two unrelated automation/dashboard items. #1183's own live-tip evidence names `scripts/build_runner_workbook.py`, `assets/vba/RunnerLaunch.bas`, and `tests/test_runner_workbook.py`; its implementation PR #1185 currently has failing Python 3.12/3.13 checks. It is not resolved.
- No independently verified, non-duplicate defect met the issue format threshold. No issue was dropped merely because a closed issue existed, so no `REFUTED:` line is due.

### Risks and unknowns

- The audit host cannot perform the Windows Excel COM click-test or a frozen PyInstaller launch. A successful `gui --headless --dry-run-discovery` is not visual/UI evidence.
- The live pipeline emitted a fixture-data warning for unmatched series and a limit/data-quality failure state. Those are observable outputs of the synthetic fixture set; this audit has insufficient evidence to classify them as a production defect.
- A current PR's failed checks are an active delivery risk for #1183, not evidence of a new issue or a main-branch regression.

### Storage boundary

The unit's write boundary permits this report and checkpoint under `artifacts/audits`, but not the external `Code/Audits` ledger directory specified by the generic skill. No ledger or measurement file was modified; no URLs were filed to append.
