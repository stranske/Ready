# D4 Implementation Verification — Cursor Review

**Unit:** `D4-verify-merged-2026-09-15T02`  
**Scope:** Workflows #3425, #3437, #3432, #3436, #3439, #3424, #3440 (first seven selected PRs)  
**Method:** Squash diffs from cached `diff.patch`; issue bodies from cached `issue-*.json`; merge-commit checks from `pr.json` / `merge-checks.json`. Read-only — no GitHub mutations.

## Summary

| Repo | PR | Issue | Merge SHA | Verdict | Follow-up needed |
|------|-----|-------|-----------|---------|------------------|
| Workflows | 3425 | — | `f4d3dea` | VERIFIED | no |
| Workflows | 3437 | — | `35bdde2` | VERIFIED | no |
| Workflows | 3432 | #3431 | `5740e81` | VERIFIED | no |
| Workflows | 3436 | #3433 | `f65449d` | PARTIAL | yes |
| Workflows | 3439 | #3438 | `2b2bfd6` | PARTIAL | yes |
| Workflows | 3424 | #3389 | `3ecbe0e` | PARTIAL | yes |
| Workflows | 3440 | — | `a5908e2` | VERIFIED | no |

**Strongest finding:** #3436 closed #3433 on paper but left a latched-gate refusal after retry exhaustion and omitted the issue-named test gate. Owner reopened #3433; #3440 corrects the latch. Treat green merge gates as necessary, not sufficient, for #3433-class issues.

---

## Workflows #3425 — config revert after travel window

**Verdict: VERIFIED** (no linked issue; revert of #3351)

Squash diff is a single-file config change:

```9:13:config/repo_review_feedback.json
+    "omitted_repo_decision": "defer",
     "approved_candidates": "all",
-    "window_note": "2026-09-04..2026-09-14: owner travelling; ..."
+    "history_note": "2026-09-04..2026-09-14 the default was 'approve' (owner travelling; Workflows #3351). Reverted to 'defer' on 2026-09-13 ..."
```

- **MET:** `defaults.omitted_repo_decision` restored to `defer` with auditable `history_note`.
- **Gate:** merge-commit `Gate / gate` and `summary` both SUCCESS ([run 34781762966](https://github.com/stranske/Workflows/actions/runs/34781762966)).
- **Owner note:** Copilot flagged a minor history_note date-boundary wording concern ([PR comment](https://github.com/stranske/Workflows/pull/3425)); does not block the revert itself.

---

## Workflows #3437 — tracked-variable contract link fix

**Verdict: VERIFIED** (no linked issue; follows #3354 absolute-URL pattern)

```10:10:docs/contracts/tracked-variable-v1.md
+> Program context: [`research-backplane-contract.md`](https://github.com/stranske/Workflows/blob/main/docs/contracts/research-backplane-contract.md) (Workflows-only; deliberately not synced to consumers).
```

- **MET:** Broken relative link replaced with absolute GitHub URL plus Workflows-only note.
- **Gate:** docs-only fast-pass; `docs guard` and `summary` SUCCESS on merge commit `35bdde2`.
- **Narrow PR:** fixes synced-doc link breakage (Collab-Admin #978); not a full issue implementation.

---

## Workflows #3432 — multi-publisher GitHub Models catalog (#3431)

**Verdict: VERIFIED**

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Accept all publishers in `parse_catalog` | MET | `tools/discover_model_catalog.py:136-140` removes `publisher == "OpenAI"` filter; keeps `id` + `capabilities` |
| Multi-publisher tests | MET | `tests/tools/test_discover_model_catalog.py:40-78` |
| CLI parses multi-publisher payloads | MET | `test_github_catalog_cli_reports_publishers_without_promoting` |
| `pytest tests/tools/test_discover_model_catalog.py` | MET | PR body: 19 passed; Gate SUCCESS |
| Deliberate-break | MET | PR body documents publisher-filter mutation → 6 failures → restore |

- **Gate:** named test module present; would fail if OpenAI-only filter restored (parametrized publisher tests).
- **Owner:** [#3431 closed](https://github.com/stranske/Workflows/issues/3431#issuecomment-5658989561) after provider PASS with full diff review.

---

## Workflows #3436 — keepalive debounce zero-output latch (#3433)

**Verdict: PARTIAL**

### What landed (substantive)

- Productivity measurement wired in keepalive workflows (head SHA compare → `--produced-work`).
- `scripts/runner_lib/core.py` retries unproductive completions up to `UNPRODUCTIVE_COMPLETION_RETRY_LIMIT = 2`.
- Non-vacuous tests in `tests/scripts/test_runner_lib.py:483-617` (not vacuous no-raise stubs).

### Gaps vs issue #3433

| Criterion | Status | Gap |
|-----------|--------|-----|
| Surface prior commits + task deltas on refusal | **NOT MET** | `drainable` strings omit commit/task counts |
| `tests/workflows/test_keepalive_dispatch_debounce.py` | **NOT MET** | File absent from squash diff |
| Run named pytest gate; retain output in PR body | **NOT MET** | PR body checkboxes still unchecked |
| Deliberate-break gate documented | **NOT MET** | No fail/pass transcript in PR body |
| Zero-output → `should_dispatch: true` | **MET** | `test_unproductive_completion_is_retried_on_the_same_head` |
| Post-exhaustion drain path | **NOT MET** | `drainable` still requires "a new head commit" — latched gate moved two runs later |

- **Owner blocker:** [#3433 reopened](https://github.com/stranske/Workflows/issues/3433#issuecomment-5659019906) after #3436 merge.
- **Gate vs issue gate:** merge-commit Gate SUCCESS ≠ issue-named gate present.
- **Follow-up:** #3440 (reviewed below) addresses the exhaustion latch; parent should judge combined #3436+#3440 against #3433.

---

## Workflows #3439 — codex Linux sandbox repair (#3438)

**Verdict: PARTIAL**

### Code/tasks (VERIFIED in diff)

| Task | Status | Evidence |
|------|--------|----------|
| sysctl repair (workspace-write scoped) | MET | `.github/workflows/reusable-codex-run.yml:33-42` |
| network-access fallback (bounded) | MET | `.github/workflows/reusable-codex-run.yml:66-77` |
| Force failure on bwrap stderr | MET | `.github/workflows/reusable-codex-run.yml:82-88` |
| Workflow-derived tests | MET | `tests/workflows/test_codex_sandbox_startup_failure.py` (anchored regex, prose false-positive guard) |

### Acceptance criteria

| AC | Status | Notes |
|----|--------|-------|
| Sandbox failure reports failure, not success | **MET** | Code + `test_a_failed_sandbox_cannot_report_success` |
| Consumer keepalive run produces commit | **NOT MET (in diff)** | Runtime claim only — owner cites Ready #569 commits in [#3438 comment](https://github.com/stranske/Workflows/issues/3438#issuecomment-5659457903); not independently reproduced here |

- **Gate:** merge-commit Gate SUCCESS; Keepalive E2E SUCCESS.
- **Confidence:** high on workflow mechanism; medium on consumer-runtime AC without independent rerun.

---

## Workflows #3424 — issue_format CLI coverage (#3389)

**Verdict: PARTIAL**

```19:64:tests/scripts/test_issue_format.py
def test_cli_checks_addressability_in_working_directory(...):
    """The CLI must reject well-formed issues whose evidence is in another repo."""
    ...
    assert result == (0 if has_local_evidence else 1)
```

| Criterion | Status | Notes |
|-----------|--------|-------|
| Add regression test for uncovered branch | **MET** | Exercises `main()` file vs stdin (`issue_format.py:617-621`) and cwd addressability |
| Verify coverage increase | **NOT MET** | No `--cov` before/after in PR body |
| `pytest tests/scripts/test_issue_format.py` exit 0 | **MET** | Gate `github scripts tests` SUCCESS |
| Line coverage maintained/improved | **NOT MET** | No coverage artifact |
| Fresh-clone pytest clean | **MET** | CI checkout |

- **Issue state:** PR claims Closes #3389; cached issue JSON shows **#3389 still OPEN**.
- **Tests are non-vacuous:** assert exit codes and specific stdout for addressability failure vs advisory pass.

---

## Workflows #3440 — cooldown correction to #3436

**Verdict: VERIFIED** (follow-up; no linked issue)

Owner-identified correction: replace head-commit-only exhaustion refusal with time-based cooldown.

| Claim | Status | Evidence |
|-------|--------|----------|
| 30-minute cooldown after spent retries | MET | `scripts/runner_lib/core.py:84`, `1126-1164` |
| Cooldown drainable is time, not head commit | MET | `tests/scripts/test_runner_lib.py:228-230` |
| Unmeasurable `completed_at` fails toward motion | MET | `tests/scripts/test_runner_lib.py:263-277` |
| Documentation | MET | `docs/keepalive/GoalsAndPlumbing.md` new section |
| Deliberate-break | MET | PR body + tests in diff |

- **Gate:** PR reports 1122 passed (`test_runner_lib` + `tests/workflows`); merge `summary` SUCCESS.
- **#3433:** still OPEN in cache; this PR does not close it. Parent should adjudicate whether #3436+#3440 jointly complete #3433.

---

## Calibration

| Claim | Confidence | Would change my mind |
|-------|------------|----------------------|
| #3432 fully delivers #3431 | High | Failing deliberate-break rerun on merge commit |
| #3436 is PARTIAL for #3433 | High | Finding `test_keepalive_dispatch_debounce.py` on merge commit with PR-body deliberate-break evidence |
| #3440 fixes #3436 latch defect | High | Cooldown path reverted to head-commit-only on merge commit |
| #3439 consumer-runtime AC met | Medium | Independent consumer keepalive run log showing commit after merge SHA `2b2bfd6` |
| #3424 coverage AC met | Low | PR-body or CI artifact showing `--cov=.github/scripts/issue_format.py` increase |

**Read-only offload complete.** Structured machine output: `cursor-review.json`.
