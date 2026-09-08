# Ready formatting failure: existing issue owns repair

Live main d1a4aa222367e90ab89337d2eaab1c9115a646b4 fails run https://github.com/stranske/Ready/actions/runs/34243116713 in Python CI / lint-format. Black lists unformatted mirrored research proof scripts. Refreshed pyproject.toml has Ruff extend-exclude at line 64 but no Black exclusion under tool.black at line 102.

Existing open issue https://github.com/stranske/Ready/issues/557 exactly covers this failure; do not create a duplicate. Its requested Black extend-exclude must be a regex string, preserving default exclusions. Acceptance should exercise discovery with an unformatted artifact alongside ordinary project Python, then run black --check . and the repository hygiene tests. No source changes or issue mutation in this research-only run.
