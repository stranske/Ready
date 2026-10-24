Scorecard: 2 work / 5 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 1; closed-still-broken 0.

Issues filed: 2 ([#784](https://github.com/stranske/learning-management-system/issues/784), [#785](https://github.com/stranske/learning-management-system/issues/785)).

REFUTED: https://github.com/stranske/learning-management-system/issues/712 — `pytest tests/scheduling/test_attempt_to_next_review_e2e.py::test_remediation_queue_item_can_be_cleared_after_failure` passes on tip `2427791`.

REFUTED: https://github.com/stranske/learning-management-system/issues/713 — `pytest tests/feedback/test_revision_requests.py::test_revision_acceptance_enqueues_review_queue_item` passes on tip `2427791`.

## Run report

**Repo:** stranske/learning-management-system @ `2427791c48fdab52c0bdd585adfcdaf2fa61f609`  
**Trigger:** Track D refill (agent-ready supply 4 ≤ 25% of last set 2; scorecard age 32d).  
**Method:** repo-audit skill; Phase 1 bash orient; Phase 1.5 live scorecard reprobes; targeted dimension-3 wiring review; adversarial verify before filing.

### Scorecard summary

Seven contract core functions exercised. CF4 (review loop) and CF7 (capability plan) **work** with varying-input checks. CF1–CF3, CF5, CF6 remain **partial** (author friction, learn-route scoring copy, mastery confidence record-count-only, no learner calibration page). Primary journey **passes** end-to-end on tip. No broken or fabricated core functions. One interior CLI surface remains unscored (`scripts/export_offline_review_packet.py`).

### Tests

`uv run pytest -m 'not slow' --no-cov`: **2809 passed**, 6 skipped. Targeted scorecard tests for remediation drain and revision scheduling: green.

### Issues filed (verified, deduped)

| Issue | Severity | Finding |
|---|---|---|
| [#784](https://github.com/stranske/learning-management-system/issues/784) | P2 / D3 | `per_mode_daily_cap_micro_usd` never loaded from environment; per-mode budget kill-switch inert despite `DailyBudgetTracker` support |
| [#785](https://github.com/stranske/learning-management-system/issues/785) | P2 / D1 | `PENDING_DRAFT_CAP` bypassable under concurrent `lms maintenance load` (check-then-insert race) |

Dedup: open [#757](https://github.com/stranske/learning-management-system/issues/757)–[#763](https://github.com/stranske/learning-management-system/issues/763) retained; no duplicate filing. Closed #712/#713 reproduction **refuted** on tip (fixes merged).

### Format guard

Agents Issue Format Guard: #784 run `40075762153` **success**; #785 run `40075763613` **success**.

### Artifacts

- Scorecard: `Code/Audits/learning-management-system/2026-10-24-SCORECARD.md`
- Issue bodies: `Code/Audits/learning-management-system/2026-10-24-issue-bodies/`
- Checkpoint: `artifacts/audits/D-audit-learning-management-system--2026-10-24T04-03-30Z.CHECKPOINT.md`
