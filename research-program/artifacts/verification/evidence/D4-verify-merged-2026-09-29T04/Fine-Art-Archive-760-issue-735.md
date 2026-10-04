title:	Dropbox conflict resolution is forking operations.log, the discovery frontier and the growth_tick lock
state:	CLOSED
author:	stranske
labels:	agents:formatted, bug, priority:normal
comments:	11
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	735
--
## Why

Dropbox conflict resolution on the synced archive workspace forks `operations.log`, `discovery_frontier.json`, and lock files when two hosts run the scheduled tick against the same tree. Measured on the Mac workspace 2026-09-21 (nine conflicted copies; G55 budget undercount; discovery cycle rolled back).

## Scope

Repository-owned guards and lock placement for Track A automation (`scripts/build_weekly_review.py`, `src/fine_art_archive/api/gates.py`). Data merge of forked workspace files is out of scope here.

## Non-Goals

- Do not merge or delete owner workspace conflict copies without an explicit relocation grant.
- Do not change image bytes under `data/` or work sidecars.

## Tasks

- [ ] In `src/fine_art_archive/api/gates.py`, document and enforce a non-synced lock path (or host-aware lease) instead of a lock file on the Dropbox-synced workspace root.
- [ ] In `scripts/build_weekly_review.py`, add a preflight that fails when any `*conflicted copy*` filename exists beside `operations.log` or `discovery_frontier.json` defaults.
- [ ] Add `tests/test_workspace_conflict_guard.py` with `pytest` coverage for the conflicted-copy detector and lock-path policy.

## Acceptance Criteria

- [ ] Run `pytest tests/test_workspace_conflict_guard.py` and confirm conflicted-copy filenames fail the guard and a fixture without conflicted-copy names passes.
- [ ] Run `python scripts/build_weekly_review.py --help` and confirm the new preflight flag or default behavior is documented in the CLI help text.

## Implementation Notes

Evidence in the issue body references Dropbox workspace paths that are not checked into git; agents implement guards in this repository and leave fork reconciliation to the owner.

