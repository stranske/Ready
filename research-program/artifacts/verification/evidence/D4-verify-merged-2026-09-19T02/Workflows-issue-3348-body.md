## Upstream sync review debt

Consumer delivery PR: stranske/Manager-Database#1622

Manifest-synced paths with unresolved bot review threads:
- consumer `scripts/check_deliberate_break.py` → source `stranske/Workflows/scripts/check_deliberate_break.py`

Fix these paths in Workflows main so the next sync regeneration outdates the consumer threads.