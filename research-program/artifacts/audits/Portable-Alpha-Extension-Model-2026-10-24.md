Scorecard: 2 work / 4 partial / 0 broken / 0 fabricated / 0 not exercised of 6; journey: passes via CLI/library simulate and alpha_shares sweep on bundled configs, stops at Kaleido/Chromium PNG export failure in audit environment; surfaces unscored 0; closed-still-broken 0.

Issues filed: 1 — https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2428 (`pa run --help` stub does not delegate to `pa_core.cli` flag help).

REFUTED: https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2307 — reproduction now prints explicit PNG export failure instead of silently ignoring `--png` on the sweep path (fix merged; remaining failure is Kaleido/Chromium renderer, not silent omission).

## Run report (Track D refill 2026-10-24)

**Tip:** `bd6664d1890da78f5deba8868e5f48db2599343d`  
**Trigger:** audit-refill scorecard age >30d (2026-09-23) and open agent-ready supply ≤25% of last filed set.

### Phase 1.5 product scorecard

| Core | Result | Evidence |
|------|--------|----------|
| F1 simulate | WORKS | θ 0.2→0.8: AnnReturn 0.0381→0.0443 |
| F2 sweep | WORKS | ext cap 30→170: max terminal_AnnReturn 0.0128→0.0600 |
| F3 export | PARTIAL | Excel OK; `--png` fails with Kaleido/Chromium error, 0 PNG |
| F4–F6 dashboard | PARTIAL | Page-module pytest harness (wizard/grid/stress); no browser drive |
| Interior 1/2/7 | exercised | 16 page tests passed |

Golden tutorials: **11 passed**. pytest collect: **1929/1932**.

### Dimensions (summary)

- **D1/D3:** Core simulation and sweep output correctness confirmed with varying-input probes; no new numerical defect filed.
- **D4:** Streamlit not browser-driven; dashboard logic covered via existing page tests.
- **Dedup:** Open fleet issues (coverage epics, LLM credential audits) not re-filed. #2307 re-run → refuted silent-ignore claim.

### Filing

| Issue | Priority | Summary |
|-------|----------|---------|
| [#2428](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2428) | P2 / priority:normal | `pa run --help` and `pa validate --help` show stub argparse help (`pa_core/pa.py:126-127`) instead of delegating to `cli.main --help`. |

Local `issue_format.py`: agent-processable (advisory: future test path). Format guard workflow run `40073791470` completed success; `agents:formatted` label not yet on issue at write time.

### Artifacts

- Canonical scorecard: `Code/Audits/Portable-Alpha-Extension-Model/2026-10-24-SCORECARD.md`
- Surface inventory: `Code/Audits/Portable-Alpha-Extension-Model/2026-10-24-surface-inventory.txt`
- Checkpoint: `artifacts/audits/D-audit-Portable-Alpha-Extension-Model--2026-10-24T04-03-27Z.CHECKPOINT.md`
