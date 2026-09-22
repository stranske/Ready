# PR #33

Closes #31

## Summary

- derive validator document identities with the renderer's `stable_id`-then-`name` precedence
- reject projected mention and publication evidence when `source_id` does not resolve in `documents[]`
- add the named regression across both evidence-pointer call sites with an orphan-source diagnostic

## Validation

- `.venv/bin/python -m pytest tests/store/test_communication_render_profile.py::test_validator_rejects_evidence_source_not_in_documents -q -o addopts=` — 2 passed
- `.venv/bin/python -m pytest -q` — 153 passed; 88.50% coverage
- `.venv/bin/ruff check src tests` — passed
- `.venv/bin/ruff format --check src tests` — passed
- `.venv/bin/mypy src` — passed
- deliberate break: removed only the new document cross-check; both named regression cases failed because validation incorrectly returned valid; restored the cross-check and the full suite passed
