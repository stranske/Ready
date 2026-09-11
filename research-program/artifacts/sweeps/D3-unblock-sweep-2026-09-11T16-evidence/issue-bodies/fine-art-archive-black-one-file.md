# Fine-Art-Archive `main` red: one unformatted test file

## Context
`Python CI / lint-format` fails on `main` (job 102245751229, head `92408ee`, 2026-09-08T21:32Z).
The head has not moved since, so `main` has been red for 3 days.

## Evidence
```
black --check --line-length 100 --exclude '(\.venv|\.workflows-lib|node_modules)' .
would reformat tests/test_gate_commit_status_fork_tolerance.py
1 file would be reformatted, 332 files would be left unchanged.
```

## Tasks
- [ ] Run `black --line-length 100 tests/test_gate_commit_status_fork_tolerance.py` and commit
      the result.

## Acceptance criteria
- [ ] `black --check --line-length 100 --exclude '(\.venv|\.workflows-lib|node_modules)' .`
      exits 0.
- [ ] `Python CI / lint-format` is green on `main`.

## Test gate
Named gate: the `lint-format` job of `Python CI`, which currently fails and must pass after the
change. Its load-bearing nature is already demonstrated by the present failure.

## Non-goals
- No behavioural change to `tests/test_gate_commit_status_fork_tolerance.py` — formatting only.
