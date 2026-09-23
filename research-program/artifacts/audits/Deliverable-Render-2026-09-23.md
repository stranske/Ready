Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0 (this unit). Fleet delivery today: 1 ([#47](https://github.com/stranske/Deliverable-Render/issues/47) from unit `D-audit-Deliverable-Render--2026-09-23T09-11-14Z`; format guard run 35842880654 succeeded).

REFUTED: https://github.com/stranske/Deliverable-Render/issues/40 — cross-entry `entry_id` rejected with `cross-entry-mention` on tip `a867f3f`.
REFUTED: https://github.com/stranske/Deliverable-Render/issues/41 — `pub` without detail/state rejected with `missing-pub-detail` on tip `a867f3f`.

# Deliverable-Render audit — 2026-09-23 (attempt 2)

**Unit:** `D-audit-Deliverable-Render--2026-09-23T22-11-12Z` (refill re-run after scorecard headline parse failure on first engine pass; line 1 re-verified here.)

**Tip:** `a867f3fe6817d589bd3a624d6670fb3aba2c851e` (`chore: sync workflow templates`)

## Verdict

Independent re-audit on unchanged tip. Phase 1.5 scorecard and primary journey (validate → HTML + PPTX + DOCX on `communication_render.json`) pass. Closed-issue reproductions for #40/#41 no longer apply. Open validator seams remain #37 (thesis/pub without resolvable `first`/`last`) and #47 (no renderable content after whitespace-only mentions). No additional verified defects met the filing bar; uncited extra `documents[]` rows failing at adapt-time only (paths supplied at render) are documented in `tests/store/test_communication_render_profile.py:202-212` and treated as intentional render-profile behavior, not a new validator bug.

| Priority | Finding | Evidence | Filed |
| --- | --- | --- | --- |
| P2 (open) | Entry `thesis`/`pub` without `first`/`last` passes validation then fails adapt | `src/deliverable_render/store/validate.py:303-311`; `src/deliverable_render/store/communication.py:123-130` | [#37](https://github.com/stranske/Deliverable-Render/issues/37) (prior round) |
| P2 (open) | Whitespace-only mentions pass validation then fail all render CLIs | `src/deliverable_render/store/validate.py:245-311`; `src/deliverable_render/store/communication.py:111-112`, `:151-152` | [#47](https://github.com/stranske/Deliverable-Render/issues/47) (09:11Z unit) |

## Product scorecard (Phase 1.5)

| ID | Core function | Score | How exercised |
| --- | --- | --- | --- |
| CF1 | An operator can validate a communication-synthesis store | WORKS | `validate_store(valid_evidence_store.json)` → valid |
| CF2 | A developer can render a deep-linked offline HTML hub | WORKS | `render-html-hub` on fixtures; ALPHA vs BETA mention text changes hub HTML |
| CF3 | A developer can build a manifest-gated PPTX deck | WORKS | `tests/test_deck_completeness_gate.py` (8 tests) |
| CF4 | An operator can render consultant memos | WORKS | `render-docx-memo --profile communication-synthesis` |
| CF5 | An operator can run offline capability probes | WORKS | `tests/test_probe_offline_and_minimal.py` (10 tests) |
| CF6 | A validated communication-synthesis store renders to HTML/PPTX/DOCX | WORKS | `test_validated_store_renders_all_three_public_outputs` |
| CF7 | Memo tier vocabulary is validated at load | WORKS | invalid tier rejected on communication memo path |

**Primary journey:** communication-synthesis store → validated → HTML hub + PPTX deck + DOCX memo. Passes on tip.

## Reproductions (tip `a867f3f`)

```text
# #37 still open — remove first/last from entry with thesis
validate_store → valid; render-html-hub → exit 2 (thesis period must be a nonempty string)

# #47 — open; filed earlier today
validate_store → valid; render-html-hub → exit 2 (no renderable entry text)

# #40/#41 closed — now fail validation
cross-entry mention → cross-entry-mention; pub without detail/state → missing-pub-detail
```

- `python3 -m pytest -q --no-cov` → 188 passed
- `python3 -m ruff check src tests` → clean
- `gh` unavailable in this seat (no `GH_TOKEN`); dedup against open #37/#47 via local queue `intake_urls_before`; no `gh issue create` this unit

## Dimension coverage (abbreviated)

| Dim | Notes |
| --- | --- |
| D1 | No new P0/P1 correctness bugs beyond open #37/#47 |
| D2 | No actionable duplication campaign |
| D3 | Validator→adapter seams concentrated in open #37, #47 |
| D4 | No browser UI; CLIs exercised directly |
| D5–D8 | No filable near-term items |

Confidence: **high** that no new issue should be filed this unit. **Medium** on whether uncited `documents[]` path coverage deserves a future doc-only issue (not filed: render-time path map is explicit in README). Would change mind if product contract required `validate-structured-store` to imply render readiness without a path map.
