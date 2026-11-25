Scorecard: 8 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 8; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0

## Run report (Track D refill, 2026-11-25)

**Trigger:** Scorecard dated 2026-10-25 (>30d); open agent-ready implementation issues ≤25% of last filed set (0 open vs prior rounds).

**Tip:** `6b8175d43f4765824b5a39ad1d499150054d705e` (`main`). One commit since `5605c75`: `chore: sync workflow templates` (no app diff).

**Phase 1 — orient:** 458 Python modules; `2762` tests collected; CI green on tip.

**Phase 1.5 — scorecard:** Re-exercised MDB-1…MDB-8 via the same ASGI/SQLite/fixture probes as 2026-10-25. OpenAPI surface inventory: 44 paths, empty diff vs prior round.

**Phases 2–3 — dimensions + adversarial verify:** No new defect reproduced at cited lines. `#1786` reproduction (`pytest tests/test_bitemporal_holdings.py -k "original_replay or reverse_order"`) passes. `scripts/emit_reference_run.sh` and `tests/test_emit_reference_run.py` pass (run-contract closed via #1849). Two local-only pytest failures traced to a leaked shell `DB_URL`, not product logic.

**Phase 4 — file:** Dedup against open issues (only `tracker:durable` #927, #1164). No AGENT_ISSUE_FORMAT issue filed.

**Deferred (not filable as defects):** `docs/PRODUCT_CONTRACT.md` status column still shows NOT-EXERCISED/PARTIAL for MDB-3/6/7/8 while live probes show WORKS — contract maintenance only.

REFUTED: https://github.com/stranske/Manager-Database/issues/1786 — bitemporal original-replay acceptance tests pass on tip `6b8175d` (issue closed; prior audit text said still-open tracked work).

**Artifacts:** `Code/Audits/Manager-Database/2026-11-25-SCORECARD.md`, `2026-11-25-audit-run.md`, `2026-11-25-surface-inventory.txt`.

**Confidence:** High for 0 new issues; would change on red CI at tip or a reproduced closed-issue claim.