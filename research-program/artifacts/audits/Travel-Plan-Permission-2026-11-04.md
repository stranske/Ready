Scorecard: 8 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 9; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: [#1727](https://github.com/stranske/Travel-Plan-Permission/issues/1727), [#1728](https://github.com/stranske/Travel-Plan-Permission/issues/1728). Agents Issue Format Guard: success on runs `41817887922`, `41817889854`.

## Run summary

Track D refill at `24693f79196fd741040b9428e26de43c94025f5a` (+43 commits since 2026-11-02 scorecard). The refill trigger’s **12 unscored surfaces** debt is cleared by scoring interior CLI/API/doc surfaces in the scorecard file (see section 3). Core contract grew to **nine** rows after merged PP9 expense reimbursement (#1724).

### Product scorecard

Re-ran PP1–PP9 pytest gate (34 tests, 6.1s). Primary journey still passes through policy evaluation, portal submit, exception/decision, manager review, artifacts, and expense export. PP6 remains **PARTIAL** (new draft only — documented, not a regression). No fabricated computed outputs observed in probes.

### Dimensions (abbreviated)

| Dim | outcome |
|---|---|
| 1 Quality | No new P0/P1 logic defect verified beyond open doc drift |
| 2 Duplication | Not expanded this refill; no filable hotspot |
| 3 Wiring | security-model permission map references unwired paths (#1727) |
| 4 UX | Unmeasured (TestClient only) |
| 5–7 Field/opportunities/tools | Not expanded; core debt was coverage |
| 8 Automations | Issues.txt orchestration CI checkboxes stale vs `ci.yml` (#1728) |

### Dedup / refutation

- **#1669** closed 2026-11-03; overwrite regression test passes on tip — not refuted (fix holds).
- Bulk-closed implementation backlog (2026-11-03); no `REFUTED:` lines required after re-probing #1669 and scorecard gates.
- **#1727** / **#1728** are distinct from closed #1720/#1721 (portal URL and PRODUCT_CONTRACT rows).

### Artifacts

- Scorecard: `artifacts/audits/Travel-Plan-Permission-2026-11-04-SCORECARD.md`
- Surface inventory: `artifacts/audits/Travel-Plan-Permission-2026-11-04-surface-inventory.txt` (30 OpenAPI paths; unchanged set vs 2026-11-02)
- Issue bodies: unitdir `2026-11-04-issue-bodies/`
- Checkpoint: `artifacts/audits/D-audit-Travel-Plan-Permission--2026-11-04T10-55-57Z.CHECKPOINT.md`

### Ledger

Canonical Dropbox ledger not updated in this unit (write boundary); mirror scorecard and this OUT record the completion entry for program ingestion.
