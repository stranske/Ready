## Why (verified evidence)

A communication-synthesis store with two `documents[]` rows sharing the same identity (`name` or `stable_id`) passes `validate-structured-store`, then fails at render with a duplicate-document error. The validator already enforces unique period and entry IDs; document identity should meet the same gate.

- `src/deliverable_render/store/validate.py:195-197` — loads the `documents` array but performs no per-document semantic checks (no duplicate-identity scan).
- `src/deliverable_render/store/communication.py:84-88` — adapter rejects `duplicate document identity 'doc-1'` when building the render `Store`.
- `docs/STRUCTURED_STORE_VALIDATION.md` documents unique `id` fields for periods and entries but not duplicate document identities.

**Reproduction (tip 3e4c68a):**

```bash
# Copy tests/fixtures/stores/communication_render.json and append
# {"name": "doc-1"} to documents[], then:
validate-structured-store /path/to/dup-doc.json   # exit 0
render-html-hub --store /path/to/dup-doc.json \
  --document-paths tests/fixtures/stores/communication_paths.json --out /tmp/hub.html
# exit 2; stderr contains: duplicate document identity 'doc-1'
```

## Tasks

- [ ] In `src/deliverable_render/store/validate.py`, after loading `sections.get("documents", [])`, reject duplicate document identity using the same `stable_id`-if-present-else-`name` rule as `communication.py:84-86`.
- [ ] Add regression test `test_validator_rejects_duplicate_document_identity` that appends a second `{"name": "doc-1"}` row to `communication_render.json` and asserts `validate_store` is invalid with a path under `/documents`.

## Acceptance Criteria

- Named test: `test_validator_rejects_duplicate_document_identity` asserting validation fails before any render command is invoked.
- Deliberate-break → revert: remove the duplicate scan → confirm `test_validator_rejects_duplicate_document_identity` FAILS → revert.

## Non-Goals

- Do NOT change how `adapt_store` detects duplicates in `communication.py`.
- Do NOT add filesystem existence checks for mapped paths (out of scope).
- No scaffolding / TODO-only changes.

_Surfaced by Track D audit 2026-09-21; verified by live repro on tip 3e4c68a._
