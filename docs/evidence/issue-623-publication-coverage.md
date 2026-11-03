# Ready publication coverage: issue 623

Base `276a25c1`; merged measurement work in #638 (`4d9a07cf`). Declared
pinned tools: pytest 9.2.0, pytest-cov 7.1.0, coverage **7.17.0**
(`pyproject.toml` / `autofix-versions.env` / `ci-python-versions.env`).

Hosted Gate uses the existing reusable Python CI job on Python 3.13 and
3.14 with two workers. The real removal control already runs in this job;
`-rP` retains its measured proof in the hosted log. No separate proof job
is needed. The control invokes `python scripts/publication_coverage_gate.py`
against its restored real-script report.

`python -m pytest -q -n 2` reports exactly the two Ready-owned publication
scripts plus product `src/` files. Both run and report include paths are
explicit; the final report excludes synced tooling and temporary copies of
publication scripts. Subprocess coverage captures the real CLI tests.
The pytest-cov controller also seeds every `src/**/*.py` into the data before
reporting, preserving the old discovery of unexecuted product files.
A temporary unimported source file with an unconditional exception appeared
as 0/1 lines without executing it; it was then removed. This was exercised
with xdist, matching the reusable Gate's controller/worker arrangement.

Historical #638 local counts (retained for the recorded-floor regression tests):

| File | Lines | Branches | Independent floors |
|---|---:|---:|---|
| scripts/check_publication_safety.py | 213/215 | 110/114 | line 99.0697%; branch 96.4912% |
| scripts/prepare_publication.py | 107/121 | 60/62 | line 88.4297%; branch 96.7741% |
| src/my_project/__init__.py | 6/6 | none | existing aggregate gate |

Floors round the actual measurement down by less than 0.0001 percentage
point. The existing aggregate 80% threshold remains intact. Per-file line
and branch losses fail independently, and absent/malformed measurements
fail closed. The coverage-enabled pytest session hook checks the newly
created report, so both CI and PR Gate use this control through their
existing reusable pytest invocation. `--no-cov` remains available for
focused functional checks; it is not a coverage PASS.

## Deliberate loss and restoration (local break/restore packet)

Temporarily removing the real `test_unreadable_directory_fails_closed`
from collection left all 382 tests passing but lowered scanner lines from
213 to 212. The aggregate stayed above 80%; the new per-script gate exited
1. Exact test-file byte restoration returned 383 passing tests and exit 0.

A second control temporarily removed the two-case
`test_empty_or_missing_tree_fails`: all 381 remaining tests passed, scanner
lines dropped to 212/215 and branches to 109/114. The gate exited 1 on both
floors while the aggregate remained 95.37%. Exact-byte restoration returned
383 passing tests and exit 0. Production publication rules were unchanged
in both controls. The temporary test edits are absent from this PR.

Initial module-based measurement counted test fixture copies and produced
an invalid aggregate; that result was rejected. The final exact report
selection fixes that issue. Neither coverage nor passing tests certify
confidentiality, allowlist policy, live publication, or future safety.

## Hosted CI demonstration

Gate [run 41605396922](https://github.com/stranske/Ready/actions/runs/41605396922)
completed successfully on 2026-11-03. Tested merge commit
`ebc8046a7a56396596562e123b20d43696d0f07b` combines PR head
`5d2f1192c02387647b85056dd941e337ff6cd23a` with main
`fdf097082d8271a06d4b8083062a0962ed06a318`.

| Hosted job | Installed Python | Full suite | Real control duration |
|---|---|---|---|
| [3.13](https://github.com/stranske/Ready/actions/runs/41605396922/job/125814113396) | 3.13.17 | 1057 passed, exit 0, 586.40 s | 102.897 s |
| [3.14](https://github.com/stranske/Ready/actions/runs/41605396922/job/125814113319) | 3.14.9 | 1057 passed, exit 0, 609.24 s | 107.110 s |

Both installed coverage **7.17.0**, pytest 9.2.0 and pytest-cov 7.1.0.
Full-suite artifacts measure scanner lines **213/215**, branches **111/114**;
preparer lines **115/121**, branches **60/62**. Both pass the unchanged
configured line and branch floors.

The existing Gate executes
`tests/test_coverage_baseline.py::test_real_test_removal_fails_publication_gate[guard]`.
Its `ISSUE623_PROOF=` log records real-script observations in both runtimes:

| Phase | Scanner lines | Scanner branches | Pytest exit |
|---|---:|---:|---:|
| Baseline | 213/215 | 111/114 | 0 |
| Deselect `test_empty_or_missing_tree_fails` | 212/215 | 110/114 | 1 |
| Restore collection | 213/215 | 111/114 | 0 |

Preparer counts remain 115/121 lines and 60/62 branches throughout.
`python scripts/publication_coverage_gate.py` against each restored isolated
report exits 0 and prints `Ready publication coverage floors PASS`.

The existing control first passes repository floors, then calibrates its
isolated probe floors to observed baseline counts. Removal breaches both
calibrated floors. The observed line loss also breaches the repository
scanner line floor; the branch loss alone still meets its repository branch
floor. No committed floor is changed. Thus the proof demonstrates branch
loss and gate failure without claiming a branch-only failure at current
repository floors.

The JSON `hosted_ci` packet records installed versions, full-suite and
before/removal/restored counts, exit statuses, elapsed seconds and artifact
IDs, extracted from the hosted logs and coverage artifacts. Top-level counts
remain the historical #638 packet. Run 41591960131 is superseded because its
proof job failed with `KeyError: PYTEST_EXIT` after pytest/CLI completion.

## Commands

- `python -m pytest -q -n 2`
- `python scripts/publication_coverage_gate.py`
- `python -m mypy --explicit-package-bases scripts/publication_coverage_gate.py tests/conftest.py`
- `python -m ruff check scripts/publication_coverage_gate.py tests/conftest.py tests/test_coverage_baseline.py`
- `python -m black --check scripts/publication_coverage_gate.py tests/conftest.py tests/test_coverage_baseline.py`
- `git diff --check`
