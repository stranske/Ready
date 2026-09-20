title:	docs: normalize setup checklist references
state:	MERGED
author:	stranske
labels:	
comments:	2
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	2180
--
## Summary
- Reword the consumer setup checklist automation shortcut to use plain "GitHub settings" wording and section numbers.
- Update the sync manifest description to avoid section-symbol references in generated sync PR summaries.

## Validation
- python scripts/validate_template_sync.py
- python scripts/validate_template_completeness.py --strict --manifest .github/sync-manifest.yml --source local-review-fix
- python -c 'import yaml; yaml.safe_load(open(".github/sync-manifest.yml", encoding="utf-8")); print("sync-manifest.yml parsed")'
- git diff --check
