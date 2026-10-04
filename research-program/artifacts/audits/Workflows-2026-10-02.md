Scorecard: 5 work / 0 partial / 0 broken / 0 fabricated / 2 not exercised of 7; journey: passes; surfaces unscored 0; closed-still-broken 0.

# Workflows Track D refill — 2026-10-02

Unit: `D-audit-Workflows--2026-10-02T10-11-02Z`. Trigger: fleet-ready-issue supply for `stranske/Workflows`
dropped to ≤25% of the last filed set (20 open issues total; only 1 carries `agent:auto`, 1 carries
`needs-human`; the rest are trackers/automated/sync-review bookkeeping).

## What changed since the last scorecard (2026-09-27, tip `a8f1e45`)

Tip is now `61345dd9d4aae38324627237ac0128672a1d4b6e` (57 intervening commits). `gh` is authenticated
in this executor — the prior three rounds (09-23, 09-26, 09-27) were all blocked on `gh` auth and
filed 0 issues despite real findings (09-27's REFUTED `#3525` recheck). This is the first round able
to file since 09-23.

## C1–C5 reconfirmed WORKS

Re-ran the test suites rather than trusting the prior round's numbers given 57 new commits, two of
which touch the C5 surface (`#3614`, `#3615`):

- C1 sync-manifest: `pytest -k "manifest or sync_manifest"` — 202 passed, 1 skipped (needs `GH_TOKEN`, n/a)
- C2 run-contract validation: `pytest -k contract` — 328 passed
- C3 capability bundle: `node --test capability-bundle-contract.test.js` — 13 passed
- C4 metrics dashboard: `pytest tests/e2e/test_metrics_dashboard.py` — 2 passed
- C5 belt-scan proxy: `node --test github-rate-limited-wrapper.test.js github-api-with-retry.test.js`
  — 57 passed, including the `__getTokenSource` identity test that #3525/#3587 turned on.

C6 (consumer sync delivery) and C7 (Gate verdict on a real consumer PR) remain NOT-EXERCISED by
deliberate, repeatedly-reaffirmed policy — withheld from production mutation. This is unchanged
debt, not new.

## Interior-surface scoring — closes "surfaces unscored 2"

The two scripts flagged "unscored" on 2026-09-24/09-26/09-27 are
`scripts/audit_belt_ledger_completion.py` and `scripts/belt_ledger_completion.py` — the documented
tool (`docs/ci/LEDGER.md:35-40`) for retrospectively auditing whether a Codex-belt task marked `done`
actually has evidence. I ran it live against a **full, unshallowed** clone of the tip (not the
research-program driver's default shallow clone, specifically to rule out a shallow-depth artifact
before concluding anything):

```
python3 scripts/audit_belt_ledger_completion.py --root .
```

It printed 170 findings across 51 ledgers, exit 1. I verified every distinct cause class by hand
(`git cat-file`, `git ls-tree`, and the GitHub commits API where the local object store couldn't
answer):

- **162/170 — false "cannot verify."** The cited commit is real (confirmed via
  `gh api repos/stranske/Workflows/commits/<sha>`) but unreachable from any local clone of `main`,
  because this repo's belt workflow commits land on a PR branch that is squash-merged and then
  deleted — this repo's standard merge path. The *live* belt worker isn't affected (its "Checkout
  branch" step in `agents-72-codex-belt-worker.yml` uses `fetch-depth: 0` on the still-live branch,
  before merge); only the retrospective audit, run after the fact, hits this. `completion_errors()`
  folds this into the same findings list as a real defect with no distinguishing type.
- **2/170 — false "missing named artifact."** `task_artifacts()` strips directory context from a
  bare backtick-quoted filename in the task title, and `commit_has_path()` then requires an exact
  path match — so a file that is genuinely present one directory down (verified with `git ls-tree`,
  e.g. `.github/scripts/github-api-with-retry.js` for a title naming only `` `github-api-with-retry.js` ``)
  reads as missing.
- **6/170 (3.5%) — genuine**, and all predate and are already explained by `#3391` (closed
  2026-09-24; all 6 cited commits date to February 2026).

Scored: **BROKEN**. The tool is ~96% noise around its own stated purpose, and its output format gives
no way to separate the 3.5% signal from the rest. Full output saved at
`Workflows-2026-10-02-assets/belt-ledger-audit-full.txt`.

Surfaces unscored this round: **0** (was 2).

## Delivery

Filed **stranske/Workflows#3696** — `[P1] audit_belt_ledger_completion.py is ~96% false positives —
squash-merged commits unreachable + bare-filename artifact matching` — `priority:high` applied;
dedup-checked clean (`gh issue list --search` on the tool's function names and symptom, 0 hits).
Body at `Workflows-2026-10-02-assets/issue-belt-ledger-audit.md`. The fleet's `agents:formatted`
format-guard label had not yet landed as of this report (checked ~1 minute post-filing); nothing in
the body uses the `[LOCAL_WORKSPACE]/<Repo>/...` path form the format guard rejects, and every cited path is
relative to the target repo per the citation rule.

No REFUTED lines this round — no candidate was dropped against a closed issue whose reproduction
still fails.

## Coverage debt

4 (not-exercised 2 + unscored 2) on 09-26/09-27 → **2** (not-exercised 2 + unscored 0) today. The
remaining 2 are the deliberately-withheld production-mutation probes (C6/C7), not an open gap.

## Artifacts

- `Code/Audits/Workflows/2026-10-02-SCORECARD.md`
- `Code/Audits/AUDIT_LEDGER.md` (2026-10-02 entry appended)
- `Code/Audits/Workflows/README.md` (latest-round pointer updated)
- `research-program/artifacts/audits/Workflows-2026-10-02-assets/belt-ledger-audit-full.txt` (raw tool output, full-clone run)
- `research-program/artifacts/audits/Workflows-2026-10-02-assets/issue-belt-ledger-audit.md` (filed issue body)
- `~/.codex/orchestrator/measurement/intake-2026-09-04.log` (appended: `stranske/Workflows|...|https://github.com/stranske/Workflows/issues/3696`)
