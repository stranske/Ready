title:	Resolve SQLite manager identity in RAG context extraction
state:	CLOSED
author:	stranske
labels:	bug, priority:normal, testing
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
number:	1672
--
## Why

Current conditional break: `chains/rag_search.py:87` queries managers.manager_id and returns an empty catalog on schema error. `chains/rag_search.py:197` repeats the assumption for explicit manager filters. The repo bootstrap at `scripts/seed_managers.py:48` uses id. Matched fixtures yield a manager-1 match for the full Elliott name on manager_id schema and no match on id schema, silently dropping structured manager context.

## Scope

RAG catalog, manager matching, and structured manager context on both supported SQLite schemas and Postgres.

## Non-Goals

Do not change LLM prompts, model selection, or semantic ranking. Scaffold-only completion does NOT count: resolving catalog names but leaving explicit structured filters broken is a failure of this issue.

## Tasks

- [ ] Resolve and alias the manager key in `_manager_catalog` in `chains/rag_search.py` using the existing helper in `adapters/base.py`.
- [ ] Use the resolved manager key for the explicit manager filter in `_structured_search` in `chains/rag_search.py`.
- [ ] Add id-schema cases to `tests/test_rag_search_chain.py` for name extraction, explicit manager context, and unrelated managers.

## Acceptance Criteria

- [ ] pytest tests/test_rag_search_chain.py must pass; new key-matrix tests extract manager ID 1 from the same manager name on either schema and return that manager context for explicit filters without cross-manager records.
- [ ] Deliberate-break gate: Restore the hardcoded catalog query in `chains/rag_search.py`; the new id-schema extraction test in `tests/test_rag_search_chain.py` must fail; revert and rerun.

## Implementation Notes

Verified at 4523cf50dac3f3fe2ba338b8243e630940c54fd0. Reproduction imports llm before chains to match application startup and isolate the schema issue from the separate standalone circular-import limitation. No LLM/provider calls used.

