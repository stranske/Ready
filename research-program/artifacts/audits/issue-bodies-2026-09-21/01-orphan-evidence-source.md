## Why (verified evidence)

`validate-structured-store` reports success for a communication-synthesis store whose evidence `stable_id` does not appear in `documents[]`, but every render command fails later with an adapter error. Operators who trust the validator as a publish gate ship stores that cannot produce HTML, PPTX, or DOCX.

- `src/deliverable_render/store/validate.py:221-228` — `_validate_pointer()` checks only evidence-object schema projection; it never cross-checks `source_id`/`stable_id` against declared `documents[]`.
- `src/deliverable_render/store/communication.py:64-68` — `_evidence()` rejects undeclared sources at render time: `source 'ghost-doc' is not a declared document`.
- `docs/STRUCTURED_STORE_VALIDATION.md:12-18` documents orphan checks for period and entry references but not evidence→document resolution.

**Reproduction (tip 3e4c68a):**

```bash
# Copy tests/fixtures/stores/communication_render.json, set
# entries[0].mentions[0].src.stable_id to "ghost-doc", then:
validate-structured-store /path/to/store.json   # exit 0, prints "structured store valid"
render-html-hub --store /path/to/store.json \
  --document-paths tests/fixtures/stores/communication_paths.json --out /tmp/hub.html
# exit 2; stderr contains: source 'ghost-doc' is not a declared document
```

## Tasks

- [ ] In `src/deliverable_render/store/validate.py`, collect document identities from `documents[]` (same `stable_id`/`name` rule as `communication.py:84-86`) and fail validation when any projected evidence `source_id` is not in that set (`validate.py:221-236` call sites for mentions and `pub.src`).
- [ ] Add a regression test in `tests/store/test_communication_render_profile.py` (or a dedicated validator test module) that mutates `communication_render.json` to reference an undeclared `stable_id` and asserts `validate_store(...).valid` is false with a diagnostic naming the orphan source.

## Acceptance Criteria

- Named test: `test_validator_rejects_evidence_source_not_in_documents` asserting `validate_store` fails when `mentions[].src.stable_id` references a document absent from `documents[]`.
- Deliberate-break → revert: remove the new cross-check in `validate.py` → confirm `test_validator_rejects_evidence_source_not_in_documents` FAILS → revert.

## Non-Goals

- Do NOT change `adapt_store` rejection behavior in `communication.py`; the adapter gate stays as-is.
- Do NOT broaden this issue to duplicate-document or missing-period seams (separate findings if filed).
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Surfaced by Track D audit 2026-09-21; verified by live repro on tip 3e4c68a._
