Scorecard: 4 work / 1 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes; surfaces unscored 2; closed-still-broken 0.

Issues filed: 1 — https://github.com/stranske/Counter_Risk/issues/1112 ([P2] in-repo audit logs still list fixed BLOCKERs).

## Run report — Track D refill — 2026-09-23

**Tip:** `2f92b174303f3ef977828ed4588794fcec42e6ef` (`docs: sync LABELS.md from Workflows repository`).

### Phase 0–1 (orient)

- Shallow clone pulled; 2231 tests collected.
- CLI surfaces: `counter-risk {run,gui}`, `mapping_diff_report` (unchanged since 2026-09-21).
- Open agent-ready issues: #1106 (chat multi-mover, still valid), #1073 (coverage gate file), plus dependency/dashboard noise.

### Phase 1.5 (product scorecard)

- **CF1** fixture-replay run completed to `/tmp/cr-audit-20260923`.
- **CF3** concentration/limit regressions: 13 pipeline + 5 HHI tests passed (varying-input via distinct fixtures).
- **CF4** closed #1104/#1107 verified: `test_apply_repo_cash_syncs_notional_change_columns` PASS; no manifest mover desync on tip.
- **CF5** prior CPRS/variant fixes remain green on targeted tests.
- **CF2/CF6/CF7** not driven (GUI headless / Windows COM / PyInstaller).

### Phases 2–3 (dimensions + verification)

- Re-ran reproduction tests for merged 2026-09-21 fixes (#1104, #1105) on tip — both PASS.
- Closed-issue reproductions for #1081–#1090 and #1103 do not reproduce on tip (limits denominator, fail→RED, GUI worker thread, repo-cash deltas, etc.).
- No new reproducible core-function defect beyond documentation debt.
- **Finding filed:** `docs/audit/AUDIT_REPORT.md` and `docs/audit/REMAINING_WORK.md` still assert BLOCKERs fixed on main (evidence in issue #1112).

### Phase 4–5 (filing + ledger)

- Issue #1112 filed with `bug` + `priority:normal`.
- Canonical scorecard: `Code/Audits/Counter_Risk/2026-09-23-SCORECARD.md`.

### Dedup / refutation

- Did not re-file #1106 (open).
- No `REFUTED:` lines (closed issues #1104/#1105 claims are fixed on tip; reproduction correctly fails to show the old defect).

### Format guard

Agents Issue Format Guard: success (run 35842151407).
