# D3 unblock sweep — 2026-09-25T05 (attempt 2 complete)

**Coverage:** all fourteen fleet repos in `SUPPORTED_REPOS` except `stranske/Orchestrator`. Attempt 1: Workflows → Pension-Data. Attempt 2: Ready → Manager-Mosaic. **Deferred:** none.

| Repository | Frozen repaired | Left for owner / left alone | Stalled PR reroutes | Default-branch state | Agent-ready supply |
|---|---:|---|---:|---|---:|
| Workflows | 6 (#3449, #3549, #3556–#3558, #3579) | [#3123](https://github.com/stranske/Workflows/issues/3123) — LangSmith degraded; owner/cloud verification | 0 | green (sampled Gate/CI) | 42 (26 `priority:*`) |
| Travel-Plan-Permission | 26 (#1598–#1622, #1627) | — | 0 | green | 34 (9 `priority:*`) |
| Trend_Model_Project | 0 | — | 0 | green | 5 (5 `priority:*`) |
| Portable-Alpha-Extension-Model | 0 | — | 0 | latest sampled run skipped | 5 (5 `priority:*`) |
| Counter_Risk | 0 | — | 0 | green | 7 (7 `priority:*`) |
| Manager-Database | 0 | — | 0 | green | 3 (3 `priority:*`) |
| Inv-Man-Intake | 1 ([#985](https://github.com/stranske/Inv-Man-Intake/issues/985)) | — | 0 | green | 2 (2 `priority:*`) |
| Pension-Data | 4 ([#919](https://github.com/stranske/Pension-Data/issues/919)–#922) | — | 0 | green | 6 (6 `priority:*`) |
| Ready | 0 | — | 0 | green / Cross-Repo Smoke skipped | 3 (3 `priority:*`) |
| trip-planner | 4 ([#1837](https://github.com/stranske/trip-planner/issues/1837), #1838, #1842, #1844) | — | 0 | green | 8 (8 `priority:*`) |
| learning-management-system | 1 ([#718](https://github.com/stranske/learning-management-system/issues/718)) | [#723](https://github.com/stranske/learning-management-system/issues/723) — `needs-human`; verify:compare disposition after merged PR #724 | 0 | green | 4 (4 `priority:*`) |
| Fine-Art-Archive | 1 ([#735](https://github.com/stranske/Fine-Art-Archive/issues/735)) | — | 0 | green | 4 (4 `priority:*`) |
| Doc-Lineage | 0 | [#1](https://github.com/stranske/Doc-Lineage/issues/1) Renovate dependency dashboard (bot tracker; not reformatted) | 0 | green | 5 (4 `priority:*`) |
| Deliverable-Render | 0 | [#1](https://github.com/stranske/Deliverable-Render/issues/1) Renovate dependency dashboard (bot tracker; not reformatted) | 0 | green | 6 (5 `priority:*`) |
| Manager-Mosaic | 0 | — | 0 | green | 14 (3 `priority:*`) |

**Attempt 2 actions:** Rewrote paused issue bodies to pass each repo’s `.github/scripts/issue_format.py` (concrete file paths per task; `pytest` / `npm test` / `gh` gates in acceptance criteria). Removed `agents:auto-pilot-pause` on repaired issues only. No `gh pr create` (offload).

**Silent claims:** none released (no stale `status:in-progress` / `agent:*` without PR >12h in pass 2 repos).

**Red main:** no sampled failing Gate/CI on `main` requiring a mechanical PR in this offload.

**Priority gaps:** Workflows 26/42, Travel-Plan-Permission 9/34, Doc-Lineage 4/6, Deliverable-Render 5/7, Manager-Mosaic 3/15 open issues carry `priority:*`.

REFUTED: https://github.com/stranske/Workflows/issues/3449 — upstream debounce/embedding fixes landed via merged PR #3577; issue body is fully checked off.

REFUTED: https://github.com/stranske/trip-planner/issues/1844 — merged PR #1862 delivers the Seattle-first / de-jargon workspace gate on current `main`; audit record only unless regression reproduces on tip.

**Genuinely needs the owner**

- Workflows #3123 — confirm LangSmith sentinel / cloud access for degraded observability.
- learning-management-system #723 — post-merge verify:compare PASS for PR #724 before closing the reopened source issue (owner comment 2026-09-25).

**Offload:** GitHub API via `detached-net.sh`; mutations issue bodies/labels only.

**Confidence:** High on pass-2 counts and repairs (live API + local `issue_format.py`). **Objection:** Renovate dashboards still carry `agents:auto-pilot-pause` while the brief says to leave bot trackers alone — that label is misleading capacity state, not opener-ready work; clearing it without owner consent may re-trigger the optimizer on junk bodies. **Uncertainty:** trip-planner #1842 cites a not-yet-created `tests/integration/test_portal_handoff.py` (advisory-only in validator).
