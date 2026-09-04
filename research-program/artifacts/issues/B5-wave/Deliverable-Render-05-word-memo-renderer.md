## Why

The work-environment inventory names Word memos as a first-class deliverable from the consultant-report comparison tool — change memo, continuity memo, cross-consultant memo — alongside the HTML hub and Excel ledgers ([INFORMATION-REQUEST-RESPONSE.md §D, consultant-report comparison tool](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). Deliverable-Render's README already allocates `render/docx` for memo rendering (`README.md:20`) and states every output must be a local file with no server ([README.md:9](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) constraint echoed at `README.md:7-12`). Verified: `tests/test_main.py:23-27` only tests template `add()`; the `render/` tree described at `README.md:16-21` does not exist. **Missing behavior:** no `.docx` memo renderer. **Latent fragility** — HTML hub (#2) and deck builder (#3) are filed; memos remain unimplemented.

## Scope

Implement `render/docx` — a Word memo renderer that consumes the structured store (post store-contract work) and emits `.docx` change/continuity memos matching the consultant tracker's memo shapes from [response §D](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).

## Non-Goals

- Do NOT require Word COM automation at runtime — write `.docx` via a pure-Python library (the response confirms both COM and library paths exist in the target environment; this repo stays portable).
- Do NOT implement the structured-store validator (separate issue).
- Do NOT add server endpoints or database dependencies (`README.md:9`).
- Scaffold-only completion does NOT count: emitting an empty `.docx` or a memo missing required sections is a failure. The deliberate-break gate below must be demonstrated.

## Tasks

- [ ] Create `src/deliverable_render/docx/__init__.py` and `src/deliverable_render/docx/memo.py` with `render_change_memo(store: StructuredStore, output_path: Path) -> Path` writing sections for material `T1`/`T2` changes using ledger field names from the adopted schemas (Doc-Lineage #4).
- [ ] Create `src/deliverable_render/docx/templates/change_memo.docx` (or equivalent programmatic styles) and `src/deliverable_render/docx/templates/continuity_memo.docx`.
- [ ] Add `src/deliverable_render/cli/render_docx.py` CLI entry wired in `pyproject.toml` `[project.scripts]` as `render-docx-memo`.
- [ ] Add `tests/docx/test_change_memo_renderer.py` using a committed synthetic store fixture under `tests/fixtures/stores/consultant_change_minimal.json`.
- [ ] Add `tests/docx/test_continuity_memo_renderer.py` for the continuity ledger slice.
- [ ] Perform deliberate-break verification (see Acceptance Criteria), capture FAIL output, then revert.

## Acceptance Criteria

- [ ] Named test: `tests/docx/test_change_memo_renderer.py::test_change_memo_includes_t1_sections` passes — opens the rendered `.docx` and asserts at least one `T1` change section with `canonical_section` and `change_type` text present.
- [ ] Named smoke command: `render-docx-memo --store tests/fixtures/stores/consultant_change_minimal.json --out /tmp/memo.docx` exits 0 and produces a non-empty `.docx` file.
- [ ] **Deliberate-break gate:** temporarily edit `src/deliverable_render/docx/memo.py` to skip rendering any row where `tier == "T1"`. `tests/docx/test_change_memo_renderer.py::test_change_memo_includes_t1_sections` **must FAIL**. Revert after capturing the failure.

## Implementation Notes

- Align section headings with consultant tracker ledger columns from [response §D](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) (`canonical_section`, `change_type`, `tier`, `prior_text`, `current_text`).
- Confirmed-green local reproduction (scaffold baseline): `python -m pytest tests/test_main.py -q` → passes today.
- Depends on Deliverable-Render store contract alignment issue and Doc-Lineage #4 ledger schemas for field names.
