Scorecard: 6 work / 1 partial / 0 broken / 0 fabricated / 1 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

**Issues filed:** [#1274](https://github.com/stranske/Counter_Risk/issues/1274) — post-banner bullets in `docs/audit/REMAINING_WORK.md` and `docs/audit/IMPLEMENTATION_SUMMARY.md` still describe resolved headless error handling (#1273) and unwired Ask-about control (#1236).

## Run summary

| Item | Value |
|------|--------|
| Unit | `D-audit-Counter_Risk--2026-11-26T04-50-05Z` |
| Tip audited | `main` @ `83a89871776c5fa7ea4977f87f338445b3331a3d` |
| Trigger | audit-refill: coverage debt 2 unchanged since 2026-10-25 |
| Coverage debt | **2 → 1** (unscored frozen bundle absorbed into scored CF7 NOT EXERCISED row) |

## Phase 1.5 — product scorecard

- **Journey:** `counter-risk run --fixture-replay --config config/fixture_replay.yml --output-dir /tmp/cr-audit-20261126` produced MOSERS XLSX trio, historical workbooks, PPTX, and `manifest.json` (`mode: fixture_replay`, `as_of_date: 2025-12-31`).
- **Varying-input probes:** `pytest tests/compute/test_concentration_metrics.py -k hhi` (5 passed); `pytest tests/test_dates.py` (55 passed); limit/fleet regressions via gate run.
- **CF2:** headless smoke `pytest tests/test_cli_coverage_round.py -k headless` passes on tip — #1272 reproduction **does not** reproduce (`cli/__init__.py:310-314` prints `error_message`). Interactive Tk still not driven on macOS → **PARTIAL**.
- **CF6:** `pytest tests/test_runner_workbook.py` in batch — static macro/Form-Control map green.
- **CF7:** NOT EXERCISED (Windows PyInstaller + RELEASE_CHECKLIST); row formally scored so `surfaces unscored 0`.

## Dimensions (abbreviated)

Eight dimensions reviewed at token budget; no additional verified code defects beyond the docs-debt item above. Maintainer plumbing (config→pipeline→manifest/fleet) matches dossier; `run.json` still absent (documented contract-only). Workspace clone `main` ref stale — exercise used fresh shallow `main`.

## Filing and verification

- Format guard: success on run `45758568402` for issue #1274.
- Canonical scorecard: `Code/Audits/Counter_Risk/2026-11-26-SCORECARD.md`
- Issue body: `Code/Audits/Counter_Risk/2026-11-26-issue-bodies/01-remaining-work-stale-bullets.md`

## Deliverables

- OUT (this file)
- Checkpoint: `artifacts/audits/D-audit-Counter_Risk--2026-11-26T04-50-05Z.CHECKPOINT.md`