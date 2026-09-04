# Workflows dossier — verification table

Verified against clone `clones/Workflows` at HEAD `8f03e5696e342f2ed77194531fc244be5c1764ca` (2026-09-04).
Method: every cited file:line/symbol in sections 4, 5, 8, and 9 opened and checked against current code and documentation.

## Summary

| Verdict | N |
| --- | --- |
| CONFIRMED | 25 |
| WRONG (corrected in dossier) | 7 |
| CITE-DRIFT (substance right, citation refined) | 5 |
| UNVERIFIABLE (requires sibling-repo clone) | 1 |
| **Total checked** | **38** |

### Key Findings & Corrections

1. **§1 fleet size:** Dossier said "13 first-party repositories"; README lists **15** registered consumers (`README.md:16`).
2. **§2 citation drift:** `README.md:12` is "Production Ready", not the Gate claim; sole PR-required check is at `README.md:108`. Keepalive evidence is at `README.md:71`/`83`, not `:43` (delivery PR mechanics).
3. **§3/§7 test counts:** `find tests/` yields **327** Python test files (not 326); `.github/scripts/__tests__/` yields **92** JS test files (not "100+").
4. **§5 evidence ref line:** `EvidenceRef.ref_id` returning `evidence:<digest[:16]>` is at `contract.py:96`, not `:87` (which is the `@property` decorator).
5. **§5 capability-bundle consume cite:** Consumption is via `keepalive_prompt_composer.js:7` (`require('./capability_bundle')`), not `keepalive_loop.js:977` (invalid-JSON error handler).
6. **§5 evidence-object validation cite:** `validate_run_contract.py:259` is a comment; actual consumer-path validation is `_validate_consumer` at `:130-179`; schema self-test at `:403`.
7. **§8 backplane claim cite (adversarial):** Original cited `README.md:96` (blank/`## What's Included`); program docs at `research-backplane-contract.md:6-8` and `run-contract-v1.md:15-17` still say no participant emits yet — stale vs Pension-Data conformant status.
8. **§8 "5 repos deferred with operational blockers":** Overstated — five producers are `planned` with `issue_deferred`, but only Counter_Risk, Manager-Database, and Inv-Man-Intake cite explicit blockers; Trend_Model_Project and Portable-Alpha defer until issues are selected.
9. **§8 closed-loop cite:** `pr-verification-evidence-plan.md:52` is a section separator; non-goal "re-enabling automatic follow-up issue creation" is at `:65`; README follow-up label requirement at `:73`.
10. **§9 sibling ID collisions:** Specific Trend_Model_Project / Inv-Man-Intake / Manager-Database ID-format claims cannot be verified from the Workflows clone alone.

---

## §4 — Major code features

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 1 | PR Gate consumes diffs + path-classification for dynamic CI toggles and delivery seals | `pr-00-gate.yml`, `detect-changes.js`, `path-classification.yml` | CONFIRMED | `pr-00-gate.yml:94` requires `detect-changes.js`; `:80` loads `path-classification.yml`; `:158-165` enforces delivery seal. |
| 2 | Sync manifest compiler emits per-repo sync plans from manifest + templates | `sync_manifest_compiler.py` | CONFIRMED | Module docstring and `PLAN_SCHEMA` at `:1-18`; deterministic plan compilation. |
| 3 | Keepalive loop is event-driven, produces prompt appendices and agent dispatches | `keepalive_loop.js`, `reusable-16-agents.yml` | CONFIRMED | README `:71` documents Gate-completion trigger; `reusable-16-agents.yml:997+` runs keepalive job. |
| 4 | Capability bundle selector injects playbooks from schema-validated bundles | `capability_bundle.js`, schema | CONFIRMED | `capability_bundle.js:6` sets `SCHEMA_VERSION = 'capability-bundle/v1'`. |
| 5 | Dual-model verifier requires unanimous compare-mode agreement (gpt-5.6-terra + claude-sonnet-5) | `reusable-agents-verifier.yml`, `llm_provider.py` | CITE-DRIFT | Compare mode in workflow `:1076-1108` calls `pr_verifier.py --compare`; model names documented at `README.md:90`; slot resolution via `llm_registry.py`, not hardcoded in `llm_provider.py`. |
| 6 | Backplane validator checks run.json + manifest.json with SHA-256 integrity | `validate_run_contract.py` | CONFIRMED | Producer validation at `:207-254` including manifest cross-check `:242-254`. |
| 7 | Fleet review coordinator + evaluator produce decision packets from multi-agent audits | `repo_review_coordinator.py`, `repo_review_evaluator.py` | CONFIRMED | `REPO_REVIEW_PROCESS.md:55-65` documents coordinator entry point and Phase-4 flow. |
| 8 | PDF contract produces content-hashed evidence locators and bbox locators | `contract.py` | CONFIRMED | `BBox` at `:27`; `EvidenceRef.ref_id` at `:96` returns `evidence:{digest[:16]}`. |

---

## §5 — Data model, identifiers and contracts

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 9 | Canonical IDs follow `<entity_type>:<normalized_identity>` with closed vocabulary | `identity-map-conventions.md:44-62` | CONFIRMED | Format at `:44-48`; regex at `:59-61`; closed types table at `:79-88`. |
| 10 | Artifact SHA-256 pattern `^[a-f0-9]{64}$` | `artifact-manifest-v1.schema.json:73` | CONFIRMED | Exact pattern at line 75. |
| 11 | Evidence locator hash `evidence:<sha256[:16]>` | `contract.py:87` | CITE-DRIFT | Property at `:87`; hash computation at `:95-96`. |
| 12 | Capability bundles use `capability_id` + SHA-256 payload hash | `capability-bundle-v1.md:5` | CONFIRMED | Required fields listed at lines 7-8; hash rule at line 12. |
| 13 | run-contract/v1 validated; Workflows excluded; Pension-Data emits | `validate_run_contract.py:207`, `backplane_participants.json:250`, `:32` | CONFIRMED | Producer validation at `:207`; Pension-Data `status: conformant` at `:32`; Workflows excluded at `:249-250`. |
| 14 | evidence-object/v1 validated but verifier does not project outputs | `validate_run_contract.py:259`, `pr-verification-evidence-plan.md:50` | CITE-DRIFT | Line 259 is comment; consumer validation at `:130-179`; gap at plan `:50`. |
| 15 | artifact-manifest/v1 consumed by validator | `validate_run_contract.py:228` | CONFIRMED | Manifest schema validation at `:245-247`. |
| 16 | capability-bundle/v1 emitted and consumed in keepalive | `capability_bundle.js:6`, `keepalive_loop.js:977` | CITE-DRIFT | Emit at `capability_bundle.js:6`; consume via `keepalive_prompt_composer.js:7`, metrics at `keepalive_loop.js:954`. |
| 17 | langsmith-fleet/v1 consumed; Workflows export paused | `langsmith_fleet.py:23`, `langsmith_fleet_registry.json:19` | CONFIRMED | `SCHEMA_VERSION` at `:23`; `rollout_status: paused` at registry `:19-21`. |
| 18 | agent-runner-output.md consumed by codex/claude runners | runner workflows | CONFIRMED | Contract lists compliant implementations at `agent-runner-output.md:19-21`; workflows exist. |

---

## §8 — Claims vs reality (checked hardest)

| # | Dossier claim | Cite | Verdict | Correct statement / Evidence |
|---|---|---|---|---|
| 19 | Docs claim active cross-tool backplane | `README.md:96` | **WRONG (false cite)** | `README.md:96` is blank/`## What's Included`. Stale program claim is at `research-backplane-contract.md:6-8` ("No participant emits…yet"). Reality: Pension-Data conformant (`backplane_participants.json:32`). |
| 20 | Only Pension-Data conformant; 5 repos deferred with operational blockers | `backplane_participants.json:7-233` | **WRONG (overstated)** | One conformant producer confirmed. Five others `planned` with `issue_deferred`; explicit blockers only in Counter_Risk (`:110`), Manager-Database (`:168`), Inv-Man-Intake (`:194`). |
| 21 | PDF extraction README claim vs scaffold reality | `README.md:3`, `DESIGN.md:3,10` | CONFIRMED | Package README `:3-5` claims replacement; DESIGN `:3` status scaffolded, `:10` deliverable 5; no migration completed. |
| 22 | Closed-loop verification vs label-triggered follow-up | `README.md:45-72`, `pr-verification-evidence-plan.md:50-52` | CITE-DRIFT | Pipeline diagram `:45-60` is accurate; follow-up requires labels (`README.md:73`); automatic follow-up is non-goal (`pr-verification-evidence-plan.md:65`). |
| 23 | Live LangSmith metrics vs paused Workflows artifact export | `README.md:90`, `langsmith_fleet_registry.json:19-24` | CONFIRMED | README `:92` cites weekly tracker/dashboard; Workflows `rollout_status: paused` since `2026-06-13` with pause reason at registry `:19-21`. |
| 24 | trend_analysis is CI autofix fixtures, excluded from coverage | `pyproject.toml:201`, `src/trend_analysis/README.md:1-12` | CONFIRMED | Omit pattern at `pyproject.toml:202`; README documents intentional fixtures excluded from coverage. |

---

## §9 — Interoperability hooks

| # | Claim | Cite | Verdict | Evidence / Note |
|---|---|---|---|---|
| 25 | Offers schemas, validator CLI, baseline kit, PDF contract, staged review queues | various | CONFIRMED | Schemas under `docs/contracts/schemas/`; `validate_run_contract.py` CLI; `repo_review_evaluator.py` `issue_queue_status` at `:385`. |
| 26 | Consumes run envelopes, manifests, LangSmith NDJSON, downstream git trees | — | CONFIRMED | Validator inputs; `langsmith_fleet.py` consumes registry; maint-68 syncs consumer trees. |
| 27 | Sibling repos use incompatible ID formats (CSV columns, unaliased slugs, integer IDs) | `identity-map-conventions.md:44` | UNVERIFIABLE | Canonical format confirmed in Workflows docs; per-repo CSV/slug/UUID specifics require sibling clones (not present in this workspace). |

---

## Additional corrections applied outside §4/5/8/9 scope

| Area | Original | Corrected | Verdict |
|---|---|---|---|
| §1 purpose | 13 repos | 15 registered consumers | WRONG |
| §2 Gate cite | README:12 | README:108 | CITE-DRIFT |
| §2 Keepalive cite | README:43 | README:71,83 | CITE-DRIFT |
| §3/§7 test counts | 326 Python, 100+ JS | 327 Python, 92 JS | WRONG |
| §7 gap #3 cite | plan:52 | plan:65 + README:73 | CITE-DRIFT |
