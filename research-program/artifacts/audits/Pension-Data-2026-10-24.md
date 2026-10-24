Scorecard: 3 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 3; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed this round: 0.

## Run report — Track D refill — 2026-10-24

**Tip:** `4f5d14a49482c6e914b0127946d677ae3d703776` (main). **Trigger:** scorecard age >30d (`audit-refill.md`).

### Product scorecard
The resumed checkpoint records live varying-input exercises for core functions F1–F3 from `docs/PRODUCT_CONTRACT.md`: synthetic versus CA-PERS pilot outputs, dual-plan artifact-backed analytics, and workspace-bundle construction. Its stated journey (PDF pilot → artifact-backed analytics → workspace bundle) completed without a blocking step. The detailed scorecard/evidence files are not visible from this unit's permitted paths, so this is resumed evidence rather than a newly re-opened scorecard artifact.

### Verification
- `pytest -q`: 1945 passed, 25 skipped, 3 xfailed.
- OpenAPI surface inventory unchanged (7 paths); unscored K=0.
- Adversarial dedup against open #957–#964: no duplicate filing; several open issues appear already satisfied on tip (orchestration parser validation, cash-flow rate vs dollar, revised-plan conflict isolation, disclosed flow → funding-trend net cash). Recommend implementation-verification closeout on those issues rather than re-filing.
- Resume validation on the current tip: `pytest -q --no-cov tests/api/test_artifact_data.py tests/api/test_app_serving.py tests/ops/test_document_orchestration.py tests/ingest/test_holdings_pipeline.py tests/db/test_staging_persistence.py tests/quant/test_contracts.py tests/web/test_build_workspace_bundle.py` collected and passed **220 tests**. The implementation now loads declared flow artifacts and exposes scoped trend conflicts (`src/pension_data/api/artifact_data.py:299-320,549-556`); rejects contribution-rate rows as dollar amounts (`src/pension_data/ops/document_orchestration.py:302-350`); joins holdings by `security_id` rather than issuer spelling (`src/pension_data/query/saved_views/holdings_ingest.py:24-49`); and canonicalizes evidence/timestamps for assertion comparison (`src/pension_data/db/staging_persistence.py:95-129`). These reproduce the claimed resolutions for #957–#962 and support not filing equivalents.

### Dimensions
The resumed checkpoint records the D1–D8 sweep; its separately cited detailed summary is not available in this unit's permitted paths.

### Filing
No new AGENT_ISSUE_FORMAT defects met prove-before-file on this tip beyond the existing repo-review backlog. Intake log not appended (zero URLs).

### Artifacts
| Path | Role |
|---|---|
| `artifacts/audits/Pension-Data-2026-10-24.md` | Mirror report (this file) |
| `artifacts/audits/D-audit-Pension-Data--2026-10-24T04-03-29Z.CHECKPOINT.md` | Unit checkpoint |

The resumed checkpoint records the detailed scorecard exercise and dimension sweep. This unit's filesystem boundary does not expose the separately cited `Code/Audits/Pension-Data/` directory, so those paths are not asserted here as locally re-opened artifacts.

**Confidence:** Medium on the resumed scorecard because the detailed live-probe artifacts could not be re-opened here; high that the focused current-tip regressions pass. Medium that no filable interior defect was missed in one sitting; low-churn tip (single deps PR) limits expected novelty.
