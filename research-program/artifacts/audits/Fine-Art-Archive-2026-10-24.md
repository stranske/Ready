Scorecard: 5 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 9; closed-still-broken 0.

Issues filed: 1 — https://github.com/stranske/Fine-Art-Archive/issues/842.

## Run report — Track D refill, current tip `020e03cefb265a53201f569a4952105b069a2c3e`

The strongest objection to calling this round healthy is the remaining coverage debt: nine previously enumerated API/UI surfaces still lack seeded, runtime substance evidence. No new route was added since the earlier same-day scorecard, so the inventory remains 49 OpenAPI paths and the unscored count remains 9. That debt was not reduced; this is not a claim of exhaustive product coverage.

The five product-contract core functions retain their prior same-day WORKS result. The only current-tip changes touch prior audit findings: #839 excludes XMP sidecars from e-ink master lookup, #840 enforces the documented positive-year merge boundary, and #841 aligns the weekly-review legacy works-root fallback. Current targeted runtime gates passed with `/opt/anaconda3/bin/python3 --no-cov`: 11 tests covering `merge_works`, XMP-only e-ink lookup, and `FAA_STAGING_DIR` fallback. The broader 184-test companion/e-ink/weekly-review run emitted passing progress through its captured output but did not return a terminal summary before the command window ended, so it is not counted as a completed test result. GitHub’s recent scheduled workflow runs were successful; local test evidence remains supporting, not CI authority.

## Verified finding and delivery

Filed [#842](https://github.com/stranske/Fine-Art-Archive/issues/842), `[P2] merge_works treats astronomical year 0 as missing during deduplication`.

Evidence is in the target repository, not the audit workspace: `src/fine_art_archive/known_works/fetchers.py:317-318` fills an existing year using truthiness, and `src/fine_art_archive/known_works/fetchers.py:338` applies its ±2 proximity guard only when both years are truthy. On the current tip, `(0, 3)` returns one merged row, year 3, despite exceeding the documented window; `(0, 1)` returns one row at year 1. By contrast, `(1, 4)` correctly returns two rows. The issue specifies explicit `None` checks, a named runtime gate, and deliberate-break/revert evidence.

Dedup was performed against all open and recent closed merge findings. Closed #737’s own sorting reproduction now passes, as does #837’s positive-year `(1880, 1883)` boundary reproduction; #842 is a distinct, still-live year-zero merge defect. Closed #836 and #838’s named acceptance tests also pass. No REFUTED line applies: no open claim was disproved and no closed issue was dropped as a duplicate without a distinct live finding.

The issue has repo-native labels `bug`, `enhancement`, `priority:normal`, `testing`, and `agents:format`. Its GitHub format-guard run completed successfully: https://github.com/stranske/Fine-Art-Archive/actions/runs/40132113918. The required measurement intake entry was appended using the issue-body path and URL. No repository source files were modified.

Confidence: high in #842’s reproduction and format-guard result; medium in retaining the 5-WORKS headline because the current tip differs only in bounded fixes and the full local suite did not yield a terminal result; low that the nine unscored surfaces are harmless until they are run with realistic seeded data.
