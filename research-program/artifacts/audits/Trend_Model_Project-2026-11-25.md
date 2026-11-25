Scorecard: 4 work / 0 partial / 0 broken / 0 fabricated / 0 not exercised of 4; journey: passes; surfaces unscored 0; closed-still-broken 0.

Issues filed: 0

## Run report (Track D refill — 2026-11-25)

**Tip:** `9b7a7d4` on `main`. **Trigger:** agent-ready open issues ≤25% of last filed set; prior scorecard 2026-10-25 was >30 days old.

### Phase 1 — orient
- ~7120 tests collected (`uv run pytest --collect-only`).
- CI: recent `Agents PR Health` / `Agents Issue Intake` success on 2026-11-25.
- Open formatted agent issues: 0 (only housekeeping #5558, #5192).

### Phase 1.5 — product scorecard
Exercised C1–C4 on isolated audit outputs under the unit scratch dir. Varying-input check: `vol_adjust.enabled` moves User Weight OS CAGR 1.49% → 2.61%. Regime export and lookback wiring tests pass. Surface inventory unchanged vs 2026-10-25.

### Phases 2–4 — analysis and filing
- Re-verified October Track D issues #6127–#6129 and the 2026-11-16 design-review batch (#6228–#6230, #6246): all delivered on tip with named tests.
- Dimension-3 scan: no new config→consumer gap rose above the repo’s explicit inert-key allowlist (`tests/config/test_no_inert_keys.py` pass).
- **No AGENT_ISSUE_FORMAT issues filed** — queue refill requires new verified defects; none found after dedup.

### Artifacts
- Scorecard: `Code/Audits/Trend_Model_Project/2026-11-25-SCORECARD.md`
- Verification log: `Code/Audits/Trend_Model_Project/2026-11-25-verification-log.md`
- Evidence: unitdir `scorecard-assets/` (CLI/report/stress outputs)

### Follow-up
- Backplane conformance remains opt-in skip until `scripts/emit_reference_run.sh` and `config/backplane_participants.json` exist (documented, not a new regression).
- Next refill should re-score any new CLI/API surfaces added after this inventory diff.