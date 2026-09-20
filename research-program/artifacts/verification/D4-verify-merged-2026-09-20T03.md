# D4 implementation verification — 2026-09-20T03

Scope: the 20 oldest eligible, issue-linked PRs merged during the preceding 36 hours. Template-sync, dependency/release chores, and `stranske/Orchestrator` were excluded. Each verdict is based on the captured squash diff and linked issue acceptance criteria, with the PR's completed Gate/check evidence used only to confirm the named test gate ran.

| Repo | PR | Issue | Verdict | Evidence and unmet criteria | Follow-up |
|---|---:|---:|---|---|---|
| Trend_Model_Project | #6039 | #6020 | VERIFIED | `src/trend_analysis/util/weights.py` adds ambiguous-total handling; `tests/test_weights_utils.py` asserts positive, mixed-sign, zero, and non-finite cases. Named gate and executed break/revert evidence are present. | — |
| Trend_Model_Project | #6042 | #6023 | PARTIAL | Finite guards and `test_lambda_tc_rejects_non_finite` are in `src/trend_analysis/config/{model,models}.py` and `tests/test_config_turnover_validation.py`; Gate succeeded. The PR says removal *would* fail “by test design,” rather than recording the required executed break/revert. | #6046 |
| Trend_Model_Project | #6045 | #6026 | VERIFIED | `tests/test_golden_csv_tracking.py` asserts both the broad ignore and golden exception and checks Git's matching rule; executed removal/revert evidence is recorded. | — |
| Doc-Lineage | #22 | #15 | PARTIAL | `src/doc_lineage/export/docx_redline.py` and `tests/export/test_docx_redline_golden.py` provide a real renderer and assertions for Word insertion/deletion markup. The required disabled-markup break/revert is only a checked box, with no executed evidence. | #45 |
| Trend_Model_Project | #6041 | #6022 | VERIFIED | `tests/streamlit/conftest.py` adds teardown and `test_stub_reload_teardown.py` demonstrates the order-sensitive AppTest failure it prevents; the PR records the disabled-eviction break. | — |
| Doc-Lineage | #40 | #11 | VERIFIED | `src/doc_lineage/harvest/edgar_ex10.py`, offline filing fixtures, CLI wiring, and `test_parse_ex10_fixture` deliver/validate EX-10 harvest and manifest output. The PR records that filtering EX-10 items fails the named test. | — |
| Trend_Model_Project | #6043 | #6024 | PARTIAL | `pipeline_runner.py` stops swallowing `CoreConfigError`; `test_run_from_config_rejects_invalid_regime_turnover_cap` asserts failure before selection/weighting. No required fallback-restoration break/revert evidence appears. | #6047 |
| Trend_Model_Project | #6044 | #6025 | PARTIAL | Regime and pipeline helper guards reject string booleans/non-finite values and tests assert those paths. The required temporary guard-removal failure is not evidenced. | #6048 |
| Doc-Lineage | #41 | #12 | VERIFIED | Mutation catalog/materialization, fixtures, and `test_gate_provision_change_detected` are substantive; the diff also has a failure assertion for skipped catalog mutations and the PR records break/revert. | — |
| Workflows | #3467 | #3372 | VERIFIED | Adds mosaic-core schemas, fixtures, contract validation, and discriminating schema tests including required-field and traversal protection. Named gate and break evidence are present. | — |
| Doc-Lineage | #34 | #9 | VERIFIED | Evidence emitter, manifest linkage, and tests require `excerpt`, method, deterministic IDs, and schema validity. Named gate and executed omission/revert evidence are present. | — |
| Doc-Lineage | #39 | #5 | VERIFIED | Delivers data-driven segment classes/tiers, silence invariant, synthetic corpus, and tests for no false `DROPPED` classification. Both specified break gates are recorded. | — |
| Doc-Lineage | #42 | #13 | VERIFIED | Adds manifest-backed fact-key export/CLI and tests for ontology joins, identity rejection, and artifact integrity. Named gate and `entity_ref` break evidence are present. | — |
| Workflows | #3468 | #3374 | VERIFIED | Adds output-substrate schema, ingest mapping, fixture, and rejection tests for missing renderer profile/path violations. Named test and break evidence are present. | — |
| Workflows | #3469 | #3389 | VERIFIED | Diff adds a discriminating known-build-file regression; it asserts both accepted `Makefile` and rejected generic `file`. PR records 157 passing tests, coverage increase, and branch-removal failure. | — |
| Doc-Lineage | #43 | #5 | VERIFIED | Corrective follow-up to #39 keeps runtime/package catalog mirrors aligned and adds an explicit mirror-equality assertion; #39 already supplies the issue's original engine and acceptance coverage. | — |
| Manager-Mosaic | #35 | #8 | VERIFIED | `Issues.txt` removes template paths and the new test rejects `my_project`; the deliberate reintroduction/revert is recorded. | — |
| Manager-Mosaic | #36 | #10 | VERIFIED | Adds valid/invalid evidence-object fixtures and schema/consumer-CLI tests that require `excerpt`; named gate and omission/revert evidence are present. | — |
| Workflows | #3472 | #3373 | VERIFIED | Adds document-mirror schema, valid/invalid fixtures, validation CLI, and tests for content hashes, paths, URLs, and empty/local-only cases. Named gate and deliberate invalid-hash evidence are present. | — |
| Doc-Lineage | #44 | #14 | VERIFIED | Adds triple-link resolver, documented page/mirror/source-system links, schema-backed fixture, and tests requiring three hrefs. The missing-anchor mutation is recorded as fail then restore/pass. | — |

Result: 16 VERIFIED, 4 PARTIAL, 0 NOT IMPLEMENTED. The four follow-ups request acceptance-evidence capture only; no missing production behavior was found in their squash diffs.
