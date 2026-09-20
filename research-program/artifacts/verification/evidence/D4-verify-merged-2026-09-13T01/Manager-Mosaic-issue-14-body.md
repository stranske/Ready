title:	[P2] Add config/fact_key_registry.json starter registry and loader
state:	CLOSED
author:	stranske
labels:	agent:codex, enhancement, priority:normal
comments:	1
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	14
--
## Why (verified evidence)

Discrepancy detection and thesis monitoring both require a shared, documented `fact_key` vocabulary, but `config/` contains only LLM and docs-drift entries — no fact registry exists.

- `config/` on tip `02ffccf` lists `llm_slots.json`, `model_registry.json`, `model_selection_policy.json`, and `source_of_truth_docs.yml` only.
- R3 synthesis (`artifacts/research/R3-manager-mosaic-synthesis.md` §10 step 1) calls for a starter registry (fees, liquidity, team, performance, capacity keys) before cross-repo ingest.
- Without a registry, each module will invent parallel keys and contradictions will never join (`R3-manager-mosaic-synthesis.md` §2 row "Contradiction detection").

## Scope

Add a versioned JSON registry of starter `fact_key` strings plus a test that every key referenced in synthetic fixtures appears in the registry.

## Tasks

- [ ] Add `config/fact_key_registry.json` with `"schema_version": "fact-key-registry/v1"` and at least 20 keys covering fees, liquidity, team turnover, net/gross IRR, capacity, and legal notice periods (use work-environment names from Ready grounding doc section D where they exist).
- [ ] Add `src/manager_mosaic/fact_keys.py` with `load_fact_key_registry(path: Path | None = None) -> frozenset[str]` defaulting to `config/fact_key_registry.json`.
- [ ] Add `tests/test_fact_key_registry.py::test_fact_key_registry_contains_core_performance_and_liquidity_keys` asserting keys such as `fund.net_irr` and `legal.withdrawal_notice_days` are present.

## Acceptance Criteria

- Named test: `tests/test_fact_key_registry.py::test_fact_key_registry_contains_core_performance_and_liquidity_keys` passes under `pytest tests/test_fact_key_registry.py`.
- Deliberate-break → revert: remove `fund.net_irr` from the registry → confirm the named test FAILS → revert and confirm it passes.

## Non-Goals

- Do not wire the registry into LLM extraction pipelines (Doc-Lineage / Inv-Man-Intake own extraction).
- Do not publish the registry to Workflows in this issue — local consumer copy first.
- No scaffolding / TODO-only JSON without the loader and test above.

_Surfaced by repo-audit Track D 2026-09-05; verified by listing `config/` and confirming no `fact_key_registry.json` on tip `02ffccf`._

