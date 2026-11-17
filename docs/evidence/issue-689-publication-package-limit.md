# Issue #689: publication package member limit

The [reported job](https://github.com/stranske/Ready/actions/runs/44024346307/job/133840992850)
failed in **Check published research** while running
`python scripts/check_publication_safety.py --allowlist "$SOURCE_ALLOWLIST"`.
The selected policy was the repository-root `.publication-allow`.

Five audit workbooks under
`research-program/artifacts/audits/Counter_Risk-2026-09-13-assets/demo-output/`
have `xl/styles.xml` members larger than the former 8 MiB limit:

| Workbook | Uncompressed styles bytes |
| --- | ---: |
| Historical Counterparty Risk Graphs - All Programs 3 Year.xlsx | 10,180,211 |
| Historical Counterparty Risk Graphs - LLC 3 Year.xlsx | 10,179,539 |
| Historical Counterparty Risk Graphs - ex LLC 3 Year.xlsx | 10,179,952 |
| MOSERS Counterparty Risk Summary 12-31-2025 - Ex Trend.xlsx | 10,188,355 |
| MOSERS Counterparty Risk Summary 12-31-2025 - Trend.xlsx | 10,185,924 |

Commit `6566752e` raises the member limit to 16 MiB. The existing 64 MiB
total budget and 4,096-member budget still apply. No workflow, allowlist,
or published artifact changes are needed.

## Local verification (2026-11-17)

- [x] Read the linked job log and identify the failing step and command.
- [x] Reproduce the failure with the exact command and the former 8 MiB limit.
  It exits 1, rejects exactly the five workbooks listed above, and reports
  `files_scanned=3437`, `allowed_hits=11`, `errors=5`.
- [x] Verify the fixed command with the repository-root policy:
  `python scripts/check_publication_safety.py --allowlist "$PWD/.publication-allow"`.
  It exits 0 and reports `files_scanned=3437`, `allowed_hits=11`, `errors=0`,
  with zero unallowed hits for every rule.
- [x] Inspect `pyproject.toml` and confirm the source uses pytest.
- [x] Extend `test_large_xlsx_styles_are_fully_scanned` to run through the
  dependency-free CLI with an explicit policy, about 60,000 styles, and a
  styles member between 8 and 16 MiB. A clean workbook passes; unsafe content
  at the end of the styles member or split across runs in a subsequent shared
  strings member fails with the expected finding and zero package errors.
  Diagnostics disclose neither member names nor matched text, and workbook
  bytes remain intact.
- [x] Deliberate break: temporarily restore the 8 MiB limit and run
  `pytest tests/test_publication_safety.py -k large_xlsx_styles -m "not slow" --no-cov`.
  All three cases fail because the member is rejected. The same three cases
  pass with 16 MiB. Restore the 16 MiB limit after the experiment.
- [x] Run Black on the changed Python file and pass the required repository check:
  `black --check --line-length 100 --exclude '(\.workflows-lib|node_modules)' .`.
  All 97 files are unchanged. Set `BLACK_NUM_WORKERS=1` and a writable
  `BLACK_CACHE_DIR` under `/tmp` for the restricted runner.
- [ ] Run the full repository test command: `pytest -m "not slow"`.
  Started the command; stopped it after discovering that PR #690 had merged
  during this run. All three real source-addition coverage probes passed,
  and no failures had been reported. The full suite did not complete, so its
  acceptance criterion remains unchecked.

## External follow-up

- [ ] Verify `publication-safety` passes on regenerated sync PR #688.
- [ ] Verify the next sync-core round omits this finding.

PR #690 merged externally at 2026-11-17 06:52:25 UTC as
`9be68acdcfd8a3249769cd6b474dffabf2000c06`, including the existing 16 MiB fix.
Its final observed state was merged, with `draft=false`. This run's additional
CLI regression changes remain local and were not included in that merge.
The live checks depend on the existing external sync process. This run does
not edit the generated sync branch or workflow files.
The issue's elided three subtasks have no supplied definitions and remain unverified.

## Execution restrictions

The workspace permits these source and evidence edits, but mounts `.git` read-only.
Staging the changes fails because Git cannot create `.git/index.lock`
(`Read-only file system`); committing requires a writable Git metadata directory
or the automation's outer commit step.

Attempts to add the required `needs-human` label and a blocker comment to PR #690
were also rejected: `MCP tool call requires approval, but approval policy is never`.
Neither GitHub write succeeded. This local note records the blocker instead.
