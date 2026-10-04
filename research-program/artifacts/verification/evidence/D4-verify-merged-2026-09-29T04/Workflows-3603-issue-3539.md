title:	[sync-review] Fix upstream manifest-synced paths blocking stranske/learning-management-system#710
state:	CLOSED
author:	stranske
labels:	automation, consumer-sync, priority:normal
comments:	4
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	3539
--
## Upstream sync review debt

Consumer delivery PR: stranske/learning-management-system#710

Manifest-synced paths with unresolved bot review threads:
- consumer `docs/contracts/schemas/output-substrate-v1.schema.json` → source `stranske/Workflows/docs/contracts/schemas/output-substrate-v1.schema.json`

Fix these paths in Workflows main so the next sync regeneration outdates the consumer threads.
