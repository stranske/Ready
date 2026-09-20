## Why

`README.md:10` says renderers are built as local commands, and `README.md:27` says a store produced by the work tools renders without a translation step. The current communication-synthesis fixture is accepted by `src/deliverable_render/store/validate.py:176-263`, but neither renderer input loader can load it: `Store.from_json` at `src/deliverable_render/store/__init__.py:155-197` requires `documents[].stable_id`, `documents[].path`, and `records`, while `StructuredStore.from_json` at `src/deliverable_render/store/__init__.py:281-315` requires memo `changes`. The reproduced valid fixture therefore fails both loaders. `pyproject.toml:29-32` exposes only the validator and the DOCX command. This is a current integration break: a validated canonical store has no public path to HTML, PPTX, or DOCX rendering.

## Scope

Create one documented rendering profile for the communication-synthesis format and make it consumable through local HTML, PPTX, and DOCX commands. Preserve existing `Store` and `StructuredStore` callers while explicitly requiring any data needed for local-file evidence links; do not invent document paths or provenance.

## Non-Goals

- Do not weaken `src/deliverable_render/store/validate.py` evidence or reference checks.
- Do not add a hosted service, database, or proprietary fixture.
- Do not silently manufacture a document path when a source document cannot be mapped.
- Scaffold-only completion does NOT count: a command that parses arguments but cannot render the valid communication-synthesis fixture into each promised output is a failure of this issue.

## Tasks

- [ ] Add a documented adapter in `src/deliverable_render/store/` that maps a validated communication-synthesis store plus an explicit document-path mapping into the existing renderer inputs without fabricating evidence fields.
- [ ] Add `src/deliverable_render/cli/render_html.py` and wire a `render-html-hub` command in `pyproject.toml` that validates, adapts, and writes a self-contained HTML hub.
- [ ] Add `src/deliverable_render/cli/render_pptx.py` and wire a `render-pptx-deck` command in `pyproject.toml` that validates, adapts, applies an explicit manifest/template, and writes a PPTX file.
- [ ] Extend `src/deliverable_render/cli/render_docx.py` to accept the documented rendering profile or fail with a named mapping diagnostic rather than parsing a different silent schema.
- [ ] Add end-to-end fixtures and command tests under `tests/` for a valid communication-synthesis store, an explicit document-path mapping, and each of the three rendered outputs.

## Acceptance Criteria

- [ ] `python3 -m pytest tests/store tests/docx tests/test_render_html_offline.py tests/test_deck_completeness_gate.py -q` passes and includes an end-to-end case that first accepts the communication-synthesis fixture through `validate_store` and then renders each supported output.
- [ ] `render-html-hub`, `render-pptx-deck`, and `render-docx-memo` each exit 0 with synthetic inputs and produce a non-empty output file; the HTML output remains free of external resource URLs.
- [ ] A store that lacks the required document-path mapping fails the named adapter or command test with a mapping diagnostic and does not emit a deliverable.
- [ ] Deliberate-break gate: temporarily bypass the adapter's document-path-mapping check; the named missing-mapping test must fail, then revert the temporary change before review.

## Implementation Notes

`docs/STRUCTURED_STORE_VALIDATION.md:36-39` currently documents the semantic validator as a separate gate from renderer loaders. Update that boundary and `README.md:25-27` so supported mappings, inputs, and output commands are unambiguous. Keep all citations and test fixtures repository-relative.
