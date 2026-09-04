# trip-planner dossier verification (2026-09-04)

Adversarial cite-check of `artifacts/dossiers/trip-planner.md` against `clones/trip-planner`.

| Section | Claim | Status | Evidence / correction |
| :--- | :--- | :--- | :--- |
| 4 | `get_workspace_payload` assembles workspace JSON | CONFIRMED | `trip_planner/app/services/workspace.py:2880` |
| 4 | `submit_planner_turn` executes planning dialogue | CONFIRMED | `trip_planner/app/services/planner.py:2258` |
| 4 | `LeisureRankingEngine` / `BusinessRankingEngine` rank scenarios | CONFIRMED | `trip_planner/ranking/leisure.py:121`, `trip_planner/ranking/business.py:127` |
| 4 | `evaluate_itinerary_feasibility` validates bundles | WRONG | Function is `evaluate_bundle_feasibility` returning `FeasibilityAssessment` (`trip_planner/itinerary/feasibility.py:393`) |
| 4 | `build_approval_ready_package` compiles approval packages | CONFIRMED | `trip_planner/business/approval_ready.py:136` |
| 4 | `update_revealed_preferences` adjusts weights from interactions | WRONG | Function is `build_revealed_preference_update` (`trip_planner/preferences/revealed_preference.py:119`) |
| 4 | `HTTPTPPIntegrationClient` + `_CircuitBreaker` wrap remote TPP | CONFIRMED | `trip_planner/integrations/tpp/client.py:216`, `:415` |
| 5 | `trip_id` is root container with example `trip-tokyo-2026` | WRONG | Example not in repo; seeded IDs include `trip-leisure-kyoto-draft` (`trip_planner/resources/state/trips/leisure_draft_trip.json:3`) |
| 5 | `user_id`, `session_id`, SHA-256 `token_hash` auth | CONFIRMED | `trip_planner/persistence/models/session.py:22`, `trip_planner/app/services/auth.py:84` |
| 5 | `saved_scenario_id` + `current_version_id` version head | CONFIRMED | `trip_planner/state/scenarios.py:239-241` |
| 5 | `proposal_id`, `proposal_version` identify proposals | CONFIRMED | `trip_planner/persistence/models/proposal.py:31` |
| 5 | Catalog IDs (`option_id`, `bundle_id`, etc.) and `source_id` | CONFIRMED | `trip_planner/options/*.py` |
| 5 | Catalog items carry `snapshot_id` and `sha256:` content hashes | WRONG | `source_id` on options; `snapshot_id` on `RawSnapshot` (`trip_planner/sources/snapshots.py:132`); no `sha256:` field on catalog option records |
| 5 | SQLAlchemy 2.0 + Alembic; SQLite default; PostgreSQL via env | CONFIRMED | `trip_planner/persistence/db.py:16-31` |
| 5 | Emitted/consumed contract markdown set | CONFIRMED | Files present under `docs/contracts/` |
| 5 | Workflows-only synced contracts documented locally | CONFIRMED | `docs/contracts/schemas/evidence-object-v1.schema.json`, `artifact-manifest-v1.schema.json`, etc. |
| 8 | No `run-contract/v1` emission in `trip_planner/`; validator opt-in SKIP | CONFIRMED | No matches under `trip_planner/`; `scripts/validate_run_contract.py:16-18`; no `config/backplane_participants.json` in repo |
| 8 | Source adapter framework documented but only `base.py` implemented | CONFIRMED | `trip_planner/sources/adapters/base.py` only concrete adapter file |
| 8 | Legacy quick start broken (`jinja2` missing; test skipped) | CONFIRMED | `README.md:95-100`, `scripts/build_html.py:11`, `pyproject.toml:65` |
| 8 | Semantic planner memory vs keyword matching at `planner_tools.py:902` | WRONG citation | Substance confirmed: keyword routing in `planner_routing.py:154-167`; semantic recall still open (`docs/langchain-planner-runtime-epic.md:28`). Line 902 is inside `_read_route_geometry`, not memory logic |
| 8 | Live remote TPP disabled (`live_tpp=off`) | CONFIRMED | `scripts/check_full_product_verification.py:504-508` |
| 9 | Offer `TripPlanProposal` | CONFIRMED | `trip_planner/business/policy_contracts.py:191` |
| 9 | Offer `ApprovalReadyPackage` | CONFIRMED | `trip_planner/business/approval_ready.py:56` |
| 9 | Offer `RankedResultSet` | CONFIRMED | `trip_planner/ranking/models.py:354` |
| 9 | Offer `langsmith-fleet/v1` telemetry | CONFIRMED | `trip_planner/observability/langsmith_fleet.py:23-27` |
| 9 | Consume `TPPPolicyRequirement` via `policy_sync.py` | CONFIRMED | `trip_planner/integrations/tpp/policy_sync.py:52` |
| 9 | Consume `PersistedEvaluationResult` from TPP | CONFIRMED | `trip_planner/integrations/tpp/results.py:65` |
| 9 | Consume calendar events into `required_presence_windows` | CONFIRMED (hook) | Field on `BusinessTravelProfile` (`trip_planner/business/profile.py:59`); no `.ics` ingest yet (prospective) |
| 9 | Collision: `user_id` vs corporate AD/SSO GUIDs | UNVERIFIABLE | Design-level interoperability risk; no AD integration in repo |
| 9 | Collision: `organization_id` vs LEI | UNVERIFIABLE | `organization_id` exists (`trip_planner/persistence/models/policy.py:34`) but LEI validation not implemented |
| 9 | Collision: local slugs (`kyoto`) vs IATA (`NRT`) | UNVERIFIABLE | Fixture uses `trip-leisure-kyoto-draft`; no enforced geo-code standard in code |
| 9 | Collision: internal `EvidenceRecord` vs `evidence-object-v1` | WRONG | Class is `DimensionEvidenceRecord` (`trip_planner/preferences/evidence.py:157`); lacks `evidence-object/v1` schema fields |

**Summary:** 36 claims checked, 7 corrected, 3 unverifiable.

**Corrections applied in dossier:** feasibility function name, revealed-preference function name, `trip_id` example, catalog hash wording, map surface entry point and seam citation, TPP/semantic-memory line refs, `DimensionEvidenceRecord` naming, `AuthSession` location, CI reusable workflow wording.
