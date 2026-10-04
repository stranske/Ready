title:	Maint 71: serialize exact-head review requests across selectors
state:	CLOSED
author:	stranske
labels:	priority:normal
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
number:	3534
--
Maint 71's concurrency group includes active_sync_hash, so candidate/campaign selectors can overlap on the same stable PR. Both runs may list comments before either posts the exact-head @codex review marker, producing duplicate review requests. This does not bypass current exact-head settlement or merge gates, but it wastes reviewer capacity and can delay settlement. Add per-PR serialization or a durable conditional ownership claim; retain owner-token identity, immutable plan/generation/head, read-only dry-run semantics, and regression coverage for simultaneous requests. Follow-up to Workflows#3531; do not mutate generated consumer PRs directly.
