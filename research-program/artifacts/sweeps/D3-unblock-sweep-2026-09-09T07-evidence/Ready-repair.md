# Ready formatting failure: existing issue owns repair

At observed main ae25ff4ae863037cc674b963380b06d8137a6204, https://github.com/stranske/Ready/actions/runs/34322664837 completed with failure. Python CI / lint-format lists unformatted Python files under research-program/artifacts. The refreshed pyproject.toml has Ruff extend-exclude at line 64, but tool.black at lines 102-104 has no exclusion.

Existing open https://github.com/stranske/Ready/issues/557 owns this repair; no duplicate issue is needed. Add a Black extend-exclude regex string for research-program/artifacts, retaining default exclusions. Validate discovery with an unformatted artifact and a normal project Python file, then run black --check . and pytest tests/test_repo_hygiene.py. The current issue includes a deliberate-break check. No source changes or remote mutation in this research-only run. Current failure log, final run state, issue body and clone SHA are retained alongside this note.
