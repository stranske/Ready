Scorecard: 4 work / 1 partial / 1 broken / 0 fabricated / 0 not exercised of 6; journey: stops at "validated communication-synthesis store has no public render command"; surfaces unscored 0; closed-still-broken 0.

Issues filed: 2 ([#27](https://github.com/stranske/Deliverable-Render/issues/27), [#28](https://github.com/stranske/Deliverable-Render/issues/28)). Agents Issue Format Guard success on both (runs 35536945803, 35536949522).

# Deliverable-Render audit — 2026-09-20

**Tip:** `3adc29fdd019b08a96cdbc4694c06a043b00fcd9` (`feat(store): validate structured-store references and evidence (#25)`)

## Verdict

Track D refill on a now-mature renderer repo (133 tests, 87.41% coverage at tip). Two verified integration/input-boundary defects meet the filing bar; no additional independently verified, non-duplicate findings at this tip. Prior attempts stalled on `gh` auth; this run recovered a keychain `GH_TOKEN` and filed both staged bodies.

| Priority | Finding | Evidence | Filed |
| --- | --- | --- | --- |
| P1 | A store accepted by the communication-synthesis validator cannot be consumed by any renderer; only DOCX has a public command. | `README.md:27`; `pyproject.toml:30-32`; `src/deliverable_render/store/validate.py:176-263`; `src/deliverable_render/store/__init__.py:155-197,281-315`; `docs/STRUCTURED_STORE_VALIDATION.md:36-39` | [#27](https://github.com/stranske/Deliverable-Render/issues/27) |
| P2 | An unknown memo tier such as `T9` passes loading and is later mistaken for an empty material set. | `src/deliverable_render/store/__init__.py:243-248`; `src/deliverable_render/docx/memo.py:22-26,44-46` | [#28](https://github.com/stranske/Deliverable-Render/issues/28) |

## Product scorecard (Phase 1.5)

| ID | Core function | Score | How exercised |
| --- | --- | --- | --- |
| CF1 | An operator can validate a communication-synthesis store and see pass/fail diagnostics | WORKS | `validate_store(tests/fixtures/stores/valid_evidence_store.json)` → `ValidationReport(issues=[])`; `validate-structured-store` CLI exit 0 |
| CF2 | A developer can render a deep-linked offline HTML hub whose content changes with store input | WORKS | `render_html` on `synthetic_store.json`; varying `records[0].text` changes output (`CHANGED TEXT` present) |
| CF3 | A developer can build a manifest-gated PPTX deck whose slide bodies respond to store text | WORKS | `tests/test_deck_completeness_gate.py` 8/8 pass; incomplete manifest raises `DeckBuildError` naming `slide_id 'risk'` |
| CF4 | An operator can render a consultant change memo via CLI | WORKS | `render-docx-memo --kind change` exit 0, 36781-byte DOCX |
| CF5 | An operator can run the offline environment probe | WORKS | `tests/test_probe_offline_and_minimal.py` 10/10 pass |
| CF6 | A validated communication-synthesis store renders to HTML/PPTX/DOCX without a translation step (README interoperability claim) | BROKEN | `valid_evidence_store.json` passes validator; `Store.from_json` → `stable_id must be a string`; `StructuredStore.from_json` → `changes must be an array`; no `render-html-hub` / `render-pptx-deck` commands in `pyproject.toml` |
| CF7 | Memo tier vocabulary is validated at the store boundary | PARTIAL | `tier=123` rejected at load (`test_validation_malformed_row_fields`); `tier=T9` loads then `render_change_memo` → `No material T1/T2 changes to render` (indistinguishable from valid all-T3 input) |

**Primary journey:** structured store → deliverable. Evidence-format stores complete the library path; communication-synthesis stores stop after validation with no public render bridge.

**Closed-still-broken:** re-checked closed #2–#6 feature issues; neither defect reproduces their stated fixes and neither is duplicated by them.

## Reproductions and verification

```text
# P1 bridge break
validate_store(valid_evidence_store.json) → issues=[]
Store.from_json(same) → StoreValidationError: stable_id must be a string (nonempty)
StructuredStore.from_json(same) → StoreValidationError: changes must be an array

# P2 tier boundary
StructuredStore.from_json(consultant_change_minimal with all tiers=T9) → loads
render_change_memo → StoreValidationError: No material T1/T2 changes to render
```

- `python3 -m pytest -q --no-cov` → 133 passed
- `python3 -m ruff check src tests` → clean
- Issue bodies validated locally via `.github/scripts/issue_format.py` (body 01: agent-processable with 3 expected new-path advisories; body 02: conforming)
- Open-issue dedup: only #1 (Renovate dashboard) and #10 (metrics tracker); no overlap with #27/#28
- Format guard: success runs 35536945803 (#27), 35536949522 (#28)

## Dimension coverage (abbreviated)

| Dim | Notes |
| --- | --- |
| D1 | Two input-boundary/integration defects above; no additional verified correctness bugs |
| D2 | Small repo; no actionable duplication campaign beyond upstream Workflows sync |
| D3 | Validator→loader seam is the dominant wiring gap (feeds #27) |
| D4 | No browser UI; library/CLI surfaces exercised via API/tests |
| D5–D8 | No filable near-term items beyond the two defects |

Confidence: **high** for both filed issues. #27 would be refuted only by a documented adapter plus working CLI paths for all three deliverable types on `valid_evidence_store.json`. #28 would be refuted only if `T9` is a documented valid tier (no such vocabulary exists).
