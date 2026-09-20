title:	[P2] Include change facts in live chat messages
state:	CLOSED
author:	stranske
labels:	bug, priority:normal
comments:	0
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1064
--
# [P2] Include change facts in live chat messages

## Why

`src/counter_risk/chat/session.py:292` is current evidence at current main 7c01963cb4173128c806347e622ed43a08fdcf4a. Current break at the transport boundary: asking show deltas computes DeltaOnlyBank delta_notional=876543.21 locally, but that name and value never reach LangChain invoke. `build_guarded_prompt` includes summary/warnings/top exposures only (`src/counter_risk/chat/session.py:404`), and `src/counter_risk/chat/providers/base.py:133` invokes the provider with messages while ignoring context_answer. Offline providers and test doubles consume context_answer, masking the missing facts. No live model response or external API call was used to establish this payload omission.

## Scope

Carry relevant loaded deltas into the actual guarded provider messages, preserving untrusted-data handling and bounded prompt size.

## Non-Goals

No upstream workflow changes, model redesign, or unrelated refactors. Scaffold-only completion does NOT count: adding a helper or a test double that leaves include change facts in live chat messages unimplemented is a failure of this issue.

## Tasks

- [ ] In `src/counter_risk/chat/session.py`, serialize the requested delta facts into guarded message content before provider invocation, using existing sanitization and data boundaries.
- [ ] In `tests/test_chat_provider_clients.py`, add `test_delta_facts_reach_langchain_invoke`. Exercise ChatSession through the actual LangChainProviderClient with only the final client.invoke transport intercepted; assert the name and value are in messages and malicious source strings remain untrusted.

## Acceptance Criteria

- [ ] `python -m pytest tests/test_chat_provider_clients.py -q` passes and collects `test_delta_facts_reach_langchain_invoke`. The named transport test finds DeltaOnlyBank and 876543.21 in the actual messages for show deltas; ordinary top-exposure queries remain supported without network access.
- [ ] Deliberate-break gate: temporarily restore the faulty behavior in `src/counter_risk/chat/session.py`; `tests/test_chat_provider_clients.py::test_delta_facts_reach_langchain_invoke` must fail; revert the deliberate break and rerun the named test to pass. Capture both outcomes in the implementation PR.
- [ ] The test exercises the actual production boundary and retains a valid-input control.

## Implementation Notes

Verified audit work order filed 2026-09-14. Current-code proof: lead-chat-delta-proof.py uses the actual adapter with an intercepted final transport. Historical #108/#25 introduced run review; #1036 fixes exposure sorting, not delta context transfer.
