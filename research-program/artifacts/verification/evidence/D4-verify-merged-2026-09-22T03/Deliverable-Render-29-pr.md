# PR #29

<!-- pr-preamble:start -->
<!-- meta:issue:27 -->
> **Source:** Issue #27

Closes #27

<!-- pr-preamble:end -->

<!-- auto-status-summary:start -->
## Automated Status Summary
#### Scope
`README.md:10` says renderers are built as local commands, and `README.md:27` says a store produced by the work tools renders without a translation step. The current communication-synthesis fixture is accepted by `src/deliverable_render/store/validate.py:176-263`, but neither renderer input loader can load it: `Store.from_json` at `src/deliverable_render/store/__init__.py:155-197` requires `documents[].stable_id`, `documents[].path`, and `records`, while `StructuredStore.from_json` at `src/deliverable_render/store/__init__.py:281-315` requires memo `changes`. The reproduced valid fixture therefore fails both loaders. `pyproject.toml:29-32` exposes only the validator and the DOCX command. This is a current integration break: a validated canonical store has no public path to HTML, PPTX, or DOCX rendering.

#### Tasks
- [x] Add a documented adapter in `src/deliverable_render/store/` that maps a validated communication-synthesis store plus an explicit document-path mapping into the existing renderer inputs without fabricating evidence fields.
- [x] Add `src/deliverable_render/cli/render_html.py` and wire a `render-html-hub` command in `pyproject.toml` that validates, adapts, and writes a self-contained HTML hub.
- [x] Add `src/deliverable_render/cli/render_pptx.py` and wire a `render-pptx-deck` command in `pyproject.toml` that validates, adapts, applies an explicit manifest/template, and writes a PPTX file.
- [x] Extend `src/deliverable_render/cli/render_docx.py` to accept the documented rendering profile or fail with a named mapping diagnostic rather than parsing a different silent schema.
- [x] Add end-to-end fixtures and command tests under `tests/` for a valid communication-synthesis store, an explicit document-path mapping, and each of the three rendered outputs.

#### Acceptance criteria
- [x] `python3 -m pytest tests/store tests/docx tests/test_render_html_offline.py tests/test_deck_completeness_gate.py -q` passes and includes an end-to-end case that first accepts the communication-synthesis fixture through `validate_store` and then renders each supported output.
- [x] `render-html-hub`, `render-pptx-deck`, and `render-docx-memo` each exit 0 with synthetic inputs and produce a non-empty output file; the HTML output remains free of external resource URLs.
- [x] A store that lacks the required document-path mapping fails the named adapter or command test with a mapping diagnostic and does not emit a deliverable.
- [x] Deliberate-break gate: temporarily bypass the adapter's document-path-mapping check; the named missing-mapping test must fail, then revert the temporary change before review.

<!-- auto-status-summary:end -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **New Features**
  * Added offline rendering for HTML evidence hubs, PowerPoint decks, and Word memos.
  * Added command-line tools supporting document mappings, deck manifests, reviewed memo overlays, custom titles, layouts, and controlled overwrites.
* **Validation**
  * Added checks for source mappings, citation pages, references, identities, and memo data before publication.
  * Added diagnostics for invalid or incomplete inputs and protection against overwriting source files.
* **Documentation**
  * Expanded guidance for interoperability, configuration, overwrite behavior, validation commands, diagnostics, and offline evidence links.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->