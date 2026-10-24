# Ready publication coverage: issue 623

Base `276a25c1`; local Anaconda CPython 3.12.2, pytest 9.1.1,
pytest-cov 7.1.0 and coverage 7.16.0. Hosted pinned coverage 7.16.2
and full current-head CI remain separate verification boundaries.

`python -m pytest -q -n 2` reports exactly the two Ready-owned publication
scripts plus product `src/` files. Both run and report include paths are
explicit; the final report excludes synced tooling and temporary copies of
publication scripts. Subprocess coverage captures the real CLI tests.
The pytest-cov controller also seeds every `src/**/*.py` into the data before
reporting, preserving the old discovery of unexecuted product files.
A temporary unimported source file with an unconditional exception appeared
as 0/1 lines without executing it; it was then removed. This was exercised
with xdist, matching the reusable Gate's controller/worker arrangement.

Measured counts (the JSON packet retains complete summaries):

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

## Deliberate loss and restoration

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

## Commands

- `python -m pytest -q -n 2`
- `python scripts/publication_coverage_gate.py`
- `python -m mypy --explicit-package-bases scripts/publication_coverage_gate.py tests/conftest.py`
- `python -m ruff check scripts/publication_coverage_gate.py tests/conftest.py tests/test_coverage_baseline.py`
- `python -m black --check scripts/publication_coverage_gate.py tests/conftest.py tests/test_coverage_baseline.py`
- `git diff --check`
