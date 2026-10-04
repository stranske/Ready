title:	[sync-review] Fix upstream manifest-synced paths blocking stranske/Ready#585
state:	CLOSED
author:	stranske
labels:	automation, consumer-sync, priority:normal
comments:	12
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	3538
--
## Upstream sync review debt

Consumer delivery PR: stranske/Ready#585

Manifest-synced paths with unresolved bot review threads:
- consumer `docs/contracts/schemas/evidence-object-v1.schema.json` → source `stranske/Workflows/docs/contracts/schemas/evidence-object-v1.schema.json`

Fix these paths in Workflows main so the next sync regeneration outdates the consumer threads.
