Scorecard: 5 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 5; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 1 — https://github.com/stranske/Fine-Art-Archive/issues/847

## Run report — Track D refill, tip `987282313d26b3b84119f808e7a1f42426cbeb82`

The unit trigger was unchanged coverage debt (`surfaces unscored 9` since 2026-09-23 r2). This round’s mandatory job was to score those nine interior companion routes, not to re-litigate the five contract core functions. Those nine are now exercised via existing seeded pytest modules plus a TestClient probe log at `Code/Audits/Fine-Art-Archive/2026-10-25-assets/evidence/unscored-surface-probe.log`, so the headline’s unscored count drops to **0**.

Core functions C1–C5 remain **WORKS** on the same isolated-data gates as 2026-10-24: `tests/test_eink_feed_endpoints.py` (118 passed), `tests/test_weekly_review_thumb_paths.py`, and companion preview/feed tests. Closed **#842** (year-0 merge) reproduces as fixed on tip via `tests/test_known_works_fetchers.py` year-zero parametrization. No `REFUTED:` line: no open issue claim was disproved, and dedup did not drop a live finding against a closed duplicate.

## Verified finding

**[#847](https://github.com/stranske/Fine-Art-Archive/issues/847)** — `[P2] Dossier key_facts omit astronomical year 0`.

At `src/fine_art_archive/enrichment/dossier.py:207`, `if sidecar.get("year"):` skips integer year `0` while year `1` adds `Dated 1.` to `key_facts`. Varying-input check: `_sidecar_facts(..., year=0)` vs `year=1` (see scorecard evidence). Body on disk: `Code/Audits/Fine-Art-Archive/2026-10-25-issue-bodies/01-dossier-year-zero-facts.md`.

Format guard: **success** on run https://github.com/stranske/Fine-Art-Archive/actions/runs/40237033109 (`Agents Issue Format Guard`). Local `issue_format.py` reports “agent-processable with advisories” (deliberate-break line cites `dossier.py:207` shorthand only).

Intake log entry appended (`repo|body-file|url`). No changes to repository source files.

## Confidence

- **High** that coverage debt fell (nine routes have named test or probe evidence; inventory still 49 paths).
- **High** on #847 reproduction at cited lines.
- **Medium** on format-guard pass until the run completes (body follows AGENT_ISSUE_FORMAT).
- **Low** that no additional interior defects remain outside the exercised nine; this round did not re-run the full 2524-test suite to completion with coverage thresholds.
