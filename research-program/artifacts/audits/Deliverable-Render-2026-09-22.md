Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 2 ([#40](https://github.com/stranske/Deliverable-Render/issues/40), [#41](https://github.com/stranske/Deliverable-Render/issues/41)). Agents Issue Format Guard success on both (runs 35784299476, 35784301083).

# Deliverable-Render audit — 2026-09-22

**Tip:** `2360128523f4a898421b0ba18a11e4399e89ffc2` (`fix(store): reject invalid evidence pages during validation (#36)`)

## Verdict

Track D refill after #36 merged on tip. Primary journey still passes on documented fixtures. Closed-issue reproductions for #28/#31/#32/#36 no longer apply. Two new validator→renderer seam defects meet the filing bar; open #37 (thesis/pub period) unchanged.

| Priority | Finding | Evidence | Filed |
| --- | --- | --- | --- |
| P1 | Mention `entry_id` naming another entry passes validation then fails at render | `src/deliverable_render/store/validate.py:256-263`; `src/deliverable_render/store/communication.py:104-107`; seam test `tests/store/test_communication_render_profile.py:423-434` | [#40](https://github.com/stranske/Deliverable-Render/issues/40) |
| P2 | `pub.src` without `detail` or `state` passes validation then fails at render | `src/deliverable_render/store/validate.py:273-282`; `src/deliverable_render/store/communication.py:136-145` | [#41](https://github.com/stranske/Deliverable-Render/issues/41) |

## Product scorecard (Phase 1.5)

| ID | Core function | Score | How exercised |
| --- | --- | --- | --- |
| CF1 | An operator can validate a communication-synthesis store | WORKS | `validate_store(valid_evidence_store.json)` → empty issues |
| CF2 | A developer can render a deep-linked offline HTML hub | WORKS | `render_html` varying marker text changes output |
| CF3 | A developer can build a manifest-gated PPTX deck | WORKS | `tests/test_deck_completeness_gate.py` 8/8 pass |
| CF4 | An operator can render consultant memos | WORKS | `render-docx-memo --profile communication-synthesis` → DOCX written |
| CF5 | An operator can run offline capability probes | WORKS | `tests/test_probe_offline_and_minimal.py` 10/10 pass |
| CF6 | A validated communication-synthesis store renders to HTML/PPTX/DOCX | WORKS | All three CLIs on `communication_render.json`; varying mention text changes hub HTML |
| CF7 | Memo tier vocabulary is validated at load | WORKS | T9 rejected on both legacy and communication paths |

**Primary journey:** communication-synthesis store → validated → HTML hub + PPTX deck + DOCX memo. Passes on tip.

**Closed-still-broken:** #27/#31/#32/#28/#36 reproductions no longer apply (merged #25, #33–#35, #34, #36).

## Reproductions

```text
# P1 cross-entry mention_id seam
# set entries[0].mentions[0].entry_id to another entry's id
validate-structured-store store.json  # exit 0
render-html-hub ...                   # exit 2: names another entry

# P2 pub detail seam
# remove pub.detail and pub.state while pub.src remains
validate-structured-store store.json  # exit 0
render-html-hub ...                   # exit 2: pub detail must be a nonempty string
```

- `python3 -m pytest -q --no-cov` → 185 passed
- Issue bodies preflighted via `.github/scripts/issue_format.py`
- Open dedup: #37 still open (thesis/pub period); no overlap with #40/#41

## Dimension coverage (abbreviated)

| Dim | Notes |
| --- | --- |
| D1 | Two validator seam defects filed; no additional verified correctness bugs |
| D2 | No actionable duplication campaign |
| D3 | Validator→adapter mention/pub gaps dominate (feeds #40, #41); #36 fixed on tip |
| D4 | No browser UI; CLIs exercised directly |
| D5–D8 | No filable near-term items |

Confidence: **high** for both filed issues. Each refuted only if `validate_store` rejects the mutated fixture before render.
