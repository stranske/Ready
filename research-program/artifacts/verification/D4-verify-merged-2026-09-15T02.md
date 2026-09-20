# Merged implementation verification — D4-verify-merged-2026-09-15T02

Run completed: 2026-09-15T02:25:42.753205+00:00. Window: 2026-09-13T14:12:35.907992Z through 2026-09-15T02:12:35.907992+00:00 (36 hours).

## Result

**18 issue-linked PRs reviewed: 12 VERIFIED, 6 PARTIAL, 0 NOT IMPLEMENTED.** Twenty candidate diffs were inspected; two turned out to reference PRs rather than issues and are excluded from implementation totals. No more than 20 PRs were inspected. Fourteen already-checkpointed PRs in the window were carried forward without re-review. Seventeen dependency/release/no-reference chores were skipped before inspection. One candidate, Workflows #3442, remains deferred by the inspection cap.

Three current gap groups need delivery attention: Workflows #3433 still lacks parts of its stated debounce contract; Ready #554 has open allowlist repair PR #574; Counter_Risk main fails Black on limits.py because PR and push formatting gates differ. Deliverable-Render #14 is historically partial but its merged #16 follow-up is verified.

No GitHub issue, comment, label, PR, or repository source was changed by this executor. The top-level research-only instruction overrides the brief's issue-filing instruction: **follow-up bodies are staged as files, zero filed**. The normal `program.py done` mirror publication is the authorized close operation.

## Method and limits

- Fresh fleet discovery from `SUPPORTED_REPOS` in handoff.sh: 15 repositories, excluding Orchestrator; 52 merged PRs returned, below each query's 100-result cap. Oldest-first candidate selection and one-second repository pacing; no secondary-rate-limit response.
- Reviewed `gh pr diff`, exact merged source snapshots, linked issue bodies, PR/issue owner comments, and named-gate wiring. Push-event CI was queried by full merge SHA. The generic check-run list is capped/noisy and is **not** treated as complete main-CI evidence.
- One successful Cursor advisory covered the first seven candidates. Parent independently checked key source, discarded false issue-link assumptions, corrected source line citations, and resolved two advisory PARTIALs with direct coverage and consumer commit evidence. Cursor's raw report is advisory, not the final ledger.
- Direct execution from exact merged snapshots: Workflows #3424 156 tests; #3440 60; #3443 174; #3444 308; Ready #569 169; Deliverable-Render #16 79 — **946 candidate tests passed**, plus 152 baseline tests for coverage comparison. Deliberate external-stylesheet injection failed two generated-output tests and restoration passed four. Other historical mutation results are explicitly attributed to retained PR evidence, not claimed as rerun here.
- No ledger-only PR occurred among selected candidates. Deliverable-Render #14 has a bootstrap title but eight substantive files; it is correctly treated as a partial implementation. No Workflows #3391 ledger defect was found in this scope.
- Workflows clone pull encountered a deleted upstream branch; exact SHA reads/fetches supplied source instead. Dirty Doc-Lineage/Portable clones were preserved and exact merged Git objects used. No runtime code changes or destructive cleanup.

## Verification table

| Repository | PR | Issue | Verdict | Unmet criteria | Follow-up filed / disposition |
|---|---|---|---|---|---|
| Workflows | [#3432](https://github.com/stranske/Workflows/pull/3432) | [#3431](https://github.com/stranske/Workflows/issues/3431) | **VERIFIED** | None within stated scope | 0 filed. None |
| Workflows | [#3436](https://github.com/stranske/Workflows/pull/3436) | [#3433](https://github.com/stranske/Workflows/issues/3433) | **PARTIAL** | Task-delta measurement, numeric refusal diagnostics, and named workflow gate remain missing; original exhaustion latch repaired by #3440. | 0 filed. Draft Workflows-3433-debounce.md; original issue remains open; #3435 is closed unmerged |
| Workflows | [#3439](https://github.com/stranske/Workflows/pull/3439) | [#3438](https://github.com/stranske/Workflows/issues/3438) | **VERIFIED** | None within stated scope | 0 filed. None |
| Workflows | [#3424](https://github.com/stranske/Workflows/pull/3424) | [#3389](https://github.com/stranske/Workflows/issues/3389) | **VERIFIED** | None within stated scope | 0 filed. None |
| Workflows | [#3440](https://github.com/stranske/Workflows/pull/3440) | [#3433](https://github.com/stranske/Workflows/issues/3433) | **PARTIAL** | Cooldown fix verified; original #3433 still lacks task-delta and named workflow acceptance. | 0 filed. Same draft Workflows-3433-debounce.md; no duplicate issue proposed |
| Ready | [#571](https://github.com/stranske/Ready/pull/571) | [#559](https://github.com/stranske/Ready/issues/559) | **VERIFIED** | None within stated scope | 0 filed. None |
| Counter_Risk | [#1069](https://github.com/stranske/Counter_Risk/pull/1069) | [#1061](https://github.com/stranske/Counter_Risk/issues/1061) | **PARTIAL** | Exact merged main CI fails formatting in limits.py despite green PR Gate. | 0 filed. Consolidated draft Counter_Risk-format-parity.md covering #1069 and #1071 |
| Doc-Lineage | [#23](https://github.com/stranske/Doc-Lineage/pull/23) | [#6](https://github.com/stranske/Doc-Lineage/issues/6) | **VERIFIED** | None within stated scope | 0 filed. None |
| Workflows | [#3445](https://github.com/stranske/Workflows/pull/3445) | [#1836](https://github.com/stranske/Workflows/issues/1836) | **VERIFIED** | None within stated scope | 0 filed. None |
| Ready | [#569](https://github.com/stranske/Ready/pull/569) | [#554](https://github.com/stranske/Ready/issues/554) | **PARTIAL** | Research-local default allowlist location unmet; repair #574 remains OPEN. | 0 filed. Existing Ready PR #574; Ready-554-existing-followup.md records the gap, no duplicate issue |
| Portable-Alpha-Extension-Model | [#2297](https://github.com/stranske/Portable-Alpha-Extension-Model/pull/2297) | [#2296](https://github.com/stranske/Portable-Alpha-Extension-Model/issues/2296) | **VERIFIED** | None within stated scope | 0 filed. None |
| Workflows | [#3451](https://github.com/stranske/Workflows/pull/3451) | [#3450](https://github.com/stranske/Workflows/issues/3450) | **VERIFIED** | None within stated scope | 0 filed. None |
| Deliverable-Render | [#14](https://github.com/stranske/Deliverable-Render/pull/14) | [#2](https://github.com/stranske/Deliverable-Render/issues/2) | **PARTIAL** | Grid source links and persisted fixture/golden acceptance were absent at this merge; now repaired by verified #16. | 0 filed. Existing merged #16; Deliverable-Render-2-resolved-followup.md; no new issue |
| Deliverable-Render | [#16](https://github.com/stranske/Deliverable-Render/pull/16) | [#2](https://github.com/stranske/Deliverable-Render/issues/2) | **VERIFIED** | None within stated scope | 0 filed. None |
| Counter_Risk | [#1071](https://github.com/stranske/Counter_Risk/pull/1071) | [#1062](https://github.com/stranske/Counter_Risk/issues/1062) | **PARTIAL** | Exact merged main CI fails inherited limits.py formatting; numerical acceptance is supported. | 0 filed. Same consolidated Counter_Risk-format-parity.md; no per-PR duplicate |
| Workflows | [#3443](https://github.com/stranske/Workflows/pull/3443) | [#3434](https://github.com/stranske/Workflows/issues/3434) | **VERIFIED** | None within stated scope | 0 filed. None |
| Workflows | [#3444](https://github.com/stranske/Workflows/pull/3444) | [#3441](https://github.com/stranske/Workflows/issues/3441) | **VERIFIED** | None within stated scope | 0 filed. None |
| Manager-Database | [#1677](https://github.com/stranske/Manager-Database/pull/1677) | [#1668](https://github.com/stranske/Manager-Database/issues/1668) | **VERIFIED** | None within stated scope | 0 filed. None |

## Criteria and evidence

### Workflows #3432 → #3431 — VERIFIED

Merge: `5740e81cabc3fe436cd6da476a567ba0b0e88f71`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34799141072).

- MET: all publishers with IDs and capabilities are returned; malformed entries are excluded and out-of-range timestamps cannot abort the catalog.
- MET: publisher parameterization and the real CLI test assert new candidates, exact output, and unchanged registry; no automatic promotion.
- MET: named test is present in tests/tools and full tests are wired in Selftest CI. PR retains 19-pass and six-failure publisher-filter mutation evidence.

Merged evidence: [tools/discover_model_catalog.py:64](https://github.com/stranske/Workflows/blob/5740e81cabc3fe436cd6da476a567ba0b0e88f71/tools/discover_model_catalog.py#L64); [tests/tools/test_discover_model_catalog.py:47](https://github.com/stranske/Workflows/blob/5740e81cabc3fe436cd6da476a567ba0b0e88f71/tests/tools/test_discover_model_catalog.py#L47); [tests/tools/test_discover_model_catalog.py:61](https://github.com/stranske/Workflows/blob/5740e81cabc3fe436cd6da476a567ba0b0e88f71/tests/tools/test_discover_model_catalog.py#L61).

### Workflows #3436 → #3433 — PARTIAL

Merge: `f65449d1d1b0074bb169792f30680fd47073762c`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34799823811).

- MET: explicit unproductive completion grants bounded retries on the same head, with non-vacuous should_dispatch assertions.
- NOT MET: workflow productivity measures only whether the head changed; it does not use completed-task delta or report prior commit/task counts on refusal.
- NOT MET at this merge: after the retry limit, refusal requires a new head commit. Merged #3440 later repairs that deadlock with a timed cooldown.
- NOT MET: issue-named tests/workflows/test_keepalive_dispatch_debounce.py and its required break/revert transcript are absent. Equivalent lower-level retry tests exist, but do not establish the workflow/task-delta contract.

Merged evidence: [.github/workflows/agents-keepalive-loop.yml:1091](https://github.com/stranske/Workflows/blob/f65449d1d1b0074bb169792f30680fd47073762c/.github/workflows/agents-keepalive-loop.yml#L1091); [scripts/runner_lib/core.py:1105](https://github.com/stranske/Workflows/blob/f65449d1d1b0074bb169792f30680fd47073762c/scripts/runner_lib/core.py#L1105); [tests/scripts/test_runner_lib.py:982](https://github.com/stranske/Workflows/blob/f65449d1d1b0074bb169792f30680fd47073762c/tests/scripts/test_runner_lib.py#L982).

### Workflows #3439 → #3438 — VERIFIED

Merge: `2b2bfd6754c608ca2d6b23169f77671990e97e5b`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34800484000).

- MET: best-effort AppArmor repair is scoped to workspace-write; a single same-model fallback shares network access while preserving filesystem confinement.
- MET: anchored real bwrap stderr forces exit 1; workflow-derived tests distinguish diagnostic lines from quoted JSON prose.
- MET: consumer runtime requirement has retained Codex work-log entries on Ready #569 and direct commit f96303e98878e291ddeefea0da97689f6dc19715, changing scanner and tests. This run fetched that commit; it did not rerun a consumer agent.
- MET: source owner disposition confirms both AC and no remaining blocker. Advisory PARTIAL was rejected because runtime evidence belongs outside the diff.

Merged evidence: [.github/workflows/reusable-codex-run.yml:956](https://github.com/stranske/Workflows/blob/2b2bfd6754c608ca2d6b23169f77671990e97e5b/.github/workflows/reusable-codex-run.yml#L956); [.github/workflows/reusable-codex-run.yml:1159](https://github.com/stranske/Workflows/blob/2b2bfd6754c608ca2d6b23169f77671990e97e5b/.github/workflows/reusable-codex-run.yml#L1159); [tests/workflows/test_codex_sandbox_startup_failure.py:123](https://github.com/stranske/Workflows/blob/2b2bfd6754c608ca2d6b23169f77671990e97e5b/tests/workflows/test_codex_sandbox_startup_failure.py#L123).

### Workflows #3424 → #3389 — VERIFIED

Merge: `3ecbe0ef73564827372ae9c44a8b4c163dbc8c08`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34805984472).

- MET: CLI regression exercises explicit argv, input file/stdin, Unicode path, cwd-sensitive addressability, failure output and valid-input controls.
- MET, measured this run: isolated merge snapshot 156 passed; parent snapshot 152 passed, same Python 3.12.2 and coverage configuration.
- MET: issue_format.py statement coverage rises from 272/283 (96.11%) to 280/283 (98.94%); branches 154/162 to 156/162. Source is unchanged. This is a scoped coverage increase, not a claim that the entire repo reached 90%.
- The advisory found absent historical coverage evidence; direct before/after execution supplies it. Fresh snapshots ran cleanly; no new follow-up is needed.

Merged evidence: [tests/scripts/test_issue_format.py:1000](https://github.com/stranske/Workflows/blob/3ecbe0ef73564827372ae9c44a8b4c163dbc8c08/tests/scripts/test_issue_format.py#L1000).

### Workflows #3440 → #3433 — PARTIAL

Merge: `a5908e2624eefd374d7582bbd600186a51ab54fe`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34807139851).

- MET for the narrow repair: exhausted retries enter a 30-minute cooldown that time alone drains; absent/unparseable timestamps permit redispatch and the counter is bounded.
- MET: tests cover expiry, a fresh cooldown after another zero-output run, and no head-commit drain requirement. This run: 60 runner-library tests passed. PR retains deliberate-break expiry failures and restoration.
- NOT MET for the full referenced issue #3433: task-delta productivity, numeric commit/task diagnostics, and the named workflow-level gate were not added. These inherited gaps must not be hidden by marking the cooldown patch sufficient for the whole issue.

Merged evidence: [scripts/runner_lib/core.py:1020](https://github.com/stranske/Workflows/blob/a5908e2624eefd374d7582bbd600186a51ab54fe/scripts/runner_lib/core.py#L1020); [scripts/runner_lib/core.py:1135](https://github.com/stranske/Workflows/blob/a5908e2624eefd374d7582bbd600186a51ab54fe/scripts/runner_lib/core.py#L1135); [tests/scripts/test_runner_lib.py:1026](https://github.com/stranske/Workflows/blob/a5908e2624eefd374d7582bbd600186a51ab54fe/tests/scripts/test_runner_lib.py#L1026); [docs/keepalive/GoalsAndPlumbing.md:302](https://github.com/stranske/Workflows/blob/a5908e2624eefd374d7582bbd600186a51ab54fe/docs/keepalive/GoalsAndPlumbing.md#L302).

### Ready #571 → #559 — VERIFIED

Merge: `4107431ed0b1a503c2e504fa5a25c153e4fb47f6`. [CI success](https://github.com/stranske/Ready/actions/runs/34820466890).

- MET: both provider implementations retain one output slot per input; local blanks receive zero vectors and OpenAI nonblank embeddings are reconstructed at original indices.
- MET: tests assert exact positions, vector dimensions, all-blank and empty input, iterator behavior, and SDK call filtering. The local-fallback one-liner follows the same path.
- MET: CI runs tests/test_main.py; PR retains 10 passing tests, four failing alignment mutations, byte restoration and the one-liner success. Blank-only OpenAI responses have unknown dimensions and empty vectors, explicitly tested rather than fabricated dimensions.

Merged evidence: [tools/embedding_provider.py:166](https://github.com/stranske/Ready/blob/4107431ed0b1a503c2e504fa5a25c153e4fb47f6/tools/embedding_provider.py#L166); [tools/embedding_provider.py:251](https://github.com/stranske/Ready/blob/4107431ed0b1a503c2e504fa5a25c153e4fb47f6/tools/embedding_provider.py#L251); [tests/test_main.py:70](https://github.com/stranske/Ready/blob/4107431ed0b1a503c2e504fa5a25c153e4fb47f6/tests/test_main.py#L70).

### Counter_Risk #1069 → #1061 — PARTIAL

Merge: `9c6cd8962536c7d1159e5d45c2a0d36b919322c4`. [CI failure](https://github.com/stranske/Counter_Risk/actions/runs/34827221311).

- MET: both check_limits and find_missing_limit_entities resolve registered counterparty aliases through one canonical helper; unknown/non-counterparty behavior is preserved.
- MET: named regression uses the production _build_limit_exposure_rows boundary, asserts exposure 200, breach 100, fail severity, alias/canonical equality, and unknown-name control.
- MET: retained comment 5661630984 reports 44 passes, alias-resolution and production-reshaper mutations each failing, then restored pass.
- NOT MET for overall completion validation: exact merge CI 34827221311 fails Black on the changed src/counter_risk/compute/limits.py. The PR Gate explicitly disables format_check while push CI enables the reusable default. Numerical tests pass; this is a format/gate-parity defect.

Merged evidence: [src/counter_risk/compute/limits.py:93](https://github.com/stranske/Counter_Risk/blob/9c6cd8962536c7d1159e5d45c2a0d36b919322c4/src/counter_risk/compute/limits.py#L93); [tests/compute/test_limits.py:502](https://github.com/stranske/Counter_Risk/blob/9c6cd8962536c7d1159e5d45c2a0d36b919322c4/tests/compute/test_limits.py#L502); [.github/workflows/pr-00-gate.yml:73](https://github.com/stranske/Counter_Risk/blob/9c6cd8962536c7d1159e5d45c2a0d36b919322c4/.github/workflows/pr-00-gate.yml#L73).

### Doc-Lineage #23 → #6 — VERIFIED

Merge: `8f4b97535571b70a1bdfffaeb18efbcdcdff7317`. [CI success](https://github.com/stranske/Doc-Lineage/actions/runs/34840191817).

- MET: versioned legal-clause vocabulary has 25 keys, canonical metadata, sources, dotted identifiers and a production loader. README points to the vocabulary.
- MET: named test invokes the loader and checks count >=20, uniqueness and key pattern; duplicate-map-key parsing fails explicitly.
- MET: packaged resources take precedence; installed-wheel test deletes its checkout and checks both clean and adjacent-decoy layouts without mocking lookup.
- MET: generated egg-info and old bootstrap marker are removed and ignored. Owner adversarial corrections are addressed by actual source and subsequent acceptance disposition.
- MET: source comment 5663197340 retains 26 suite passes, 17/17 empty-loader mutation failures, duplicate-key and source-first precedence failures, then restored passes; exact merge CI is successful.

Merged evidence: [src/doc_lineage/vocab.py:19](https://github.com/stranske/Doc-Lineage/blob/8f4b97535571b70a1bdfffaeb18efbcdcdff7317/src/doc_lineage/vocab.py#L19); [tests/vocab/test_legal_clauses.py:33](https://github.com/stranske/Doc-Lineage/blob/8f4b97535571b70a1bdfffaeb18efbcdcdff7317/tests/vocab/test_legal_clauses.py#L33); [tests/vocab/test_legal_clauses.py:80](https://github.com/stranske/Doc-Lineage/blob/8f4b97535571b70a1bdfffaeb18efbcdcdff7317/tests/vocab/test_legal_clauses.py#L80); [vocab/legal-clauses.json:20](https://github.com/stranske/Doc-Lineage/blob/8f4b97535571b70a1bdfffaeb18efbcdcdff7317/vocab/legal-clauses.json#L20).

### Workflows #3445 → #1836 — VERIFIED

Merge: `3706dc2fd51b77e87902ddfe508f06b81b83e8fc`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34855835879).

- MET for this supporting source repair: explicit None narrowing replaces bool(prior) so the optional mapping is type-safe without changing behavior.
- MET: parametrized cases cover None, empty mappings, true/false, missing productivity, and false-looking non-booleans.
- #1836 is a durable campaign tracker, not a closable implementation spec. No whole-campaign completion is claimed; the PR is a substantive source typing fix, not a generated dependency delivery.

Merged evidence: [scripts/runner_lib/core.py:1042](https://github.com/stranske/Workflows/blob/3706dc2fd51b77e87902ddfe508f06b81b83e8fc/scripts/runner_lib/core.py#L1042); [tests/scripts/test_runner_lib.py:986](https://github.com/stranske/Workflows/blob/3706dc2fd51b77e87902ddfe508f06b81b83e8fc/tests/scripts/test_runner_lib.py#L986).

### Ready #569 → #554 — PARTIAL

Merge: `2dd52d56932de83b4f0f5c02c4274802ebd7dd31`. [CI success](https://github.com/stranske/Ready/actions/runs/34862160309); [Publication guard success](https://github.com/stranske/Ready/actions/runs/34862159566).

- MET: byte scanner reports each location/rule without matched contents, all per-rule zero counts, and files scanned; missing/empty trees, invalid policies, links and unreadable inputs fail.
- MET: shared PEM patterns cover the expanded header family; tests cover encoded JSON, source preservation/read counts and binary guard behavior. This run: 169 focused tests passed.
- MET: required Gate unconditionally depends on publication-safety and rejects non-success even when Python skips; push Publication guard and CI both pass.
- MET: later owner requirement allows accurately documenting preparation as an operator staging step. README does so; CI is not claimed to auto-redact.
- NOT MET: resolve_allowlist defaults to root.parent/.publication-allow, so the requested research-program/.publication-allow is not honored. Existing open #574 is the concrete repair. Its current state was fetched; it is not counted as merged or verified.

Merged evidence: [scripts/check_publication_safety.py:29](https://github.com/stranske/Ready/blob/2dd52d56932de83b4f0f5c02c4274802ebd7dd31/scripts/check_publication_safety.py#L29); [scripts/check_publication_safety.py:155](https://github.com/stranske/Ready/blob/2dd52d56932de83b4f0f5c02c4274802ebd7dd31/scripts/check_publication_safety.py#L155); [.github/workflows/pr-00-gate.yml:88](https://github.com/stranske/Ready/blob/2dd52d56932de83b4f0f5c02c4274802ebd7dd31/.github/workflows/pr-00-gate.yml#L88); [tests/test_publication_safety.py:230](https://github.com/stranske/Ready/blob/2dd52d56932de83b4f0f5c02c4274802ebd7dd31/tests/test_publication_safety.py#L230); [tests/test_prepare_publication.py:151](https://github.com/stranske/Ready/blob/2dd52d56932de83b4f0f5c02c4274802ebd7dd31/tests/test_prepare_publication.py#L151).

### Portable-Alpha-Extension-Model #2297 → #2296 — VERIFIED

Merge: `086de8b946df86f01f3f09ef4f594bce86064d75`. [CI success](https://github.com/stranske/Portable-Alpha-Extension-Model/actions/runs/34883178073).

- MET: four cases exercise both public allocation searches with repeated infeasible/duplicate random draws, real allocation enumeration and independent feasible-grid oracle.
- MET: output/evaluation counts, uniqueness, feasibility and capital conservation are asserted for budgets below/above the feasible count; simulation/random draws alone are controlled.
- MET: retained same-environment full-suite statement coverage rises 435/635 to 516/635 in the module; focused test-file scope rises 216/635 to 386/635. These are distinct denominators/scopes.
- MET: disabling fallback or deduplication causes all four cases to fail; restoration gives seven test-file passes. The issue literal filesystem --cov selector yields no data, so the recorded module-selector measurement is the valid evidence. No whole-project 90% claim.

Merged evidence: [tests/test_sleeve_frontier.py:14](https://github.com/stranske/Portable-Alpha-Extension-Model/blob/086de8b946df86f01f3f09ef4f594bce86064d75/tests/test_sleeve_frontier.py#L14); [tests/test_sleeve_frontier.py:75](https://github.com/stranske/Portable-Alpha-Extension-Model/blob/086de8b946df86f01f3f09ef4f594bce86064d75/tests/test_sleeve_frontier.py#L75).

### Workflows #3451 → #3450 — VERIFIED

Merge: `c8561288b546c9ab6beb3d318336b7b30c36d8d0`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34887778302).

- MET: metadata observers cannot churn status URLs; dependency-contract conclusions remain visible without self-observing URLs.
- MET: bounded exact-head Gate recovery survives a flooded recent page; wrong/missing heads cannot report success and non-404 API errors propagate.
- MET: executable idempotence tests assert stable bytes, real Gate transitions, missing evidence, rate-limit propagation and template-related behavior. Source/template helper bytes match.
- MET: retained post-merge comment 5669732801 records unchanged FAA #723 head with stable body from 19:35:55Z to 19:38:02Z, across more than two former churn cycles. This supports the bounded runtime AC, not indefinite stability or FAA issue acceptance.

Merged evidence: [.github/scripts/agents_pr_meta_update_body.js:967](https://github.com/stranske/Workflows/blob/c8561288b546c9ab6beb3d318336b7b30c36d8d0/.github/scripts/agents_pr_meta_update_body.js#L967); [.github/scripts/__tests__/agents-pr-meta-status-idempotence.test.js:74](https://github.com/stranske/Workflows/blob/c8561288b546c9ab6beb3d318336b7b30c36d8d0/.github/scripts/__tests__/agents-pr-meta-status-idempotence.test.js#L74); [.github/scripts/__tests__/agents-pr-meta-contract-status.test.js:33](https://github.com/stranske/Workflows/blob/c8561288b546c9ab6beb3d318336b7b30c36d8d0/.github/scripts/__tests__/agents-pr-meta-contract-status.test.js#L33).

### Deliverable-Render #14 → #2 — PARTIAL

Merge: `e2ac49f36be9628ada5d9c30081fe11a0f7490ce`. [CI success](https://github.com/stranske/Deliverable-Render/actions/runs/34890535922).

- MET: structured records/evidence/documents, JSON/SQLite loading, entity/period indexes, offline HTML, configurable list-view source links and dangling-reference errors are implemented.
- NOT MET at this merge: grid cards contain text without source anchors; synthetic store/golden HTML files and tests/test_render_html_offline.py are absent.
- Existing merged follow-up #16 supplies these missing artifacts and grid links. The misleading bootstrap title does not make this a ledger-only commit; its eight-file diff is substantive but incomplete.

Merged evidence: [src/deliverable_render/html.py:35](https://github.com/stranske/Deliverable-Render/blob/e2ac49f36be9628ada5d9c30081fe11a0f7490ce/src/deliverable_render/html.py#L35); [src/deliverable_render/store.py:189](https://github.com/stranske/Deliverable-Render/blob/e2ac49f36be9628ada5d9c30081fe11a0f7490ce/src/deliverable_render/store.py#L189).

### Deliverable-Render #16 → #2 — VERIFIED

Merge: `da795c067565a4a8f6b1cd20da32a4e88d953530`. [CI success](https://github.com/stranske/Deliverable-Render/actions/runs/34896196226).

- MET: explicit list/grid selection produces one source anchor per evidence pointer; grid cards use the same resolved document links and missing documents raise a named error.
- MET: persisted synthetic JSON plus separate list/grid goldens are compared by parsed structure. Static markup contains all rows without executing JavaScript.
- MET: local and document-system modes differ only by link prefix; remote anchors are navigation, not fetched resources. Generated/local golden output has no HTTP resource references.
- MET: this run 79 store/HTML/offline tests pass. In-memory external-stylesheet injection causes the generated list/grid resource tests to fail (2 failed, 2 persisted controls passed); restoration gives 4 passes. No repository source file was modified.
- Owner follow-up confirms #14 deficiencies repaired. Baseline/browser support is documented; no actual work-environment browser session was performed.

Merged evidence: [src/deliverable_render/html.py:124](https://github.com/stranske/Deliverable-Render/blob/da795c067565a4a8f6b1cd20da32a4e88d953530/src/deliverable_render/html.py#L124); [src/deliverable_render/html.py:202](https://github.com/stranske/Deliverable-Render/blob/da795c067565a4a8f6b1cd20da32a4e88d953530/src/deliverable_render/html.py#L202); [tests/test_render_html_offline.py:61](https://github.com/stranske/Deliverable-Render/blob/da795c067565a4a8f6b1cd20da32a4e88d953530/tests/test_render_html_offline.py#L61); [tests/test_render_html_offline.py:122](https://github.com/stranske/Deliverable-Render/blob/da795c067565a4a8f6b1cd20da32a4e88d953530/tests/test_render_html_offline.py#L122).

### Counter_Risk #1071 → #1062 — PARTIAL

Merge: `215978393d213ce5a3bdc0ff48f9647c43b5569e`. [CI failure](https://github.com/stranske/Counter_Risk/actions/runs/34899128332).

- MET: concentration groups sum gross magnitudes by counterparty before Top5/Top10/HHI; anonymous rows remain independent and custom grouping is supported.
- MET: production reshaper regressions compare split/consolidated exposures, mixed signs, zero/near-zero totals and a valid control, with explicit expected metric values.
- MET: comment 5671057375 retains 44 passes, pre-fix source mutation (2 failures/3 controls passing), then all five named cases passing after restoration.
- NOT MET for overall completion validation: exact merge CI 34899128332 fails Black on limits.py inherited from #1069. This is the same existing format-parity defect, not a newly introduced concentration error.

Merged evidence: [src/counter_risk/compute/rollups.py:596](https://github.com/stranske/Counter_Risk/blob/215978393d213ce5a3bdc0ff48f9647c43b5569e/src/counter_risk/compute/rollups.py#L596); [tests/compute/test_concentration_metrics.py:495](https://github.com/stranske/Counter_Risk/blob/215978393d213ce5a3bdc0ff48f9647c43b5569e/tests/compute/test_concentration_metrics.py#L495); [.github/workflows/pr-00-gate.yml:73](https://github.com/stranske/Counter_Risk/blob/215978393d213ce5a3bdc0ff48f9647c43b5569e/.github/workflows/pr-00-gate.yml#L73).

### Workflows #3443 → #3434 — VERIFIED

Merge: `3e1d15ca52bf9fde9437a6706f4cf888f52b6341`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34901143910).

- MET: root/consumer evaluators count only failed or timed-out Gate attempts with actual failed jobs; reruns of one run ID are individually inspected.
- MET: jobless current failures return before writing autofix:escalated; genuine failures retain escalation and report examined/failed attempt counts.
- MET: root/consumer basic autofix recognizes timed_out and excludes cancelled/skipped. Intended wrapper differences are explicitly retained in drift fingerprints.
- MET: this run 174 workflow-derived cases pass, including cancelled-only histories, same-run repeated attempts, jobless escalation ordering, timeout eligibility and injected mutation detection. Named gate is wired into Selftest CI.
- Owner review-followup concerns are addressed in actual code and later thread-specific disposition; retained PR evidence includes literal commands and failure/restoration results.

Merged evidence: [.github/workflows/agents-autofix-loop.yml:560](https://github.com/stranske/Workflows/blob/3e1d15ca52bf9fde9437a6706f4cf888f52b6341/.github/workflows/agents-autofix-loop.yml#L560); [.github/workflows/agents-autofix-loop.yml:690](https://github.com/stranske/Workflows/blob/3e1d15ca52bf9fde9437a6706f4cf888f52b6341/.github/workflows/agents-autofix-loop.yml#L690); [tests/workflows/test_autofix_cancelled_gate.py:283](https://github.com/stranske/Workflows/blob/3e1d15ca52bf9fde9437a6706f4cf888f52b6341/tests/workflows/test_autofix_cancelled_gate.py#L283); [tests/workflows/test_autofix_cancelled_gate.py:538](https://github.com/stranske/Workflows/blob/3e1d15ca52bf9fde9437a6706f4cf888f52b6341/tests/workflows/test_autofix_cancelled_gate.py#L538).

### Workflows #3444 → #3441 — VERIFIED

Merge: `4da3c7426ce55a2147eafdee306d3c71e0078de1`. [Selftest CI success](https://github.com/stranske/Workflows/actions/runs/34905589741).

- MET: dispatch, running-state focus and live progress use visible outside-summary tasks; outstanding work prevents a tasks-complete result and removes stale automerge authorization.
- MET: prefix reviewer tasks survive metadata regeneration; known template choices, fenced examples and comments are excluded without eating later visible tasks.
- MET: fence state is recognized before comment/template-control processing, covering the owner counterexample; root and all three consumer helper copies match.
- MET: source issue remains task of record and refresh timing is documented. This run 308 parser/metadata/keepalive tests pass; retained comment 5672188235 identifies original summary-only, fenced-comment and fenced-template mutations with restored passes.

Merged evidence: [.github/scripts/issue_scope_parser.js:15](https://github.com/stranske/Workflows/blob/4da3c7426ce55a2147eafdee306d3c71e0078de1/.github/scripts/issue_scope_parser.js#L15); [.github/scripts/issue_scope_parser.js:56](https://github.com/stranske/Workflows/blob/4da3c7426ce55a2147eafdee306d3c71e0078de1/.github/scripts/issue_scope_parser.js#L56); [.github/scripts/keepalive_loop.js:1476](https://github.com/stranske/Workflows/blob/4da3c7426ce55a2147eafdee306d3c71e0078de1/.github/scripts/keepalive_loop.js#L1476); [.github/scripts/keepalive_loop.js:3466](https://github.com/stranske/Workflows/blob/4da3c7426ce55a2147eafdee306d3c71e0078de1/.github/scripts/keepalive_loop.js#L3466); [docs/keepalive/GoalsAndPlumbing.md:221](https://github.com/stranske/Workflows/blob/4da3c7426ce55a2147eafdee306d3c71e0078de1/docs/keepalive/GoalsAndPlumbing.md#L221).

### Manager-Database #1677 → #1668 — VERIFIED

Merge: `f5aa6d84f6471028dac6bd99b9d0993f59a9849c`. [CI success](https://github.com/stranske/Manager-Database/actions/runs/34913834671).

- MET: holdings_as_of orders by filed date, normalized amendment flag, then numeric ID, preserving no-type schemas and existing knowledge-time visibility filtering.
- MET: shared inverted-ID fixture asserts ORIGINAL before the amendment becomes known and AMENDED afterward, with tuple/mapping cursors and cross-selector agreement.
- MET: equal-type ID ordering, latest-filed-date precedence, normalized type and no-type legacy controls remain protected.
- MET: retained comment 5672102879 reports 29 selector passes, 14 backtest passes, exact ID-only mutation producing two failures, then restoration; merge CI succeeds including the repository integration topology.

Merged evidence: [etl/point_in_time.py:103](https://github.com/stranske/Manager-Database/blob/f5aa6d84f6471028dac6bd99b9d0993f59a9849c/etl/point_in_time.py#L103); [etl/point_in_time.py:138](https://github.com/stranske/Manager-Database/blob/f5aa6d84f6471028dac6bd99b9d0993f59a9849c/etl/point_in_time.py#L138); [tests/test_bitemporal_holdings.py:253](https://github.com/stranske/Manager-Database/blob/f5aa6d84f6471028dac6bd99b9d0993f59a9849c/tests/test_bitemporal_holdings.py#L253); [tests/test_diff_holdings.py:523](https://github.com/stranske/Manager-Database/blob/f5aa6d84f6471028dac6bd99b9d0993f59a9849c/tests/test_diff_holdings.py#L523).

## Exclusions and continuation

- Workflows #3425 references PR #3351, and #3437 references PR #3354 plus a consumer delivery PR. `gh issue view` accepts PR numbers; its returned `/pull/` URLs proved these were not linked issues. Both diffs were read before exclusion, so they still consume the conservative 20-inspection budget. They are not falsely counted VERIFIED implementation work.
- Workflows #3442 (merged 2026-09-15T01:33:20Z) is the oldest remaining unreviewed candidate at the cutoff. Resume there if it remains inside the next run's window.
- The inherited September 14 ledger supplies 14 already-reviewed in-window records. These are **not** current-run verified totals. Complete inventory, skip decisions, exact-SHA files, comments, CI evidence and adjudication are in this unit's evidence directory.

## Follow-up files

All files are research-only handoffs; they have not been filed. Recheck existing issue/PR ownership before publication.

- `followups/D4-verify-merged-2026-09-15T02/Workflows-3433-debounce.md`: one consolidated body for remaining original issue requirements across #3436/#3440; original #3433 is open and prior #3435 is closed unmerged.
- `followups/D4-verify-merged-2026-09-15T02/Counter_Risk-format-parity.md`: one consolidated body for the same limits.py/Black failure across #1069/#1071.
- `followups/D4-verify-merged-2026-09-15T02/Ready-554-existing-followup.md`: track existing open #574; do not duplicate it.
- `followups/D4-verify-merged-2026-09-15T02/Deliverable-Render-2-resolved-followup.md`: historical gap closed by verified merged #16; no new issue needed.

## Close and publication status

`program.py done` completed at 2026-09-15T02:27:13Z; the local queue records this unit as done and STATUS.md is rebuilt. Mirror publication was **deferred**, not confirmed remote: the existing Ready #570 closer lease was created at 02:27:01Z and expires by 2026-09-15T04:27:01.035503+00:00. The engine honors that hold so strict-base review can finish. No lease was cleared or bypassed. The report and follow-up files remain ready for the engine's next permitted mirror push. UTC hour is 02, so digest is not due.
