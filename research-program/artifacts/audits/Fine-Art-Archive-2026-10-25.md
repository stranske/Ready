Scorecard: 5 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 9; closed-still-broken 0.

# Fine-Art-Archive audit — 2026-10-25

Base: `main` at `987282313d26b3b84119f808e7a1f42426cbeb82` (`fix: preserve year zero during known-work deduplication (#843)`). Scope was repository-owned application code only. Excluded sync-managed `.github/`, `node_modules/`, `langchain/`, `runner_lib/`, and CI/tool scripts identified by the repository distinctives.

## Scorecard and evidence

| Core function | Result | Runtime evidence | Input/output variation |
| --- | --- | --- | --- |
| C1 manifest and browse | WORKS | `tests/test_build_manifest.py` exercises generated manifest rows and API-facing archive fixtures. | Valid/invalid sidecars and distinct work IDs alter manifest membership. |
| C2 e-ink selected-work preview | WORKS | `tests/test_eink_monochrome_delivery.py`, `tests/test_eink_export_format.py`; implementation entrypoints `src/fine_art_archive/api/main.py:785-849`. | Masters, targets, and dither choices produce distinct render paths/palette outputs. |
| C3 playlist and feed | WORKS | `tests/test_eink_pipeline.py`, `tests/test_eink_feed_endpoints.py`; saved playlist/feed handlers at `src/fine_art_archive/api/main.py:2230-2353`. | Filter/target/dither and cursor inputs alter selected work/feed response. |
| C4 weekly review | WORKS | `tests/test_weekly_review_thumb_paths.py` drives builder and renderer with isolated workspace inputs; builder entrypoint `scripts/build_weekly_review.py:438-491`. | Workspace/path overrides and review dates alter generated JSON/HTML. |
| C5 companion health, works and selection | WORKS | `tests/test_companion_app_api.py`; routes begin at `src/fine_art_archive/api/main.py:285-406`. | Synthetic archive contents and ratings alter response content. |

`/opt/anaconda3/bin/python3 -m pytest --collect-only -q` collected 2,524 tests. A selected 89-test weekly-review/companion run passed all tests, then returned nonzero only because the repository's global 25% coverage floor measures that intentionally narrow slice at 16.41%. A broader 395-test focused command progressed through manifest and e-ink tests before the execution time bound; it has not been represented as a completed green suite.

The primary synthetic journey — stage sidecars, build manifest, browse, render e-ink, create/feed playlist, and generate review output — has maintained focused runtime tests. This does not prove the owner archive, cloud sources, or physical e-ink hardware; none was accessed.

## Surface inventory and audit judgment

Nine surface groups remain outside the current five-row product contract: dossier/research requests, queues, acquisition review, review gates/decisions, tag proposals, DeepZoom, ratings, variant upgrades, and delivery/export administration. The 2026-10-24 scorecard also reported nine unscored surfaces. This round did not reduce that debt, so the product cannot honestly be described as comprehensively covered.

Open work already owns the reviewable e-ink divergence and coverage topics: #805, #816, #826, #827, #799, and #810. I found no independently verified, non-duplicate defect in repository-owned scope that met the required issue body and reproduction standard. Issues filed: 0.

## Reconciliation and limitations

- No candidate was suppressed based on a closed issue, so there is no `REFUTED:` line.
- No changes were made to the repository.
- The required canonical continuity locations (`Code/Audits/AUDIT_LEDGER.md`, `Code/Audits/Fine-Art-Archive/`, and `~/.codex/orchestrator/measurement/intake-2026-09-04.log`) are outside this unit's allowed write roots. An authorized program writer should record this exact scorecard line, this report path, and zero filed URLs; no intake line is due.
- Confidence: high for the stated scope and test/inventory evidence; medium for C1–C5 production equivalence because exercises use isolated synthetic data; low/unknown for the nine unscored surfaces and physical hardware/cloud integrations.
