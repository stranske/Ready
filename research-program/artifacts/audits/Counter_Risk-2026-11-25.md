Scorecard: 6 work / 1 partial / 0 broken / 0 fabricated / 1 not exercised of 8; journey: passes; surfaces unscored 1; closed-still-broken 0.

UX panel: not run (macOS headless; Tk/Excel not UI-driven); gate: not measured.

**Issues filed:** 1 — [#1272](https://github.com/stranske/Counter_Risk/issues/1272) (headless GUI discards `execute_gui_run` operator-formatted `error_message`).

**Coverage debt:** unchanged vs 2026-10-25 — still `N=1` (frozen Windows bundle) plus `K=1` (same surface unscored); no Windows host in this unit to score CF7.

## Run summary

| Field | Value |
|---|---|
| Repo | `stranske/Counter_Risk` |
| Tip audited | `ab62a5c0f3d74e308547fac2c56ff63f7902f5a3` (`main`, shallow clone) |
| Workspace clone | `fix/black-langsmith-fleet-test` @ `affd8bf` (stale; `.git` fetch blocked — code verified via temp clone) |
| Trigger | Track D refill — open agent-ready 0/1; scorecard coverage debt 2 unchanged since 2026-10-25 |
| Unit | `D-audit-Counter_Risk--2026-11-25T16-43-03Z` |

## Phase 0 — scope

- **In scope:** `src/`, `tests/`, `docs/PRODUCT_CONTRACT.md`, operator surfaces (CLI/GUI/Runner.xlsm); exclude synced `.github/` and `node_modules/`.
- **Depth:** live pytest on Python 3.13 venv against GitHub `main`; no Windows PyInstaller exercise.
- **Deliverables:** scorecard, one verified AGENT_ISSUE_FORMAT issue, ledger + intake log.

## Phase 1 — orientation

- ~70k LOC Python across `src/` + `tests/`; **2242** tests collected on tip (`requires-python >=3.13`).
- CI on `main` green (latest `CI` push success @ `ab62a5c`, 2026-11-25).
- CLI surface unchanged: `counter-risk {run,gui}`, `mapping_diff_report`.

## Phase 1.5 — product scorecard

| id | function | score | exercise |
|---|---|---|---|
| C1 | Maintainer monthly pipeline run | WORKS | limit denominator + date/report suites on tip |
| C2 | Limits + registry identity | WORKS | `tests/compute/test_limits.py` (denominator scoping) |
| C3 | Concentration HHI / Top-N | WORKS | `tests/compute/test_concentration_metrics.py -k hhi` (5 pass) |
| C4 | Reporting package + manifest quality | WORKS | prior round + manifest/fleet tests (spot-checked) |
| C5 | Source report-date conflicts | WORKS | `tests/test_dates.py` (63 pass) |
| CF2 | Tk GUI operator run | PARTIAL | not UI-driven on macOS; **headless sub-path loses operator messages** → #1272 |
| CF6 | `Runner.xlsm` Form Control macros | WORKS | `tests/test_runner_workbook.py` (20 pass) |
| CF7 | Windows PyInstaller frozen bundle | NOT EXERCISED | no Windows host |

**Primary journey:** maintainer CLI / fixture-replay probes → deliverables + manifest — **passes** on macOS.

**Surface inventory:** unchanged vs earlier 2026-11-25 round. **Unscored (1):** frozen Windows bundle end-to-end.

## Dimensions (abbreviated)

1. **Code quality** — tip stable; Python floor now 3.13+ on `main`.
2. **Duplication** — no new targets.
3. **Wiring** — **filed #1272:** headless GUI CLI path ignores formatted `GuiRunResult.error_message` (`cli/__init__.py:309`); interactive GUI uses it.
4. **Design/UX** — #1267 delivered earlier today (closed); banners on dimension audits aligned on tip.
5. **Public field** — no change.
6. **Missed opportunities** — `run.json` / `run-contract/v1` emitter still absent in `src/`.
7. **Tools** — N/A.
8. **Local automations** — workspace clone behind GitHub `main`; audits must shallow-clone tip.

## Verification / filing

| Finding | Action |
|---|---|
| Headless GUI drops `error_message` | Filed **#1272** |
| #1267 Ask-about banner | **Closed/fixed on tip** (verified `tests/docs/test_audit_log_historical.py`) |
| `docs/audit/REMAINING_WORK.md:33` stale Ask-about bullet in body | Not filed (historical narrative; banner already warns readers) |

**Format guard:** `Agents Issue Format Guard` run [45658793944](https://github.com/stranske/Counter_Risk/actions/runs/45658793944) — **success**; `agents:formatted` not yet on #1272 at write time.

## Artifacts

- Canonical scorecard: `[LOCAL_HOME]/Library/CloudStorage/Dropbox/Learning/Code/Audits/Counter_Risk/2026-11-25-SCORECARD.md` (updated this unit)
- Issue body: `unitdirs/D-audit-Counter_Risk--2026-11-25T16-43-03Z/issue-1270-body.md`
- Checkpoint: `[LOCAL_HOME]/.codex/automations/research-program/artifacts/audits/D-audit-Counter_Risk--2026-11-25T16-43-03Z.CHECKPOINT.md`