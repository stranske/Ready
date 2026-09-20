## Why (verified evidence)

The repo charter promises contradictions that "surface on their own" (`README.md:9`), but no discrepancy logic exists anywhere in `src/`.

- `README.md:9-10` lists discrepancy detection as in-scope for Manager-Mosaic.
- `src/manager_mosaic/__init__.py:1-33` contains only template arithmetic/greet helpers.
- Inv-Man-Intake already ships a deterministic numeric conflict pattern in `performance/conflict_resolver.py:14-47` (threshold-based escalation) that this repo should mirror for normalized facts rather than reinventing LLM comparison.

Issue #3 covers the hand-edited store shapes; this issue adds the **cross-fact comparator** that turns multiple evidence-backed facts with the same key into reviewable discrepancy records.

## Scope

Implement deterministic numeric discrepancy detection for normalized facts sharing `(fact_key, entity_ref, period)`. Narrative/LLM discrepancy detection is out of scope for v1.

## Tasks

- [ ] Add `src/manager_mosaic/discrepancy.py` with `@dataclass(frozen=True) FactRecord(fact_key, entity_ref, period, value: float, evidence_id: str)` and `@dataclass(frozen=True) DiscrepancyRecord(discrepancy_id, fact_key, entity_ref, period, values: tuple[float, ...], evidence_ids: tuple[str, ...], kind: Literal["numeric_delta"])`.
- [ ] Implement `detect_numeric_discrepancies(facts: Sequence[FactRecord], *, threshold_percent: float = 5.0) -> list[DiscrepancyRecord]` flagging groups where two or more facts share the same `(fact_key, entity_ref, period)` and relative difference exceeds `threshold_percent`.
- [ ] Add `tests/test_discrepancy_detection.py::test_detect_numeric_discrepancies_flags_conflicting_irr_values` with two synthetic IRR facts at 12.0 and 18.0 for the same key/entity/period expecting one discrepancy.

## Acceptance Criteria

- Named test: `tests/test_discrepancy_detection.py::test_detect_numeric_discrepancies_flags_conflicting_irr_values` passes under `pytest tests/test_discrepancy_detection.py`.
- Deliberate-break → revert: raise `threshold_percent` above the fixture spread so the function returns `[]` → confirm the named test FAILS → revert and confirm it passes.

## Non-Goals

- Do not implement narrative/LLM discrepancy classification in this issue.
- Do not build HTML rendering (Deliverable-Render).
- Do not duplicate #3 store validation — consume normalized facts only.
- No scaffolding / TODO-only modules.

_Surfaced by repo-audit Track D 2026-09-05; verified by reading `README.md:9` and confirming absence of `src/manager_mosaic/discrepancy.py` on tip `02ffccf`._

