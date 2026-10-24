Scorecard: 2 work / 5 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 1; closed-still-broken 0.

# Audit run report — stranske/learning-management-system — 2026-10-24

Tip audited: `2427791c48fdab52c0bdd585adfcdaf2fa61f609` (`main`).

## Outcome

Filed 0 new issues. The two verified current findings are already open, actionable issues, so refiling them would be duplicate noise rather than useful supply:

| Issue | Verified live evidence | Disposition |
| --- | --- | --- |
| [#784](https://github.com/stranske/learning-management-system/issues/784) | `src/lms/llm/config.py:64-97` reads the global cap but never assigns `per_mode_daily_cap_micro_usd`; a direct `load_llm_config_from_env` probe with `LLM_MODE_DAILY_CAPS_MICRO_USD={"study-coach": 1}` returned `mode_caps {}`. `src/lms/llm/api.py:203-209` consequently supplies an empty map to `DailyBudgetTracker`. | Keep open; latent runtime mis-wiring. |
| [#785](https://github.com/stranske/learning-management-system/issues/785) | `src/lms/maintenance/drafts.py:146-169` performs a non-atomic count-then-decide admission check. `src/lms/__main__.py:642-658` checks once before adding a batch, with no reservation or database constraint. | Keep open; concurrent CLI sessions can overshoot the documented cap. |

## Product coverage

The current durable scorecard is at `Code/Audits/learning-management-system/2026-10-24-SCORECARD.md`. It scores all seven contract functions: CF4 review completion and CF7 capability planning work; CF1 authoring, CF2 lesson work, CF3 feedback, CF5 mastery/progress, and CF6 calibration remain partial. The primary journey passes. The one unscored surface is the interior offline-review export CLI, not an untested core product journey.

## Verification and risks

- The latest Issue Format Guard succeeded for this same tip: https://github.com/stranske/learning-management-system/actions/runs/40134310557.
- The repository virtual environment currently has no `pytest`, so this run did not claim a local suite result. Previous durable evidence records 2,809 passing non-slow tests; that is historical CI/audit evidence, not a fresh local test verdict.
- No candidate was discarded solely because a related issue was closed. Closed #571 addressed global budget-secret parsing; it does not address #784’s per-mode-cap wiring.
- No closed issue’s asserted current defect was refuted, so there is no `REFUTED:` line.

## Reconciliation

The surface inventory and prior scorecard were re-read, both viable candidates were opened and reproduced against the live tip, and each maps to an already-open issue with repository-relative evidence and a named test gate. No additional verified, non-duplicate issue remains to file.
