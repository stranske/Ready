title:	[Agent] [M1] Add LangChain-based “Run Review” chat UI (model selection + guardrails) for maintainers/operators
state:	CLOSED
author:	stranske
labels:	needs-human
comments:	2
assignees:	stranske-automation-bot
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	108
--
## Why

You want interactive Q&A on the results (“what changed?”, “top exposures?”, “why did class shift?”) with selectable models.

## Scope

Provide a chat interface inside the Runner (preferred) or as a separate lightweight window that loads run context.

## Non-Goals

RAG over arbitrary folders
Complex multi-user chat history storage

## Tasks

- [ ] Create `src/counter_risk/chat/context.py` to load `manifest.json`, canonical tables saved as CSV/Parquet in the run folder, and key warnings and deltas.
  - [ ] Define scope for: Create the context.py module with a RunContext class that holds loaded run data (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Create the context.py module with a RunContext class that holds loaded run data (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Create the context.py module with a RunContext class that holds loaded run data (verify: confirm completion in repo)
  - [ ] Implement a function to load (verify: confirm completion in repo)
  - [ ] parse manifest.json from a run folder path (verify: confirm completion in repo)
  - [ ] Implement a function to discover (verify: confirm completion in repo)
  - [ ] load CSV or Parquet tables from the run folder (verify: confirm completion in repo)
  - [ ] Implement a function to extract key warnings (verify: confirm completion in repo)
  - [ ] deltas from the loaded manifest data (verify: confirm completion in repo)
  - [ ] Add error handling for missing or malformed files in the run folder (verify: confirm completion in repo)
- [ ] Create `src/counter_risk/chat/session.py` with provider/model selection flags.
  - [ ] Define the ChatSession class interface with initialization parameters for provider (verify: confirm completion in repo)
  - [ ] Define the ChatSession class interface with model (verify: confirm completion in repo)
  - [ ] Implement provider selection logic supporting multiple LLM providers with API key validation (verify: confirm completion in repo)
  - [ ] Implement model selection logic with validation against available models per provider (verify: confirm completion in repo)
  - [ ] Add configuration flags or parameters to specify provider (verify: config validated)
  - [ ] model at runtime (verify: confirm completion in repo)
  - [ ] Define scope for: Implement session state management to track conversation context across queries (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Implement session state management to track conversation context across queries (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Implement session state management to track conversation context across queries (verify: confirm completion in repo)
- [ ] Add prompt-injection safeguards in the chat prompting logic to treat workbook text as untrusted input.
  - [ ] Implement input sanitization to escape or remove potentially malicious prompt injection patterns (verify: confirm completion in repo)
  - [ ] Define scope for: Add clear delimiters in prompts to separate system instructions from user-provided data (verify: confirm completion in repo)
  - [ ] Implement focused slice for: Add clear delimiters in prompts to separate system instructions from user-provided data (verify: confirm completion in repo)
  - [ ] Validate focused slice for: Add clear delimiters in prompts to separate system instructions from user-provided data (verify: confirm completion in repo)
  - [ ] Implement validation to detect (verify: confirm completion in repo)
  - [ ] reject queries containing prompt injection attempts (verify: confirm completion in repo)
  - [ ] Add logging for suspicious input patterns that may indicate injection attempts (verify: confirm completion in repo)
  - [ ] Document the prompt injection safeguards (verify: confirm completion in repo)
  - [ ] their limitations in code comments (verify: confirm completion in repo)
- [ ] Update the Runner UI to integrate a chat entrypoint labeled “Ask about this run”.
- [ ] Write minimal tests to verify the chat context loader returns non-empty summaries for a run folder.

## Acceptance Criteria

- [ ] Provider/model can be selected (where keys exist) and a question can be asked about a run via the chat interface.
- [ ] For the query “top exposures”, the returned values match `manifest.json`-derived values within tolerance.
- [ ] Tests verifying context loads and returns non-empty summaries pass.

## Implementation Notes

_Not provided._

<details>
<summary>Original Issue</summary>

```text
Topic GUID: 79a13e17-34a8-5bcb-961a-0b9a9cf365c8

## Why
You want interactive Q&A on the results (“what changed?”, “top exposures?”, “why did class shift?”) with selectable models.

## Scope
Provide a chat interface inside the Runner (preferred) or as a separate lightweight window that loads run context.

## Non-Goals
- RAG over arbitrary folders
- Complex multi-user chat history storage

## Tasks
- [ ] Add `src/counter_risk/chat/context.py` to load:
- [ ] manifest.json
- [ ] canonical tables saved as CSV/Parquet in the run folder
- [ ] key warnings and deltas
- [ ] Add `src/counter_risk/chat/session.py` with provider/model selection flags
- [ ] Add prompt-injection safeguards (treat workbook text as untrusted)
- [ ] Integrate chat entrypoint into Runner UI (“Ask about this run”)
- [ ] Add minimal tests: context loads and returns non-empty summaries

## Acceptance Criteria
- [ ] User can select provider/model (where keys exist) and ask questions about a run
- [ ] Answers for “top exposures” match manifest-derived values within tolerance

## Implementation Notes
_Not provided._

---
Synced by [workflow run](https://github.com/stranske/Counter_Risk/actions/runs/21969701501).
```
</details>
