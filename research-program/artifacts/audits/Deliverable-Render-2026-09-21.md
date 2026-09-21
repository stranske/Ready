Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 2 ([#36](https://github.com/stranske/Deliverable-Render/issues/36), [#37](https://github.com/stranske/Deliverable-Render/issues/37)). Agents Issue Format Guard success on both (runs 35667081941, 35667088177).

# Deliverable-Render audit — 2026-09-21 (attempt 2)

**Tip:** `3e479ba4cfe652bf07ca6beea2df48c9caa10e46` (`fix(store): reject duplicate document identities (#32) (#35)`)

## Verdict

Track D refill re-run after morning audit issues #31/#32/#28 merged same day (PRs #33–#35, #34). Primary journey still passes; CF7 memo tier validation now WORKS on both legacy and communication paths. Two new validator→renderer seam defects meet the filing bar.

| Priority | Finding | Evidence | Filed |
| --- | --- | --- | --- |
| P1 | Evidence `page` of 0, missing, or JSON float passes `validate-structured-store` then fails at render | `src/deliverable_render/store/validate.py:149-180`; `src/deliverable_render/store/communication.py:69-72`; seam test at `tests/store/test_communication_render_profile.py:293-310` | [#36](https://github.com/stranske/Deliverable-Render/issues/36) |
| P2 | Entry `thesis`/`pub` without resolvable `first`/`last` period passes validation then fails at adapt | `src/deliverable_render/store/validate.py:270-278`; `src/deliverable_render/store/communication.py:123-147` | [#37](https://github.com/stranske/Deliverable-Render/issues/37) |

## Product scorecard (Phase 1.5)

| ID | Core function | Score | How exercised |
| --- | --- | --- | --- |
| CF1 | An operator can validate a communication-synthesis store | WORKS | `validate_store(valid_evidence_store.json)` → empty issues |
| CF2 | A developer can render a deep-linked offline HTML hub | WORKS | `render-html-hub` on synthetic store; varying record text changes output |
| CF3 | A developer can build a manifest-gated PPTX deck | WORKS | `tests/test_deck_completeness_gate.py` 8/8 pass |
| CF4 | An operator can render consultant memos | WORKS | `render-docx-memo --kind change` → DOCX written |
| CF5 | An operator can run offline capability probes | WORKS | `tests/test_probe_offline_and_minimal.py` 10/10 pass |
| CF6 | A validated communication-synthesis store renders to HTML/PPTX/DOCX | WORKS | All three CLIs on `communication_render.json` exit 0; varying mention text changes hub HTML |
| CF7 | Memo tier vocabulary is validated at load | WORKS | T9 rejected on legacy `StructuredStore.from_dict` and communication `adapt_memo` (#34 fixed) |

**Primary journey:** communication-synthesis store → validated → HTML hub + PPTX deck + DOCX memo. Passes on tip.

**Closed-still-broken:** #27/#31/#32/#28 reproductions no longer apply (merged #25, #33–#35, #34).

## Reproductions

```text
# P1 evidence page seam
# mutate mentions[0].src.page → 0 | 3.0 | delete page
validate-structured-store store.json  # exit 0
render-html-hub ...                   # exit 2: positive one-based evidence page required

# P2 thesis/pub period seam
# remove first/last from entries with thesis or pub.src
validate-structured-store store.json  # exit 0
render-html-hub ...                   # exit 2: thesis/pub period must be a nonempty string
```

- `python3 -m pytest -q --no-cov` → 158 passed
- `python3 -m ruff check src tests` → clean
- Issue bodies preflighted via `.github/scripts/issue_format.py`
- Open dedup: no overlap with closed #31/#32 or open tracker issues

## Dimension coverage (abbreviated)

| Dim | Notes |
| --- | --- |
| D1 | Two validator seam defects filed; no additional verified correctness bugs |
| D2 | No actionable duplication campaign |
| D3 | Validator→adapter page/period gaps dominate (feeds #36, #37); prior seams fixed on tip |
| D4 | No browser UI; CLIs exercised directly |
| D5–D8 | No filable near-term items |

Confidence: **high** for both filed issues. #36 refuted only if validator rejects invalid evidence pages. #37 refuted only if thesis/pub without period fails validation.
