# Audit run report — learning-management-system (2026-09-05)

**Repo:** [stranske/learning-management-system](https://github.com/stranske/learning-management-system)  
**Base SHA:** `b0df3a1` (main, pulled 2026-09-05)  
**Trigger:** Track D refill — agent-ready supply at 2/6 (≤25% threshold)

## Summary

Follow-up audit after the 2026-09-04 intake wave. Six of six prior filed issues (#570–#575) are now closed on main; only #575 (CLI LLM policy) remains open. This run found **residual deployed-mode authorization gaps** left after PR #578, plus numeric-trust-boundary and rubric-atomicity defects.

**Filed:** 8 verified AGENT_ISSUE_FORMAT issues (#584–#591).

## Dominant defect classes

1. **Partial ownership sweep (P1)** — attempts/evidence/feedback/scheduling were fixed in #574/#578, but mastery, inspect, rubric-score, and capability routes still accept arbitrary learner ids when `AUTH_REQUIRED=true`.
2. **Non-finite score propagation (P2)** — `record_score` and calibration analytics accept NaN `normalized_score` values; mastery output can become NaN.
3. **Last-mile loop atomicity (P2)** — rubric scoring still logs-and-continues when `schedule_for_evidence` fails; test suite pins silent success.
4. **Deploy surface exposure (P2)** — `/docs`, `/redoc`, and `/openapi.json` stay public even when auth is required.

## Issues filed

| # | Title | Priority |
|---|---|---|
| [#584](https://github.com/stranske/learning-management-system/issues/584) | Mastery estimates route lacks learner ownership enforcement | P1 |
| [#585](https://github.com/stranske/learning-management-system/issues/585) | Inspect learner routes expose foreign learner evidence and calibration | P1 |
| [#586](https://github.com/stranske/learning-management-system/issues/586) | Rubric score routes lack learner ownership enforcement | P1 |
| [#587](https://github.com/stranske/learning-management-system/issues/587) | Capability routes lack learner ownership enforcement | P1 |
| [#588](https://github.com/stranske/learning-management-system/issues/588) | record_score propagates NaN normalized scores into mastery estimates | P2 |
| [#589](https://github.com/stranske/learning-management-system/issues/589) | Calibration analytics treat NaN normalized_score as measurable accuracy | P2 |
| [#590](https://github.com/stranske/learning-management-system/issues/590) | Rubric scoring commits when schedule_for_evidence fails | P2 |
| [#591](https://github.com/stranske/learning-management-system/issues/591) | OpenAPI docs and schema remain public when AUTH_REQUIRED=true | P2 |

## Artifacts

- Run record: `Code/Audits/learning-management-system/2026-09-05-audit-run.md`
- Verification log: `Code/Audits/learning-management-system/2026-09-05-verification-log.md`
- Issue bodies: `Code/Audits/learning-management-system/2026-09-05-issue-bodies/`

## Orientation notes

- Tests collected: 1141 (8 deselected slow); CI recent runs green.
- Prior Sept-04 findings on rubric remediation wiring, Render budget env, and Postgres migration gate are **fixed on main** — not refiled.
- Open #575 retained as the CLI LLM policy gap; not duplicated.

## Confidence

High on filed items — each was adversarially re-read on tip `b0df3a1` with live repro where feasible. Format-guard workflow verdict should be rechecked on the issue threads after the guard runs complete.
