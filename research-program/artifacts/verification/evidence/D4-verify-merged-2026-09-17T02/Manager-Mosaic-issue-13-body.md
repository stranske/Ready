## Why (verified evidence)

Investment thesis monitoring is explicit repo scope (`README.md:9`, `CLAUDE.md:109-113`) but no code evaluates thesis claims against incoming facts.

- `README.md:3-4` states the mosaic monitors a written investment thesis against what documents actually say.
- `src/manager_mosaic/__init__.py:1-33` has no thesis types or evaluators.
- R3 synthesis (`artifacts/research/R3-manager-mosaic-synthesis.md` §5.1) specifies a `ThesisCheck.verdict` enum (`supported`, `at_risk`, `contradicted`, `insufficient_evidence`) aligned with public thesis-monitor products — the fleet should encode that enum now so downstream renderers do not invent parallel vocabulary.

## Scope

Add thesis claim/check datatypes and a deterministic evaluator for numeric `expected_pattern` rules (`min`, `max`). LLM narrative evaluation is out of scope.

## Tasks

- [ ] Add `src/manager_mosaic/thesis.py` defining `ThesisClaim(claim_id, claim_text, entity_ref, fact_key, expected_pattern: Literal["min","max"], threshold: float)` and `ThesisCheck(claim_id, verdict, evidence_ids: tuple[str, ...])` with `verdict` in `{supported, at_risk, contradicted, insufficient_evidence}`.
- [ ] Implement `evaluate_claim(claim: ThesisClaim, facts: Sequence[FactRecord]) -> ThesisCheck` importing `FactRecord` from `manager_mosaic.discrepancy` (or a shared `facts.py` if created while implementing #7).
- [ ] Return `insufficient_evidence` when no fact matches `(claim.entity_ref, claim.fact_key)`; return `contradicted` when the latest fact violates the pattern; return `supported` when it satisfies the pattern.
- [ ] Add `tests/test_thesis_monitoring.py::test_evaluate_claim_marks_contradicted_when_irr_below_min_threshold` with a `min` pattern claim and a fact below threshold.

## Acceptance Criteria

- Named test: `tests/test_thesis_monitoring.py::test_evaluate_claim_marks_contradicted_when_irr_below_min_threshold` passes under `pytest tests/test_thesis_monitoring.py`.
- Deliberate-break → revert: invert the comparison so a below-threshold fact returns `supported` → confirm the named test FAILS → revert and confirm it passes.

## Non-Goals

- Do not build alerting, scheduling, or HTML dashboards.
- Do not auto-resolve discrepancies — human analyst only (`R3-manager-mosaic-synthesis.md` §9 Q4 default).
- No scaffolding / TODO-only enums without evaluator logic.

_Surfaced by repo-audit Track D 2026-09-05; verified by reading `README.md:3-4` and confirming absence of `src/manager_mosaic/thesis.py` on tip `02ffccf`._

