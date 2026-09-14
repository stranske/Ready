## Why

Current automation failure: `.github/workflows/database-snapshot.yml:23` installs awscli through apt on ubuntu-latest. The scheduled 2026-09-14 run 34809590737 at the audited SHA exits 100 with Package awscli has no installation candidate. This prevents both the credential-free contract validation at `.github/workflows/database-snapshot.yml:28` and any configured backup. Main CI success does not validate this scheduled job.

## Scope

Repo-owned snapshot workflow client installation and dry-run acceptance.

## Non-Goals

Do not rotate backup credentials, change retention/encryption, or restore production data. Scaffold-only completion does NOT count: a green unit test without a successful runner installation and dry-run is a failure of this issue.

## Tasks

- [ ] Replace the unavailable apt awscli dependency in `.github/workflows/database-snapshot.yml` with a supported, version-verifiable AWS CLI installation and retain the PostgreSQL client.
- [ ] Verify aws and pg_dump availability before the dry-run step in `.github/workflows/database-snapshot.yml`.
- [ ] Add workflow installation assertions to `tests/test_db_snapshot_restore.py` without requiring production secrets or performing a live restore.

## Acceptance Criteria

- [ ] pytest tests/test_db_snapshot_restore.py must pass. Run the revised snapshot workflow in a branch and test environment without production backup credentials; installation must succeed, aws and pg_dump versions must print, and backup --dry-run must finish before the guarded production step is skipped.
- [ ] Deliberate-break gate: Restore apt installation of awscli in `.github/workflows/database-snapshot.yml`; the new installation-contract test in `tests/test_db_snapshot_restore.py` must fail; revert. Capture a successful credential-free workflow run on the revised branch.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Failure evidence: https://github.com/stranske/Manager-Database/actions/runs/34809590737 . AWS installation guidance: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html . Closed issue 1150 established the contract; this is a current failure of its client bootstrap.
