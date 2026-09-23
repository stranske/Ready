Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 1 ([#47](https://github.com/stranske/Deliverable-Render/issues/47)). Agents Issue Format Guard success (run 35842880654).

REFUTED: https://github.com/stranske/Deliverable-Render/issues/40 — cross-entry `entry_id` now rejected by `validate_store` with `cross-entry-mention` on tip `a867f3f`.
REFUTED: https://github.com/stranske/Deliverable-Render/issues/41 — `pub` without detail/state now rejected by `validate_store` with `missing-pub-detail` on tip `a867f3f`.

# Deliverable-Render audit — 2026-09-23

**Tip:** `a867f3fe6817d589bd3a624d6670fb3aba2c851e` (`chore: sync workflow templates`)

## Verdict

Track D refill on tip after #40/#41 merged. Primary journey (validate → HTML + PPTX + DOCX on `communication_render.json`) still passes. Closed-issue reproductions for #40/#41 no longer apply. Open #37 (thesis/pub period without `first`/`last`) still reproduces. One new validator→renderer seam filed.

| Priority | Finding | Evidence | Filed |
| --- | --- | --- | --- |
| P2 | Store with only whitespace mentions (no thesis/pub records) passes validation then fails all render CLIs | `src/deliverable_render/store/validate.py:245-311`; `src/deliverable_render/store/communication.py:111-112`, `:151-152`; `tests/store/test_communication_render_profile.py:385-396` | [#47](https://github.com/stranske/Deliverable-Render/issues/47) |

## Product scorecard (Phase 1.5)

| ID | Core function | Score | How exercised |
| --- | --- | --- | --- |
| CF1 | An operator can validate a communication-synthesis store | WORKS | `validate_store(valid_evidence_store.json)` → empty issues |
| CF2 | A developer can render a deep-linked offline HTML hub | WORKS | `render-html-hub` on fixtures; varying mention text |
| CF3 | A developer can build a manifest-gated PPTX deck | WORKS | `tests/test_deck_completeness_gate.py` 8/8 |
| CF4 | An operator can render consultant memos | WORKS | `render-docx-memo --profile communication-synthesis` |
| CF5 | An operator can run offline capability probes | WORKS | `tests/test_probe_offline_and_minimal.py` 10/10 |
| CF6 | A validated communication-synthesis store renders to HTML/PPTX/DOCX | WORKS | three CLIs on `communication_render.json` |
| CF7 | Memo tier vocabulary is validated at load | WORKS | T9 rejected on legacy and communication paths |

**Primary journey:** communication-synthesis store → validated → HTML hub + PPTX deck + DOCX memo. Passes on tip.

**Closed-still-broken:** none. **Open validator seam:** #37 (period resolution for thesis/pub), #47 (no renderable content).

## Reproductions

```text
# #37 still open
python3 reproduction from issue #37 → validate_store valid, render-html-hub exit 2

# #47 (new)
entries with only whitespace mention → validate_store valid, render-html-hub exit 2
```

- `python3 -m pytest -q --no-cov` → 188 passed
- Dedup: no overlap with open #37; #40/#41 closed fixed

## Dimension coverage (abbreviated)

| Dim | Notes |
| --- | --- |
| D1 | One verified validator seam filed (#47); no additional P0/P1 correctness bugs |
| D2 | No actionable duplication campaign |
| D3 | Validator→adapter renderability gap (#47); #37 still open |
| D4 | No browser UI; CLIs exercised directly |
| D5–D8 | No filable near-term items |

Confidence: **high** for #47. Refuted only if `validate_store` rejects the whitespace-only fixture before render.
