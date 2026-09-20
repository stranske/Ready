# learning-management-system — Track D audit refill run report (2026-09-20)

**Unit:** `D-audit-learning-management-system--2026-09-20T08-24-44Z`
**Tip:** `ecfe8de075de7989af19345b4783e00d580cb775` (2026-09-20T03:57:28Z)
**Outcome:** 8 issues filed — [#688](https://github.com/stranske/learning-management-system/issues/688)–[#695](https://github.com/stranske/learning-management-system/issues/695) (2×P1, 5×P2, 1×P2-docs)

## What this establishes

The repo's agent-ready supply was 2 (`#666`, `#580`) because the two veins that produced the last
~40 issues are genuinely exhausted, not because the repo is clean. Steering the run at the
dimensions the 2026-09-08 reconciliation had left unverified — D8 latched gates, D3 dead config,
D2 divergent duplicates — produced 8 new verified defects, including two P1s.

## Filed

| Issue | Sev | Finding |
|---|---|---|
| #688 | P1 | `DailyBudgetTracker` never rolls over a day — the "daily" LLM cap is a permanent process-lifetime kill switch (`src/lms/llm/budgets.py:33-49,76-79`; singleton at `src/lms/llm/api.py:171-201`). |
| #689 | P1 | `get_or_seed_card_state` check-then-insert races a unique index with no savepoint recovery (`src/lms/scheduling/card_state.py:49-76`); the sibling policy helper already implements the fix. |
| #690 | P2 | Misconception lookup applies `LIMIT` before its signature filter (`src/lms/feedback/repository.py:501-507`); the correct filter-then-limit shape is at `:590-597`. |
| #691 | P2 | Stale review-queue items sort to the HEAD of the daily queue; the priority clamp is structurally inert because `due_at ASC` outranks it (`src/lms/scheduling/service.py:266-278,345-353`). |
| #692 | P2 | Export `PII_FIELDS` covers only `User.email`; `username`, `display_name` and all `Learner` fields leak by default (`src/lms/export_import.py:409`). |
| #693 | P2 | Five unguarded numeric form-coercion helpers vs one hardened copy → HTTP 500 on bad input; no `ValueError` handler in `src/lms/main.py`. |
| #694 | P2 | Five latest-record/page queries lack an id tiebreaker against a ~20-site convention (incl. `src/lms/api/inspect.py:126` vs the correct `src/lms/evidence/repository.py:389`). |
| #695 | P2 | Three `config/*.json` policy files have zero `src/lms/` references; `LLM_DEFAULT_PROVIDER` is read then discarded (`src/lms/llm/config.py:89,108-111`). |

All 8 bodies passed the repo's own `scripts/verify_agent_issue_create.py` before filing, carry
repo-relative paths only, and have a deliberate-break→revert test gate. Priority labels applied so
the opener can order them.

## Latched-gate sweep (CLAUDE.md mandatory)

- `DailyBudgetTracker` — **fails all four questions**; filed as #688, and the fix is required to
  report drainable headroom next to the blocking quantity.
- `PENDING_DRAFT_CAP` — **passes**; the TTL drain is evaluated at read time so it runs while closed.
- Review-queue `stale` — passes as a gate (completion is a real drain); the defect is ordering (#691).

## Refuted on verification (not filed)

`UTCDateTime` tz divergence (INSUFFICIENT_EVIDENCE — comparisons are SQL-side); export model registry
(48/48, closed); `LLM_DAILY_BUDGET_USD` (fixed); interaction-policy matching (correctly lowercased);
draft-cap concurrent bypass (real, CLI-only, deferred); seven `_read_form` copies (duplication without
divergence).

## Process finding worth carrying forward

`gh` was authenticated on the host for this entire run. The three preceding D-audit units
(Deliverable-Render ×3 attempts, Trend_Model_Project ×3 attempts) each concluded "`gh` is
unauthenticated" and filed nothing — that was the **offload sandbox's** environment, not the host's.
Those units' zero-filed outcomes should be re-examined: their findings may be stageable from the lead
seat. A future unit should run `gh auth status` in the lead seat before treating filing as blocked.

Secondary: the Codex offload wrote a `uv.lock` into the read-only clone (removed; clone verified
clean), and the host carried ~124 leaked processes from the `issue-completion-audit` skill at load 5.7.

## Out-of-unit: the 5-day mirror outage is diagnosed (no fix applied)

The owner asked twice (2026-09-16, 2026-09-18) why `research-program/` had stopped mirroring to
stranske/Ready. It is not git and not auth — `git pull`, `git push --dry-run` and `gh` all succeed.

`mirror_push` runs `tools/publication/prepare_publication.py` with `check=True` before `git push`,
and that redactor aborts the entire publication if any `.json`/`.jsonl` file in the staging copy
fails `json.loads`. Twenty files do, from three causes: sixteen `*.checks.json` sweep artifacts are
CONCATENATED `gh api` pages (3 JSON documents in one file); `D3-parsed.json` / `D3-raw.jsonl` have
shell log text prepended (`done 15`); and three `*-dispatch.json` files are plain prose agent output
that was never added to the script's existing `TEXT_CAPTURE_JSON` allowlist.

It is a latched gate: one malformed artifact blocks every future mirror, nothing drains it, new units
keep adding artifacts, and it fails toward silence — the checkpoint records only a generic
`CalledProcessError` and never names the file. Full detail and a four-step recommended fix are in
`artifacts/audits/CHECKPOINT.md` under the 2026-09-20T11:30Z entry.

No fix was applied: the failing component is a publication safety redactor, and loosening its abort
behaviour unattended is not an appropriate call for a scheduled run. Consequence for THIS unit: the
8 filed issues are live on GitHub and the durable Dropbox records are written, but this OUT report
will not appear in stranske/Ready until the mirror is unblocked.
