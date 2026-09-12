# Ready `main` is red on every sweep: `[tool.black]` lacks the `research-program/artifacts` exclude

## Context
`Python CI / lint-format` fails on `main` (job 103463375265, run 34661021852, head `56de613`, 2026-09-12T00:15:39Z).
It has been failing consistently across consecutive heads (`09f8ee6`, `96eb461`, `17cf0f1`, `56de613`).

## Evidence
The CI step runs:
```bash
black --check --line-length 100 --exclude '(\.venv|\.workflows-lib|node_modules)' .
```
and reports 29 files needing reformatting, every one of them under `research-program/artifacts/audits/…`, e.g.:
```
would reformat research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/finalize_report.py
would reformat research-program/artifacts/audits/paem-20260907/probe_cvar_interval.py
would reformat research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/serve.py
```
These are artifacts the Research Program writes into Ready when `program.py done` pushes the mirror — scratch/evidence scripts, not maintained source code.

`pyproject.toml` already excludes exactly this path for Ruff but not for Black:
- `[tool.ruff]`, line 64: `extend-exclude = ["research-program/artifacts"]`
- `[tool.black]`, lines 102-104: `line-length`, `target-version` — no exclude

## Tasks
- [ ] Add `extend-exclude = "research-program/artifacts"` to `[tool.black]` in `pyproject.toml` (Black accepts a regex string).

## Acceptance criteria
- [ ] `black --check --line-length 100 --exclude '(\.venv|\.workflows-lib|node_modules)' .` exits 0 at the repository root with mirrored artifacts present.
- [ ] `Python CI / lint-format` is green on `main`.
- [ ] Subsequent Research Program mirror pushes adding unformatted helpers under `research-program/artifacts/` do not turn `main` red.

## Test gate
Named gate: `lint-format` job of `Python CI`.
