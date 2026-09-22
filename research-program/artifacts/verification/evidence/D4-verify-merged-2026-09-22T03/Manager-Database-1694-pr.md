# PR #1694

## Summary
- Replace unavailable `apt` `awscli` with a pinned, SHA-verified AWS CLI v2 installer in `database-snapshot.yml`.
- Add `aws`/`pg_dump` version checks and credential-isolation assertions before the dry-run step.
- Gate manual `workflow_dispatch` on `dry_run` (default `true`) so branches can validate installation without production secrets.

Closes #1675

## Test plan
- [x] `uv run pytest tests/test_db_snapshot_restore.py --no-cov` — 6 passed
- [x] Deliberate-break gate: restoring apt `awscli` fails `test_database_snapshot_workflow_installs_verified_clients_before_dry_run`; reverted
- [x] Credential-free workflow dispatch on this branch (`dry_run=true`) — https://github.com/stranske/Manager-Database/actions/runs/35519010660 SUCCESS on head 9760cc249efcd63081ea9e35b78d1e2573c0c40f; installer, client versions, secret isolation, and dry-run PASS; production snapshot SKIPPED.