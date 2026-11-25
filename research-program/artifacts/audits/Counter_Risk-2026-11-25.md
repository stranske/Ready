Scorecard: 6 work / 1 partial / 0 broken / 0 fabricated / 1 not exercised of 8; journey: passes; surfaces unscored 1; closed-still-broken 0.

UX panel: not run (macOS headless; Tk/Excel not UI-driven); gate: not measured.

**Issues filed:** 1 — [#1267](https://github.com/stranske/Counter_Risk/issues/1267) (stale `22-design-ux.md` banner still claims Ask-about unbound after #1236).

## Run summary

| Field | Value |
|---|---|
| Repo | `stranske/Counter_Risk` |
| Tip audited | `683a970af12ac7a707c46d14b341d7e2e93190cb` (`main`) |
| Workspace clone | stale branch `fix/black-langsmith-fleet-test` @ `affd8bf` (workflow-sync only; code verified via `/tmp/Counter_Risk-main-audit`) |
| Trigger | Track D refill — open agent-ready 0/1, scorecard 31d old |
| Unit | `D-audit-Counter_Risk--2026-11-25T04-28-16Z` |

## Phase 1.5 — product scorecard

| id | function | score | exercise |
|---|---|---|---|
| C1 | Maintainer monthly pipeline run | WORKS | `pytest` pipeline/limit scope tests on `main`; fixture-replay path unchanged |
| C2 | Limits + registry identity | WORKS | `tests/compute/test_limits.py` denominator scoping; fail breaches raise via `_raise_for_fail_limit_breaches` (`pipeline/run.py:690`) |
| C3 | Concentration HHI / Top-N | WORKS | `tests/compute/test_concentration_metrics.py -k hhi` — 5 passed; varying HHI fixtures |
| C4 | Reporting package + manifest quality | WORKS | manifest data-quality tests; langsmith fleet status tests (clone) |
| C5 | Source report-date conflicts (`PRODUCT_CONTRACT` row added post-2026-10-25) | WORKS | `tests/test_dates.py` + `tests/test_report_date_evidence_publication.py` — 63 passed |
| CF2 | Tk GUI operator run | PARTIAL | Code + prior tests; not driven headless on macOS |
| CF6 | `Runner.xlsm` Form Control macros | WORKS | `tests/test_runner_workbook.py` — 20 passed on `main` (nine buttons incl. D5/I5 post-#1236) |
| CF7 | Windows PyInstaller frozen bundle | NOT EXERCISED | No Windows host in this unit |

**Primary journey:** fixture-replay / synthetic pipeline tests → deliverables + manifest — **passes** on macOS CI probes.

**Surface inventory:** CLI unchanged (`counter-risk {run,gui}`, `mapping_diff_report`). **New since 2026-10-25:** `PRODUCT_CONTRACT` C5 row + `tests/test_dates.py` report-date suite (now scored). **Unscored (1):** frozen Windows bundle end-to-end.

## Dimensions (abbreviated)

1. **Code quality** — No new defects; maintainer paths strongly typed; stale in-repo audit *bodies* remain behind banners.
2. **Duplication** — No new consolidation targets surfaced this round.
3. **Wiring** — Fail-severity limit breaches halt the run on tip; concentration denominator scoping holds.
4. **Design/UX** — Historical banner exception in `22-design-ux.md` contradicts shipped Runner + contract → filed #1267.
5. **Public field** — No change vs prior round.
6. **Missed opportunities** — `run.json` / `run-contract/v1` emitter still absent (`src/` has zero `run.json` writers); backplane gate continues to skip.
7. **Tools** — N/A.
8. **Local automations** — Stale workspace `origin/main` ref (`262a811`) behind GitHub `main` (`683a970`); audits must shallow-clone or refresh refs.

## Verification / filing

| Finding | Action |
|---|---|
| `docs/audit/22-design-ux.md:3` + `tests/docs/test_audit_log_historical.py:41-43` stale #1183 exception | Filed **#1267** |
| #1188 dimension banners | **Fixed on `main`** (prior round delivered; verified `test_dimension_audit_logs_marked_historical`) |
| #1183 D5/I5 Runner wiring | **Fixed on `main`** via PR #1236 |
| `run.json` emitter | Known documented gap; no new issue (no open duplicate; epic-scale) |

**Format guard:** `Agents Issue Format Guard` run [45548240936](https://github.com/stranske/Counter_Risk/actions/runs/45548240936) — **skipped** on open; `agents:formatted` not yet on #1267 at write time (re-check after guard completes).

## Artifacts

- Canonical scorecard: `[LOCAL_HOME]/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/2026-11-25-SCORECARD.md`
- Checkpoint: `[LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/D-audit-Counter_Risk--2026-11-25T04-28-16Z.CHECKPOINT.md`