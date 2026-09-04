## Why

Owner requires one-click page navigation (B3 §3.2 `provenance.document`). Verified: `design-system/README.md:1-10` ships CSS tokens only — no `render/links.py` or HTML output module. **Missing behavior:** triple-link resolver. **Depends on:** Workflows B2-023 `document-mirror/v1`.

## Scope

Jinja/static helper resolving triple URLs in HTML output.

## Non-Goals

- Do NOT implement full output-substrate renderer (Pension-Data B2-029).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/doc_lineage/render/links.py` with `resolve_triple_link(tracked_variable) -> html`.
- [ ] Add `tests/render/test_triple_link_resolver.py` with fixture provenance object.

## Acceptance Criteria

- [ ] Named test: `tests/render/test_triple_link_resolver.py::test_emits_three_hrefs` passes.
- [ ] **Deliberate-break gate:** omit `page_anchor` → test **must FAIL** → revert.

_Surfaced by B2-025._
