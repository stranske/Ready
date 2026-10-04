## Why (verified evidence)

`scripts/audit_belt_ledger_completion.py` is the documented tool for finding historical belt-task
completions recorded `done` without real evidence (`docs/ci/LEDGER.md:35-40`: "Use the read-only
historical audit to find older false completions. It reports findings and exits non-zero"). Run
against a fresh `main` checkout of this repo (tip `61345dd9d4aae38324627237ac0128672a1d4b6e`, with
full unshallowed history so this is not a shallow-clone artifact), it printed 170 "findings" across
51 ledgers. Manually verifying every distinct cause shows essentially all of them are false
positives from two independent bugs in `scripts/belt_ledger_completion.py`, and the output format
gives a reader no way to tell a false positive from a real one:

1. **Unreachable commit = false "cannot verify."** `commit_files()` (`scripts/belt_ledger_completion.py:65-83`)
   calls `git show <commit>` and raises `CompletionEvidenceError` when it fails; `completion_errors()`
   (`scripts/belt_ledger_completion.py:96-120`) turns that into the finding string
   `"task {id} commit {commit} cannot verify commit {commit}: {exc}"`. 162 of the 170 findings are
   this message. Every one I checked cites a commit that still exists on GitHub (confirmed via
   `gh api repos/stranske/Workflows/commits/<sha>`, e.g. `b4fb397923778003bc49d715b196edba3e653bd9`
   and `a0f2f6d338277619bac4dedd7fa6dc788713bba3`, both `parents:1`) but is **not reachable from `main`
   in any clone**, full or shallow — because this repo's belt workflow commits the task on a PR
   branch and the PR is squash-merged with the branch deleted (`agents-72-codex-belt-worker.yml`'s own
   "Checkout branch" step uses `fetch-depth: 0`, so the live gate sees these fine at write time; it is
   only the *retrospective* audit that runs after squash-merge discards the branch). A squash-merged
   repo's historical belt commits are therefore permanently unverifiable by this tool, and it reports
   that as the same kind of "finding" as a real false completion.

2. **Bare filename in the task title = false "missing artifact."** `task_artifacts()`
   (`scripts/belt_ledger_completion.py:40-63`) extracts path-like tokens from backtick spans in the
   task title and requires a file-suffix (`:58`), but does not require — or recover — a directory
   prefix. `commit_has_path()` (`:85-93`) then checks the *extracted bare token* against the commit
   tree with `git cat-file -e {commit}:{path}`, which fails whenever the real file lives in a
   subdirectory. Both of this run's 2 "missing named artifact" findings are this bug, not real
   defects:
   - `.agents/issue-1023-ledger.yml` task `task-01` (commit `e17b5a7d…`) is flagged missing
     `github-api-with-retry.js`; the commit actually adds/modifies `.github/scripts/github-api-with-retry.js`
     (confirmed: `git ls-tree -r --name-only e17b5a7d… | grep github-api-with-retry.js`).
   - `.agents/issue-1296-ledger.yml` task `task-01` (commit `a6c1811e…`) is flagged missing
     `test_llm_provider.py`; the commit actually adds `tests/tools/test_llm_provider.py`.

The remaining 6 findings ("changes only ledger paths") are genuine and already explained by the
2026-09-04 incident fixed in #3391 — all 6 cited commits date to February 2026, before that fix — so
they need no new action. But they are 4% of this run's output; a human or agent reading this tool's
170 lines has no mechanical way to find that 4% signal in the 96% noise, and the tool's own exit code
(1) and framing ("finds older false completions") invite treating all 170 as real.

## Tasks
- [ ] `scripts/belt_ledger_completion.py:65-83` (`commit_files`) — when `git show` fails, distinguish
      "commit unreachable in this checkout" from a genuine missing-artifact/ledger-only verdict.
      Either raise a distinct exception class the caller renders as its own category (e.g.
      `task {id} commit {commit}: UNVERIFIABLE (not reachable from this checkout — likely squash-merged
      and branch-deleted; not evidence of a false completion)`), or have `completion_errors` skip and
      tally such commits separately instead of folding them into `errors`.
- [ ] `scripts/audit_belt_ledger_completion.py:17-33` (`audit_ledgers`) — report the unverifiable count
      separately from the findings count (e.g. a trailing `N commits unverifiable (skipped, not
      findings)` line), so exit code and findings count reflect only commits this checkout could
      actually judge.
- [ ] `scripts/belt_ledger_completion.py:40-63` (`task_artifacts`) — when a backtick token has no
      directory separator, resolve it against the commit tree by basename (e.g. via
      `git ls-tree -r --name-only {commit} | match on Path(p).name == token`) before concluding it is
      absent, and only report "missing" when no path in the tree ends with that basename either.

## Acceptance Criteria
- Named test: `tests/workflows/test_belt_ledger_completion.py::test_commit_files_reports_unverifiable_distinctly`
  — construct a task citing a syntactically valid but locally-unreachable commit SHA (not present in
  the test repo's object store) and assert `completion_errors` (or `audit_ledgers`) classifies it as
  unverifiable, not as a false-completion finding.
- Named test: `tests/workflows/test_belt_ledger_completion.py::test_task_artifacts_bare_filename_matches_nested_path`
  — construct a task titled with a bare backtick filename (e.g. `` `foo.js` ``) and a commit that adds
  `sub/dir/foo.js`; assert `completion_errors` reports no missing-artifact error for that task.
- Deliberate-break → revert: re-introduce the unconditional `git show` failure path (drop the new
  unverifiable classification) → `test_commit_files_reports_unverifiable_distinctly` FAILS → revert.
  Separately, re-introduce bare-basename-only matching in `commit_has_path` → `test_task_artifacts_bare_filename_matches_nested_path`
  FAILS → revert.

## Non-Goals
- Do NOT change the live `agents-72-codex-belt-worker.yml` write-time completion check — it already
  runs on a `fetch-depth: 0` checkout of the live branch and is not affected by either bug.
- Do NOT re-file or relabel the 6 February-2026 "changes only ledger paths" findings — they predate
  and are already covered by #3391; no new ledger edits are in scope here.
- No scaffolding / TODO-only changes; every task above is a concrete edit verified by the named tests.

_Surfaced by the Track D repo-audit refill round (2026-10-02), Phase 1.5 scorecard follow-up on the
`scripts/audit_belt_ledger_completion.py` / `scripts/belt_ledger_completion.py` surface; verified by
running the tool against a full (unshallowed) clone of `main` and cross-checking every distinct
finding class against `git ls-tree`/`git cat-file` and the GitHub commits API._
