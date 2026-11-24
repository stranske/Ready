Scorecard: 3 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 3; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed this round: 0.

## Run report — Track D refill — 2026-11-24

**Tip:** `29aaa8a9f6dee84f29622c03b699ab7c9684974c` (main). **Trigger:** scorecard age >30d and agent-ready supply ≤25% (`audit-refill.md`: 0 open formatted issues, last round filed 0).

### Phase 0–1 orientation
- `pytest --collect-only`: 2621 tests; full `pytest -q` on audit interpreter: 2569 passed, 51 skipped, **1 failed** (`tests/staging/test_doc_lineage_import.py::test_non_editable_wheel_loads_packaged_schemas` — local `pip wheel` subprocess; **CI `ci.yml` on tip green**, 2026-11-23).
- Tip delta since 2026-10-24 scorecard: single commit `29aaa8a chore: sync workflow templates` (no application-code delta).
- Open issues: only durable trackers #542, #343; **no open `priority:*` implementation issues**.

### Phase 1.5 product scorecard
Core functions from `docs/PRODUCT_CONTRACT.md` (F1–F3). Evidence: `Pension-Data-2026-11-24-scorecard-evidence.txt`.

| id | score | varying-input |
|---|---|---|
| F1 | WORKS | SYN 0.784 vs CA-PERS 0.768 `funded_ratio` in pilot staging/workspace artifacts |
| F2 | WORKS | `test_metric_history_serves_two_plans_under_one_artifact_root` + artifact-backed API path |
| F3 | WORKS | workspace bundle tests + `data_origin: generated` on live pilot bundles |

Primary journey (PDF pilot → artifact-backed analytics → workspace bundle): **passes**. Interior OpenAPI routes (`POST /api/nl/query`, findings explain/compare) remain intentionally unwired (501/503); not contract core functions; inventory unchanged vs 2026-10-24.

### Phase 2 dimensions (abbreviated)
- **D1–D3:** No new wiring or output defect found; backplane now emits `evidence-object/v1` files via `build_evidence_objects` (`src/pension_data/ops/backplane_emitter.py:179-199`).
- **D4:** Web/API exercised via tests; browser not driven (API/bundle parity per owner 2026-09-20 rule).
- **D5–D8:** No filable two-week gap; automations/CI quality tests green.

### Phase 3 adversarial verification
- Dedup against open issues: none to drop (empty implementation backlog).
- Closed-issue reproduction sample: #1031 workspace bundle containment — acceptance tests pass on tip; no `REFUTED` or `closed-still-broken` candidates on F1–F3.

### Filing
No candidate met prove-before-file with a non-duplicate, AGENT_ISSUE_FORMAT-ready defect on this tip. Intake log not appended (zero URLs).

### Confidence
**High** on scorecard (live F1 probes + named F2/F3 tests). **High** that zero filings is correct given tip churn and empty open backlog; **medium** that no interior P2 was missed in one sitting — recommend repo-review meta-audit or capability gap sweep if the fleet needs non-defect roadmap issues.