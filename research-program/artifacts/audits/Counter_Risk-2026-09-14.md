# Counter_Risk demand-driven audit refill — 2026-09-14

**Result:** filed eight verified, agent-ready issues on `stranske/Counter_Risk` at remote `main` `7c01963cb4173128c806347e622ed43a08fdcf4a`. The trigger was one open agent-ready issue against a threshold of two.

## Verification

- Scope: first-party application code, tests, documentation, and repo-owned automation. Workflows-synced `.github/` content was excluded.
- Orientation: 26,119 application Python LOC, 41,731 test Python LOC, 2,109 collected tests, and `uv run ruff check src tests` passed.
- The 2026-09-13 audit findings were independently re-opened at repo-relative citations. Current main differs only in dependency/workflow-pin metadata, not any cited app or test path.
- All eight bodies pass `uv run python .github/scripts/issue_format.py <body>` from the refreshed clone. A focused suite covering the touched modules collected 301 tests and was green through its completed output.
- Dedup: three open issues were present; only #1058 was agent-ready and it is a coverage task. Recent closed issues #1000–#1050 cover earlier finite/alias/rendering repairs, not these eight defects.

## Filed work

1. [#1061](https://github.com/stranske/Counter_Risk/issues/1061) — canonical registry aliases bypass counterparty caps (P1).
2. [#1062](https://github.com/stranske/Counter_Risk/issues/1062) — split counterparty rows understate concentration (P1).
3. [#1063](https://github.com/stranske/Counter_Risk/issues/1063) — malformed nonblank maturity values become zero (P2).
4. [#1064](https://github.com/stranske/Counter_Risk/issues/1064) — live chat omits computed delta facts at provider transport (P2).
5. [#1065](https://github.com/stranske/Counter_Risk/issues/1065) — skipped link refresh is reported as skipped PPT generation (P2).
6. [#1066](https://github.com/stranske/Counter_Risk/issues/1066) — PDF requests disappear when distribution output is disabled (P2).
7. [#1067](https://github.com/stranske/Counter_Risk/issues/1067) — active optional report inputs lack manifest hashes (P2).
8. [#1068](https://github.com/stranske/Counter_Risk/issues/1068) — PDF export receives a deck before its optional concentration slide is appended (P2).

Each uses only `bug` plus the repository's priority label; no routing labels were added. The Agents Issue Format Guard completed successfully for every final body.

## Limits and risk

Browser UI, Windows frozen GUI, and real COM/PDF rendering were unavailable. The PDF finding captures the real pipeline's export-generator input (23 slides) and final PPTX (24 slides), not rendered PDF pages. The issue explicitly retains that platform handoff boundary.

An issue-body normalization command briefly changed PR #1060 due to a zero-based offset. It was immediately restored to its original preamble and automated-status body; no code, branch, title, or review state was touched. Every target issue was then re-read with the intended title, body, and labels.

## Durable-record exception

The required Dropbox `Code/Audits/Counter_Risk/` and `Code/Audits/AUDIT_LEDGER.md` updates could not be written from this execution environment: the filesystem policy rejects writes outside the research-program workspace and permits no approval escalation. This OUT report, the unit checkpoint, and the intake rows contain the complete handoff needed to mirror the record; no claim is made that the Dropbox ledger changed.

## Attempt 2 reconciliation

At `2026-09-14T07:51:03Z`, `git pull --ff-only` confirmed that the clone and `origin/main` remain at `7c01963cb4173128c806347e622ed43a08fdcf4a`. Live GitHub reads confirmed #1061–#1068 are open with the intended six issue-format sections and only `bug` plus the applicable repository priority label. The eight corresponding Agents Issue Format Guard runs all have `conclusion=success`. The required eight intake rows remain present. A read-only check of the Dropbox ledger and repo index found no #1061–#1068 or 2026-09-14 Counter_Risk entry, so the durable-record exception remains real rather than resolved.

## Attempt 3 reconciliation

At `2026-09-14T08:06Z`, a fresh `git pull --ff-only` again left the clone and `origin/main` at `7c01963cb4173128c806347e622ed43a08fdcf4a`; pre-existing untracked `dossier-out/` and `uv.lock` were not touched. Public GitHub API reads confirmed that #1061–#1068 remain open, have all six required issue-format headings, and retain exactly `bug` plus `priority:high` (P1) or `priority:normal` (P2). The final matching format-guard runs are successful: 34815783575, 34815783690, 34815785952, 34815787152, 34815788415, 34815790525, 34815790506, and 34815792439. All eight intake URLs remain in the required sink.

The original proof scripts were rerun at that exact main tip. They reproduced all eight behavioral claims: alias-limit bypass, split-row concentration understatement, malformed XLSX total coercion to zero, delta omission at the final chat transport, skipped-link status skew, silent PDF suppression, optional-input hash omission, and export at 23 slides before the final deck reaches 24. The only comparison difference between issued bodies and their pre-filing drafts is intentional filing normalization (the current-main SHA and filed-status note); each remote body still matches the verified finding and format contract.

The durable-record exception is still the only unmet directive. The Dropbox `Code/Audits` record remains read-only under this sandbox, so this run deliberately did not claim that it was updated.
