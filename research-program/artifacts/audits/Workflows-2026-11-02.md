Scorecard: 5 work / 0 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

# Workflows Track D refill — 2026-11-02

Unit: `D-audit-Workflows--2026-11-02T10-02-41Z`. Trigger: agent-ready supply ≤25% of last filed set; scorecard age 31d (>30).

## Tip and delta

- Tip: `c4633a95058d927c309dc7d666ff1d8dc85c2cc3` (`Retire GitHub Models as a fallback provider`, #4362).
- **1 commit** since 2026-10-02 scorecard (`61345dd`).

## Scorecard (C1–C7)

| ID | Result | Probe |
|---|---|---|
| C1 sync manifest | WORKS | `pytest -k "manifest or sync_manifest"` → 455 passed, 1 skipped |
| C2 run-contract validator | WORKS | `pytest -k contract` → 1193 passed |
| C3 capability bundle | WORKS | `node --test capability-bundle-contract.test.js` |
| C4 metrics dashboard | WORKS | `pytest tests/e2e/test_metrics_dashboard.py` → 2 passed |
| C5 belt rate-limit proxy | WORKS | `node --test github-rate-limited-wrapper.test.js github-api-with-retry.test.js` |
| C6 consumer sync delivery | NOT-EXERCISED | production mutation withheld (policy) |
| C7 Gate on consumer PR | NOT-EXERCISED | production mutation withheld (policy) |

Primary journey (fleet maintainer runs local `dev_check.sh` / manifest compile / validator smoke): **passes** on this tip.

## Regression checks

- **Belt ledger audit** (`scripts/audit_belt_ledger_completion.py --root .`): exit **0**; 170 squash-unreachable commits **skipped** (fix from #3697/#3696). Confirms closed issue #3696 fix holds — not re-filed.
- **Backplane registry** (`scripts/validate_backplane_registry.py config/backplane_participants.json`): **5 blocking** `issue_deferred.expires_at` past 2026-10-22. Pre-existing main CI failure already tracked by **#4386** (sync-core handoff); dedup — no second issue filed.

## Issues filed (1)

- **#4387** — `[P1] Maint 39 LLM provider smoke workflow still forces retired github-models — default dispatch fails` (`priority:high`). Maint 39 still offers `github-models` and runs `get_llm_provider(force_provider='github-models')`, which raises on tip after #4362 removed the slot model. Body: `Workflows-2026-11-02-assets/issue-maint39-github-models-retired.md`. Format guard run `41431683400` **success**; `agents:formatted` label not yet on issue ~1m post-file (re-check in fleet intake).

## Dedup / REFUTED

- No REFUTED lines (no closed-issue dedup drops where reproduction still held).
- Backplane expiry: open **#4386** covers the same CI symptom without AGENT_ISSUE_FORMAT tasks — left for sync-core / owner path.

## Surface inventory

No new surfaces in `61345dd..c4633a95`; unscored K=0. Inventory note: `unitdirs/.../2026-11-02-surface-inventory.txt`.

## Artifacts

- `Code/Audits/Workflows/2026-11-02-SCORECARD.md`
- `Code/Audits/AUDIT_LEDGER.md` (2026-11-02 Workflows entry)
- `Code/Audits/Workflows/README.md` (latest pointer)
- `artifacts/audits/Workflows-2026-11-02-assets/`
- Intake log append: `stranske/Workflows|...|https://github.com/stranske/Workflows/issues/4387`

## Verdict

Core automation surfaces remain healthy on a quiet tip. One new operator-facing defect: Maint 39 contradicts the GitHub Models retirement. Registry deferral expiry is operational debt with an open tracker (#4386), not a duplicate filing target this round.
