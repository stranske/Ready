## Why (verified evidence)

D4-verify-merged-2026-09-27T03 read squash diff for stranske/Manager-Database#1728 (merge `ae68cd2cb1c37780979ef7cca7739a7e7808093b`) against #1682. Postgres CI wiring landed: `.github/workflows/ci.yml` exports `DOCUMENT_TEST_POSTGRES_URL` and runs `pytest tests/test_document_managers_migration.py -k document_association` in the `postgres-integration` job.

The acceptance criterion requiring a **deliberate-break → revert** demonstration (disable `document_managers` insert in `embeddings.py` → shared-document test FAILS on Postgres → restore → passes) is not evidenced in the squash diff or PR body beyond a narrative claim—no RED/GREEN pytest transcript.

## Tasks

- [ ] Execute the deliberate-break on `main`: temporarily disable the `document_managers` association insert in `src/manager_database/embeddings.py` (or the path cited in #1682), run `pytest tests/test_document_managers_migration.py -k document_association -v` against Postgres (or the CI-equivalent env), capture FAIL output.
- [ ] Revert the mutation, re-run the same command, capture PASS output, and post both blocks as a comment on #1682 (or add `docs/evidence/` transcript linked from the issue).

## Acceptance Criteria

- Named test: `pytest tests/test_document_managers_migration.py -k document_association` passes on Gate with Postgres available (already true on `main` after #1728).
- Deliberate-break → revert: disable `document_managers` insert → named pytest FAILS with Postgres → restore → passes; **literal command output** for FAIL and PASS recorded on #1682.

## Non-Goals

- Do NOT remove or weaken the CI Postgres wiring from #1728.
- No scaffolding / TODO-only changes.

_Surfaced by D4-verify-merged-2026-09-27T03; verified against `Manager-Database-1728.diff` and issue #1682. Related: #1682, merged PR #1728._
