## Why

R4 requires a standalone mirror tool reusing Pension-Data supersession pattern without SQLAlchemy (`B2-gap-analysis` §2.3). Repo does not exist yet. Verified: no `clones/doc-mirror` directory in research-program workspace. Pension-Data pattern at `ingest/artifacts.py:52-56` is the behavioral reference.

## Scope

New repo `stranske/doc-mirror` with CLI `doc-mirror ingest|validate|status`, `document-mirror/v1` output, synthetic fixture.

## Non-Goals

- Do NOT use SQLAlchemy or require a database.
- Do NOT implement Graph delta sync (B2-026 — IT blocked).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Scaffold repo from Workflows consumer template with `pyproject.toml` script `doc-mirror`.
- [ ] Implement `src/doc_mirror/ingest.py` mirroring checksum supersession semantics from Pension-Data `artifacts.py:28-35`.
- [ ] Implement `src/doc_mirror/validate.py` against synced `document-mirror-v1.schema.json` (after Workflows B2-023).
- [ ] Add `tests/fixtures/synthetic_mirror/` and `tests/test_ingest_supersede.py`.
- [ ] Add `tests/test_validate_manifest.py`.

## Acceptance Criteria

- [ ] Named test: `tests/test_ingest_supersede.py::test_new_checksum_supersedes_active` passes.
- [ ] **Deliberate-break gate:** skip supersession on duplicate key → test **must FAIL** → revert.
- [ ] `doc-mirror validate tests/fixtures/synthetic_mirror/manifest.json` exits 0.

## Implementation Notes

File after Workflows `03-document-mirror-v1-schema` merges.

_Surfaced by B2-024; greenfield repo._
