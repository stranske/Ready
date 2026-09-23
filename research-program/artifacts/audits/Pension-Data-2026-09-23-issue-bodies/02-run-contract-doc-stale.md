## Why (verified evidence)
`docs/contracts/run-contract-v1.md:15-17` still states “No participant emits an envelope yet (that is P1+)”, which contradicts the shipped one-PDF pilot emitter:

- `src/pension_data/ops/backplane_emitter.py:19-20` sets `RUN_SCHEMA_VERSION = "run-contract/v1"` and writes `run.json` / `manifest.json`.
- `src/pension_data/ops/one_pdf_pilot_cli.py:117-131` documents backplane outputs on every successful pilot run.
- `tests/ops/test_backplane_emitter.py:91-150` validates strict conformance.

**User-facing consequence:** integrators and fleet validators reading the contract doc believe Pension-Data does not emit envelopes, causing duplicate emitter work or skipped conformance checks.

## Tasks
- [ ] Update `docs/contracts/run-contract-v1.md:15-17` to record that `stranske/Pension-Data` participates via `one-pdf-pilot` / `build_backplane_reference_run` and reference `config/backplane_participants.json` entry if present.
- [ ] Add a short “Pension-Data reference run” subsection pointing to `src/pension_data/ops/backplane_emitter.py:104-235` and the CLI flags that write `run.json`.
- [ ] Add `tests/docs/test_contract_doc_drift.py::test_run_contract_doc_mentions_pension_data_emitter` (or extend an existing docs contract test) asserting the stale “No participant emits” sentence is absent.

## Acceptance Criteria
- Named test: `tests/docs/test_contract_doc_drift.py::test_run_contract_doc_mentions_pension_data_emitter`.
- Deliberate-break → revert: reintroduce the “No participant emits an envelope yet” sentence → confirm the named test FAILS → revert.

## Non-Goals
- Do NOT change JSON schema or emitter logic in this doc-only issue.
- No scaffolding / TODO-only changes.

_Surfaced by repo-audit Track D 2026-09-23; verified by reading `run-contract-v1.md` and `backplane_emitter.py` on tip `33a29aa`._
