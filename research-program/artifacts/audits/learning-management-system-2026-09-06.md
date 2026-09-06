# Audit run report — learning-management-system (2026-09-06)

**Repo:** [stranske/learning-management-system](https://github.com/stranske/learning-management-system)  
**Base SHA:** `fd0ea516100d6022029a6ed0b4659e95badb189b` (main, pulled 2026-09-06)  
**Trigger:** Track D refill — agent-ready supply at 1 open issue (#580) ≤ threshold 2

## Summary

Track D demand-driven refill audit following the completion and merge of the 2026-09-05 audit batch (#584–#591). All 8 prior filed issues from 2026-09-05 are now closed on `main`.

A comprehensive audit of the current codebase (`fd0ea51`, 30,465 LOC in `src/lms/`, 29,655 LOC in `tests/`, 1,239 tests) identified 9 new genuine defects across multi-tenant authorization boundaries, markdown importer parsing, LLM provider routing, data export security, numeric scheduling bounds, and operator UI scoping.

All 9 findings were adversarially verified with isolated reproduction scripts and FastAPI TestClient probes under `AUTH_REQUIRED=true`, validated locally against `.github/scripts/issue_format.py` (0 errors, 0 advisories), and filed on GitHub as issues [#602](https://github.com/stranske/learning-management-system/issues/602)–[#610](https://github.com/stranske/learning-management-system/issues/610).

**Filed:** 9 verified AGENT_ISSUE_FORMAT issues (#602–#610; 4×P1, 5×P2).

## Dominant Defect Classes

1. **Multi-tenant learner ownership gaps (P1)** — While earlier PRs hardened mastery, rubric, and inspect routes, four major route modules still lacked ownership enforcement:
   - `src/lms/learners/api.py:47-262` declares `_current_user: CurrentUserDep` across all handlers but never references `_current_user`, leaking foreign learning goals, reflections, progress, and knowledge profiles.
   - `src/lms/competencies/api.py:86-150` allows querying foreign learner evidence links or listing unconstrained tenant evidence.
   - `src/lms/cases/api.py:156-258` allows submitting, retrieving, and scoring transfer case work products belonging to other learners.
   - `src/lms/llm/api.py:428-560` leaks tenant feedback events on unparameterized `GET /llm/feedback-events` and allows creating foreign LLM sessions and events.
2. **Markdown importer Setext heading corruption (P2)** — `src/lms/importers/markdown.py:349-358` `_section_description` only strips lines starting with `#`, leaving Setext underline characters (`===` and `---`) prepended to `KnowledgeNode.description`.
3. **LLMClient replay provider routing discrepancy (P2)** — `src/lms/llm/client.py:207-218` `replay()` resolves providers directly via `self._resolve_provider(provider_name)` rather than calling `self.config.provider_and_model_for(mode)`, ignoring mode-configured provider prefixes (e.g. `anthropic:claude-...` routes to `fake` provider).
4. **Argon2 password hash exposure in JSONL export (P2)** — `src/lms/export_import.py:256, 384-412` `PII_FIELDS` only redacts `email`, emitting plaintext Argon2 password hashes in exported `User` JSONL records.
5. **FSRS evidence rating over-allocation on NaN/Inf scores (P2)** — `src/lms/scheduling/fsrs_adapter.py:49-133` lacks `math.isfinite()` validation in `_score()`. Evidence with `normalized_score=NaN` evaluates `False` on partial-credit checks and falls through to rating 3 (Good) or rating 4 (Easy) when `correctness=True`.
6. **Support admin dashboard cross-learner signal leaks (P2)** — `src/lms/ui/support_admin.py:44-71, 116-160` renders `_support_signals` across all learners, leaking foreign learner names and open feedback actions to any authenticated user.

## Issues Filed

| # | Title | Priority | Labels | URL |
|---|---|---|---|---|
| [#602](https://github.com/stranske/learning-management-system/issues/602) | [P1] Learner API routes lack learner ownership enforcement | P1 | `bug,priority:high,testing` | https://github.com/stranske/learning-management-system/issues/602 |
| [#603](https://github.com/stranske/learning-management-system/issues/603) | [P1] Competency evidence routes lack learner ownership enforcement | P1 | `bug,priority:high,testing` | https://github.com/stranske/learning-management-system/issues/603 |
| [#604](https://github.com/stranske/learning-management-system/issues/604) | [P1] Transfer case work product routes lack learner ownership enforcement | P1 | `bug,priority:high,testing` | https://github.com/stranske/learning-management-system/issues/604 |
| [#605](https://github.com/stranske/learning-management-system/issues/605) | [P1] LLM feedback event and session routes lack learner ownership enforcement | P1 | `bug,priority:high,testing` | https://github.com/stranske/learning-management-system/issues/605 |
| [#606](https://github.com/stranske/learning-management-system/issues/606) | [P2] Markdown importer leaks Setext heading underlines into node descriptions | P2 | `bug,priority:normal,testing` | https://github.com/stranske/learning-management-system/issues/606 |
| [#607](https://github.com/stranske/learning-management-system/issues/607) | [P2] LLMClient.replay ignores per-mode provider configuration | P2 | `bug,priority:normal,testing` | https://github.com/stranske/learning-management-system/issues/607 |
| [#608](https://github.com/stranske/learning-management-system/issues/608) | [P2] export_jsonl exports plaintext Argon2 password hashes in User records | P2 | `bug,priority:normal,testing` | https://github.com/stranske/learning-management-system/issues/608 |
| [#609](https://github.com/stranske/learning-management-system/issues/609) | [P2] FSRS adapter awards Good and Easy ratings to evidence with NaN scores | P2 | `bug,priority:normal,testing` | https://github.com/stranske/learning-management-system/issues/609 |
| [#610](https://github.com/stranske/learning-management-system/issues/610) | [P2] Support dashboard exposes cross-learner feedback and review signals | P2 | `bug,priority:normal,testing` | https://github.com/stranske/learning-management-system/issues/610 |

## Artifacts

- Run record: `Code/Audits/learning-management-system/2026-09-06-audit-run.md`
- Repo map: `Code/Audits/learning-management-system/2026-09-06-00-repo-map.md`
- Verification log: `Code/Audits/learning-management-system/2026-09-06-verification-log.md`
- Issue bodies: `Code/Audits/learning-management-system/2026-09-06-issue-bodies/01-*.md` through `09-*.md`
- Intake log entries: `~/.codex/orchestrator/measurement/intake-2026-09-04.log` (9 entries appended)
- Audit ledger: `Code/Audits/AUDIT_LEDGER.md` (updated with 2026-09-06 audit entry)

## Orientation & Verification Notes

- **Baseline suite:** 1,239 tests collected; 1,229 passed, 2 skipped, 8 deselected (0 failures, 90.33% coverage).
- **Issue linter:** Every issue body validated with `uv run python .github/scripts/issue_format.py` inside repo root. All 9 bodies passed with 0 missing sections, 0 problems, and 0 advisories (`Issue body conforms to docs/AGENT_ISSUE_FORMAT.md.`).
- **Live verification:** All 9 issues reproduce deterministically on tip `fd0ea51`. Ownership leaks confirmed via FastAPI `TestClient` with multi-user JWT authentication.

## Confidence

High confidence (99%) on defect validity, reproducer fidelity, and conformance to `AGENT_ISSUE_FORMAT`. All 9 issues are immediately actionable by automated agent lanes.
