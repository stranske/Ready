Scorecard: 2 work / 5 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 1; closed-still-broken 0. Issues filed: 2 ([#712](https://github.com/stranske/learning-management-system/issues/712), [#713](https://github.com/stranske/learning-management-system/issues/713)).

# learning-management-system — Track D audit refill (2026-09-22)

**Unit:** `D-audit-learning-management-system--2026-09-22T20-42-45Z`  
**Tip:** `3bdd840da6dd9d658dc6f6da2d599def00b3a936`  
**Trigger:** agent-ready supply 2/4 (≤50%); prior round #688–#695 merged on tip.

## Scorecard summary

| id | core function | score | varying-input check |
|---|---|---|---|
| CF1 | author builds knowledge/goals/prompts | PARTIAL | author flow still needs source refs and hand-pasted relationship UUIDs |
| CF2 | learner works a lesson | PARTIAL | empty `prompt_id` POST returns 200 with “pending scoring” instead of blocking; scored path works via `/attempts` |
| CF3 | learner receives feedback | PARTIAL | learn-surface feedback remains generic; author/rubric paths differ |
| CF4 | learner completes review | WORKS | `tests/scheduling/test_attempt_to_next_review_e2e.py` drives attempt→queue→complete |
| CF5 | learner views mastery/progress | PARTIAL | estimates differ (1.0 vs 0.0) but confidence saturates at 1.0 for both (`src/lms/mastery/policy.py:30`) |
| CF6 | learner inspects calibration | PARTIAL | API buckets vary (`overconfident` False vs True) but no learner HTML readout |
| CF7 | learner capability plan | WORKS | capability repository/API tests green; gap severity responds to evidence |

**Primary journey:** attempt → self-grade → review queue → complete passes on tip (e2e suite).  
**Surfaces unscored (1):** `scripts/export_offline_review_packet.py` (interior local-first adjunct; smoke tests pass).  
**Closed-still-broken:** 0 — re-checked #688–#695 reproduction classes; all merged fixes hold on tip.

## Prior round verification

| Issue | Fix on tip |
|---|---|
| #688 daily budget rollover | `src/lms/llm/budgets.py:66-72` `_roll_period_locked` |
| #689 card-state race | `src/lms/scheduling/card_state.py` savepoint recovery + tests |
| #690 misconception LIMIT | `src/lms/feedback/repository.py` filter-before-limit |
| #691 stale queue ordering | `src/lms/scheduling/service.py` stale deprioritized |
| #692 export PII | `src/lms/export_import.py:411-414` expanded `PII_FIELDS` |
| #693 form coercion | `src/lms/ui/forms.py` consolidated helpers |
| #694 latest-record tiebreaker | tests in `tests/ui/test_latest_record_ordering.py` |
| #695 LLM provider override | `src/lms/llm/config.py:100-124` honors registered override |

## Filed this round

| Issue | Sev | Finding |
|---|---|---|
| [#712](https://github.com/stranske/learning-management-system/issues/712) | P1 | Remediation queue items render **Mark reviewed** (`src/lms/ui/api.py:491-500`) but `complete_review_queue_item` rejects `reason_code="remediation"` (`src/lms/scheduling/repository.py:119-122`) — latched pending backlog. |
| [#713](https://github.com/stranske/learning-management-system/issues/713) | P1 | Revision accept path stores `scheduler_hook` JSON (`src/lms/feedback/repository.py:403`) but no code consumes it; revised scored attempts create zero `ReviewQueueItem` rows. |

## Refuted / deferred (not filed)

- **LLM per-mode cap / timeout env wiring** — real D3 gap (`load_llm_config_from_env` omits `per_mode_daily_cap_micro_usd` and `default_timeout_seconds`), but lower severity than the two learning-loop P1s; defer to next refill.
- **Sustainability helpers unwired** (`mark_stale_queue_items`, pause/resume) — service functions exist with tests only; documented v1 behavior not mounted on API/UI surfaces.
- **UTCDateTime tz divergence** — still INSUFFICIENT_EVIDENCE (SQL-side comparisons only).
- **Graph-edge concurrency** — already tracked in open #666.

## Orientation

- **LOC:** ~31.7k `src/lms/`, ~36.8k `tests/`
- **Tests collected:** 2579 (8 deselected slow)
- **CI:** green on recent scheduled workflows
- **Open agent-ready before filing:** 2 (`#666`, trackers); after filing: 4 agent-ready including #712–#713

## Artifacts

- Canonical: `Code/Audits/learning-management-system/2026-09-22-SCORECARD.md`, `2026-09-22-audit-run.md`, `2026-09-22-issue-bodies/`
- Mirror: `artifacts/audits/learning-management-system-2026-09-22.md`
