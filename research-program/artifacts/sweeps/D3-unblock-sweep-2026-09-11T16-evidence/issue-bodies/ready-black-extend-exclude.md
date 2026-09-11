# Ready `main` is red on every sweep: `[tool.black]` lacks the `research-program/artifacts` exclude

## Context
`Python CI / lint-format` fails on `main` (job 103350260778, head `09f8ee6`, 2026-09-11T17:06Z),
and failed identically on the two preceding heads today (`96eb461`, `17cf0f1`). It has been red
since at least 2026-09-08.

## Evidence
The CI step runs:

```
black --check --line-length 100 --exclude '(\.venv|\.workflows-lib|node_modules)' .
```

and reports 24 files needing reformatting, every one under `research-program/artifacts/audits/…`,
e.g.:

```
would reformat research-program/artifacts/audits/Counter_Risk-2026-09-08-evidence/finalize_report.py
would reformat research-program/artifacts/audits/paem-20260907/probe_cvar_interval.py
would reformat research-program/artifacts/audits/Travel-Plan-Permission-2026-09-05-assets/serve.py
```

These are artifacts the Research Program writes into Ready when `program.py done` pushes the
mirror — scratch/evidence scripts, not maintained source.

`pyproject.toml` already excludes exactly this path for Ruff but not for Black:

- `[tool.ruff]`, line 64: `extend-exclude = ["research-program/artifacts"]`
- `[tool.black]`, lines 102-104: `line-length`, `target-version` — no exclude

## Tasks
- [ ] Add `extend-exclude = "research-program/artifacts"` to `[tool.black]` in `pyproject.toml`
      (Black takes a regex string here, unlike Ruff's list).

## Acceptance criteria
- [ ] `black --check --line-length 100 --exclude '(\.venv|\.workflows-lib|node_modules)' .`
      exits 0 at the repository root with the mirrored artifacts present.
- [ ] `Python CI / lint-format` is green on `main`.
- [ ] A subsequent Research Program mirror push that adds an unformatted helper under
      `research-program/artifacts/` does not turn `main` red.

## Test gate
Named gate: the `lint-format` job of `Python CI`. Demonstrate it is load-bearing by temporarily
removing the new `extend-exclude` line, confirming `black --check` fails on the artifact files,
then restoring it.

## Non-goals
- Do not reformat the files under `research-program/artifacts/` — they are generated evidence and
  will be overwritten by the next mirror push, so formatting them fixes nothing durably.
- Do not widen the CLI `--exclude` in the shared workflow; the fix belongs in this repo's config.
