Scorecard: 2 work / 5 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

# Audit run report — stranske/learning-management-system — 2026-10-25

Tip audited: `e08460aadef353e4ca7ab347956dd1fbd7b07588` (`main`, PR #788).

## Issues filed

| Issue | Core function | Summary |
| --- | --- | --- |
| [#789](https://github.com/stranske/learning-management-system/issues/789) | CF5 | Mastery confidence uses record count only (`src/lms/mastery/policy.py:30`). |
| [#790](https://github.com/stranske/learning-management-system/issues/790) | CF6 | No learner HTML calibration page; JSON-only Inspect route. |
| [#791](https://github.com/stranske/learning-management-system/issues/791) | CF3 | Learn POST hardcodes feedback and pending-scoring copy (`src/lms/ui/api.py:214-256`). |

Agents Issue Format Guard: success runs `40184873681`, `40184875136`, `40184876560`.

## Coverage delta

- Cleared the 2026-10-24 **surfaces unscored 1** debt by scoring `scripts/export_offline_review_packet.py` (interior WORKS; `tests/test_local_first_delivery.py`).
- Re-verified CF4 remediation/revision seams and transfer-excluded card freeze on tip.
- Local tests: `uv run pytest -m 'not slow' --no-cov` → 2868 passed.

## Closed-issue reproduction (dedup / refutation)

REFUTED: https://github.com/stranske/learning-management-system/issues/784 — `load_llm_config_from_env` now populates `per_mode_daily_cap_micro_usd` from `LLM_MODE_DAILY_CAPS_MICRO_USD` on tip.

REFUTED: https://github.com/stranske/learning-management-system/issues/785 — `reserve_draft_capacity` serializes admission; e2e maintenance tests pass after #788.

Open repo-review issues #757, #758, #760 describe defects that appear fixed on tip (export redaction, inspect scope, transfer card freeze) but remain open on GitHub; not re-filed.

## Artifacts

- Scorecard: `Code/Audits/learning-management-system/2026-10-25-SCORECARD.md`
- Issue bodies: `Code/Audits/learning-management-system/2026-10-25-issue-bodies/`
