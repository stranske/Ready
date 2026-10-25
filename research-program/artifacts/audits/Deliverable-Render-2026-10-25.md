Scorecard: 7 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0.

REFUTED: https://github.com/stranske/Deliverable-Render/issues/89 — native `locator.page` / `document_ref.page` conflicts now fail validation and every public renderer before output publication.

# Deliverable-Render audit — 2026-10-25

Tip: `4cf90c0eb5cab56c78b1130c69ef1ddf17840c41` (`main`). Scope was repo-owned `src/`, `tests/`, README, and contracts. Synced `.github/`, `tools/`, model-registry configuration, and fleet-maintenance scripts were excluded except for CI and issue-format context. The requested dossier and verification table were absent.

## Verdict

The primary journey passes in an isolated installation of the audited tip: validate a communication-synthesis store, then render its HTML hub, manifest-gated PPTX, and communication-profile DOCX. No new reproducible, non-duplicate defect met the filing threshold.

The direct checkout run initially reported 352 passed / 1 failed because stale global `/opt/anaconda3/bin` console shims could not import an uninstalled checkout. That is not a product failure: a clean temporary virtual environment with this exact package installed passed all 353 tests, including the three public console commands. Current exact-head GitHub Action runs are successful.

## Product scorecard

| ID | Core function | Result | Live exercise and varying-input result |
| --- | --- | --- | --- |
| CF1 | An operator can validate a communication-synthesis store and see diagnostics. | WORKS | `validate-structured-store tests/fixtures/stores/communication_render.json` printed `structured store valid`. |
| CF2 | A developer can render a deep-linked offline HTML hub whose visible content responds to the store. | WORKS | `render-html-hub` wrote `audit-evidence/hub.html`; changing `entries[0].mentions[0].text` from `Capital of $36B` to `Capital changed to $999B` replaced the rendered text and changed the HTML. |
| CF3 | A developer can build a manifest-gated PPTX deck whose body responds to the store. | WORKS | `render-pptx-deck` wrote `audit-evidence/deck.pptx` and reported its four counts; changing the same mention changed text re-read from the generated PPTX. The fixture intentionally leaves thesis/publication records uncovered and reports that warning; `--strict` correctly blocks that incomplete manifest. |
| CF4 | An operator can render a reviewed communication-synthesis change memo. | WORKS | `render-docx-memo --profile communication-synthesis` wrote `audit-evidence/memo.docx`. |
| CF5 | An operator can generate an offline capability probe. | WORKS | `tests/test_probe_offline_and_minimal.py` passed, including the external-resource deliberate-break gate. The target work browser itself was not available, so its capability results remain a future operator observation rather than audit evidence. |
| CF6 | A valid communication-synthesis store can reach HTML, PPTX, and DOCX without a translation step. | WORKS | `tests/store/test_communication_render_profile.py::test_validated_store_renders_all_three_public_outputs` passed in the isolated installed package. |
| CF7 | Invalid memo tiers and rendering-seam input are rejected before publication. | WORKS | `tests/docx/test_validation_and_cli.py::test_validation_rejects_unknown_tier_before_render` passed; focused validator/render rejection tests passed. |

Primary journey: communication-synthesis store -> validation -> HTML hub + PPTX deck + DOCX memo. It passes.

## Closed/open issue re-check

Focused current-tip tests re-ran the former validation-to-render seams: cross-entry mention IDs, missing publication detail/state, missing entry periods, invalid pages, no-renderable-content, literal POSIX backslashes, template-slide rejection, and incomplete-deck reporting all reject or report as their contracts require. Therefore no closed issue in that core path was found still broken.

Open #89's stated conflicting-native-page reproduction is now false on this tip: `src/deliverable_render/store/validate.py:113-123,181-186` rejects contradictory anchors, and `src/deliverable_render/store/communication.py:64-84` prevents adaptation/publication. The current focused native-page tests cover both mention and publication paths. #104 remains an unrelated open CI-runtime modernization request, not an audit finding.

## Dimension coverage and disposition

| Dimension | Result |
| --- | --- |
| D1 code quality | 353 tests pass in the clean installed environment; Ruff is clean. No verified source defect retained. |
| D2 duplication | Small, purpose-separated renderer modules; no actionable duplication finding. |
| D3 wiring/output correctness | Validation -> adapter -> all three public renderers exercised. HTML and PPTX output changed for materially different text input. |
| D4 operator UX | No browser application exists. Per the required fallback, the four CLI surfaces were driven directly; the generated offline probe is covered by its runtime-focused test suite. |
| D5 approach vs field | Local-file outputs, explicit provenance, and template-free deck assembly remain aligned with the stated constrained-environment product contract; no bounded corrective issue established. |
| D6 missed opportunities | No independently evidenced, two-week-scope opportunity exceeded the existing output and probe contracts. |
| D7 tools | No tool integration is necessary to exercise or verify the present product contract. |
| D8 automations | CI is green at the exact head. The stale local global command shims were isolated from repository behavior and are not filed as a repo issue. |

## Verification

- `ruff check src tests` -> clean.
- Checkout-local suite: 352 passed / 1 environment-installation failure; clean isolated installed package: 353 passed.
- Focused core journey, input-boundary, and deliberate-break tests: 32 passed.
- `gh run list -R stranske/Deliverable-Render --limit 10` showed successful exact-head scheduled checks.
- Open and recently closed GitHub issues were deduplicated before disposition. No issue was filed, so there is no format-guard run or intake-log row for this unit.

## Storage boundary

The durable `Code/Audits` ledger and repository folder were read for continuity, but this unit's write boundary permits only the supplied audit-artifact directory; this report and its append-only checkpoint are the persisted unit record. No attempt was made to alter the protected ledger or unrelated program files.

Confidence: high that no new issue should be filed at this tip. The conclusion would change if the target work browser fails to open the generated probe or local-file deliverables, if the deployed environment cannot install the package used by the documented console commands, or if an input variation changes neither rendered text nor PPTX content.
