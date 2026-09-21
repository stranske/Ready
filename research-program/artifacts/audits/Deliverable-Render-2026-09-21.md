Scorecard: 6 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 2 ([#31](https://github.com/stranske/Deliverable-Render/issues/31), [#32](https://github.com/stranske/Deliverable-Render/issues/32)). Agents Issue Format Guard success on both (runs 35579311070, 35579312080).

# Deliverable-Render audit — 2026-09-21

**Tip:** `3e4c68a9ed296fcdf88d2fedb07535d7b46087c7` (`feat(store): validate structured-store references and evidence (#25)`)

## Verdict

Track D refill after PR #25 closed the P1 bridge (#27). The primary journey now passes: a validated communication-synthesis store renders to HTML, PPTX, and DOCX via the three new public commands. Two new validator→renderer seam defects meet the filing bar; open #28 (memo tier T9) was deduped, not re-filed.

| Priority | Finding | Evidence | Filed |
| --- | --- | --- | --- |
| P1 | Evidence `stable_id` not declared in `documents[]` passes `validate-structured-store` then fails at render | `src/deliverable_render/store/validate.py:221-228`; `src/deliverable_render/store/communication.py:64-68` | [#31](https://github.com/stranske/Deliverable-Render/issues/31) |
| P2 | Duplicate `documents[]` identity passes validation then fails at `adapt_store` | `src/deliverable_render/store/validate.py:195-197`; `src/deliverable_render/store/communication.py:84-88` | [#32](https://github.com/stranske/Deliverable-Render/issues/32) |

## Product scorecard (Phase 1.5)

| ID | Core function | Score | How exercised |
| --- | --- | --- | --- |
| CF1 | An operator can validate a communication-synthesis store | WORKS | `validate_store(valid_evidence_store.json)` → empty issues |
| CF2 | A developer can render a deep-linked offline HTML hub | WORKS | `render_html` on synthetic store; varying record text changes output |
| CF3 | A developer can build a manifest-gated PPTX deck | WORKS | `tests/test_deck_completeness_gate.py` 8/8 pass |
| CF4 | An operator can render consultant memos | WORKS | `render-docx-memo --kind change` → 36781-byte DOCX |
| CF5 | An operator can run offline capability probes | WORKS | `tests/test_probe_offline_and_minimal.py` 10/10 pass |
| CF6 | A validated communication-synthesis store renders to HTML/PPTX/DOCX | WORKS | All three CLIs on `communication_render.json` exit 0; varying mention text changes hub HTML |
| CF7 | Memo tier vocabulary is validated at load | PARTIAL | `tier=123` rejected; `tier=T9` loads on legacy path then empty-material error (#28 open); communication profile rejects T9 at `adapt_memo` |

**Primary journey:** communication-synthesis store → validated → HTML hub + PPTX deck + DOCX memo. Passes on tip.

**Closed-still-broken:** #27 reproduction no longer applies (bridge shipped). #28 still reproduces on legacy `StructuredStore` path.

## Reproductions

```text
# CF6 bridge (now works)
render-html-hub --store tests/fixtures/stores/communication_render.json \
  --document-paths tests/fixtures/stores/communication_paths.json --out /tmp/hub.html  # exit 0

# P1 orphan evidence source
# mutate mentions[0].src.stable_id → "ghost-doc"
validate-structured-store store.json  # exit 0
render-html-hub ...  # exit 2: source 'ghost-doc' is not a declared document

# P2 duplicate document
# append {"name": "doc-1"} to documents[]
validate-structured-store dup.json  # exit 0
render-html-hub ...  # exit 2: duplicate document identity 'doc-1'
```

- `python3 -m pytest -q --no-cov` → 151 passed
- `python3 -m ruff check src tests` → clean
- Issue bodies preflighted via `.github/scripts/issue_format.py`
- Open dedup: #28 (tier T9) kept open; no overlap with #31/#32

## Dimension coverage (abbreviated)

| Dim | Notes |
| --- | --- |
| D1 | Two validator seam defects filed; no additional verified correctness bugs |
| D2 | No actionable duplication campaign |
| D3 | Validator→adapter gaps dominate (feeds #31, #32); CF6 bridge now wired |
| D4 | No browser UI; CLIs exercised directly |
| D5–D8 | No filable near-term items |

Confidence: **high** for both filed issues. #31 refuted only if validator rejects undeclared evidence sources. #32 refuted only if duplicate document identities fail validation.
