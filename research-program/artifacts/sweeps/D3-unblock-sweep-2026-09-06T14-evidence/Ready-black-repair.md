# Ready: exclude mirrored research evidence from Black discovery

Staged repair specification; no repository code changed and no PR opened under the research executor rules.

Latest inspected CI: https://github.com/stranske/Ready/actions/runs/34038402493 at main `58b1ccc9e4a35079828b593ae02a40b54c59f032`.

`Python CI / lint-format` fails because Black discovers eight Python research proof scripts in `research-program/artifacts/audits/`. The fresh clone's `pyproject.toml` already has `[tool.ruff] extend-exclude = ["research-program/artifacts"]`, but `[tool.black]` only sets line-length and target-version. This is a mechanical formatting-scope mismatch.

Proposed edit to the existing `[tool.black]` table in `pyproject.toml`:

```toml
extend-exclude = '^/research-program/artifacts/'
```

Black expects one regular-expression string here, not Ruff's array syntax. Preserve the current line length, target version, and default excludes. Evidence artifacts remain reviewable; production source and tests remain covered by Black.

Validation for the implementation lane: run the pinned `black --check .` from the repository root and inspect `black --check --verbose .` to confirm research artifacts are excluded while `src` and `tests` still participate; run normal lint-format CI. This sweep verified the configuration and failing CI evidence, but did not implement or test the proposed edit. Recheck the current main configuration before opening a repair PR.
