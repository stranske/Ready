## Why (verified evidence)

The mosaic is architecturally a **consumer** of sibling backplane artifacts (evidence objects, manifests, identity refs), but this repo ships no participant registry entry even though local docs and CI already watch for one.

- `docs/contracts/run-contract-v1.md:166-195` documents `config/backplane_participants.json` as the opt-in registry and describes the `consumer` role validating only declared `ingests`.
- `.github/workflows/backplane-conformance.yml:22` triggers on changes to `config/backplane_participants.json`.
- `config/` contains only LLM and docs-drift files — **`config/backplane_participants.json` is absent** (verified with `ls config/` on tip `02ffccf`).
- R3 synthesis (`artifacts/research/R3-manager-mosaic-synthesis.md` §8 rank 2) designates Manager-Mosaic as the cross-source join home.

Without a registry row the conformance workflow cannot ever graduate from permanent skip to validating ingested evidence.

## Scope

Add a consumer-local `config/backplane_participants.json` with a **planned** Manager-Mosaic entry. Do not edit Workflows' fleet registry in this issue.

## Tasks

- [ ] Add `config/backplane_participants.json` declaring `stranske/Manager-Mosaic` with `"role": "consumer"`, `"status": "planned"`, and `"ingests": ["evidence-object/v1", "artifact-manifest/v1", "run-contract/v1", "identity-map-conventions"]`.
- [ ] Point `"parent_issue"` at this repo's mosaic charter issue (`stranske/Manager-Mosaic#3`) until a dedicated backplane rollout issue exists.
- [ ] Add `tests/test_backplane_registry.py::test_manager_mosaic_consumer_entry_present` loading the JSON and asserting the repo entry exists with role `consumer` and the four ingest tokens above.

## Acceptance Criteria

- Named test: `tests/test_backplane_registry.py::test_manager_mosaic_consumer_entry_present` passes under `pytest tests/test_backplane_registry.py`.
- Deliberate-break → revert: remove the Manager-Mosaic participant block → confirm the named test FAILS → revert and confirm it passes.

## Non-Goals

- Do not change synced `scripts/validate_run_contract.py` (fix upstream in Workflows if the validator API changes).
- Do not register Manager-Mosaic in `stranske/Workflows/config/backplane_participants.json` here.
- No scaffolding / TODO-only JSON stubs without the test above.

_Surfaced by repo-audit Track D 2026-09-05; verified by reading `docs/contracts/run-contract-v1.md:166` and confirming `config/backplane_participants.json` missing on tip `02ffccf`._

